# parser/dispatch/math.py
"""
Математические функции: ROUND, INT, FRAC, FRAC_DIGITS.
"""

from ._helpers import call_parse


def dispatch(self, token_type, token, value):
    if token_type in ('ROUND', 'INT', 'FRAC', 'FRAC_DIGITS'):
        self.pos += 1
        return call_parse(self, 'parse_math', token_type)

    return None