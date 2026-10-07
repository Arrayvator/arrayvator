# parser/parse_functions/insert.py
"""
Парсинг INSERT (только программист).

СИНТАКСИС:
    insert(s[2, :], before)
    insert(s[2, :], after)
    insert(s[end, :], after)
    insert(s[:, 3], before)
    insert(s[:, "Имя"], before)
    insert(s[:, end], after)
    insert(v, 3, after)
    insert(v[3], after)
"""

from ast_nodes import InsertNode
from errors import ArrayVatorError


def parse_insert(self):
    """Парсинг INSERT"""
    self.expect('LPAREN')

    first_arg = self.parse_primary()

    from ast_nodes.index import IndexNode
    from ast_nodes.variables import VariableNode

    # ============================================================
    # СЛУЧАЙ 1: IndexNode — insert(s[2, :], before)
    # ============================================================
    if isinstance(first_arg, IndexNode):
        # Проверяем: есть ли направление?
        if self.check('RPAREN'):
            raise ArrayVatorError(
                code="INSERT_MISSING_DIRECTION",
                context=self._get_context(),
                message=(
                    "insert: не указано направление — before или after."
                ),
                suggestion=(
                    "insert принимает направление: before или after.\n"
                    "\n"
                    "Неправильно:\n"
                    "     insert(m[2, :])\n"
                    "\n"
                    "Правильно:\n"
                    "     insert(m[2, :], before)\n"
                    "     insert(m[2, :], after)\n"
                    "\n"
                    "Примеры:\n"
                    "     insert(s[2, :], before)\n"
                    "     insert(s[:, 3], after)"
                ),
            )

        self.expect('COMMA')
        direction = self.parse_expression()
        self.expect('RPAREN')
        return InsertNode(first_arg, direction)

    # ============================================================
    # СЛУЧАЙ 2: VariableNode — insert(v, 3, after)
    # ============================================================
    if isinstance(first_arg, VariableNode):
        self.expect('COMMA')
        position = self.parse_expression()

        # Проверяем: есть ли направление?
        if self.check('RPAREN'):
            raise ArrayVatorError(
                code="INSERT_MISSING_DIRECTION",
                context=self._get_context(),
                message=(
                    "insert: не указано направление — before или after."
                ),
                suggestion=(
                    "Для вектора insert принимает ТРИ аргумента:\n"
                    "  insert(v, N, before | after)\n"
                    "\n"
                    "Неправильно:\n"
                    "     insert(v, 3)\n"
                    "\n"
                    "Правильно:\n"
                    "     insert(v, 3, before)\n"
                    "     insert(v, 3, after)"
                ),
            )

        self.expect('COMMA')
        direction = self.parse_expression()
        self.expect('RPAREN')

        index_node = IndexNode(first_arg, [position])
        return InsertNode(index_node, direction)

    # ============================================================
    # ОШИБКА
    # ============================================================
    raise ArrayVatorError(
        code="INSERT_BAD_INDEX",
        context=self._get_context(),
        message="insert: ожидается индекс матрицы или вектор.",
        suggestion=(
            "Примеры:\n"
            "     insert(s[2, :], before)       — вставить строку\n"
            "     insert(s[:, 3], after)        — вставить столбец\n"
            "     insert(v, 3, after)           — вставить в вектор"
        ),
    )