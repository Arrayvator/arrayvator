# parser/parse_functions/percentof.py
"""
Парсинг PERCENTOF — доля от итога.

СИНТАКСИС (порядок аргументов ЛЮБОЙ):
    percentof(срез)
    percentof(срез, coef)
    percentof(срез, by m[:, "Категория"])
    percentof(срез, by m[:, "Категория"], coef)
    percentof(срез, coef, by m[:, "Категория"])
"""

from ast_nodes import PercentOfNode
from ast_nodes.index import IndexNode
from errors import ArrayVatorError


def parse_percentof(self):
    """Парсинг PERCENTOF."""
    self.expect('LPAREN')

    # 1. Обязательный срез
    data = self.parse_primary()
    if not isinstance(data, IndexNode):
        raise ArrayVatorError(
            code="PERCENTOF_NEED_SLICE",
            context=self._get_context(),
        )

    # 2. Остальные аргументы — в любом порядке
    by = None
    option = None

    while self.check('COMMA'):
        self.expect('COMMA')

        token = self.peek()
        if not token:
            raise ArrayVatorError(
                code="PERCENTOF_BAD_SYNTAX",
                context=self._get_context(),
                message="percentof: неожиданный конец аргументов.",
            )

        # 2.1. coef — коэффициент
        if token[0] == 'COEF':
            self.expect('COEF')
            if option is not None:
                raise ArrayVatorError(
                    code="PERCENTOF_TOO_MANY_OPTIONS",
                    context=self._get_context(token),
                )
            option = 'coef'

        # 2.2. by срез — группировка
        elif token[0] == 'BY':
            self.expect('BY')
            if by is not None:
                raise ArrayVatorError(
                    code="PERCENTOF_TOO_MANY_BY",
                    context=self._get_context(token),
                )
            by = self.parse_primary()
            if not isinstance(by, IndexNode):
                raise ArrayVatorError(
                    code="PERCENTOF_BAD_BY",
                    context=self._get_context(),
                )

        # 2.3. Неизвестный аргумент
        else:
            raise ArrayVatorError(
                code="PERCENTOF_BAD_ARG",
                context=self._get_context(token),
                message=(
                    f"percentof: неожиданный аргумент '{token[1]}'.\n"
                    f"  Ожидается: coef или by m[:, ...]."
                ),
            )

    self.expect('RPAREN')

    return PercentOfNode(data, by=by, option=option)