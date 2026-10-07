# parser/parse_functions/conditional_agg.py
"""
Парсинг условных агрегатов.

СИНТАКСИС:

    sumif(усл, срез)
    sumif(by m[:, "X"], срез)
    countif(усл)
    countif(by m[:, "X"])
    avgif(усл, срез)
    avgif(by m[:, "X"], срез)
    minif(усл, срез)
    minif(by m[:, "X"], срез)
    maxif(усл, срез)
    maxif(by m[:, "X"], срез)
    medianif(усл, срез)
    countuniqueif(усл, срез)
    sumproduct(срез1, срез2 [, срез3, ...])

ПРАВИЛА:
    - Перед парсингом условия проверяем, что в нём нет
      одиночного '=' (ASSIGN). Если есть — бросаем
      <PREFIX>_ASSIGN_IN_CONDITION.
"""

from ast_nodes import (
    SumIfNode, CountIfNode, AvgIfNode,
    MinIfNode, MaxIfNode, MedianIfNode,
    CountUniqueIfNode, SumProductNode,
)
from ast_nodes.index import IndexNode
from errors import ArrayVatorError


# ============================================================
# ПРОВЕРКА: '=' ВМЕСТО '==' В УСЛОВИИ
# ============================================================
def _check_assign_in_condition(self, error_code):
    """
    Проверяет, что в условии нет одиночного '=' (ASSIGN).
    Идёт по токенам до запятой верхнего уровня.

    Бросает ArrayVatorError с указанным кодом, если нашёл ASSIGN.

    ⚠️  ВАЖНО: не путать ASSIGN (=) и EQUALS (==).
        Лексер выдаёт их разными токенами:
            '=='  → 'EQUALS'
            '='   → 'ASSIGN'
    """
    save_pos = self.pos
    depth = 0

    while self.peek():
        token = self.peek()
        t = token[0]

        # Отслеживаем вложенность
        if t in ('LPAREN', 'LBRACKET'):
            depth += 1
        elif t in ('RPAREN', 'RBRACKET'):
            if depth == 0:
                break
            depth -= 1
        elif t == 'COMMA' and depth == 0:
            break

        if t == 'ASSIGN' and depth == 0:
            self.pos = save_pos
            raise ArrayVatorError(
                code=error_code,
                context=self._get_context(token),
            )

        self.pos += 1

    self.pos = save_pos


# ============================================================
# ХЕЛПЕР: ПОИСК BY
# ============================================================
def _try_parse_by(self):
    if not self.check('BY'):
        return None
    self.expect('BY')
    by_node = self.parse_primary()
    if not isinstance(by_node, IndexNode):
        raise ArrayVatorError(
            code="CONDAGG_BY_NOT_SLICE",
            context=self._get_context(),
            message="by требует срез m[:, \"X\"].",
        )
    return by_node


# ============================================================
# ОБЩИЙ ПАРСЕР ДЛЯ COND-AGG (кроме sumproduct)
# ============================================================
def _parse_cond_agg(self, node_class, has_value=True, error_prefix='CONDAGG'):
    """
    Парсит sumif / countif / avgif / minif / maxif / medianif / countuniqueif.

    error_prefix — префикс для кода ошибки:
        'SUMIF'       → SUMIF_ASSIGN_IN_CONDITION
        'COUNTIF'     → COUNTIF_ASSIGN_IN_CONDITION
        'AVGIF'       → AVGIF_ASSIGN_IN_CONDITION
        'MINIF'       → MINIF_ASSIGN_IN_CONDITION
        'MAXIF'       → MAXIF_ASSIGN_IN_CONDITION
        'MEDIANIF'    → MEDIANIF_ASSIGN_IN_CONDITION
        'COUNTUNIQUEIF' → COUNTUNIQUEIF_ASSIGN_IN_CONDITION
    """
    self.expect('LPAREN')

    # ============================================================
    # 1. Проверка на '=' в условии (ДО парсинга)
    # ============================================================
    assign_error_code = f'{error_prefix}_ASSIGN_IN_CONDITION'
    _check_assign_in_condition(self, assign_error_code)

    # ============================================================
    # 2. BY или CONDITION
    # ============================================================
    by_node = _try_parse_by(self)

    if by_node is not None:
        value_col = None
        if self.check('COMMA'):
            self.expect('COMMA')
            if not self.check('RPAREN'):
                value_col = self.parse_primary()
                if not isinstance(value_col, IndexNode):
                    raise ArrayVatorError(
                        code="CONDAGG_VALUE_NOT_SLICE",
                        context=self._get_context(),
                        message="value_col — срез m[:, \"X\"].",
                    )
        self.expect('RPAREN')
        return node_class(condition=None, value_col=value_col, by=by_node)

    condition = self.parse_expression()

    value_col = None
    if has_value:
        self.expect('COMMA')
        value_col = self.parse_primary()
        if not isinstance(value_col, IndexNode):
            raise ArrayVatorError(
                code="CONDAGG_VALUE_NOT_SLICE",
                context=self._get_context(),
                message="value_col — срез m[:, \"X\"].",
            )

    self.expect('RPAREN')
    return node_class(condition=condition, value_col=value_col, by=None)


# ============================================================
# КОНКРЕТНЫЕ ФУНКЦИИ
# ============================================================
def parse_sumif(self):
    return _parse_cond_agg(
        self, SumIfNode, has_value=True, error_prefix='SUMIF'
    )


def parse_countif(self):
    return _parse_cond_agg(
        self, CountIfNode, has_value=False, error_prefix='COUNTIF'
    )


def parse_avgif(self):
    return _parse_cond_agg(
        self, AvgIfNode, has_value=True, error_prefix='AVGIF'
    )


def parse_minif(self):
    return _parse_cond_agg(
        self, MinIfNode, has_value=True, error_prefix='MINIF'
    )


def parse_maxif(self):
    return _parse_cond_agg(
        self, MaxIfNode, has_value=True, error_prefix='MAXIF'
    )


def parse_medianif(self):
    return _parse_cond_agg(
        self, MedianIfNode, has_value=True, error_prefix='MEDIANIF'
    )


def parse_countuniqueif(self):
    return _parse_cond_agg(
        self, CountUniqueIfNode, has_value=True, error_prefix='COUNTUNIQUEIF'
    )


# ============================================================
# SUMPRODUCT
# ============================================================
def parse_sumproduct(self):
    self.expect('LPAREN')

    columns = []
    first = self.parse_primary()
    if not isinstance(first, IndexNode):
        raise ArrayVatorError(
            code="SUMPRODUCT_BAD_ARG",
            context=self._get_context(),
            message="sumproduct: аргументы — срезы m[:, \"X\"].",
        )
    columns.append(first)

    while self.check('COMMA'):
        self.expect('COMMA')
        col = self.parse_primary()
        if not isinstance(col, IndexNode):
            raise ArrayVatorError(
                code="SUMPRODUCT_BAD_ARG",
                context=self._get_context(),
                message="sumproduct: аргументы — срезы m[:, \"X\"].",
            )
        columns.append(col)

    self.expect('RPAREN')

    if len(columns) < 2:
        raise ArrayVatorError(
            code="SUMPRODUCT_BAD_SYNTAX",
            context=self._get_context(),
            message="sumproduct: нужно минимум два среза.",
        )

    return SumProductNode(columns)