# parser/parse_functions/datetime_now.py
"""
Парсинг DATENOW, TIMENOW, TIMESTAMP

СИНТАКСИС:
    datenow()
    datenow("DD.MM.YYYY")
    timenow()
    timenow("HH:MM:SS")
    timestamp()
    timestamp("DD.MM.YYYY HH:MM")
    timestamp("MM/DD/YYYY hh:MM AM")
"""

from ast_nodes import DateNowNode, TimeNowNode, TimestampNode


def parse_datenow(self):
    """Парсинг DATENOW"""
    self.expect('LPAREN')
    
    format_str = None
    if not self.check('RPAREN'):
        format_str = self.parse_expression()
    
    self.expect('RPAREN')
    return DateNowNode(format_str)


def parse_timenow(self):
    """Парсинг TIMENOW"""
    self.expect('LPAREN')
    
    format_str = None
    if not self.check('RPAREN'):
        format_str = self.parse_expression()
    
    self.expect('RPAREN')
    return TimeNowNode(format_str)


def parse_timestamp(self):
    """timestamp([формат])"""
    self.expect('LPAREN')
    format_str = None
    if not self.check('RPAREN'):
        format_str = self.parse_expression()
    self.expect('RPAREN')
    return TimestampNode(format_str)