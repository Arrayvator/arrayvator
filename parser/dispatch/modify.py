# parser/dispatch/modify.py
"""
Модификация: INSERT, INSERTIF, COPY, MOVE, MATRIXMOD.
"""

from ._helpers import call_parse


def dispatch(self, token_type, token, value):
    if token_type == 'INSERT':
        self.pos += 1
        return call_parse(self, 'parse_insert')

    if token_type == 'INSERTIF':
        self.pos += 1
        return call_parse(self, 'parse_insertif')

    if token_type == 'COPY':
        self.pos += 1
        return call_parse(self, 'parse_copy')

    if token_type == 'MOVE':
        self.pos += 1
        return call_parse(self, 'parse_move')

    if token_type == 'MATRIXMOD':
        self.pos += 1
        return call_parse(self, 'parse_matrixmod')

    return None