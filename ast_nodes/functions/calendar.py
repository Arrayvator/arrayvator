# ast_nodes/functions/calendar.py
"""
Календарные функции: calendar, calendarpro.

СИНТАКСИС:
    calendar("dd.mm.yyyy", месяц, год [, "ru"|"eu"|"us"])
        месяц: 1-12 или all
        год:   1981, 2026, datenow()
        страна/язык: "ru" (по умолчанию), "eu", "us"

    calendarpro(год, месяц [, "ru"|"eu"|"us"])
        месяц: 1-12 или all
        страна: "ru" (по умолчанию), "eu", "us"
"""

import datetime

from ..base import Node
from runtime.matrix import MatrExMatrix
from errors import ArrayVatorError


# ============================================================
# НАЗВАНИЯ МЕСЯЦЕВ И ДНЕЙ
# ============================================================
MONTHS_RU = [
    "Январь", "Февраль", "Март", "Апрель", "Май", "Июнь",
    "Июль", "Август", "Сентябрь", "Октябрь", "Ноябрь", "Декабрь",
]
MONTHS_EN = [
    "January", "February", "March", "April", "May", "June",
    "July", "August", "September", "October", "November", "December",
]

WEEKDAYS_RU = [
    "Понедельник", "Вторник", "Среда", "Четверг",
    "Пятница", "Суббота", "Воскресенье",
]
WEEKDAYS_EN = [
    "Monday", "Tuesday", "Wednesday", "Thursday",
    "Friday", "Saturday", "Sunday",
]
WEEKDAYS_RU_SHORT = ["Пн", "Вт", "Ср", "Чт", "Пт", "Сб", "Вс"]
WEEKDAYS_EN_SHORT = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]


# ============================================================
# ЛОКАЛИЗАЦИЯ
# ============================================================
def _get_language():
    """Возвращает язык интерфейса: 'ru' или 'en'."""
    try:
        from locales import get_language
        return get_language()
    except Exception:
        return 'ru'


def _normalize_locale(value):
    """
    Приводит строку локали к 'ru' | 'eu' | 'us'.

    Принимает: 'ru', 'russia', 'рф', 'eu', 'europe', 'us', 'usa', 'en'.
    """
    if value is None:
        return None

    s = str(value).strip().lower()

    if s in ('ru', 'russia', 'рф', 'rus'):
        return 'ru'
    if s in ('eu', 'europe', 'european', 'de', 'fr', 'it', 'es'):
        return 'eu'
    if s in ('us', 'usa', 'en', 'uk', 'gb'):
        return 'us'

    return None


def _detect_locale():
    """Определяет локаль по языку интерфейса (fallback)."""
    lang = _get_language()
    return 'ru' if lang == 'ru' else 'us'


def _month_name(month, locale):
    """Полное название месяца."""
    if locale == 'ru':
        return MONTHS_RU[month - 1]
    return MONTHS_EN[month - 1]


def _weekday_name(dt, locale):
    """Полное название дня недели."""
    if locale == 'ru':
        return WEEKDAYS_RU[dt.weekday()]
    return WEEKDAYS_EN[dt.weekday()]


def _weekday_name_short(dt, locale):
    """Краткое название дня недели."""
    if locale == 'ru':
        return WEEKDAYS_RU_SHORT[dt.weekday()]
    return WEEKDAYS_EN_SHORT[dt.weekday()]


# ============================================================
# ФОРМАТИРОВАНИЕ ДАТЫ
# ============================================================
def _format_date(dt, fmt, locale):
    """
    Форматирует datetime по шаблону.

    Токены:
        yyyy / YYYY  — 2026
        yy / YY      — 26
        MMMM         — Январь / January
        MMM          — янв / Jan
        MM / mm      — 01
        M / m        — 1
        dd / DD      — 01
        d / D        — 1
        dddd         — Четверг / Thursday
        ddd          — Чт / Thu
    """
    result = []
    i = 0
    n = len(fmt)

    while i < n:
        # dddd
        if fmt[i:i+4].lower() == 'dddd':
            result.append(_weekday_name(dt, locale))
            i += 4
            continue

        # ddd
        if fmt[i:i+3].lower() == 'ddd':
            result.append(_weekday_name_short(dt, locale))
            i += 3
            continue

        # yyyy
        if fmt[i:i+4].lower() == 'yyyy':
            result.append(str(dt.year).zfill(4))
            i += 4
            continue

        # MMMM
        if fmt[i:i+4] == 'MMMM':
            result.append(_month_name(dt.month, locale))
            i += 4
            continue

        # MMM
        if fmt[i:i+3] == 'MMM':
            if locale == 'ru':
                result.append(MONTHS_RU[dt.month - 1][:3].lower())
            else:
                result.append(MONTHS_EN[dt.month - 1][:3])
            i += 3
            continue

        # MM / mm
        if fmt[i:i+2] in ('MM', 'mm'):
            result.append(str(dt.month).zfill(2))
            i += 2
            continue

        # dd / DD
        if fmt[i:i+2] in ('dd', 'DD'):
            result.append(str(dt.day).zfill(2))
            i += 2
            continue

        # yy / YY
        if fmt[i:i+2] in ('yy', 'YY'):
            result.append(str(dt.year)[-2:].zfill(2))
            i += 2
            continue

        # d / D
        if fmt[i] in ('d', 'D'):
            result.append(str(dt.day))
            i += 1
            continue

        # m
        if fmt[i] == 'm':
            result.append(str(dt.month))
            i += 1
            continue

        # M
        if fmt[i] == 'M':
            result.append(str(dt.month))
            i += 1
            continue

        result.append(fmt[i])
        i += 1

    return ''.join(result)


# ============================================================
# ДНИ В МЕСЯЦЕ
# ============================================================
def _days_in_month(year, month):
    if month == 2:
        if year % 4 == 0 and (year % 100 != 0 or year % 400 == 0):
            return 29
        return 28
    return [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31][month - 1]


# ============================================================
# ПРАЗДНИКИ
# ============================================================
HOLIDAYS_RU = {
    (1, 1): "Новый год",
    (1, 2): "Новогодние каникулы",
    (1, 3): "Новогодние каникулы",
    (1, 4): "Новогодние каникулы",
    (1, 5): "Новогодние каникулы",
    (1, 6): "Новогодние каникулы",
    (1, 7): "Рождество Христово",
    (1, 8): "Новогодние каникулы",
    (2, 23): "День защитника Отечества",
    (3, 8): "Международный женский день",
    (5, 1): "Праздник Весны и Труда",
    (5, 9): "День Победы",
    (6, 12): "День России",
    (11, 4): "День народного единства",
}

HOLIDAYS_US = {
    (1, 1): "New Year's Day",
    (7, 4): "Independence Day",
    (12, 25): "Christmas Day",
}

HOLIDAYS_EU = {}   # у EU нет общих праздников


def _holiday_name(month, day, locale):
    if locale == 'ru':
        return HOLIDAYS_RU.get((month, day))
    if locale == 'us':
        return HOLIDAYS_US.get((month, day))
    if locale == 'eu':
        return HOLIDAYS_EU.get((month, day))
    return None


# ============================================================
# CALENDAR NODE
# ============================================================
class CalendarNode(Node):
    def __init__(self, fmt, month, year, locale=None):
        self.fmt = fmt
        self.month = month
        self.year = year
        self.locale = locale

    def _eval_locale(self, env):
        if self.locale is None:
            return _detect_locale()

        val = (self.locale.evaluate(env)
               if hasattr(self.locale, 'evaluate')
               else self.locale)

        loc = _normalize_locale(val)
        if loc is None:
            raise ArrayVatorError(
                code="CALENDAR_BAD_LOCALE",
                context=None,
                message=(
                    f"calendar: локаль должна быть 'ru', 'eu' или 'us', "
                    f"получено '{val}'"
                ),
            )
        return loc

    def evaluate(self, env):
        locale = self._eval_locale(env)

        # 1. Формат
        fmt_val = (self.fmt.evaluate(env)
                   if hasattr(self.fmt, 'evaluate')
                   else self.fmt)
        if not isinstance(fmt_val, str):
            raise ArrayVatorError(
                code="CALENDAR_BAD_FORMAT",
                context=None,
                message=(
                    f"calendar: формат должен быть строкой, "
                    f"получено {type(fmt_val).__name__}"
                ),
            )

        # 2. Год
        year_val = (self.year.evaluate(env)
                    if hasattr(self.year, 'evaluate')
                    else self.year)

        if isinstance(year_val, str):
            y = year_val.strip().lower()
            if y == 'now':
                year_val = datetime.datetime.now().year
            else:
                raise ArrayVatorError(
                    code="CALENDAR_BAD_YEAR",
                    context=None,
                    message=(
                        f"calendar: год должен быть числом, "
                        f"получено '{year_val}'"
                    ),
                )

        if not isinstance(year_val, (int, float)) or isinstance(year_val, bool):
            raise ArrayVatorError(
                code="CALENDAR_BAD_YEAR",
                context=None,
                message=(
                    f"calendar: год должен быть числом, "
                    f"получено {type(year_val).__name__}"
                ),
            )

        year = int(year_val)
        if year < 1900 or year > 2200:
            raise ArrayVatorError(
                code="CALENDAR_BAD_YEAR",
                context=None,
                message=(
                    f"calendar: год вне диапазона 1900–2200, "
                    f"получено {year}"
                ),
            )

        # 3. Месяц
        month_val = (self.month.evaluate(env)
                     if hasattr(self.month, 'evaluate')
                     else self.month)

        if isinstance(month_val, str):
            m = month_val.strip().lower()
            if m == 'all':
                return self._build_all_months(fmt_val, year, locale)
            if m == 'now':
                month_val = datetime.datetime.now().month
            else:
                raise ArrayVatorError(
                    code="CALENDAR_BAD_MONTH",
                    context=None,
                    message=(
                        f"calendar: месяц должен быть числом (1-12) "
                        f"или all, получено '{month_val}'"
                    ),
                )

        if not isinstance(month_val, (int, float)) or isinstance(month_val, bool):
            raise ArrayVatorError(
                code="CALENDAR_BAD_MONTH",
                context=None,
                message=(
                    f"calendar: месяц должен быть числом (1-12) "
                    f"или all, получено {type(month_val).__name__}"
                ),
            )

        month = int(month_val)
        if month < 1 or month > 12:
            raise ArrayVatorError(
                code="CALENDAR_BAD_MONTH",
                context=None,
                message=(
                    f"calendar: месяц должен быть 1-12, "
                    f"получено {month}"
                ),
            )

        return self._build_one_month(fmt_val, year, month, locale)

    def _build_one_month(self, fmt, year, month, locale):
        header = f"{_month_name(month, locale)} {year}"

        days = _days_in_month(year, month)
        col = [header]
        for day in range(1, days + 1):
            dt = datetime.date(year, month, day)
            col.append(_format_date(dt, fmt, locale))

        return MatrExMatrix([[x] for x in col], True)

    def _build_all_months(self, fmt, year, locale):
        columns = []
        max_len = 1

        for month in range(1, 13):
            header = f"{_month_name(month, locale)} {year}"
            col = [header]

            days = _days_in_month(year, month)
            for day in range(1, days + 1):
                dt = datetime.date(year, month, day)
                col.append(_format_date(dt, fmt, locale))

            columns.append(col)
            max_len = max(max_len, len(col))

        for col in columns:
            while len(col) < max_len:
                col.append(None)

        result = []
        for i in range(max_len):
            row = [col[i] if i < len(col) else None for col in columns]
            result.append(row)

        return MatrExMatrix(result, True)

    def __repr__(self):
        return f"Calendar({self.fmt}, {self.month}, {self.year}, {self.locale})"


# ============================================================
# CALENDARPRO NODE
# ============================================================
class CalendarProNode(Node):
    def __init__(self, year, month, locale=None):
        self.year = year
        self.month = month
        self.locale = locale

    def _eval_locale(self, env):
        if self.locale is None:
            return _detect_locale()

        val = (self.locale.evaluate(env)
               if hasattr(self.locale, 'evaluate')
               else self.locale)

        loc = _normalize_locale(val)
        if loc is None:
            raise ArrayVatorError(
                code="CALENDARPRO_BAD_LOCALE",
                context=None,
                message=(
                    f"calendarpro: локаль должна быть 'ru', 'eu' или 'us', "
                    f"получено '{val}'"
                ),
            )
        return loc

    def evaluate(self, env):
        locale = self._eval_locale(env)

        # 1. Год
        year_val = (self.year.evaluate(env)
                    if hasattr(self.year, 'evaluate')
                    else self.year)

        if isinstance(year_val, str):
            y = year_val.strip().lower()
            if y == 'now':
                year_val = datetime.datetime.now().year
            else:
                raise ArrayVatorError(
                    code="CALENDARPRO_BAD_YEAR",
                    context=None,
                    message=(
                        f"calendarpro: год должен быть числом, "
                        f"получено '{year_val}'"
                    ),
                )

        if not isinstance(year_val, (int, float)) or isinstance(year_val, bool):
            raise ArrayVatorError(
                code="CALENDARPRO_BAD_YEAR",
                context=None,
                message=(
                    f"calendarpro: год должен быть числом, "
                    f"получено {type(year_val).__name__}"
                ),
            )

        year = int(year_val)
        if year < 1900 or year > 2200:
            raise ArrayVatorError(
                code="CALENDARPRO_BAD_YEAR",
                context=None,
                message=(
                    f"calendarpro: год вне диапазона 1900–2200, "
                    f"получено {year}"
                ),
            )

        # 2. Месяц
        month_val = (self.month.evaluate(env)
                     if hasattr(self.month, 'evaluate')
                     else self.month)

        if isinstance(month_val, str):
            m = month_val.strip().lower()
            if m == 'all':
                return self._build_all_year(year, locale)
            if m == 'now':
                month_val = datetime.datetime.now().month
            else:
                raise ArrayVatorError(
                    code="CALENDARPRO_BAD_MONTH",
                    context=None,
                    message=(
                        f"calendarpro: месяц должен быть числом (1-12) "
                        f"или all, получено '{month_val}'"
                    ),
                )

        if not isinstance(month_val, (int, float)) or isinstance(month_val, bool):
            raise ArrayVatorError(
                code="CALENDARPRO_BAD_MONTH",
                context=None,
                message=(
                    f"calendarpro: месяц должен быть числом (1-12) "
                    f"или all, получено {type(month_val).__name__}"
                ),
            )

        month = int(month_val)
        if month < 1 or month > 12:
            raise ArrayVatorError(
                code="CALENDARPRO_BAD_MONTH",
                context=None,
                message=(
                    f"calendarpro: месяц должен быть 1-12, "
                    f"получено {month}"
                ),
            )

        return self._build_month(year, month, locale)

    def _header(self, locale):
        if locale == 'ru':
            return ["Дата", "ДеньНедели", "Рабочий", "Праздник", "Сокращённый"]
        return ["Date", "Weekday", "Working", "Holiday", "Short"]

    def _build_row(self, dt, locale):
        date_str = dt.strftime("%d.%m.%Y")
        weekday = _weekday_name_short(dt, locale)

        is_weekend = dt.weekday() >= 5
        holiday = _holiday_name(dt.month, dt.day, locale)
        is_working = (not is_weekend) and (holiday is None)

        is_short = False
        if is_working:
            next_day = dt + datetime.timedelta(days=1)
            next_holiday = _holiday_name(next_day.month, next_day.day, locale)
            if next_holiday is not None:
                is_short = True

        if locale == 'ru':
            yes, no = "да", "нет"
        else:
            yes, no = "yes", "no"

        return [
            date_str,
            weekday,
            yes if is_working else no,
            holiday,
            yes if is_short else no,
        ]

    def _build_month(self, year, month, locale):
        result = [self._header(locale)]

        days = _days_in_month(year, month)
        for day in range(1, days + 1):
            dt = datetime.date(year, month, day)
            result.append(self._build_row(dt, locale))

        return MatrExMatrix(result, True)

    def _build_all_year(self, year, locale):
        result = [self._header(locale)]

        for month in range(1, 13):
            days = _days_in_month(year, month)
            for day in range(1, days + 1):
                dt = datetime.date(year, month, day)
                result.append(self._build_row(dt, locale))

        return MatrExMatrix(result, True)

    def __repr__(self):
        return f"CalendarPro({self.year}, {self.month}, {self.locale})"