# ast_nodes/functions/sort.py
"""
Функция SORT - сортировка строк матрицы по столбцу.

ВАЖНО: sort() НЕ изменяет исходную матрицу.
Она ВОЗВРАЩАЕТ НОВУЮ матрицу.

СИНТАКСИС:
    # Матрица (сортировка по столбцу):
    sort(s[:, "Имя"], AZ)
    sort(s[:, "Имя"], ZA)
    sort(s[:, 3], AZ)
    sort(s[:, end], AZ)
    sort(s[:, last 1], AZ)
    sort(s[10:end, "Возраст"], AZ)
    sort(s[last 100, "Возраст"], ZA)

    # Вектор:
    sort(v, AZ)
    sort(v, ZA)
    sort(v[3:6], AZ)
    sort(v[last 3], AZ)

DUCKDB:
    - sort(m[:, "X"], AZ)  → SQL ORDER BY
    - Диапазоны строк (m[10:end, "X"]) НЕ поддерживаются на DuckDB.
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
    try:
        from duckdb_engine import DuckDBTable
        return isinstance(val, DuckDBTable)
    except ImportError:
        return False


# ============================================================
# DUCKDB: СОРТИРОВКА
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
            "sort: DuckDB не поддерживает сортировку диапазона строк.\n"
            f"  Указано: {row_spec}\n"
            "  ✅ Используйте: sort(m[:, \"X\"], AZ)"
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


def _sort_duckdb(duck_table, col_name, ascending=True):
    from duckdb_engine import DuckDBTable
    import uuid

    safe_col = '"' + str(col_name).replace('"', '""') + '"'
    direction = "ASC" if ascending else "DESC"

    new_name = f"sorted_{uuid.uuid4().hex[:8]}"
    sql = f"""
        CREATE OR REPLACE VIEW {new_name} AS
        SELECT * FROM {duck_table.table_name}
        ORDER BY {safe_col} {direction}
    """

    try:
        duck_table.con.execute(sql)
    except Exception as e:
        raise RuntimeError(f"Ошибка sort: {e}")

    new_table = DuckDBTable.__new__(DuckDBTable)
    new_table.path = duck_table.path
    new_table.table_name = new_name
    new_table.con = duck_table.con
    new_table.utf8_path = duck_table.utf8_path
    new_table.is_temp = False
    new_table._tmp_path = None

    return new_table


# ============================================================
# АНАЛИЗ СРЕЗА МАТРИЦЫ (для Matrix)
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

    col_idx, skip_header = resolve_column_index(matrix_obj, col_spec, env)

    if not is_explicit and skip_header:
        row_start = max(row_start, 2)

    return (matrix_obj, row_start, row_end, col_idx)


# ============================================================
# АНАЛИЗ СРЕЗА ВЕКТОРА (для Matrix)
# ============================================================
def _analyze_vector_index(index_node, env):
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


# ============================================================
# КЛЮЧ СОРТИРОВКИ (для Matrix)
# ============================================================
def _sort_key(value):
    if value is None:
        return (2, "")
    if isinstance(value, (int, float)):
        return (0, value)
    return (1, str(value))


# ============================================================
# SORT NODE
# ============================================================
class SortNode(Node):
    def __init__(self, data, arg1, arg2=None, order=None):
        self.data = data
        self.arg1 = arg1
        self.arg2 = arg2
        self.order = order

    # ------------------------------------------------------------
    # Направление
    # ------------------------------------------------------------
    def _get_order(self, order_node, env):
        """Получает 'az' или 'za'."""
        if order_node is None:
            return 'az'

        order_val = (order_node.evaluate(env)
                     if hasattr(order_node, 'evaluate')
                     else order_node)

        if isinstance(order_val, str):
            o = order_val.strip().lower()
            if o in ('az', 'za'):
                return o

        from errors import ArrayVatorError
        raise ArrayVatorError(
            code="SORT_BAD_DIRECTION",
            context=None,
        )

    # ------------------------------------------------------------
    # Evaluate
    # ------------------------------------------------------------
    def evaluate(self, env):
        # ============================================================
        # DUCKDB: sort(m[:, col], AZ)
        # ============================================================
        duck_table, col_name = _extract_duckdb_column(self.data, env)
        if duck_table is not None:
            order = self._get_order(self.arg1, env)
            ascending = (order == 'az')
            return _sort_duckdb(duck_table, col_name, ascending)

        # ============================================================
        # Срез матрицы: sort(s[:, "Имя"], AZ)
        # ============================================================
        analysis = _analyze_matrix_index(self.data, env)
        if analysis is not None:
            matrix_obj, row_start, row_end, col_idx = analysis
            order = self._get_order(self.arg1, env)

            protected_before = matrix_obj.data[:row_start - 1]
            working = matrix_obj.data[row_start - 1:row_end]
            protected_after = matrix_obj.data[row_end:]

            reverse = (order == 'za')

            sorted_working = sorted(
                working,
                key=lambda row: _sort_key(
                    row[col_idx] if col_idx < len(row) else None
                ),
                reverse=reverse,
            )

            result_data = (
                list(protected_before)
                + sorted_working
                + list(protected_after)
            )
            return MatrExMatrix(result_data, True)

        # ============================================================
        # Срез вектора: sort(v[3:6], AZ)
        # ============================================================
        vector_analysis = _analyze_vector_index(self.data, env)
        if vector_analysis is not None:
            vector_obj, start, end = vector_analysis
            order = self._get_order(self.arg1, env)

            protected_before = vector_obj.data[:start - 1]
            working = vector_obj.data[start - 1:end]
            protected_after = vector_obj.data[end:]

            reverse = (order == 'za')
            sorted_working = sorted(working, key=_sort_key, reverse=reverse)

            result_data = (
                list(protected_before)
                + sorted_working
                + list(protected_after)
            )
            return MatrExMatrix(result_data, False)

        # ============================================================
        # Обычный режим
        # ============================================================
        data_obj = self.data.evaluate(env)

        # --- Вектор: sort(v, AZ) ---
        if hasattr(data_obj, 'data') and not data_obj.is_2d:
            order = self._get_order(self.arg1, env)
            reverse = (order == 'za')
            sorted_data = sorted(data_obj.data, key=_sort_key, reverse=reverse)
            return MatrExMatrix(sorted_data, False)

        # --- Список (вектор) ---
        if isinstance(data_obj, list) and not (data_obj and isinstance(data_obj[0], list)):
            order = self._get_order(self.arg1, env)
            reverse = (order == 'za')
            sorted_data = sorted(data_obj, key=_sort_key, reverse=reverse)
            return MatrExMatrix(sorted_data, False)

        # --- Матрица без среза: sort(m, AZ) — ОШИБКА! ---
        if hasattr(data_obj, 'data') and data_obj.is_2d:
            from errors import ArrayVatorError
            raise ArrayVatorError(
                code="SORT_BAD_FIRST_ARG",
                context=None,
            )

        # --- Всё остальное — ошибка ---
        from errors import ArrayVatorError
        raise ArrayVatorError(
            code="SORT_BAD_FIRST_ARG",
            context=None,
        )

    def __repr__(self):
        if self.arg2 is not None:
            return f"sort({self.data}, {self.arg1}, {self.arg2})"
        return f"sort({self.data}, {self.arg1})"