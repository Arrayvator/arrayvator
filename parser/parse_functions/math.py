"""
Парсинг математических функций: ROUND, INT, FRAC, FRAC_DIGITS
"""

from ast_nodes import RoundNode, IntNode, FracNode, FracDigitsNode


def parse_math(self, token_type):
    """Парсинг математических функций"""
    self.expect('LPAREN')
    arg = self.parse_expression()
    digits = None
    
    if token_type in ['ROUND', 'FRAC']:
        if self.check('COMMA'):
            self.expect('COMMA')
            digits = self.parse_expression()
    
    self.expect('RPAREN')
    
    if token_type == 'ROUND':
        return RoundNode(arg, digits)
    elif token_type == 'INT':
        return IntNode(arg)
    elif token_type == 'FRAC':
        return FracNode(arg, digits)
    elif token_type == 'FRAC_DIGITS':
        return FracDigitsNode(arg)