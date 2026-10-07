# parser/parse_functions/trim.py
"""
Парсинг trim / trimleft / trimright.

СИНТАКСИС:
    trim(s)                    — обе стороны
    trim(s, "chars")           — обе стороны, свои символы

    trimleft(s)                — слева
    trimleft(s, "chars")       — слева, свои символы

    trimright(s)               — справа
    trimright(s, "chars")      — справа, свои символы

ПРАВИЛА ПАРСИНГА:
    1-й аргумент — данные (срез, переменная, вектор, скаляр).
    2-й (опц.) — строка символов в кавычках.
"""

from ast_nodes import TrimNode, TrimLeftNode, TrimRightNode
from errors import ArrayVatorError


def _parse_trim_generic(self, node_class, func_name):
    """Общий парсер для trim / trimleft / trimright."""
    self.expect('LPAREN')

    if self.check('RPAREN'):
        raise ArrayVatorError(
            code="TRIM_BAD_SYNTAX",
            context=self._get_context(),
            message=(
                f"{func_name}: нужен хотя бы один аргумент.\n"
                f"  Пример: {func_name}(m[:, \"Имя\"])"
            ),
        )

    # 1. Данные
    save_pos = self.pos
    try:
        data = self.parse_primary()
    except Exception:
        self.pos = save_pos
        data = self.parse_expression()

    # 2. Опциональные символы
    chars = None
    if self.check('COMMA'):
        self.expect('COMMA')

        if self.check('RPAREN'):
            raise ArrayVatorError(
                code="TRIM_BAD_SYNTAX",
                context=self._get_context(),
                message=(
                    f"{func_name}: после запятой ожидается строка символов.\n"
                    f"  Пример: {func_name}(m[:, \"Имя\"], \"+-\")"
                ),
            )

        chars = self.parse_expression()

    self.expect('RPAREN')

    return node_class(data, chars)


def parse_trim(self):
    """Парсинг TRIM."""
    return _parse_trim_generic(self, TrimNode, 'trim')


def parse_trimleft(self):
    """Парсинг TRIMLEFT."""
    return _parse_trim_generic(self, TrimLeftNode, 'trimleft')


def parse_trimright(self):
    """Парсинг TRIMRIGHT."""
    return _parse_trim_generic(self, TrimRightNode, 'trimright')