# parser/dispatch/create.py
"""
Создание значений и последовательностей:
VECTOR, MATRIX, ZEROS, ONES, FILL, RANDOM, RANGE, NUMSEQ, SAMPLE.
"""

from ._helpers import call_parse


def dispatch(self, token_type, token, value):
    if token_type == 'VECTOR':
        self.pos += 1
        return call_parse(self, 'parse_vector')

    if token_type == 'MATRIX':
        self.pos += 1
        return call_parse(self, 'parse_matrix_create')

    if token_type in ('ZEROS', 'ONES', 'FILL'):
        self.pos += 1
        return call_parse(self, 'parse_matrix_ops', token_type)

    if token_type == 'RANDOM':
        self.pos += 1
        return call_parse(self, 'parse_random')

    if token_type in ('RANGE', 'NUMSEQ'):
        self.pos += 1
        return call_parse(self, 'parse_numseq')

    if token_type == 'SAMPLE':
        self.pos += 1
        return call_parse(self, 'parse_sample')

    return None