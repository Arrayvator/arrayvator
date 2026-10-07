# parser/parse_functions/filterif.py
"""
Парсинг FILTERIF.

СИНТАКСИС:
    filterif(s[:, "Пол"] == "Ж")
    filterif(s[:, 3] > 80)
    filterif(s[10:end, "Итого"] > 100)
    filterif(v > 20)
    filterif(v[3:6] > 20)

    # Модификаторы (для строк):
    filterif(m[:, "Имя"] == "ов", inside)           — подстрока
    filterif(m[:, "Имя"] == "аня", ignore)          — без регистра
    filterif(m[:, "Имя"] == "ов", inside, ignore)   — оба
"""

from ast_nodes import FilterIfNode
from errors import ArrayVatorError


def parse_filterif(self):
    """Парсинг FILTERIF с модификаторами inside / ignore."""
    self.expect('LPAREN')

    # ============================================================
    # 1. Основное условие
    # ============================================================
    condition = self.parse_expression()

    # ============================================================
    # 2. Модификаторы (inside / ignore)
    # ============================================================
    inside = False
    ignore = False

    while self.check('COMMA'):
        self.expect('COMMA')

        token = self.peek()
        if not token:
            break

        if token[0] == 'INSIDE':
            self.expect('INSIDE')
            inside = True
        elif token[0] == 'IGNORE':
            self.expect('IGNORE')
            ignore = True
        else:
            raise ArrayVatorError(
                code="FILTERIF_BAD_SYNTAX",
                context=self._get_context(token),
                message=(
                    f"filterif: неожиданный модификатор '{token[1]}'.\n"
                    f"  Допустимо: inside, ignore."
                ),
                suggestion=(
                    "Примеры:\n"
                    "     filterif(m[:, \"Имя\"] == \"ов\", inside)\n"
                    "     filterif(m[:, \"Имя\"] == \"аня\", ignore)\n"
                    "     filterif(m[:, \"Имя\"] == \"ов\", inside, ignore)"
                ),
            )

    self.expect('RPAREN')

    return FilterIfNode(
        matrix=None,
        condition=condition,
        inside=inside,
        ignore=ignore,
    )