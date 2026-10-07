# parser/parse_functions/applyif.py
"""
Парсинг APPLYIF.

СИНТАКСИС:
    applyif(условие, m[:, "X"] = значение)
    applyif(условие, m[:, end+1] = значение)

ПРИМЕРЫ:
    r = applyif(m[:, "Отдел"] == "IT", m[:, "Статус"] = "VIP")
    m = applyif(m[:, "Отдел"] == "IT", m[:, "Статус"] = "VIP")
    r = applyif(m[2:10, "Отдел"] == "IT", m[:, "Статус"] = "VIP")
    r = applyif(m[:, "Отдел"] == "IT" and m[:, "Возраст"] > 30,
                m[:, "Статус"] = "VIP")
"""

from ast_nodes import ApplyIfNode
from ast_nodes.index import IndexNode
from errors import ArrayVatorError


def parse_applyif(self):
    """Парсинг APPLYIF"""
    self.expect('LPAREN')

    # ============================================================
    # 1. Условие
    # ============================================================
    try:
        condition = self.parse_expression()
    except Exception:
        raise ArrayVatorError(
            code="APPLYIF_BAD_SYNTAX",
            context=self._get_context(),
        )

    # ============================================================
    # 2. Запятая после условия
    # ============================================================
    if not self.check('COMMA'):
        raise ArrayVatorError(
            code="APPLYIF_BAD_SYNTAX",
            context=self._get_context(),
        )
    self.expect('COMMA')

    # ============================================================
    # 3. Целевой срез — m[:, "X"] или m[:, end+1]
    # ============================================================
    try:
        target = self.parse_primary()
    except Exception:
        raise ArrayVatorError(
            code="APPLYIF_BAD_TARGET",
            context=self._get_context(),
        )

    if not isinstance(target, IndexNode):
        raise ArrayVatorError(
            code="APPLYIF_BAD_TARGET",
            context=self._get_context(),
        )

    # ============================================================
    # 4. Оператор = (обязателен)
    # ============================================================
    if not self.check('ASSIGN'):
        raise ArrayVatorError(
            code="APPLYIF_NEED_ASSIGN",
            context=self._get_context(),
        )
    self.expect('ASSIGN')

    # ============================================================
    # 5. Значение
    # ============================================================
    value = self.parse_expression()

    self.expect('RPAREN')
    return ApplyIfNode(condition, target, value)