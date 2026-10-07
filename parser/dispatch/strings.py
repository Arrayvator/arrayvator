# parser/dispatch/strings.py
"""
Строковые функции: replacetext, deletetextleft/right,
trim / trimleft / trimright, split, joinvector, clean.
"""

from ._helpers import call_parse


def dispatch(self, token_type, token, value):
    if token_type == 'REPLACETEXT':
        self.pos += 1
        return call_parse(self, 'parse_string', 'REPLACETEXT')

    if token_type == 'SPLIT':
        self.pos += 1
        return call_parse(self, 'parse_string', 'SPLIT')

    if token_type == 'JOINVECTOR':
        self.pos += 1
        return call_parse(self, 'parse_string', 'JOINVECTOR')

    if token_type == 'CLEAN':
        self.pos += 1
        return call_parse(self, 'parse_clean')

    if token_type == 'DELETETEXTLEFT':
        self.pos += 1
        return call_parse(self, 'parse_deletetextleft')

    if token_type == 'DELETETEXTRIGHT':
        self.pos += 1
        return call_parse(self, 'parse_deletetextright')

    if token_type == 'TRIM':
        self.pos += 1
        return call_parse(self, 'parse_trim')

    if token_type == 'TRIMLEFT':
        self.pos += 1
        return call_parse(self, 'parse_trimleft')

    if token_type == 'TRIMRIGHT':
        self.pos += 1
        return call_parse(self, 'parse_trimright')

    return None