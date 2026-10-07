# parser/parse_functions/date.py
"""
Парсинг DATE.

СИНТАКСИС:
    date(данные, "входной_формат", "выходной_формат")
"""

from ast_nodes import DateNode
from errors import ArrayVatorError


def parse_date(self):
    """Парсинг DATE"""
    self.expect('LPAREN')

    # 1. Данные
    data = self.parse_expression()
    self.expect('COMMA')

    # 2. Входной формат
    in_fmt = self.parse_expression()
    self.expect('COMMA')

    # 3. Выходной формат
    out_fmt = self.parse_expression()

    self.expect('RPAREN')

    return DateNode(data, in_fmt, out_fmt)