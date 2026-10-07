# parser/dispatch/case_apply.py
"""
Условное преобразование: CASE, APPLYIF.
"""

from ._helpers import call_parse


def dispatch(self, token_type, token, value):
    if token_type == 'CASE':
        self.pos += 1
        return call_parse(self, 'parse_case')

    if token_type == 'APPLYIF':
        self.pos += 1
        return call_parse(self, 'parse_applyif')

    return None