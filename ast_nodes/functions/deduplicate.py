# ast_nodes/functions/deduplicate.py
"""
Функции для работы с дубликатами:
    Unique()           - уникальные строки матрицы по столбцу
    CountDistinct()    - количество уникальных
    ValueCounts()      - частотная таблица
    DeleteDuplicate()  - удаление дубликатов (синоним Unique)

СИНТАКСИС:
    Unique(вектор)                    # уникальные значения вектора
    Unique(матрица)                   # уникальные строки матрицы (DISTINCT *)
    Unique(матрица[:, "Отдел"])       # уникальные строки по столбцу "Отдел"
    Unique(матрица[:, 3])             # уникальные строки по столбцу 3

    CountDistinct(вектор)
    CountDistinct(матрица[:, "Отдел"])

    ValueCounts(вектор)
    ValueCounts(матрица[:, "Отдел"])

    DeleteDuplicate(вектор)
    DeleteDuplicate(матрица[:, "Отдел"])

DUCKDB:
    - Unique(m[:, "X"]) → SELECT * с ROW_NUMBER() OVER PARTITION BY
    - Unique(m)         → SELECT DISTINCT *
    - CountDistinct     → SELECT COUNT(DISTINCT)
    - ValueCounts       → SELECT col, COUNT(*) GROUP BY
    - Диапазоны строк (m[10:end, "X"]) НЕ поддерживаются.
"""

from ..base import Node
from runtime.matrix import MatrExMatrix
from ..utils.index_utils import (
    parse_range_spec,
    resolve_column_index,
)


# ============================================================
# ХЕЛПЕР: определение DuckDBTable
# ============================================================
def _is_duckdb(val):
    """Проверяет, является ли значение DuckDBTable."""
    try:
        from duckdb_engine import DuckDBTable
        return isinstance(val, DuckDBTable)
    except ImportError:
        return False


# ============================================================
# ИЗВЛЕЧЕНИЕ DUCKDBTABLE ИЗ INDEXNODE
# ============================================================
def _extract_duckdb_column(index_node, env):
    """
    Извлекает (duck_table, col_name | None) из IndexNode.

    Возвращает:
        (duck_table, col_name) — если IndexNode с одним столбцом
        (duck_table, None)     — если IndexNode с : (все столбцы)

    ВАЖНО: поддерживает только полный срез m[:, "X"] или m[:, :].
    Диапазоны строк (m[10:end, "X"]) НЕ поддерживаются.
    """
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

    # --- Проверка row_spec ---
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
            "Unique / DeleteDuplicate: DuckDB не поддерживает "
            "диапазоны строк.\n"
            f"  Указано: {row_spec}\n"
            "  ✅ Используйте: Unique(m[:, \"X\"])  или  Unique(m)"
        )

    # --- Извлечение столбца ---
    col_spec_node = index_node.indices[1]
    col_spec = (col_spec_node.evaluate(env)
                if hasattr(col_spec_node, 'evaluate')
                else col_spec_node)

    # Если столбец — : или all, то col_name = None (все столбцы)
    if isinstance(col_spec, str) and col_spec.strip().lower() in (':', 'all'):
        return (matrix_obj, None)

    from .filterif import _resolve_column_for_duckdb
    columns = matrix_obj.get_columns()
    col_idx = _resolve_column_for_duckdb(columns, col_spec)

    if 0 <= col_idx < len(columns):
        return (matrix_obj, columns[col_idx])

    return (None, None)


def _extract_duckdb_table(node, env):
    """
    Извлекает (duck_table) из узла — без среза.

    Поддерживает:
        Unique(m)   — переменная с DuckDBTable

    Возвращает:
        (duck_table)  — если узел — DuckDBTable
        (None)        — иначе
    """
    from ast_nodes.index import IndexNode

    # Если это IndexNode — не наш случай
    if isinstance(node, IndexNode):
        return None

    try:
        obj = node.evaluate(env) if hasattr(node, 'evaluate') else node
    except Exception:
        return None

    if _is_duckdb(obj):
        return obj

    return None


# ============================================================
# ХЕЛПЕРЫ ДЛЯ MATRIX
# ============================================================
def _get_unique_list(items):
    """Уникальные значения с сохранением порядка."""
    seen = set()
    result = []
    for item in items:
        try:
            if item in seen:
                continue
            seen.add(item)
        except TypeError:
            if item in result:
                continue
        result.append(item)
    return result


def _count_values(values):
    """Частоты значений, отсортированные по убыванию частоты."""
    freq_dict = {}
    for val in values:
        try:
            if val in freq_dict:
                freq_dict[val] += 1
            else:
                freq_dict[val] = 1
        except TypeError:
            key = str(val)
            if key in freq_dict:
                freq_dict[key] += 1
            else:
                freq_dict[key] = 1

    # Сортировка: сначала по частоте (DESC), потом по значению (ASC)
    def _sort_key(item):
        val, cnt = item
        if isinstance(val, (int, float)) and not isinstance(val, bool):
            val_key = (0, val)
        else:
            val_key = (1, str(val))
        return (-cnt, val_key)

    items = list(freq_dict.items())
    try:
        items.sort(key=_sort_key)
    except Exception:
        items.sort(key=lambda x: -x[1])

    return [[k, v] for k, v in items]


def _get_unique_rows_by_key(rows, key_idx):
    """Уникализация строк по значению в key_idx."""
    seen = set()
    result = []
    for row in rows:
        try:
            key = row[key_idx] if key_idx < len(row) else None
            if key in seen:
                continue
            seen.add(key)
        except TypeError:
            key = str(row[key_idx]) if key_idx < len(row) else ""
            if key in seen:
                continue
            seen.add(key)
        result.append(row)
    return result


def _get_unique_rows(rows):
    """Уникализация строк целиком."""
    seen = set()
    result = []
    for row in rows:
        try:
            row_tuple = tuple(row)
            if row_tuple in seen:
                continue
            seen.add(row_tuple)
        except TypeError:
            row_tuple = tuple(str(x) for x in row)
            if row_tuple in seen:
                continue
            seen.add(row_tuple)
        result.append(row)
    return result


# ============================================================
# DUCKDB: UNIQUE (уникальные СТРОКИ по столбцу)
# ============================================================
def _unique_duckdb(duck_table, col_name):
    """
    Уникальные СТРОКИ матрицы по значению в col_name.

    Если col_name is None → SELECT DISTINCT * (все столбцы).

    Порядок результата:
        • col_name задан  → порядок ПЕРВОГО появления
                            в исходной таблице.
        • col_name is None → порядок DISTINCT.
    """
    from duckdb_engine import DuckDBTable
    import uuid

    new_name = f"unique_{uuid.uuid4().hex[:8]}"

    if col_name is None:
        sql = f"""
            CREATE OR REPLACE VIEW {new_name} AS
            SELECT DISTINCT * FROM {duck_table.table_name}
        """
    else:
        safe_col = '"' + str(col_name).replace('"', '""') + '"'

        columns = duck_table.get_columns()
        col_list = ", ".join(
            f'"{str(c).replace(chr(34), chr(34)+chr(34))}"'
            for c in columns
        )

        # ============================================================
        # ВАЖНО:
        #   1. __orig_row — номер строки в ИСХОДНОМ порядке.
        #   2. PARTITION BY col ORDER BY __orig_row
        #      → берём ПЕРВОЕ появление в исходной таблице.
        #   3. Финальный ORDER BY __orig_row
        #      → порядок результата = порядок первого появления.
        # ============================================================
        sql = f"""
            CREATE OR REPLACE VIEW {new_name} AS
            SELECT {col_list} FROM (
                SELECT *,
                       ROW_NUMBER() OVER (
                           PARTITION BY {safe_col}
                           ORDER BY __orig_row
                       ) AS __rn
                FROM (
                    SELECT *,
                           ROW_NUMBER() OVER () AS __orig_row
                    FROM {duck_table.table_name}
                )
            ) WHERE __rn = 1
            ORDER BY __orig_row
        """

    try:
        duck_table.con.execute(sql)
    except Exception as e:
        raise RuntimeError(f"Ошибка Unique: {e}\nSQL: {sql}")

    new_table = DuckDBTable.__new__(DuckDBTable)
    new_table.path = duck_table.path
    new_table.table_name = new_name
    new_table.con = duck_table.con
    new_table.utf8_path = duck_table.utf8_path
    new_table.is_temp = False
    new_table._tmp_path = None

    return new_table


# ============================================================
# DUCKDB: COUNT DISTINCT
# ============================================================
def _count_distinct_duckdb(duck_table, col_name):
    """SELECT COUNT(DISTINCT col) FROM table"""
    if col_name is None:
        raise ValueError(
            "CountDistinct: укажите столбец.\n"
            "  Пример: CountDistinct(m[:, \"Отдел\"])"
        )

    safe_col = '"' + str(col_name).replace('"', '""') + '"'

    sql = f"""
        SELECT COUNT(DISTINCT {safe_col})
        FROM {duck_table.table_name}
    """

    try:
        result = duck_table.con.execute(sql).fetchone()
        return result[0] if result else 0
    except Exception as e:
        raise RuntimeError(f"Ошибка CountDistinct: {e}")


# ============================================================
# DUCKDB: VALUE COUNTS
# ============================================================
def _value_counts_duckdb(duck_table, col_name):
    """SELECT col, COUNT(*) FROM table GROUP BY col"""
    if col_name is None:
        raise ValueError(
            "ValueCounts: укажите столбец.\n"
            "  Пример: ValueCounts(m[:, \"Отдел\"])"
        )

    from duckdb_engine import DuckDBTable
    import uuid

    safe_col = '"' + str(col_name).replace('"', '""') + '"'

    new_name = f"vcounts_{uuid.uuid4().hex[:8]}"
    sql = f"""
        CREATE OR REPLACE VIEW {new_name} AS
        SELECT {safe_col} AS "Значение", COUNT(*) AS "Частота"
        FROM {duck_table.table_name}
        GROUP BY {safe_col}
        ORDER BY COUNT(*) DESC, {safe_col} ASC
    """

    try:
        duck_table.con.execute(sql)
    except Exception as e:
        raise RuntimeError(f"Ошибка ValueCounts: {e}")

    new_table = DuckDBTable.__new__(DuckDBTable)
    new_table.path = duck_table.path
    new_table.table_name = new_name
    new_table.con = duck_table.con
    new_table.utf8_path = duck_table.utf8_path
    new_table.is_temp = False
    new_table._tmp_path = None

    return new_table


# ============================================================
# UNIQUE
# ============================================================
class UniqueNode(Node):
    def __init__(self, data, column=None):
        self.data = data
        self.column = column

    def evaluate(self, env):
        # DuckDB: Unique(m[:, "X"])
        duck_table, col_name = _extract_duckdb_column(self.data, env)
        if duck_table is not None:
            return _unique_duckdb(duck_table, col_name)

        # DuckDB: Unique(m) без среза
        duck_table = _extract_duckdb_table(self.data, env)
        if duck_table is not None:
            return _unique_duckdb(duck_table, None)

        # MATRIX
        from ast_nodes.index import IndexNode

        if isinstance(self.data, IndexNode):
            analysis = _analyze_matrix_index(self.data, env)
            if analysis is not None:
                matrix_obj, row_start, row_end, col_idx = analysis
                protected_before = matrix_obj.data[:row_start - 1]
                working = matrix_obj.data[row_start - 1:row_end]
                protected_after = matrix_obj.data[row_end:]
                unique_working = _get_unique_rows_by_key(working, col_idx)
                result_data = (
                    list(protected_before)
                    + unique_working
                    + list(protected_after)
                )
                return MatrExMatrix(result_data, True)

        vector_analysis = _analyze_vector_index(self.data, env)
        if vector_analysis is not None:
            vector_obj, start, end = vector_analysis
            protected_before = vector_obj.data[:start - 1]
            working = vector_obj.data[start - 1:end]
            protected_after = vector_obj.data[end:]
            unique_working = _get_unique_list(working)
            result_data = (
                list(protected_before)
                + unique_working
                + list(protected_after)
            )
            return MatrExMatrix(result_data, False)

        data_obj = self.data.evaluate(env)

        if hasattr(data_obj, 'data') and not data_obj.is_2d:
            return MatrExMatrix(_get_unique_list(data_obj.data), False)

        if isinstance(data_obj, list) and not (data_obj and isinstance(data_obj[0], list)):
            return MatrExMatrix(_get_unique_list(data_obj), False)

        if hasattr(data_obj, 'data') and data_obj.is_2d:
            return MatrExMatrix(_get_unique_rows(data_obj.data), True)

        if isinstance(data_obj, list) and data_obj and isinstance(data_obj[0], list):
            return MatrExMatrix(_get_unique_rows(data_obj), True)

        raise TypeError(
            f"Unique() работает с векторами и матрицами, "
            f"получен {type(data_obj)}"
        )

    def __repr__(self):
        if self.column is None:
            return f"Unique({self.data})"
        return f"Unique({self.data}, column={self.column})"


# ============================================================
# COUNT DISTINCT
# ============================================================
class CountDistinctNode(Node):
    def __init__(self, data, column=None):
        self.data = data
        self.column = column

    def evaluate(self, env):
        # DUCKDB
        duck_table, col_name = _extract_duckdb_column(self.data, env)
        if duck_table is not None:
            return _count_distinct_duckdb(duck_table, col_name)

        # MATRIX
        from ast_nodes.index import IndexNode

        if isinstance(self.data, IndexNode):
            analysis = _analyze_matrix_index(self.data, env)
            if analysis is not None:
                matrix_obj, row_start, row_end, col_idx = analysis
                values = []
                for i in range(row_start - 1, row_end):
                    if i < len(matrix_obj.data):
                        row = matrix_obj.data[i]
                        values.append(row[col_idx] if col_idx < len(row) else None)
                return len(_get_unique_list(values))

        vector_analysis = _analyze_vector_index(self.data, env)
        if vector_analysis is not None:
            vector_obj, start, end = vector_analysis
            values = list(vector_obj.data[start - 1:end])
            return len(_get_unique_list(values))

        data_obj = self.data.evaluate(env)

        if hasattr(data_obj, 'data') and not data_obj.is_2d:
            return len(_get_unique_list(data_obj.data))

        if isinstance(data_obj, list) and not (data_obj and isinstance(data_obj[0], list)):
            return len(_get_unique_list(data_obj))

        raise TypeError(
            f"CountDistinct() работает с векторами и столбцами, "
            f"получен {type(data_obj)}"
        )

    def __repr__(self):
        if self.column is None:
            return f"CountDistinct({self.data})"
        return f"CountDistinct({self.data}, column={self.column})"


# ============================================================
# VALUE COUNTS
# ============================================================
class ValueCountsNode(Node):
    def __init__(self, data, column=None):
        self.data = data
        self.column = column

    def evaluate(self, env):
        # DUCKDB
        duck_table, col_name = _extract_duckdb_column(self.data, env)
        if duck_table is not None:
            return _value_counts_duckdb(duck_table, col_name)

        # MATRIX
        from ast_nodes.index import IndexNode

        if isinstance(self.data, IndexNode):
            analysis = _analyze_matrix_index(self.data, env)
            if analysis is not None:
                matrix_obj, row_start, row_end, col_idx = analysis
                values = []
                for i in range(row_start - 1, row_end):
                    if i < len(matrix_obj.data):
                        row = matrix_obj.data[i]
                        values.append(row[col_idx] if col_idx < len(row) else None)
                return MatrExMatrix(_count_values(values), True)

        vector_analysis = _analyze_vector_index(self.data, env)
        if vector_analysis is not None:
            vector_obj, start, end = vector_analysis
            values = list(vector_obj.data[start - 1:end])
            return MatrExMatrix(_count_values(values), True)

        data_obj = self.data.evaluate(env)

        if hasattr(data_obj, 'data') and not data_obj.is_2d:
            return MatrExMatrix(_count_values(data_obj.data), True)

        if isinstance(data_obj, list) and not (data_obj and isinstance(data_obj[0], list)):
            return MatrExMatrix(_count_values(data_obj), True)

        raise TypeError(
            f"ValueCounts() работает с векторами и столбцами, "
            f"получен {type(data_obj)}"
        )

    def __repr__(self):
        if self.column is None:
            return f"ValueCounts({self.data})"
        return f"ValueCounts({self.data}, column={self.column})"


# ============================================================
# DELETE DUPLICATE
# ============================================================
class DeleteDuplicateNode(Node):
    def __init__(self, data, column=None):
        self.data = data
        self.column = column

    def evaluate(self, env):
        return UniqueNode(self.data, self.column).evaluate(env)

    def __repr__(self):
        if self.column is None:
            return f"DeleteDuplicate({self.data})"
        return f"DeleteDuplicate({self.data}, column={self.column})"


# ============================================================
# АНАЛИЗ СРЕЗА МАТРИЦЫ (для Matrix)
# ============================================================
def _analyze_matrix_index(index_node, env):
    """Разбирает IndexNode для матрицы (2D)."""
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

    col_idx, skip_header = resolve_column_index(matrix_obj, col_spec, env)

    if not is_explicit and skip_header:
        row_start = max(row_start, 2)

    return (matrix_obj, row_start, row_end, col_idx)


def _analyze_vector_index(index_node, env):
    """Разбирает IndexNode для вектора (1D)."""
    if not hasattr(index_node, 'indices'):
        return None
    if len(index_node.indices) != 1:
        return None

    vector_obj = index_node.matrix.evaluate(env)
    if not hasattr(vector_obj, 'data') or vector_obj.is_2d:
        return None

    idx_node = index_node.indices[0]
    idx_spec = (idx_node.evaluate(env)
                if hasattr(idx_node, 'evaluate')
                else idx_node)

    start, end = parse_range_spec(idx_spec, len(vector_obj.data), is_column=False)
    return (vector_obj, start, end)