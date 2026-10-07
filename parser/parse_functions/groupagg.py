# parser/parse_functions/groupagg.py
"""
Парсинг GROUPAGG.

СИНТАКСИС:
    groupagg(m[:, "Клиент"], m[:, "Сумма"], sum)
    groupagg(m[:, "Клиент"], m[:, "Сумма"], sum, "ИТОГО")
    groupagg(m[:, "Клиент"], m[:, "Сумма"], sum, "ИТОГО", fill)
    groupagg(m[:, "Клиент"], m[:, "Сумма"], sum, "ИТОГО", exact)

АГРЕГАТЫ:
    sum, count, avg, min, max, median, std, first, last

ОСОБЕННОСТИ ЛЕКСЕРА:
    sum     → SUM
    count   → COUNT
    avg     → AVG
    min     → MIN
    max     → MAX
    median  → MEDIAN
    std     → STD
    first   → IDENTIFIER
    last    → LAST_KEYWORD     ← ключевое слово индексации!
"""

from ast_nodes import StringNode
from ast_nodes.functions.groupagg import GroupAggNode
from errors import ArrayVatorError


AGG_NAMES = {
    'sum', 'count', 'avg', 'min', 'max',
    'median', 'std', 'first', 'last',
}


def parse_groupagg(self):
    """Парсинг GROUPAGG"""
    from ast_nodes.index import IndexNode

    self.expect('LPAREN')

    # 1. Key slice
    key_slice = self.parse_primary()

    if not isinstance(key_slice, IndexNode):
        raise ArrayVatorError(
            code="GROUPAGG_BAD_KEY_SLICE",
            context=self._get_context(),
            message=(
                "groupagg: 1-й аргумент — срез m[:, \"X\"].\n"
                "  Пример: groupagg(m[:, \"Клиент\"], m[:, \"Сумма\"], sum)"
            ),
            suggestion=(
                "Первый аргумент — срез столбца-маркера:\n"
                "     m[:, \"Клиент\"]\n"
                "     m[:, 1]"
            ),
        )

    self.expect('COMMA')

    # 2. Value slice
    value_slice = self.parse_primary()

    if not isinstance(value_slice, IndexNode):
        raise ArrayVatorError(
            code="GROUPAGG_BAD_VALUE_SLICE",
            context=self._get_context(),
            message=(
                "groupagg: 2-й аргумент — срез m[:, \"X\"].\n"
                "  Пример: groupagg(m[:, \"Клиент\"], m[:, \"Сумма\"], sum)"
            ),
            suggestion=(
                "Второй аргумент — срез столбца-значения:\n"
                "     m[:, \"Сумма\"]\n"
                "     m[:, 2]"
            ),
        )

    self.expect('COMMA')

    # 3. Agg
    agg_token = self.peek()
    if not agg_token:
        raise ArrayVatorError(
            code="GROUPAGG_BAD_AGG",
            context=self._get_context(),
            message="groupagg: ожидается агрегат.",
            suggestion=(
                "Допустимо: sum, count, avg, min, max,\n"
                "           median, std, first, last"
            ),
        )

    # ============================================================
    # МЯГКАЯ ПРОВЕРКА ПО ЗНАЧЕНИЮ ТОКЕНА
    # ============================================================
    # Не смотрим на тип токена — лексер отдаёт разные типы:
    #   SUM, COUNT, AVG, MIN, MAX, MEDIAN, STD  — специальные
    #   FIRST                                    — IDENTIFIER
    #   LAST                                     — LAST_KEYWORD
    # Значение у всех — строка 'sum', 'last', 'first' и т.д.
    # ============================================================
    token_value = str(agg_token[1]).lower().strip()

    if token_value in AGG_NAMES:
        agg = token_value
        self.pos += 1
    else:
        raise ArrayVatorError(
            code="GROUPAGG_BAD_AGG",
            context=self._get_context(agg_token),
            message=(
                f"groupagg: неверный агрегат '{agg_token[1]}'.\n"
                f"  Допустимо: sum, count, avg, min, max,\n"
                f"             median, std, first, last"
            ),
            suggestion=(
                "Допустимо: sum, count, avg, min, max,\n"
                "           median, std, first, last"
            ),
        )

    # 4. Name (опционально)
    name = None
    if self.check('COMMA'):
        self.expect('COMMA')
        name = self.parse_expression()

    # 5. Mode (опционально)
    mode = None
    if self.check('COMMA'):
        self.expect('COMMA')
        mode_token = self.peek()
        if mode_token and mode_token[0] in ('FILL', 'EXACT'):
            mode = StringNode(mode_token[1].lower())
            self.pos += 1
        else:
            raise ArrayVatorError(
                code="GROUPAGG_BAD_MODE",
                context=self._get_context(mode_token),
                message=(
                    "groupagg: режим должен быть fill или exact."
                ),
                suggestion=(
                    "Допустимо:\n"
                    "     fill  — пустые к блоку\n"
                    "     exact — каждое значение — блок"
                ),
            )

    self.expect('RPAREN')

    return GroupAggNode(key_slice, value_slice, agg, name, mode)