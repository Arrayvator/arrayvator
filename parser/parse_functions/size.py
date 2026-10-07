# parser/parse_functions/size.py
"""
Парсинг функций размеров: LEN, LENROW, LENCOL
"""

from ast_nodes import LenRowNode, LenColNode, LenNode


def parse_size(self, token_type):
    """Парсинг функций размеров"""
    self.expect('LPAREN')
    arg = self.parse_expression()
    self.expect('RPAREN')
    
    if token_type == 'LEN':
        return LenNode(arg)
    elif token_type == 'LENROW':
        return LenRowNode(arg)
    elif token_type == 'LENCOL':
        return LenColNode(arg)