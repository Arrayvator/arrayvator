# parser/dispatch/input_output.py
"""
Ввод/вывод и логирование:
INPUTLISTSHOW, INPUTSHOWFORM, INPUTSHOW, LOGTOFILE, LOGOFF, PRINT_SHOW.
"""

from ._helpers import call_parse


def dispatch(self, token_type, token, value):
    if token_type == 'INPUTLISTSHOW':
        self.pos += 1
        return call_parse(self, 'parse_inputlistshow')

    if token_type == 'INPUTSHOWFORM':
        self.pos += 1
        return call_parse(self, 'parse_inputshowform')

    if token_type == 'INPUTSHOW':
        self.pos += 1
        return call_parse(self, 'parse_inputshow')

    if token_type == 'LOGTOFILE':
        self.pos += 1
        return call_parse(self, 'parse_logtofile')

    if token_type == 'LOGOFF':
        self.pos += 1
        return call_parse(self, 'parse_logoff')

    if token_type == 'PRINT_SHOW':
        self.pos += 1
        return call_parse(self, 'parse_printshow')

    return None