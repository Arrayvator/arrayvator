# parser/parse_functions/unpivot.py
"""
Парсинг UNPIVOT.

СИНТАКСИС:
    unpivot(срез, by срез)
    unpivot(срез, by срез1, срез2, ...)
    unpivot(срез, by срез, names "Имя1", "Имя2")
    unpivot(срез, by срез1, срез2, names "Имя1", "Имя2")

ПРИМЕРЫ:
    r = unpivot(m[:, 2:end], by m[:, "Страна"])
    r = unpivot(m[:, 3:end], by m[:, "Страна"], m[:, "Город"])
    r = unpivot(m[:, 2:end], by m[:, "Страна"],
                names "Год", "Население")
    r = unpivot(m[:, 3:end], by m[:, 1:2])     # диапазон
"""

from ast_nodes import UnpivotNode
from ast_nodes.index import IndexNode
from errors import ArrayVatorError


def parse_unpivot(self):
    """Парсинг UNPIVOT"""
    self.expect('LPAREN')

    # ============================================================
    # 1. Первый аргумент — срез данных
    # ============================================================
    data = self.parse_primary()
    if not isinstance(data, IndexNode):
        raise ArrayVatorError(
            code="UNPIVOT_BAD_DATA_SLICE",
            context=self._get_context(),
        )

    if not self.check('COMMA'):
        raise ArrayVatorError(
            code="UNPIVOT_NEED_BY",
            context=self._get_context(),
        )
    self.expect('COMMA')

    # ============================================================
    # 2. by — обязательный
    # ============================================================
    by_token = self.peek()
    if not by_token or by_token[0] != 'BY':
        raise ArrayVatorError(
            code="UNPIVOT_NEED_BY",
            context=self._get_context(by_token),
        )
    self.pos += 1

    # 2.1. Первый by-срез — обязателен
    by_first = self.parse_primary()
    if not isinstance(by_first, IndexNode):
        raise ArrayVatorError(
            code="UNPIVOT_BAD_BY_SLICE",
            context=self._get_context(),
        )

    # 2.2. Второй (и последующие) by-срезы — опционально
    #
    #     Отличие от `names`:
    #         by m[:, "A"], m[:, "B"]        ← второй by-срез
    #         by m[:, "A"], names "X", "Y"   ← блок names
    #
    #     Смотрим на следующий токен после COMMA:
    #         IDENTIFIER с именем "names" → это names
    #         IDENTIFIER (другое)         → это ещё один by-срез
    #
    by_list = [by_first]

    while self.check('COMMA'):
        save_pos = self.pos
        self.expect('COMMA')

        nxt = self.peek()
        if not nxt:
            self.pos = save_pos
            break

        # ------------------------------------------------------------------
        # `names` — стоп, переходим к блоку имён
        # ------------------------------------------------------------------
        if (nxt[0] == 'IDENTIFIER'
                and str(nxt[1]).lower() == 'names'):
            self.pos = save_pos
            break

        # ------------------------------------------------------------------
        # Ещё один by-срез
        # ------------------------------------------------------------------
        try:
            extra_by = self.parse_primary()
        except Exception:
            self.pos = save_pos
            break

        if not isinstance(extra_by, IndexNode):
            self.pos = save_pos
            break

        by_list.append(extra_by)

    # ============================================================
    # 3. names (опционально)
    # ============================================================
    names = None

    if self.check('COMMA'):
        self.expect('COMMA')

        names_token = self.peek()
        if (not names_token
                or names_token[0] != 'IDENTIFIER'
                or str(names_token[1]).lower() != 'names'):
            raise ArrayVatorError(
                code="UNPIVOT_BAD_NAMES",
                context=self._get_context(names_token),
            )
        self.pos += 1

        name1 = self.parse_expression()

        if not self.check('COMMA'):
            raise ArrayVatorError(
                code="UNPIVOT_BAD_NAMES",
                context=self._get_context(),
            )
        self.expect('COMMA')

        name2 = self.parse_expression()

        # Третий элемент — ошибка
        if self.check('COMMA'):
            raise ArrayVatorError(
                code="UNPIVOT_BAD_NAMES",
                context=self._get_context(),
            )

        names = (name1, name2)

    self.expect('RPAREN')

    # Если один by — передаём один узел, если несколько — список
    by_result = by_list[0] if len(by_list) == 1 else by_list

    return UnpivotNode(data, by_result, names)