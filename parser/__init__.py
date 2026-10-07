# parser/__init__.py
"""
Пакет парсера ArrayVator
"""

from .base import Parser
from .program import parse_program
from .statements import parse_statement, parse_print_show
from .expressions import (
    parse_expression, parse_or, parse_and, parse_not,
    parse_comparison, parse_add, parse_mul, parse_pow, parse_unary
)
from .functions import parse_primary
from .matrix import parse_index, parse_index_expression, parse_matrix


# Регистрируем все методы в Parser
Parser.parse_program = parse_program
Parser.parse_statement = parse_statement
Parser.parse_print_show = parse_print_show
Parser.parse_expression = parse_expression
Parser.parse_or = parse_or
Parser.parse_and = parse_and
Parser.parse_not = parse_not
Parser.parse_comparison = parse_comparison
Parser.parse_add = parse_add
Parser.parse_mul = parse_mul
Parser.parse_pow = parse_pow
Parser.parse_unary = parse_unary
Parser.parse_primary = parse_primary
Parser.parse_index = parse_index
Parser._parse_index_expression = parse_index_expression
Parser.parse_matrix = parse_matrix

__all__ = ['Parser']