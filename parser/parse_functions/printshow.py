"""
Парсинг PRINT_SHOW
"""

from ast_nodes import PrintShowNode


def parse_printshow(self):
    """Парсинг PRINT_SHOW"""
    self.expect('LPAREN')
    data = self.parse_expression()
    
    title = None
    if self.check('COMMA'):
        self.expect('COMMA')
        title = self.parse_expression()
    
    self.expect('RPAREN')
    return PrintShowNode(data, title)