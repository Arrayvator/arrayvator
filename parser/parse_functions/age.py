# parser/parse_functions/age.py
"""
Парсинг AGE.

СИНТАКСИС:
    age(дата1, дата2)              — полных лет (по умолчанию)
    age(дата1, дата2, "years")     — полных лет
    age(дата1, дата2, "months")    — полных месяцев
    age(дата1, дата2, "days")      — полных дней
    age(дата1, дата2, "all")       — "5 лет 7 месяцев 1 день"
"""

from ast_nodes import AgeNode
from errors import ArrayVatorError


def parse_age(self):
    self.expect('LPAREN')

    # ============================================================
    # 1. Первая дата
    # ============================================================
    if self.check('RPAREN'):
        raise ArrayVatorError(
            code="AGE_BAD_SYNTAX",
            context=self._get_context(),
        )
    date1 = self.parse_expression()

    # ============================================================
    # 2. Запятая + вторая дата
    # ============================================================
    if not self.check('COMMA'):
        raise ArrayVatorError(
            code="AGE_BAD_SYNTAX",
            context=self._get_context(),
        )
    self.expect('COMMA')

    if self.check('RPAREN'):
        raise ArrayVatorError(
            code="AGE_BAD_SYNTAX",
            context=self._get_context(),
        )
    date2 = self.parse_expression()

    # ============================================================
    # 3. Единица измерения (опционально)
    # ============================================================
    unit = None
    if self.check('COMMA'):
        self.expect('COMMA')

        if self.check('RPAREN'):
            raise ArrayVatorError(
                code="AGE_BAD_SYNTAX",
                context=self._get_context(),
            )
        unit = self.parse_expression()

    self.expect('RPAREN')
    return AgeNode(date1, date2, unit)