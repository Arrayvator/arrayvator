# parser/parse_functions/find.py
"""
Парсинг FIND и FINDIF.

СИНТАКСИС:
    find(s[:, "Имя"] == "Аня")
    find(s[:, 3] == "Аня")
    find(s[10:end, "Имя"] == "Аня")
    find(s[:, :] == "Аня")
    find(s[:, "Имя"] == "Ан", inside)
    find(s[:, "Имя"] == "аня", ignore)
    find(s[:, "Имя"] == "ан", inside, ignore)

    find(s[:, "Имя"] == "Аня", rows)          # → номера строк
    find(s[:, "Имя"] == "Аня", cols)          # → номера столбцов

    find(v == 5)
    find(v == 5, rows)
"""

from ast_nodes import FindNode, FindIfNode, StringNode
from errors import ArrayVatorError


def parse_find(self):
    """Парсинг FIND"""
    self.expect('LPAREN')

    # Условие: s[:, "X"] == "Y"
    condition = self.parse_expression()

    modifiers = []
    return_rows = False
    return_cols = False

    while self.check('COMMA'):
        self.expect('COMMA')
        if self.check('INSIDE'):
            self.expect('INSIDE')
            modifiers.append(StringNode('inside'))
        elif self.check('IGNORE'):
            self.expect('IGNORE')
            modifiers.append(StringNode('ignore'))
        elif self.check('ROWS'):
            self.expect('ROWS')
            return_rows = True
        elif self.check('COLS'):
            self.expect('COLS')
            return_cols = True
        else:
            break

    self.expect('RPAREN')

    if return_rows and return_cols:
        raise ArrayVatorError(
            code="FIND_BAD_SYNTAX",
            context=self._get_context(),
            message=(
                "find: нельзя одновременно указать rows и cols.\n"
                "  Выберите что-то одно."
            ),
            suggestion=(
                "Правильно: find(m[:, \"X\"] == \"Y\")            — координаты\n"
                "Правильно: find(m[:, \"X\"] == \"Y\", rows)      — номера строк\n"
                "Правильно: find(m[:, \"X\"] == \"Y\", cols)      — номера столбцов\n"
                "Неправильно: find(m[:, \"X\"] == \"Y\", rows, cols)"
            ),
        )

    args = modifiers + [None] * (3 - len(modifiers))
    return FindNode(
        data=None,
        condition=condition,
        arg1=args[0],
        arg2=args[1],
        arg3=args[2],
        return_rows=return_rows,
        return_cols=return_cols,
    )


def parse_findif(self):
    """Парсинг FINDIF (заглушка)"""
    self.expect('LPAREN')
    matrix = self.parse_expression()
    self.expect('COMMA')
    condition = self.parse_expression()
    self.expect('RPAREN')
    return FindIfNode(matrix, condition)