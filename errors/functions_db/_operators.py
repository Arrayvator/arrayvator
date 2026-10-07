# errors/functions_db/_operators.py
"""
База ошибок для операторов:
    сравнение:   ==, !=, <, >, <=, >=
    логика:      and, or, not
    арифметика:  +, -, *, /, %, ^, //
    присваивание: =
"""


RU = {
    # ============================================================
    # СРАВНЕНИЕ
    # ============================================================
    'eq': {
        'name': '== (равно)',
        'category': 'operator',
        'signature': 'значение1 == значение2',
        'description': 'Сравнение на равенство.',
        'examples': [
            'if x == 5 then { print("равно") }',
            'r = filterif(m[:, "Отдел"] == "IT")',
        ],
        'errors': {
            'ASSIGN_IN_CONDITION': {
                'message': (
                    "В условии используется '=' (присваивание), "
                    "а нужно '==' (сравнение)."
                ),
                'wrong': 'if x = 5 then',
                'right': 'if x == 5 then',
                'explanation': (
                    "'=' — присваивает значение переменной.\n"
                    "'==' — сравнивает два значения.\n"
                    "\n"
                    "В условии (if, while, filterif, case) "
                    "ВСЕГДА используется '=='."
                ),
                'variants': [
                    'if x == 5 then { print("равно") }',
                    'if m[:, "Отдел"] == "IT" then { ... }',
                    'r = filterif(m[:, "Пол"] == "Ж")',
                    'r = case(m[:, "Возраст"] == 18, "совершеннолетний", "нет")',
                ],
            },
        },
    },
    'ne': {
        'name': '!= (не равно)',
        'category': 'operator',
        'signature': 'значение1 != значение2',
        'description': 'Сравнение на неравенство.',
        'examples': [
            'if x != 5 then { print("не равно") }',
            'r = filterif(m[:, "Отдел"] != "HR")',
        ],
        'errors': {
            'NOT_EQUAL_SYNTAX': {
                'message': (
                    "Оператор 'не равно' пишется как '!=', а не '<>'."
                ),
                'wrong': 'if x <> 5 then',
                'right': 'if x != 5 then',
                'explanation': (
                    "В ArrayVator только один вариант 'не равно' — '!='.\n"
                    "Символы '<>' не используются."
                ),
                'variants': [
                    'if x != 5 then { ... }',
                    'r = filterif(m[:, "Отдел"] != "HR")',
                ],
            },
        },
    },
    'lt': {
        'name': '< (меньше)',
        'category': 'operator',
        'signature': 'значение1 < значение2',
        'description': 'Сравнение «меньше».',
        'examples': [
            'if x < 5 then { ... }',
            'r = filterif(m[:, "Возраст"] < 18)',
        ],
        'errors': {},
    },
    'gt': {
        'name': '> (больше)',
        'category': 'operator',
        'signature': 'значение1 > значение2',
        'description': 'Сравнение «больше».',
        'examples': [
            'if x > 5 then { ... }',
            'r = filterif(m[:, "Возраст"] > 18)',
        ],
        'errors': {},
    },
    'le': {
        'name': '<= (меньше или равно)',
        'category': 'operator',
        'signature': 'значение1 <= значение2',
        'description': 'Сравнение «меньше или равно».',
        'examples': [
            'if x <= 5 then { ... }',
        ],
        'errors': {},
    },
    'ge': {
        'name': '>= (больше или равно)',
        'category': 'operator',
        'signature': 'значение1 >= значение2',
        'description': 'Сравнение «больше или равно».',
        'examples': [
            'if x >= 5 then { ... }',
        ],
        'errors': {},
    },

    # ============================================================
    # ЛОГИКА
    # ============================================================
    'and': {
        'name': 'and (логическое И)',
        'category': 'operator',
        'signature': 'условие1 and условие2',
        'description': (
            'Истинно, если ОБА условия истинны.\n'
            '  • Используется в if, while, filterif, case.'
        ),
        'examples': [
            'if x > 5 and y < 10 then { ... }',
            'r = filterif(m[:, "Отдел"] == "IT" and m[:, "Возраст"] > 25)',
        ],
        'errors': {
            'AND_OPERATOR': {
                'message': (
                    "Логическое И пишется как 'and', а не '&&'."
                ),
                'wrong': 'if x > 5 && y < 10 then',
                'right': 'if x > 5 and y < 10 then',
                'explanation': (
                    "В ArrayVator используются СЛОВА, а не символы:\n"
                    "  'and' — логическое И (оба истинны)\n"
                    "  'or'  — логическое ИЛИ (хотя бы один)\n"
                    "  'not' — логическое НЕ (отрицание)"
                ),
                'variants': [
                    'if x > 5 and y < 10 then { ... }',
                    'r = filterif(m[:, "Отдел"] == "IT" and m[:, "Возраст"] > 25)',
                    'r = applyif(m[:, "Отдел"] == "IT" and m[:, "Возраст"] > 30, m[:, "Статус"] = "VIP")',
                ],
            },
        },
    },
    'or': {
        'name': 'or (логическое ИЛИ)',
        'category': 'operator',
        'signature': 'условие1 or условие2',
        'description': (
            'Истинно, если ХОТЯ БЫ ОДНО условие истинно.'
        ),
        'examples': [
            'if x == 1 or x == 2 then { ... }',
            'r = filterif(m[:, "Отдел"] == "IT" or m[:, "Отдел"] == "HR")',
        ],
        'errors': {
            'OR_OPERATOR': {
                'message': (
                    "Логическое ИЛИ пишется как 'or', а не '||'."
                ),
                'wrong': 'if x > 5 || y < 10 then',
                'right': 'if x > 5 or y < 10 then',
                'explanation': (
                    "В ArrayVator используются СЛОВА:\n"
                    "  'and' — логическое И\n"
                    "  'or'  — логическое ИЛИ\n"
                    "  'not' — логическое НЕ"
                ),
                'variants': [
                    'if x > 5 or y < 10 then { ... }',
                    'r = filterif(m[:, "Отдел"] == "IT" or m[:, "Отдел"] == "HR")',
                ],
            },
        },
    },
    'not': {
        'name': 'not (логическое НЕ)',
        'category': 'operator',
        'signature': 'not условие',
        'description': 'Инвертирует логическое значение.',
        'examples': [
            'if not active then { ... }',
            'r = filterif(not (m[:, "Отдел"] == "IT"))',
        ],
        'errors': {
            'NOT_OPERATOR': {
                'message': (
                    "Логическое НЕ пишется как 'not', а не '!'."
                ),
                'wrong': 'if !active then',
                'right': 'if not active then',
                'explanation': (
                    "В ArrayVator используется слово 'not'.\n"
                    "Символ '!' не работает."
                ),
                'variants': [
                    'if not active then { ... }',
                    'r = filterif(not (m[:, "Отдел"] == "IT"))',
                ],
            },
        },
    },

    # ============================================================
    # АРИФМЕТИКА
    # ============================================================
    'plus': {
        'name': '+ (сложение)',
        'category': 'operator',
        'signature': 'значение1 + значение2',
        'description': (
            'Сложение чисел ИЛИ конкатенация строк.\n'
            '  • Число + Число → Число\n'
            '  • Строка + Строка → Строка\n'
            '  • Число + Строка → Строка (неявное приведение)'
        ),
        'examples': [
            'x = 5 + 3                # 8',
            's = "Hello" + "World"    # "HelloWorld"',
            'm = addcolumn(m, "Сумма", m[:, "A"] + m[:, "B"])',
        ],
        'errors': {
            'PLUS_TYPE_ERROR': {
                'message': (
                    "Нельзя сложить значение с None через '+'."
                ),
                'wrong': 'x = 5 + None',
                'right': 'x = 5 + 3',
                'explanation': (
                    "None нельзя складывать с числами.\n"
                    "Используйте coalesce() или fillna()\n"
                    "для замены None на число."
                ),
                'variants': [
                    'x = 5 + 3',
                    'x = coalesce(m[:, "A"], 0) + coalesce(m[:, "B"], 0)',
                ],
            },
        },
    },
    'minus': {
        'name': '- (вычитание)',
        'category': 'operator',
        'signature': 'значение1 - значение2',
        'description': 'Вычитание чисел.',
        'examples': [
            'x = 10 - 3               # 7',
            'm = addcolumn(m, "Разница", m[:, "A"] - m[:, "B"])',
        ],
        'errors': {},
    },
    'star': {
        'name': '* (умножение)',
        'category': 'operator',
        'signature': 'значение1 * значение2',
        'description': (
            'Умножение чисел ИЛИ повторение строки.\n'
            '  • Число * Число → Число\n'
            '  • Строка * Число → Строка (повтор)'
        ),
        'examples': [
            'x = 5 * 3                # 15',
            's = "ab" * 3             # "ababab"',
        ],
        'errors': {},
    },
    'slash': {
        'name': '/ (деление)',
        'category': 'operator',
        'signature': 'значение1 / значение2',
        'description': (
            'Деление (результат — float).\n'
            '  • 10 / 2 → 5.0\n'
            '  • 10 / 4 → 2.5'
        ),
        'examples': [
            'x = 10 / 4               # 2.5',
        ],
        'errors': {
            'DIVISION_BY_ZERO': {
                'message': "Деление на ноль.",
                'wrong': 'x = 10 / 0',
                'right': 'x = 10 / 2',
                'explanation': (
                    "Деление на 0 возвращает inf (бесконечность).\n"
                    "Программа НЕ падает.\n"
                    "\n"
                    "Если нужно избежать — проверьте знаменатель:\n"
                    "  if d != 0 then { x = a / d } else { x = 0 }"
                ),
                'variants': [
                    'x = 10 / 2',
                    'if d != 0 then { x = a / d } else { x = 0 }',
                ],
            },
        },
    },
    'mod': {
        'name': '% (остаток от деления)',
        'category': 'operator',
        'signature': 'значение1 % значение2',
        'description': 'Остаток от деления.',
        'examples': [
            'x = 10 % 3               # 1',
        ],
        'errors': {},
    },
    'pow': {
        'name': '^ (возведение в степень)',
        'category': 'operator',
        'signature': 'значение1 ^ значение2',
        'description': 'Возведение в степень.',
        'examples': [
            'x = 2 ^ 10               # 1024',
        ],
        'errors': {},
    },
    'floordiv': {
        'name': '// (целочисленное деление)',
        'category': 'operator',
        'signature': 'значение1 // значение2',
        'description': 'Целая часть от деления.',
        'examples': [
            'x = 10 // 3              # 3',
        ],
        'errors': {},
    },

    # ============================================================
    # ПРИСВАИВАНИЕ
    # ============================================================
    'assign': {
        'name': '= (присваивание)',
        'category': 'operator',
        'signature': 'переменная = значение',
        'description': 'Присваивает значение переменной.',
        'examples': [
            'x = 5',
            'm[1, 1] = "ID"',
            'm[:, "X"] = [1, 2, 3]',
        ],
        'errors': {
            'EQ_IN_STATEMENT': {
                'message': (
                    "Для присваивания нужен '=', а не '=='."
                ),
                'wrong': 'x == 5',
                'right': 'x = 5',
                'explanation': (
                    "'=' — присваивает значение.\n"
                    "'==' — сравнивает значения.\n"
                    "\n"
                    "В присваивании ВСЕГДА один '='."
                ),
                'variants': [
                    'x = 5',
                    'm[1, 1] = "ID"',
                    'm[:, "Отдел"] = ["IT", "HR", "Sales"]',
                ],
            },
        },
    },
}


EN = {
    # ============================================================
    # COMPARISON
    # ============================================================
    'eq': {
        'name': '== (equal)',
        'category': 'operator',
        'signature': 'value1 == value2',
        'description': 'Equality comparison.',
        'examples': [
            'if x == 5 then { print("equal") }',
            'r = filterif(m[:, "Department"] == "IT")',
        ],
        'errors': {
            'ASSIGN_IN_CONDITION': {
                'message': (
                    "In condition, '=' (assignment) is used "
                    "instead of '==' (comparison)."
                ),
                'wrong': 'if x = 5 then',
                'right': 'if x == 5 then',
                'explanation': (
                    "'=' — assigns a value.\n"
                    "'==' — compares two values.\n"
                    "\n"
                    "In conditions (if, while, filterif, case) "
                    "ALWAYS use '=='."
                ),
                'variants': [
                    'if x == 5 then { print("equal") }',
                    'r = filterif(m[:, "Gender"] == "F")',
                ],
            },
        },
    },
    'ne': {
        'name': '!= (not equal)',
        'category': 'operator',
        'signature': 'value1 != value2',
        'description': 'Inequality comparison.',
        'examples': [
            'if x != 5 then { print("not equal") }',
            'r = filterif(m[:, "Department"] != "HR")',
        ],
        'errors': {
            'NOT_EQUAL_SYNTAX': {
                'message': (
                    "'Not equal' is written as '!=', not '<>'."
                ),
                'wrong': 'if x <> 5 then',
                'right': 'if x != 5 then',
                'explanation': (
                    "In ArrayVator there is only one form: '!='.\n"
                    "Symbols '<>' are not used."
                ),
            },
        },
    },
    'lt': {
        'name': '< (less than)',
        'category': 'operator',
        'signature': 'value1 < value2',
        'description': '"Less than" comparison.',
        'examples': [
            'if x < 5 then { ... }',
            'r = filterif(m[:, "Age"] < 18)',
        ],
        'errors': {},
    },
    'gt': {
        'name': '> (greater than)',
        'category': 'operator',
        'signature': 'value1 > value2',
        'description': '"Greater than" comparison.',
        'examples': ['if x > 5 then { ... }'],
        'errors': {},
    },
    'le': {
        'name': '<= (less or equal)',
        'category': 'operator',
        'signature': 'value1 <= value2',
        'description': '"Less or equal" comparison.',
        'examples': ['if x <= 5 then { ... }'],
        'errors': {},
    },
    'ge': {
        'name': '>= (greater or equal)',
        'category': 'operator',
        'signature': 'value1 >= value2',
        'description': '"Greater or equal" comparison.',
        'examples': ['if x >= 5 then { ... }'],
        'errors': {},
    },

    # ============================================================
    # LOGIC
    # ============================================================
    'and': {
        'name': 'and (logical AND)',
        'category': 'operator',
        'signature': 'condition1 and condition2',
        'description': (
            'True if BOTH conditions are true.'
        ),
        'examples': [
            'if x > 5 and y < 10 then { ... }',
            'r = filterif(m[:, "Dept"] == "IT" and m[:, "Age"] > 25)',
        ],
        'errors': {
            'AND_OPERATOR': {
                'message': (
                    "Logical AND is written as 'and', not '&&'."
                ),
                'wrong': 'if x > 5 && y < 10 then',
                'right': 'if x > 5 and y < 10 then',
                'explanation': (
                    "ArrayVator uses WORDS, not symbols:\n"
                    "  'and' — logical AND\n"
                    "  'or'  — logical OR\n"
                    "  'not' — logical NOT"
                ),
                'variants': [
                    'if x > 5 and y < 10 then { ... }',
                    'r = filterif(m[:, "Dept"] == "IT" and m[:, "Age"] > 25)',
                ],
            },
        },
    },
    'or': {
        'name': 'or (logical OR)',
        'category': 'operator',
        'signature': 'condition1 or condition2',
        'description': 'True if AT LEAST ONE condition is true.',
        'examples': [
            'if x == 1 or x == 2 then { ... }',
            'r = filterif(m[:, "Dept"] == "IT" or m[:, "Dept"] == "HR")',
        ],
        'errors': {
            'OR_OPERATOR': {
                'message': (
                    "Logical OR is written as 'or', not '||'."
                ),
                'wrong': 'if x > 5 || y < 10 then',
                'right': 'if x > 5 or y < 10 then',
                'explanation': (
                    "ArrayVator uses WORDS:\n"
                    "  'and' — logical AND\n"
                    "  'or'  — logical OR\n"
                    "  'not' — logical NOT"
                ),
            },
        },
    },
    'not': {
        'name': 'not (logical NOT)',
        'category': 'operator',
        'signature': 'not condition',
        'description': 'Inverts a boolean value.',
        'examples': [
            'if not active then { ... }',
        ],
        'errors': {
            'NOT_OPERATOR': {
                'message': (
                    "Logical NOT is written as 'not', not '!'."
                ),
                'wrong': 'if !active then',
                'right': 'if not active then',
                'explanation': (
                    "ArrayVator uses the word 'not'.\n"
                    "Symbol '!' does not work."
                ),
            },
        },
    },

    # ============================================================
    # ARITHMETIC
    # ============================================================
    'plus': {
        'name': '+ (addition)',
        'category': 'operator',
        'signature': 'value1 + value2',
        'description': (
            'Addition of numbers OR string concatenation.'
        ),
        'examples': [
            'x = 5 + 3',
            's = "Hello" + "World"',
        ],
        'errors': {
            'PLUS_TYPE_ERROR': {
                'message': "Cannot add None with '+'.",
                'wrong': 'x = 5 + None',
                'right': 'x = 5 + 3',
                'explanation': (
                    "None cannot be added to numbers.\n"
                    "Use coalesce() or fillna() to replace None."
                ),
            },
        },
    },
    'minus': {
        'name': '- (subtraction)',
        'category': 'operator',
        'signature': 'value1 - value2',
        'description': 'Subtraction of numbers.',
        'examples': ['x = 10 - 3'],
        'errors': {},
    },
    'star': {
        'name': '* (multiplication)',
        'category': 'operator',
        'signature': 'value1 * value2',
        'description': 'Multiplication OR string repetition.',
        'examples': [
            'x = 5 * 3',
            's = "ab" * 3',
        ],
        'errors': {},
    },
    'slash': {
        'name': '/ (division)',
        'category': 'operator',
        'signature': 'value1 / value2',
        'description': 'Division (float result).',
        'examples': ['x = 10 / 4'],
        'errors': {
            'DIVISION_BY_ZERO': {
                'message': "Division by zero.",
                'wrong': 'x = 10 / 0',
                'right': 'x = 10 / 2',
                'explanation': (
                    "Division by 0 returns inf (infinity).\n"
                    "The program does NOT crash."
                ),
            },
        },
    },
    'mod': {
        'name': '% (modulo)',
        'category': 'operator',
        'signature': 'value1 % value2',
        'description': 'Modulo (remainder).',
        'examples': ['x = 10 % 3'],
        'errors': {},
    },
    'pow': {
        'name': '^ (power)',
        'category': 'operator',
        'signature': 'value1 ^ value2',
        'description': 'Power.',
        'examples': ['x = 2 ^ 10'],
        'errors': {},
    },
    'floordiv': {
        'name': '// (integer division)',
        'category': 'operator',
        'signature': 'value1 // value2',
        'description': 'Integer part of division.',
        'examples': ['x = 10 // 3'],
        'errors': {},
    },

    # ============================================================
    # ASSIGNMENT
    # ============================================================
    'assign': {
        'name': '= (assignment)',
        'category': 'operator',
        'signature': 'variable = value',
        'description': 'Assigns a value to a variable.',
        'examples': [
            'x = 5',
            'm[1, 1] = "ID"',
        ],
        'errors': {
            'EQ_IN_STATEMENT': {
                'message': (
                    "For assignment use '=', not '=='."
                ),
                'wrong': 'x == 5',
                'right': 'x = 5',
                'explanation': (
                    "'=' — assigns.\n"
                    "'==' — compares.\n"
                    "\n"
                    "In assignment ALWAYS single '='."
                ),
            },
        },
    },
}