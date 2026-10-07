# syntax/autocomplete/items_null.py
"""
Описания литерала None и функций работы с None:
None (литерал), isnone, fillna, dropna, coalesce.

ВАЖНО:
    Слова 'null' и 'nan' в языке НЕ используются.
    Единственный правильный литерал — None (с большой буквы).
"""

RU = {
    # ============================================================
    # ЛИТЕРАЛ NONE
    # ============================================================
    'None': {
        'signature': 'None',
        'description': (
            '🕳️ ПУСТОЕ ЗНАЧЕНИЕ (аналог NULL в SQL)\n'
            '\n'
            'ЗАЧЕМ НУЖНО:\n'
            '  • Обозначить "нет данных" / "неизвестно" / "пропуск".\n'
            '  • Отличается от 0, "" и false.\n'
            '  • Классика: "у клиента нет отчества".\n'
            '\n'
            'ПРАВИЛА:\n'
            '  • Регистр не важен: None, none, NONE.\n'
            '  • Проверяется через isnone().\n'
            '  • Заменяется через fillna().\n'
            '  • Удаляется через dropna().\n'
            '  • Первое не-None берётся через coalesce().\n'
            '\n'
            '⚠️ Слова null и nan НЕ используются — только None.\n'
            '\n'
            'КАКИЕ ЗАДАЧИ РЕШАЕТ:\n'
            '  • Пометить отсутствие значения.\n'
            '  • Различить "0" и "неизвестно".\n'
            '  • Заполнить пропуски перед анализом.'
        ),
        'example': (
            'x = None\n'
            'r = isnone(None)         # True\n'
            'm = [1, None, 3]\n'
            'm = fillna(m, 0)         # None → 0\n'
            'r = coalesce(None, 5)    # 5'
        ),
    },

    # ============================================================
    # ISNONE
    # ============================================================
    'isnone': {
        'signature': 'isnone(значение)',
        'description': (
            '❓ ПРОВЕРКА НА None\n'
            '\n'
            'ЗАЧЕМ НУЖНА:\n'
            '  • Узнать, пустое ли значение.\n'
            '  • Работает поэлементно для векторов и матриц.\n'
            '\n'
            'ВАЖНО:\n'
            '  • isnone(None)     → True\n'
            '  • isnone(5)        → False\n'
            '  • isnone("")       → False (пустая строка — НЕ None!)\n'
            '  • isnone(0)        → False\n'
            '  • isnone(false)    → False\n'
            '\n'
            'КАКИЕ ЗАДАЧИ РЕШАЕТ:\n'
            '  • Найти строки с пропусками.\n'
            '  • Условие для filterif.\n'
            '  • Валидация данных перед расчётами.'
        ),
        'example': (
            'r = isnone(None)         # True\n'
            'r = isnone(5)            # False\n'
            'r = isnone("")           # False\n'
            'r = isnone(m[:, "X"])    # вектор True/False'
        ),
    },

    # ============================================================
    # FILLNA
    # ============================================================
    'fillna': {
        'signature': 'fillna(данные, значение)',
        'description': (
            '💧 ЗАМЕНА None НА ЗНАЧЕНИЕ\n'
            '\n'
            'ЗАЧЕМ НУЖНА:\n'
            '  • Заменить все None указанным значением.\n'
            '  • Остальные значения не трогает.\n'
            '\n'
            'ЧТО МОЖНО ВМЕСТО None:\n'
            '  • число — 0, -1, 999\n'
            '  • строку — "—", "N/A", ""\n'
            '  • другое значение\n'
            '\n'
            'КАКИЕ ЗАДАЧИ РЕШАЕТ:\n'
            '  • "Заменить пропуски нулями перед суммой".\n'
            '  • "Заменить пустые категории на \'—\'".\n'
            '  • Подготовка данных для отчёта.\n'
            '\n'
            '  • Работает с Matrix, DuckDB, скалярами, векторами.'
        ),
        'example': (
            'r = fillna([1, None, 3], 0)     # [1, 0, 3]\n'
            'm = fillna(m, 0)                # все None → 0\n'
            'm = fillna(m[:, "Отдел"], "—")  # None → "—"'
        ),
        'matrix_example': (
            '# ДАНО:\n'
            '#\n'
            '#   m = ["Имя", "Отдел";\n'
            '#        "Аня", "IT";\n'
            '#        "Боб", None;\n'
            '#        "Света", None]\n'
            '\n'
            '# ЗАДАЧА: заменить пропуски в отделе\n'
            'm[:, "Отдел"] = fillna(m[:, "Отдел"], "—")\n'
            'print(m)\n'
            '\n'
            '# ВЫВОД:\n'
            '#\n'
            '#   Имя    Отдел\n'
            '#   Аня    IT\n'
            '#   Боб    —\n'
            '#   Света  —'
        ),
    },

    # ============================================================
    # DROPNA
    # ============================================================
    'dropna': {
        'signature': 'dropna(данные)',
        'description': (
            '🗑️ УДАЛИТЬ СТРОКИ С None\n'
            '\n'
            'ЗАЧЕМ НУЖНА:\n'
            '  • Убрать строки, где есть хоть один None.\n'
            '  • Для вектора — убрать None-элементы.\n'
            '\n'
            'ОТЛИЧИЕ ОТ fillna:\n'
            '  fillna — ЗАМЕНЯЕТ None на значение.\n'
            '  dropna — УДАЛЯЕТ строки с None.\n'
            '\n'
            'КАКИЕ ЗАДАЧИ РЕШАЕТ:\n'
            '  • Очистка данных перед анализом.\n'
            '  • Убрать неполные записи.\n'
            '  • Удалить пустые категории.\n'
            '\n'
            '  • Работает с Matrix и векторами.'
        ),
        'example': (
            'r = dropna([1, None, 3, None, 5])   # [1, 3, 5]\n'
            'm = dropna(m)                        # строки без None'
        ),
    },

    # ============================================================
    # COALESCE
    # ============================================================
    'coalesce': {
        'signature': 'coalesce(знач1, знач2, ...)',
        'description': (
            '🎯 ПЕРВОЕ НЕ-None ЗНАЧЕНИЕ\n'
            '\n'
            'ЗАЧЕМ НУЖНА:\n'
            '  • Вернуть первое значение, которое НЕ None.\n'
            '  • Классика: "использовать резервный телефон, если основной пуст".\n'
            '\n'
            'КАК РАБОТАЕТ:\n'
            '  • Проверяет аргументы СЛЕВА НАПРАВО.\n'
            '  • Первое не-None возвращается.\n'
            '  • Если все None — вернёт None.\n'
            '\n'
            'КАКИЕ ЗАДАЧИ РЕШАЕТ:\n'
            '  • "Основной контакт или резервный".\n'
            '  • Подстановка дефолта для пустых полей.\n'
            '  • Выбор первого заполненного значения из нескольких.\n'
            '\n'
            '  • Работает со скалярами.'
        ),
        'example': (
            'r = coalesce(None, 5)           # 5\n'
            'r = coalesce(None, None, 10)    # 10\n'
            'r = coalesce(1, 2, 3)           # 1\n'
            'r = coalesce(None, None, None)  # None'
        ),
    },
}


EN = {
    'None': {
        'signature': 'None',
        'description': (
            '🕳️ EMPTY VALUE (analog of NULL in SQL)\n'
            '\n'
            'WHY NEEDED:\n'
            '  • Mark "no data" / "unknown" / "missing".\n'
            '  • Different from 0, "" and false.\n'
            '\n'
            'RULES:\n'
            '  • Case-insensitive: None, none, NONE.\n'
            '  • Tested by isnone().\n'
            '  • Replaced by fillna().\n'
            '  • Removed by dropna().\n'
            '  • First non-None is taken by coalesce().\n'
            '\n'
            '⚠️ Literals null and nan are NOT used — only None.'
        ),
        'example': (
            'x = None\n'
            'r = isnone(None)         # True\n'
            'm = [1, None, 3]\n'
            'm = fillna(m, 0)         # None → 0\n'
            'r = coalesce(None, 5)    # 5'
        ),
    },
    'isnone': {
        'signature': 'isnone(value)',
        'description': (
            '❓ CHECK FOR None\n'
            '\n'
            'IMPORTANT:\n'
            '  • isnone(None)     → True\n'
            '  • isnone(5)        → False\n'
            '  • isnone("")       → False (empty string is NOT None!)\n'
            '  • isnone(0)        → False\n'
            '  • isnone(false)    → False'
        ),
        'example': (
            'r = isnone(None)         # True\n'
            'r = isnone(5)            # False\n'
            'r = isnone("")           # False'
        ),
    },
    'fillna': {
        'signature': 'fillna(data, value)',
        'description': (
            '💧 REPLACE None WITH A VALUE\n'
            '\n'
            'WHY NEEDED:\n'
            '  • Replace all None with the given value.\n'
            '  • Other values are not touched.'
        ),
        'example': (
            'r = fillna([1, None, 3], 0)     # [1, 0, 3]\n'
            'm = fillna(m, 0)\n'
            'm = fillna(m[:, "Dept"], "-")'
        ),
    },
    'dropna': {
        'signature': 'dropna(data)',
        'description': (
            '🗑️ REMOVE ROWS WITH None\n'
            '\n'
            'HOW IT DIFFERS FROM fillna:\n'
            '  fillna — REPLACES None with a value.\n'
            '  dropna — REMOVES rows with None.'
        ),
        'example': (
            'r = dropna([1, None, 3, None, 5])   # [1, 3, 5]\n'
            'm = dropna(m)'
        ),
    },
    'coalesce': {
        'signature': 'coalesce(val1, val2, ...)',
        'description': (
            '🎯 FIRST NON-None VALUE\n'
            '\n'
            'HOW IT WORKS:\n'
            '  • Checks arguments LEFT TO RIGHT.\n'
            '  • Returns the first non-None.\n'
            '  • If all are None — returns None.'
        ),
        'example': (
            'r = coalesce(None, 5)           # 5\n'
            'r = coalesce(None, None, 10)    # 10\n'
            'r = coalesce(1, 2, 3)           # 1'
        ),
    },
}