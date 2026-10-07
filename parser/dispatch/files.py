# parser/dispatch/files.py
"""
Файловые функции:
Excel: OPENEXCEL, SAVEEXCEL, OPENEXCELSHOW, SAVEEXCELSHOW
CSV: OPENCSV, SAVECSV, OPENCSVSHOW, SAVECSVSHOW
TXT: OPENTXT, SAVETXT, OPENTXTSHOW, SAVETXTSHOW
Parquet: OPENPARQUET, SAVEPARQUET
SQLite: OPENSQLITE, SAVESQLITE, QUERYSQLITE, OPENSQLITESHOW, SAVESQLITESHOW
Дубликаты: UNIQUE, COUNT_DISTINCT, VALUE_COUNTS, DELETE_DUPLICATE
"""

from ._helpers import call_parse


def dispatch(self, token_type, token, value):
    # ============================================================
    # Excel
    # ============================================================
    if token_type in ('OPENEXCEL', 'SAVEEXCEL',
                      'OPENEXCELSHOW', 'SAVEEXCELSHOW'):
        self.pos += 1
        return call_parse(self, 'parse_excel', token_type)

    # ============================================================
    # CSV
    # ============================================================
    if token_type in ('OPENCSV', 'SAVECSV',
                      'OPENCSVSHOW', 'SAVECSVSHOW'):
        self.pos += 1
        return call_parse(self, 'parse_csv', token_type)

    # ============================================================
    # TXT
    # ============================================================
    if token_type in ('OPENTXT', 'SAVETXT',
                      'OPENTXTSHOW', 'SAVETXTSHOW'):
        self.pos += 1
        return call_parse(self, 'parse_txt', token_type)

    # ============================================================
    # Parquet
    # ============================================================
    if token_type in ('OPENPARQUET', 'SAVEPARQUET'):
        self.pos += 1
        return call_parse(self, 'parse_parquet', token_type)

    # ============================================================
    # SQLite
    # ============================================================
    if token_type in ('OPENSQLITE', 'SAVESQLITE', 'QUERYSQLITE',
                      'OPENSQLITESHOW', 'SAVESQLITESHOW'):
        self.pos += 1
        return call_parse(self, 'parse_sqlite', token_type)

    # ============================================================
    # Дубликаты
    # ============================================================
    if token_type in ('UNIQUE', 'COUNT_DISTINCT',
                      'VALUE_COUNTS', 'DELETE_DUPLICATE'):
        self.pos += 1
        return call_parse(self, 'parse_deduplicate', token_type)

    return None