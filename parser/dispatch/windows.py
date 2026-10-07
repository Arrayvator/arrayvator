# parser/dispatch/windows.py
"""
Оконные функции:
ROWNUMBER, RANK, DENSERANK, PERCENTRANK, CUMEDIST, NTILE,
LAG, LEAD, FIRSTVALUE, LASTVALUE, NTHVALUE,
WINSUM, WINAVG, WINCOUNT, WINMIN, WINMAX, WINMEDIAN, WINSTDEV,
QUALIFY.
"""

from ._helpers import call_parse


def dispatch(self, token_type, token, value):
    if token_type == 'ROWNUMBER':
        self.pos += 1
        return call_parse(self, 'parse_rownumber')

    if token_type == 'RANK':
        self.pos += 1
        return call_parse(self, 'parse_rank')

    if token_type == 'DENSERANK':
        self.pos += 1
        return call_parse(self, 'parse_denserank')

    if token_type == 'PERCENTRANK':
        self.pos += 1
        return call_parse(self, 'parse_percentrank')

    if token_type == 'CUMEDIST':
        self.pos += 1
        return call_parse(self, 'parse_cumedist')

    if token_type == 'NTILE':
        self.pos += 1
        return call_parse(self, 'parse_ntile')

    if token_type == 'LAG':
        self.pos += 1
        return call_parse(self, 'parse_lag')

    if token_type == 'LEAD':
        self.pos += 1
        return call_parse(self, 'parse_lead')

    if token_type == 'FIRSTVALUE':
        self.pos += 1
        return call_parse(self, 'parse_firstvalue')

    if token_type == 'LASTVALUE':
        self.pos += 1
        return call_parse(self, 'parse_lastvalue')

    if token_type == 'NTHVALUE':
        self.pos += 1
        return call_parse(self, 'parse_nthvalue')

    if token_type == 'WINSUM':
        self.pos += 1
        return call_parse(self, 'parse_winsum')

    if token_type == 'WINAVG':
        self.pos += 1
        return call_parse(self, 'parse_winavg')

    if token_type == 'WINCOUNT':
        self.pos += 1
        return call_parse(self, 'parse_wincount')

    if token_type == 'WINMIN':
        self.pos += 1
        return call_parse(self, 'parse_winmin')

    if token_type == 'WINMAX':
        self.pos += 1
        return call_parse(self, 'parse_winmax')

    if token_type == 'WINMEDIAN':
        self.pos += 1
        return call_parse(self, 'parse_winmedian')

    if token_type == 'WINSTDEV':
        self.pos += 1
        return call_parse(self, 'parse_winstdev')

    if token_type == 'QUALIFY':
        self.pos += 1
        return call_parse(self, 'parse_qualify')

    return None