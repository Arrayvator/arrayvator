# parser/parse_functions/addcolumn.py
"""
Парсинг ADDCOLUMN.

СИНТАКСИС:
    m2 = addcolumn(m, "Сумма", m[:, "ID"] + m[:, "ID_10"])
    m2 = addcolumn(m, "Год", 2024)
    m2 = addcolumn(m, "Статус", "новый")
"""

from ast_nodes import AddColumnNode


def parse_addcolumn(self):
    """Парсинг ADDCOLUMN"""
    self.expect('LPAREN')

    data = self.parse_expression()
    self.expect('COMMA')

    name = self.parse_expression()
    self.expect('COMMA')

    expr = self.parse_expression()
    self.expect('RPAREN')

    return AddColumnNode(data, name, expr)