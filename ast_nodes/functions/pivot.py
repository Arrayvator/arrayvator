# ast_nodes/functions/pivot.py
"""
Функция PIVOT — сводная таблица.

ДВА РЕЖИМА:
    3 аргумента — один ключ. Простая сводка (2 столбца).
    4 аргумента — два ключа. Pivot-таблица (строки × столбцы).

АГРЕГАТЫ:
    sum, avg, count, min, max, median, first, last, std

ПРАВИЛА:
    - Порядок строк/столбцов — по первому появлению.
    - Пустые ячейки → None.
    - Заголовки:
        * 1 ключ: Ключ, Значение (или имена столбцов).
        * 2 ключа: имя 1-го ключа + значения 2-го ключа.
"""

from ..base import Node
from runtime.matrix import MatrExMatrix


# ============================================================
# АГРЕГАЦИЯ
# ============================================================
def _aggregate(values, agg_name):
    """Применяет агрегат к списку значений."""
    if not values:
        if agg_name == 'count':
            return 0
        return None

    if agg_name == 'count':
        return len(values)

    nums = []
    for v in values:
        if isinstance(v, (int, float)) and not isinstance(v, bool):
            nums.append(v)

    if not nums:
        return None

    if agg_name == 'sum':
        return sum(nums)
    if agg_name == 'avg':
        return sum(nums) / len(nums)
    if agg_name == 'min':
        return min(nums)
    if agg_name == 'max':
        return max(nums)
    if agg_name == 'median':
        s = sorted(nums)
        n = len(s)
        if n % 2 == 1:
            return s[n // 2]
        return (s[n // 2 - 1] + s[n // 2]) / 2
    if agg_name == 'first':
        return nums[0]
    if agg_name == 'last':
        return nums[-1]
    if agg_name == 'std':
        mean = sum(nums) / len(nums)
        var = sum((x - mean) ** 2 for x in nums) / len(nums)
        return var ** 0.5

    return None


# ============================================================
# ИЗВЛЕЧЕНИЕ ДАННЫХ ИЗ СРЕЗА
# ============================================================
def _extract_column(index_node, env):
    """
    Из IndexNode вида m[:, "X"] извлекает:
        (matrix_obj, col_idx, values, column_name)
    Где values — список БЕЗ заголовка,
        column_name — имя столбца (для заголовка результата).
    """
    matrix_obj = index_node.matrix.evaluate(env)

    col_spec_node = index_node.indices[1]
    col_spec = (col_spec_node.evaluate(env)
                if hasattr(col_spec_node, 'evaluate')
                else col_spec_node)

    # Индекс столбца
    if isinstance(col_spec, (int, float)):
        col_idx = int(col_spec) - 1
        column_name = None
    else:
        # Ищем по имени в заголовке
        from ..utils.index_utils import resolve_column_index
        col_idx, _ = resolve_column_index(matrix_obj, col_spec, env)
        column_name = col_spec

    # Значения (без заголовка)
    values = []
    for i in range(1, matrix_obj.rows):
        row = matrix_obj.data[i]
        if col_idx < len(row):
            values.append(row[col_idx])
        else:
            values.append(None)

    # Если имя не найдено — берём из заголовка
    if column_name is None and matrix_obj.rows > 0:
        header = matrix_obj.data[0]
        if col_idx < len(header):
            column_name = header[col_idx]

    return (matrix_obj, col_idx, values, column_name)


# ============================================================
# PIVOT NODE
# ============================================================
class PivotNode(Node):
    def __init__(self, data=None, key1=None, key2=None,
                 values=None, agg=None, **kwargs):
        self.key1 = key1
        self.key2 = key2
        self.values = values
        self.agg = agg

    def evaluate(self, env):
        # ------------------------------------------------------------
        # Имя агрегата
        # ------------------------------------------------------------
        agg_name = 'sum'
        if self.agg is not None:
            agg_val = (self.agg.evaluate(env)
                       if hasattr(self.agg, 'evaluate')
                       else self.agg)
            if isinstance(agg_val, str):
                agg_name = agg_val.lower().strip()

        # ------------------------------------------------------------
        # Извлекаем данные из срезов
        # ------------------------------------------------------------
        _, _, keys1, name1 = _extract_column(self.key1, env)
        _, _, vals, name_val = _extract_column(self.values, env)

        # ============================================================
        # РЕЖИМ 1: ОДИН КЛЮЧ
        # ============================================================
        if self.key2 is None:
            return self._pivot_single(keys1, vals, agg_name, name1)

        # ============================================================
        # РЕЖИМ 2: ДВА КЛЮЧА
        # ============================================================
        _, _, keys2, name2 = _extract_column(self.key2, env)

        return self._pivot_double(
            keys1, keys2, vals,
            agg_name, name1, name2
        )

    # ============================================================
    # ОДИН КЛЮЧ
    # ============================================================
    def _pivot_single(self, keys, values, agg_name, name1):
        """
        Простая сводка: 2 столбца.
        Результат:
            Ключ     Значение
            IT       250000
            HR       137000
            ...
        """
        header_key = name1 if name1 else "Ключ"
        header_val = "Значение"

        groups = {}
        order = []

        n = min(len(keys), len(values))
        for i in range(n):
            key = keys[i]
            val = values[i]

            if key not in groups:
                groups[key] = []
                order.append(key)
            groups[key].append(val)

        result = [[header_key, header_val]]

        for key in order:
            agg_result = _aggregate(groups[key], agg_name)
            result.append([key, agg_result])

        return MatrExMatrix(result, True)

    # ============================================================
    # ДВА КЛЮЧА
    # ============================================================
    def _pivot_double(self, keys1, keys2, values,
                      agg_name, name1, name2):
        """
        Pivot-таблица: строки × столбцы.
        Результат:
            Отдел   2023     2024
            IT      180000   70000
            HR      65000    72000
            ...
        """
        # ------------------------------------------------------------
        # Собираем группы
        # groups[(k1, k2)] = [val, val, ...]
        # ------------------------------------------------------------
        groups = {}
        row_keys = []      # порядок строк
        col_keys = []      # порядок столбцов

        n = min(len(keys1), len(keys2), len(values))
        for i in range(n):
            k1 = keys1[i]
            k2 = keys2[i]
            val = values[i]

            if k1 not in row_keys:
                row_keys.append(k1)
            if k2 not in col_keys:
                col_keys.append(k2)

            key = (k1, k2)
            if key not in groups:
                groups[key] = []
            groups[key].append(val)

        # ------------------------------------------------------------
        # Формируем заголовок
        # ------------------------------------------------------------
        header_row = name1 if name1 else "Ключ"
        header = [header_row] + list(col_keys)

        # ------------------------------------------------------------
        # Формируем строки
        # ------------------------------------------------------------
        result = [header]

        for rk in row_keys:
            row = [rk]
            for ck in col_keys:
                key = (rk, ck)
                if key in groups:
                    agg_result = _aggregate(groups[key], agg_name)
                else:
                    agg_result = None
                row.append(agg_result)
            result.append(row)

        return MatrExMatrix(result, True)

    def __repr__(self):
        if self.key2 is not None:
            return (f"pivot({self.key1}, {self.key2}, "
                    f"{self.values}, {self.agg})")
        return f"pivot({self.key1}, {self.values}, {self.agg})"