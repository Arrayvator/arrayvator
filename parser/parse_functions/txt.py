# parser/parse_functions/txt.py
"""
Парсинг TXT-функций:
    OpenTXT("file.txt" [, delimiter])
    SaveTXT(data, "file.txt" [, delimiter])
    OpenTXTShow([delimiter])
    SaveTXTShow(data [, delimiter])
"""

from ast_nodes import (
    OpenTXTNode,
    SaveTXTNode,
    OpenTXTShowNode,
    SaveTXTShowNode,
)


def parse_txt(self, token_type):
    """Парсинг TXT-функций"""
    self.expect('LPAREN')

    if token_type == 'OPENTXT':
        file_path = self.parse_expression()
        delimiter = None
        if self.check('COMMA'):
            self.expect('COMMA')
            delimiter = self.parse_expression()
        self.expect('RPAREN')
        return OpenTXTNode(file_path, delimiter)

    elif token_type == 'SAVETXT':
        data = self.parse_expression()
        self.expect('COMMA')
        file_path = self.parse_expression()
        delimiter = None
        if self.check('COMMA'):
            self.expect('COMMA')
            delimiter = self.parse_expression()
        self.expect('RPAREN')
        return SaveTXTNode(data, file_path, delimiter)

    elif token_type == 'OPENTXTSHOW':
        delimiter = None
        if not self.check('RPAREN'):
            delimiter = self.parse_expression()
        self.expect('RPAREN')
        return OpenTXTShowNode(delimiter)

    elif token_type == 'SAVETXTSHOW':
        data = self.parse_expression()
        delimiter = None
        if self.check('COMMA'):
            self.expect('COMMA')
            delimiter = self.parse_expression()
        self.expect('RPAREN')
        return SaveTXTShowNode(data, delimiter)