"""
Парсинг RANGE
"""

from ast_nodes import RangeNode


def parse_range_ops(self):
    """Парсинг RANGE"""
    self.expect('LPAREN')
    start = self.parse_expression()
    self.expect('COMMA')
    end = self.parse_expression()
    step = None
    if self.check('COMMA'):
        self.expect('COMMA')
        step = self.parse_expression()
    self.expect('RPAREN')
    return RangeNode(start, end, step)