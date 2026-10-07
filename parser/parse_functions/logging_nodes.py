# parser/parse_functions/logging_nodes.py
"""
Парсинг LogToFile / LogOff
"""

from ast_nodes import LogToFileNode, LogOffNode


def parse_logtofile(self):
    """Парсинг LOGTOFILE"""
    self.expect('LPAREN')
    file_path = self.parse_expression()

    level = None
    if self.check('COMMA'):
        self.expect('COMMA')
        level = self.parse_expression()

    self.expect('RPAREN')
    return LogToFileNode(file_path, level)


def parse_logoff(self):
    """Парсинг LOGOFF"""
    self.expect('LPAREN')
    self.expect('RPAREN')
    return LogOffNode()