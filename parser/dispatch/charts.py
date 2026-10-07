# parser/dispatch/charts.py
"""
Графики: CHART.
"""

from ._helpers import call_parse


def dispatch(self, token_type, token, value):
    if token_type == 'CHART':
        self.pos += 1
        return call_parse(self, 'parse_chart')

    return None