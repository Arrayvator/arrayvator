# parser/dispatch/convert.py
"""
Конвертация: TOMATRIX, TOBIGDATA,
CONVERT_BIGDATA_TO_MATRIX, CONVERT_MATRIX_TO_BIGDATA.
"""

from ._helpers import call_parse


def dispatch(self, token_type, token, value):
    if token_type == 'TOMATRIX':
        self.pos += 1
        return call_parse(self, 'parse_to_matrix')

    if token_type == 'TOBIGDATA':
        self.pos += 1
        return call_parse(self, 'parse_tobigdata')

    if token_type == 'CONVERT_BIGDATA_TO_MATRIX':
        self.pos += 1
        return call_parse(self, 'parse_convert_bigdata_to_matrix')

    if token_type == 'CONVERT_MATRIX_TO_BIGDATA':
        self.pos += 1
        return call_parse(self, 'parse_convert_matrix_to_bigdata')

    return None