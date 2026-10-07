# parser/parse_functions/matrixmod.py
"""
Парсинг MATRIXMOD.

СИНТАКСИС:
    matrixmod(m, delete, N)
    matrixmod(m, insert, N, before)
    matrixmod(m, insert, N, after)
    matrixmod(m, duplicate, N, before)
    matrixmod(m, duplicate, N, after)
    matrixmod(m, clear, N)
    matrixmod(m, keep, N)
    matrixmod(m, swap, [a, b])

ПРАВИЛА:
    - insert и duplicate ТРЕБУЮТ направление (before / after).
    - Остальные действия — без направления.
"""

from ast_nodes import StringNode
from ast_nodes.functions.matrixmod import MatrixModNode
from errors import ArrayVatorError


def parse_matrixmod(self):
    """Парсинг MATRIXMOD"""
    self.expect('LPAREN')

    # 1. Матрица
    data = self.parse_expression()
    self.expect('COMMA')

    # 2. Действие
    action_token = self.peek()
    if not action_token:
        raise ArrayVatorError(
            code="MATRIXMOD_MISSING_ACTION",
            context=self._get_context(),
            message=(
                "matrixmod: ожидается действие.\n"
                "  Допустимо: delete, insert, duplicate, clear, keep, swap."
            ),
            suggestion=(
                "Примеры:\n"
                "     matrixmod(m, delete, 2)\n"
                "     matrixmod(m, insert, 2, before)\n"
                "     matrixmod(m, duplicate, [2, 4], after)\n"
                "     matrixmod(m, clear, 2)\n"
                "     matrixmod(m, keep, [2, 4])\n"
                "     matrixmod(m, swap, [2, 5])"
            ),
        )

    action_map = {
        'DELETE': 'delete',
        'INSERT': 'insert',
        'DUPLICATE': 'duplicate',
        'CLEAR': 'clear',
        'KEEP': 'keep',
        'SWAP': 'swap',
    }

    if action_token[0] not in action_map:
        raise ArrayVatorError(
            code="MATRIXMOD_BAD_ACTION",
            context=self._get_context(action_token),
            message=(
                f"matrixmod: неизвестное действие '{action_token[1]}'.\n"
                f"  Допустимо: delete, insert, duplicate, clear, keep, swap."
            ),
            suggestion=(
                "Только шесть действий:\n"
                "     delete      — удалить строки\n"
                "     insert      — вставить пустые строки\n"
                "     duplicate   — дублировать строки\n"
                "     clear       — обнулить строки\n"
                "     keep        — оставить только указанные\n"
                "     swap        — поменять две строки"
            ),
        )

    action = action_map[action_token[0]]
    self.pos += 1

    self.expect('COMMA')

    # 3. Позиции (N)
    positions = self.parse_expression()

    # ============================================================
    # 4. Направление
    # ============================================================
    # Для insert / duplicate — ОБЯЗАТЕЛЬНО
    # Для остальных — не нужно
    direction = None

    if self.check('COMMA'):
        self.expect('COMMA')
        dir_token = self.peek()
        if dir_token and dir_token[0] in ('BEFORE', 'AFTER'):
            direction = dir_token[1].lower()
            self.pos += 1
        else:
            raise ArrayVatorError(
                code="MATRIXMOD_MISSING_DIRECTION",
                context=self._get_context(dir_token),
                message=(
                    "matrixmod: ожидается 'before' или 'after'.\n"
                    "  Для insert / duplicate направление обязательно."
                ),
                suggestion=(
                    "insert и duplicate требуют направление:\n"
                    "     before — ПЕРЕД указанной строкой\n"
                    "     after  — ПОСЛЕ указанной строки\n"
                    "\n"
                    "Правильно:\n"
                    "     matrixmod(m, insert, 2, before)\n"
                    "     matrixmod(m, duplicate, [2, 4], after)"
                ),
            )

    # ============================================================
    # 5. Проверка: insert / duplicate требуют направление
    # ============================================================
    if action in ('insert', 'duplicate') and direction is None:
        raise ArrayVatorError(
            code="MATRIXMOD_MISSING_DIRECTION",
            context=self._get_context(),
            message=(
                f"matrixmod: для '{action}' нужно направление.\n"
                f"  Укажите before или after."
            ),
            suggestion=(
                "insert и duplicate требуют направление:\n"
                "     before — ПЕРЕД указанной строкой\n"
                "     after  — ПОСЛЕ указанной строки\n"
                "\n"
                "Неправильно:\n"
                f"     matrixmod(m, {action}, 2)\n"
                f"     matrixmod(m, {action}, [2, 4])\n"
                "\n"
                "Правильно:\n"
                f"     matrixmod(m, {action}, 2, before)\n"
                f"     matrixmod(m, {action}, [2, 4], after)"
            ),
        )

    self.expect('RPAREN')

    return MatrixModNode(data, action, positions, direction)