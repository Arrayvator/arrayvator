# parser/parse_functions/addcolumn.py
"""
Парсинг ADDCOLUMN.

СИНТАКСИС:
    addcolumn(m, "Сумма", m[:, "ID"] + m[:, "ID_10"])
    addcolumn(m, "Год", 2024)
    addcolumn(m, "Статус", "новый")

    addcolumn(m, 2)              — добавить 2 ПУСТЫХ столбца
    addcolumn(m, 2, 0)           — добавить 2 столбца, заполнить 0
    addcolumn(m, "Новый")        — один столбец с именем, значения None
"""

from ast_nodes import AddColumnNode
from errors import ArrayVatorError


def parse_addcolumn(self):
    self.expect('LPAREN')

    args = []

    # 1. Матрица
    if self.check('RPAREN'):
        raise ArrayVatorError(
            code="ADDCOLUMN_BAD_SYNTAX",
            context=self._get_context(),
            message="addcolumn: нужен хотя бы один аргумент — матрица.",
        )
    args.append(self.parse_expression())

    # 2. Остальные аргументы (2 или 3 всего)
    while self.check('COMMA'):
        self.expect('COMMA')
        if self.check('RPAREN'):
            break
        args.append(self.parse_expression())

    self.expect('RPAREN')

    if len(args) < 2:
        raise ArrayVatorError(
            code="ADDCOLUMN_BAD_SYNTAX",
            context=self._get_context(),
            message=(
                "addcolumn: нужно минимум 2 аргумента.\n"
                "  Пример: addcolumn(m, \"Сумма\", m[:, \"A\"] * m[:, \"B\"])\n"
                "  Пример: addcolumn(m, 2)          — 2 пустых столбца\n"
                "  Пример: addcolumn(m, 2, 0)       — 2 столбца со значениями 0"
            ),
        )

    if len(args) > 3:
        raise ArrayVatorError(
            code="ADDCOLUMN_BAD_SYNTAX",
            context=self._get_context(),
            message=(
                "addcolumn: не больше 3 аргументов.\n"
                "  addcolumn(матрица, имя_или_N [, значение])"
            ),
        )

    return AddColumnNode(args)