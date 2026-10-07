# parser/dispatch/filter_delete.py
"""
Фильтрация и удаление: FILTERIF, DELETEIF, DELETE.
"""

from ._helpers import call_parse


def dispatch(self, token_type, token, value):
    if token_type == 'FILTERIF':
        self.pos += 1
        return call_parse(self, 'parse_filterif')

    if token_type == 'DELETEIF':
        self.pos += 1
        return call_parse(self, 'parse_deleteif')

    if token_type == 'DELETE':
        self.pos += 1
        return call_parse(self, 'parse_delete')

    return None