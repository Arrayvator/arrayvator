# parser/parse_functions/delete.py
"""
Парсинг DELETE и DELETEIF (только программист).

СИНТАКСИС DELETE:
    delete(s[2, :])
    delete(s[10:end, :])
    delete(s[last 3, :])
    delete(s[:, 3])
    delete(s[:, "Имя"])
    delete(s[:, 2:5])
    delete(s[:, last 2])
    delete(v[3:6])
    delete(v[last 2])

СИНТАКСИС DELETEIF:
    deleteif(s[:, "Пол"] == "Ж")
    deleteif(s[:, 3] > 80)
    deleteif(s[10:end, "Итого"] > 100)
    deleteif(v > 20)
    deleteif(v[3:6] > 20)

    # Модификаторы:
    deleteif(m[:, "Имя"] == "ов", inside)
    deleteif(m[:, "Имя"] == "аня", ignore)
    deleteif(m[:, "Имя"] == "ов", inside, ignore)
    deleteif(m[:, "ID"] == 10044, inside)
"""

from ast_nodes import DeleteNode, DeleteIfNode
from errors import ArrayVatorError


# ============================================================
# DELETE
# ============================================================
def parse_delete(self):
    """Парсинг DELETE (только программист)"""
    self.expect('LPAREN')

    first_arg = self.parse_expression()

    from ast_nodes.index import IndexNode
    if not isinstance(first_arg, IndexNode):
        raise ArrayVatorError(
            code="DELETE_BAD_SYNTAX",
            context=self._get_context(),
            message="delete: неверный синтаксис.",
            suggestion=(
                "Используйте индекс:\n"
                "     delete(s[2, :])       — удалить строку 2\n"
                "     delete(s[:, 3])       — удалить столбец 3\n"
                "     delete(s[10:end, :])  — удалить строки 10..end\n"
                "     delete(s[:, \"Имя\"])   — удалить столбец \"Имя\"\n"
                "     delete(v[3:6])        — удалить элементы 3..6"
            ),
        )

    self.expect('RPAREN')
    return DeleteNode(first_arg)


# ============================================================
# DELETEIF
# ============================================================
def parse_deleteif(self):
    """Парсинг DELETEIF (только программист) с модификаторами."""
    self.expect('LPAREN')

    condition = self.parse_expression()

    # ============================================================
    # Модификаторы (inside / ignore)
    # ============================================================
    inside = False
    ignore = False

    while self.check('COMMA'):
        self.expect('COMMA')

        token = self.peek()
        if not token:
            break

        if token[0] == 'INSIDE':
            self.expect('INSIDE')
            inside = True
        elif token[0] == 'IGNORE':
            self.expect('IGNORE')
            ignore = True
        else:
            raise ArrayVatorError(
                code="DELETEIF_BAD_SYNTAX",
                context=self._get_context(token),
                message=(
                    f"deleteif: неожиданный модификатор '{token[1]}'.\n"
                    f"  Допустимо: inside, ignore."
                ),
                suggestion=(
                    "Примеры:\n"
                    "     deleteif(m[:, \"Имя\"] == \"ов\", inside)\n"
                    "     deleteif(m[:, \"Имя\"] == \"аня\", ignore)\n"
                    "     deleteif(m[:, \"Имя\"] == \"ов\", inside, ignore)\n"
                    "     deleteif(m[:, \"ID\"] == 10044, inside)"
                ),
            )

    self.expect('RPAREN')
    return DeleteIfNode(matrix=None, condition=condition,
                        inside=inside, ignore=ignore)