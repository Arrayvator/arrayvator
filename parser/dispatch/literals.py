# parser/dispatch/literals.py
"""
Литералы и простые значения: NUMBER, STRING, TRUE, FALSE,
NONE (литерал None), AZ, ZA, ALL.

ЗАПРЕЩЁННЫЕ ЛИТЕРАЛЫ:
    BANNED_NULL (null) → ArrayVatorError с кодом BANNED_NULL_LITERAL
    BANNED_NAN  (nan)  → ArrayVatorError с кодом BANNED_NAN_LITERAL

Эти ошибки содержат подробное объяснение, что в ArrayVator
используется только None (с большой буквы).
"""

from ast_nodes import (
    NumberNode, StringNode, BooleanNode, NullNode,
)
from errors import ArrayVatorError


def dispatch(self, token_type, token, value):
    # ============================================================
    # ЗАПРЕЩЁННЫЕ ЛИТЕРАЛЫ — null и nan
    # ============================================================
    if token_type == 'BANNED_NULL':
        raise ArrayVatorError(
            code='BANNED_NULL_LITERAL',
            context=self._get_context(token),
        )

    if token_type == 'BANNED_NAN':
        raise ArrayVatorError(
            code='BANNED_NAN_LITERAL',
            context=self._get_context(token),
        )

    # ============================================================
    # ОБЫЧНЫЕ ЛИТЕРАЛЫ
    # ============================================================
    if token_type == 'NUMBER':
        self.pos += 1
        return NumberNode(value)

    if token_type == 'STRING':
        self.pos += 1
        return StringNode(value)

    if token_type == 'TRUE':
        self.pos += 1
        return BooleanNode(True)

    if token_type == 'FALSE':
        self.pos += 1
        return BooleanNode(False)

    if token_type == 'NONE':
        self.pos += 1
        return NullNode()

    if token_type == 'AZ':
        self.pos += 1
        return StringNode('az')

    if token_type == 'ZA':
        self.pos += 1
        return StringNode('za')

    if token_type == 'ALL':
        self.pos += 1
        return StringNode('all')

    return None