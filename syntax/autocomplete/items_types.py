# syntax/autocomplete/items_types.py
"""
Описания функций типов:
type, is_number, is_integer, is_float, is_string, is_boolean,
to_string, to_number, is_valid_time.
"""

RU = {
    'type': {
        'signature': 'type(значение)',
        'description': (
            '🔎 ОПРЕДЕЛИТЬ ТИП ЗНАЧЕНИЯ\n'
            '\n'
            'ЗАЧЕМ НУЖНА:\n'
            '  • Узнать, что за тип у значения.\n'
            '  • Полезно для отладки и валидации.\n'
            '\n'
            'ВОЗМОЖНЫЕ ОТВЕТЫ:\n'
            '  • "matrix"  — двумерная матрица\n'
            '  • "vector"  — вектор\n'
            '  • "duckdb"  — таблица DuckDB\n'
            '  • "integer" — целое число\n'
            '  • "float"   — число с плавающей точкой\n'
            '  • "string"  — строка\n'
            '  • "boolean" — true / false\n'
            '  • "null"    — None'
        ),
        'example': (
            'r = type(42)       # "integer"\n'
            'r = type(3.14)     # "float"\n'
            'r = type("abc")    # "string"\n'
            'r = type(true)     # "boolean"\n'
            'r = type(None)     # "null"\n'
            'r = type(m)        # "matrix"'
        ),
    },
    'is_number': {
        'signature': 'is_number(значение)',
        'description': (
            '🔢 ПРОВЕРКА НА ЧИСЛО\n'
            '\n'
            'ВОЗВРАЩАЕТ:\n'
            '  • True — если int или float (кроме bool)\n'
            '  • False — во всех остальных случаях\n'
            '\n'
            'ВАЖНО:\n'
            '  • bool (true/false) — НЕ число.\n'
            '  • "42" (строка) — НЕ число.\n'
            '\n'
            'КАКИЕ ЗАДАЧИ РЕШАЕТ:\n'
            '  • Проверка данных перед расчётом.\n'
            '  • Фильтрация только числовых значений.\n'
            '  • Поэлементно для векторов и матриц.'
        ),
        'example': (
            'r = is_number(42)       # True\n'
            'r = is_number(3.14)     # True\n'
            'r = is_number("42")     # False\n'
            'r = is_number(true)     # False\n'
            'r = is_number(None)     # False'
        ),
    },
    'is_integer': {
        'signature': 'is_integer(значение)',
        'description': (
            '🔢 ПРОВЕРКА НА ЦЕЛОЕ ЧИСЛО\n'
            '\n'
            'ВОЗВРАЩАЕТ:\n'
            '  • True — если int (кроме bool)\n'
            '  • False — иначе\n'
            '\n'
            'ВАЖНО:\n'
            '  • 3.14 — НЕ integer.\n'
            '  • true — НЕ integer.'
        ),
        'example': (
            'r = is_integer(42)      # True\n'
            'r = is_integer(3.14)    # False\n'
            'r = is_integer(true)    # False'
        ),
    },
    'is_float': {
        'signature': 'is_float(значение)',
        'description': (
            '🔢 ПРОВЕРКА НА FLOAT\n'
            '\n'
            'ВОЗВРАЩАЕТ True только для чисел с плавающей точкой.'
        ),
        'example': (
            'r = is_float(3.14)      # True\n'
            'r = is_float(42)        # False'
        ),
    },
    'is_string': {
        'signature': 'is_string(значение)',
        'description': (
            '📝 ПРОВЕРКА НА СТРОКУ\n'
            '\n'
            'Возвращает True для строковых значений.'
        ),
        'example': (
            'r = is_string("abc")    # True\n'
            'r = is_string(42)       # False\n'
            'r = is_string("")       # True'
        ),
    },
    'is_boolean': {
        'signature': 'is_boolean(значение)',
        'description': (
            '✅ ПРОВЕРКА НА BOOLEAN\n'
            '\n'
            'Возвращает True только для true / false.'
        ),
        'example': (
            'r = is_boolean(true)    # True\n'
            'r = is_boolean(false)   # True\n'
            'r = is_boolean(1)       # False\n'
            'r = is_boolean(0)       # False'
        ),
    },
    'to_string': {
        'signature': 'to_string(значение)',
        'description': (
            '➡️ ПРЕОБРАЗОВАТЬ В СТРОКУ\n'
            '\n'
            'ЗАЧЕМ НУЖНА:\n'
            '  • Явно превратить число/None/boolean в строку.\n'
            '  • Полезно для склейки с другими строками.\n'
            '\n'
            'ПРАВИЛА:\n'
            '  • None → "" (пустая строка).\n'
            '  • true → "true", false → "false".\n'
            '  • 42 → "42", 3.14 → "3.14".\n'
            '\n'
            '  • Поэлементно для векторов и матриц.'
        ),
        'example': (
            'r = to_string(42)      # "42"\n'
            'r = to_string(3.14)    # "3.14"\n'
            'r = to_string(true)    # "true"\n'
            'r = to_string(None)    # ""'
        ),
    },
    'to_number': {
        'signature': 'to_number(значение)',
        'description': (
            '➡️ ПРЕОБРАЗОВАТЬ В ЧИСЛО\n'
            '\n'
            'ЗАЧЕМ НУЖНА:\n'
            '  • Превратить строку "42" в число 42.\n'
            '  • Для арифметики с "числами, пришедшими как текст".\n'
            '\n'
            'ПРАВИЛА:\n'
            '  • "42" → 42 (int).\n'
            '  • "3.14" → 3.14 (float).\n'
            '  • "abc" → None (не число).\n'
            '  • "" → None.\n'
            '  • None → None.'
        ),
        'example': (
            'r = to_number("42")     # 42\n'
            'r = to_number("3.14")   # 3.14\n'
            'r = to_number("abc")    # None\n'
            'r = to_number("")       # None'
        ),
    },
    'is_valid_time': {
        'signature': 'is_valid_time(данные [, "формат"])',
        'description': (
            '⏰ ПРОВЕРКА КОРРЕКТНОСТИ ВРЕМЕНИ\n'
            '\n'
            'ЗАЧЕМ НУЖНА:\n'
            '  • Проверить, что строка — валидное время.\n'
            '  • До вызова hour()/minute() и подобных.\n'
            '\n'
            'ПОДДЕРЖИВАЕТ:\n'
            '  • 24-часовой формат: "14:30:15", "14:30".\n'
            '  • 12-часовой с AM/PM: "02:30 PM", "09:15 AM".\n'
            '  • Автоопределение формата.\n'
            '\n'
            'ПРАВИЛА:\n'
            '  • None / не-строка / пустая строка → False.\n'
            '  • "25:99:99" → False (некорректное время).\n'
            '  • Дата "29.09.2026" → False (это не время).'
        ),
        'example': (
            'r = is_valid_time("14:30:15")   # True\n'
            'r = is_valid_time("14:30")      # True\n'
            'r = is_valid_time("02:30 PM")   # True\n'
            'r = is_valid_time("25:99:99")   # False\n'
            'r = is_valid_time("29.09.2026") # False'
        ),
    },
}


EN = {
    'type': {
        'signature': 'type(value)',
        'description': (
            '🔎 DETERMINE VALUE TYPE\n'
            '\n'
            'POSSIBLE ANSWERS:\n'
            '  • "matrix"  — 2D matrix\n'
            '  • "vector"  — vector\n'
            '  • "duckdb"  — DuckDB table\n'
            '  • "integer" — integer\n'
            '  • "float"   — floating point\n'
            '  • "string"  — string\n'
            '  • "boolean" — true / false\n'
            '  • "null"    — None'
        ),
        'example': (
            'r = type(42)       # "integer"\n'
            'r = type(3.14)     # "float"\n'
            'r = type("abc")    # "string"\n'
            'r = type(true)     # "boolean"\n'
            'r = type(None)     # "null"\n'
            'r = type(m)        # "matrix"'
        ),
    },
    'is_number': {
        'signature': 'is_number(value)',
        'description': (
            '🔢 CHECK IF VALUE IS A NUMBER\n'
            '\n'
            'RETURNS:\n'
            '  • True — if int or float (not bool)\n'
            '  • False — otherwise'
        ),
        'example': (
            'r = is_number(42)       # True\n'
            'r = is_number(3.14)     # True\n'
            'r = is_number("42")     # False\n'
            'r = is_number(true)     # False'
        ),
    },
    'is_integer': {
        'signature': 'is_integer(value)',
        'description': '🔢 CHECK IF VALUE IS AN INTEGER.',
        'example': (
            'r = is_integer(42)      # True\n'
            'r = is_integer(3.14)    # False'
        ),
    },
    'is_float': {
        'signature': 'is_float(value)',
        'description': '🔢 CHECK IF VALUE IS A FLOAT.',
        'example': (
            'r = is_float(3.14)      # True\n'
            'r = is_float(42)        # False'
        ),
    },
    'is_string': {
        'signature': 'is_string(value)',
        'description': '📝 CHECK IF VALUE IS A STRING.',
        'example': (
            'r = is_string("abc")    # True\n'
            'r = is_string(42)       # False'
        ),
    },
    'is_boolean': {
        'signature': 'is_boolean(value)',
        'description': '✅ CHECK IF VALUE IS A BOOLEAN.',
        'example': (
            'r = is_boolean(true)    # True\n'
            'r = is_boolean(false)   # True\n'
            'r = is_boolean(1)       # False'
        ),
    },
    'to_string': {
        'signature': 'to_string(value)',
        'description': (
            '➡️ CONVERT TO STRING\n'
            '\n'
            'RULES:\n'
            '  • None → ""\n'
            '  • true → "true", false → "false"\n'
            '  • 42 → "42", 3.14 → "3.14"'
        ),
        'example': (
            'r = to_string(42)      # "42"\n'
            'r = to_string(3.14)    # "3.14"\n'
            'r = to_string(true)    # "true"\n'
            'r = to_string(None)    # ""'
        ),
    },
    'to_number': {
        'signature': 'to_number(value)',
        'description': (
            '➡️ CONVERT TO NUMBER\n'
            '\n'
            'RULES:\n'
            '  • "42" → 42 (int)\n'
            '  • "3.14" → 3.14 (float)\n'
            '  • "abc" → None\n'
            '  • "" → None\n'
            '  • None → None'
        ),
        'example': (
            'r = to_number("42")     # 42\n'
            'r = to_number("3.14")   # 3.14\n'
            'r = to_number("abc")    # None'
        ),
    },
    'is_valid_time': {
        'signature': 'is_valid_time(data [, "format"])',
        'description': (
            '⏰ CHECK IF TIME IS VALID\n'
            '\n'
            'SUPPORTS:\n'
            '  • 24-hour: "14:30:15", "14:30"\n'
            '  • 12-hour with AM/PM: "02:30 PM"\n'
            '  • Auto-detect format'
        ),
        'example': (
            'r = is_valid_time("14:30:15")   # True\n'
            'r = is_valid_time("14:30")      # True\n'
            'r = is_valid_time("02:30 PM")   # True\n'
            'r = is_valid_time("25:99:99")   # False'
        ),
    },
}