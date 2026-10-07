# parser/parse_functions/move.py
"""
Парсинг MOVE (только программист).

СИНТАКСИС:
    move(s[:, 1], s[:, 10], after)
    move(s[:, 1:3], s[:, 10], after)
    move(s[:, end], s[:, 10], after)
    move(s[2, :], s[10, :], before)
    move(s[1:10, :], s[end, :], after)

ПРАВИЛА:
    - Первый и второй аргументы — IndexNode (в одной матрице).
    - Третий аргумент — направление (before / after).
"""

from ast_nodes import MoveNode
from errors import ArrayVatorError


def parse_move(self):
    """Парсинг MOVE"""
    self.expect('LPAREN')

    from ast_nodes.index import IndexNode

    # 1. Источник — IndexNode
    source = self.parse_primary()
    if not isinstance(source, IndexNode):
        raise ArrayVatorError(
            code="MOVE_BAD_SOURCE",
            context=self._get_context(),
            message="move: первый аргумент должен быть индексом (источник).",
            suggestion=(
                "Примеры:\n"
                "     move(s[:, 1], s[:, 10], after)\n"
                "     move(s[2, :], s[10, :], before)"
            ),
        )

    self.expect('COMMA')

    # 2. Цель — IndexNode
    target = self.parse_primary()
    if not isinstance(target, IndexNode):
        raise ArrayVatorError(
            code="MOVE_BAD_TARGET",
            context=self._get_context(),
            message="move: второй аргумент должен быть индексом (цель).",
            suggestion=(
                "Примеры:\n"
                "     move(s[:, 1], s[:, 10], after)\n"
                "     move(s[2, :], s[10, :], before)"
            ),
        )

    # ============================================================
    # 3. НАПРАВЛЕНИЕ
    # ============================================================
    if self.check('RPAREN'):
        raise ArrayVatorError(
            code="MOVE_MISSING_DIRECTION",
            context=self._get_context(),
            message=(
                "move: не указано направление — before или after."
            ),
            suggestion=(
                "move принимает ТРИ аргумента:\n"
                "  1. источник — срез m[:, ...] или m[N, :]\n"
                "  2. цель — срез той же матрицы\n"
                "  3. направление — before | after\n"
                "\n"
                "Неправильно:\n"
                "     move(m[:, 1], m[:, 4])\n"
                "\n"
                "Правильно:\n"
                "     move(m[:, 1], m[:, 4], after)\n"
                "     move(m[:, 1], m[:, 4], before)\n"
                "\n"
                "Примеры:\n"
                "     move(s[:, 1], s[:, 10], after)\n"
                "     move(s[2, :], s[10, :], before)"
            ),
        )

    self.expect('COMMA')

    direction = self.parse_expression()

    self.expect('RPAREN')

    return MoveNode(
        data=source,
        source_type=None,
        source_value=None,
        target_type=None,
        target_value=target,
        direction=direction,
    )