# syntax/autocomplete/items_search.py
"""
Описания функций поиска: find, index, vlookup.
"""

RU = {
    'find': {
        'signature': 'find(m[:, "X"] == "Y" [, inside] [, ignore] [, rows|cols])',
        'description': (
            'Находит координаты значений, удовлетворяющих условию.\n'
            '  • По умолчанию возвращает МАТРИЦУ координат [[строка, столбец], ...].\n'
            '  • `rows` — вектор номеров строк.\n'
            '  • `cols` — вектор номеров столбцов.\n'
            '  • `inside` — поиск подстроки, `ignore` — без учёта регистра.'
        ),
        'example': (
            'r = find(m[:, "Имя"] == "Аня")\n'
            'r = find(m[:, "Имя"] == "ов", inside)\n'
            'r = find(m[:, "Отдел"] == "IT", rows)'
        ),
        'matrix_example': (
            '# ДАНО:\n'
            '#\n'
            '#   m = ["Имя", "Отдел", "Возраст";\n'
            '#        "Аня", "IT",    25;\n'
            '#        "Боб", "HR",    32;\n'
            '#        "Света","IT",  28;\n'
            '#        "Гена","Sales", 41]\n'
            '\n'
            '# 1. Найти координаты всех сотрудников из IT\n'
            'r1 = find(m[:, "Отдел"] == "IT")\n'
            'print(r1)\n'
            '\n'
            '# ВЫВОД (строка 2, столбец 2; строка 3, столбец 2):\n'
            '#\n'
            '#   [[2, 2], [3, 2]]\n'
            '\n'
            '# 2. Найти только номера строк, где возраст > 30\n'
            'r2 = find(m[:, "Возраст"] > 30, rows)\n'
            'print(r2)\n'
            '\n'
            '# ВЫВОД (Боб и Гена):\n'
            '#\n'
            '#   [3, 5]'
        ),
    },
    'index': {
        'signature': 'index(m[:, "X"] == "Y" [, inside] [, ignore])',
        'description': (
            'Полный аналог find. Координаты найденных значений.'
        ),
        'example': 'r = index(m[:, "Имя"] == "Аня")',
    },
    'vlookup': {
        'signature': 'vlookup(где_искать, что_искать, что_возвращать)',
        'description': (
            'Аналог ВПР. Ищет значения в справочнике.\n'
            '\n'
            'МНЕМОНИКА:\n'
            '     vlookup( где_искать,  что_искать,  что_возвращать )\n'
            '             └── a ───┘  └── b ───┘  └── a ───┘\n'
            '             справочник    запрос      справочник\n'
            '\n'
            '  1-й аргумент — срез столбца-ключа СПРАВОЧНИКА.\n'
            '  2-й аргумент — что искать (скаляр или вектор).\n'
            '  3-й аргумент — срез столбца ЗНАЧЕНИЙ справочника.\n'
            '\n'
            '  • 1-й и 3-й аргументы — из ОДНОЙ таблицы (справочника).\n'
            '  • 2-й — откуда угодно (источник запроса).\n'
            '  • Не найдено → None.\n'
            '  • Дубликаты ключа — берётся первое совпадение.\n'
            '  • Строки сравниваются без учёта регистра.\n'
            '  • Числа — с приведением типов (101 == "101").'
        ),
        'example': (
            '# Справочник\n'
            'a = ["ID", "Имя",   "Отдел";\n'
            '     101,  "Аня",   "IT";\n'
            '     102,  "Боб",   "HR";\n'
            '     103,  "Света", "IT"]\n'
            '\n'
            '# Данные\n'
            'b = ["ID", "Сумма";\n'
            '     101,  5000;\n'
            '     103,  7000;\n'
            '     102,  3000]\n'
            '\n'
            '# Поиск одного значения\n'
            'r = vlookup(a[:, "ID"], 101, a[:, "Отдел"])\n'
            '# r = "IT"\n'
            '\n'
            '# Обогащение таблицы\n'
            'b[:, end+1] = vlookup(a[:, "ID"], b[:, "ID"], a[:, "Отдел"])\n'
            'print(b)'
        ),
        'matrix_example': (
            '# ДАНО:\n'
            '#\n'
            '#   a = ["ID", "Имя",   "Отдел";\n'
            '#        101,  "Аня",   "IT";\n'
            '#        102,  "Боб",   "HR";\n'
            '#        103,  "Света", "IT"]\n'
            '#\n'
            '#   b = ["ID", "Сумма";\n'
            '#        101,  5000;\n'
            '#        103,  7000;\n'
            '#        102,  3000]\n'
            '\n'
            'b[:, end+1] = vlookup(a[:, "ID"], b[:, "ID"], a[:, "Отдел"])\n'
            'print(b)\n'
            '\n'
            '# ВЫВОД:\n'
            '#\n'
            '#   ID    Сумма  None\n'
            '#   101   5000   IT\n'
            '#   103   7000   IT\n'
            '#   102   3000   HR'
        ),
    },
}


EN = {
    'find': {
        'signature': 'find(m[:, "X"] == "Y" [, inside] [, ignore] [, rows|cols])',
        'description': (
            'Coordinates of found values.\n'
            '  • By default returns a MATRIX of coordinates [[row, col], ...].\n'
            '  • `rows` — vector of row numbers.\n'
            '  • `cols` — vector of column numbers.\n'
            '  • `inside` — substring search, `ignore` — case-insensitive.'
        ),
        'example': (
            'r = find(m[:, "Name"] == "Anna")\n'
            'r = find(m[:, "Name"] == "ov", inside)\n'
            'r = find(m[:, "Dept"] == "IT", rows)'
        ),
    },
    'index': {
        'signature': 'index(m[:, "X"] == "Y" [, inside] [, ignore])',
        'description': 'Alias of find. Coordinates of found values.',
        'example': 'r = index(m[:, "Name"] == "Anna")',
    },
    'vlookup': {
        'signature': 'vlookup(where_lookup, what_search, what_return)',
        'description': (
            'VLOOKUP analog. Searches values in a lookup table.\n'
            '\n'
            'MNEMONIC:\n'
            '     vlookup( where_lookup,  what_search,  what_return )\n'
            '              └─── a ────┘  └─── b ────┘  └─── a ────┘\n'
            '              lookup table    query        lookup table\n'
            '\n'
            '  1st arg — slice of the KEY column of the LOOKUP table.\n'
            '  2nd arg — what to search (scalar or vector).\n'
            '  3rd arg — slice of the VALUE column of the lookup table.\n'
            '\n'
            '  • 1st and 3rd args — from the SAME table (lookup).\n'
            '  • 2nd — from ANY table (source of query).\n'
            '  • Not found → None.\n'
            '  • Duplicates — first match wins.\n'
            '  • Strings are compared case-insensitively.\n'
            '  • Numbers — with type coercion (101 == "101").'
        ),
        'example': (
            '# Lookup table\n'
            'a = ["ID", "Name", "Dept";\n'
            '     101,  "Anna", "IT";\n'
            '     102,  "Bob",  "HR";\n'
            '     103,  "Eve",  "IT"]\n'
            '\n'
            '# Data\n'
            'b = ["ID", "Amount";\n'
            '     101,  5000;\n'
            '     103,  7000;\n'
            '     102,  3000]\n'
            '\n'
            '# Single value lookup\n'
            'r = vlookup(a[:, "ID"], 101, a[:, "Dept"])\n'
            '# r = "IT"\n'
            '\n'
            '# Enrich table\n'
            'b[:, end+1] = vlookup(a[:, "ID"], b[:, "ID"], a[:, "Dept"])\n'
            'print(b)'
        ),
        'matrix_example': (
            '# INPUT:\n'
            '#\n'
            '#   a = ["ID", "Name", "Dept";\n'
            '#        101,  "Anna", "IT";\n'
            '#        102,  "Bob",  "HR";\n'
            '#        103,  "Eve",  "IT"]\n'
            '#\n'
            '#   b = ["ID", "Amount";\n'
            '#        101,  5000;\n'
            '#        103,  7000;\n'
            '#        102,  3000]\n'
            '\n'
            'b[:, end+1] = vlookup(a[:, "ID"], b[:, "ID"], a[:, "Dept"])\n'
            'print(b)\n'
            '\n'
            '# OUTPUT:\n'
            '#\n'
            '#   ID    Amount  None\n'
            '#   101   5000    IT\n'
            '#   103   7000    IT\n'
            '#   102   3000    HR'
        ),
    },
}