# parser/dispatch/reports.py
"""
Отчёты: REPORT, REPORT_SECTION, REPORT_TEXT, REPORT_TABLE,
REPORT_CHART, REPORT_SAVE, REPORT_SHOW, REPORT_SAVE_PDF.
"""

from ._helpers import call_parse


def dispatch(self, token_type, token, value):
    if token_type == 'REPORT':
        self.pos += 1
        return call_parse(self, 'parse_report')

    if token_type == 'REPORT_SECTION':
        self.pos += 1
        return call_parse(self, 'parse_report_section')

    if token_type == 'REPORT_TEXT':
        self.pos += 1
        return call_parse(self, 'parse_report_text')

    if token_type == 'REPORT_TABLE':
        self.pos += 1
        return call_parse(self, 'parse_report_table')

    if token_type == 'REPORT_CHART':
        self.pos += 1
        return call_parse(self, 'parse_report_chart')

    if token_type == 'REPORT_SAVE':
        self.pos += 1
        return call_parse(self, 'parse_report_save')

    if token_type == 'REPORT_SHOW':
        self.pos += 1
        return call_parse(self, 'parse_report_show')

    if token_type == 'REPORT_SAVE_PDF':
        self.pos += 1
        return call_parse(self, 'parse_report_save_pdf')

    return None