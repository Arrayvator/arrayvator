# parser/parse_functions/copy.py
"""
Парсинг COPY (только программист).

СИНТАКСИС:
    copy(s[:, 1], s[:, 10], after)
    copy(s[:, 1:3], s[:, 10], after)
    copy(s[:, end], s[:, 10], after)
    copy(s[2, :], s[10, :], before)
    copy(s[2:5, :], s[10, :], after)

ПРАВИЛА:
    - Первый и второй аргументы — IndexNode (в одной матрице).
    - Третий аргумент — направление (before / after).
"""

from ast_nodes import CopyNode
from errors import ArrayVatorError


def parse_copy(self):
    """Парсинг COPY"""
    self.expect('LPAREN')

    from ast_nodes.index import IndexNode

    # 1. Источник — IndexNode
    source = self.parse_primary()
    if not isinstance(source, IndexNode):
        raise ArrayVatorError(
            code="COPY_BAD_SOURCE",
            context=self._get_context(),
            message="copy: первый аргумент должен быть индексом (источник).",
            suggestion=(
                "Примеры:\n"
                "     copy(s[:, 1], s[:, 10], after)\n"
                "     copy(s[2, :], s[10, :], before)"
            ),
        )

    self.expect('COMMA')

    # 2. Цель — IndexNode
    target = self.parse_primary()
    if not isinstance(target, IndexNode):
        raise ArrayVatorError(
            code="COPY_BAD_TARGET",
            context=self._get_context(),
            message="copy: второй аргумент должен быть индексом (цель).",
            suggestion=(
                "Примеры:\n"
                "     copy(s[:, 1], s[:, 10], after)\n"
                "     copy(s[2, :], s[10, :], before)"
            ),
        )

    # ============================================================
    # 3. НАПРАВЛЕНИЕ
    # ============================================================
    # Если дальше сразу ')' — забыто направление
    if self.check('RPAREN'):
        raise ArrayVatorError(
            code="COPY_MISSING_DIRECTION",
            context=self._get_context(),
            message=(
                "copy: не указано направление — before или after."
            ),
            suggestion=(
                "copy принимает ТРИ аргумента:\n"
                "  1. источник — срез m[:, ...] или m[N, :]\n"
                "  2. цель — срез той же матрицы\n"
                "  3. направление — before | after\n"
                "\n"
                "Неправильно:\n"
                "     copy(m[:, 1], m[:, 3])\n"
                "\n"
                "Правильно:\n"
                "     copy(m[:, 1], m[:, 3], after)\n"
                "     copy(m[:, 1], m[:, 3], before)\n"
                "\n"
                "Примеры:\n"
                "     copy(s[:, 1], s[:, 10], after)\n"
                "     copy(s[2, :], s[10, :], before)"
            ),
        )

    self.expect('COMMA')

    direction = self.parse_expression()

    self.expect('RPAREN')

    return CopyNode(
        data=source,
        source_type=None,
        source_value=None,
        target_type=None,
        target_value=target,
        direction=direction,
    )