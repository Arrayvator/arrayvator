"""
Функция VLOOKUP — аналог ВПР.

СИНТАКСИС:
    vlookup(срез_поиска, что_искать, срез_возврата)

МНЕМОНИКА:
    vlookup( где_искать, что_искать, что_возвращать )
             └── a ───┘  └── b ───┘  └── a ───┘
             справочник    запрос     справочник

ЛОГИКА:
    1. Берём каждое значение из "что_искать".
    2. Ищем его в "срез_поиска".
    3. Найденная позиция i даёт строку в справочнике.
    4. Возвращаем значение из "срез_возврата" этой строки.

ВОЗВРАЩАЕТ:
    - Скаляр: если что_искать — скаляр.
    - Вектор: если что_искать — вектор.
    - None: если не найдено.

ПРАВИЛА СРАВНЕНИЯ:
    - Строки — без учёта регистра.
    - Числа — с приведением типов (101 == "101").
    - None можно найти, только если искать None.
    - При дубликатах ключа — берётся ПЕРВОЕ совпадение.
"""

from ..base import Node
from runtime.matrix import MatrExMatrix
from ..utils.index_utils import resolve_column_index


class VLookupNode(Node):
    def __init__(self, search_val, search_slice, return_slice):
        self.search_val = search_val
        self.search_slice = search_slice      # срез поиска (a[:, "ID"])
        self.return_slice = return_slice      # срез возврата (a[:, "Отдел"])

    # ============================================================
    # ХЕЛПЕР: разбор среза → (таблица, индекс столбца, значения)
    # ============================================================
    def _resolve_slice(self, index_node, env):
        """
        Из IndexNode вида a[:, "X"] извлекает:
            (matrix_obj, col_idx, values)

        Где:
            matrix_obj — таблица справочника,
            col_idx    — 0-based индекс столбца,
            values     — список значений столбца БЕЗ заголовка.
        """
        matrix_obj = index_node.matrix.evaluate(env)

        col_spec_node = index_node.indices[1]
        col_spec = (col_spec_node.evaluate(env)
                    if hasattr(col_spec_node, 'evaluate')
                    else col_spec_node)

        col_idx, _ = resolve_column_index(matrix_obj, col_spec, env)

        values = []
        for i in range(1, matrix_obj.rows):
            row = matrix_obj.data[i]
            if col_idx < len(row):
                values.append(row[col_idx])
            else:
                values.append(None)

        return (matrix_obj, col_idx, values)

    # ============================================================
    # СРАВНЕНИЕ ЗНАЧЕНИЙ
    # ============================================================
    def _compare(self, a, b):
        """Сравнивает два значения с приведением типов."""
        if a is None and b is None:
            return True
        if a is None or b is None:
            return False

        # Оба числа
        if isinstance(a, (int, float)) and isinstance(b, (int, float)):
            return a == b

        # Обе строки — без учёта регистра
        if isinstance(a, str) and isinstance(b, str):
            return a.strip().lower() == b.strip().lower()

        # Строка + число → пробуем как число
        if isinstance(a, str) and isinstance(b, (int, float)):
            try:
                return float(a.strip()) == b
            except (ValueError, TypeError):
                return False

        if isinstance(a, (int, float)) and isinstance(b, str):
            try:
                return a == float(b.strip())
            except (ValueError, TypeError):
                return False

        return False

    # ============================================================
    # ПОИСК ОДНОГО ЗНАЧЕНИЯ
    # ============================================================
    def _find_one(self, search_val, search_values, return_values):
        """
        Ищет search_val в search_values.
        Возвращает соответствующее значение из return_values.
        Или None, если не найдено.
        """
        if search_val is None:
            # Ищем None
            for i, item in enumerate(search_values):
                if item is None:
                    return return_values[i]
            return None

        for i, item in enumerate(search_values):
            if self._compare(item, search_val):
                return return_values[i]

        return None

    # ============================================================
    # EVALUATE
    # ============================================================
    def evaluate(self, env):
        # 1. Разбираем срез поиска
        search_matrix, search_col_idx, search_values = \
            self._resolve_slice(self.search_slice, env)

        # 2. Разбираем срез возврата
        return_matrix, return_col_idx, return_values = \
            self._resolve_slice(self.return_slice, env)

        # 3. Что искать
        val = (self.search_val.evaluate(env)
               if hasattr(self.search_val, 'evaluate')
               else self.search_val)

        # 4. Если скаляр — возвращаем скаляр
        if not (hasattr(val, 'data') and not val.is_2d):
            return self._find_one(val, search_values, return_values)

        # 5. Если вектор — возвращаем вектор
        results = []
        for v in val.data:
            results.append(self._find_one(v, search_values, return_values))

        return MatrExMatrix(results, False)

    def __repr__(self):
        return f"vlookup({self.search_slice}, {self.search_val}, {self.return_slice})"