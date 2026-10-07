# syntax/autocomplete/items_dates.py
"""
Описания функций работы с датами и временем:
date, DateDiff, datenow, timenow, timestamp,
year, month, day, quarter,
weekday, weekdayname, monthname,
adddays, addmonths, addyears, datetrunc,
hour, minute, second, ampm, is_pm,
addhours, addminutes, addseconds,
timetrunc, time.

ПРАВИЛО ВОЗВРАТА:
    Один столбец   → вектор.
    Несколько столбцов → матрица.
    Скаляр → скаляр.
"""

RU = {
    # ============================================================
    # СТАРЫЕ ДАТЫ
    # ============================================================
    'date': {
        'signature': 'date(данные, "входной", "выходной")',
        'description': (
            'Конвертация формата даты.\n'
            '  • Токены: YYYY, YY, MM, MMMM, MMM, DD, HH, SS, '
            'hh (12-часовой), AM, PM.\n'
            '  • Если не распознано — возвращает как есть.\n'
            '  • Возвращает ВЕКТОР (один столбец).\n'
            '  • Возвращает МАТРИЦУ (несколько столбцов).'
        ),
        'example': (
            'r = date("20.06.2025", "DD.MM.YYYY", "DD MMMM YYYY")\n'
            'r = date("06/20/2025", "MM/DD/YYYY", "DD.MM.YYYY")\n'
            'm[:, "Дата"] = date(m[:, "Дата"], "MM/DD/YYYY", "DD.MM.YYYY")'
        ),
    },
    'DateDiff': {
        'signature': 'DateDiff(дата1, дата2, "формат", "единица")',
        'description': (
            'Разница между датами/временем.\n'
            '  • Единицы: seconds, minutes, hours, days, weeks, months, years.'
        ),
        'example': (
            'r = DateDiff("20.06.2024", "25.06.2024", "DD.MM.YYYY", "days")\n'
            'r = DateDiff("10:30", "14:45", "HH:MM", "minutes")'
        ),
    },
    'datenow': {
        'signature': 'datenow([формат])',
        'description': 'Текущая дата.',
        'example': (
            'r = datenow()                  # "2026-09-29"\n'
            'r = datenow("DD.MM.YYYY")      # "29.09.2026"'
        ),
    },
    'timenow': {
        'signature': 'timenow([формат])',
        'description': 'Текущее время.',
        'example': (
            'r = timenow()                  # "14:30:15"\n'
            'r = timenow("HH:MM")           # "14:30"'
        ),
    },

    # ============================================================
    # ИЗВЛЕЧЕНИЕ ИЗ ДАТЫ
    # ============================================================
    'year': {
        'signature': 'year(данные [, "формат"])',
        'description': (
            'Год из даты.\n'
            '  • Формат по умолчанию: DD.MM.YYYY.\n'
            '  • Если не дата — None.\n'
            '  • Возвращает ВЕКТОР (один столбец).\n'
            '  • Возвращает МАТРИЦУ (несколько столбцов).'
        ),
        'example': (
            'r = year("20.06.2025")             # 2025\n'
            'r = year(m[:, "Дата"])              # вектор\n'
            'm[:, "Год"] = year(m[:, "Дата"])     # присваивание в столбец'
        ),
    },
    'month': {
        'signature': 'month(данные [, "формат"])',
        'description': (
            'Месяц (1-12).\n'
            '  • Возвращает ВЕКТОР (один столбец).'
        ),
        'example': (
            'r = month("20.06.2025")    # 6\n'
            'm[:, "Месяц"] = month(m[:, "Дата"])'
        ),
    },
    'day': {
        'signature': 'day(данные [, "формат"])',
        'description': (
            'День (1-31).\n'
            '  • Возвращает ВЕКТОР (один столбец).'
        ),
        'example': (
            'r = day("20.06.2025")      # 20\n'
            'm[:, "День"] = day(m[:, "Дата"])'
        ),
    },
    'quarter': {
        'signature': 'quarter(данные [, "формат"])',
        'description': (
            'Квартал (1-4).\n'
            '  • Возвращает ВЕКТОР (один столбец).'
        ),
        'example': (
            'r = quarter("20.06.2025")  # 2\n'
            'm[:, "Кв"] = quarter(m[:, "Дата"])'
        ),
    },
    'weekday': {
        'signature': 'weekday(данные [, "формат"])',
        'description': (
            'День недели: 1=Пн, 7=Вс.\n'
            '  • Возвращает ВЕКТОР (один столбец).'
        ),
        'example': (
            'r = weekday("20.06.2025")  # 5\n'
            'm[:, "ДеньНедели"] = weekday(m[:, "Дата"])'
        ),
    },
    'weekdayname': {
        'signature': 'weekdayname(данные [, "формат"])',
        'description': (
            'Название дня недели.\n'
            '  • Возвращает ВЕКТОР (один столбец).'
        ),
        'example': (
            'r = weekdayname("20.06.2025")   # "Пятница"\n'
            'm[:, "ДеньНедели"] = weekdayname(m[:, "Дата"])'
        ),
    },
    'monthname': {
        'signature': 'monthname(данные [, "формат"])',
        'description': (
            'Название месяца.\n'
            '  • Возвращает ВЕКТОР (один столбец).'
        ),
        'example': (
            'r = monthname("20.06.2025")     # "Июнь"\n'
            'm[:, "Месяц"] = monthname(m[:, "Дата"])'
        ),
    },

    # ============================================================
    # АРИФМЕТИКА ДАТ
    # ============================================================
    'adddays': {
        'signature': 'adddays(данные, N [, "формат"])',
        'description': (
            'Прибавить N дней. N может быть отрицательным.\n'
            '  • Возвращает ВЕКТОР (один столбец).'
        ),
        'example': (
            'r = adddays("20.06.2025", 10)    # "30.06.2025"\n'
            'r = adddays("20.06.2025", -5)    # "15.06.2025"\n'
            'm[:, "Дата"] = adddays(m[:, "Дата"], 10)'
        ),
    },
    'addmonths': {
        'signature': 'addmonths(данные, N [, "формат"])',
        'description': (
            'Прибавить N месяцев.\n'
            '  • Возвращает ВЕКТОР (один столбец).'
        ),
        'example': (
            'r = addmonths("20.06.2025", 2)   # "20.08.2025"\n'
            'm[:, "Дата"] = addmonths(m[:, "Дата"], 2)'
        ),
    },
    'addyears': {
        'signature': 'addyears(данные, N [, "формат"])',
        'description': (
            'Прибавить N лет.\n'
            '  • Возвращает ВЕКТОР (один столбец).'
        ),
        'example': (
            'r = addyears("20.06.2025", 1)    # "20.06.2026"\n'
            'm[:, "Дата"] = addyears(m[:, "Дата"], 1)'
        ),
    },

    # ============================================================
    # ОБРЕЗКА ДАТ
    # ============================================================
    'datetrunc': {
        'signature': 'datetrunc(данные, "единица" [, "формат"])',
        'description': (
            'Обрезать до начала периода.\n'
            '  • Единица: "day" | "month" | "quarter" | "year" | '
            '"hour" | "minute" | "second".\n'
            '  • Возвращает ВЕКТОР (один столбец).'
        ),
        'example': (
            'r = datetrunc("20.06.2025", "month")    # "01.06.2025"\n'
            'r = datetrunc("20.06.2025", "year")     # "01.01.2025"\n'
            'm[:, "Месяц"] = datetrunc(m[:, "Дата"], "month")'
        ),
    },

    # ============================================================
    # ИЗВЛЕЧЕНИЕ ИЗ ВРЕМЕНИ
    # ============================================================
    'hour': {
        'signature': 'hour(данные [, "формат"])',
        'description': (
            'Часы из даты/времени (0-23).\n'
            '  • Поддерживает 12-часовой формат (AM/PM).\n'
            '  • Автоопределение: HH:MM:SS, HH:MM, hh:MM AM, ...\n'
            '  • Возвращает ВЕКТОР (один столбец).'
        ),
        'example': (
            'r = hour("14:30:15")                        # 14\n'
            'r = hour("02:30 PM")                        # 14\n'
            'm[:, "Часы"] = hour(m[:, "Время"])'
        ),
    },
    'minute': {
        'signature': 'minute(данные [, "формат"])',
        'description': (
            'Минуты из времени (0-59).\n'
            '  • Возвращает ВЕКТОР (один столбец).'
        ),
        'example': (
            'r = minute("14:30:15")   # 30\n'
            'm[:, "Мин"] = minute(m[:, "Время"])'
        ),
    },
    'second': {
        'signature': 'second(данные [, "формат"])',
        'description': (
            'Секунды из времени (0-59).\n'
            '  • Если во входной строке нет секунд — вернёт 0.\n'
            '  • Возвращает ВЕКТОР (один столбец).'
        ),
        'example': (
            'r = second("14:30:15")   # 15\n'
            'm[:, "Сек"] = second(m[:, "Время"])'
        ),
    },
    'ampm': {
        'signature': 'ampm(данные [, "формат"])',
        'description': (
            'Маркер дня: "AM" / "PM".\n'
            '  • Для 24-часового формата — по часу.\n'
            '  • Возвращает ВЕКТОР (один столбец).'
        ),
        'example': (
            'r = ampm("02:30 PM")   # "PM"\n'
            'r = ampm("09:15 AM")   # "AM"\n'
            'r = ampm("14:30")      # "PM"\n'
            'm[:, "AM_PM"] = ampm(m[:, "Время"])'
        ),
    },
    'is_pm': {
        'signature': 'is_pm(данные [, "формат"])',
        'description': (
            'True, если время после полудня.\n'
            '  • 12:00–23:59 → True (PM).\n'
            '  • 00:00–11:59 → False (AM).\n'
            '  • Возвращает ВЕКТОР (один столбец).'
        ),
        'example': (
            'r = is_pm("02:30 PM")   # True\n'
            'r = is_pm("09:15 AM")   # False\n'
            'm[:, "После_полудня"] = is_pm(m[:, "Время"])'
        ),
    },

    # ============================================================
    # АРИФМЕТИКА ВРЕМЕНИ
    # ============================================================
    'addhours': {
        'signature': 'addhours(данные, N [, "формат"])',
        'description': (
            'Прибавить N часов.\n'
            '  • N может быть отрицательным.\n'
            '  • Работает и с датой+временем.\n'
            '  • Возвращает ВЕКТОР (один столбец).'
        ),
        'example': (
            'r = addhours("14:30:15", 2)              # "16:30:15"\n'
            'r = addhours("20.06.2025 23:00", 2)      # "21.06.2025 01:00"\n'
            'm[:, "Время"] = addhours(m[:, "Время"], 2)'
        ),
    },
    'addminutes': {
        'signature': 'addminutes(данные, N [, "формат"])',
        'description': (
            'Прибавить N минут. N может быть отрицательным.\n'
            '  • Возвращает ВЕКТОР (один столбец).'
        ),
        'example': (
            'r = addminutes("14:30:15", 45)   # "15:15:15"\n'
            'm[:, "Время"] = addminutes(m[:, "Время"], 45)'
        ),
    },
    'addseconds': {
        'signature': 'addseconds(данные, N [, "формат"])',
        'description': (
            'Прибавить N секунд. N может быть отрицательным.\n'
            '  • Возвращает ВЕКТОР (один столбец).'
        ),
        'example': (
            'r = addseconds("14:30:15", 30)   # "14:30:45"\n'
            'm[:, "Время"] = addseconds(m[:, "Время"], 30)'
        ),
    },

    # ============================================================
    # ОБРЕЗКА И КОНВЕРТАЦИЯ ВРЕМЕНИ
    # ============================================================
    'timetrunc': {
        'signature': 'timetrunc(данные, "hour"|"minute"|"second" [, "формат"])',
        'description': (
            'Обрезать время до начала периода.\n'
            '  • "hour"   → "14:00:00"\n'
            '  • "minute" → "14:30:00"\n'
            '  • "second" → "14:30:15"\n'
            '  • Возвращает ВЕКТОР (один столбец).'
        ),
        'example': (
            'r = timetrunc("14:30:15", "hour")     # "14:00:00"\n'
            'r = timetrunc("14:30:15", "minute")   # "14:30:00"\n'
            'm[:, "Время"] = timetrunc(m[:, "Время"], "hour")'
        ),
    },
    'time': {
        'signature': 'time(данные, "входной", "выходной")',
        'description': (
            'Конвертация формата времени.\n'
            '  • Токены: HH (24-часовой), hh (12-часовой), '
            'MM (минуты), SS, AM/PM.\n'
            '  • Если не распознано — возвращает как есть.\n'
            '  • Возвращает ВЕКТОР (один столбец).'
        ),
        'example': (
            'r = time("02:30 PM", "hh:MM AM", "HH:MM")         # "14:30"\n'
            'r = time("14:30", "HH:MM", "hh:MM AM")            # "02:30 PM"\n'
            'm[:, "Время"] = time(m[:, "Время"], "hh:MM AM", "HH:MM")'
        ),
    },

    # ============================================================
    # УТИЛИТЫ
    # ============================================================
    'timestamp': {
        'signature': 'timestamp([формат])',
        'description': (
            'Текущая дата и время одной строкой.\n'
            '  • По умолчанию: "2026-09-29 14:30:15".\n'
            '  • Поддерживает dddd/ddd (день недели), MMMM/MMM (месяц).\n'
            '  • Названия дней и месяцев — на русском.'
        ),
        'example': (
            'r = timestamp()                          # "2026-09-29 14:30:15"\n'
            'r = timestamp("DD.MM.YYYY HH:MM")       # "29.09.2026 14:30"\n'
            'r = timestamp("dddd, DD MMMM YYYY")     # "Вторник, 29 Сентябрь 2026"'
        ),
    },
}


EN = {
    # ============================================================
    # OLD DATES
    # ============================================================
    'date': {
        'signature': 'date(data, "input", "output")',
        'description': (
            'Convert date format.\n'
            '  • Tokens: YYYY, YY, MM, MMMM, MMM, DD, HH, SS, '
            'hh (12-hour), AM, PM.\n'
            '  • If not recognized — returns as is.\n'
            '  • Returns a VECTOR (single column).\n'
            '  • Returns a MATRIX (multiple columns).'
        ),
        'example': (
            'r = date("06/20/2025", "MM/DD/YYYY", "DD.MM.YYYY")\n'
            'r = date("14:30", "HH:MM", "hh:MM AM")   # "02:30 PM"\n'
            'm[:, "Date"] = date(m[:, "Date"], "MM/DD/YYYY", "DD.MM.YYYY")'
        ),
    },
    'DateDiff': {
        'signature': 'DateDiff(date1, date2, "format", "unit")',
        'description': (
            'Difference between dates/times.\n'
            '  • Units: seconds, minutes, hours, days, weeks, months, years.'
        ),
        'example': (
            'r = DateDiff("06/20/2024", "06/25/2024", "MM/DD/YYYY", "days")\n'
            'r = DateDiff("10:30", "14:45", "HH:MM", "minutes")'
        ),
    },
    'datenow': {
        'signature': 'datenow([format])',
        'description': 'Current date.',
        'example': (
            'r = datenow()                  # "2026-09-29"\n'
            'r = datenow("DD.MM.YYYY")      # "29.09.2026"'
        ),
    },
    'timenow': {
        'signature': 'timenow([format])',
        'description': 'Current time.',
        'example': (
            'r = timenow()                  # "14:30:15"\n'
            'r = timenow("HH:MM")           # "14:30"'
        ),
    },

    # ============================================================
    # EXTRACT FROM DATE
    # ============================================================
    'year': {
        'signature': 'year(data [, "format"])',
        'description': (
            'Year from date.\n'
            '  • Default format: DD.MM.YYYY.\n'
            '  • Not a date — None.\n'
            '  • Returns a VECTOR (single column).\n'
            '  • Returns a MATRIX (multiple columns).'
        ),
        'example': (
            'r = year("20.06.2025")             # 2025\n'
            'r = year(m[:, "Date"])              # vector\n'
            'm[:, "Year"] = year(m[:, "Date"])    # assign into column'
        ),
    },
    'month': {
        'signature': 'month(data [, "format"])',
        'description': (
            'Month (1-12).\n'
            '  • Returns a VECTOR (single column).'
        ),
        'example': (
            'r = month("20.06.2025")    # 6\n'
            'm[:, "Month"] = month(m[:, "Date"])'
        ),
    },
    'day': {
        'signature': 'day(data [, "format"])',
        'description': (
            'Day (1-31).\n'
            '  • Returns a VECTOR (single column).'
        ),
        'example': (
            'r = day("20.06.2025")      # 20\n'
            'm[:, "Day"] = day(m[:, "Date"])'
        ),
    },
    'quarter': {
        'signature': 'quarter(data [, "format"])',
        'description': (
            'Quarter (1-4).\n'
            '  • Returns a VECTOR (single column).'
        ),
        'example': (
            'r = quarter("20.06.2025")  # 2\n'
            'm[:, "Q"] = quarter(m[:, "Date"])'
        ),
    },
    'weekday': {
        'signature': 'weekday(data [, "format"])',
        'description': (
            'Weekday: 1=Mon, 7=Sun.\n'
            '  • Returns a VECTOR (single column).'
        ),
        'example': (
            'r = weekday("20.06.2025")  # 5\n'
            'm[:, "Weekday"] = weekday(m[:, "Date"])'
        ),
    },
    'weekdayname': {
        'signature': 'weekdayname(data [, "format"])',
        'description': (
            'Weekday name.\n'
            '  • Returns a VECTOR (single column).'
        ),
        'example': (
            'r = weekdayname("20.06.2025")   # "Пятница"\n'
            'm[:, "Weekday"] = weekdayname(m[:, "Date"])'
        ),
    },
    'monthname': {
        'signature': 'monthname(data [, "format"])',
        'description': (
            'Month name.\n'
            '  • Returns a VECTOR (single column).'
        ),
        'example': (
            'r = monthname("20.06.2025")     # "Июнь"\n'
            'm[:, "Month"] = monthname(m[:, "Date"])'
        ),
    },

    # ============================================================
    # DATE ARITHMETIC
    # ============================================================
    'adddays': {
        'signature': 'adddays(data, N [, "format"])',
        'description': (
            'Add N days. N can be negative.\n'
            '  • Returns a VECTOR (single column).'
        ),
        'example': (
            'r = adddays("20.06.2025", 10)    # "30.06.2025"\n'
            'r = adddays("20.06.2025", -5)    # "15.06.2025"\n'
            'm[:, "Date"] = adddays(m[:, "Date"], 10)'
        ),
    },
    'addmonths': {
        'signature': 'addmonths(data, N [, "format"])',
        'description': (
            'Add N months.\n'
            '  • Returns a VECTOR (single column).'
        ),
        'example': (
            'r = addmonths("20.06.2025", 2)   # "20.08.2025"\n'
            'm[:, "Date"] = addmonths(m[:, "Date"], 2)'
        ),
    },
    'addyears': {
        'signature': 'addyears(data, N [, "format"])',
        'description': (
            'Add N years.\n'
            '  • Returns a VECTOR (single column).'
        ),
        'example': (
            'r = addyears("20.06.2025", 1)    # "20.06.2026"\n'
            'm[:, "Date"] = addyears(m[:, "Date"], 1)'
        ),
    },

    # ============================================================
    # DATE TRUNCATE
    # ============================================================
    'datetrunc': {
        'signature': 'datetrunc(data, "unit" [, "format"])',
        'description': (
            'Truncate to the start of the period.\n'
            '  • Unit: "day" | "month" | "quarter" | "year" | '
            '"hour" | "minute" | "second".\n'
            '  • Returns a VECTOR (single column).'
        ),
        'example': (
            'r = datetrunc("20.06.2025", "month")    # "01.06.2025"\n'
            'r = datetrunc("20.06.2025", "year")     # "01.01.2025"\n'
            'm[:, "Month"] = datetrunc(m[:, "Date"], "month")'
        ),
    },

    # ============================================================
    # EXTRACT FROM TIME
    # ============================================================
    'hour': {
        'signature': 'hour(data [, "format"])',
        'description': (
            'Hour from date/time (0-23).\n'
            '  • Supports 12-hour format (AM/PM).\n'
            '  • Auto-detect: HH:MM:SS, HH:MM, hh:MM AM, ...\n'
            '  • Returns a VECTOR (single column).'
        ),
        'example': (
            'r = hour("14:30:15")                        # 14\n'
            'r = hour("02:30 PM")                        # 14\n'
            'm[:, "Hour"] = hour(m[:, "Time"])'
        ),
    },
    'minute': {
        'signature': 'minute(data [, "format"])',
        'description': (
            'Minute from time (0-59).\n'
            '  • Returns a VECTOR (single column).'
        ),
        'example': (
            'r = minute("14:30:15")   # 30\n'
            'm[:, "Min"] = minute(m[:, "Time"])'
        ),
    },
    'second': {
        'signature': 'second(data [, "format"])',
        'description': (
            'Second from time (0-59).\n'
            '  • If the input has no seconds — returns 0.\n'
            '  • Returns a VECTOR (single column).'
        ),
        'example': (
            'r = second("14:30:15")   # 15\n'
            'm[:, "Sec"] = second(m[:, "Time"])'
        ),
    },
    'ampm': {
        'signature': 'ampm(data [, "format"])',
        'description': (
            'Day marker: "AM" / "PM".\n'
            '  • For 24-hour format — based on the hour.\n'
            '  • Returns a VECTOR (single column).'
        ),
        'example': (
            'r = ampm("02:30 PM")   # "PM"\n'
            'r = ampm("09:15 AM")   # "AM"\n'
            'r = ampm("14:30")      # "PM"\n'
            'm[:, "AM_PM"] = ampm(m[:, "Time"])'
        ),
    },
    'is_pm': {
        'signature': 'is_pm(data [, "format"])',
        'description': (
            'True if the time is after noon.\n'
            '  • 12:00–23:59 → True (PM).\n'
            '  • 00:00–11:59 → False (AM).\n'
            '  • Returns a VECTOR (single column).'
        ),
        'example': (
            'r = is_pm("02:30 PM")   # True\n'
            'r = is_pm("09:15 AM")   # False\n'
            'm[:, "Afternoon"] = is_pm(m[:, "Time"])'
        ),
    },

    # ============================================================
    # TIME ARITHMETIC
    # ============================================================
    'addhours': {
        'signature': 'addhours(data, N [, "format"])',
        'description': (
            'Add N hours.\n'
            '  • N can be negative.\n'
            '  • Works with date+time too.\n'
            '  • Returns a VECTOR (single column).'
        ),
        'example': (
            'r = addhours("14:30:15", 2)              # "16:30:15"\n'
            'r = addhours("20.06.2025 23:00", 2)      # "21.06.2025 01:00"\n'
            'm[:, "Time"] = addhours(m[:, "Time"], 2)'
        ),
    },
    'addminutes': {
        'signature': 'addminutes(data, N [, "format"])',
        'description': (
            'Add N minutes. N can be negative.\n'
            '  • Returns a VECTOR (single column).'
        ),
        'example': (
            'r = addminutes("14:30:15", 45)   # "15:15:15"\n'
            'm[:, "Time"] = addminutes(m[:, "Time"], 45)'
        ),
    },
    'addseconds': {
        'signature': 'addseconds(data, N [, "format"])',
        'description': (
            'Add N seconds. N can be negative.\n'
            '  • Returns a VECTOR (single column).'
        ),
        'example': (
            'r = addseconds("14:30:15", 30)   # "14:30:45"\n'
            'm[:, "Time"] = addseconds(m[:, "Time"], 30)'
        ),
    },

    # ============================================================
    # TIME TRUNCATE AND CONVERT
    # ============================================================
    'timetrunc': {
        'signature': 'timetrunc(data, "hour"|"minute"|"second" [, "format"])',
        'description': (
            'Truncate time to the start of the period.\n'
            '  • "hour"   → "14:00:00"\n'
            '  • "minute" → "14:30:00"\n'
            '  • "second" → "14:30:15"\n'
            '  • Returns a VECTOR (single column).'
        ),
        'example': (
            'r = timetrunc("14:30:15", "hour")     # "14:00:00"\n'
            'r = timetrunc("14:30:15", "minute")   # "14:30:00"\n'
            'm[:, "Time"] = timetrunc(m[:, "Time"], "hour")'
        ),
    },
    'time': {
        'signature': 'time(data, "input", "output")',
        'description': (
            'Convert time format.\n'
            '  • Tokens: HH (24-hour), hh (12-hour), '
            'MM (minutes), SS, AM/PM.\n'
            '  • If not recognized — returns as is.\n'
            '  • Returns a VECTOR (single column).'
        ),
        'example': (
            'r = time("02:30 PM", "hh:MM AM", "HH:MM")         # "14:30"\n'
            'r = time("14:30", "HH:MM", "hh:MM AM")            # "02:30 PM"\n'
            'm[:, "Time"] = time(m[:, "Time"], "hh:MM AM", "HH:MM")'
        ),
    },

    # ============================================================
    # UTILITIES
    # ============================================================
    'timestamp': {
        'signature': 'timestamp([format])',
        'description': (
            'Current date and time in one string.\n'
            '  • Default: "2026-09-29 14:30:15".\n'
            '  • Supports dddd/ddd (weekday), MMMM/MMM (month).\n'
            '  • Day and month names are in Russian.'
        ),
        'example': (
            'r = timestamp()                          # "2026-09-29 14:30:15"\n'
            'r = timestamp("DD.MM.YYYY HH:MM")       # "29.09.2026 14:30"\n'
            'r = timestamp("dddd, DD MMMM YYYY")     # "Вторник, 29 Сентябрь 2026"'
        ),
    },
}