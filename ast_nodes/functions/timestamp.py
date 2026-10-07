# ast_nodes/functions/timestamp.py
"""
Функция TIMESTAMP — текущая дата и время одной строкой.

СИНТАКСИС:
    timestamp()                          # "2026-09-29 14:30:15"
    timestamp("DD.MM.YYYY HH:MM")        # "29.09.2026 14:30"
    timestamp("MM/DD/YYYY hh:MM AM")     # "09/29/2026 02:30 PM"
    timestamp("HH:MM:SS")                # "14:30:15"
    timestamp("DD MMMM YYYY")            # "29 Сентябрь 2026"
    timestamp("DD MMM YYYY")             # "29 Сен 2026"
    timestamp("dddd, DD MMMM YYYY")      # "Вторник, 29 Сентябрь 2026"
    timestamp("ddd, DD MMM YYYY")        # "Вт, 29 Сен 2026"

ПРАВИЛО ЗАМЕНЫ ТОКЕНОВ (порядок важен!):
    dddd           → %A (полное название дня недели)
    ddd            → %a (краткое название дня недели)
    AM / PM        → %p
    MMMM           → %B (полное название месяца)
    MMM            → %b (краткое название месяца)
    YYYY           → %Y
    YY             → %y
    HH             → %H (24-часовой)
    hh             → %I (12-часовой)
    SS             → %S
    MM до HH/hh    → %m (месяц)
    MM после HH/hh → %M (минуты)
    DD             → %d

РУССКИЙ ПЕРЕВОД:
    Названия дней и месяцев подставляются через словари,
    не через locale.setlocale — не влияет на систему.
"""

import datetime
from ..base import Node


DEFAULT_TIMESTAMP_FORMAT = "YYYY-MM-DD HH:MM:SS"


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
    "January": "Январь",
    "February": "Февраль",
    "March": "Март",
    "April": "Апрель",
    "May": "Май",
    "June": "Июнь",
    "July": "Июль",
    "August": "Август",
    "September": "Сентябрь",
    "October": "Октябрь",
    "November": "Ноябрь",
    "December": "Декабрь",
}

RU_MONTHS_SHORT = {
    "Jan": "Янв",
    "Feb": "Фев",
    "Mar": "Мар",
    "Apr": "Апр",
    "May": "Май",
    "Jun": "Июн",
    "Jul": "Июл",
    "Aug": "Авг",
    "Sep": "Сен",
    "Oct": "Окт",
    "Nov": "Ноя",
    "Dec": "Дек",
}


def _translate_to_ru(text):
    """
    Переводит английские названия дней и месяцев на русский.

    Порядок важен: сначала ПОЛНЫЕ названия, потом КРАТКИЕ.
    Иначе "May" может конфликтовать с "Monday"... хотя нет,
    но правило безопасности — полные раньше.
    """
    if not isinstance(text, str):
        return text

    # Полные названия дней
    for en, ru in RU_DAYS_FULL.items():
        text = text.replace(en, ru)

    # Краткие названия дней
    for en, ru in RU_DAYS_SHORT.items():
        text = text.replace(en, ru)

    # Полные названия месяцев
    for en, ru in RU_MONTHS_FULL.items():
        text = text.replace(en, ru)

    # Краткие названия месяцев
    for en, ru in RU_MONTHS_SHORT.items():
        text = text.replace(en, ru)

    return text


# ============================================================
# КОНВЕРТАЦИЯ ФОРМАТА
# ============================================================
def _to_strftime_format(fmt):
    """
    Конвертирует формат ArrayVator в strftime.

    Порядок замены важен:
        1. dddd, ddd (день недели) — ДО DD!
        2. AM/PM
        3. MMMM, MMM (названия месяцев) — ДО MM!
        4. YYYY, YY (год)
        5. HH, hh (часы)
        6. SS (секунды)
        7. MM контекстно (месяц или минуты)
        8. DD (день)
    """
    if not isinstance(fmt, str):
        return "%Y-%m-%d %H:%M:%S"

    result = fmt

    # ============================================================
    # 1. ДЕНЬ НЕДЕЛИ — ДО DD!
    # ============================================================
    result = result.replace("dddd", "%A")   # полное: "Вторник"
    result = result.replace("ddd", "%a")    # краткое: "Вт"

    # ============================================================
    # 2. AM/PM
    # ============================================================
    result = result.replace("AM", "%p").replace("PM", "%p")

    # ============================================================
    # 3. НАЗВАНИЯ МЕСЯЦЕВ — ДО MM!
    # ============================================================
    result = result.replace("MMMM", "%B")   # полное: "Сентябрь"
    result = result.replace("MMM", "%b")    # краткое: "Сен"

    # ============================================================
    # 4. Год (длинные раньше коротких)
    # ============================================================
    result = result.replace("YYYY", "%Y")
    result = result.replace("YY", "%y")

    # ============================================================
    # 5. Часы (длинные раньше коротких)
    # ============================================================
    result = result.replace("HH", "%H")
    result = result.replace("hh", "%I")

    # ============================================================
    # 6. Секунды
    # ============================================================
    result = result.replace("SS", "%S")

    # ============================================================
    # 7. MM — контекстно
    # ============================================================
    hour_pos = -1
    if "%H" in result:
        hour_pos = result.find("%H")
    elif "%I" in result:
        hour_pos = result.find("%I")

    if hour_pos >= 0:
        before = result[:hour_pos].replace("MM", "%m")
        after = result[hour_pos:].replace("MM", "%M")
        result = before + after
    else:
        result = result.replace("MM", "%m")

    # ============================================================
    # 8. День
    # ============================================================
    result = result.replace("DD", "%d")

    return result


# ============================================================
# TIMESTAMP NODE
# ============================================================
class TimestampNode(Node):
    def __init__(self, format_str=None):
        self.format_str = format_str

    def _eval_fmt(self, env):
        if self.format_str is None:
            return DEFAULT_TIMESTAMP_FORMAT

        val = (self.format_str.evaluate(env)
               if hasattr(self.format_str, 'evaluate')
               else self.format_str)

        if not isinstance(val, str):
            raise TypeError(
                f"timestamp: формат должен быть строкой, "
                f"получено {type(val).__name__}"
            )

        if val.strip() == "":
            return DEFAULT_TIMESTAMP_FORMAT

        return val

    def evaluate(self, env):
        fmt = self._eval_fmt(env)
        now = datetime.datetime.now()

        try:
            result = now.strftime(_to_strftime_format(fmt))
        except Exception as e:
            raise ValueError(
                f"timestamp: неверный формат '{fmt}': {e}"
            )

        # Перевод названий дней/месяцев на русский
        result = _translate_to_ru(result)

        return result

    def __repr__(self):
        if self.format_str is None:
            return "timestamp()"
        return f"timestamp({self.format_str})"