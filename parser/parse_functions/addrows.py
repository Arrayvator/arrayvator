# parser/parse_functions/addrows.py
"""
Парсинг ADDROWS.

СИНТАКСИС:
    addrows(m, n)
    addrows(m, n, fill)
"""

from ast_nodes import AddRowsNode


def parse_addrows(self):
    """Парсинг ADDROWS"""
    self.expect('LPAREN')

    data = self.parse_expression()
    self.expect('COMMA')

    count = self.parse_expression()

    fill = None
    if self.check('COMMA'):
        self.expect('COMMA')
        fill = self.parse_expression()

    self.expect('RPAREN')
    return AddRowsNode(data, count, fill)