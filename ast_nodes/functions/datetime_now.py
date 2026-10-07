# ast_nodes/functions/datetime_now.py
"""
Функции текущей даты и времени:
    datenow([формат])  — текущая дата
    timenow([формат])  — текущее время

СИНТАКСИС:
    datenow()                          # "2024-06-25"
    datenow("DD.MM.YYYY")              # "25.06.2024"
    datenow("YYYY-MM-DD")              # "2024-06-25"
    datenow("DD.MM.YY")                # "25.06.24"
    datenow("DD MMMM YYYY")            # "25 Июнь 2024"
    datenow("DD MMM YYYY")             # "25 Июн 2024"
    datenow("dddd, DD MMMM YYYY")      # "Вторник, 25 Июнь 2024"
    datenow("ddd, DD MMM YYYY")        # "Вт, 25 Июн 2024"

    timenow()                          # "14:30:15"
    timenow("HH:MM")                   # "14:30"
    timenow("HH:MM:SS")                # "14:30:15"
    timenow("hh:MM AM")                # "02:30 PM"

ВОЗВРАЩАЕТ:
    Строку с текущей датой/временем.

ПРАВИЛО ЗАМЕНЫ ТОКЕНОВ (порядок важен!):
    dddd           → полное название дня недели
    ddd            → краткое название дня недели
    AM / PM        → маркер дня
    MMMM           → полное название месяца
    MMM            → краткое название месяца
    YYYY           → год (4 цифры)
    YY             → год (2 цифры)
    HH             → часы (24-часовой)
    hh             → часы (12-часовой)
    SS             → секунды
    MM до HH/hh    → месяц
    MM после HH/hh → минуты
    DD             → день

РУССКИЙ ПЕРЕВОД:
    Названия дней и месяцев подставляются через словари,
    не через locale.setlocale — не влияет на систему.
"""

import datetime
from ..base import Node


# ============================================================
# РУССКИЕ НАЗВАНИЯ
# ============================================================
RU_DAYS_FULL = {
    "Monday": "Понедельник",
    "Tuesday": "Вторник",
    "Wednesday": "Среда",
    "Thursday": "Четверг",
    "Friday": "Пятница",
    "Saturday": "Суббота",
    "Sunday": "Воскресенье",
}

RU_DAYS_SHORT = {
    "Mon": "Пн",
    "Tue": "Вт",
    "Wed": "Ср",
    "Thu": "Чт",
    "Fri": "Пт",
    "Sat": "Сб",
    "Sun": "Вс",
}

RU_MONTHS_FULL = {
    1: "Январь",
    2: "Февраль",
    3: "Март",
    4: "Апрель",
    5: "Май",
    6: "Июнь",
    7: "Июль",
    8: "Август",
    9: "Сентябрь",
    10: "Октябрь",
    11: "Ноябрь",
    12: "Декабрь",
}

RU_MONTHS_SHORT = {
    1: "Янв",
    2: "Фев",
    3: "Мар",
    4: "Апр",
    5: "Май",
    6: "Июн",
    7: "Июл",
    8: "Авг",
    9: "Сен",
    10: "Окт",
    11: "Ноя",
    12: "Дек",
}


# ============================================================
# ФОРМАТИРОВАНИЕ
# ============================================================
def _format_datetime(dt, format_str, kind='date'):
    """
    Форматирует datetime по строке формата ArrayVator.

    kind:
        'date'  — MM = месяц
        'time'  — MM = минуты

    Порядок замены ВАЖЕН:
        1. dddd, ddd (день недели)    — ДО DD
        2. AM / PM
        3. MMMM, MMM (месяц словом)   — ДО MM
        4. YYYY, YY
        5. HH, hh
        6. SS
        7. MM контекстно (месяц или минуты)
        8. DD
    """
    if format_str is None:
        if kind == 'date':
            return dt.strftime("%Y-%m-%d")
        else:
            return dt.strftime("%H:%M:%S")

    if not isinstance(format_str, str):
        raise TypeError(
            f"Формат должен быть строкой, получен {type(format_str)}"
        )

    result = format_str

    # ============================================================
    # 1. ДЕНЬ НЕДЕЛИ — ДО DD!
    # ============================================================
    if "dddd" in result:
        day_en = dt.strftime("%A")     # "Friday"
        day_ru = RU_DAYS_FULL.get(day_en, day_en)
        result = result.replace("dddd", day_ru)

    if "ddd" in result:
        day_en = dt.strftime("%a")     # "Fri"
        day_ru = RU_DAYS_SHORT.get(day_en, day_en)
        result = result.replace("ddd", day_ru)

    # ============================================================
    # 2. AM / PM
    # ============================================================
    ampm = "PM" if dt.hour >= 12 else "AM"
    if "AM" in result:
        result = result.replace("AM", ampm)
    if "PM" in result:
        result = result.replace("PM", ampm)

    # ============================================================
    # 3. НАЗВАНИЯ МЕСЯЦЕВ — ДО MM!
    # ============================================================
    if "MMMM" in result:
        result = result.replace("MMMM", RU_MONTHS_FULL[dt.month])

    if "MMM" in result:
        result = result.replace("MMM", RU_MONTHS_SHORT[dt.month])

    # ============================================================
    # 4. ГОД
    # ============================================================
    result = result.replace("YYYY", str(dt.year).zfill(4))
    result = result.replace("YY", str(dt.year)[-2:].zfill(2))

    # ============================================================
    # 5. ЧАСЫ
    # ============================================================
    # hh — 12-часовой формат
    if "hh" in result:
        hour_12 = dt.hour % 12
        if hour_12 == 0:
            hour_12 = 12
        result = result.replace("hh", str(hour_12).zfill(2))

    # HH — 24-часовой
    result = result.replace("HH", str(dt.hour).zfill(2))

    # ============================================================
    # 6. СЕКУНДЫ
    # ============================================================
    result = result.replace("SS", str(dt.second).zfill(2))

    # ============================================================
    # 7. MM — контекстно (месяц или минуты)
    # ============================================================
    if kind == 'date':
        result = result.replace("MM", str(dt.month).zfill(2))
    else:
        # В time-режиме MM = минуты
        # НО! если есть YYYY — значит это datetime, MM до HH = месяц
        if "YYYY" in format_str or "YY" in format_str:
            result = result.replace("MM", str(dt.month).zfill(2))
        else:
            result = result.replace("MM", str(dt.minute).zfill(2))

    # ============================================================
    # 8. DD — день
    # ============================================================
    result = result.replace("DD", str(dt.day).zfill(2))

    return result


# ============================================================
# DATENOW
# ============================================================
class DateNowNode(Node):
    """Возвращает текущую дату"""

    def __init__(self, format_str=None):
        self.format_str = format_str

    def evaluate(self, env):
        fmt = None
        if self.format_str is not None:
            fmt = (self.format_str.evaluate(env)
                   if hasattr(self.format_str, 'evaluate')
                   else self.format_str)

        now = datetime.datetime.now()
        return _format_datetime(now, fmt, kind='date')

    def __repr__(self):
        if self.format_str is None:
            return "datenow()"
        return f"datenow({self.format_str})"


# ============================================================
# TIMENOW
# ============================================================
class TimeNowNode(Node):
    """Возвращает текущее время"""

    def __init__(self, format_str=None):
        self.format_str = format_str

    def evaluate(self, env):
        fmt = None
        if self.format_str is not None:
            fmt = (self.format_str.evaluate(env)
                   if hasattr(self.format_str, 'evaluate')
                   else self.format_str)

        now = datetime.datetime.now()
        return _format_datetime(now, fmt, kind='time')

    def __repr__(self):
        if self.format_str is None:
            return "timenow()"
        return f"timenow({self.format_str})"