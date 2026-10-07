# ast_nodes/functions/conditional_agg.py
"""
Условные агрегаты: sumif, countif, avgif, minif, maxif, medianif,
sumproduct, countuniqueif.

ДВА РЕЖИМА КАЖДОЙ ФУНКЦИИ:

    Без by — скаляр (агрегат по всей таблице):
        r = sumif(m[:, "Отдел"] == "IT", m[:, "Зарплата"])

    С by — вектор (агрегат внутри групп, разложенный по строкам):
        r = sumif(by m[:, "Отдел"], m[:, "Зарплата"])

ДОПОЛНИТЕЛЬНО:
    condition=None (без условия) означает "вся таблица" или "вся группа".
    Это используется для нового синтаксиса:
        sum(m[:, "Зарплата"], by m[:, "Отдел"])
    который делегирует в SumIfNode(condition=None, value_col=..., by=...).

DUCKDB:
    - Скаляр: SELECT AGG(col) FROM t WHERE условие.
    - С by:   SELECT AGG(col) OVER (PARTITION BY grp) FROM t.
    - Условие транслируется как VARCHAR-сравнение (как в filterif).
"""

from ..base import Node


def _is_duckdb(val):
    try:
        from duckdb_engine import DuckDBTable
        return isinstance(val, DuckDBTable)
    except ImportError:
        return False


def _is_number(v):
    return isinstance(v, (int, float)) and not isinstance(v, bool)


# ============================================================
# ХЕЛПЕРЫ: Matrix
# ============================================================
def _resolve_column(matrix_obj, col_node, env):
    """Возвращает 0-based индекс столбца из узла-среза или спецификации."""
    from ..utils.index_utils import resolve_column_index

    if hasattr(col_node, 'indices') and len(col_node.indices) == 2:
        col_spec = col_node.indices[1]
    else:
        col_spec = col_node

    col_val = (col_spec.evaluate(env)
               if hasattr(col_spec, 'evaluate')
               else col_spec)

    idx, _ = resolve_column_index(matrix_obj, col_val, env)
    return idx


def _get_column_values(matrix_obj, col_idx):
    """Возвращает список значений столбца (без заголовка)."""
    values = []
    for i in range(1, matrix_obj.rows):
        row = matrix_obj.data[i]
        values.append(row[col_idx] if col_idx < len(row) else None)
    return values


def _evaluate_condition_rows(matrix_obj, condition, env):
    """
    Возвращает список булевых значений для строк данных.
    Если condition is None — все True (весь столбец проходит).
    """
    row_start = 2
    row_end = matrix_obj.rows

    if condition is None:
        return [True] * (row_end - row_start + 1)

    from .filterif import _evaluate_condition_matrix

    result = _evaluate_condition_matrix(
        condition, env, matrix_obj, row_start, row_end
    )

    if not isinstance(result, list):
        result = [bool(result)] * (row_end - row_start + 1)

    return result


def _groups_by_column(matrix_obj, group_col_idx):
    """Список ключей группы для каждой строки (без заголовка)."""
    groups = []
    for i in range(1, matrix_obj.rows):
        row = matrix_obj.data[i]
        groups.append(row[group_col_idx] if group_col_idx < len(row) else None)
    return groups


# ============================================================
# АГРЕГАТЫ (для Matrix)
# ============================================================
def _apply_sum(values):
    return sum(v for v in values if _is_number(v))


def _apply_count(values):
    """
    Считает НЕПУСТЫЕ значения.

    Для count(m[:, "X"]) / count(m[:, "X"], by ...) в values лежат
    значения столбца — None пропускаем.
    Для count(by ...) в values лежат единицы-заглушки — они не None,
    поэтому считаются все строки группы.
    """
    return sum(1 for v in values if v is not None)


def _apply_avg(values):
    nums = [v for v in values if _is_number(v)]
    return sum(nums) / len(nums) if nums else None


def _apply_min(values):
    nums = [v for v in values if _is_number(v)]
    return min(nums) if nums else None


def _apply_max(values):
    nums = [v for v in values if _is_number(v)]
    return max(nums) if nums else None


def _apply_median(values):
    nums = sorted(v for v in values if _is_number(v))
    if not nums:
        return None
    n = len(nums)
    if n % 2 == 1:
        return nums[n // 2]
    return (nums[n // 2 - 1] + nums[n // 2]) / 2


def _apply_countunique(values):
    seen = set()
    for v in values:
        try:
            seen.add(v)
        except TypeError:
            seen.add(str(v))
    return len(seen)


_AGG_FUNCS = {
    'sum':         _apply_sum,
    'count':       _apply_count,
    'avg':         _apply_avg,
    'min':         _apply_min,
    'max':         _apply_max,
    'median':      _apply_median,
    'countunique': _apply_countunique,
}


_SQL_AGG = {
    'sum':         'SUM',
    'count':       'COUNT',
    'avg':         'AVG',
    'min':         'MIN',
    'max':         'MAX',
    'median':      'MEDIAN',
    'countunique': 'COUNT_DISTINCT',
}


# ============================================================
# БАЗОВЫЙ КЛАСС: условный агрегат
# ============================================================
class _CondAggBase(Node):
    agg_name = None

    def __init__(self, condition=None, value_col=None, by=None):
        self.condition = condition
        self.value_col = value_col
        self.by = by

    def evaluate(self, env):
        if self.by is not None:
            return self._evaluate_by(env)
        return self._evaluate_scalar(env)

    # ============================================================
    # MATRIX: скаляр
    # ============================================================
    def _evaluate_scalar(self, env):
        matrix_obj = self._extract_matrix(env)
        if matrix_obj is None:
            raise TypeError(
                f"{self.agg_name}if: не удалось определить матрицу."
            )

        if _is_duckdb(matrix_obj):
            return self._evaluate_scalar_duckdb(matrix_obj, env)

        value_col_idx = None
        if self.value_col is not None:
            value_col_idx = _resolve_column(matrix_obj, self.value_col, env)

        mask = _evaluate_condition_rows(matrix_obj, self.condition, env)

        if value_col_idx is not None:
            all_values = _get_column_values(matrix_obj, value_col_idx)
        else:
            all_values = [1] * len(mask)

        filtered = [v for v, ok in zip(all_values, mask) if ok]

        agg_fn = _AGG_FUNCS.get(self.agg_name)
        if agg_fn is None:
            raise ValueError(f"Неизвестный агрегат: {self.agg_name}")

        return agg_fn(filtered)

    # ============================================================
    # MATRIX: вектор (по группам)
    # ============================================================
    def _evaluate_by(self, env):
        matrix_obj = self._extract_matrix_by(env)
        if matrix_obj is None:
            raise TypeError(
                f"{self.agg_name}if: не удалось определить матрицу."
            )

        if _is_duckdb(matrix_obj):
            return self._evaluate_by_duckdb(matrix_obj, env)

        group_col_idx = _resolve_column(matrix_obj, self.by, env)
        value_col_idx = None
        if self.value_col is not None:
            value_col_idx = _resolve_column(matrix_obj, self.value_col, env)

        groups = _groups_by_column(matrix_obj, group_col_idx)

        if value_col_idx is not None:
            values = _get_column_values(matrix_obj, value_col_idx)
        else:
            values = [1] * len(groups)

        group_vals = {}
        for g, v in zip(groups, values):
            group_vals.setdefault(g, []).append(v)

        agg_fn = _AGG_FUNCS.get(self.agg_name)
        if agg_fn is None:
            raise ValueError(f"Неизвестный агрегат: {self.agg_name}")

        group_result = {g: agg_fn(vs) for g, vs in group_vals.items()}

        from runtime.matrix import MatrExMatrix
        result = [group_result[g] for g in groups]
        return MatrExMatrix(result, False)

    # ============================================================
    # DUCKDB: скаляр
    # ============================================================
    def _evaluate_scalar_duckdb(self, duck_table, env):
        from .filterif import _translate_to_sql, _resolve_column_for_duckdb

        columns = duck_table.get_columns()

        if self.condition is not None:
            where_sql = _translate_to_sql(self.condition, env, duck_table)
            where_part = f"WHERE {where_sql}"
        else:
            where_part = ""

        if self.value_col is not None:
            val_idx = _resolve_column_for_duckdb(
                columns, self._value_col_spec(env)
            )
            val_col = columns[val_idx]
            safe_val = '"' + str(val_col).replace('"', '""') + '"'
        else:
            safe_val = "*"

        sql_agg = _SQL_AGG.get(self.agg_name)
        if sql_agg is None:
            raise ValueError(f"Неизвестный агрегат: {self.agg_name}")

        if self.agg_name == 'countunique':
            expr = f'COUNT(DISTINCT {safe_val})'
        elif self.agg_name == 'count' and self.value_col is None:
            expr = 'COUNT(*)'
        else:
            expr = f'{sql_agg}(CAST({safe_val} AS DOUBLE))'

        sql = (
            f"SELECT {expr} FROM {duck_table.table_name} "
            f"{where_part}"
        )

        try:
            row = duck_table.con.execute(sql).fetchone()
        except Exception as e:
            raise RuntimeError(
                f"{self.agg_name}if: ошибка DuckDB: {e}\nSQL: {sql}"
            )

        if row is None or row[0] is None:
            if self.agg_name in ('sum', 'count', 'countunique'):
                return 0
            return None
        return row[0]

    # ============================================================
    # DUCKDB: вектор (по группам)
    # ============================================================
    def _evaluate_by_duckdb(self, duck_table, env):
        from .filterif import _resolve_column_for_duckdb
        from runtime.matrix import MatrExMatrix

        columns = duck_table.get_columns()

        grp_idx = _resolve_column_for_duckdb(columns, self._by_spec(env))
        grp_col = columns[grp_idx]
        safe_grp = '"' + str(grp_col).replace('"', '""') + '"'

        if self.value_col is not None:
            val_idx = _resolve_column_for_duckdb(
                columns, self._value_col_spec(env)
            )
            val_col = columns[val_idx]
            safe_val = '"' + str(val_col).replace('"', '""') + '"'
        else:
            safe_val = "*"

        sql_agg = _SQL_AGG.get(self.agg_name)
        if sql_agg is None:
            raise ValueError(f"Неизвестный агрегат: {self.agg_name}")

        if self.agg_name == 'countunique':
            expr = f'COUNT(DISTINCT {safe_val})'
        elif self.agg_name == 'count' and self.value_col is None:
            expr = 'COUNT(*)'
        else:
            expr = f'{sql_agg}(CAST({safe_val} AS DOUBLE))'

        sql = f"""
            SELECT
                {expr} OVER (PARTITION BY {safe_grp}) AS __val
            FROM (
                SELECT *, ROW_NUMBER() OVER () AS __orig_row
                FROM {duck_table.table_name}
            )
            ORDER BY __orig_row
        """

        try:
            rows = duck_table.con.execute(sql).fetchall()
        except Exception as e:
            raise RuntimeError(
                f"{self.agg_name}if by: ошибка DuckDB: {e}\nSQL: {sql}"
            )

        values = [r[0] for r in rows]
        return MatrExMatrix(values, False)

    # ============================================================
    # ПОИСК MATRIX
    # ============================================================
    def _extract_matrix(self, env):
        from ast_nodes.index import IndexNode
        from ast_nodes.operations import BinaryOp, UnaryOp

        def _find_in_node(node):
            if node is None:
                return None
            if isinstance(node, IndexNode):
                try:
                    return node.matrix.evaluate(env)
                except Exception:
                    pass
            if isinstance(node, BinaryOp):
                left = _find_in_node(node.left)
                if left is not None:
                    return left
                return _find_in_node(node.right)
            if isinstance(node, UnaryOp):
                return _find_in_node(node.right)
            return None

        for node in (self.condition, self.value_col):
            result = _find_in_node(node)
            if result is not None:
                return result
        return None

    def _extract_matrix_by(self, env):
        from ast_nodes.index import IndexNode
        from ast_nodes.operations import BinaryOp, UnaryOp

        def _find_in_node(node):
            if node is None:
                return None
            if isinstance(node, IndexNode):
                try:
                    return node.matrix.evaluate(env)
                except Exception:
                    pass
            if isinstance(node, BinaryOp):
                left = _find_in_node(node.left)
                if left is not None:
                    return left
                return _find_in_node(node.right)
            if isinstance(node, UnaryOp):
                return _find_in_node(node.right)
            return None

        for node in (self.by, self.value_col):
            result = _find_in_node(node)
            if result is not None:
                return result
        return None

    # ============================================================
    # СПЕЦИФИКАЦИИ СТОЛБЦОВ
    # ============================================================
    def _value_col_spec(self, env):
        from ast_nodes.index import IndexNode
        if (isinstance(self.value_col, IndexNode)
                and len(self.value_col.indices) == 2):
            spec = self.value_col.indices[1]
            return spec.evaluate(env) if hasattr(spec, 'evaluate') else spec
        raise TypeError(
            f"{self.agg_name}if: value_col — срез m[:, \"X\"]."
        )

    def _by_spec(self, env):
        from ast_nodes.index import IndexNode
        if isinstance(self.by, IndexNode) and len(self.by.indices) == 2:
            spec = self.by.indices[1]
            return spec.evaluate(env) if hasattr(spec, 'evaluate') else spec
        raise TypeError(
            f"{self.agg_name}if by: by — срез m[:, \"X\"]."
        )

    def __repr__(self):
        if self.by is not None:
            return f"{self.agg_name}if(by {self.by}, {self.value_col})"
        return f"{self.agg_name}if({self.condition}, {self.value_col})"


# ============================================================
# КОНКРЕТНЫЕ КЛАССЫ
# ============================================================
class SumIfNode(_CondAggBase):
    agg_name = 'sum'


class CountIfNode(_CondAggBase):
    agg_name = 'count'


class AvgIfNode(_CondAggBase):
    agg_name = 'avg'


class MinIfNode(_CondAggBase):
    agg_name = 'min'


class MaxIfNode(_CondAggBase):
    agg_name = 'max'


class MedianIfNode(_CondAggBase):
    agg_name = 'median'


class CountUniqueIfNode(_CondAggBase):
    agg_name = 'countunique'


# ============================================================
# SUMPRODUCT
# ============================================================
class SumProductNode(Node):
    def __init__(self, columns):
        self.columns = columns

    def evaluate(self, env):
        if not self.columns:
            raise TypeError("sumproduct: нужен хотя бы один срез.")

        matrix_obj = self._extract_matrix(env)
        if matrix_obj is None:
            raise TypeError("sumproduct: не удалось определить матрицу.")

        if _is_duckdb(matrix_obj):
            return self._evaluate_duckdb(matrix_obj, env)

        return self._evaluate_matrix(matrix_obj, env)

    def _extract_matrix(self, env):
        from ast_nodes.index import IndexNode
        for node in self.columns:
            if isinstance(node, IndexNode):
                try:
                    return node.matrix.evaluate(env)
                except Exception:
                    pass
        return None

    def _evaluate_matrix(self, matrix_obj, env):
        col_idxs = [
            _resolve_column(matrix_obj, c, env) for c in self.columns
        ]

        total = 0.0
        for i in range(1, matrix_obj.rows):
            row = matrix_obj.data[i]
            product = 1.0
            ok = True
            for ci in col_idxs:
                v = row[ci] if ci < len(row) else None
                if not _is_number(v):
                    ok = False
                    break
                product *= v
            if ok:
                total += product
        return total

    def _evaluate_duckdb(self, duck_table, env):
        from .filterif import _resolve_column_for_duckdb

        columns = duck_table.get_columns()
        parts = []
        for node in self.columns:
            idx = self._resolve_duckdb_col(node, columns, env)
            col_name = columns[idx]
            safe = '"' + str(col_name).replace('"', '""') + '"'
            parts.append(f'CAST({safe} AS DOUBLE)')

        expr = " * ".join(parts)
        sql = f"SELECT SUM({expr}) FROM {duck_table.table_name}"

        try:
            row = duck_table.con.execute(sql).fetchone()
        except Exception as e:
            raise RuntimeError(
                f"sumproduct: ошибка DuckDB: {e}\nSQL: {sql}"
            )

        return row[0] if row and row[0] is not None else 0

    def _resolve_duckdb_col(self, node, columns, env):
        from ast_nodes.index import IndexNode
        from .filterif import _resolve_column_for_duckdb

        if not isinstance(node, IndexNode) or len(node.indices) != 2:
            raise TypeError(
                "sumproduct: аргументы — срезы m[:, \"X\"]."
            )
        spec = node.indices[1]
        val = spec.evaluate(env) if hasattr(spec, 'evaluate') else spec
        return _resolve_column_for_duckdb(columns, val)

    def __repr__(self):
        return f"sumproduct({', '.join(str(c) for c in self.columns)})"