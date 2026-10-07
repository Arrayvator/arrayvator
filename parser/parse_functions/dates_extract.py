# parser/parse_functions/dates_extract.py
"""
Парсинг функций дат и времени:
    year, month, day, quarter,
    weekday, weekdayname, monthname,
    adddays, addmonths, addyears,
    datetrunc,

    hour, minute, second,
    ampm, is_pm,
    addhours, addminutes, addseconds,
    timetrunc, time.

СИНТАКСИС:
    year(данные [, "формат"])
    hour(данные [, "формат"])
    adddays(данные, N [, "формат"])
    addhours(данные, N [, "формат"])
    datetrunc(данные, "единица" [, "формат"])
        единица: "day" | "month" | "quarter" | "year" | "hour" | "minute" | "second"
    timetrunc(данные, "единица" [, "формат"])
        единица: "hour" | "minute" | "second"
    time(данные, "входной", "выходной")
"""

from ast_nodes import (
    YearNode, MonthNode, DayNode, QuarterNode,
    WeekdayNode, WeekdayNameNode, MonthNameNode,
    AddDaysNode, AddMonthsNode, AddYearsNode,
    DateTruncNode,
)
from errors import ArrayVatorError


# ============================================================
# ОБЩИЕ ПАРСЕРЫ
# ============================================================
def _parse_extract_generic(self, node_class, func_name):
    """
    Общий парсер для year / month / day / quarter /
    weekday / weekdayname / monthname / hour / minute / second /
    ampm / is_pm.

    Аргументы:
        1. данные (обязательно)
        2. формат (опционально, строка)
    """
    self.expect('LPAREN')

    if self.check('RPAREN'):
        raise ArrayVatorError(
            code="DATE_EXTRACT_BAD_SYNTAX",
            context=self._get_context(),
        )

    # 1. Данные
    save_pos = self.pos
    try:
        data = self.parse_primary()
    except Exception:
        self.pos = save_pos
        data = self.parse_expression()

    # 2. Формат (опционально)
    fmt = None
    if self.check('COMMA'):
        self.expect('COMMA')

        if self.check('RPAREN'):
            raise ArrayVatorError(
                code="DATE_EXTRACT_BAD_SYNTAX",
                context=self._get_context(),
            )

        fmt = self.parse_expression()

    self.expect('RPAREN')

    return node_class(data, fmt)


def _parse_add_generic(self, node_class, func_name):
    """
    Общий парсер для adddays / addmonths / addyears /
    addhours / addminutes / addseconds.

    Аргументы:
        1. данные (обязательно)
        2. N — число (обязательно)
        3. формат (опционально, строка)
    """
    self.expect('LPAREN')

    if self.check('RPAREN'):
        raise ArrayVatorError(
            code="DATE_ADD_BAD_SYNTAX",
            context=self._get_context(),
        )

    # 1. Данные
    save_pos = self.pos
    try:
        data = self.parse_primary()
    except Exception:
        self.pos = save_pos
        data = self.parse_expression()

    # 2. N (обязательно)
    if not self.check('COMMA'):
        raise ArrayVatorError(
            code="DATE_ADD_BAD_SYNTAX",
            context=self._get_context(),
        )

    self.expect('COMMA')

    if self.check('RPAREN'):
        raise ArrayVatorError(
            code="DATE_ADD_BAD_SYNTAX",
            context=self._get_context(),
        )

    n = self.parse_expression()

    # 3. Формат (опционально)
    fmt = None
    if self.check('COMMA'):
        self.expect('COMMA')

        if self.check('RPAREN'):
            raise ArrayVatorError(
                code="DATE_ADD_BAD_SYNTAX",
                context=self._get_context(),
            )

        fmt = self.parse_expression()

    self.expect('RPAREN')

    return node_class(data, n, fmt)


# ============================================================
# ПАРСЕРЫ ИЗВЛЕЧЕНИЯ ДАТ
# ============================================================
def parse_year(self):
    return _parse_extract_generic(self, YearNode, 'year')


def parse_month(self):
    return _parse_extract_generic(self, MonthNode, 'month')


def parse_day(self):
    return _parse_extract_generic(self, DayNode, 'day')


def parse_quarter(self):
    return _parse_extract_generic(self, QuarterNode, 'quarter')


def parse_weekday(self):
    return _parse_extract_generic(self, WeekdayNode, 'weekday')


def parse_weekdayname(self):
    return _parse_extract_generic(self, WeekdayNameNode, 'weekdayname')


def parse_monthname(self):
    return _parse_extract_generic(self, MonthNameNode, 'monthname')


# ============================================================
# ПАРСЕРЫ АРИФМЕТИКИ ДАТ
# ============================================================
def parse_adddays(self):
    return _parse_add_generic(self, AddDaysNode, 'adddays')


def parse_addmonths(self):
    return _parse_add_generic(self, AddMonthsNode, 'addmonths')


def parse_addyears(self):
    return _parse_add_generic(self, AddYearsNode, 'addyears')


# ============================================================
# DATETRUNC
# ============================================================
def parse_datetrunc(self):
    """
    datetrunc(данные, "единица" [, "формат"])

    единица: "day" | "month" | "quarter" | "year"
             "hour" | "minute" | "second"
    """
    self.expect('LPAREN')

    if self.check('RPAREN'):
        raise ArrayVatorError(
            code="DATETRUNC_BAD_SYNTAX",
            context=self._get_context(),
        )

    # 1. Данные
    save_pos = self.pos
    try:
        data = self.parse_primary()
    except Exception:
        self.pos = save_pos
        data = self.parse_expression()

    # 2. Единица (обязательно)
    if not self.check('COMMA'):
        raise ArrayVatorError(
            code="DATETRUNC_BAD_SYNTAX",
            context=self._get_context(),
        )

    self.expect('COMMA')

    if self.check('RPAREN'):
        raise ArrayVatorError(
            code="DATETRUNC_BAD_SYNTAX",
            context=self._get_context(),
        )

    unit = self.parse_expression()

    # 3. Формат (опционально)
    fmt = None
    if self.check('COMMA'):
        self.expect('COMMA')

        if self.check('RPAREN'):
            raise ArrayVatorError(
                code="DATETRUNC_BAD_SYNTAX",
                context=self._get_context(),
            )

        fmt = self.parse_expression()

    self.expect('RPAREN')

    return DateTruncNode(data, unit, fmt)


# ============================================================
# ПАРСЕРЫ ВРЕМЕНИ
# ============================================================
def parse_hour(self):
    """hour(данные [, "формат"])"""
    from ast_nodes import HourNode
    return _parse_extract_generic(self, HourNode, 'hour')


def parse_minute(self):
    """minute(данные [, "формат"])"""
    from ast_nodes import MinuteNode
    return _parse_extract_generic(self, MinuteNode, 'minute')


def parse_second(self):
    """second(данные [, "формат"])"""
    from ast_nodes import SecondNode
    return _parse_extract_generic(self, SecondNode, 'second')


def parse_ampm(self):
    """ampm(данные [, "формат"])"""
    from ast_nodes import AmPmNode
    return _parse_extract_generic(self, AmPmNode, 'ampm')


def parse_is_pm(self):
    """is_pm(данные [, "формат"])"""
    from ast_nodes import IsPmNode
    return _parse_extract_generic(self, IsPmNode, 'is_pm')


def parse_addhours(self):
    """addhours(данные, N [, "формат"])"""
    from ast_nodes import AddHoursNode
    return _parse_add_generic(self, AddHoursNode, 'addhours')


def parse_addminutes(self):
    """addminutes(данные, N [, "формат"])"""
    from ast_nodes import AddMinutesNode
    return _parse_add_generic(self, AddMinutesNode, 'addminutes')


def parse_addseconds(self):
    """addseconds(данные, N [, "формат"])"""
    from ast_nodes import AddSecondsNode
    return _parse_add_generic(self, AddSecondsNode, 'addseconds')


def parse_timetrunc(self):
    """
    timetrunc(данные, "единица" [, "формат"])
    единица: "hour" | "minute" | "second"

    Проверка единицы выполняется ЗДЕСЬ (в парсере),
    чтобы текст ошибки брался из базы errors/messages/.
    """
    from ast_nodes import TimeTruncNode

    self.expect('LPAREN')

    if self.check('RPAREN'):
        raise ArrayVatorError(
            code="TIMETRUNC_BAD_SYNTAX",
            context=self._get_context(),
        )

    save_pos = self.pos
    try:
        data = self.parse_primary()
    except Exception:
        self.pos = save_pos
        data = self.parse_expression()

    if not self.check('COMMA'):
        raise ArrayVatorError(
            code="TIMETRUNC_BAD_SYNTAX",
            context=self._get_context(),
        )

    self.expect('COMMA')

    if self.check('RPAREN'):
        raise ArrayVatorError(
            code="TIMETRUNC_BAD_SYNTAX",
            context=self._get_context(),
        )

    # Парсим единицу
    unit_node = self.parse_expression()

    # Проверяем единицу ЗДЕСЬ, пока парсер знает контекст
    unit_val = (unit_node.evaluate(None)
                if hasattr(unit_node, 'evaluate')
                else unit_node)

    if not isinstance(unit_val, str):
        raise ArrayVatorError(
            code="TIMETRUNC_BAD_UNIT",
            context=self._get_context(),
        )

    unit_val_lower = unit_val.strip().lower()
    if unit_val_lower not in ('hour', 'minute', 'second'):
        raise ArrayVatorError(
            code="TIMETRUNC_BAD_UNIT",
            context=self._get_context(),
        )

    # Формат (опционально)
    fmt = None
    if self.check('COMMA'):
        self.expect('COMMA')
        fmt = self.parse_expression()

    self.expect('RPAREN')
    return TimeTruncNode(data, unit_node, fmt)


def parse_time(self):
    """
    time(данные, "входной", "выходной")
    Конвертер форматов времени.
    """
    from ast_nodes import TimeNode

    self.expect('LPAREN')

    if self.check('RPAREN'):
        raise ArrayVatorError(
            code="TIME_BAD_SYNTAX",
            context=self._get_context(),
        )

    data = self.parse_expression()

    if not self.check('COMMA'):
        raise ArrayVatorError(
            code="TIME_BAD_SYNTAX",
            context=self._get_context(),
        )
    self.expect('COMMA')

    in_fmt = self.parse_expression()

    if not self.check('COMMA'):
        raise ArrayVatorError(
            code="TIME_BAD_SYNTAX",
            context=self._get_context(),
        )
    self.expect('COMMA')

    out_fmt = self.parse_expression()

    self.expect('RPAREN')

    return TimeNode(data, in_fmt, out_fmt)