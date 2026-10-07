# parser/parse_functions/sort.py
"""
Парсинг SORT (только программист).

СИНТАКСИС:
    sort(s[:, "Имя"], AZ)
    sort(s[:, "Имя"], ZA)
    sort(s[:, 3], AZ)
    sort(s[10:end, "Возраст"], AZ)
    sort(s[:, end], AZ)
    sort(v, AZ)
    sort(v[3:6], ZA)
    sort(v[last 3], AZ)

ПРАВИЛА:
    - 1-й аргумент — срез m[:, "X"] или переменная-вектор.
    - 2-й аргумент — направление (AZ или ZA).
"""

from ast_nodes import SortNode
from ast_nodes.index import IndexNode
from ast_nodes.variables import VariableNode
from errors import ArrayVatorError


def parse_sort(self):
    """Парсинг SORT (программист)."""
    self.expect('LPAREN')

    # 1. Первый аргумент — срез или вектор-переменная
    first_arg = self.parse_expression()

    if not isinstance(first_arg, (IndexNode, VariableNode)):
        raise ArrayVatorError(
            code="SORT_BAD_FIRST_ARG",
            context=self._get_context(),
        )

    # 2. Запятая
    self.expect('COMMA')

    # 3. Второй аргумент — направление
    direction = self.parse_expression()

    self.expect('RPAREN')

    return SortNode(
        data=first_arg,
        arg1=direction,
        arg2=None,
    )