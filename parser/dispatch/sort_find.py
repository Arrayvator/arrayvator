# parser/dispatch/sort_find.py
"""
Сортировка и поиск: SORT, FIND, FINDIF, VLOOKUP.
"""

from ._helpers import call_parse


def dispatch(self, token_type, token, value):
    if token_type == 'SORT':
        self.pos += 1
        return call_parse(self, 'parse_sort')

    if token_type == 'FIND':
        self.pos += 1
        return call_parse(self, 'parse_find')

    if token_type == 'FINDIF':
        self.pos += 1
        return call_parse(self, 'parse_findif')

    if token_type == 'VLOOKUP':
        self.pos += 1
        return call_parse(self, 'parse_vlookup')

    return None