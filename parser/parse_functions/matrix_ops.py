"""
Парсинг матричных операций: ZEROS, ONES, FILL
"""

from ast_nodes import ZerosNode, OnesNode, FillNode


def parse_matrix_ops(self, token_type):
    """Парсинг матричных операций"""
    self.expect('LPAREN')
    
    if token_type == 'ZEROS':
        rows = self.parse_expression()
        cols = None
        if self.check('COMMA'):
            self.expect('COMMA')
            cols = self.parse_expression()
        self.expect('RPAREN')
        return ZerosNode(rows, cols)
    
    elif token_type == 'ONES':
        rows = self.parse_expression()
        cols = None
        if self.check('COMMA'):
            self.expect('COMMA')
            cols = self.parse_expression()
        self.expect('RPAREN')
        return OnesNode(rows, cols)
    
    elif token_type == 'FILL':
        matrix = self.parse_expression()
        self.expect('COMMA')
        value = self.parse_expression()
        self.expect('RPAREN')
        return FillNode(matrix, value)