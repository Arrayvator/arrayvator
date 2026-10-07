# errors/functions_db/dates.py
"""
База ошибок для всех функций дат и времени.

ПОКРЫТИЕ:
    Старые даты:      date, DateDiff, datenow, timenow, timestamp
    Календарь:        calendar, calendarpro
    Извлечение даты:  year, month, day, quarter,
                      weekday, weekdayname, monthname
    Арифметика даты:  adddays, addmonths, addyears, datetrunc
    Извлечение времени: hour, minute, second, ampm, is_pm
    Арифметика времени: addhours, addminutes, addseconds
    Обрезка времени:  timetrunc, time
    Проверка времени: is_valid_time

ПРАВИЛА:
    - Формат даты/времени — строка в кавычках.
    - Оба конца диапазона включательны.
    - 12-часовой формат: hh:MM AM/PM.
    - 24-часовой формат: HH:MM:SS.
"""


RU = {
    # ============================================================
    # DATE — конвертация формата
    # ============================================================
    'date': {
        'name': 'date',
        'category': 'dates',
        'signature': 'date(данные, "входной_формат", "выходной_формат")',
        'description': (
            'Конвертирует дату из одного формата в другой.\n'
            '  • Все три аргумента обязательны.\n'
            '  • Если значение не распознано — возвращается как есть.\n'
            '  • Работает со скаляром, вектором, срезом.\n'
            '\n'
            'ТОКЕНЫ:\n'
            '     YYYY  — год (4 цифры)      YY   — год (2 цифры)\n'
            '     MM    — месяц (2 цифры)    M    — месяц (1-2)\n'
            '     MMMM  — месяц словом       MMM  — месяц кратко\n'
            '     DD    — день (2 цифры)     D    — день (1-2)\n'
            '     HH    — часы 24ч           SS   — секунды'
        ),
        'examples': [
            'r = date("20.06.2025", "DD.MM.YYYY", "DD MMMM YYYY")',
            'm = date(m[:, "Дата"], "MM/DD/YYYY", "DD.MM.YYYY")',
            'r = date("2025-06-20", "YYYY-MM-DD", "DD.MM.YYYY")',
        ],
        'errors': {
            'DATE_BAD_SYNTAX': {
                'message': (
                    "date: неверный синтаксис.\n"
                    "  Нужны данные и ОБА формата: входной и выходной."
                ),
                'wrong': 'date("20.06.2025", "DD.MM.YYYY")',
                'right': 'date("20.06.2025", "DD.MM.YYYY", "DD MMMM YYYY")',
                'explanation': (
                    "date ВСЕГДА принимает ТРИ аргумента:\n"
                    "  1. данные — строка или срез\n"
                    "  2. входной формат\n"
                    "  3. выходной формат\n"
                    "\n"
                    "Только с одним форматом невозможно определить,\n"
                    "как распарсить дату и как её вывести."
                ),
                'variants': [
                    'r = date("20.06.2025", "DD.MM.YYYY", "DD MMMM YYYY")',
                    'm = date(m[:, "Дата"], "MM/DD/YYYY", "DD.MM.YYYY")',
                    'r = date("2025-06-20", "YYYY-MM-DD", "DD.MM.YYYY")',
                ],
            },
            'DATE_BAD_FORMAT': {
                'message': (
                    "date: формат должен быть строкой в кавычках.\n"
                    "  Например: \"DD.MM.YYYY\", \"YYYY-MM-DD\"."
                ),
                'wrong': 'date("20.06.2025", DD.MM.YYYY, "YYYY-MM-DD")',
                'right': 'date("20.06.2025", "DD.MM.YYYY", "YYYY-MM-DD")',
                'explanation': (
                    "Формат — это СТРОКА В КАВЫЧКАХ.\n"
                    "\n"
                    "Неправильно:\n"
                    "     date(..., DD.MM.YYYY, ...)\n"
                    "\n"
                    "Правильно:\n"
                    '     date(..., "DD.MM.YYYY", ...)'
                ),
                'variants': [
                    'r = date("20.06.2025", "DD.MM.YYYY", "DD MMMM YYYY")',
                    'r = date("06/20/2025", "MM/DD/YYYY", "DD.MM.YYYY")',
                ],
            },
            'DATE_BAD_DATA': {
                'message': (
                    "date: данные должны быть строкой или срезом.\n"
                    "  Число или другая дата не подходят."
                ),
                'wrong': 'date(42, "DD.MM.YYYY", "YYYY-MM-DD")',
                'right': 'date("20.06.2025", "DD.MM.YYYY", "YYYY-MM-DD")',
                'explanation': (
                    "Первый аргумент — дата в виде строки или срез столбца.\n"
                    "\n"
                    "Неправильно:\n"
                    "     date(42, ...)\n"
                    "     date(m, ...)                — вся матрица\n"
                    "\n"
                    "Правильно:\n"
                    '     date("20.06.2025", ...)\n'
                    '     date(m[:, "Дата"], ...)'
                ),
                'variants': [
                    'r = date("20.06.2025", "DD.MM.YYYY", "DD MMMM YYYY")',
                    'm = date(m[:, "Дата"], "MM/DD/YYYY", "DD.MM.YYYY")',
                ],
            },
        },
    },

    # ============================================================
    # DATEDIFF — разница между датами
    # ============================================================
    'DateDiff': {
        'name': 'DateDiff',
        'category': 'dates',
        'signature': 'DateDiff(дата1, дата2, "формат", "единица")',
        'description': (
            'Разница между двумя датами.\n'
            '  • Единицы: seconds, minutes, hours, days, weeks, months, years.\n'
            '  • Знак: результат = дата2 − дата1.\n'
            '  • Работает со скалярами и векторами.'
        ),
        'examples': [
            'r = DateDiff("20.06.2024", "25.06.2024", "DD.MM.YYYY", "days")',
            'r = DateDiff(m[:, "Д1"], m[:, "Д2"], "DD.MM.YYYY", "days")',
            'r = DateDiff("01.01.2025", "01.01.2026", "DD.MM.YYYY", "years")',
        ],
        'errors': {
            'DATEDIFF_BAD_SYNTAX': {
                'message': (
                    "DateDiff: неверный синтаксис.\n"
                    "  Нужны: дата1, дата2, формат, единица."
                ),
                'wrong': 'DateDiff("20.06.2024", "25.06.2024", "DD.MM.YYYY")',
                'right': (
                    'DateDiff("20.06.2024", "25.06.2024", '
                    '"DD.MM.YYYY", "days")'
                ),
                'explanation': (
                    "DateDiff принимает ЧЕТЫРЕ аргумента:\n"
                    "  1. дата1\n"
                    "  2. дата2\n"
                    "  3. формат (строка)\n"
                    "  4. единица измерения\n"
                    "\n"
                    "Допустимые единицы:\n"
                    "     seconds, minutes, hours,\n"
                    "     days, weeks, months, years"
                ),
                'variants': [
                    'r = DateDiff("20.06.2024", "25.06.2024", "DD.MM.YYYY", "days")',
                    'r = DateDiff(m[:, "Д1"], m[:, "Д2"], "DD.MM.YYYY", "days")',
                ],
            },
            'DATEDIFF_BAD_UNIT': {
                'message': (
                    "DateDiff: неверная единица измерения.\n"
                    "  Допустимо: seconds, minutes, hours, "
                    "days, weeks, months, years."
                ),
                'wrong': 'DateDiff("20.06.2024", "25.06.2024", "DD.MM.YYYY", "d")',
                'right': (
                    'DateDiff("20.06.2024", "25.06.2024", '
                    '"DD.MM.YYYY", "days")'
                ),
                'explanation': (
                    "Единица указывается ЦЕЛИКОМ, без сокращений:\n"
                    "     ✅  \"days\", \"months\", \"years\"\n"
                    "     ❌  \"d\", \"m\", \"y\"\n"
                    "\n"
                    "Полный список: seconds, minutes, hours,\n"
                    "               days, weeks, months, years"
                ),
                'variants': [
                    'r = DateDiff("20.06.2024", "25.06.2024", "DD.MM.YYYY", "days")',
                    'r = DateDiff("20.06.2024", "25.06.2024", "DD.MM.YYYY", "months")',
                ],
            },
        },
    },

    # ============================================================
    # DATENOW — текущая дата
    # ============================================================
    'datenow': {
        'name': 'datenow',
        'category': 'dates',
        'signature': 'datenow([формат])',
        'description': (
            'Текущая дата.\n'
            '  • Без аргумента — "YYYY-MM-DD".\n'
            '  • С аргументом — по указанному формату.'
        ),
        'examples': [
            'r = datenow()',
            'r = datenow("DD.MM.YYYY")',
            'r = datenow("DD MMMM YYYY")',
        ],
        'errors': {
            'DATENOW_BAD_SYNTAX': {
                'message': (
                    "datenow: неверный синтаксис.\n"
                    "  Либо без аргументов, либо один формат."
                ),
                'wrong': 'datenow("DD.MM.YYYY", "YYYY-MM-DD")',
                'right': 'datenow("DD.MM.YYYY")',
                'explanation': (
                    "datenow принимает 0 или 1 аргумент:\n"
                    "     datenow()                    — YYYY-MM-DD\n"
                    '     datenow("DD.MM.YYYY")        — 20.06.2025\n'
                    '     datenow("DD MMMM YYYY")      — 20 Июнь 2025'
                ),
                'variants': [
                    'r = datenow()',
                    'r = datenow("DD.MM.YYYY")',
                    'r = datenow("DD MMMM YYYY")',
                ],
            },
            'DATENOW_BAD_FORMAT': {
                'message': (
                    "datenow: формат должен быть строкой в кавычках."
                ),
                'wrong': 'datenow(DD.MM.YYYY)',
                'right': 'datenow("DD.MM.YYYY")',
                'explanation': (
                    "Формат — строка В КАВЫЧКАХ:\n"
                    '     ✅  datenow("DD.MM.YYYY")\n'
                    "     ❌  datenow(DD.MM.YYYY)"
                ),
                'variants': [
                    'r = datenow()',
                    'r = datenow("DD.MM.YYYY")',
                ],
            },
        },
    },

    # ============================================================
    # TIMENOW — текущее время
    # ============================================================
    'timenow': {
        'name': 'timenow',
        'category': 'dates',
        'signature': 'timenow([формат])',
        'description': (
            'Текущее время.\n'
            '  • Без аргумента — "HH:MM:SS".\n'
            '  • С аргументом — по указанному формату.'
        ),
        'examples': [
            'r = timenow()',
            'r = timenow("HH:MM")',
            'r = timenow("hh:MM AM")',
        ],
        'errors': {
            'TIMENOW_BAD_SYNTAX': {
                'message': (
                    "timenow: неверный синтаксис.\n"
                    "  Либо без аргументов, либо один формат."
                ),
                'wrong': 'timenow("HH:MM", "HH:MM:SS")',
                'right': 'timenow("HH:MM")',
                'explanation': (
                    "timenow принимает 0 или 1 аргумент:\n"
                    "     timenow()                — HH:MM:SS\n"
                    '     timenow("HH:MM")         — HH:MM\n'
                    '     timenow("hh:MM AM")      — 12-часовой'
                ),
                'variants': [
                    'r = timenow()',
                    'r = timenow("HH:MM")',
                    'r = timenow("hh:MM AM")',
                ],
            },
            'TIMENOW_BAD_FORMAT': {
                'message': (
                    "timenow: формат должен быть строкой в кавычках."
                ),
                'wrong': 'timenow(HH:MM)',
                'right': 'timenow("HH:MM")',
                'explanation': (
                    "Формат — строка В КАВЫЧКАХ:\n"
                    '     ✅  timenow("HH:MM")\n'
                    "     ❌  timenow(HH:MM)"
                ),
                'variants': [
                    'r = timenow()',
                    'r = timenow("HH:MM")',
                ],
            },
        },
    },

    # ============================================================
    # TIMESTAMP — дата и время одной строкой
    # ============================================================
    'timestamp': {
        'name': 'timestamp',
        'category': 'dates',
        'signature': 'timestamp([формат])',
        'description': (
            'Текущая дата и время.\n'
            '  • Без аргумента — "YYYY-MM-DD HH:MM:SS".\n'
            '  • С аргументом — по указанному формату.'
        ),
        'examples': [
            'r = timestamp()',
            'r = timestamp("DD.MM.YYYY HH:MM")',
            'r = timestamp("dddd, DD MMMM YYYY")',
        ],
        'errors': {
            'TIMESTAMP_BAD_SYNTAX': {
                'message': (
                    "timestamp: неверный синтаксис.\n"
                    "  Либо без аргументов, либо один формат."
                ),
                'wrong': 'timestamp("DD.MM.YYYY", "HH:MM")',
                'right': 'timestamp("DD.MM.YYYY HH:MM")',
                'explanation': (
                    "timestamp принимает 0 или 1 аргумент.\n"
                    "Дата и время — в ОДНОМ формате:\n"
                    '     timestamp("DD.MM.YYYY HH:MM")'
                ),
                'variants': [
                    'r = timestamp()',
                    'r = timestamp("DD.MM.YYYY HH:MM")',
                ],
            },
        },
    },

    # ============================================================
    # CALENDAR — календарь дат
    # ============================================================
    'calendar': {
        'name': 'calendar',
        'category': 'dates',
        'signature': 'calendar("dd.mm.yyyy", месяц, год [, "ru"|"eu"|"us"])',
        'description': (
            'Календарь дат по шаблону.\n'
            '  • месяц: 1-12 или all (все 12 колонок)\n'
            '  • год: 1981, 2026, datenow()\n'
            '  • локаль: "ru", "eu", "us" (по умолчанию — из интерфейса)'
        ),
        'examples': [
            'v = calendar("dd.mm.yyyy", 1, 2026, "ru")',
            'm = calendar("dd.mm.yyyy", all, 2026, "eu")',
            'v = calendar("yyyy-mm-dd", datenow(), datenow())',
        ],
        'errors': {
            'CALENDAR_BAD_FORMAT': {
                'message': (
                    "calendar: формат должен быть строкой.\n"
                    "  Пример: \"dd.mm.yyyy\", \"yyyy-mm-dd\"."
                ),
                'wrong': 'calendar(dd.mm.yyyy, 1, 2026)',
                'right': 'calendar("dd.mm.yyyy", 1, 2026)',
                'explanation': (
                    "Первый аргумент — формат даты, СТРОКА В КАВЫЧКАХ.\n"
                    "\n"
                    "Правильно:\n"
                    '     calendar("dd.mm.yyyy", 1, 2026)\n'
                    '     calendar("yyyy-mm-dd", all, 2026)\n'
                    '     calendar("dd MMMM yyyy", 5, 2026)'
                ),
                'variants': [
                    'v = calendar("dd.mm.yyyy", 1, 2026)',
                    'm = calendar("yyyy-mm-dd", all, 2026)',
                ],
            },
            'CALENDAR_BAD_YEAR': {
                'message': (
                    "calendar: год должен быть числом (1900–2200)."
                ),
                'wrong': 'calendar("dd.mm.yyyy", 1, "2026")',
                'right': 'calendar("dd.mm.yyyy", 1, 2026)',
                'explanation': (
                    "Год — ЧИСЛО без кавычек или datenow():\n"
                    '     calendar("dd.mm.yyyy", 1, 2026)\n'
                    '     calendar("dd.mm.yyyy", 1, 1981)\n'
                    '     calendar("dd.mm.yyyy", 1, datenow())\n'
                    "\n"
                    "Диапазон: 1900–2200."
                ),
                'variants': [
                    'v = calendar("dd.mm.yyyy", 1, 2026)',
                    'v = calendar("dd.mm.yyyy", 1, 1981)',
                ],
            },
            'CALENDAR_BAD_MONTH': {
                'message': (
                    "calendar: месяц должен быть 1–12 или all."
                ),
                'wrong': 'calendar("dd.mm.yyyy", 13, 2026)',
                'right': 'calendar("dd.mm.yyyy", 1, 2026)',
                'explanation': (
                    "Месяц — ЧИСЛО от 1 до 12 или ключевое слово all:\n"
                    '     calendar("dd.mm.yyyy", 1, 2026)     — январь\n'
                    '     calendar("dd.mm.yyyy", 12, 2026)    — декабрь\n'
                    '     calendar("dd.mm.yyyy", all, 2026)   — 12 колонок\n'
                    "\n"
                    "НЕ:\n"
                    "     calendar(..., 0, ...)   ❌\n"
                    "     calendar(..., 13, ...)  ❌"
                ),
                'variants': [
                    'v = calendar("dd.mm.yyyy", 1, 2026)',
                    'm = calendar("dd.mm.yyyy", all, 2026)',
                ],
            },
            'CALENDAR_BAD_LOCALE': {
                'message': (
                    "calendar: локаль должна быть \"ru\", \"eu\" или \"us\"."
                ),
                'wrong': 'calendar("dd.mm.yyyy", 1, 2026, "russia")',
                'right': 'calendar("dd.mm.yyyy", 1, 2026, "ru")',
                'explanation': (
                    "Только три локали:\n"
                    '     "ru"  — русский    (Понедельник, Январь)\n'
                    '     "eu"  — европейский (Monday, January)\n'
                    '     "us"  — американский (Monday, January, Sun First)\n'
                    "\n"
                    "НЕ:\n"
                    '     "russia"     ❌\n'
                    '     "english"    ❌'
                ),
                'variants': [
                    'v = calendar("dd.mm.yyyy", 1, 2026, "ru")',
                    'v = calendar("dd.mm.yyyy", 1, 2026, "us")',
                ],
            },
        },
    },

    # ============================================================
    # CALENDARPRO — календарь с рабочими днями
    # ============================================================
    'calendarpro': {
        'name': 'calendarpro',
        'category': 'dates',
        'signature': 'calendarpro(год, месяц [, "ru"|"eu"|"us"])',
        'description': (
            'Календарь с информацией о рабочих/праздничных днях.\n'
            '  • месяц: 1-12 или all\n'
            '  • локаль: "ru", "eu", "us"\n'
            '  • Колонки: Дата, ДеньНедели, Рабочий, Праздник, Сокращённый.'
        ),
        'examples': [
            'm = calendarpro(2026, 1)',
            'm = calendarpro(2026, all)',
            'm = calendarpro(datenow(), datenow(), "ru")',
        ],
        'errors': {
            'CALENDARPRO_BAD_YEAR': {
                'message': (
                    "calendarpro: год должен быть числом (1900–2200)."
                ),
                'wrong': 'calendarpro("2026", 1)',
                'right': 'calendarpro(2026, 1)',
                'explanation': (
                    "Год — ЧИСЛО или datenow():\n"
                    "     calendarpro(2026, 1)\n"
                    "     calendarpro(datenow(), datenow())"
                ),
                'variants': [
                    'm = calendarpro(2026, 1)',
                    'm = calendarpro(datenow(), datenow())',
                ],
            },
            'CALENDARPRO_BAD_MONTH': {
                'message': (
                    "calendarpro: месяц должен быть 1–12 или all."
                ),
                'wrong': 'calendarpro(2026, 0)',
                'right': 'calendarpro(2026, 1)',
                'explanation': (
                    "Месяц — ЧИСЛО от 1 до 12 или all:\n"
                    "     calendarpro(2026, 1)\n"
                    "     calendarpro(2026, all)"
                ),
                'variants': [
                    'm = calendarpro(2026, 1)',
                    'm = calendarpro(2026, all)',
                ],
            },
            'CALENDARPRO_BAD_LOCALE': {
                'message': (
                    "calendarpro: локаль — \"ru\", \"eu\" или \"us\"."
                ),
                'wrong': 'calendarpro(2026, 1, "russia")',
                'right': 'calendarpro(2026, 1, "ru")',
                'explanation': (
                    '     "ru"  — русские праздники\n'
                    '     "eu"  — без праздников\n'
                    '     "us"  — американские праздники'
                ),
                'variants': [
                    'm = calendarpro(2026, 1, "ru")',
                    'm = calendarpro(2026, 1, "us")',
                ],
            },
        },
    },

    # ============================================================
    # YEAR / MONTH / DAY / QUARTER
    # ============================================================
    'year': {
        'name': 'year',
        'category': 'dates',
        'signature': 'year(данные [, "формат"])',
        'description': (
            'Извлекает год из даты.\n'
            '  • Без формата — автоопределение.\n'
            '  • Возвращает число.'
        ),
        'examples': [
            'r = year("20.06.2025")',
            'r = year("2025-06-20", "YYYY-MM-DD")',
            'r = year(m[:, "Дата"])',
        ],
        'errors': {
            'YEAR_BAD_SYNTAX': {
                'message': "year: неверный синтаксис.",
                'wrong': 'year()',
                'right': 'year("20.06.2025")',
                'explanation': (
                    "year принимает 1 или 2 аргумента:\n"
                    '     year("20.06.2025")              — автоопределение\n'
                    '     year("2025-06-20", "YYYY-MM-DD")  — явный формат'
                ),
                'variants': [
                    'r = year("20.06.2025")',
                    'r = year("2025-06-20", "YYYY-MM-DD")',
                ],
            },
        },
    },

    'month': {
        'name': 'month',
        'category': 'dates',
        'signature': 'month(данные [, "формат"])',
        'description': (
            'Извлекает номер месяца (1–12).\n'
            '  • Возвращает число.'
        ),
        'examples': [
            'r = month("20.06.2025")',
            'r = month(m[:, "Дата"])',
        ],
        'errors': {
            'MONTH_BAD_SYNTAX': {
                'message': "month: неверный синтаксис.",
                'wrong': 'month()',
                'right': 'month("20.06.2025")',
                'explanation': (
                    "month принимает 1 или 2 аргумента:\n"
                    '     month("20.06.2025")\n'
                    '     month(m[:, "Дата"])'
                ),
                'variants': [
                    'r = month("20.06.2025")',
                    'r = month(m[:, "Дата"])',
                ],
            },
        },
    },

    'day': {
        'name': 'day',
        'category': 'dates',
        'signature': 'day(данные [, "формат"])',
        'description': (
            'Извлекает день месяца (1–31).\n'
            '  • Возвращает число.'
        ),
        'examples': [
            'r = day("20.06.2025")',
            'r = day(m[:, "Дата"])',
        ],
        'errors': {
            'DAY_BAD_SYNTAX': {
                'message': "day: неверный синтаксис.",
                'wrong': 'day()',
                'right': 'day("20.06.2025")',
                'explanation': (
                    "day принимает 1 или 2 аргумента:\n"
                    '     day("20.06.2025")\n'
                    '     day(m[:, "Дата"])'
                ),
                'variants': [
                    'r = day("20.06.2025")',
                    'r = day(m[:, "Дата"])',
                ],
            },
        },
    },

    'quarter': {
        'name': 'quarter',
        'category': 'dates',
        'signature': 'quarter(данные [, "формат"])',
        'description': (
            'Извлекает номер квартала (1–4).\n'
            '  • Возвращает число.'
        ),
        'examples': [
            'r = quarter("20.06.2025")   # 2',
            'r = quarter(m[:, "Дата"])',
        ],
        'errors': {
            'QUARTER_BAD_SYNTAX': {
                'message': "quarter: неверный синтаксис.",
                'wrong': 'quarter()',
                'right': 'quarter("20.06.2025")',
                'explanation': (
                    "quarter принимает 1 или 2 аргумента.\n"
                    "Возвращает 1–4."
                ),
                'variants': [
                    'r = quarter("20.06.2025")',
                    'r = quarter(m[:, "Дата"])',
                ],
            },
        },
    },

    # ============================================================
    # WEEKDAY / WEEKDAYNAME / MONTHNAME
    # ============================================================
    'weekday': {
        'name': 'weekday',
        'category': 'dates',
        'signature': 'weekday(данные [, "формат"])',
        'description': (
            'День недели числом (1–7).\n'
            '  • 1 = Понедельник, 7 = Воскресенье.'
        ),
        'examples': [
            'r = weekday("20.06.2025")   # 5',
            'r = weekday(m[:, "Дата"])',
        ],
        'errors': {
            'WEEKDAY_BAD_SYNTAX': {
                'message': "weekday: неверный синтаксис.",
                'wrong': 'weekday()',
                'right': 'weekday("20.06.2025")',
                'explanation': (
                    "weekday принимает 1 или 2 аргумента.\n"
                    "Возвращает 1–7 (1 = Понедельник)."
                ),
                'variants': [
                    'r = weekday("20.06.2025")',
                    'r = weekday(m[:, "Дата"])',
                ],
            },
        },
    },

    'weekdayname': {
        'name': 'weekdayname',
        'category': 'dates',
        'signature': 'weekdayname(данные [, "формат"])',
        'description': (
            'Название дня недели строкой.\n'
            '  • "Понедельник", "Вторник", ...'
        ),
        'examples': [
            'r = weekdayname("20.06.2025")   # "Пятница"',
        ],
        'errors': {
            'WEEKDAYNAME_BAD_SYNTAX': {
                'message': "weekdayname: неверный синтаксис.",
                'wrong': 'weekdayname()',
                'right': 'weekdayname("20.06.2025")',
                'explanation': (
                    "weekdayname принимает 1 или 2 аргумента.\n"
                    "Возвращает название дня недели."
                ),
                'variants': [
                    'r = weekdayname("20.06.2025")',
                ],
            },
        },
    },

    'monthname': {
        'name': 'monthname',
        'category': 'dates',
        'signature': 'monthname(данные [, "формат"])',
        'description': (
            'Название месяца строкой.\n'
            '  • "Январь", "Февраль", ...'
        ),
        'examples': [
            'r = monthname("20.06.2025")   # "Июнь"',
        ],
        'errors': {
            'MONTHNAME_BAD_SYNTAX': {
                'message': "monthname: неверный синтаксис.",
                'wrong': 'monthname()',
                'right': 'monthname("20.06.2025")',
                'explanation': (
                    "monthname принимает 1 или 2 аргумента.\n"
                    "Возвращает название месяца."
                ),
                'variants': [
                    'r = monthname("20.06.2025")',
                ],
            },
        },
    },

    # ============================================================
    # ADDDAYS / ADDMONTHS / ADDYEARS
    # ============================================================
    'adddays': {
        'name': 'adddays',
        'category': 'dates',
        'signature': 'adddays(данные, N [, "формат"])',
        'description': (
            'Прибавляет N дней к дате.\n'
            '  • N может быть отрицательным.\n'
            '  • Без формата — результат в формате входной строки.'
        ),
        'examples': [
            'r = adddays("20.06.2025", 10)    # "30.06.2025"',
            'r = adddays("20.06.2025", -5)    # "15.06.2025"',
            'r = adddays(m[:, "Дата"], 30)',
        ],
        'errors': {
            'ADDDAYS_BAD_SYNTAX': {
                'message': (
                    "adddays: неверный синтаксис.\n"
                    "  Нужны данные и N — число дней."
                ),
                'wrong': 'adddays("20.06.2025")',
                'right': 'adddays("20.06.2025", 10)',
                'explanation': (
                    "adddays принимает 2 или 3 аргумента:\n"
                    "  1. данные\n"
                    "  2. N — число дней (может быть отрицательным)\n"
                    "  3. формат (опционально)"
                ),
                'variants': [
                    'r = adddays("20.06.2025", 10)',
                    'r = adddays("20.06.2025", -5)',
                    'r = adddays(m[:, "Дата"], 30, "DD.MM.YYYY")',
                ],
            },
            'ADDDAYS_BAD_N': {
                'message': "adddays: N должно быть числом.",
                'wrong': 'adddays("20.06.2025", "10")',
                'right': 'adddays("20.06.2025", 10)',
                'explanation': (
                    "N — ЧИСЛО без кавычек.\n"
                    "Может быть отрицательным."
                ),
                'variants': [
                    'r = adddays("20.06.2025", 10)',
                    'r = adddays("20.06.2025", -5)',
                ],
            },
        },
    },

    'addmonths': {
        'name': 'addmonths',
        'category': 'dates',
        'signature': 'addmonths(данные, N [, "формат"])',
        'description': 'Прибавляет N месяцев к дате.',
        'examples': [
            'r = addmonths("20.06.2025", 2)   # "20.08.2025"',
        ],
        'errors': {
            'ADDMONTHS_BAD_SYNTAX': {
                'message': (
                    "addmonths: неверный синтаксис.\n"
                    "  Нужны данные и N — число месяцев."
                ),
                'wrong': 'addmonths("20.06.2025")',
                'right': 'addmonths("20.06.2025", 2)',
                'explanation': (
                    "addmonths(данные, N [, \"формат\"])\n"
                    "N может быть отрицательным."
                ),
                'variants': [
                    'r = addmonths("20.06.2025", 2)',
                    'r = addmonths(m[:, "Дата"], -3)',
                ],
            },
        },
    },

    'addyears': {
        'name': 'addyears',
        'category': 'dates',
        'signature': 'addyears(данные, N [, "формат"])',
        'description': 'Прибавляет N лет к дате.',
        'examples': [
            'r = addyears("20.06.2025", 1)   # "20.06.2026"',
        ],
        'errors': {
            'ADDYEARS_BAD_SYNTAX': {
                'message': (
                    "addyears: неверный синтаксис.\n"
                    "  Нужны данные и N — число лет."
                ),
                'wrong': 'addyears("20.06.2025")',
                'right': 'addyears("20.06.2025", 1)',
                'explanation': (
                    "addyears(данные, N [, \"формат\"])\n"
                    "N может быть отрицательным."
                ),
                'variants': [
                    'r = addyears("20.06.2025", 1)',
                    'r = addyears(m[:, "Дата"], -2)',
                ],
            },
        },
    },

    # ============================================================
    # DATETRUNC
    # ============================================================
    'datetrunc': {
        'name': 'datetrunc',
        'category': 'dates',
        'signature': 'datetrunc(данные, "единица" [, "формат"])',
        'description': (
            'Обрезает дату/время до указанной единицы.\n'
            '  • Единицы: "day", "month", "quarter", "year",\n'
            '             "hour", "minute", "second".'
        ),
        'examples': [
            'r = datetrunc("20.06.2025", "month")    # "01.06.2025"',
            'r = datetrunc("20.06.2025", "year")     # "01.01.2025"',
            'r = datetrunc("14:30:15", "hour")       # "14:00:00"',
        ],
        'errors': {
            'DATETRUNC_BAD_UNIT': {
                'message': (
                    "datetrunc: неверная единица.\n"
                    "  Допустимо: day, month, quarter, year, "
                    "hour, minute, second."
                ),
                'wrong': 'datetrunc("20.06.2025", "m")',
                'right': 'datetrunc("20.06.2025", "month")',
                'explanation': (
                    "Единица указывается ЦЕЛИКОМ, без сокращений:\n"
                    '     "day"       — день\n'
                    '     "month"     — месяц\n'
                    '     "quarter"   — квартал\n'
                    '     "year"      — год\n'
                    '     "hour"      — час\n'
                    '     "minute"    — минута\n'
                    '     "second"    — секунда\n'
                    "\n"
                    "НЕ:\n"
                    '     "d", "m", "y"  ❌'
                ),
                'variants': [
                    'r = datetrunc("20.06.2025", "day")',
                    'r = datetrunc("20.06.2025", "month")',
                    'r = datetrunc("20.06.2025", "quarter")',
                    'r = datetrunc("20.06.2025", "year")',
                    'r = datetrunc("14:30:15", "hour")',
                ],
            },
            'DATETRUNC_BAD_SYNTAX': {
                'message': (
                    "datetrunc: неверный синтаксис.\n"
                    "  Нужны данные и единица обрезки."
                ),
                'wrong': 'datetrunc("20.06.2025")',
                'right': 'datetrunc("20.06.2025", "month")',
                'explanation': (
                    "datetrunc(данные, \"единица\" [, \"формат\"])\n"
                    "\n"
                    "Единица обязательна."
                ),
                'variants': [
                    'r = datetrunc("20.06.2025", "month")',
                    'r = datetrunc(m[:, "Дата"], "year")',
                ],
            },
        },
    },

    # ============================================================
    # HOUR / MINUTE / SECOND / AMPM / IS_PM
    # ============================================================
    'hour': {
        'name': 'hour',
        'category': 'dates',
        'signature': 'hour(данные [, "формат"])',
        'description': (
            'Извлекает часы (0–23).\n'
            '  • Работает и с 24-часовым, и с 12-часовым форматом.'
        ),
        'examples': [
            'r = hour("14:30:15")              # 14',
            'r = hour("02:30 PM")              # 14',
            'r = hour(m[:, "Время"], "HH:MM")',
        ],
        'errors': {
            'HOUR_BAD_SYNTAX': {
                'message': "hour: неверный синтаксис.",
                'wrong': 'hour()',
                'right': 'hour("14:30:15")',
                'explanation': (
                    "hour(данные [, \"формат\"])\n"
                    "     hour(\"14:30:15\")\n"
                    "     hour(\"02:30 PM\")\n"
                    "     hour(m[:, \"Время\"], \"HH:MM\")"
                ),
                'variants': [
                    'r = hour("14:30:15")',
                    'r = hour("02:30 PM")',
                ],
            },
        },
    },

    'minute': {
        'name': 'minute',
        'category': 'dates',
        'signature': 'minute(данные [, "формат"])',
        'description': 'Извлекает минуты (0–59).',
        'examples': [
            'r = minute("14:30:15")   # 30',
        ],
        'errors': {
            'MINUTE_BAD_SYNTAX': {
                'message': "minute: неверный синтаксис.",
                'wrong': 'minute()',
                'right': 'minute("14:30:15")',
                'explanation': (
                    "minute(данные [, \"формат\"])\n"
                    "     minute(\"14:30:15\")   # 30"
                ),
                'variants': [
                    'r = minute("14:30:15")',
                    'r = minute(m[:, "Время"])',
                ],
            },
        },
    },

    'second': {
        'name': 'second',
        'category': 'dates',
        'signature': 'second(данные [, "формат"])',
        'description': 'Извлекает секунды (0–59).',
        'examples': [
            'r = second("14:30:15")   # 15',
        ],
        'errors': {
            'SECOND_BAD_SYNTAX': {
                'message': "second: неверный синтаксис.",
                'wrong': 'second()',
                'right': 'second("14:30:15")',
                'explanation': (
                    "second(данные [, \"формат\"])\n"
                    "     second(\"14:30:15\")   # 15"
                ),
                'variants': [
                    'r = second("14:30:15")',
                ],
            },
        },
    },

    'ampm': {
        'name': 'ampm',
        'category': 'dates',
        'signature': 'ampm(данные [, "формат"])',
        'description': (
            'Определяет AM или PM.\n'
            '  • Возвращает "AM" или "PM".'
        ),
        'examples': [
            'r = ampm("02:30 PM")   # "PM"',
            'r = ampm("09:15 AM")   # "AM"',
            'r = ampm("14:30")      # "PM"',
        ],
        'errors': {
            'AMPM_BAD_SYNTAX': {
                'message': "ampm: неверный синтаксис.",
                'wrong': 'ampm()',
                'right': 'ampm("02:30 PM")',
                'explanation': (
                    "ampm(данные [, \"формат\"])\n"
                    "Возвращает \"AM\" или \"PM\"."
                ),
                'variants': [
                    'r = ampm("02:30 PM")',
                    'r = ampm("14:30")',
                ],
            },
        },
    },

    'is_pm': {
        'name': 'is_pm',
        'category': 'dates',
        'signature': 'is_pm(данные [, "формат"])',
        'description': (
            'Проверяет: время после полудня?\n'
            '  • True / False.'
        ),
        'examples': [
            'r = is_pm("02:30 PM")   # True',
            'r = is_pm("09:15 AM")   # False',
            'r = is_pm("14:30")      # True',
        ],
        'errors': {
            'IS_PM_BAD_SYNTAX': {
                'message': "is_pm: неверный синтаксис.",
                'wrong': 'is_pm()',
                'right': 'is_pm("14:30")',
                'explanation': (
                    "is_pm(данные [, \"формат\"])\n"
                    "Возвращает True / False."
                ),
                'variants': [
                    'r = is_pm("02:30 PM")',
                    'r = is_pm("14:30")',
                ],
            },
        },
    },

    # ============================================================
    # ADDHOURS / ADDMINUTES / ADDSECONDS
    # ============================================================
    'addhours': {
        'name': 'addhours',
        'category': 'dates',
        'signature': 'addhours(данные, N [, "формат"])',
        'description': (
            'Прибавляет N часов.\n'
            '  • Корректно переносит через сутки.'
        ),
        'examples': [
            'r = addhours("14:30:15", 2)              # "16:30:15"',
            'r = addhours("20.06.2025 23:00", 2)      # "21.06.2025 01:00"',
        ],
        'errors': {
            'ADDHOURS_BAD_SYNTAX': {
                'message': (
                    "addhours: неверный синтаксис.\n"
                    "  Нужны данные и N — число часов."
                ),
                'wrong': 'addhours("14:30:15")',
                'right': 'addhours("14:30:15", 2)',
                'explanation': (
                    "addhours(данные, N [, \"формат\"])\n"
                    "N может быть отрицательным."
                ),
                'variants': [
                    'r = addhours("14:30:15", 2)',
                    'r = addhours("14:30:15", -1)',
                ],
            },
        },
    },

    'addminutes': {
        'name': 'addminutes',
        'category': 'dates',
        'signature': 'addminutes(данные, N [, "формат"])',
        'description': 'Прибавляет N минут.',
        'examples': [
            'r = addminutes("14:30:15", 45)   # "15:15:15"',
        ],
        'errors': {
            'ADDMINUTES_BAD_SYNTAX': {
                'message': (
                    "addminutes: неверный синтаксис.\n"
                    "  Нужны данные и N — число минут."
                ),
                'wrong': 'addminutes("14:30:15")',
                'right': 'addminutes("14:30:15", 45)',
                'explanation': (
                    "addminutes(данные, N [, \"формат\"])"
                ),
                'variants': [
                    'r = addminutes("14:30:15", 45)',
                ],
            },
        },
    },

    'addseconds': {
        'name': 'addseconds',
        'category': 'dates',
        'signature': 'addseconds(данные, N [, "формат"])',
        'description': 'Прибавляет N секунд.',
        'examples': [
            'r = addseconds("14:30:15", 30)   # "14:30:45"',
        ],
        'errors': {
            'ADDSECONDS_BAD_SYNTAX': {
                'message': (
                    "addseconds: неверный синтаксис.\n"
                    "  Нужны данные и N — число секунд."
                ),
                'wrong': 'addseconds("14:30:15")',
                'right': 'addseconds("14:30:15", 30)',
                'explanation': (
                    "addseconds(данные, N [, \"формат\"])"
                ),
                'variants': [
                    'r = addseconds("14:30:15", 30)',
                ],
            },
        },
    },

    # ============================================================
    # TIMETRUNC
    # ============================================================
    'timetrunc': {
        'name': 'timetrunc',
        'category': 'dates',
        'signature': 'timetrunc(данные, "единица" [, "формат"])',
        'description': (
            'Обрезает время до указанной единицы.\n'
            '  • Единицы: "hour", "minute", "second".'
        ),
        'examples': [
            'r = timetrunc("14:30:15", "hour")     # "14:00:00"',
            'r = timetrunc("14:30:15", "minute")   # "14:30:00"',
        ],
        'errors': {
            'TIMETRUNC_BAD_UNIT': {
                'message': (
                    "timetrunc: неверная единица.\n"
                    "  Допустимо: hour, minute, second."
                ),
                'wrong': 'timetrunc("14:30:15", "h")',
                'right': 'timetrunc("14:30:15", "hour")',
                'explanation': (
                    "Единица указывается ЦЕЛИКОМ:\n"
                    '     "hour"     — "14:00:00"\n'
                    '     "minute"   — "14:30:00"\n'
                    '     "second"   — "14:30:15"\n'
                    "\n"
                    "НЕ:\n"
                    '     "h", "m", "s"  ❌\n'
                    '     "day"          ❌ (для дат — datetrunc)'
                ),
                'variants': [
                    'r = timetrunc("14:30:15", "hour")',
                    'r = timetrunc("14:30:15", "minute")',
                    'r = timetrunc("14:30:15", "second")',
                ],
            },
            'TIMETRUNC_BAD_SYNTAX': {
                'message': (
                    "timetrunc: неверный синтаксис.\n"
                    "  Нужны данные и единица обрезки."
                ),
                'wrong': 'timetrunc("14:30:15")',
                'right': 'timetrunc("14:30:15", "hour")',
                'explanation': (
                    "timetrunc(данные, \"единица\" [, \"формат\"])\n"
                    "\n"
                    "Единица обязательна."
                ),
                'variants': [
                    'r = timetrunc("14:30:15", "hour")',
                ],
            },
        },
    },

    # ============================================================
    # TIME — конвертер форматов
    # ============================================================
    'time': {
        'name': 'time',
        'category': 'dates',
        'signature': 'time(данные, "входной_формат", "выходной_формат")',
        'description': (
            'Конвертирует время из одного формата в другой.\n'
            '  • Все три аргумента обязательны.'
        ),
        'examples': [
            'r = time("02:30 PM", "hh:MM AM", "HH:MM")      # "14:30"',
            'r = time("14:30", "HH:MM", "hh:MM AM")         # "02:30 PM"',
        ],
        'errors': {
            'TIME_BAD_SYNTAX': {
                'message': (
                    "time: неверный синтаксис.\n"
                    "  Нужны данные и ОБА формата."
                ),
                'wrong': 'time("02:30 PM", "hh:MM AM")',
                'right': 'time("02:30 PM", "hh:MM AM", "HH:MM")',
                'explanation': (
                    "time ВСЕГДА принимает ТРИ аргумента:\n"
                    "  1. данные — строка или срез\n"
                    "  2. входной формат\n"
                    "  3. выходной формат"
                ),
                'variants': [
                    'r = time("02:30 PM", "hh:MM AM", "HH:MM")',
                    'r = time("14:30", "HH:MM", "hh:MM AM")',
                    'r = time("14:30:15", "HH:MM:SS", "hh:MM:SS AM")',
                ],
            },
        },
    },

    # ============================================================
    # IS_VALID_TIME
    # ============================================================
    'is_valid_time': {
        'name': 'is_valid_time',
        'category': 'types',
        'signature': 'is_valid_time(данные [, "формат"])',
        'description': (
            'Проверяет, что строка — корректное время.\n'
            '  • Поддерживает 24-часовой и 12-часовой (AM/PM).\n'
            '  • None / не-строка / пустая строка → False.\n'
            '  • Даты возвращают False (это не время).'
        ),
        'examples': [
            'r = is_valid_time("14:30:15")   # True',
            'r = is_valid_time("25:99:99")   # False',
            'r = is_valid_time("29.09.2026") # False',
            'r = is_valid_time(m[:, "Время"], "HH:MM:SS")',
        ],
        'errors': {
            'VALID_TIME_BAD_SYNTAX': {
                'message': (
                    "is_valid_time: неверный синтаксис.\n"
                    "  Нужны данные и, опционально, формат."
                ),
                'wrong': 'is_valid_time()',
                'right': 'is_valid_time("14:30:15")',
                'explanation': (
                    "is_valid_time(данные [, \"формат\"])\n"
                    "\n"
                    "     is_valid_time(\"14:30:15\")              — авто\n"
                    "     is_valid_time(m[:, \"Время\"], \"HH:MM:SS\")"
                ),
                'variants': [
                    'r = is_valid_time("14:30:15")',
                    'r = is_valid_time(m[:, "Время"], "HH:MM:SS")',
                ],
            },
        },
    },
}


EN = {
    # ============================================================
    # DATE — format conversion
    # ============================================================
    'date': {
        'name': 'date',
        'category': 'dates',
        'signature': 'date(data, "input_format", "output_format")',
        'description': (
            'Convert a date from one format to another.\n'
            '  • All three arguments are required.\n'
            '  • If the value is not recognized — returned as is.\n'
            '  • Works with scalar, vector, slice.\n'
            '\n'
            'TOKENS:\n'
            '     YYYY  — year (4 digits)   YY   — year (2 digits)\n'
            '     MM    — month (2 digits)  M    — month (1-2)\n'
            '     MMMM  — full month name   MMM  — short month name\n'
            '     DD    — day (2 digits)    D    — day (1-2)\n'
            '     HH    — hours (24h)       SS   — seconds'
        ),
        'examples': [
            'r = date("20.06.2025", "DD.MM.YYYY", "DD MMMM YYYY")',
            'm = date(m[:, "Date"], "MM/DD/YYYY", "DD.MM.YYYY")',
            'r = date("2025-06-20", "YYYY-MM-DD", "DD.MM.YYYY")',
        ],
        'errors': {
            'DATE_BAD_SYNTAX': {
                'message': (
                    "date: invalid syntax.\n"
                    "  Need data and BOTH formats: input and output."
                ),
                'wrong': 'date("20.06.2025", "DD.MM.YYYY")',
                'right': 'date("20.06.2025", "DD.MM.YYYY", "DD MMMM YYYY")',
                'explanation': (
                    "date ALWAYS takes THREE arguments:\n"
                    "  1. data — string or slice\n"
                    "  2. input format\n"
                    "  3. output format\n"
                    "\n"
                    "With only one format it's impossible to know\n"
                    "how to parse and how to output the date."
                ),
                'variants': [
                    'r = date("20.06.2025", "DD.MM.YYYY", "DD MMMM YYYY")',
                    'm = date(m[:, "Date"], "MM/DD/YYYY", "DD.MM.YYYY")',
                ],
            },
            'DATE_BAD_FORMAT': {
                'message': (
                    "date: format must be a quoted string.\n"
                    "  Example: \"DD.MM.YYYY\", \"YYYY-MM-DD\"."
                ),
                'wrong': 'date("20.06.2025", DD.MM.YYYY, "YYYY-MM-DD")',
                'right': 'date("20.06.2025", "DD.MM.YYYY", "YYYY-MM-DD")',
                'explanation': (
                    "Format is a STRING IN QUOTES.\n"
                    "\n"
                    "Incorrect:\n"
                    "     date(..., DD.MM.YYYY, ...)\n"
                    "\n"
                    "Correct:\n"
                    '     date(..., "DD.MM.YYYY", ...)'
                ),
                'variants': [
                    'r = date("20.06.2025", "DD.MM.YYYY", "DD MMMM YYYY")',
                ],
            },
            'DATE_BAD_DATA': {
                'message': (
                    "date: data must be a string or a slice.\n"
                    "  A number or another date is not accepted."
                ),
                'wrong': 'date(42, "DD.MM.YYYY", "YYYY-MM-DD")',
                'right': 'date("20.06.2025", "DD.MM.YYYY", "YYYY-MM-DD")',
                'explanation': (
                    "First argument — a date as a string or a column slice.\n"
                    "\n"
                    "Incorrect:\n"
                    "     date(42, ...)\n"
                    "     date(m, ...)                — whole matrix\n"
                    "\n"
                    "Correct:\n"
                    '     date("20.06.2025", ...)\n'
                    '     date(m[:, "Date"], ...)'
                ),
                'variants': [
                    'r = date("20.06.2025", "DD.MM.YYYY", "DD MMMM YYYY")',
                ],
            },
        },
    },

    # ============================================================
    # DATEDIFF
    # ============================================================
    'DateDiff': {
        'name': 'DateDiff',
        'category': 'dates',
        'signature': 'DateDiff(date1, date2, "format", "unit")',
        'description': (
            'Difference between two dates.\n'
            '  • Units: seconds, minutes, hours, days, weeks, months, years.\n'
            '  • Sign: result = date2 − date1.\n'
            '  • Works with scalars and vectors.'
        ),
        'examples': [
            'r = DateDiff("20.06.2024", "25.06.2024", "DD.MM.YYYY", "days")',
            'r = DateDiff(m[:, "D1"], m[:, "D2"], "DD.MM.YYYY", "days")',
        ],
        'errors': {
            'DATEDIFF_BAD_SYNTAX': {
                'message': (
                    "DateDiff: invalid syntax.\n"
                    "  Need: date1, date2, format, unit."
                ),
                'wrong': 'DateDiff("20.06.2024", "25.06.2024", "DD.MM.YYYY")',
                'right': (
                    'DateDiff("20.06.2024", "25.06.2024", '
                    '"DD.MM.YYYY", "days")'
                ),
                'explanation': (
                    "DateDiff takes FOUR arguments:\n"
                    "  1. date1\n"
                    "  2. date2\n"
                    "  3. format (string)\n"
                    "  4. unit\n"
                    "\n"
                    "Allowed units:\n"
                    "     seconds, minutes, hours,\n"
                    "     days, weeks, months, years"
                ),
                'variants': [
                    'r = DateDiff("20.06.2024", "25.06.2024", "DD.MM.YYYY", "days")',
                ],
            },
            'DATEDIFF_BAD_UNIT': {
                'message': (
                    "DateDiff: invalid unit.\n"
                    "  Allowed: seconds, minutes, hours, "
                    "days, weeks, months, years."
                ),
                'wrong': 'DateDiff("20.06.2024", "25.06.2024", "DD.MM.YYYY", "d")',
                'right': (
                    'DateDiff("20.06.2024", "25.06.2024", '
                    '"DD.MM.YYYY", "days")'
                ),
                'explanation': (
                    "Unit is written IN FULL, without abbreviations:\n"
                    "     ✅  \"days\", \"months\", \"years\"\n"
                    "     ❌  \"d\", \"m\", \"y\"\n"
                    "\n"
                    "Full list: seconds, minutes, hours,\n"
                    "           days, weeks, months, years"
                ),
                'variants': [
                    'r = DateDiff("20.06.2024", "25.06.2024", "DD.MM.YYYY", "days")',
                    'r = DateDiff("20.06.2024", "25.06.2024", "DD.MM.YYYY", "months")',
                ],
            },
        },
    },

    # ============================================================
    # DATENOW
    # ============================================================
    'datenow': {
        'name': 'datenow',
        'category': 'dates',
        'signature': 'datenow([format])',
        'description': (
            'Current date.\n'
            '  • Without argument — "YYYY-MM-DD".\n'
            '  • With argument — by the given format.'
        ),
        'examples': [
            'r = datenow()',
            'r = datenow("DD.MM.YYYY")',
        ],
        'errors': {
            'DATENOW_BAD_SYNTAX': {
                'message': (
                    "datenow: invalid syntax.\n"
                    "  Either no arguments or one format."
                ),
                'wrong': 'datenow("DD.MM.YYYY", "YYYY-MM-DD")',
                'right': 'datenow("DD.MM.YYYY")',
                'explanation': (
                    "datenow takes 0 or 1 argument:\n"
                    "     datenow()                    — YYYY-MM-DD\n"
                    '     datenow("DD.MM.YYYY")        — 20.06.2025'
                ),
                'variants': [
                    'r = datenow()',
                    'r = datenow("DD.MM.YYYY")',
                ],
            },
            'DATENOW_BAD_FORMAT': {
                'message': (
                    "datenow: format must be a quoted string."
                ),
                'wrong': 'datenow(DD.MM.YYYY)',
                'right': 'datenow("DD.MM.YYYY")',
                'explanation': (
                    "Format is a STRING IN QUOTES:\n"
                    '     ✅  datenow("DD.MM.YYYY")\n'
                    "     ❌  datenow(DD.MM.YYYY)"
                ),
                'variants': [
                    'r = datenow()',
                    'r = datenow("DD.MM.YYYY")',
                ],
            },
        },
    },

    # ============================================================
    # TIMENOW
    # ============================================================
    'timenow': {
        'name': 'timenow',
        'category': 'dates',
        'signature': 'timenow([format])',
        'description': (
            'Current time.\n'
            '  • Without argument — "HH:MM:SS".\n'
            '  • With argument — by the given format.'
        ),
        'examples': [
            'r = timenow()',
            'r = timenow("HH:MM")',
        ],
        'errors': {
            'TIMENOW_BAD_SYNTAX': {
                'message': (
                    "timenow: invalid syntax.\n"
                    "  Either no arguments or one format."
                ),
                'wrong': 'timenow("HH:MM", "HH:MM:SS")',
                'right': 'timenow("HH:MM")',
                'explanation': (
                    "timenow takes 0 or 1 argument:\n"
                    "     timenow()                — HH:MM:SS\n"
                    '     timenow("HH:MM")         — HH:MM'
                ),
                'variants': [
                    'r = timenow()',
                    'r = timenow("HH:MM")',
                ],
            },
            'TIMENOW_BAD_FORMAT': {
                'message': (
                    "timenow: format must be a quoted string."
                ),
                'wrong': 'timenow(HH:MM)',
                'right': 'timenow("HH:MM")',
                'explanation': (
                    "Format is a STRING IN QUOTES."
                ),
                'variants': [
                    'r = timenow()',
                    'r = timenow("HH:MM")',
                ],
            },
        },
    },

    # ============================================================
    # TIMESTAMP
    # ============================================================
    'timestamp': {
        'name': 'timestamp',
        'category': 'dates',
        'signature': 'timestamp([format])',
        'description': (
            'Current date and time.\n'
            '  • Without argument — "YYYY-MM-DD HH:MM:SS".\n'
            '  • With argument — by the given format.'
        ),
        'examples': [
            'r = timestamp()',
            'r = timestamp("DD.MM.YYYY HH:MM")',
        ],
        'errors': {
            'TIMESTAMP_BAD_SYNTAX': {
                'message': (
                    "timestamp: invalid syntax.\n"
                    "  Either no arguments or one format."
                ),
                'wrong': 'timestamp("DD.MM.YYYY", "HH:MM")',
                'right': 'timestamp("DD.MM.YYYY HH:MM")',
                'explanation': (
                    "timestamp takes 0 or 1 argument.\n"
                    "Date and time — in ONE format:\n"
                    '     timestamp("DD.MM.YYYY HH:MM")'
                ),
                'variants': [
                    'r = timestamp()',
                    'r = timestamp("DD.MM.YYYY HH:MM")',
                ],
            },
        },
    },

    # ============================================================
    # CALENDAR
    # ============================================================
    'calendar': {
        'name': 'calendar',
        'category': 'dates',
        'signature': 'calendar("dd.mm.yyyy", month, year [, "ru"|"eu"|"us"])',
        'description': (
            'Calendar of dates by a template.\n'
            '  • month: 1-12 or all (12 columns)\n'
            '  • year: 1981, 2026, datenow()\n'
            '  • locale: "ru", "eu", "us"'
        ),
        'examples': [
            'v = calendar("dd.mm.yyyy", 1, 2026, "ru")',
            'm = calendar("dd.mm.yyyy", all, 2026, "eu")',
        ],
        'errors': {
            'CALENDAR_BAD_FORMAT': {
                'message': (
                    "calendar: format must be a string.\n"
                    "  Example: \"dd.mm.yyyy\", \"yyyy-mm-dd\"."
                ),
                'wrong': 'calendar(dd.mm.yyyy, 1, 2026)',
                'right': 'calendar("dd.mm.yyyy", 1, 2026)',
                'explanation': (
                    "First argument — date format, a STRING IN QUOTES."
                ),
                'variants': [
                    'v = calendar("dd.mm.yyyy", 1, 2026)',
                    'm = calendar("yyyy-mm-dd", all, 2026)',
                ],
            },
            'CALENDAR_BAD_YEAR': {
                'message': (
                    "calendar: year must be a number (1900–2200)."
                ),
                'wrong': 'calendar("dd.mm.yyyy", 1, "2026")',
                'right': 'calendar("dd.mm.yyyy", 1, 2026)',
                'explanation': (
                    "Year — a NUMBER without quotes, or datenow():\n"
                    '     calendar("dd.mm.yyyy", 1, 2026)\n'
                    '     calendar("dd.mm.yyyy", 1, datenow())'
                ),
                'variants': [
                    'v = calendar("dd.mm.yyyy", 1, 2026)',
                ],
            },
            'CALENDAR_BAD_MONTH': {
                'message': (
                    "calendar: month must be 1–12 or all."
                ),
                'wrong': 'calendar("dd.mm.yyyy", 13, 2026)',
                'right': 'calendar("dd.mm.yyyy", 1, 2026)',
                'explanation': (
                    "Month — a NUMBER from 1 to 12 or the keyword all:\n"
                    '     calendar("dd.mm.yyyy", 1, 2026)     — January\n'
                    '     calendar("dd.mm.yyyy", all, 2026)   — 12 columns'
                ),
                'variants': [
                    'v = calendar("dd.mm.yyyy", 1, 2026)',
                    'm = calendar("dd.mm.yyyy", all, 2026)',
                ],
            },
            'CALENDAR_BAD_LOCALE': {
                'message': (
                    "calendar: locale must be \"ru\", \"eu\" or \"us\"."
                ),
                'wrong': 'calendar("dd.mm.yyyy", 1, 2026, "russia")',
                'right': 'calendar("dd.mm.yyyy", 1, 2026, "ru")',
                'explanation': (
                    "Only three locales:\n"
                    '     "ru"  — Russian\n'
                    '     "eu"  — European\n'
                    '     "us"  — American'
                ),
                'variants': [
                    'v = calendar("dd.mm.yyyy", 1, 2026, "ru")',
                    'v = calendar("dd.mm.yyyy", 1, 2026, "us")',
                ],
            },
        },
    },

    # ============================================================
    # CALENDARPRO
    # ============================================================
    'calendarpro': {
        'name': 'calendarpro',
        'category': 'dates',
        'signature': 'calendarpro(year, month [, "ru"|"eu"|"us"])',
        'description': (
            'Calendar with working/holiday day info.\n'
            '  • month: 1-12 or all\n'
            '  • locale: "ru", "eu", "us"'
        ),
        'examples': [
            'm = calendarpro(2026, 1)',
            'm = calendarpro(2026, all)',
        ],
        'errors': {
            'CALENDARPRO_BAD_YEAR': {
                'message': (
                    "calendarpro: year must be a number (1900–2200)."
                ),
                'wrong': 'calendarpro("2026", 1)',
                'right': 'calendarpro(2026, 1)',
                'explanation': (
                    "Year — a NUMBER or datenow():\n"
                    "     calendarpro(2026, 1)"
                ),
                'variants': [
                    'm = calendarpro(2026, 1)',
                ],
            },
            'CALENDARPRO_BAD_MONTH': {
                'message': (
                    "calendarpro: month must be 1–12 or all."
                ),
                'wrong': 'calendarpro(2026, 0)',
                'right': 'calendarpro(2026, 1)',
                'explanation': (
                    "Month — a NUMBER from 1 to 12 or all."
                ),
                'variants': [
                    'm = calendarpro(2026, 1)',
                    'm = calendarpro(2026, all)',
                ],
            },
            'CALENDARPRO_BAD_LOCALE': {
                'message': (
                    "calendarpro: locale — \"ru\", \"eu\" or \"us\"."
                ),
                'wrong': 'calendarpro(2026, 1, "russia")',
                'right': 'calendarpro(2026, 1, "ru")',
                'explanation': (
                    '     "ru"  — Russian holidays\n'
                    '     "eu"  — no holidays\n'
                    '     "us"  — US holidays'
                ),
                'variants': [
                    'm = calendarpro(2026, 1, "ru")',
                    'm = calendarpro(2026, 1, "us")',
                ],
            },
        },
    },

    # ============================================================
    # YEAR / MONTH / DAY / QUARTER
    # ============================================================
    'year': {
        'name': 'year',
        'category': 'dates',
        'signature': 'year(data [, "format"])',
        'description': (
            'Extract the year from a date.\n'
            '  • Without format — auto-detect.\n'
            '  • Returns a number.'
        ),
        'examples': [
            'r = year("20.06.2025")',
            'r = year("2025-06-20", "YYYY-MM-DD")',
        ],
        'errors': {
            'YEAR_BAD_SYNTAX': {
                'message': "year: invalid syntax.",
                'wrong': 'year()',
                'right': 'year("20.06.2025")',
                'explanation': (
                    "year takes 1 or 2 arguments:\n"
                    '     year("20.06.2025")              — auto\n'
                    '     year("2025-06-20", "YYYY-MM-DD")  — explicit'
                ),
                'variants': [
                    'r = year("20.06.2025")',
                ],
            },
        },
    },

    'month': {
        'name': 'month',
        'category': 'dates',
        'signature': 'month(data [, "format"])',
        'description': 'Extract the month number (1–12).',
        'examples': [
            'r = month("20.06.2025")',
        ],
        'errors': {
            'MONTH_BAD_SYNTAX': {
                'message': "month: invalid syntax.",
                'wrong': 'month()',
                'right': 'month("20.06.2025")',
                'explanation': (
                    "month takes 1 or 2 arguments."
                ),
                'variants': [
                    'r = month("20.06.2025")',
                ],
            },
        },
    },

    'day': {
        'name': 'day',
        'category': 'dates',
        'signature': 'day(data [, "format"])',
        'description': 'Extract the day of the month (1–31).',
        'examples': [
            'r = day("20.06.2025")',
        ],
        'errors': {
            'DAY_BAD_SYNTAX': {
                'message': "day: invalid syntax.",
                'wrong': 'day()',
                'right': 'day("20.06.2025")',
                'explanation': (
                    "day takes 1 or 2 arguments."
                ),
                'variants': [
                    'r = day("20.06.2025")',
                ],
            },
        },
    },

    'quarter': {
        'name': 'quarter',
        'category': 'dates',
        'signature': 'quarter(data [, "format"])',
        'description': 'Extract the quarter number (1–4).',
        'examples': [
            'r = quarter("20.06.2025")   # 2',
        ],
        'errors': {
            'QUARTER_BAD_SYNTAX': {
                'message': "quarter: invalid syntax.",
                'wrong': 'quarter()',
                'right': 'quarter("20.06.2025")',
                'explanation': (
                    "quarter takes 1 or 2 arguments.\n"
                    "Returns 1–4."
                ),
                'variants': [
                    'r = quarter("20.06.2025")',
                ],
            },
        },
    },

    # ============================================================
    # WEEKDAY / WEEKDAYNAME / MONTHNAME
    # ============================================================
    'weekday': {
        'name': 'weekday',
        'category': 'dates',
        'signature': 'weekday(data [, "format"])',
        'description': (
            'Weekday as a number (1–7).\n'
            '  • 1 = Monday, 7 = Sunday.'
        ),
        'examples': [
            'r = weekday("20.06.2025")   # 5',
        ],
        'errors': {
            'WEEKDAY_BAD_SYNTAX': {
                'message': "weekday: invalid syntax.",
                'wrong': 'weekday()',
                'right': 'weekday("20.06.2025")',
                'explanation': (
                    "weekday takes 1 or 2 arguments.\n"
                    "Returns 1–7."
                ),
                'variants': [
                    'r = weekday("20.06.2025")',
                ],
            },
        },
    },

    'weekdayname': {
        'name': 'weekdayname',
        'category': 'dates',
        'signature': 'weekdayname(data [, "format"])',
        'description': 'Weekday name as a string.',
        'examples': [
            'r = weekdayname("20.06.2025")   # "Пятница" / "Friday"',
        ],
        'errors': {
            'WEEKDAYNAME_BAD_SYNTAX': {
                'message': "weekdayname: invalid syntax.",
                'wrong': 'weekdayname()',
                'right': 'weekdayname("20.06.2025")',
                'explanation': (
                    "weekdayname takes 1 or 2 arguments."
                ),
                'variants': [
                    'r = weekdayname("20.06.2025")',
                ],
            },
        },
    },

    'monthname': {
        'name': 'monthname',
        'category': 'dates',
        'signature': 'monthname(data [, "format"])',
        'description': 'Month name as a string.',
        'examples': [
            'r = monthname("20.06.2025")   # "Июнь" / "June"',
        ],
        'errors': {
            'MONTHNAME_BAD_SYNTAX': {
                'message': "monthname: invalid syntax.",
                'wrong': 'monthname()',
                'right': 'monthname("20.06.2025")',
                'explanation': (
                    "monthname takes 1 or 2 arguments."
                ),
                'variants': [
                    'r = monthname("20.06.2025")',
                ],
            },
        },
    },

    # ============================================================
    # ADDDAYS / ADDMONTHS / ADDYEARS
    # ============================================================
    'adddays': {
        'name': 'adddays',
        'category': 'dates',
        'signature': 'adddays(data, N [, "format"])',
        'description': (
            'Add N days to a date.\n'
            '  • N can be negative.\n'
            '  • Without format — result in the input string format.'
        ),
        'examples': [
            'r = adddays("20.06.2025", 10)    # "30.06.2025"',
            'r = adddays("20.06.2025", -5)    # "15.06.2025"',
        ],
        'errors': {
            'ADDDAYS_BAD_SYNTAX': {
                'message': (
                    "adddays: invalid syntax.\n"
                    "  Need data and N — number of days."
                ),
                'wrong': 'adddays("20.06.2025")',
                'right': 'adddays("20.06.2025", 10)',
                'explanation': (
                    "adddays takes 2 or 3 arguments:\n"
                    "  1. data\n"
                    "  2. N — number of days (can be negative)\n"
                    "  3. format (optional)"
                ),
                'variants': [
                    'r = adddays("20.06.2025", 10)',
                    'r = adddays("20.06.2025", -5)',
                ],
            },
            'ADDDAYS_BAD_N': {
                'message': "adddays: N must be a number.",
                'wrong': 'adddays("20.06.2025", "10")',
                'right': 'adddays("20.06.2025", 10)',
                'explanation': (
                    "N — a NUMBER without quotes.\n"
                    "Can be negative."
                ),
                'variants': [
                    'r = adddays("20.06.2025", 10)',
                    'r = adddays("20.06.2025", -5)',
                ],
            },
        },
    },

    'addmonths': {
        'name': 'addmonths',
        'category': 'dates',
        'signature': 'addmonths(data, N [, "format"])',
        'description': 'Add N months to a date.',
        'examples': [
            'r = addmonths("20.06.2025", 2)   # "20.08.2025"',
        ],
        'errors': {
            'ADDMONTHS_BAD_SYNTAX': {
                'message': (
                    "addmonths: invalid syntax.\n"
                    "  Need data and N — number of months."
                ),
                'wrong': 'addmonths("20.06.2025")',
                'right': 'addmonths("20.06.2025", 2)',
                'explanation': (
                    "addmonths(data, N [, \"format\"])"
                ),
                'variants': [
                    'r = addmonths("20.06.2025", 2)',
                ],
            },
        },
    },

    'addyears': {
        'name': 'addyears',
        'category': 'dates',
        'signature': 'addyears(data, N [, "format"])',
        'description': 'Add N years to a date.',
        'examples': [
            'r = addyears("20.06.2025", 1)   # "20.06.2026"',
        ],
        'errors': {
            'ADDYEARS_BAD_SYNTAX': {
                'message': (
                    "addyears: invalid syntax.\n"
                    "  Need data and N — number of years."
                ),
                'wrong': 'addyears("20.06.2025")',
                'right': 'addyears("20.06.2025", 1)',
                'explanation': (
                    "addyears(data, N [, \"format\"])"
                ),
                'variants': [
                    'r = addyears("20.06.2025", 1)',
                ],
            },
        },
    },

    # ============================================================
    # DATETRUNC
    # ============================================================
    'datetrunc': {
        'name': 'datetrunc',
        'category': 'dates',
        'signature': 'datetrunc(data, "unit" [, "format"])',
        'description': (
            'Truncate a date/time to the given unit.\n'
            '  • Units: "day", "month", "quarter", "year",\n'
            '           "hour", "minute", "second".'
        ),
        'examples': [
            'r = datetrunc("20.06.2025", "month")    # "01.06.2025"',
            'r = datetrunc("14:30:15", "hour")       # "14:00:00"',
        ],
        'errors': {
            'DATETRUNC_BAD_UNIT': {
                'message': (
                    "datetrunc: invalid unit.\n"
                    "  Allowed: day, month, quarter, year, "
                    "hour, minute, second."
                ),
                'wrong': 'datetrunc("20.06.2025", "m")',
                'right': 'datetrunc("20.06.2025", "month")',
                'explanation': (
                    "Unit is written IN FULL, without abbreviations:\n"
                    '     "day", "month", "quarter", "year",\n'
                    '     "hour", "minute", "second"\n'
                    "\n"
                    "NOT:\n"
                    '     "d", "m", "y"  ❌'
                ),
                'variants': [
                    'r = datetrunc("20.06.2025", "day")',
                    'r = datetrunc("20.06.2025", "month")',
                    'r = datetrunc("20.06.2025", "year")',
                    'r = datetrunc("14:30:15", "hour")',
                ],
            },
            'DATETRUNC_BAD_SYNTAX': {
                'message': (
                    "datetrunc: invalid syntax.\n"
                    "  Need data and the truncation unit."
                ),
                'wrong': 'datetrunc("20.06.2025")',
                'right': 'datetrunc("20.06.2025", "month")',
                'explanation': (
                    "datetrunc(data, \"unit\" [, \"format\"])\n"
                    "Unit is required."
                ),
                'variants': [
                    'r = datetrunc("20.06.2025", "month")',
                ],
            },
        },
    },

    # ============================================================
    # HOUR / MINUTE / SECOND / AMPM / IS_PM
    # ============================================================
    'hour': {
        'name': 'hour',
        'category': 'dates',
        'signature': 'hour(data [, "format"])',
        'description': (
            'Extract hours (0–23).\n'
            '  • Works with both 24-hour and 12-hour format.'
        ),
        'examples': [
            'r = hour("14:30:15")              # 14',
            'r = hour("02:30 PM")              # 14',
        ],
        'errors': {
            'HOUR_BAD_SYNTAX': {
                'message': "hour: invalid syntax.",
                'wrong': 'hour()',
                'right': 'hour("14:30:15")',
                'explanation': (
                    "hour(data [, \"format\"])"
                ),
                'variants': [
                    'r = hour("14:30:15")',
                    'r = hour("02:30 PM")',
                ],
            },
        },
    },

    'minute': {
        'name': 'minute',
        'category': 'dates',
        'signature': 'minute(data [, "format"])',
        'description': 'Extract minutes (0–59).',
        'examples': [
            'r = minute("14:30:15")   # 30',
        ],
        'errors': {
            'MINUTE_BAD_SYNTAX': {
                'message': "minute: invalid syntax.",
                'wrong': 'minute()',
                'right': 'minute("14:30:15")',
                'explanation': (
                    "minute(data [, \"format\"])"
                ),
                'variants': [
                    'r = minute("14:30:15")',
                ],
            },
        },
    },

    'second': {
        'name': 'second',
        'category': 'dates',
        'signature': 'second(data [, "format"])',
        'description': 'Extract seconds (0–59).',
        'examples': [
            'r = second("14:30:15")   # 15',
        ],
        'errors': {
            'SECOND_BAD_SYNTAX': {
                'message': "second: invalid syntax.",
                'wrong': 'second()',
                'right': 'second("14:30:15")',
                'explanation': (
                    "second(data [, \"format\"])"
                ),
                'variants': [
                    'r = second("14:30:15")',
                ],
            },
        },
    },

    'ampm': {
        'name': 'ampm',
        'category': 'dates',
        'signature': 'ampm(data [, "format"])',
        'description': (
            'Determines AM or PM.\n'
            '  • Returns "AM" or "PM".'
        ),
        'examples': [
            'r = ampm("02:30 PM")   # "PM"',
            'r = ampm("14:30")      # "PM"',
        ],
        'errors': {
            'AMPM_BAD_SYNTAX': {
                'message': "ampm: invalid syntax.",
                'wrong': 'ampm()',
                'right': 'ampm("02:30 PM")',
                'explanation': (
                    "ampm(data [, \"format\"])\n"
                    "Returns \"AM\" or \"PM\"."
                ),
                'variants': [
                    'r = ampm("02:30 PM")',
                    'r = ampm("14:30")',
                ],
            },
        },
    },

    'is_pm': {
        'name': 'is_pm',
        'category': 'dates',
        'signature': 'is_pm(data [, "format"])',
        'description': (
            'Checks if the time is after noon.\n'
            '  • True / False.'
        ),
        'examples': [
            'r = is_pm("02:30 PM")   # True',
            'r = is_pm("09:15 AM")   # False',
        ],
        'errors': {
            'IS_PM_BAD_SYNTAX': {
                'message': "is_pm: invalid syntax.",
                'wrong': 'is_pm()',
                'right': 'is_pm("14:30")',
                'explanation': (
                    "is_pm(data [, \"format\"])\n"
                    "Returns True / False."
                ),
                'variants': [
                    'r = is_pm("02:30 PM")',
                    'r = is_pm("14:30")',
                ],
            },
        },
    },

    # ============================================================
    # ADDHOURS / ADDMINUTES / ADDSECONDS
    # ============================================================
    'addhours': {
        'name': 'addhours',
        'category': 'dates',
        'signature': 'addhours(data, N [, "format"])',
        'description': (
            'Add N hours.\n'
            '  • Correctly rolls over to next day.'
        ),
        'examples': [
            'r = addhours("14:30:15", 2)              # "16:30:15"',
            'r = addhours("20.06.2025 23:00", 2)      # "21.06.2025 01:00"',
        ],
        'errors': {
            'ADDHOURS_BAD_SYNTAX': {
                'message': (
                    "addhours: invalid syntax.\n"
                    "  Need data and N — number of hours."
                ),
                'wrong': 'addhours("14:30:15")',
                'right': 'addhours("14:30:15", 2)',
                'explanation': (
                    "addhours(data, N [, \"format\"])\n"
                    "N can be negative."
                ),
                'variants': [
                    'r = addhours("14:30:15", 2)',
                ],
            },
        },
    },

    'addminutes': {
        'name': 'addminutes',
        'category': 'dates',
        'signature': 'addminutes(data, N [, "format"])',
        'description': 'Add N minutes.',
        'examples': [
            'r = addminutes("14:30:15", 45)   # "15:15:15"',
        ],
        'errors': {
            'ADDMINUTES_BAD_SYNTAX': {
                'message': (
                    "addminutes: invalid syntax.\n"
                    "  Need data and N — number of minutes."
                ),
                'wrong': 'addminutes("14:30:15")',
                'right': 'addminutes("14:30:15", 45)',
                'explanation': (
                    "addminutes(data, N [, \"format\"])"
                ),
                'variants': [
                    'r = addminutes("14:30:15", 45)',
                ],
            },
        },
    },

    'addseconds': {
        'name': 'addseconds',
        'category': 'dates',
        'signature': 'addseconds(data, N [, "format"])',
        'description': 'Add N seconds.',
        'examples': [
            'r = addseconds("14:30:15", 30)   # "14:30:45"',
        ],
        'errors': {
            'ADDSECONDS_BAD_SYNTAX': {
                'message': (
                    "addseconds: invalid syntax.\n"
                    "  Need data and N — number of seconds."
                ),
                'wrong': 'addseconds("14:30:15")',
                'right': 'addseconds("14:30:15", 30)',
                'explanation': (
                    "addseconds(data, N [, \"format\"])"
                ),
                'variants': [
                    'r = addseconds("14:30:15", 30)',
                ],
            },
        },
    },

    # ============================================================
    # TIMETRUNC
    # ============================================================
    'timetrunc': {
        'name': 'timetrunc',
        'category': 'dates',
        'signature': 'timetrunc(data, "unit" [, "format"])',
        'description': (
            'Truncate a time to the given unit.\n'
            '  • Units: "hour", "minute", "second".'
        ),
        'examples': [
            'r = timetrunc("14:30:15", "hour")     # "14:00:00"',
            'r = timetrunc("14:30:15", "minute")   # "14:30:00"',
        ],
        'errors': {
            'TIMETRUNC_BAD_UNIT': {
                'message': (
                    "timetrunc: invalid unit.\n"
                    "  Allowed: hour, minute, second."
                ),
                'wrong': 'timetrunc("14:30:15", "h")',
                'right': 'timetrunc("14:30:15", "hour")',
                'explanation': (
                    "Unit is written IN FULL:\n"
                    '     "hour"     — "14:00:00"\n'
                    '     "minute"   — "14:30:00"\n'
                    '     "second"   — "14:30:15"\n'
                    "\n"
                    "NOT:\n"
                    '     "h", "m", "s"  ❌'
                ),
                'variants': [
                    'r = timetrunc("14:30:15", "hour")',
                    'r = timetrunc("14:30:15", "minute")',
                ],
            },
            'TIMETRUNC_BAD_SYNTAX': {
                'message': (
                    "timetrunc: invalid syntax.\n"
                    "  Need data and the truncation unit."
                ),
                'wrong': 'timetrunc("14:30:15")',
                'right': 'timetrunc("14:30:15", "hour")',
                'explanation': (
                    "timetrunc(data, \"unit\" [, \"format\"])"
                ),
                'variants': [
                    'r = timetrunc("14:30:15", "hour")',
                ],
            },
        },
    },

    # ============================================================
    # TIME
    # ============================================================
    'time': {
        'name': 'time',
        'category': 'dates',
        'signature': 'time(data, "input_format", "output_format")',
        'description': (
            'Convert time from one format to another.\n'
            '  • All three arguments are required.'
        ),
        'examples': [
            'r = time("02:30 PM", "hh:MM AM", "HH:MM")      # "14:30"',
            'r = time("14:30", "HH:MM", "hh:MM AM")         # "02:30 PM"',
        ],
        'errors': {
            'TIME_BAD_SYNTAX': {
                'message': (
                    "time: invalid syntax.\n"
                    "  Need data and BOTH formats."
                ),
                'wrong': 'time("02:30 PM", "hh:MM AM")',
                'right': 'time("02:30 PM", "hh:MM AM", "HH:MM")',
                'explanation': (
                    "time ALWAYS takes THREE arguments:\n"
                    "  1. data — string or slice\n"
                    "  2. input format\n"
                    "  3. output format"
                ),
                'variants': [
                    'r = time("02:30 PM", "hh:MM AM", "HH:MM")',
                    'r = time("14:30", "HH:MM", "hh:MM AM")',
                ],
            },
        },
    },

    # ============================================================
    # IS_VALID_TIME
    # ============================================================
    'is_valid_time': {
        'name': 'is_valid_time',
        'category': 'types',
        'signature': 'is_valid_time(data [, "format"])',
        'description': (
            'Check that a string is a valid time.\n'
            '  • Supports 24-hour and 12-hour (AM/PM).\n'
            '  • None / non-string / empty → False.\n'
            '  • Dates return False (not a time).'
        ),
        'examples': [
            'r = is_valid_time("14:30:15")   # True',
            'r = is_valid_time("25:99:99")   # False',
            'r = is_valid_time("29.09.2026") # False',
        ],
        'errors': {
            'VALID_TIME_BAD_SYNTAX': {
                'message': (
                    "is_valid_time: invalid syntax.\n"
                    "  Need data and optionally a format."
                ),
                'wrong': 'is_valid_time()',
                'right': 'is_valid_time("14:30:15")',
                'explanation': (
                    "is_valid_time(data [, \"format\"])\n"
                    "\n"
                    "     is_valid_time(\"14:30:15\")              — auto\n"
                    "     is_valid_time(m[:, \"Time\"], \"HH:MM:SS\")"
                ),
                'variants': [
                    'r = is_valid_time("14:30:15")',
                    'r = is_valid_time(m[:, "Time"], "HH:MM:SS")',
                ],
            },
        },
    },
}