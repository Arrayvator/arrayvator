# parser/parse_functions/null_handling.py
"""
Парсинг функций для None:
    IS_NONE    → isnone
    FILLNA     → fillna
    DROPNA     → dropna
    COALESCE   → coalesce
    NONE_IF    → noneif
"""

from ast_nodes import (
    IsNullNode, FillnaNode, DropnaNode, CoalesceNode, NullIfNode,
)


def parse_null_handling(self, token_type):
    """Парсинг функций для None."""
    self.expect('LPAREN')

    if token_type == 'IS_NONE':
        value = self.parse_expression()
        self.expect('RPAREN')
        return IsNullNode(value)

    elif token_type == 'FILLNA':
        data = self.parse_expression()
        self.expect('COMMA')
        fill_value = self.parse_expression()
        self.expect('RPAREN')
        return FillnaNode(data, fill_value)

    elif token_type == 'DROPNA':
        data = self.parse_expression()
        self.expect('RPAREN')
        return DropnaNode(data)

    elif token_type == 'COALESCE':
        values = []
        while not self.check('RPAREN'):
            values.append(self.parse_expression())
            if self.check('COMMA'):
                self.expect('COMMA')
            else:
                break
        self.expect('RPAREN')
        return CoalesceNode(*values)

    elif token_type == 'NONE_IF':
        value = self.parse_expression()
        self.expect('COMMA')
        condition = self.parse_expression()
        self.expect('RPAREN')
        return NullIfNode(value, condition)

    raise ValueError(f"Неизвестный тип: {token_type}")