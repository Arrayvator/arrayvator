# ast_nodes/functions/trim.py
"""
Функции очистки пробелов по краям: trim, trimleft, trimright.

СИНТАКСИС:
    trim(s)                  — убрать пробелы с обеих сторон
    trim(s, "chars")         — убрать указанные символы с обеих сторон

    trimleft(s)              — убрать пробелы слева
    trimleft(s, "chars")     — убрать указанные символы слева

    trimright(s)             — убрать пробелы справа
    trimright(s, "chars")    — убрать указанные символы справа

ПРАВИЛА:
    - Работает со строками.
    - None → None.
    - Числа и другие типы → возвращаются как есть.
    - По умолчанию убираются все whitespace: " \\t\\n\\r\\v\\f".
    - Вектор — по всем элементам.
    - Матрица — по всем ячейкам.
    - Срез ОДНОГО столбца m[:, "X"] → вектор.
    - Срез нескольких столбцов m[:, 2:5] → матрица.
    - Срез строк с одним столбцом m[2:5, "X"] → вектор.

DUCKDB:
    - trim(s)               → TRIM(col)
    - trim(s, "x")          → TRIM(col, 'x')
    - trimleft(s)           → LTRIM(col)
    - trimleft(s, "x")      → LTRIM(col, 'x')
    - trimright(s)          → RTRIM(col)
    - trimright(s, "x")     → RTRIM(col, 'x')
"""

from ..base import Node
from runtime.matrix import MatrExMatrix
from ..utils.index_utils import parse_range_spec, resolve_column_index


# ============================================================
# ХЕЛПЕР: определение DuckDBTable
# ============================================================
def _is_duckdb(val):
    try:
        from duckdb_engine import DuckDBTable
        return isinstance(val, DuckDBTable)
    except ImportError:
        return False


# ============================================================
# ОЧИСТКА ОДНОГО ЗНАЧЕНИЯ (для RAM)
# ============================================================
def _trim_single(value, chars, side):
    if value is None:
        return None

    if not isinstance(value, str):
        return value

    if side == 'left':
        return value.lstrip(chars)
    if side == 'right':
        return value.rstrip(chars)
    return value.strip(chars)


# ============================================================
# ИЗВЛЕЧЕНИЕ DUCKDBTABLE И СТОЛБЦА
# ============================================================
def _extract_duckdb_column(index_node, env, func_name):
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

    row_spec_node = index_node.indices[0]
    row_spec = (row_spec_node.evaluate(env)
                if hasattr(row_spec_node, 'evaluate')
                else row_spec_node)

    is_full = (
        isinstance(row_spec, str)
        and row_spec.strip().lower() in (':', 'all')
    )
    if not is_full:
        raise ValueError(
            f"{func_name}: DuckDB не поддерживает диапазоны строк.\n"
            f"  Указано: {row_spec}\n"
            f"  Используйте: {func_name}(m[:, \"X\"])"
        )

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
# DUCKDB: TRIM / LTRIM / RTRIM
# ============================================================
def _trim_duckdb(duck_table, col_name, chars, side, func_name):
    from duckdb_engine import DuckDBTable
    import uuid

    safe_col = '"' + str(col_name).replace('"', '""') + '"'

    if side == 'left':
        sql_func = 'LTRIM'
    elif side == 'right':
        sql_func = 'RTRIM'
    else:
        sql_func = 'TRIM'

    if chars is None:
        value_expr = f"{sql_func}({safe_col})"
    else:
        chars_sql = str(chars).replace("'", "''")
        value_expr = f"{sql_func}({safe_col}, '{chars_sql}')"

    new_name = f"trim_{uuid.uuid4().hex[:8]}"
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
        raise RuntimeError(f"Ошибка {func_name}: {e}\nSQL: {sql}")

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

    row_start, row_end = parse_range_spec(
        row_spec, matrix_obj.rows, is_column=False
    )

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
            col_start, col_end = parse_range_spec(
                s, matrix_obj.cols, is_column=True
            )
            col_info = (col_start, col_end)
        else:
            idx, skip_header = resolve_column_index(
                matrix_obj, col_spec, env
            )
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
# ХЕЛПЕР: применить fn к срезу матрицы
# ============================================================
def _apply_to_matrix_slice(matrix_obj, row_start, row_end, col_info, fn):
    """
    Применяет fn(value) ко всем ячейкам среза.

    Возвращает:
        - скаляр (одна ячейка)
        - вектор (один столбец)
        - матрицу (несколько столбцов)
    """
    col_start, col_end = col_info

    if row_start == row_end and col_start == col_end:
        i = row_start - 1
        j = col_start - 1
        if i < len(matrix_obj.data) and j < len(matrix_obj.data[i]):
            return fn(matrix_obj.data[i][j])
        return None

    result_data = [
        row.copy() if isinstance(row, list) else [row]
        for row in matrix_obj.data
    ]

    for i in range(row_start - 1, row_end):
        if i >= len(result_data):
            continue
        row = result_data[i]
        for j in range(col_start - 1, col_end):
            if j < len(row):
                row[j] = fn(row[j])

    n_cols = col_end - col_start + 1

    if n_cols == 1:
        j = col_start - 1
        vector_data = []
        for i in range(row_start - 1, row_end):
            if i < len(result_data):
                row = result_data[i]
                vector_data.append(row[j] if j < len(row) else None)
        return MatrExMatrix(vector_data, False)
    else:
        return MatrExMatrix(result_data, True)


# ============================================================
# ХЕЛПЕР: применить fn к срезу вектора
# ============================================================
def _apply_to_vector_slice(vector_obj, start, end, fn):
    if start == end:
        i = start - 1
        if 0 <= i < len(vector_obj.data):
            return fn(vector_obj.data[i])
        return None

    result_data = list(vector_obj.data)
    for i in range(start - 1, end):
        if i < len(result_data):
            result_data[i] = fn(result_data[i])

    return MatrExMatrix(result_data, False)


# ============================================================
# БАЗОВЫЙ КЛАСС
# ============================================================
class _TrimBase(Node):
    _side = 'both'
    _name = 'trim'

    def __init__(self, data, chars=None):
        self.data = data
        self.chars = chars

    def _eval_chars(self, env):
        if self.chars is None:
            return None

        val = (self.chars.evaluate(env)
               if hasattr(self.chars, 'evaluate')
               else self.chars)

        if val is None:
            return None

        if not isinstance(val, str):
            raise TypeError(
                f"{self._name}: символы должны быть строкой, "
                f"получено {type(val).__name__}"
            )

        if val == "":
            return None

        return val

    def evaluate(self, env):
        from ast_nodes.index import IndexNode

        chars = self._eval_chars(env)
        side = self._side

        def fn(v):
            return _trim_single(v, chars, side)

        # DUCKDB
        duck_table, col_name = _extract_duckdb_column(
            self.data, env, self._name
        )
        if duck_table is not None:
            return _trim_duckdb(
                duck_table, col_name, chars, side, self._name
            )

        # МАТРИЦА: срез
        analysis = _analyze_matrix_index(self.data, env)
        if analysis is not None:
            matrix_obj, row_start, row_end, col_info = analysis
            return _apply_to_matrix_slice(
                matrix_obj, row_start, row_end, col_info, fn
            )

        # СРЕЗ ВЕКТОРА
        if isinstance(self.data, IndexNode) and len(self.data.indices) == 1:
            vector_obj = self.data.matrix.evaluate(env)
            if hasattr(vector_obj, 'data') and not vector_obj.is_2d:
                idx_spec_node = self.data.indices[0]
                idx_spec = (idx_spec_node.evaluate(env)
                            if hasattr(idx_spec_node, 'evaluate')
                            else idx_spec_node)
                start, end = parse_range_spec(
                    idx_spec, len(vector_obj.data), is_column=False
                )
                return _apply_to_vector_slice(
                    vector_obj, start, end, fn
                )

        # ОБЫЧНЫЙ РЕЖИМ
        data_obj = self.data.evaluate(env)

        if isinstance(data_obj, (int, float, str)) or data_obj is None:
            return fn(data_obj)

        if hasattr(data_obj, 'data') and data_obj.is_2d:
            result_data = []
            for row in data_obj.data:
                new_row = [fn(v) for v in row]
                result_data.append(new_row)
            return MatrExMatrix(result_data, True)

        if hasattr(data_obj, 'data') and not data_obj.is_2d:
            result_data = [fn(v) for v in data_obj.data]
            return MatrExMatrix(result_data, False)

        if isinstance(data_obj, list):
            if data_obj and isinstance(data_obj[0], list):
                result_data = []
                for row in data_obj:
                    new_row = [fn(v) for v in row]
                    result_data.append(new_row)
                return MatrExMatrix(result_data, True)
            else:
                result_data = [fn(v) for v in data_obj]
                return MatrExMatrix(result_data, False)

        raise TypeError(
            f"{self._name}() работает со строками, числами, "
            f"векторами и матрицами, получен {type(data_obj)}"
        )

    def __repr__(self):
        if self.chars is not None:
            return f"{self._name}({self.data}, {self.chars})"
        return f"{self._name}({self.data})"


# ============================================================
# КОНКРЕТНЫЕ КЛАССЫ
# ============================================================
class TrimNode(_TrimBase):
    _side = 'both'
    _name = 'trim'


class TrimLeftNode(_TrimBase):
    _side = 'left'
    _name = 'trimleft'


class TrimRightNode(_TrimBase):
    _side = 'right'
    _name = 'trimright'