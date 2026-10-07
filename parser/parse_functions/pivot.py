# parser/parse_functions/pivot.py
"""
Парсинг PIVOT — сводная таблица.

СИНТАКСИС:
    # Один ключ (3 аргумента)
    pivot(ключ, значения, агрегат)

    # Два ключа (4 аргумента)
    pivot(ключ_строк, ключ_столбцов, значения, агрегат)

МНЕМОНИКА (один ключ):
    pivot( ключ , значения , агрегат )
           └─a─┘   └──b───┘   └──c──┘
           группы  что считать как считать

МНЕМОНИКА (два ключа):
    pivot( ключ_строк , ключ_столбцов , значения , агрегат )
           └────a────┘  └─────b──────┘   └──c───┘   └──d───┘
           строки        столбцы          что считать как считать

АГРЕГАТЫ:
    sum, avg, count, min, max, median, first, last, std

ПРАВИЛА:
    - Все аргументы — срезы (m[:, "X"]), кроме последнего.
    - Последний аргумент — агрегат (sum, avg, ...).
    - 3 аргумента → один ключ (2 столбца).
    - 4 аргумента → два ключа (N×M таблица).
"""

from ast_nodes import PivotNode, StringNode
from ast_nodes.index import IndexNode
from errors import ArrayVatorError


# ============================================================
# АГРЕГАТЫ
# ============================================================
# Простые токены лексера (regex \bsum\b → SUM, \bavg\b → AVG, ...)
# Плюс count/median/std — они тоже отдельные токены
# (regex \bcount\b → COUNT, \bmedian\b → MEDIAN, \bstd\b → STD).
AGG_TOKENS = {'SUM', 'AVG', 'MIN', 'MAX',
              'COUNT', 'MEDIAN', 'STD'}

# Строковые имена — на случай IDENTIFIER/STRING.
AGG_STRINGS = {'sum', 'avg', 'count', 'min', 'max',
               'median', 'first', 'last', 'std'}


def _is_agg_token(self):
    """Проверяет, является ли следующий токен агрегатом."""
    token = self.peek()
    if not token:
        return False

    if token[0] in AGG_TOKENS:
        return True

    if token[0] in ('IDENTIFIER', 'STRING'):
        val = token[1]
        if isinstance(val, str) and val.lower().strip() in AGG_STRINGS:
            return True

    return False


def _parse_agg(self):
    """Парсит функцию агрегации."""
    token = self.peek()
    if not token:
        raise ArrayVatorError(
            code="PIVOT_BAD_SYNTAX",
            context=self._get_context(),
            message="pivot: ожидается функция агрегации.",
            suggestion=(
                "Доступные агрегаты:\n"
                "     sum, avg, count, min, max,\n"
                "     median, first, last, std"
            ),
        )

    token_type = token[0]
    value = token[1]

    # Токены лексера: SUM, AVG, MIN, MAX, COUNT, MEDIAN, STD
    if token_type in AGG_TOKENS:
        self.pos += 1
        return StringNode(token_type.lower())

    # IDENTIFIER / STRING: first, last (и на всякий случай остальные)
    if token_type in ('IDENTIFIER', 'STRING'):
        val_lower = value.lower().strip() if isinstance(value, str) else ''
        if val_lower in AGG_STRINGS:
            self.pos += 1
            return StringNode(val_lower)

    raise ArrayVatorError(
        code="PIVOT_BAD_SYNTAX",
        context=self._get_context(token),
        message=(
            f"pivot: неверная функция агрегации: '{value}'.\n"
            f"  Доступные: sum, avg, count, min, max,\n"
            f"             median, first, last, std"
        ),
    )


def _parse_slice(self, arg_name):
    """Парсит срез столбца и валидирует."""
    node = self.parse_primary()
    if not isinstance(node, IndexNode):
        raise ArrayVatorError(
            code="PIVOT_BAD_SYNTAX",
            context=self._get_context(),
            message=(
                f"pivot: {arg_name} — срез столбца m[:, \"X\"].\n"
                f"  Пример: pivot(m[:, \"Отдел\"], m[:, \"Зарплата\"], sum)"
            ),
        )
    return node


def parse_pivot(self):
    """Парсинг PIVOT."""
    self.expect('LPAREN')

    # ============================================================
    # 1. Первый ключ (обязательно)
    # ============================================================
    key1 = _parse_slice(self, "ключ")

    self.expect('COMMA')

    # ============================================================
    # 2. Второй аргумент — либо key2, либо values
    # ============================================================
    second = _parse_slice(self, "второй аргумент")

    self.expect('COMMA')

    # ============================================================
    # 3. Третий аргумент — либо values, либо agg
    # ============================================================
    # КЛЮЧЕВОЕ: сначала проверяем — а не агрегат ли это?
    if _is_agg_token(self):
        # ---------------------------------------------------------
        # 3 аргумента: key1, values, agg
        # ---------------------------------------------------------
        agg = _parse_agg(self)
        self.expect('RPAREN')

        return PivotNode(
            data=None,
            key1=key1,
            key2=None,
            values=second,
            agg=agg,
        )

    # ---------------------------------------------------------
    # Иначе — это values (срез), значит 4 аргумента
    # ---------------------------------------------------------
    values = _parse_slice(self, "значения")
    self.expect('COMMA')

    if not _is_agg_token(self):
        raise ArrayVatorError(
            code="PIVOT_BAD_SYNTAX",
            context=self._get_context(),
            message=(
                "pivot: 4-й аргумент — агрегат.\n"
                "  Пример: pivot(Отдел, Год, Зарплата, sum)"
            ),
        )

    agg = _parse_agg(self)
    self.expect('RPAREN')

    return PivotNode(
        data=None,
        key1=key1,
        key2=second,
        values=values,
        agg=agg,
    )