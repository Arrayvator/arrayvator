# parser/dispatch/identifiers.py
"""
Идентификаторы и структурные скобки:
IDENTIFIER, LPAREN, LBRACKET.
"""

from ast_nodes import StringNode, VariableNode
from errors import ArrayVatorError


def _build_unknown_function_suggestion(value):
    """
    Строит подсказку для неизвестной функции:
    автоподбор ближайших имён через similar.find_similar.
    """
    try:
        from syntax.similar import find_similar
        similar = find_similar(value, limit=3)
    except Exception:
        similar = []

    if similar:
        variants = '\n'.join(f"     • {name}()" for name in similar)
        first = similar[0]

        return (
            f"Возможно, вы имели в виду:\n"
            f"{variants}\n"
            f"\n"
            f"Пример:\n"
            f"     {first}(...)\n"
            f"\n"
            f"Подсказка: при вводе работает автодополнение —\n"
            f"           начните печатать имя, появится список."
        )

    return (
        "Проверьте имя функции.\n"
        "\n"
        "Подсказка: при вводе работает автодополнение —\n"
        "           начните печатать имя, появится список.\n"
        "\n"
        "Если вы хотели использовать переменную — уберите '()':\n"
        "     Неправильно: myvar()\n"
        "     Правильно: myvar"
    )


def dispatch(self, token_type, token, value):
    # ============================================================
    # IDENTIFIER
    # ============================================================
    if token_type == 'IDENTIFIER':
        self.pos += 1

        if value.lower() in ('end', 'begin', 'all', 'last'):
            if self.check('LBRACKET'):
                from ..matrix import parse_index
                return parse_index(self, value.lower())
            return StringNode(value.lower())

        if self.check('LBRACKET'):
            from ..matrix import parse_index
            return parse_index(self, value)

        if self.check('LPAREN'):
            ctx = self._get_context(token)
            raise ArrayVatorError(
                code="UNKNOWN_FUNCTION",
                context=ctx,
                message=f"Неизвестная функция '{value}'.",
                suggestion=_build_unknown_function_suggestion(value),
            )

        return VariableNode(value)

    # ============================================================
    # LPAREN — группировка
    # ============================================================
    if token_type == 'LPAREN':
        self.expect('LPAREN')
        expr = self.parse_expression()
        self.expect('RPAREN')
        return expr

    # ============================================================
    # LBRACKET — матрица
    # ============================================================
    if token_type == 'LBRACKET':
        from ..matrix import parse_matrix
        return parse_matrix(self)

    return None