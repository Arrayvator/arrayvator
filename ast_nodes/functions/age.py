# ast_nodes/functions/age.py
"""
Функция AGE — упрощённый аналог DateDiff.

ОТЛИЧИЯ ОТ DateDiff:
    • формат всегда "DD.MM.YYYY" — не нужно указывать
    • единица измерения опциональна, по умолчанию "years"

СИНТАКСИС:
    age(дата1, дата2)              → полных лет
    age(дата1, дата2, "years")     → полных лет
    age(дата1, дата2, "months")    → полных месяцев
    age(дата1, дата2, "days")      → полных дней
    age(дата1, дата2, "all")       → "5 лет 7 месяцев 1 день"

ПРАВИЛА:
    - Считаются ПОЛНЫЕ прошедшие периоды.
    - Если хотя бы одного дня не хватает — период не полный.
    - Формат всегда DD.MM.YYYY.
"""

from ..base import Node

# ============================================================
# Используем хелперы из datediff (не дублируем код)
# ============================================================
from .datediff import (
    _parse_date,
    _to_list,
    _calc_diff,
)


DEFAULT_FORMAT = "DD.MM.YYYY"
DEFAULT_UNIT = "years"


class AgeNode(Node):
    def __init__(self, date1, date2, unit=None):
        self.date1 = date1
        self.date2 = date2
        self.unit = unit

    def evaluate(self, env):
        from runtime.matrix import MatrExMatrix

        # ============================================================
        # 1. Единица измерения (по умолчанию "years")
        # ============================================================
        unit_val = DEFAULT_UNIT
        if self.unit is not None:
            try:
                unit_val = (self.unit.evaluate(env)
                            if hasattr(self.unit, 'evaluate')
                            else self.unit)
            except Exception:
                unit_val = None

        if not isinstance(unit_val, str):
            return None

        # ============================================================
        # 2. Формат — всегда DD.MM.YYYY
        # ============================================================
        format_val = DEFAULT_FORMAT

        # ============================================================
        # 3. Значения
        # ============================================================
        try:
            date1_val = (self.date1.evaluate(env)
                         if hasattr(self.date1, 'evaluate')
                         else self.date1)
        except Exception:
            date1_val = None

        try:
            date2_val = (self.date2.evaluate(env)
                         if hasattr(self.date2, 'evaluate')
                         else self.date2)
        except Exception:
            date2_val = None

        # ============================================================
        # 4. Оба скаляры
        # ============================================================
        if (not isinstance(date1_val, list)
                and not hasattr(date1_val, 'data')
                and not isinstance(date2_val, list)
                and not hasattr(date2_val, 'data')):
            d1 = _parse_date(date1_val, format_val)
            d2 = _parse_date(date2_val, format_val)
            return _calc_diff(d1, d2, unit_val)

        # ============================================================
        # 5. Приводим оба к списку
        # ============================================================
        list1 = _to_list(date1_val)
        list2 = _to_list(date2_val)

        # ============================================================
        # 6. Поэлементно
        # ============================================================
        n = max(len(list1), len(list2))
        results = []
        for i in range(n):
            v1 = list1[i] if i < len(list1) else None
            v2 = list2[i] if i < len(list2) else None

            d1 = _parse_date(v1, format_val)
            d2 = _parse_date(v2, format_val)
            results.append(_calc_diff(d1, d2, unit_val))

        # ============================================================
        # 7. Один элемент → скаляр
        # ============================================================
        if len(results) == 1:
            return results[0]

        # ============================================================
        # 8. Вектор
        # ============================================================
        return MatrExMatrix(results, False)

    def __repr__(self):
        if self.unit is None:
            return f"age({self.date1}, {self.date2})"
        return f"age({self.date1}, {self.date2}, {self.unit})"