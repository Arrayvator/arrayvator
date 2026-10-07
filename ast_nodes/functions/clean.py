# ast_nodes/functions/clean.py
"""
Функция очистки: CleanNode

СИНТАКСИС:
    clean(data, "digits")     — оставить только цифры
    clean(data, "letters")    — оставить только буквы
    clean(data, "special")    — оставить только спецсимволы
    clean(data, "alnum")      — оставить только буквы и цифры

DUCKDB:
    - Если данные в DuckDBTable → SQL REGEXP_REPLACE через * REPLACE
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

import re
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
def _clean_single(value, mode):
    """Очищает одно значение по режиму."""
    str_val = str(value)

    if mode == 'digits':
        result = re.sub(r'[^0-9]', '', str_val)
    elif mode == 'letters':
        result = re.sub(r'[^a-zA-Zа-яА-Я]', '', str_val)
    elif mode == 'special':
        result = re.sub(r'[a-zA-Zа-яА-Я0-9]', '', str_val)
    elif mode == 'alnum':
        result = re.sub(r'[^a-zA-Zа-яА-Я0-9]', '', str_val)
    else:
        raise ValueError(f"Неизвестный режим очистки: {mode}")

    if mode == 'digits' and result:
        try:
            return int(result)
        except ValueError:
            return result
    return result


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
            "clean: DuckDB не поддерживает диапазоны строк.\n"
            f"  Указано: {row_spec}\n"
            "  ✅ Используйте: clean(m[:, \"X\"], \"digits\")"
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
# DUCKDB: CLEAN через * REPLACE
# ============================================================
def _clean_duckdb(duck_table, col_name, mode):
    from duckdb_engine import DuckDBTable
    import uuid

    safe_col = '"' + str(col_name).replace('"', '""') + '"'

    if mode == 'digits':
        pattern = '[^0-9]'
    elif mode == 'letters':
        pattern = '[^a-zA-Zа-яА-Я]'
    elif mode == 'special':
        pattern = '[a-zA-Zа-яА-Я0-9]'
    elif mode == 'alnum':
        pattern = '[^a-zA-Zа-яА-Я0-9]'
    else:
        raise ValueError(f"Неизвестный режим очистки: {mode}")

    pattern_sql = pattern.replace("'", "''")

    new_name = f"clean_{uuid.uuid4().hex[:8]}"
    sql = f"""
        CREATE OR REPLACE VIEW {new_name} AS
        SELECT * REPLACE (
            REGEXP_REPLACE(
                CAST({safe_col} AS VARCHAR),
                '{pattern_sql}',
                '',
                'g'
            ) AS {safe_col}
        )
        FROM {duck_table.table_name}
    """

    try:
        duck_table.con.execute(sql)
    except Exception as e:
        raise RuntimeError(f"Ошибка clean: {e}\nSQL: {sql}")

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
# CLEAN NODE
# ============================================================
class CleanNode(Node):
    def __init__(self, data, mode):
        self.data = data
        self.mode = mode

    def evaluate(self, env):
        from ast_nodes.index import IndexNode

        mode = self.mode.evaluate(env)

        if not isinstance(mode, str):
            raise TypeError(f"Режим очистки должен быть строкой, получен {type(mode)}")

        # DUCKDB
        duck_table, col_name = _extract_duckdb_column(self.data, env)
        if duck_table is not None:
            return _clean_duckdb(duck_table, col_name, mode)

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
                    return _clean_single(
                        matrix_obj.data[i][j], mode
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
                            result.append(_clean_single(row[c_idx], mode))
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
                        row[j] = _clean_single(row[j], mode)

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
                        return _clean_single(vector_obj.data[i], mode)
                    return None

                result_data = list(vector_obj.data)
                for i in range(start - 1, end):
                    if i < len(result_data):
                        result_data[i] = _clean_single(result_data[i], mode)

                return MatrExMatrix(result_data, False)

        # ОБЫЧНЫЙ РЕЖИМ
        data_obj = self.data.evaluate(env)

        if isinstance(data_obj, (int, float, str)):
            return _clean_single(data_obj, mode)

        if hasattr(data_obj, 'data'):
            if not data_obj.is_2d:
                result = []
                for item in data_obj.data:
                    result.append(_clean_single(item, mode))
                return MatrExMatrix(result, False)
            else:
                result = []
                for row in data_obj.data:
                    new_row = []
                    for item in row:
                        new_row.append(_clean_single(item, mode))
                    result.append(new_row)
                return MatrExMatrix(result, True)

        if isinstance(data_obj, list):
            if data_obj and isinstance(data_obj[0], list):
                result = []
                for row in data_obj:
                    new_row = []
                    for item in row:
                        new_row.append(_clean_single(item, mode))
                    result.append(new_row)
                return MatrExMatrix(result, True)
            else:
                result = []
                for item in data_obj:
                    result.append(_clean_single(item, mode))
                return MatrExMatrix(result, False)

        raise TypeError(
            f"clean() работает со строками, числами, векторами и матрицами, "
            f"получен {type(data_obj)}"
        )

    def __repr__(self):
        return f"clean({self.data}, {self.mode})"