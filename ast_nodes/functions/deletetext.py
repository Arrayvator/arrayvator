# ast_nodes/functions/deletetext.py
"""
Функции удаления символов слева/справа: deletetextleft, deletetextright.

СИНТАКСИС:
    deletetextleft("PR-001", 3)          # "001"
    deletetextright("PR-001", 2)         # "PR-"

    deletetextleft(s[:, "Код"], 4)
    deletetextright(s[:, "Город"], 2)

DUCKDB:
    - Если данные в DuckDBTable → SQL SUBSTRING через * REPLACE
    - Возвращает новый DuckDBTable (view)
    - Столбец остаётся на своём месте

Matrix:
    - m[:, "X"]      → вектор
    - m[:, 2:5]      → матрица
    - m              → матрица
    - скаляр         → скаляр
"""

from ..base import Node
from runtime.matrix import MatrExMatrix
from ..utils.index_utils import parse_range_spec, resolve_column_index


def _is_duckdb(val):
    try:
        from duckdb_engine import DuckDBTable
        return isinstance(val, DuckDBTable)
    except ImportError:
        return False


# ============================================================
# УДАЛЕНИЕ СИМВОЛОВ (для RAM)
# ============================================================
def _delete_left_single(value, count):
    """Удаляет count символов слева. Если всё удалено → None."""
    if value is None:
        return None
    str_val = str(value)
    if len(str_val) <= count:
        return None
    return str_val[count:]


def _delete_right_single(value, count):
    """Удаляет count символов справа. Если всё удалено → None."""
    if value is None:
        return None
    str_val = str(value)
    if len(str_val) <= count:
        return None
    return str_val[:-count]


# ============================================================
# ИЗВЛЕЧЕНИЕ DUCKDBTABLE И СТОЛБЦА
# ============================================================
def _extract_duckdb_column(index_node, env):
    from ast_nodes.index import IndexNode

    if not isinstance(index_node, IndexNode):
        return (None, None)

    if len(index_node.indices) != 2:
        return (None, None)

    try:
        matrix_obj = index_node.matrix.evaluate(env)
    except Exception:
        return (None, None)

    if not _is_duckdb(matrix_obj):
        return (None, None)

    col_spec_node = index_node.indices[1]
    col_spec = (col_spec_node.evaluate(env)
                if hasattr(col_spec_node, 'evaluate')
                else col_spec_node)

    from .filterif import _resolve_column_for_duckdb
    columns = matrix_obj.get_columns()
    col_idx = _resolve_column_for_duckdb(columns, col_spec)

    if 0 <= col_idx < len(columns):
        return (matrix_obj, columns[col_idx])

    return (None, None)


# ============================================================
# DUCKDB: DELETETEXTLEFT через * REPLACE
# ============================================================
def _deletetextleft_duckdb(duck_table, col_name, count):
    from duckdb_engine import DuckDBTable
    import uuid

    safe_col = '"' + str(col_name).replace('"', '""') + '"'
    n = int(count)

    value_expr = f"SUBSTRING(CAST({safe_col} AS VARCHAR), {n + 1})"

    new_name = f"dtl_{uuid.uuid4().hex[:8]}"
    sql = f"""
        CREATE OR REPLACE VIEW {new_name} AS
        SELECT * REPLACE (
            {value_expr} AS {safe_col}
        )
        FROM {duck_table.table_name}
    """

    try:
        duck_table.con.execute(sql)
    except Exception as e:
        raise RuntimeError(f"Ошибка deletetextleft: {e}\nSQL: {sql}")

    new_table = DuckDBTable.__new__(DuckDBTable)
    new_table.path = duck_table.path
    new_table.table_name = new_name
    new_table.con = duck_table.con
    new_table.utf8_path = duck_table.utf8_path
    new_table.is_temp = False
    new_table._tmp_path = None

    return new_table


# ============================================================
# DUCKDB: DELETETEXTRIGHT через * REPLACE
# ============================================================
def _deletetextright_duckdb(duck_table, col_name, count):
    from duckdb_engine import DuckDBTable
    import uuid

    safe_col = '"' + str(col_name).replace('"', '""') + '"'
    n = int(count)

    value_expr = (
        f"SUBSTRING(CAST({safe_col} AS VARCHAR), 1, "
        f"LENGTH(CAST({safe_col} AS VARCHAR)) - {n})"
    )

    new_name = f"dtr_{uuid.uuid4().hex[:8]}"
    sql = f"""
        CREATE OR REPLACE VIEW {new_name} AS
        SELECT * REPLACE (
            {value_expr} AS {safe_col}
        )
        FROM {duck_table.table_name}
    """

    try:
        duck_table.con.execute(sql)
    except Exception as e:
        raise RuntimeError(f"Ошибка deletetextright: {e}\nSQL: {sql}")

    new_table = DuckDBTable.__new__(DuckDBTable)
    new_table.path = duck_table.path
    new_table.table_name = new_name
    new_table.con = duck_table.con
    new_table.utf8_path = duck_table.utf8_path
    new_table.is_temp = False
    new_table._tmp_path = None

    return new_table


# ============================================================
# АНАЛИЗ СРЕЗА МАТРИЦЫ
# ============================================================
def _analyze_matrix_index(index_node, env):
    if not hasattr(index_node, 'indices'):
        return None
    if len(index_node.indices) != 2:
        return None

    matrix_obj = index_node.matrix.evaluate(env)
    if not hasattr(matrix_obj, 'data') or not matrix_obj.is_2d:
        return None

    row_spec_node = index_node.indices[0]
    row_spec = (row_spec_node.evaluate(env)
                if hasattr(row_spec_node, 'evaluate')
                else row_spec_node)

    row_start, row_end = parse_range_spec(row_spec, matrix_obj.rows, is_column=False)

    is_explicit = False
    if isinstance(row_spec, str) and row_spec.strip().lower() not in (':', 'all'):
        is_explicit = True
    elif isinstance(row_spec, (int, float)):
        is_explicit = True

    col_spec_node = index_node.indices[1]
    col_spec = (col_spec_node.evaluate(env)
                if hasattr(col_spec_node, 'evaluate')
                else col_spec_node)

    col_info = None
    skip_header = False

    if isinstance(col_spec, str):
        s = col_spec.strip().lower()

        if s in (':', 'all'):
            col_info = (1, matrix_obj.cols)
        elif s == 'end':
            col_info = (matrix_obj.cols, matrix_obj.cols)
        elif s.startswith('end-'):
            try:
                n = int(s[4:].strip())
                idx = matrix_obj.cols - n
                if idx < 1:
                    idx = 1
                col_info = (idx, idx)
            except Exception:
                col_info = (1, matrix_obj.cols)
        elif s.startswith('last'):
            rest = s[4:].strip()
            try:
                n = int(rest)
                if n == 1:
                    col_info = (matrix_obj.cols, matrix_obj.cols)
                else:
                    col_info = (matrix_obj.cols - n + 1, matrix_obj.cols)
            except Exception:
                col_info = (1, matrix_obj.cols)
        elif ':' in s:
            col_start, col_end = parse_range_spec(s, matrix_obj.cols, is_column=True)
            col_info = (col_start, col_end)
        else:
            idx, skip_header = resolve_column_index(matrix_obj, col_spec, env)
            col_info = (idx + 1, idx + 1)
    elif isinstance(col_spec, (int, float)):
        n = int(col_spec)
        if n < 1 or n > matrix_obj.cols:
            n = matrix_obj.cols
        col_info = (n, n)
    else:
        col_info = (1, matrix_obj.cols)

    if not is_explicit and skip_header:
        row_start = max(row_start, 2)

    return (matrix_obj, row_start, row_end, col_info)


# ============================================================
# БАЗОВЫЙ КЛАСС
# ============================================================
class _DeleteTextBase(Node):
    """Базовый класс для deletetextleft / deletetextright."""

    _name = "deletetext"

    def __init__(self, data, count, column=None, row=None):
        self.data = data
        self.count = count
        self.column = column
        self.row = row

    def _delete_single(self, value, count):
        raise NotImplementedError

    def evaluate(self, env):
        from ast_nodes.index import IndexNode

        count_val = (self.count.evaluate(env)
                     if hasattr(self.count, 'evaluate')
                     else self.count)

        if not isinstance(count_val, (int, float)):
            raise TypeError(
                f"Количество символов должно быть числом, "
                f"получен {type(count_val)}"
            )

        count_int = int(count_val)
        if count_int < 0:
            raise ValueError(
                f"Количество символов не может быть отрицательным: {count_int}"
            )

        # DUCKDB
        duck_table, col_name = _extract_duckdb_column(self.data, env)
        if duck_table is not None:
            if self._name == "deletetextleft":
                return _deletetextleft_duckdb(duck_table, col_name, count_int)
            else:
                return _deletetextright_duckdb(duck_table, col_name, count_int)

        # СРЕЗ МАТРИЦЫ (RAM)
        analysis = _analyze_matrix_index(self.data, env)
        if analysis is not None:
            matrix_obj, row_start, row_end, col_info = analysis
            col_start, col_end = col_info

            # ============================================================
            # ОДНА ЯЧЕЙКА → скаляр
            # ============================================================
            if row_start == row_end and col_start == col_end:
                i = row_start - 1
                j = col_start - 1
                if i < len(matrix_obj.data) and j < len(matrix_obj.data[i]):
                    return self._delete_single(
                        matrix_obj.data[i][j], count_int
                    )
                return None

            # ============================================================
            # ОДИН СТОЛБЕЦ → вектор
            # ============================================================
            if col_start == col_end:
                c_idx = col_start - 1
                result = []
                for i in range(row_start - 1, row_end):
                    if i < len(matrix_obj.data):
                        row = matrix_obj.data[i]
                        if c_idx < len(row):
                            result.append(
                                self._delete_single(row[c_idx], count_int)
                            )
                        else:
                            result.append(None)
                    else:
                        result.append(None)
                return MatrExMatrix(result, False)

            # ============================================================
            # НЕСКОЛЬКО СТОЛБЦОВ → матрица
            # ============================================================
            result_data = [row.copy() if isinstance(row, list) else [row]
                           for row in matrix_obj.data]

            for i in range(row_start - 1, row_end):
                if i >= len(result_data):
                    continue
                row = result_data[i]
                for j in range(col_start - 1, col_end):
                    if j < len(row):
                        row[j] = self._delete_single(row[j], count_int)

            return MatrExMatrix(result_data, True)

        # СРЕЗ ВЕКТОРА
        if isinstance(self.data, IndexNode) and len(self.data.indices) == 1:
            vector_obj = self.data.matrix.evaluate(env)
            if hasattr(vector_obj, 'data') and not vector_obj.is_2d:
                idx_spec_node = self.data.indices[0]
                idx_spec = (idx_spec_node.evaluate(env)
                            if hasattr(idx_spec_node, 'evaluate')
                            else idx_spec_node)
                start, end = parse_range_spec(idx_spec, len(vector_obj.data), is_column=False)

                if start == end:
                    i = start - 1
                    if 0 <= i < len(vector_obj.data):
                        return self._delete_single(
                            vector_obj.data[i], count_int
                        )
                    return None

                result_data = list(vector_obj.data)
                for i in range(start - 1, end):
                    if i < len(result_data):
                        result_data[i] = self._delete_single(result_data[i], count_int)

                return MatrExMatrix(result_data, False)

        # ОБЫЧНЫЙ РЕЖИМ
        data_obj = self.data.evaluate(env)

        if hasattr(data_obj, 'data') and data_obj.is_2d:
            result_data = []
            for row in data_obj.data:
                new_row = [self._delete_single(v, count_int) for v in row]
                result_data.append(new_row)
            return MatrExMatrix(result_data, True)

        if hasattr(data_obj, 'data') and not data_obj.is_2d:
            result_data = [self._delete_single(v, count_int)
                           for v in data_obj.data]
            return MatrExMatrix(result_data, False)

        if isinstance(data_obj, (int, float, str)):
            return self._delete_single(data_obj, count_int)

        if isinstance(data_obj, list):
            if data_obj and isinstance(data_obj[0], list):
                result_data = []
                for row in data_obj:
                    new_row = [self._delete_single(v, count_int) for v in row]
                    result_data.append(new_row)
                return MatrExMatrix(result_data, True)
            else:
                result_data = [self._delete_single(v, count_int)
                               for v in data_obj]
                return MatrExMatrix(result_data, False)

        raise TypeError(
            f"{self._name}() работает со строками, числами, "
            f"векторами и матрицами, получен {type(data_obj)}"
        )

    def __repr__(self):
        return f"{self._name}({self.data}, {self.count})"


# ============================================================
# DELETETEXTLEFT
# ============================================================
class DeleteTextLeftNode(_DeleteTextBase):
    _name = "deletetextleft"

    def _delete_single(self, value, count):
        return _delete_left_single(value, count)


# ============================================================
# DELETETEXTRIGHT
# ============================================================
class DeleteTextRightNode(_DeleteTextBase):
    _name = "deletetextright"

    def _delete_single(self, value, count):
        return _delete_right_single(value, count)