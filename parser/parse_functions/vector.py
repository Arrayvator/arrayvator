"""
Парсинг VECTOR

СИНТАКСИС:
    vector(N)
    vector(10)
"""

from ast_nodes import VectorNode


def parse_vector(self):
    """Парсинг VECTOR"""
    self.expect('LPAREN')
    
    # Парсим размер
    size = self.parse_expression()
    
    self.expect('RPAREN')
    
    return VectorNode(size)