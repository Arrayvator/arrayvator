# parser/dispatch/join_unpivot.py
"""
Соединение и разворот: JOIN, JOINARRAY, UNPIVOT, PIVOT.
"""

from ._helpers import call_parse


def dispatch(self, token_type, token, value):
    if token_type == 'JOIN':
        self.pos += 1
        return call_parse(self, 'parse_join')

    if token_type == 'JOINARRAY':
        self.pos += 1
        return call_parse(self, 'parse_joinarray')

    if token_type == 'UNPIVOT':
        self.pos += 1
        return call_parse(self, 'parse_unpivot')

    if token_type == 'PIVOT':
        self.pos += 1
        return call_parse(self, 'parse_pivot')

    return None