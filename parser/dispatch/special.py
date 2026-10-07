# parser/dispatch/special.py
"""
Специальные токены: ERROR, BIGDATA, TABLE, AFTER, BEFORE,
BEGIN_KEYWORD, END_KEYWORD, END_PLUS, END_MINUS, LAST_KEYWORD.
"""

from ast_nodes import StringNode, VariableNode
from errors import ArrayVatorError
from ._helpers import call_parse


def dispatch(self, token_type, token, value):
    # ============================================================
    # ERROR — встроенная переменная
    # ============================================================
    if token_type == 'ERROR':
        self.pos += 1

        if self.check('ASSIGN'):
            raise ArrayVatorError(
                code="RESERVED_WORD",
                context=self._get_context(token),
                message=(
                    "Имя 'error' зарезервировано.\n"
                    "  Используется для обработки ошибок."
                ),
                suggestion=(
                    "Используйте другое имя:\n"
                    "     err  = ...\n"
                    "     err1 = ...\n"
                    "\n"
                    "Переменная 'error' доступна ТОЛЬКО ДЛЯ ЧТЕНИЯ:\n"
                    "     if error then { print(error) }"
                ),
            )

        return VariableNode('error')

    # ============================================================
    # РЕЖИМЫ ОТКРЫТИЯ CSV
    # ============================================================
    if token_type == 'BIGDATA':
        self.pos += 1
        return StringNode('duckdb')

    if token_type == 'TABLE':
        self.pos += 1
        return StringNode('matrix')

    # ============================================================
    # ИНДЕКСАЦИЯ
    # ============================================================
    if token_type in ('BEGIN_KEYWORD', 'END_KEYWORD'):
        self.pos += 1
        return StringNode(value.lower())

    if token_type == 'AFTER':
        self.pos += 1
        return StringNode('after')

    if token_type == 'BEFORE':
        self.pos += 1
        return StringNode('before')

    if token_type == 'LAST_KEYWORD':
        self.pos += 1
        next_token = self.peek()
        if next_token and next_token[0] == 'NUMBER':
            self.pos += 1
            result = StringNode(f"last {next_token[1]}")
            if self.check('LBRACKET'):
                from ..matrix import parse_index
                return parse_index(self, result.value)
            return result
        return StringNode('last')

    if token_type == 'END_PLUS':
        self.pos += 1
        if self.check('LBRACKET'):
            from ..matrix import parse_index
            return parse_index(self, value)
        return StringNode(value)

    if token_type == 'END_MINUS':
        self.pos += 1
        if self.check('LBRACKET'):
            from ..matrix import parse_index
            return parse_index(self, value)
        return StringNode(value)

    return None