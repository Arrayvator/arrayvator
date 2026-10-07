# parser/parse_functions/join.py
"""
Парсинг JOIN (для таблиц).

СИНТАКСИС:
    join(m1, m2, on "ID")
    join(m1, m2, on "ID", how "left")
    join(m1, m2, on ["ID", "Дата"])
    join(m1, m2, on "ID" == "Код")
    join(m1, m2, on "ID", suffixes ["_1", "_2"])

ПРАВИЛА:
    - how — только left / inner / right / outer.
    - suffixes — массив из ДВУХ строк.
    - on — обязательное ключевое слово.
"""

from ast_nodes import JoinNode, StringNode
from errors import ArrayVatorError


# ============================================================
# ДОПУСТИМЫЕ РЕЖИМЫ HOW
# ============================================================
ALLOWED_HOW = {"left", "inner", "right", "outer"}


def parse_join(self):
    """Парсинг JOIN"""
    self.expect('LPAREN')

    # ============================================================
    # 1. Левая таблица
    # ============================================================
    left = self.parse_expression()

    if not self.check('COMMA'):
        raise ArrayVatorError(
            code="JOIN_NEED_TWO_TABLES",
            context=self._get_context(),
            message="join: нужно ДВЕ таблицы.",
        )
    self.expect('COMMA')

    # ============================================================
    # 2. Правая таблица
    # ============================================================
    right = self.parse_expression()

    if not self.check('COMMA'):
        raise ArrayVatorError(
            code="JOIN_NEED_ON",
            context=self._get_context(),
            message="join: пропущено ключевое слово 'on'.",
        )
    self.expect('COMMA')

    # ============================================================
    # 3. ON — ключи соединения
    # ============================================================
    on_token = self.peek()
    if not on_token or on_token[0] != 'ON':
        raise ArrayVatorError(
            code="JOIN_NEED_ON",
            context=self._get_context(on_token),
        )
    self.expect('ON')

    on_keys = []

    if self.check('LBRACKET'):
        # on ["ID", "Дата"]
        self.expect('LBRACKET')
        while True:
            on_keys.append(_parse_one_key(self))
            if self.check('COMMA'):
                self.expect('COMMA')
            else:
                break
        self.expect('RBRACKET')
    else:
        on_keys.append(_parse_one_key(self))

    # ============================================================
    # 4. HOW / SUFFIXES (опционально)
    # ============================================================
    how = "left"
    suffixes = None

    while self.check('COMMA'):
        self.expect('COMMA')
        token = self.peek()
        if not token:
            break

        # --------------------------------------------------------
        # HOW
        # --------------------------------------------------------
        if token[0] == 'HOW':
            how_token = token
            self.expect('HOW')
            how_val = self.parse_expression()

            if not isinstance(how_val, StringNode):
                raise ArrayVatorError(
                    code="JOIN_BAD_HOW",
                    context=self._get_context(how_token),
                )

            how_str = how_val.value.strip().lower()

            if how_str not in ALLOWED_HOW:
                raise ArrayVatorError(
                    code="JOIN_BAD_HOW",
                    context=self._get_context(how_token),
                )

            how = how_str

        # --------------------------------------------------------
        # SUFFIXES
        # --------------------------------------------------------
        elif token[0] == 'SUFFIXES':
            self.expect('SUFFIXES')

            if not self.check('LBRACKET'):
                raise ArrayVatorError(
                    code="JOIN_BAD_SUFFIXES",
                    context=self._get_context(),
                    message=(
                        "join: suffixes требует список из ДВУХ строк.\n"
                        "  Пример: suffixes [\"_1\", \"_2\"]."
                    ),
                )

            self.expect('LBRACKET')

            s1 = self.parse_expression()
            self.expect('COMMA')
            s2 = self.parse_expression()

            # Третий элемент — ошибка
            if self.check('COMMA'):
                raise ArrayVatorError(
                    code="JOIN_BAD_SUFFIXES",
                    context=self._get_context(),
                    message=(
                        "join: suffixes требует РОВНО ДВЕ строки.\n"
                        "  Пример: suffixes [\"_1\", \"_2\"]."
                    ),
                )

            self.expect('RBRACKET')

            suffixes = (
                s1.value if isinstance(s1, StringNode) else str(s1),
                s2.value if isinstance(s2, StringNode) else str(s2),
            )

        else:
            break

    self.expect('RPAREN')
    return JoinNode(left, right, on_keys, how, suffixes)


# ============================================================
# ПАРСИНГ ОДНОГО КЛЮЧА
# ============================================================
def _parse_one_key(self):
    """
    Парсит один ключ: "ID" или "ID" == "Код".

    Возвращает кортеж (left_name, right_name) — обе строки.
    """
    left = self.parse_primary()
    left_name = left.value if isinstance(left, StringNode) else str(left)

    if self.check('EQUALS'):
        self.expect('EQUALS')
        right = self.parse_primary()
        right_name = right.value if isinstance(right, StringNode) else str(right)
        return (left_name, right_name)

    return (left_name, left_name)