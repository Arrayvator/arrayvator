# parser/parse_functions/groupby.py
"""
Парсинг GROUPBY.

СИНТАКСИС:
    r = groupby(by m[:, "Отдел"], agg sum(m[:, "Зарплата"]))

    r = groupby(by m[:, "Отдел"], m[:, "Год"],
                agg sum(m[:, "Продажи"]))

    r = groupby(by m[:, "Отдел"],
                agg sum(m[:, "Зарплата"]),
                    avg(m[:, "Зарплата"]),
                    count())

    r = groupby(by m[:, "Отдел"],
                agg sum(m[:, "Зарплата"]),
                having sum(m[:, "Зарплата"]) > 100000)
"""

from ast_nodes import GroupByNode, StringNode
from ast_nodes.index import IndexNode
from errors import ArrayVatorError


# ============================================================
# АГРЕГАТНЫЕ ФУНКЦИИ
# ============================================================
AGG_FUNCS = {
    'SUM': 'sum',
    'AVG': 'avg',
    'MIN': 'min',
    'MAX': 'max',
}

AGG_STR_FUNCS = {
    'count': 'count',
    'median': 'median',
    'first': 'first',
    'last': 'last',
    'std': 'std',
}

# Токены-агрегаты (лексер отдаёт их как отдельные типы, не IDENTIFIER)
TOKEN_AGG = {
    'COUNT':  'count',
    'MEDIAN': 'median',
    'STD':    'std',
}


def _parse_agg_expr(self):
    """
    Парсит один агрегат:
        sum(m[:, "X"])
        avg(m[:, "X"])
        count()
        count(m[:, "X"])
        median(m[:, "X"])
        std(m[:, "X"])
        first(m[:, "X"])
        last(m[:, "X"])

    Возвращает (agg_name, IndexNode | None).
    """
    token = self.peek()
    if not token:
        raise ArrayVatorError(
            code="GROUPBY_BAD_AGG_NAME",
            context=self._get_context(),
            message="groupby: ожидается агрегатная функция.",
        )

    token_type = token[0]
    value = token[1]

    # ============================================================
    # 1. SUM / AVG / MIN / MAX — всегда требуют срез
    # ============================================================
    if token_type in AGG_FUNCS:
        agg_name = AGG_FUNCS[token_type]
        self.pos += 1
        self.expect('LPAREN')
        arg = self.parse_primary()
        if not isinstance(arg, IndexNode):
            raise ArrayVatorError(
                code="GROUPBY_BAD_VALUE_SLICE",
                context=self._get_context(),
                message=f"groupby: {agg_name}() требует срез m[:, \"X\"].",
            )
        self.expect('RPAREN')
        return (agg_name, arg)

    # ============================================================
    # 2. COUNT / MEDIAN / STD — отдельные токены в лексере.
    #    ⚠️  count() может быть БЕЗ аргумента.
    # ============================================================
    if token_type in TOKEN_AGG:
        agg_name = TOKEN_AGG[token_type]
        self.pos += 1
        self.expect('LPAREN')

        # count() — без аргумента (считает строки в группе)
        if agg_name == 'count' and self.check('RPAREN'):
            self.pos += 1
            return (agg_name, None)

        # Иначе — обязателен срез m[:, "X"]
        arg = self.parse_primary()
        if not isinstance(arg, IndexNode):
            raise ArrayVatorError(
                code="GROUPBY_BAD_VALUE_SLICE",
                context=self._get_context(),
                message=f"groupby: {agg_name}(...) требует срез m[:, \"X\"].",
            )
        self.expect('RPAREN')
        return (agg_name, arg)

    # ============================================================
    # 3. FIRST / LAST — лексер отдаёт их как IDENTIFIER
    # ============================================================
    if token_type == 'IDENTIFIER':
        name_lower = value.lower()
        if name_lower in AGG_STR_FUNCS:
            agg_name = AGG_STR_FUNCS[name_lower]
            self.pos += 1
            self.expect('LPAREN')

            # На всякий случай — если count всё-таки попадёт сюда
            if agg_name == 'count' and self.check('RPAREN'):
                self.pos += 1
                return (agg_name, None)

            arg = self.parse_primary()
            if not isinstance(arg, IndexNode):
                raise ArrayVatorError(
                    code="GROUPBY_BAD_VALUE_SLICE",
                    context=self._get_context(),
                    message=f"groupby: {agg_name}() требует срез m[:, \"X\"].",
                )
            self.expect('RPAREN')
            return (agg_name, arg)

    raise ArrayVatorError(
        code="GROUPBY_BAD_AGG_NAME",
        context=self._get_context(token),
        message=f"groupby: неизвестная агрегатная функция '{value}'.",
    )


def _parse_having(self):
    """Парсит HAVING: having sum(m[:, "X"]) > 100."""
    self.expect('HAVING')

    agg_name, agg_node = _parse_agg_expr(self)

    op_token = self.peek()
    if not op_token or op_token[0] not in (
        'EQUALS', 'NOTEQUAL', 'LESS', 'GREATER', 'LESSEQUAL', 'GREATEREQUAL'
    ):
        raise ArrayVatorError(
            code="GROUPBY_HAVING_BAD",
            context=self._get_context(op_token),
            message="groupby: в having ожидается оператор сравнения.",
        )
    op = self.expect(op_token[0])[0]

    value = self.parse_expression()

    return (agg_name, agg_node, op, value)


def parse_groupby(self):
    """Парсинг GROUPBY"""
    self.expect('LPAREN')

    # ============================================================
    # 1. BY — список ключей
    # ============================================================
    by_token = self.peek()
    if not by_token or by_token[0] != 'BY':
        raise ArrayVatorError(
            code="GROUPBY_NEED_BY",
            context=self._get_context(by_token),
        )
    self.expect('BY')

    by_list = []
    first_by = self.parse_primary()
    if not isinstance(first_by, IndexNode):
        raise ArrayVatorError(
            code="GROUPBY_BAD_KEY_SLICE",
            context=self._get_context(),
            message="groupby: ключ должен быть срезом m[:, \"X\"].",
        )
    by_list.append(first_by)

    while self.check('COMMA'):
        save_pos = self.pos
        self.expect('COMMA')
        nxt = self.peek()
        if nxt and nxt[0] in ('AGG', 'HAVING', 'RPAREN'):
            self.pos = save_pos
            break

        next_by = self.parse_primary()
        if not isinstance(next_by, IndexNode):
            self.pos = save_pos
            break
        by_list.append(next_by)

    # ============================================================
    # 2. AGG — список агрегатов
    # ============================================================
    if not self.check('COMMA'):
        raise ArrayVatorError(
            code="GROUPBY_NEED_AGG",
            context=self._get_context(),
        )
    self.expect('COMMA')

    agg_token = self.peek()
    if not agg_token or agg_token[0] != 'AGG':
        raise ArrayVatorError(
            code="GROUPBY_NEED_AGG",
            context=self._get_context(agg_token),
        )
    self.expect('AGG')

    agg_list = []
    agg_list.append(_parse_agg_expr(self))

    while self.check('COMMA'):
        save_pos = self.pos
        self.expect('COMMA')
        nxt = self.peek()
        if nxt and nxt[0] in ('HAVING', 'RPAREN'):
            self.pos = save_pos
            break

        try:
            agg_list.append(_parse_agg_expr(self))
        except ArrayVatorError:
            self.pos = save_pos
            break

    # ============================================================
    # 3. HAVING (опционально)
    # ============================================================
    having = None
    if self.check('COMMA'):
        self.expect('COMMA')
        if self.check('HAVING'):
            having = _parse_having(self)

    self.expect('RPAREN')
    return GroupByNode(by_list, agg_list, having)