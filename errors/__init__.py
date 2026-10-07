# errors/__init__.py
"""
Система ошибок ArrayVator.
Поддерживает русский и английский языки, автоподсказки.
"""

from .base import ArrayVatorError, ErrorContext, make_error, syntax_error
from .i18n import set_language, get_language, t
from .formatter import format_error, print_error, set_color_enabled
from .detector import detect_suggestion

__all__ = [
    'ArrayVatorError',
    'ErrorContext',
    'make_error',
    'syntax_error',
    'set_language',
    'get_language',
    't',
    'format_error',
    'print_error',
    'set_color_enabled',
    'detect_suggestion',
]