# parser/dispatch/groupby.py
"""
Группировка и блочные операции:
GROUPBY, GROUPAGG, FILLDOWN, ADDCOLUMN, ADDROWS.
"""

from ._helpers import call_parse


def dispatch(self, token_type, token, value):
    if token_type == 'GROUPBY':
        self.pos += 1
        return call_parse(self, 'parse_groupby')

    if token_type == 'GROUPAGG':
        self.pos += 1
        return call_parse(self, 'parse_groupagg')

    if token_type == 'FILLDOWN':
        self.pos += 1
        return call_parse(self, 'parse_filldown')

    if token_type == 'ADDCOLUMN':
        self.pos += 1
        return call_parse(self, 'parse_addcolumn')

    if token_type == 'ADDROWS':
        self.pos += 1
        return call_parse(self, 'parse_addrows')

    return None