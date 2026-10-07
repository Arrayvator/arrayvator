# parser/dispatch/statistics.py
"""
Диспетчер статистических функций:
    SUM, MIN, MAX, AVG, COUNT, MEDIAN, STD,
    LEN, LENROW, LENCOL,
    SUMIF, COUNTIF, AVGIF, MINIF, MAXIF, MEDIANIF,
    COUNTUNIQUEIF, SUMPRODUCT,
    TRANSPOSE.
"""

from ._helpers import call_parse


def dispatch(self, token_type, token, value):
    # ============================================================
    # Условные агрегаты (ДО обычных SUM/MIN/MAX/AVG!)
    # ============================================================
    if token_type == 'SUMIF':
        self.pos += 1
        return call_parse(self, 'parse_sumif')

    if token_type == 'COUNTIF':
        self.pos += 1
        return call_parse(self, 'parse_countif')

    if token_type == 'AVGIF':
        self.pos += 1
        return call_parse(self, 'parse_avgif')

    if token_type == 'MINIF':
        self.pos += 1
        return call_parse(self, 'parse_minif')

    if token_type == 'MAXIF':
        self.pos += 1
        return call_parse(self, 'parse_maxif')

    if token_type == 'MEDIANIF':
        self.pos += 1
        return call_parse(self, 'parse_medianif')

    if token_type == 'COUNTUNIQUEIF':
        self.pos += 1
        return call_parse(self, 'parse_countuniqueif')

    if token_type == 'SUMPRODUCT':
        self.pos += 1
        return call_parse(self, 'parse_sumproduct')

    # ============================================================
    # Обычные статистические с опциональным by
    # ============================================================
    if token_type in ('SUM', 'MIN', 'MAX', 'AVG'):
        self.pos += 1
        return call_parse(self, 'parse_statistical', token_type)

    # ============================================================
    # COUNT / MEDIAN / STD — новые функции
    # ============================================================
    if token_type == 'COUNT':
        self.pos += 1
        return call_parse(self, 'parse_count')

    if token_type == 'MEDIAN':
        self.pos += 1
        return call_parse(self, 'parse_median')

    if token_type == 'STD':
        self.pos += 1
        return call_parse(self, 'parse_std')

    # ============================================================
    # Размеры
    # ============================================================
    if token_type in ('LEN', 'LENROW', 'LENCOL'):
        self.pos += 1
        return call_parse(self, 'parse_size', token_type)

    # ============================================================
    # Транспонирование
    # ============================================================
    if token_type == 'TRANSPOSE':
        self.pos += 1
        return call_parse(self, 'parse_transpose')

    return None