"""
Парсинг TRANSPOSE
"""

from ast_nodes import TransposeNode


def parse_transpose(self):
    """Парсинг TRANSPOSE"""
    self.expect('LPAREN')
    arg = self.parse_expression()
    self.expect('RPAREN')
    return TransposeNode(arg)