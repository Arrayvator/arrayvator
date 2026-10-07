# syntax/signatures_data/dates.py
"""
Сигнатуры функций работы с датами и временем:
date, DateDiff, datenow, timenow, timestamp,
year, month, day, quarter,
weekday, weekdayname, monthname,
adddays, addmonths, addyears, datetrunc,
hour, minute, second, ampm, is_pm,
addhours, addminutes, addseconds,
timetrunc, time,
is_valid_time.
"""

SIGNATURES = {
    # ============================================================
    # СТАРЫЕ ДАТЫ
    # ============================================================
    'date': {
        'name': 'date',
        'category': 'dates',
        'args': ['данные', '"входной формат"', '"выходной формат"'],
        'examples': [
            'r = date("20.06.2025", "DD.MM.YYYY", "DD MMMM YYYY")',
            'm = date(m[:, "Дата"], "MM/DD/YYYY", "DD.MM.YYYY")',
        ],
    },

    'datediff': {
        'name': 'DateDiff',
        'category': 'dates',
        'args': ['дата1', 'дата2', 'формат', 'единица'],
        'examples': [
            'r = DateDiff("20.06.2024", "25.06.2024", "DD.MM.YYYY", "days")',
            'r = DateDiff(m[:, "Дата1"], m[:, "Дата2"], "DD.MM.YYYY", "days")',
        ],
    },

    'datenow': {
        'name': 'datenow',
        'category': 'dates',
        'args': ['формат (опц.)'],
        'examples': [
            'r = datenow()',
            'r = datenow("DD.MM.YYYY")',
        ],
    },

    'timenow': {
        'name': 'timenow',
        'category': 'dates',
        'args': ['формат (опц.)'],
        'examples': [
            'r = timenow()',
            'r = timenow("HH:MM")',
        ],
    },

    # ============================================================
    # ИЗВЛЕЧЕНИЕ ИЗ ДАТЫ
    # ============================================================
    'year': {
        'name': 'year',
        'category': 'dates',
        'args': ['данные', '"формат" (опц.)'],
        'examples': [
            'r = year("20.06.2025")             # 2025',
            'r = year(m[:, "Дата"])',
            'r = year("2025-06-20", "YYYY-MM-DD")',
        ],
    },

    'month': {
        'name': 'month',
        'category': 'dates',
        'args': ['данные', '"формат" (опц.)'],
        'examples': ['r = month("20.06.2025")    # 6'],
    },

    'day': {
        'name': 'day',
        'category': 'dates',
        'args': ['данные', '"формат" (опц.)'],
        'examples': ['r = day("20.06.2025")      # 20'],
    },

    'quarter': {
        'name': 'quarter',
        'category': 'dates',
        'args': ['данные', '"формат" (опц.)'],
        'examples': ['r = quarter("20.06.2025")  # 2'],
    },

    'weekday': {
        'name': 'weekday',
        'category': 'dates',
        'args': ['данные', '"формат" (опц.)'],
        'examples': ['r = weekday("20.06.2025")  # 5'],
    },

    'weekdayname': {
        'name': 'weekdayname',
        'category': 'dates',
        'args': ['данные', '"формат" (опц.)'],
        'examples': ['r = weekdayname("20.06.2025")   # "Пятница"'],
    },

    'monthname': {
        'name': 'monthname',
        'category': 'dates',
        'args': ['данные', '"формат" (опц.)'],
        'examples': ['r = monthname("20.06.2025")     # "Июнь"'],
    },

    # ============================================================
    # АРИФМЕТИКА ДАТ
    # ============================================================
    'adddays': {
        'name': 'adddays',
        'category': 'dates',
        'args': ['данные', 'N', '"формат" (опц.)'],
        'examples': [
            'r = adddays("20.06.2025", 10)    # "30.06.2025"',
            'r = adddays("20.06.2025", -5)    # "15.06.2025"',
        ],
    },

    'addmonths': {
        'name': 'addmonths',
        'category': 'dates',
        'args': ['данные', 'N', '"формат" (опц.)'],
        'examples': ['r = addmonths("20.06.2025", 2)   # "20.08.2025"'],
    },

    'addyears': {
        'name': 'addyears',
        'category': 'dates',
        'args': ['данные', 'N', '"формат" (опц.)'],
        'examples': ['r = addyears("20.06.2025", 1)    # "20.06.2026"'],
    },

    # ============================================================
    # ОБРЕЗКА ДАТ
    # ============================================================
    'datetrunc': {
        'name': 'datetrunc',
        'category': 'dates',
        'args': [
            'данные',
            '"единица" ("day"|"month"|"quarter"|"year"|"hour"|"minute"|"second")',
            '"формат" (опц.)',
        ],
        'examples': [
            'r = datetrunc("20.06.2025", "month")    # "01.06.2025"',
            'r = datetrunc("20.06.2025", "year")     # "01.01.2025"',
            'r = datetrunc("14:30:15", "hour")       # "14:00:00"',
        ],
    },

    # ============================================================
    # ИЗВЛЕЧЕНИЕ ИЗ ВРЕМЕНИ
    # ============================================================
    'hour': {
        'name': 'hour',
        'category': 'dates',
        'args': ['данные', '"формат" (опц.)'],
        'examples': [
            'r = hour("14:30:15")                    # 14',
            'r = hour("02:30 PM")                    # 14',
            'r = hour("20.06.2025 14:30", "DD.MM.YYYY HH:MM")   # 14',
        ],
    },

    'minute': {
        'name': 'minute',
        'category': 'dates',
        'args': ['данные', '"формат" (опц.)'],
        'examples': [
            'r = minute("14:30:15")   # 30',
            'r = minute("02:30 PM")   # 30',
        ],
    },

    'second': {
        'name': 'second',
        'category': 'dates',
        'args': ['данные', '"формат" (опц.)'],
        'examples': ['r = second("14:30:15")   # 15'],
    },

    'ampm': {
        'name': 'ampm',
        'category': 'dates',
        'args': ['данные', '"формат" (опц.)'],
        'examples': [
            'r = ampm("02:30 PM")   # "PM"',
            'r = ampm("09:15 AM")   # "AM"',
            'r = ampm("14:30")      # "PM"',
        ],
    },

    'is_pm': {
        'name': 'is_pm',
        'category': 'dates',
        'args': ['данные', '"формат" (опц.)'],
        'examples': [
            'r = is_pm("02:30 PM")   # True',
            'r = is_pm("09:15 AM")   # False',
            'r = is_pm("14:30")      # True',
        ],
    },

    # ============================================================
    # АРИФМЕТИКА ВРЕМЕНИ
    # ============================================================
    'addhours': {
        'name': 'addhours',
        'category': 'dates',
        'args': ['данные', 'N', '"формат" (опц.)'],
        'examples': [
            'r = addhours("14:30:15", 2)              # "16:30:15"',
            'r = addhours("20.06.2025 23:00", 2)      # "21.06.2025 01:00"',
            'r = addhours("11:30 PM", 2)              # "01:30 AM"',
        ],
    },

    'addminutes': {
        'name': 'addminutes',
        'category': 'dates',
        'args': ['данные', 'N', '"формат" (опц.)'],
        'examples': ['r = addminutes("14:30:15", 45)   # "15:15:15"'],
    },

    'addseconds': {
        'name': 'addseconds',
        'category': 'dates',
        'args': ['данные', 'N', '"формат" (опц.)'],
        'examples': ['r = addseconds("14:30:15", 30)   # "14:30:45"'],
    },

    # ============================================================
    # ОБРЕЗКА И КОНВЕРТАЦИЯ ВРЕМЕНИ
    # ============================================================
    'timetrunc': {
        'name': 'timetrunc',
        'category': 'dates',
        'args': [
            'данные',
            '"единица" ("hour"|"minute"|"second")',
            '"формат" (опц.)',
        ],
        'examples': [
            'r = timetrunc("14:30:15", "hour")     # "14:00:00"',
            'r = timetrunc("14:30:15", "minute")   # "14:30:00"',
            'r = timetrunc("02:30:15 PM", "hour")  # "02:00:00 PM"',
        ],
    },

    'time': {
        'name': 'time',
        'category': 'dates',
        'args': ['данные', '"входной формат"', '"выходной формат"'],
        'examples': [
            'r = time("02:30 PM", "hh:MM AM", "HH:MM")         # "14:30"',
            'r = time("14:30", "HH:MM", "hh:MM AM")            # "02:30 PM"',
            'r = time("12:30 AM", "hh:MM AM", "HH:MM")         # "00:30"',
            'r = time("14:30:15", "HH:MM:SS", "hh:MM:SS AM")   # "02:30:15 PM"',
        ],
    },

    # ============================================================
    # УТИЛИТЫ
    # ============================================================
    'timestamp': {
        'name': 'timestamp',
        'category': 'dates',
        'args': ['"формат" (опц.)'],
        'examples': [
            'r = timestamp()                          # "2026-09-29 14:30:15"',
            'r = timestamp("DD.MM.YYYY HH:MM")       # "29.09.2026 14:30"',
            'r = timestamp("MM/DD/YYYY hh:MM AM")    # "09/29/2026 02:30 PM"',
            'r = timestamp("dddd, DD MMMM YYYY")     # "Вторник, 29 Сентябрь 2026"',
        ],
    },

    'is_valid_time': {
        'name': 'is_valid_time',
        'category': 'types',
        'args': ['данные', '"формат" (опц.)'],
        'examples': [
            'r = is_valid_time("14:30:15")   # True',
            'r = is_valid_time("14:30")      # True',
            'r = is_valid_time("02:30 PM")   # True',
            'r = is_valid_time("25:99:99")   # False',
            'r = is_valid_time("29.09.2026") # False',
        ],
    },
}