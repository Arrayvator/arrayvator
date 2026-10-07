"""
Парсинг RANDOM

СИНТАКСИС:
    random(1:10, 0)
    random(-10:10, 2)
"""

from ast_nodes import RandomNode


def parse_random(self):
    """Парсинг RANDOM"""
    self.expect('LPAREN')
    
    # Парсим начало диапазона
    start = self.parse_expression()
    
    # Ожидаем COLON
    self.expect('COLON')
    
    # Парсим конец диапазона
    end = self.parse_expression()
    
    # Ожидаем COMMA
    self.expect('COMMA')
    
    # Парсим точность
    precision = self.parse_expression()
    
    self.expect('RPAREN')
    
    return RandomNode(start, end, precision)