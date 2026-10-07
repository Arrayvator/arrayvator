"""
Парсинг CLEAN
"""

from ast_nodes import CleanNode


def parse_clean(self):
    """Парсинг CLEAN"""
    self.expect('LPAREN')
    data = self.parse_expression()
    self.expect('COMMA')
    mode = self.parse_expression()
    self.expect('RPAREN')
    return CleanNode(data, mode)