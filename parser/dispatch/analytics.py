# parser/dispatch/analytics.py
"""
Аналитические функции: ABC, PERCENTOF, ANOMALY.
"""

from ._helpers import call_parse


def dispatch(self, token_type, token, value):
    if token_type == 'ABC':
        self.pos += 1
        return call_parse(self, 'parse_abc')

    if token_type == 'PERCENTOF':
        self.pos += 1
        return call_parse(self, 'parse_percentof')

    if token_type == 'ANOMALY':
        self.pos += 1
        return call_parse(self, 'parse_anomaly')

    return None