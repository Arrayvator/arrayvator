# syntax/autocomplete/items_calendar.py
"""
Описания функций calendar и calendarpro.
"""

RU = {
    'calendar': {
        'signature': 'calendar("dd.mm.yyyy", месяц, год [, "ru"|"eu"|"us"])',
        'description': (
            'Календарь дат по шаблону.\n'
            '  • месяц: 1-12 или all (все 12 колонок)\n'
            '  • год: 1981, 2026, datenow()\n'
            '  • локаль: "ru" (русский), "eu" (европейский), '
            '"us" (американский)\n'
            '  • Возвращает МАТРИЦУ с заголовком.\n'
            '  • Токены: yyyy, yy, MMMM, MMM, MM, dd, dddd, ddd'
        ),
        'example': (
            'v = calendar("dd.mm.yyyy", 1, 2026, "ru")\n'
            'm = calendar("dd.mm.yyyy", all, 2026, "eu")\n'
            'v = calendar("yyyy-mm-dd", datenow(), datenow(), "us")'
        ),
        'matrix_example': (
            'v = calendar("dd.mm.yyyy", 1, 2026, "ru")\n'
            'print(v)\n'
            '# Январь 2026\n'
            '# 01.01.2026\n'
            '# 02.01.2026\n'
            '# ...\n'
            '# 31.01.2026'
        ),
    },
    'calendarpro': {
        'signature': 'calendarpro(год, месяц [, "ru"|"eu"|"us"])',
        'description': (
            'Производственный календарь.\n'
            '  • месяц: 1-12 или all (весь год)\n'
            '  • локаль: "ru" (праздники РФ), "us" (праздники US), '
            '"eu" (без праздников)\n'
            '  • Колонки: Дата, ДеньНедели, Рабочий, Праздник, Сокращённый'
        ),
        'example': (
            'm = calendarpro(2026, 1, "ru")\n'
            'm = calendarpro(2026, all, "us")\n'
            'm = calendarpro(datenow(), datenow(), "eu")'
        ),
        'matrix_example': (
            'm = calendarpro(2026, 1, "ru")\n'
            'print(m)\n'
            '# Дата         ДеньНедели  Рабочий  Праздник             Сокращённый\n'
            '# 01.01.2026   Чт          нет      Новый год            нет\n'
            '# 02.01.2026   Пт          нет      Новогодние каникулы  нет'
        ),
    },
}


EN = {
    'calendar': {
        'signature': 'calendar("dd.mm.yyyy", month, year [, "ru"|"eu"|"us"])',
        'description': (
            'Calendar of dates by template.\n'
            '  • month: 1-12 or all (all 12 columns)\n'
            '  • year: 1981, 2026, datenow()\n'
            '  • locale: "ru" (Russian), "eu" (European), "us" (American)\n'
            '  • Returns a MATRIX with a header.\n'
            '  • Tokens: yyyy, yy, MMMM, MMM, MM, dd, dddd, ddd'
        ),
        'example': (
            'v = calendar("dd.mm.yyyy", 1, 2026, "ru")\n'
            'm = calendar("dd.mm.yyyy", all, 2026, "eu")\n'
            'v = calendar("yyyy-mm-dd", datenow(), datenow(), "us")'
        ),
        'matrix_example': (
            'v = calendar("dd.mm.yyyy", 1, 2026, "us")\n'
            'print(v)\n'
            '# January 2026\n'
            '# 01.01.2026\n'
            '# 02.01.2026'
        ),
    },
    'calendarpro': {
        'signature': 'calendarpro(year, month [, "ru"|"eu"|"us"])',
        'description': (
            'Production calendar.\n'
            '  • month: 1-12 or all (whole year)\n'
            '  • locale: "ru" (RU holidays), "us" (US holidays), '
            '"eu" (no holidays)\n'
            '  • Columns: Date, Weekday, Working, Holiday, Short'
        ),
        'example': (
            'm = calendarpro(2026, 1, "ru")\n'
            'm = calendarpro(2026, all, "us")\n'
            'm = calendarpro(datenow(), datenow(), "eu")'
        ),
    },
}