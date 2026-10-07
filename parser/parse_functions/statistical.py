# parser/parse_functions/statistical.py
"""
Парсинг статистических функций:
    sum, min, max, avg      — с опциональным by
    count                   — с опциональным by и опциональным аргументом
    median, std             — с опциональным by

СИНТАКСИС:

    # Без by — скаляр:
    r = sum(m[:, "Зарплата"])
    r = avg(m[:, "Зарплата"])
    r = min(m[:, "Зарплата"])
    r = max(m[:, "Зарплата"])
    r = median(m[:, "Зарплата"])
    r = std(m[:, "Зарплата"])
    r = count(m[:, "Зарплата"])
    r = count()                            — все строки

    # С by — вектор по группам:
    r = sum(m[:, "Зарплата"], by m[:, "Отдел"])
    r = avg(m[:, "Зарплата"], by m[:, "Отдел"])
    r = min(m[:, "Зарплата"], by m[:, "Отдел"])
    r = max(m[:, "Зарплата"], by m[:, "Отдел"])
    r = median(m[:, "Зарплата"], by m[:, "Отдел"])
    r = std(m[:, "Зарплата"], by m[:, "Отдел"])
    r = count(m[:, "Зарплата"], by m[:, "Отдел"])
    r = count(by m[:, "Отдел"])            — количество строк в группе
"""

from ast_nodes.functions import (
    SumNode, MinNode, MaxNode, AvgNode,
    CountNode, MedianNode, StdNode,
)
from ast_nodes.index import IndexNode
from errors import ArrayVatorError


# ============================================================
# ОБЩИЙ ПАРСЕР: <agg>(арг [, by ключ])
# ============================================================
def _parse_stat_with_optional_by(self, node_class, func_name, allow_no_arg=False):
    """
    Парсит <agg>( <arg> [, by <key>] )  или  <agg>( by <key> )  или  <agg>().

    Аргументы:
        node_class    — класс узла (SumNode / AvgNode / ...)
        func_name     — человеческое имя для ошибок ('sum', 'avg', ...)
        allow_no_arg  — разрешено ли вызывать без аргумента (только для count)
    """
    self.expect('LPAREN')

    arg = None
    by = None

    # ============================================================
    # СЛУЧАЙ 1: count() — сразу RPAREN
    # ============================================================
    if self.check('RPAREN'):
        if not allow_no_arg:
            raise ArrayVatorError(
                code=f"{func_name.upper()}_BAD_SYNTAX",
                context=self._get_context(),
                message=(
                    f"{func_name}: не указан аргумент.\n"
                    f"  Пример: {func_name}(m[:, \"Зарплата\"])"
                ),
                suggestion=(
                    f"Формат:\n"
                    f"     {func_name}(значение)\n"
                    f"     {func_name}(значение, by m[:, \"X\"])"
                ),
            )
        self.expect('RPAREN')
        return node_class(arg=None, by=None)

    # ============================================================
    # СЛУЧАЙ 2: <agg>(by m[:, "X"])  — только для count
    # ============================================================
    if self.check('BY'):
        if not allow_no_arg:
            raise ArrayVatorError(
                code=f"{func_name.upper()}_BAD_SYNTAX",
                context=self._get_context(),
                message=(
                    f"{func_name}: ключ by можно указывать только после аргумента.\n"
                    f"  Пример: {func_name}(m[:, \"Зарплата\"], by m[:, \"Отдел\"])"
                ),
                suggestion=(
                    f"Неправильно:\n"
                    f"     {func_name}(by m[:, \"Отдел\"])\n"
                    f"\n"
                    f"Правильно:\n"
                    f"     {func_name}(m[:, \"Зарплата\"], by m[:, \"Отдел\"])\n"
                    f"     {func_name}(by m[:, \"Отдел\"])   — только для count"
                ),
            )
        self.expect('BY')
        by = self.parse_primary()
        if not isinstance(by, IndexNode):
            raise ArrayVatorError(
                code=f"{func_name.upper()}_BAD_BY",
                context=self._get_context(),
                message=(
                    f"{func_name}: by должен быть срезом m[:, \"X\"]."
                ),
                suggestion=(
                    f"Неправильно:\n"
                    f"     by \"Отдел\"\n"
                    f"     by 3\n"
                    f"\n"
                    f"Правильно:\n"
                    f"     by m[:, \"Отдел\"]"
                ),
            )
        self.expect('RPAREN')
        return node_class(arg=None, by=by)

    # ============================================================
    # СЛУЧАЙ 3: обычный аргумент — срез или выражение
    # ============================================================
    # Пытаемся распарсить как срез (m[:, "X"], v и т.п.)
    save_pos = self.pos
    try:
        arg = self.parse_primary()
    except Exception:
        self.pos = save_pos
        arg = self.parse_expression()

    # ============================================================
    # СЛУЧАЙ 4: запятая → ожидаем "by"
    # ============================================================
    if self.check('COMMA'):
        self.expect('COMMA')

        if not self.check('BY'):
            raise ArrayVatorError(
                code=f"{func_name.upper()}_NEED_BY",
                context=self._get_context(),
                message=(
                    f"{func_name}: после запятой ожидается 'by'.\n"
                    f"  Формат: {func_name}(значение, by ключ)"
                ),
                suggestion=(
                    f"Неправильно:\n"
                    f"     {func_name}(m[:, \"Зарплата\"], m[:, \"Отдел\"])\n"
                    f"\n"
                    f"Правильно:\n"
                    f"     {func_name}(m[:, \"Зарплата\"], by m[:, \"Отдел\"])"
                ),
            )

        self.expect('BY')
        by = self.parse_primary()

        if not isinstance(by, IndexNode):
            raise ArrayVatorError(
                code=f"{func_name.upper()}_BAD_BY",
                context=self._get_context(),
                message=(
                    f"{func_name}: by должен быть срезом m[:, \"X\"]."
                ),
                suggestion=(
                    f"Неправильно:\n"
                    f"     by \"Отдел\"\n"
                    f"     by 3\n"
                    f"\n"
                    f"Правильно:\n"
                    f"     by m[:, \"Отдел\"]"
                ),
            )

    self.expect('RPAREN')
    return node_class(arg=arg, by=by)


# ============================================================
# SUM / MIN / MAX / AVG
# ============================================================
def parse_statistical(self, token_type):
    """Старые функции: sum, min, max, avg — с опциональным by."""
    if token_type == 'SUM':
        return _parse_stat_with_optional_by(self, SumNode, 'sum')
    elif token_type == 'MIN':
        return _parse_stat_with_optional_by(self, MinNode, 'min')
    elif token_type == 'MAX':
        return _parse_stat_with_optional_by(self, MaxNode, 'max')
    elif token_type == 'AVG':
        return _parse_stat_with_optional_by(self, AvgNode, 'avg')

    raise ValueError(f"parse_statistical: неизвестный токен {token_type}")


# ============================================================
# COUNT
# ============================================================
def parse_count(self):
    """
    count()
    count(m[:, "X"])
    count(m[:, "X"], by m[:, "Y"])
    count(by m[:, "Y"])
    """
    return _parse_stat_with_optional_by(
        self, CountNode, 'count', allow_no_arg=True
    )


# ============================================================
# MEDIAN
# ============================================================
def parse_median(self):
    """
    median(m[:, "X"])
    median(m[:, "X"], by m[:, "Y"])
    """
    return _parse_stat_with_optional_by(self, MedianNode, 'median')


# ============================================================
# STD
# ============================================================
def parse_std(self):
    """
    std(m[:, "X"])
    std(m[:, "X"], by m[:, "Y"])
    """
    return _parse_stat_with_optional_by(self, StdNode, 'std')