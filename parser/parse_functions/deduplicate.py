# parser/parse_functions/deduplicate.py
"""
Парсинг UNIQUE, COUNT_DISTINCT, VALUE_COUNTS, DELETE_DUPLICATE.
Только программистский синтаксис (без аналитика).

СИНТАКСИС:
    Unique(вектор)
    Unique(матрица)
    Unique(матрица[:, "Отдел"])
    Unique(матрица[:, 3])
    Unique(матрица[:, end])
    Unique(матрица[10:end, "Отдел"])

    CountDistinct(вектор)
    CountDistinct(матрица[:, "Отдел"])

    ValueCounts(вектор)
    ValueCounts(матрица[:, "Отдел"])

    DeleteDuplicate(вектор)
    DeleteDuplicate(матрица)
    DeleteDuplicate(матрица[:, "Отдел"])
"""

from ast_nodes import (
    UniqueNode,
    CountDistinctNode,
    ValueCountsNode,
    DeleteDuplicateNode,
)


def parse_deduplicate(self, token_type):
    """Парсинг функций для дубликатов (только программист)."""
    self.expect('LPAREN')

    # Один аргумент — срез или переменная
    data = self.parse_expression()

    self.expect('RPAREN')

    if token_type == 'UNIQUE':
        return UniqueNode(data, column=None)
    elif token_type == 'COUNT_DISTINCT':
        return CountDistinctNode(data, column=None)
    elif token_type == 'VALUE_COUNTS':
        return ValueCountsNode(data, column=None)
    elif token_type == 'DELETE_DUPLICATE':
        return DeleteDuplicateNode(data, column=None)

    raise ValueError(f"Неизвестный тип: {token_type}")