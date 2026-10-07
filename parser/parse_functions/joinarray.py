# parser/parse_functions/joinarray.py
"""
Парсинг JOINARRAY.

СИНТАКСИС:
    joinarray(a, b, vertical)
    joinarray(a, b, horizontal)
    joinarray(a, b, c, vertical)
    joinarray(a, b, c, d, horizontal)

ПРАВИЛА:
    - Направление (vertical / horizontal) — ПОСЛЕДНИЙ аргумент.
    - Может быть 2, 3, 4 и больше матриц.
"""

from ast_nodes import JoinArrayNode, StringNode
from errors import ArrayVatorError


def parse_joinarray(self):
    """Парсинг JOINARRAY"""
    self.expect('LPAREN')

    matrices = []
    axis = None

    # Первая матрица
    m = self.parse_expression()
    matrices.append(m)

    # Остальные аргументы
    while self.check('COMMA'):
        self.expect('COMMA')

        next_token = self.peek()
        if not next_token:
            break

        # vertical / horizontal
        if next_token[0] in ('VERTICAL', 'HORIZONTAL'):
            axis = StringNode(next_token[0].lower())
            self.pos += 1
            break

        # Строка "vertical" / "horizontal"
        if next_token[0] == 'STRING':
            val = next_token[1].lower()
            if val in ('vertical', 'horizontal'):
                axis = StringNode(val)
                self.pos += 1
                break

        # Ещё матрица
        m = self.parse_expression()
        matrices.append(m)

    self.expect('RPAREN')

    # По умолчанию vertical
    if axis is None:
        axis = StringNode('vertical')

    return JoinArrayNode(matrices, axis)