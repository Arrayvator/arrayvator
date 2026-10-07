# parser/parse_functions/input_show.py
"""
Парсинг InputShow / InputShowForm
"""

from ast_nodes import InputShowNode, InputShowFormNode


def parse_inputshow(self):
    """Парсинг INPUTSHOW"""
    self.expect('LPAREN')

    prompt = None
    mode = None

    if not self.check('RPAREN'):
        prompt = self.parse_expression()
        if self.check('COMMA'):
            self.expect('COMMA')
            mode = self.parse_expression()

    self.expect('RPAREN')
    return InputShowNode(prompt, mode)


def parse_inputshowform(self):
    """Парсинг INPUTSHOWFORM"""
    self.expect('LPAREN')

    title = self.parse_expression()

    fields = []
    while self.check('COMMA'):
        self.expect('COMMA')
        if self.check('RPAREN'):
            break
        fields.append(self.parse_expression())

    self.expect('RPAREN')
    return InputShowFormNode(title, fields)