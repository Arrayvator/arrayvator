# runtime/__init__.py
"""
Пакет runtime ArrayVator.

Содержит:
    logger          — логирование операций в файл
    matrix          — MatrExMatrix (RAM-матрица)
    random_source   — генератор случайных чисел
    logging_hook    — автоматическое логирование всех Node
"""

from . import logger
from . import matrix
from . import random_source
from . import logging_hook

__all__ = [
    'logger',
    'matrix',
    'random_source',
    'logging_hook',
]