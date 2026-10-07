# parser/parse_functions/type_handling.py
"""
Парсинг функций для типов данных:
    TYPE, IS_NUMBER, IS_INTEGER, IS_FLOAT,
    IS_STRING, IS_BOOLEAN,
    TO_STRING, TO_NUMBER,
    IS_VALID_TIME.

ВАЖНО:
    IS_NONE (функция isnone) обрабатывается не здесь,
    а в parser/parse_functions/null_handling.py.
"""

from ast_nodes import (
    TypeNode, IsNumberNode, IsIntegerNode, IsFloatNode,
    IsStringNode, IsBooleanNode, ToStringNode, ToNumberNode,
    IsValidTimeNode,
)


def parse_type_handling(self, token_type):
    """Парсинг функций для типов данных."""
    self.expect('LPAREN')
    value = self.parse_expression()
    self.expect('RPAREN')

    if token_type == 'TYPE':
        return TypeNode(value)
    elif token_type == 'IS_NUMBER':
        return IsNumberNode(value)
    elif token_type == 'IS_INTEGER':
        return IsIntegerNode(value)
    elif token_type == 'IS_FLOAT':
        return IsFloatNode(value)
    elif token_type == 'IS_STRING':
        return IsStringNode(value)
    elif token_type == 'IS_BOOLEAN':
        return IsBooleanNode(value)
    elif token_type == 'TO_STRING':
        return ToStringNode(value)
    elif token_type == 'TO_NUMBER':
        return ToNumberNode(value)

    raise ValueError(f"Неизвестный тип: {token_type}")


def parse_is_valid_time(self, token_type=None):
    """is_valid_time(данные [, "формат"])"""
    self.expect('LPAREN')
    data = self.parse_expression()
    fmt = None
    if self.check('COMMA'):
        self.expect('COMMA')
        fmt = self.parse_expression()
    self.expect('RPAREN')
    return IsValidTimeNode(data, fmt)