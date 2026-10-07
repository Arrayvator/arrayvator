# parser/parse_functions/filldown.py
"""
Парсинг FILLDOWN.

СИНТАКСИС:
    filldown(m[:, "Клиент"])
    filldown(m[:, "Клиент"], "")
"""

from ast_nodes.functions.filldown import FillDownNode
from errors import ArrayVatorError


def parse_filldown(self):
    """Парсинг FILLDOWN"""
    self.expect('LPAREN')

    data = self.parse_primary()

    from ast_nodes.index import IndexNode
    if not isinstance(data, IndexNode):
        raise ArrayVatorError(
            code="FILLDOWN_BAD_SYNTAX",
            context=self._get_context(),
            message=(
                "filldown: 1-й аргумент — срез m[:, \"X\"].\n"
                "  Пример: filldown(m[:, \"Клиент\"])"
            ),
        )

    empty_marker = None
    if self.check('COMMA'):
        self.expect('COMMA')
        empty_marker = self.parse_expression()

    self.expect('RPAREN')

    return FillDownNode(data, empty_marker)