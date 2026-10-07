# parser/dispatch/types.py
"""
Типы и None:
TYPE, IS_NUMBER, IS_INTEGER, IS_FLOAT, IS_STRING, IS_BOOLEAN,
TO_STRING, TO_NUMBER, IS_NONE, FILLNA, DROPNA, COALESCE, NONE_IF,
IS_VALID_TIME.
"""

from ._helpers import call_parse


def dispatch(self, token_type, token, value):
    # ============================================================
    # Типы
    # ============================================================
    if token_type in ('TYPE', 'IS_NUMBER', 'IS_INTEGER', 'IS_FLOAT',
                      'IS_STRING', 'IS_BOOLEAN',
                      'TO_STRING', 'TO_NUMBER'):
        self.pos += 1
        return call_parse(self, 'parse_type_handling', token_type)

    # ============================================================
    # None (обновлённые имена токенов)
    # ============================================================
    if token_type in ('IS_NONE', 'FILLNA', 'DROPNA', 'COALESCE', 'NONE_IF'):
        self.pos += 1
        return call_parse(self, 'parse_null_handling', token_type)

    # ============================================================
    # Проверка времени
    # ============================================================
    if token_type == 'IS_VALID_TIME':
        self.pos += 1
        return call_parse(self, 'parse_is_valid_time', token_type)

    return None