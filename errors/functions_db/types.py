# errors/functions_db/types.py
"""
База ошибок для функций работы с типами данных:
    type, is_number, is_integer, is_float, is_string, is_boolean,
    to_string, to_number, is_valid_time.

СИНТАКСИС:
    type(значение)                — тип значения
    is_number(значение)           — проверка на число
    is_integer(значение)          — проверка на целое
    is_float(значение)            — проверка на float
    is_string(значение)           — проверка на строку
    is_boolean(значение)          — проверка на bool
    to_string(значение)           — в строку
    to_number(значение)           — в число
    is_valid_time(значение [, "формат"]) — проверка времени

ОСОБЕННОСТИ:
    - Все is_* возвращают True/False и работают ПОЭЛЕМЕНТНО для векторов и матриц.
    - to_string / to_number работают ПОЭЛЕМЕНТНО.
    - type возвращает строку с именем типа.
    - is_valid_time проверяет формат времени (не даты).
"""


RU = {
    # ============================================================
    # TYPE — определение типа значения
    # ============================================================
    'type': {
        'name': 'type',
        'category': 'types',
        'signature': 'type(значение)',
        'description': (
            'Возвращает тип значения строкой.\n'
            '  • matrix   — двумерная матрица\n'
            '  • vector   — вектор (1D)\n'
            '  • duckdb   — DuckDBTable (BigData)\n'
            '  • integer  — целое число\n'
            '  • float    — число с плавающей точкой\n'
            '  • string   — строка\n'
            '  • boolean  — true / false\n'
            '  • null     — None\n'
            '  • datetime — дата+время\n'
            '  • date     — дата\n'
            '  • time     — время\n'
            '  • list     — список\n'
            '  • unknown  — неизвестный тип'
        ),
        'examples': [
            'r = type(42)             # "integer"',
            'r = type(3.14)           # "float"',
            'r = type("abc")          # "string"',
            'r = type(true)           # "boolean"',
            'r = type(None)           # "null"',
            'r = type(v)              # "vector"',
            'r = type(m)              # "matrix"',
        ],
        'errors': {
            'TYPE_BAD_SYNTAX': {
                'message': (
                    "type: неверный синтаксис.\n"
                    "  Нужен ровно один аргумент."
                ),
                'wrong': 'type()',
                'right': 'type(42)',
                'explanation': (
                    "type принимает ОДИН аргумент — значение любого типа:\n"
                    "     type(42)             # integer\n"
                    "     type(3.14)           # float\n"
                    "     type(\"abc\")          # string\n"
                    "     type(true)           # boolean\n"
                    "     type(None)           # null\n"
                    "     type(v)              # vector\n"
                    "     type(m)              # matrix\n"
                    "\n"
                    "Неправильно:\n"
                    "     type()\n"
                    "     type(42, 3.14)\n"
                    "\n"
                    "Правильно:\n"
                    "     type(42)"
                ),
                'variants': [
                    'r = type(42)',
                    'r = type(3.14)',
                    'r = type("abc")',
                    'r = type(true)',
                    'r = type(None)',
                    'r = type(v)',
                    'r = type(m)',
                ],
            },
        },
    },

    # ============================================================
    # IS_NUMBER — проверка на число
    # ============================================================
    'is_number': {
        'name': 'is_number',
        'category': 'types',
        'signature': 'is_number(значение)',
        'description': (
            'Проверяет, является ли значение числом (int или float).\n'
            '  • Возвращает True / False.\n'
            '  • Для вектора → вектор True/False.\n'
            '  • Для матрицы → матрица True/False.\n'
            '  • bool НЕ считается числом (true/false → False).\n'
            '  • None → False.'
        ),
        'examples': [
            'r = is_number(42)        # True',
            'r = is_number(3.14)      # True',
            'r = is_number("42")      # False',
            'r = is_number(true)      # False',
            'r = is_number(None)      # False',
            'r = is_number(v)         # вектор True/False',
        ],
        'errors': {
            'IS_NUMBER_BAD_SYNTAX': {
                'message': (
                    "is_number: неверный синтаксис.\n"
                    "  Нужен ровно один аргумент."
                ),
                'wrong': 'is_number()',
                'right': 'is_number(42)',
                'explanation': (
                    "is_number принимает ОДИН аргумент:\n"
                    "     is_number(42)         # True\n"
                    "     is_number(3.14)       # True\n"
                    "     is_number(\"42\")       # False — это строка\n"
                    "     is_number(true)       # False — это bool\n"
                    "     is_number(None)       # False\n"
                    "     is_number(v)          # вектор True/False\n"
                    "\n"
                    "Неправильно:\n"
                    "     is_number()\n"
                    "     is_number(42, 3.14)\n"
                    "\n"
                    "Правильно:\n"
                    "     is_number(42)"
                ),
                'variants': [
                    'r = is_number(42)',
                    'r = is_number(3.14)',
                    'r = is_number("42")',
                    'r = is_number(true)',
                    'r = is_number(v)',
                ],
            },
        },
    },

    # ============================================================
    # IS_INTEGER — проверка на целое число
    # ============================================================
    'is_integer': {
        'name': 'is_integer',
        'category': 'types',
        'signature': 'is_integer(значение)',
        'description': (
            'Проверяет, является ли значение целым числом.\n'
            '  • Возвращает True / False.\n'
            '  • 42 → True, 3.14 → False.\n'
            '  • bool НЕ считается целым (true/false → False).\n'
            '  • None → False.'
        ),
        'examples': [
            'r = is_integer(42)       # True',
            'r = is_integer(3.14)     # False',
            'r = is_integer("42")     # False',
            'r = is_integer(true)     # False',
        ],
        'errors': {
            'IS_INTEGER_BAD_SYNTAX': {
                'message': (
                    "is_integer: неверный синтаксис.\n"
                    "  Нужен ровно один аргумент."
                ),
                'wrong': 'is_integer()',
                'right': 'is_integer(42)',
                'explanation': (
                    "is_integer принимает ОДИН аргумент:\n"
                    "     is_integer(42)        # True\n"
                    "     is_integer(3.14)      # False\n"
                    "     is_integer(\"42\")      # False\n"
                    "     is_integer(true)      # False\n"
                    "\n"
                    "Правильно:\n"
                    "     is_integer(42)"
                ),
                'variants': [
                    'r = is_integer(42)',
                    'r = is_integer(3.14)',
                    'r = is_integer("42")',
                ],
            },
        },
    },

    # ============================================================
    # IS_FLOAT — проверка на float
    # ============================================================
    'is_float': {
        'name': 'is_float',
        'category': 'types',
        'signature': 'is_float(значение)',
        'description': (
            'Проверяет, является ли значение числом с плавающей точкой.\n'
            '  • Возвращает True / False.\n'
            '  • 3.14 → True, 42 → False.'
        ),
        'examples': [
            'r = is_float(3.14)      # True',
            'r = is_float(42)        # False',
            'r = is_float("3.14")    # False',
        ],
        'errors': {
            'IS_FLOAT_BAD_SYNTAX': {
                'message': (
                    "is_float: неверный синтаксис.\n"
                    "  Нужен ровно один аргумент."
                ),
                'wrong': 'is_float()',
                'right': 'is_float(3.14)',
                'explanation': (
                    "is_float принимает ОДИН аргумент:\n"
                    "     is_float(3.14)        # True\n"
                    "     is_float(42)          # False\n"
                    "     is_float(\"3.14\")      # False\n"
                    "\n"
                    "Правильно:\n"
                    "     is_float(3.14)"
                ),
                'variants': [
                    'r = is_float(3.14)',
                    'r = is_float(42)',
                ],
            },
        },
    },

    # ============================================================
    # IS_STRING — проверка на строку
    # ============================================================
    'is_string': {
        'name': 'is_string',
        'category': 'types',
        'signature': 'is_string(значение)',
        'description': (
            'Проверяет, является ли значение строкой.\n'
            '  • Возвращает True / False.\n'
            '  • "abc" → True, 42 → False.'
        ),
        'examples': [
            'r = is_string("abc")    # True',
            'r = is_string(42)       # False',
            'r = is_string("")       # True — пустая строка тоже строка',
        ],
        'errors': {
            'IS_STRING_BAD_SYNTAX': {
                'message': (
                    "is_string: неверный синтаксис.\n"
                    "  Нужен ровно один аргумент."
                ),
                'wrong': 'is_string()',
                'right': 'is_string("abc")',
                'explanation': (
                    "is_string принимает ОДИН аргумент:\n"
                    "     is_string(\"abc\")     # True\n"
                    "     is_string(42)        # False\n"
                    "     is_string(\"\")        # True — пустая строка тоже строка\n"
                    "\n"
                    "Правильно:\n"
                    "     is_string(\"abc\")"
                ),
                'variants': [
                    'r = is_string("abc")',
                    'r = is_string(42)',
                    'r = is_string("")',
                ],
            },
        },
    },

    # ============================================================
    # IS_BOOLEAN — проверка на bool
    # ============================================================
    'is_boolean': {
        'name': 'is_boolean',
        'category': 'types',
        'signature': 'is_boolean(значение)',
        'description': (
            'Проверяет, является ли значение логическим (true/false).\n'
            '  • Возвращает True / False.\n'
            '  • true → True, false → True, 1 → False.'
        ),
        'examples': [
            'r = is_boolean(true)    # True',
            'r = is_boolean(false)   # True',
            'r = is_boolean(1)       # False',
            'r = is_boolean(0)       # False',
        ],
        'errors': {
            'IS_BOOLEAN_BAD_SYNTAX': {
                'message': (
                    "is_boolean: неверный синтаксис.\n"
                    "  Нужен ровно один аргумент."
                ),
                'wrong': 'is_boolean()',
                'right': 'is_boolean(true)',
                'explanation': (
                    "is_boolean принимает ОДИН аргумент:\n"
                    "     is_boolean(true)      # True\n"
                    "     is_boolean(false)     # True\n"
                    "     is_boolean(1)         # False — это число\n"
                    "     is_boolean(0)         # False — это число\n"
                    "\n"
                    "Правильно:\n"
                    "     is_boolean(true)"
                ),
                'variants': [
                    'r = is_boolean(true)',
                    'r = is_boolean(false)',
                    'r = is_boolean(1)',
                ],
            },
        },
    },

    # ============================================================
    # TO_STRING — преобразование в строку
    # ============================================================
    'to_string': {
        'name': 'to_string',
        'category': 'types',
        'signature': 'to_string(значение)',
        'description': (
            'Преобразует значение в строку.\n'
            '  • 42 → "42"\n'
            '  • 3.14 → "3.14"\n'
            '  • true → "True"\n'
            '  • None → "" (пустая строка)\n'
            '  • Работает поэлементно для векторов и матриц.'
        ),
        'examples': [
            'r = to_string(42)             # "42"',
            'r = to_string(3.14)           # "3.14"',
            'r = to_string(true)           # "True"',
            'r = to_string(None)           # ""',
            'm[:, "Код"] = to_string(m[:, "Код"])',
        ],
        'errors': {
            'TO_STRING_BAD_SYNTAX': {
                'message': (
                    "to_string: неверный синтаксис.\n"
                    "  Нужен ровно один аргумент."
                ),
                'wrong': 'to_string()',
                'right': 'to_string(42)',
                'explanation': (
                    "to_string принимает ОДИН аргумент:\n"
                    "     to_string(42)             # \"42\"\n"
                    "     to_string(3.14)           # \"3.14\"\n"
                    "     to_string(true)           # \"True\"\n"
                    "     to_string(None)           # \"\"\n"
                    "     to_string(m[:, \"Код\"])    # вектор строк\n"
                    "\n"
                    "Правильно:\n"
                    "     to_string(42)"
                ),
                'variants': [
                    'r = to_string(42)',
                    'r = to_string(3.14)',
                    'r = to_string(true)',
                    'r = to_string(None)',
                    'm[:, "Код"] = to_string(m[:, "Код"])',
                ],
            },
        },
    },

    # ============================================================
    # TO_NUMBER — преобразование в число
    # ============================================================
    'to_number': {
        'name': 'to_number',
        'category': 'types',
        'signature': 'to_number(значение)',
        'description': (
            'Преобразует значение в число.\n'
            '  • "42" → 42\n'
            '  • "3.14" → 3.14\n'
            '  • Если не число → None.\n'
            '  • Пустая строка → None.\n'
            '  • Работает поэлементно для векторов и матриц.'
        ),
        'examples': [
            'r = to_number("42")          # 42',
            'r = to_number("3.14")        # 3.14',
            'r = to_number("abc")         # None',
            'r = to_number("")            # None',
            'm[:, "Цена"] = to_number(m[:, "Цена"])',
        ],
        'errors': {
            'TO_NUMBER_BAD_SYNTAX': {
                'message': (
                    "to_number: неверный синтаксис.\n"
                    "  Нужен ровно один аргумент."
                ),
                'wrong': 'to_number()',
                'right': 'to_number("42")',
                'explanation': (
                    "to_number принимает ОДИН аргумент:\n"
                    "     to_number(\"42\")          # 42\n"
                    "     to_number(\"3.14\")        # 3.14\n"
                    "     to_number(\"abc\")         # None\n"
                    "     to_number(\"\")            # None\n"
                    "     to_number(m[:, \"Цена\"])   # вектор чисел\n"
                    "\n"
                    "Правильно:\n"
                    "     to_number(\"42\")"
                ),
                'variants': [
                    'r = to_number("42")',
                    'r = to_number("3.14")',
                    'r = to_number("abc")',
                    'm[:, "Цена"] = to_number(m[:, "Цена"])',
                ],
            },
        },
    },

    # ============================================================
    # IS_VALID_TIME — проверка времени
    # ============================================================
    'is_valid_time': {
        'name': 'is_valid_time',
        'category': 'types',
        'signature': 'is_valid_time(данные [, "формат"])',
        'description': (
            'Проверяет, что строка является корректным временем.\n'
            '  • Поддерживает 24-часовой (HH:MM:SS) и 12-часовой (hh:MM AM/PM).\n'
            '  • Автоопределение формата, если не указан.\n'
            '  • None / не-строка / пустая строка → False.\n'
            '  • Дата ("29.09.2026") → False (это не время).\n'
            '  • Работает поэлементно для векторов и срезов.'
        ),
        'examples': [
            'r = is_valid_time("14:30:15")              # True',
            'r = is_valid_time("14:30")                 # True',
            'r = is_valid_time("02:30 PM")              # True',
            'r = is_valid_time("25:99:99")              # False',
            'r = is_valid_time("29.09.2026")            # False',
            'r = is_valid_time(m[:, "Время"])           # вектор',
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
                    "is_valid_time(data [, \"format\"])\n"
                    "\n"
                    "  • data   — строка, вектор или срез\n"
                    "  • format — опционально, строка в кавычках\n"
                    "\n"
                    "Примеры:\n"
                    "     is_valid_time(\"14:30:15\")              — авто\n"
                    "     is_valid_time(\"02:30 PM\")              — авто\n"
                    "     is_valid_time(m[:, \"Время\"], \"HH:MM:SS\")  — явный формат\n"
                    "\n"
                    "Неправильно:\n"
                    "     is_valid_time()\n"
                    "     is_valid_time(\"14:30\", 2)\n"
                    "\n"
                    "Правильно:\n"
                    "     is_valid_time(\"14:30\")"
                ),
                'variants': [
                    'r = is_valid_time("14:30:15")',
                    'r = is_valid_time("02:30 PM")',
                    'r = is_valid_time(m[:, "Время"])',
                    'r = is_valid_time(m[:, "Время"], "HH:MM:SS")',
                ],
            },
            'VALID_TIME_BAD_FORMAT': {
                'message': (
                    "is_valid_time: формат должен быть строкой в кавычках."
                ),
                'wrong': 'is_valid_time("14:30", HH:MM)',
                'right': 'is_valid_time("14:30", "HH:MM")',
                'explanation': (
                    "Формат — СТРОКА В КАВЫЧКАХ:\n"
                    "     is_valid_time(\"14:30\", \"HH:MM\")\n"
                    "     is_valid_time(\"02:30 PM\", \"hh:MM AM\")\n"
                    "\n"
                    "Неправильно:\n"
                    "     is_valid_time(\"14:30\", HH:MM)\n"
                    "\n"
                    "Правильно:\n"
                    "     is_valid_time(\"14:30\", \"HH:MM\")"
                ),
                'variants': [
                    'r = is_valid_time("14:30", "HH:MM")',
                    'r = is_valid_time("02:30 PM", "hh:MM AM")',
                ],
            },
        },
    },
}


EN = {
    # ============================================================
    # TYPE
    # ============================================================
    'type': {
        'name': 'type',
        'category': 'types',
        'signature': 'type(value)',
        'description': (
            'Returns the type of a value as a string.\n'
            '  • matrix   — 2D matrix\n'
            '  • vector   — 1D vector\n'
            '  • duckdb   — DuckDBTable (BigData)\n'
            '  • integer  — whole number\n'
            '  • float    — floating-point number\n'
            '  • string   — string\n'
            '  • boolean  — true / false\n'
            '  • null     — None\n'
            '  • datetime — date+time\n'
            '  • date     — date\n'
            '  • time     — time\n'
            '  • list     — list\n'
            '  • unknown  — unknown type'
        ),
        'examples': [
            'r = type(42)             # "integer"',
            'r = type(3.14)           # "float"',
            'r = type("abc")          # "string"',
            'r = type(true)           # "boolean"',
            'r = type(None)           # "null"',
            'r = type(v)              # "vector"',
            'r = type(m)              # "matrix"',
        ],
        'errors': {
            'TYPE_BAD_SYNTAX': {
                'message': (
                    "type: invalid syntax.\n"
                    "  Exactly one argument is required."
                ),
                'wrong': 'type()',
                'right': 'type(42)',
                'explanation': (
                    "type takes ONE argument — a value of any type:\n"
                    "     type(42)             # integer\n"
                    "     type(3.14)           # float\n"
                    "     type(\"abc\")          # string\n"
                    "     type(true)           # boolean\n"
                    "     type(None)           # null\n"
                    "     type(v)              # vector\n"
                    "     type(m)              # matrix\n"
                    "\n"
                    "Incorrect:\n"
                    "     type()\n"
                    "     type(42, 3.14)\n"
                    "\n"
                    "Correct:\n"
                    "     type(42)"
                ),
                'variants': [
                    'r = type(42)',
                    'r = type(3.14)',
                    'r = type("abc")',
                    'r = type(true)',
                    'r = type(None)',
                    'r = type(v)',
                    'r = type(m)',
                ],
            },
        },
    },

    # ============================================================
    # IS_NUMBER
    # ============================================================
    'is_number': {
        'name': 'is_number',
        'category': 'types',
        'signature': 'is_number(value)',
        'description': (
            'Checks whether a value is a number (int or float).\n'
            '  • Returns True / False.\n'
            '  • For a vector → vector of True/False.\n'
            '  • For a matrix → matrix of True/False.\n'
            '  • bool is NOT a number (true/false → False).\n'
            '  • None → False.'
        ),
        'examples': [
            'r = is_number(42)        # True',
            'r = is_number(3.14)      # True',
            'r = is_number("42")      # False',
            'r = is_number(true)      # False',
            'r = is_number(None)      # False',
            'r = is_number(v)         # vector of True/False',
        ],
        'errors': {
            'IS_NUMBER_BAD_SYNTAX': {
                'message': (
                    "is_number: invalid syntax.\n"
                    "  Exactly one argument is required."
                ),
                'wrong': 'is_number()',
                'right': 'is_number(42)',
                'explanation': (
                    "is_number takes ONE argument:\n"
                    "     is_number(42)         # True\n"
                    "     is_number(3.14)       # True\n"
                    "     is_number(\"42\")       # False — it's a string\n"
                    "     is_number(true)       # False — it's a bool\n"
                    "     is_number(None)       # False\n"
                    "     is_number(v)          # vector of True/False\n"
                    "\n"
                    "Incorrect:\n"
                    "     is_number()\n"
                    "     is_number(42, 3.14)\n"
                    "\n"
                    "Correct:\n"
                    "     is_number(42)"
                ),
                'variants': [
                    'r = is_number(42)',
                    'r = is_number(3.14)',
                    'r = is_number("42")',
                    'r = is_number(true)',
                    'r = is_number(v)',
                ],
            },
        },
    },

    # ============================================================
    # IS_INTEGER
    # ============================================================
    'is_integer': {
        'name': 'is_integer',
        'category': 'types',
        'signature': 'is_integer(value)',
        'description': (
            'Checks whether a value is an integer.\n'
            '  • Returns True / False.\n'
            '  • 42 → True, 3.14 → False.\n'
            '  • bool is NOT an integer (true/false → False).\n'
            '  • None → False.'
        ),
        'examples': [
            'r = is_integer(42)       # True',
            'r = is_integer(3.14)     # False',
            'r = is_integer("42")     # False',
            'r = is_integer(true)     # False',
        ],
        'errors': {
            'IS_INTEGER_BAD_SYNTAX': {
                'message': (
                    "is_integer: invalid syntax.\n"
                    "  Exactly one argument is required."
                ),
                'wrong': 'is_integer()',
                'right': 'is_integer(42)',
                'explanation': (
                    "is_integer takes ONE argument:\n"
                    "     is_integer(42)        # True\n"
                    "     is_integer(3.14)      # False\n"
                    "     is_integer(\"42\")      # False\n"
                    "     is_integer(true)      # False\n"
                    "\n"
                    "Correct:\n"
                    "     is_integer(42)"
                ),
                'variants': [
                    'r = is_integer(42)',
                    'r = is_integer(3.14)',
                    'r = is_integer("42")',
                ],
            },
        },
    },

    # ============================================================
    # IS_FLOAT
    # ============================================================
    'is_float': {
        'name': 'is_float',
        'category': 'types',
        'signature': 'is_float(value)',
        'description': (
            'Checks whether a value is a floating-point number.\n'
            '  • Returns True / False.\n'
            '  • 3.14 → True, 42 → False.'
        ),
        'examples': [
            'r = is_float(3.14)      # True',
            'r = is_float(42)        # False',
            'r = is_float("3.14")    # False',
        ],
        'errors': {
            'IS_FLOAT_BAD_SYNTAX': {
                'message': (
                    "is_float: invalid syntax.\n"
                    "  Exactly one argument is required."
                ),
                'wrong': 'is_float()',
                'right': 'is_float(3.14)',
                'explanation': (
                    "is_float takes ONE argument:\n"
                    "     is_float(3.14)        # True\n"
                    "     is_float(42)          # False\n"
                    "     is_float(\"3.14\")      # False\n"
                    "\n"
                    "Correct:\n"
                    "     is_float(3.14)"
                ),
                'variants': [
                    'r = is_float(3.14)',
                    'r = is_float(42)',
                ],
            },
        },
    },

    # ============================================================
    # IS_STRING
    # ============================================================
    'is_string': {
        'name': 'is_string',
        'category': 'types',
        'signature': 'is_string(value)',
        'description': (
            'Checks whether a value is a string.\n'
            '  • Returns True / False.\n'
            '  • "abc" → True, 42 → False.'
        ),
        'examples': [
            'r = is_string("abc")    # True',
            'r = is_string(42)       # False',
            'r = is_string("")       # True — empty string is still a string',
        ],
        'errors': {
            'IS_STRING_BAD_SYNTAX': {
                'message': (
                    "is_string: invalid syntax.\n"
                    "  Exactly one argument is required."
                ),
                'wrong': 'is_string()',
                'right': 'is_string("abc")',
                'explanation': (
                    "is_string takes ONE argument:\n"
                    "     is_string(\"abc\")     # True\n"
                    "     is_string(42)        # False\n"
                    "     is_string(\"\")        # True\n"
                    "\n"
                    "Correct:\n"
                    "     is_string(\"abc\")"
                ),
                'variants': [
                    'r = is_string("abc")',
                    'r = is_string(42)',
                    'r = is_string("")',
                ],
            },
        },
    },

    # ============================================================
    # IS_BOOLEAN
    # ============================================================
    'is_boolean': {
        'name': 'is_boolean',
        'category': 'types',
        'signature': 'is_boolean(value)',
        'description': (
            'Checks whether a value is a boolean (true/false).\n'
            '  • Returns True / False.\n'
            '  • true → True, false → True, 1 → False.'
        ),
        'examples': [
            'r = is_boolean(true)    # True',
            'r = is_boolean(false)   # True',
            'r = is_boolean(1)       # False',
            'r = is_boolean(0)       # False',
        ],
        'errors': {
            'IS_BOOLEAN_BAD_SYNTAX': {
                'message': (
                    "is_boolean: invalid syntax.\n"
                    "  Exactly one argument is required."
                ),
                'wrong': 'is_boolean()',
                'right': 'is_boolean(true)',
                'explanation': (
                    "is_boolean takes ONE argument:\n"
                    "     is_boolean(true)      # True\n"
                    "     is_boolean(false)     # True\n"
                    "     is_boolean(1)         # False — it's a number\n"
                    "     is_boolean(0)         # False — it's a number\n"
                    "\n"
                    "Correct:\n"
                    "     is_boolean(true)"
                ),
                'variants': [
                    'r = is_boolean(true)',
                    'r = is_boolean(false)',
                    'r = is_boolean(1)',
                ],
            },
        },
    },

    # ============================================================
    # TO_STRING
    # ============================================================
    'to_string': {
        'name': 'to_string',
        'category': 'types',
        'signature': 'to_string(value)',
        'description': (
            'Converts a value to a string.\n'
            '  • 42 → "42"\n'
            '  • 3.14 → "3.14"\n'
            '  • true → "True"\n'
            '  • None → "" (empty string)\n'
            '  • Works element-wise for vectors and matrices.'
        ),
        'examples': [
            'r = to_string(42)             # "42"',
            'r = to_string(3.14)           # "3.14"',
            'r = to_string(true)           # "True"',
            'r = to_string(None)           # ""',
            'm[:, "Code"] = to_string(m[:, "Code"])',
        ],
        'errors': {
            'TO_STRING_BAD_SYNTAX': {
                'message': (
                    "to_string: invalid syntax.\n"
                    "  Exactly one argument is required."
                ),
                'wrong': 'to_string()',
                'right': 'to_string(42)',
                'explanation': (
                    "to_string takes ONE argument:\n"
                    "     to_string(42)             # \"42\"\n"
                    "     to_string(3.14)           # \"3.14\"\n"
                    "     to_string(true)           # \"True\"\n"
                    "     to_string(None)           # \"\"\n"
                    "     to_string(m[:, \"Code\"])   # vector of strings\n"
                    "\n"
                    "Correct:\n"
                    "     to_string(42)"
                ),
                'variants': [
                    'r = to_string(42)',
                    'r = to_string(3.14)',
                    'r = to_string(true)',
                    'r = to_string(None)',
                    'm[:, "Code"] = to_string(m[:, "Code"])',
                ],
            },
        },
    },

    # ============================================================
    # TO_NUMBER
    # ============================================================
    'to_number': {
        'name': 'to_number',
        'category': 'types',
        'signature': 'to_number(value)',
        'description': (
            'Converts a value to a number.\n'
            '  • "42" → 42\n'
            '  • "3.14" → 3.14\n'
            '  • Not a number → None.\n'
            '  • Empty string → None.\n'
            '  • Works element-wise for vectors and matrices.'
        ),
        'examples': [
            'r = to_number("42")          # 42',
            'r = to_number("3.14")        # 3.14',
            'r = to_number("abc")         # None',
            'r = to_number("")            # None',
            'm[:, "Price"] = to_number(m[:, "Price"])',
        ],
        'errors': {
            'TO_NUMBER_BAD_SYNTAX': {
                'message': (
                    "to_number: invalid syntax.\n"
                    "  Exactly one argument is required."
                ),
                'wrong': 'to_number()',
                'right': 'to_number("42")',
                'explanation': (
                    "to_number takes ONE argument:\n"
                    "     to_number(\"42\")          # 42\n"
                    "     to_number(\"3.14\")        # 3.14\n"
                    "     to_number(\"abc\")         # None\n"
                    "     to_number(\"\")            # None\n"
                    "     to_number(m[:, \"Price\"])  # vector of numbers\n"
                    "\n"
                    "Correct:\n"
                    "     to_number(\"42\")"
                ),
                'variants': [
                    'r = to_number("42")',
                    'r = to_number("3.14")',
                    'r = to_number("abc")',
                    'm[:, "Price"] = to_number(m[:, "Price"])',
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
            'Checks that a string is a valid time.\n'
            '  • Supports 24-hour (HH:MM:SS) and 12-hour (hh:MM AM/PM).\n'
            '  • Auto-detects format if not specified.\n'
            '  • None / non-string / empty string → False.\n'
            '  • Date ("29.09.2026") → False (not a time).\n'
            '  • Works element-wise for vectors and slices.'
        ),
        'examples': [
            'r = is_valid_time("14:30:15")              # True',
            'r = is_valid_time("14:30")                 # True',
            'r = is_valid_time("02:30 PM")              # True',
            'r = is_valid_time("25:99:99")              # False',
            'r = is_valid_time("29.09.2026")            # False',
            'r = is_valid_time(m[:, "Time"])            # vector',
            'r = is_valid_time(m[:, "Time"], "HH:MM:SS")',
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
                    "  • data   — string, vector, or slice\n"
                    "  • format — optional, quoted string\n"
                    "\n"
                    "Examples:\n"
                    "     is_valid_time(\"14:30:15\")              — auto\n"
                    "     is_valid_time(\"02:30 PM\")              — auto\n"
                    "     is_valid_time(m[:, \"Time\"], \"HH:MM:SS\")  — explicit\n"
                    "\n"
                    "Incorrect:\n"
                    "     is_valid_time()\n"
                    "     is_valid_time(\"14:30\", 2)\n"
                    "\n"
                    "Correct:\n"
                    "     is_valid_time(\"14:30\")"
                ),
                'variants': [
                    'r = is_valid_time("14:30:15")',
                    'r = is_valid_time("02:30 PM")',
                    'r = is_valid_time(m[:, "Time"])',
                    'r = is_valid_time(m[:, "Time"], "HH:MM:SS")',
                ],
            },
            'VALID_TIME_BAD_FORMAT': {
                'message': (
                    "is_valid_time: format must be a quoted string."
                ),
                'wrong': 'is_valid_time("14:30", HH:MM)',
                'right': 'is_valid_time("14:30", "HH:MM")',
                'explanation': (
                    "Format is a STRING IN QUOTES:\n"
                    "     is_valid_time(\"14:30\", \"HH:MM\")\n"
                    "     is_valid_time(\"02:30 PM\", \"hh:MM AM\")\n"
                    "\n"
                    "Incorrect:\n"
                    "     is_valid_time(\"14:30\", HH:MM)\n"
                    "\n"
                    "Correct:\n"
                    "     is_valid_time(\"14:30\", \"HH:MM\")"
                ),
                'variants': [
                    'r = is_valid_time("14:30", "HH:MM")',
                    'r = is_valid_time("02:30 PM", "hh:MM AM")',
                ],
            },
        },
    },
}