# parser/parse_functions/abc.py
"""
Парсинг ABC — ABC-анализ.

СИНТАКСИС (порядок аргументов ЛЮБОЙ):
    abc(срез)
    abc(срез, %)
    abc(срез, coef)
    abc(срез, %, m[:, 3])
    abc(срез, 70, 90)
    abc(срез, 70, 90, %, m[:, 3])
    abc(срез, m[:, 3], %)
    abc(срез, 90, %, m[:, 3], 70)

ПРАВИЛА ПАРСИНГА:
    1-й аргумент — обязательно срез (IndexNode).
    Дальше в любом порядке:
        - NUMBER   → порог (макс 2)
        - %        → опция 'percent'
        - COEF     → опция 'coef'
        - срез m[:, ...] → целевой столбец

    Валидация:
        - не больше 2 порогов
        - только одна опция
        - только один целевой
        - если целевой указан, но нет опции → ошибка

    Пороги автосортируются: 90, 70 → 70, 90.
"""

from ast_nodes import AbcNode
from errors import ArrayVatorError


def parse_abc(self):
    """Парсинг ABC."""
    self.expect('LPAREN')

    # 1. Обязательный срез
    data = self.parse_primary()
    from ast_nodes.index import IndexNode
    if not isinstance(data, IndexNode):
        raise ArrayVatorError(
            code="ABC_NEED_SLICE",
            context=self._get_context(),
        )

    # 2. Остальные аргументы — в любом порядке
    thresholds = []
    option = None
    target = None

    while self.check('COMMA'):
        self.expect('COMMA')

        token = self.peek()
        if not token:
            raise ArrayVatorError(
                code="ABC_BAD_SYNTAX",
                context=self._get_context(),
                message="abc: неожиданный конец аргументов.",
            )

        # 2.1. Число — порог
        if token[0] == 'NUMBER':
            val = self.parse_expression()
            thresholds.append(val)

        # 2.2. % — проценты
        elif token[0] == 'MOD':
            self.expect('MOD')
            if option is not None:
                raise ArrayVatorError(
                    code="ABC_TOO_MANY_OPTIONS",
                    context=self._get_context(token),
                )
            option = 'percent'

        # 2.3. coef — коэффициент
        elif token[0] == 'COEF':
            self.expect('COEF')
            if option is not None:
                raise ArrayVatorError(
                    code="ABC_TOO_MANY_OPTIONS",
                    context=self._get_context(token),
                )
            option = 'coef'

        # 2.4. Срез — целевой столбец
        elif (token[0] == 'IDENTIFIER'
              and self.peek(1)
              and self.peek(1)[0] == 'LBRACKET'):
            if target is not None:
                raise ArrayVatorError(
                    code="ABC_TOO_MANY_TARGETS",
                    context=self._get_context(token),
                )
            target = self.parse_primary()
            from ast_nodes.index import IndexNode
            if not isinstance(target, IndexNode):
                raise ArrayVatorError(
                    code="ABC_BAD_TARGET",
                    context=self._get_context(token),
                )

        else:
            raise ArrayVatorError(
                code="ABC_BAD_SYNTAX",
                context=self._get_context(token),
                message=(
                    f"abc: неожиданный аргумент '{token[1]}'.\n"
                    f"  Ожидается: порог (число), %, coef "
                    f"или срез m[:, ...]."
                ),
            )

    self.expect('RPAREN')

    # 3. Валидация
    if len(thresholds) > 2:
        raise ArrayVatorError(
            code="ABC_TOO_MANY_THRESHOLDS",
            context=self._get_context(),
        )

    if target is not None and option is None:
        raise ArrayVatorError(
            code="ABC_TARGET_WITHOUT_OPTION",
            context=self._get_context(),
        )

    return AbcNode(data, thresholds, option, target)