# ast_nodes/functions/statistical.py
"""
Статистические функции: sum, min, max, avg, count, median, std.

ДВА РЕЖИМА КАЖДОЙ ФУНКЦИИ:

    Без by — СКАЛЯР (по всей таблице):
        r = sum(m[:, "Зарплата"])
        r = avg(m[:, "Зарплата"])
        r = count(m[:, "Зарплата"])
        r = min(m[:, "Зарплата"])
        r = max(m[:, "Зарплата"])
        r = median(m[:, "Зарплата"])
        r = std(m[:, "Зарплата"])

    С by — ВЕКТОР (по группам, длина = число строк):
        r = sum(m[:, "Зарплата"], by m[:, "Отдел"])
        r = avg(m[:, "Зарплата"], by m[:, "Отдел"])
        r = count(m[:, "Зарплата"], by m[:, "Отдел"])
        ...

    count() без аргумента — количество строк в группе (или всей таблице).

РЕАЛИЗАЦИЯ:
    Логика групповой агрегации уже реализована в _CondAggBase
    (см. ast_nodes/functions/conditional_agg.py).
    Здесь мы просто делегируем вызовы в SumIfNode / AvgIfNode / ...
"""

from ..base import Node
from runtime.random_source import forbid_random


# ============================================================
# ХЕЛПЕР: делегирование в условный агрегат
# ============================================================
def _delegate_cond_agg(agg_name, arg, by, env):
    """
    Делегирует вычисление в соответствующий *IfNode.

    agg_name — 'sum' | 'avg' | 'min' | 'max' | 'count' | 'median' | 'std'
    arg      — узел значения (IndexNode) или None (для count())
    by       — узел ключа группировки (IndexNode) или None
    env      — окружение
    """
    from .conditional_agg import (
        SumIfNode,
        AvgIfNode,
        MinIfNode,
        MaxIfNode,
        CountIfNode,
        MedianIfNode,
    )

    # ------------------------------------------------------------
    # ПРОВЕРКА: если arg задан — должен быть срез m[:, "X"]
    # ------------------------------------------------------------
    if arg is not None:
        from ast_nodes.index import IndexNode
        if not isinstance(arg, IndexNode):
            raise TypeError(
                f"{agg_name}: аргумент должен быть срезом m[:, \"X\"],\n"
                f"  получен {type(arg).__name__}.\n"
                f"  Пример: {agg_name}(m[:, \"Зарплата\"])"
            )

    # ------------------------------------------------------------
    # ПРОВЕРКА: если by задан — должен быть срезом m[:, "X"]
    # ------------------------------------------------------------
    if by is not None:
        from ast_nodes.index import IndexNode
        if not isinstance(by, IndexNode):
            raise TypeError(
                f"{agg_name} by: ключ группировки должен быть срезом "
                f"m[:, \"X\"],\n"
                f"  получен {type(by).__name__}.\n"
                f"  Пример: {agg_name}(m[:, \"Зарплата\"], by m[:, \"Отдел\"])"
            )

    # ------------------------------------------------------------
    # ВЫБОР КЛАССА
    # ------------------------------------------------------------
    if agg_name == 'sum':
        node = SumIfNode(condition=None, value_col=arg, by=by)
    elif agg_name == 'avg':
        node = AvgIfNode(condition=None, value_col=arg, by=by)
    elif agg_name == 'min':
        node = MinIfNode(condition=None, value_col=arg, by=by)
    elif agg_name == 'max':
        node = MaxIfNode(condition=None, value_col=arg, by=by)
    elif agg_name == 'count':
        node = CountIfNode(condition=None, value_col=arg, by=by)
    elif agg_name == 'median':
        node = MedianIfNode(condition=None, value_col=arg, by=by)
    elif agg_name == 'std':
        return _evaluate_std(arg, by, env)
    else:
        raise ValueError(f"Неизвестный агрегат: {agg_name}")

    return node.evaluate(env)


# ============================================================
# STD — собственная реализация
# ============================================================
def _evaluate_std(arg, by, env):
    """Стандартное отклонение (population, делитель N)."""
    from ast_nodes.index import IndexNode
    from .conditional_agg import (
        _resolve_column,
        _get_column_values,
        _groups_by_column,
        _is_duckdb,
    )
    from runtime.matrix import MatrExMatrix
    import math

    if arg is None:
        raise TypeError(
            "std: нужен срез значений.\n"
            "  Пример: std(m[:, \"Зарплата\"])"
        )
    if not isinstance(arg, IndexNode):
        raise TypeError(
            "std: аргумент должен быть срезом m[:, \"X\"]."
        )

    matrix_obj = arg.matrix.evaluate(env)

    if _is_duckdb(matrix_obj):
        return _std_duckdb(matrix_obj, arg, by, env)

    if not hasattr(matrix_obj, 'data') or not matrix_obj.is_2d:
        raise TypeError("std: ожидается матрица.")

    col_idx = _resolve_column(matrix_obj, arg, env)
    values = _get_column_values(matrix_obj, col_idx)

    # --- Без by: скаляр ---
    if by is None:
        nums = [v for v in values
                if isinstance(v, (int, float)) and not isinstance(v, bool)]
        if len(nums) < 2:
            return 0
        mean = sum(nums) / len(nums)
        var = sum((x - mean) ** 2 for x in nums) / len(nums)
        return math.sqrt(var)

    # --- С by: вектор ---
    if not isinstance(by, IndexNode):
        raise TypeError("std by: ключ — срез m[:, \"X\"].")

    group_col_idx = _resolve_column(matrix_obj, by, env)
    groups = _groups_by_column(matrix_obj, group_col_idx)

    group_vals = {}
    for g, v in zip(groups, values):
        group_vals.setdefault(g, []).append(v)

    group_std = {}
    for g, vs in group_vals.items():
        nums = [x for x in vs
                if isinstance(x, (int, float)) and not isinstance(x, bool)]
        if len(nums) < 2:
            group_std[g] = 0
            continue
        mean = sum(nums) / len(nums)
        var = sum((x - mean) ** 2 for x in nums) / len(nums)
        group_std[g] = math.sqrt(var)

    result = [group_std[g] for g in groups]
    return MatrExMatrix(result, False)


def _std_duckdb(duck_table, arg, by, env):
    """std для DuckDB."""
    from .filterif import _resolve_column_for_duckdb
    from runtime.matrix import MatrExMatrix

    columns = duck_table.get_columns()

    val_spec_node = arg.indices[1]
    val_spec = (val_spec_node.evaluate(env)
                if hasattr(val_spec_node, 'evaluate')
                else val_spec_node)
    val_idx = _resolve_column_for_duckdb(columns, val_spec)
    val_col = columns[val_idx]
    safe_val = '"' + str(val_col).replace('"', '""') + '"'

    if by is None:
        sql = (
            f"SELECT STDDEV_POP(CAST({safe_val} AS DOUBLE)) "
            f"FROM {duck_table.table_name}"
        )
        try:
            row = duck_table.con.execute(sql).fetchone()
        except Exception as e:
            raise RuntimeError(f"std: ошибка DuckDB: {e}\nSQL: {sql}")
        return row[0] if row and row[0] is not None else 0

    from ast_nodes.index import IndexNode
    if not isinstance(by, IndexNode):
        raise TypeError("std by: ключ — срез m[:, \"X\"].")

    by_spec_node = by.indices[1]
    by_spec = (by_spec_node.evaluate(env)
               if hasattr(by_spec_node, 'evaluate')
               else by_spec_node)
    by_idx = _resolve_column_for_duckdb(columns, by_spec)
    by_col = columns[by_idx]
    safe_by = '"' + str(by_col).replace('"', '""') + '"'

    sql = f"""
        SELECT
            STDDEV_POP(CAST({safe_val} AS DOUBLE))
            OVER (PARTITION BY {safe_by}) AS __val
        FROM (
            SELECT *, ROW_NUMBER() OVER () AS __orig_row
            FROM {duck_table.table_name}
        )
        ORDER BY __orig_row
    """

    try:
        rows = duck_table.con.execute(sql).fetchall()
    except Exception as e:
        raise RuntimeError(f"std by: ошибка DuckDB: {e}\nSQL: {sql}")

    values = [r[0] if r[0] is not None else 0 for r in rows]
    return MatrExMatrix(values, False)


# ============================================================
# SUM
# ============================================================
class SumNode(Node):
    def __init__(self, arg, by=None):
        self.arg = arg
        self.by = by

    def evaluate(self, env):
        if self.by is not None:
            return _delegate_cond_agg('sum', self.arg, self.by, env)

        value = self.arg.evaluate(env)
        forbid_random(value, "sum")

        nums = _collect_numbers(value)
        return sum(nums) if nums else 0

    def __repr__(self):
        if self.by is not None:
            return f"sum({self.arg}, by {self.by})"
        return f"sum({self.arg})"


# ============================================================
# MIN
# ============================================================
class MinNode(Node):
    def __init__(self, arg, by=None):
        self.arg = arg
        self.by = by

    def evaluate(self, env):
        if self.by is not None:
            return _delegate_cond_agg('min', self.arg, self.by, env)

        value = self.arg.evaluate(env)
        forbid_random(value, "min")

        nums = _collect_numbers(value)
        return min(nums) if nums else 0

    def __repr__(self):
        if self.by is not None:
            return f"min({self.arg}, by {self.by})"
        return f"min({self.arg})"


# ============================================================
# MAX
# ============================================================
class MaxNode(Node):
    def __init__(self, arg, by=None):
        self.arg = arg
        self.by = by

    def evaluate(self, env):
        if self.by is not None:
            return _delegate_cond_agg('max', self.arg, self.by, env)

        value = self.arg.evaluate(env)
        forbid_random(value, "max")

        nums = _collect_numbers(value)
        return max(nums) if nums else 0

    def __repr__(self):
        if self.by is not None:
            return f"max({self.arg}, by {self.by})"
        return f"max({self.arg})"


# ============================================================
# AVG
# ============================================================
class AvgNode(Node):
    def __init__(self, arg, by=None):
        self.arg = arg
        self.by = by

    def evaluate(self, env):
        if self.by is not None:
            return _delegate_cond_agg('avg', self.arg, self.by, env)

        value = self.arg.evaluate(env)
        forbid_random(value, "avg")

        nums = _collect_numbers(value)
        return sum(nums) / len(nums) if nums else 0

    def __repr__(self):
        if self.by is not None:
            return f"avg({self.arg}, by {self.by})"
        return f"avg({self.arg})"


# ============================================================
# COUNT
# ============================================================
class CountNode(Node):
    def __init__(self, arg=None, by=None):
        self.arg = arg
        self.by = by

    def evaluate(self, env):
        if self.by is not None:
            return _delegate_cond_agg('count', self.arg, self.by, env)

        if self.arg is None:
            raise TypeError(
                "count(): укажите срез значений или by-ключ.\n"
                "  Примеры:\n"
                "     count(m[:, \"Зарплата\"])              — непустые\n"
                "     count(m[:, \"Зарплата\"], by m[:, \"Отдел\"])"
            )

        value = self.arg.evaluate(env)
        forbid_random(value, "count")

        if hasattr(value, 'data') and hasattr(value, 'is_2d'):
            if value.is_2d:
                return sum(1 for row in value.data
                           for v in row if v is not None)
            else:
                return sum(1 for v in value.data if v is not None)

        if isinstance(value, list):
            return sum(1 for v in value if v is not None)

        return 0 if value is None else 1

    def __repr__(self):
        if self.by is not None:
            return f"count({self.arg}, by {self.by})"
        if self.arg is not None:
            return f"count({self.arg})"
        return "count()"


# ============================================================
# MEDIAN
# ============================================================
class MedianNode(Node):
    def __init__(self, arg, by=None):
        self.arg = arg
        self.by = by

    def evaluate(self, env):
        if self.by is not None:
            return _delegate_cond_agg('median', self.arg, self.by, env)

        value = self.arg.evaluate(env)
        forbid_random(value, "median")

        nums = sorted(_collect_numbers(value))
        if not nums:
            return 0
        n = len(nums)
        if n % 2 == 1:
            return nums[n // 2]
        return (nums[n // 2 - 1] + nums[n // 2]) / 2

    def __repr__(self):
        if self.by is not None:
            return f"median({self.arg}, by {self.by})"
        return f"median({self.arg})"


# ============================================================
# STD
# ============================================================
class StdNode(Node):
    def __init__(self, arg, by=None):
        self.arg = arg
        self.by = by

    def evaluate(self, env):
        return _evaluate_std(self.arg, self.by, env)

    def __repr__(self):
        if self.by is not None:
            return f"std({self.arg}, by {self.by})"
        return f"std({self.arg})"


# ============================================================
# ХЕЛПЕР: сбор чисел
# ============================================================
def _collect_numbers(value):
    """Собирает все числа из скаляра/вектора/матрицы/списка."""
    nums = []

    if isinstance(value, (int, float)) and not isinstance(value, bool):
        nums.append(value)
        return nums

    if hasattr(value, 'data') and hasattr(value, 'is_2d'):
        if value.is_2d:
            for row in value.data:
                for v in row:
                    if isinstance(v, (int, float)) and not isinstance(v, bool):
                        nums.append(v)
        else:
            for v in value.data:
                if isinstance(v, (int, float)) and not isinstance(v, bool):
                    nums.append(v)
        return nums

    if isinstance(value, list):
        for v in value:
            if isinstance(v, (int, float)) and not isinstance(v, bool):
                nums.append(v)
        return nums

    return nums