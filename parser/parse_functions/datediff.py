# parser/parse_functions/datediff.py
"""
Парсинг DATEDIFF (только программист).

СИНТАКСИС:
    DateDiff("20.06.2024", "25.06.2024", "DD.MM.YYYY", "days")
    DateDiff(m[:, "Дата1"], m[:, "Дата2"], "DD.MM.YYYY", "days")
"""

from ast_nodes import DateDiffNode


def parse_datediff(self):
    """Парсинг DATEDIFF"""
    self.expect('LPAREN')

    # 1. Первая дата
    arg1 = self.parse_expression()
    self.expect('COMMA')

    # 2. Вторая дата
    arg2 = self.parse_expression()
    self.expect('COMMA')

    # 3. Формат
    format_str = self.parse_expression()
    self.expect('COMMA')

    # 4. Единица измерения
    unit = self.parse_expression()

    self.expect('RPAREN')
    return DateDiffNode(arg1, arg2, format_str, unit)