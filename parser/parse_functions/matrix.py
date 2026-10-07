"""
Парсинг MATRIX

СИНТАКСИС:
    matrix(R, C)
    matrix(3, 4)
"""

from ast_nodes import MatrixCreateNode


def parse_matrix_create(self):
    """Парсинг MATRIX (создание)"""
    self.expect('LPAREN')
    
    # Парсим количество строк
    rows = self.parse_expression()
    
    self.expect('COMMA')
    
    # Парсим количество столбцов
    cols = self.parse_expression()
    
    self.expect('RPAREN')
    
    return MatrixCreateNode(rows, cols)