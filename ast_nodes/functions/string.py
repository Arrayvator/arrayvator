# ast_nodes/functions/string.py
"""
Строковые функции: SplitNode, JoinVectorNode, ReplaceTextNode

СИНТАКСИС REPLACETEXT:

    replacetext(s, "что", "на_что")
    replacetext(s, "что", "на_что", ignore)
    replacetext(s[:, "Отдел"], "что", "на_что")
    replacetext(s[:, 3], "что", "на_что")

DUCKDB:
    - Если данные в DuckDBTable → SQL REPLACE / REGEXP_REPLACE через * REPLACE
    - Возвращает новый DuckDBTable (view)
    - Столбец остаётся на своём месте

Matrix:
    - m[:, "X"]      → вектор
    - m[:, 2:5]      → матрица
    - m              → матрица
    - скаляр         → скаляр

ПРАВИЛО:
    Один столбец (col_start == col_end) → вектор.
    Несколько столбцов                 → матрица.
    Одна ячейка                         → скаляр.
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
# ЗАМЕНА В ОДНОМ ЗНАЧЕНИИ (для RAM)
# ============================================================
def _replace_single(value, old_str, new_str, ignore):
    """Заменяет old_str на new_str в одном значении."""
    if value is None:
        return None

    if isinstance(value, str):
        if ignore:
            import re
            pattern = re.compile(re.escape(old_str), re.IGNORECASE)
            return pattern.sub(new_str, value)
        return value.replace(old_str, new_str)

    if isinstance(value, (int, float)):
        str_val = str(value)
        if ignore:
            import re
            pattern = re.compile(re.escape(old_str), re.IGNORECASE)
            str_val = pattern.sub(new_str, str_val)
        else:
            str_val = str_val.replace(old_str, new_str)

        try:
            if '.' in str_val:
                return float(str_val)
            return int(str_val)
        except ValueError:
            return str_val

    return value


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
            "replacetext: DuckDB не поддерживает диапазоны строк.\n"
            f"  Указано: {row_spec}\n"
            "  ✅ Используйте: replacetext(m[:, \"X\"], \"a\", \"b\")"
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
# DUCKDB: REPLACETEXT через * REPLACE
# ============================================================
def _replacetext_duckdb(duck_table, col_name, old_str, new_str, ignore):
    from duckdb_engine import DuckDBTable
    import uuid

    safe_col = '"' + str(col_name).replace('"', '""') + '"'

    old_sql = str(old_str).replace("'", "''")
    new_sql = str(new_str).replace("'", "''")

    if ignore:
        import re
        old_escaped = re.escape(str(old_str))
        old_escaped_sql = old_escaped.replace("'", "''")
        value_expr = (
            f"REGEXP_REPLACE(CAST({safe_col} AS VARCHAR), "
            f"'(?i){old_escaped_sql}', '{new_sql}', 'g')"
        )
    else:
        value_expr = (
            f"REPLACE(CAST({safe_col} AS VARCHAR), "
            f"'{old_sql}', '{new_sql}')"
        )

    new_name = f"repl_{uuid.uuid4().hex[:8]}"
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
        raise RuntimeError(f"Ошибка replacetext: {e}\nSQL: {sql}")

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
    """Разбирает IndexNode для матрицы."""
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
# REPLACE TEXT NODE
# ============================================================
class ReplaceTextNode(Node):
    def __init__(self, data, old, new, column=None, row=None,
                 row_range=None, ignore=None):
        self.data = data
        self.old = old
        self.new = new
        self.column = column
        self.row = row
        self.row_range = row_range
        self.ignore = ignore

    def evaluate(self, env):
        old_val = self.old.evaluate(env) if hasattr(self.old, 'evaluate') else self.old
        new_val = self.new.evaluate(env) if hasattr(self.new, 'evaluate') else self.new

        if not isinstance(old_val, str):
            old_val = str(old_val)
        if not isinstance(new_val, str):
            new_val = str(new_val)

        ignore = False
        if self.ignore is not None:
            ig = self.ignore.evaluate(env) if hasattr(self.ignore, 'evaluate') else self.ignore
            if isinstance(ig, str) and ig.lower() == 'ignore':
                ignore = True

        # DUCKDB
        duck_table, col_name = _extract_duckdb_column(self.data, env)
        if duck_table is not None:
            return _replacetext_duckdb(
                duck_table, col_name, old_val, new_val, ignore
            )

        # СРЕЗ МАТРИЦЫ
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
                    return _replace_single(
                        matrix_obj.data[i][j], old_val, new_val, ignore
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
                                _replace_single(row[c_idx], old_val, new_val, ignore)
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
                        row[j] = _replace_single(row[j], old_val, new_val, ignore)

            return MatrExMatrix(result_data, True)

        # СРЕЗ ВЕКТОРА
        from ast_nodes.index import IndexNode
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
                        return _replace_single(
                            vector_obj.data[i], old_val, new_val, ignore
                        )
                    return None

                result_data = list(vector_obj.data)
                for i in range(start - 1, end):
                    if i < len(result_data):
                        result_data[i] = _replace_single(result_data[i], old_val, new_val, ignore)

                return MatrExMatrix(result_data, False)

        # ОБЫЧНЫЙ РЕЖИМ
        data_obj = self.data.evaluate(env)

        if hasattr(data_obj, 'data') and data_obj.is_2d:
            result_data = []
            for row in data_obj.data:
                new_row = [_replace_single(v, old_val, new_val, ignore) for v in row]
                result_data.append(new_row)
            return MatrExMatrix(result_data, True)

        if hasattr(data_obj, 'data') and not data_obj.is_2d:
            result_data = [_replace_single(v, old_val, new_val, ignore)
                           for v in data_obj.data]
            return MatrExMatrix(result_data, False)

        if isinstance(data_obj, (int, float, str)):
            return _replace_single(data_obj, old_val, new_val, ignore)

        if isinstance(data_obj, list):
            if data_obj and isinstance(data_obj[0], list):
                result_data = []
                for row in data_obj:
                    new_row = [_replace_single(v, old_val, new_val, ignore) for v in row]
                    result_data.append(new_row)
                return MatrExMatrix(result_data, True)
            else:
                result_data = [_replace_single(v, old_val, new_val, ignore)
                               for v in data_obj]
                return MatrExMatrix(result_data, False)

        raise TypeError(
            f"replacetext() работает со строками, числами, "
            f"векторами и матрицами, получен {type(data_obj)}"
        )

    def __repr__(self):
        return f"replacetext({self.data}, {self.old}, {self.new})"


# ============================================================
# SPLIT
# ============================================================
class SplitNode(Node):
    def __init__(self, text, delimiter=None, skip_empty=False):
        self.text = text
        self.delimiter = delimiter
        self.skip_empty = skip_empty

    def evaluate(self, env):
        text_val = self.text.evaluate(env)

        if not isinstance(text_val, str):
            raise TypeError(f"split() работает только со строками, получен {type(text_val)}")

        delim = None
        if self.delimiter is not None:
            delim = self.delimiter.evaluate(env)
            if not isinstance(delim, str):
                raise TypeError(f"Разделитель должен быть строкой, получен {type(delim)}")
        else:
            result = list(text_val)
            if self.skip_empty:
                result = [x for x in result if x != '']
            return MatrExMatrix(result, False)

        if delim == '':
            result = list(text_val)
        else:
            result = text_val.split(delim)

        if self.skip_empty:
            result = [x for x in result if x != '']

        return MatrExMatrix(result, False)

    def __repr__(self):
        if self.delimiter is not None and self.skip_empty:
            return f"split({self.text}, {self.delimiter}, skip)"
        elif self.delimiter is not None:
            return f"split({self.text}, {self.delimiter})"
        return f"split({self.text})"


# ============================================================
# JOINVECTOR (бывший join)
# ============================================================
class JoinVectorNode(Node):
    """
    joinvector(вектор [, разделитель])

    Соединяет элементы вектора в строку.
    """
    def __init__(self, data, delimiter=None):
        self.data = data
        self.delimiter = delimiter

    def evaluate(self, env):
        data_obj = self.data.evaluate(env)

        delim = ''
        if self.delimiter is not None:
            delim = self.delimiter.evaluate(env)
            if not isinstance(delim, str):
                raise TypeError(f"Разделитель должен быть строкой, получен {type(delim)}")

        if hasattr(data_obj, 'data') and not data_obj.is_2d:
            return delim.join([str(x) for x in data_obj.data])

        if hasattr(data_obj, 'data') and data_obj.is_2d:
            rows = []
            for row in data_obj.data:
                rows.append(delim.join([str(x) for x in row]))
            return "\n".join(rows)

        if isinstance(data_obj, list):
            if data_obj and isinstance(data_obj[0], list):
                rows = []
                for row in data_obj:
                    rows.append(delim.join([str(x) for x in row]))
                return "\n".join(rows)
            else:
                return delim.join([str(x) for x in data_obj])

        raise TypeError(
            f"joinvector() работает с векторами и матрицами, "
            f"получен {type(data_obj)}"
        )

    def __repr__(self):
        if self.delimiter is not None:
            return f"joinvector({self.data}, {self.delimiter})"
        return f"joinvector({self.data})"