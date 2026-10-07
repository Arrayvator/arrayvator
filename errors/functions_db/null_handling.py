# errors/functions_db/null_handling.py
"""
База ошибок для литерала None и функций работы с None.

ЛИТЕРАЛ:
    None    — единственный правильный способ написать пустое значение.
    null    — ЗАПРЕЩЁН (ошибка BANNED_NULL_LITERAL).
    nan     — ЗАПРЕЩЁН (ошибка BANNED_NAN_LITERAL).

    Регистр НЕ важен: None, none, NONE — всё одно и то же.
    Язык регистронезависимый.

ФУНКЦИИ:
    isnone(x)              — проверить, что x == None
    fillna(data, value)    — заменить None на value
    dropna(data)           — удалить строки, где есть None
    coalesce(a, b, ...)    — первое значение, не равное None
    noneif(value, cond)    — None, если cond == True, иначе value

ИСТОРИЯ:
    Раньше функция называлась null_if — теперь noneif.
    Раньше литерал был null, теперь — None.
"""


RU = {
    # ============================================================
    # ЛИТЕРАЛ NONE — что это и как писать
    # ============================================================
    'none': {
        'name': 'None',
        'category': 'null',
        'signature': 'None',
        'description': (
            'Пустое значение (аналог null / NULL в других языках).\n'
            '  • Пишется как None (регистр не важен: None, none, NONE).\n'
            '  • Проверяется функцией isnone().\n'
            '  • Заменяется функцией fillna().\n'
            '  • Удаляется функцией dropna().\n'
            '  • Первое не-None берётся через coalesce().'
        ),
        'examples': [
            'x = None',
            'r = isnone(None)         # True',
            'm = [1, None, 3]',
            'm = fillna(m, 0)',
            'r = coalesce(None, 5)    # 5',
        ],
        'errors': {
            'BANNED_NULL_LITERAL': {
                'message': (
                    "Слово 'null' в ArrayVator НЕ используется.\n"
                    "  Правильный литерал — None."
                ),
                'wrong': 'x = null',
                'right': 'x = None',
                'explanation': (
                    "В ArrayVator пустое значение называется None.\n"
                    "\n"
                    "Регистр НЕ важен: None, none, NONE — всё одно и то же.\n"
                    "Язык регистронезависимый.\n"
                    "\n"
                    "Но 'null' — это НЕ None. Это слово из других языков:\n"
                    "  • SQL, JavaScript — null\n"
                    "  • Pandas — NaN / nan\n"
                    "  • Go, Ruby — nil\n"
                    "\n"
                    "В ArrayVator используется только None."
                ),
                'variants': [
                    'x = None',
                    'x = none',
                    'x = NONE',
                    'm = [1, None, 3]',
                    'r = isnone(None)              # True',
                    'm = fillna(m, 0)              # None → 0',
                    'r = coalesce(None, 5)         # 5',
                    'm = dropna(m)                 # убрать строки с None',
                ],
            },
            'BANNED_NAN_LITERAL': {
                'message': (
                    "Литерал 'nan' / 'NaN' в ArrayVator НЕ используется.\n"
                    "  Правильный литерал — None."
                ),
                'wrong': 'x = nan',
                'right': 'x = None',
                'explanation': (
                    "В ArrayVator пустое значение — это None.\n"
                    "\n"
                    "Регистр НЕ важен: None, none, NONE — всё одно и то же.\n"
                    "Язык регистронезависимый.\n"
                    "\n"
                    "Никаких nan, NaN, NA, NULL, nil, undefined — только None.\n"
                    "\n"
                    "Проверить значение на пустоту — isnone(x).\n"
                    "Заменить пустоту на число   — fillna(m, 0).\n"
                    "Удалить пустые строки       — dropna(m)."
                ),
                'variants': [
                    'x = None',
                    'x = none',
                    'x = NONE',
                    'r = isnone(None)              # True',
                    'm = fillna(m, 0)              # None → 0',
                    'm = dropna(m)                 # убрать строки с None',
                ],
            },
        },
    },

    # ============================================================
    # ISNONE
    # ============================================================
    'isnone': {
        'name': 'isnone',
        'category': 'null',
        'signature': 'isnone(значение)',
        'description': (
            'Проверка на None.\n'
            '  • Возвращает True, если значение равно None.\n'
            '  • Пустая строка "" — НЕ None.\n'
            '  • Число 0 — НЕ None.\n'
            '  • False — НЕ None.\n'
            '  • Работает со всеми типами.'
        ),
        'examples': [
            'r = isnone(None)         # True',
            'r = isnone(5)            # False',
            'r = isnone("")           # False',
            'r = isnone(0)            # False',
            'r = isnone(false)        # False',
            'r = isnone(m[:, "X"])    # вектор True/False',
        ],
        'errors': {
            'ISNONE_BAD_SYNTAX': {
                'message': (
                    "isnone: неверный синтаксис.\n"
                    "  Нужен ровно один аргумент."
                ),
                'wrong': 'isnone()',
                'right': 'isnone(None)',
                'explanation': (
                    "isnone принимает ОДИН аргумент:\n"
                    "     isnone(значение)\n"
                    "\n"
                    "Проверяет, равно ли значение None."
                ),
                'variants': [
                    'r = isnone(None)',
                    'r = isnone(5)',
                    'r = isnone(m[:, "X"])',
                ],
            },
        },
    },

    # ============================================================
    # FILLNA
    # ============================================================
    'fillna': {
        'name': 'fillna',
        'category': 'null',
        'signature': 'fillna(данные, значение)',
        'description': (
            'Заменяет None указанным значением.\n'
            '  • Работает со скаляром, вектором, матрицей.\n'
            '  • None → указанное значение.\n'
            '  • Остальные значения не трогает.\n'
            '  • Возвращает НОВЫЙ объект — результат нужно сохранить.'
        ),
        'examples': [
            'r = fillna([1, None, 3], 0)',
            'm = fillna(m, 0)',
            'm = fillna(m, "—")',
        ],
        'errors': {
            'FILLNA_BAD_SYNTAX': {
                'message': (
                    "fillna: неверный синтаксис.\n"
                    "  Нужны данные и значение для замены."
                ),
                'wrong': 'fillna(m)',
                'right': 'fillna(m, 0)',
                'explanation': (
                    "fillna принимает ДВА аргумента:\n"
                    "  1. данные\n"
                    "  2. значение, на которое заменить None\n"
                    "\n"
                    "Неправильно:\n"
                    "     fillna(m)\n"
                    "\n"
                    "Правильно:\n"
                    "     fillna(m, 0)\n"
                    '     fillna(m, "—")'
                ),
                'variants': [
                    'r = fillna([1, None, 3], 0)',
                    'm = fillna(m, "—")',
                ],
            },
            'FILLNA_REQUIRES_ASSIGNMENT': {
                'message': (
                    "fillna() возвращает значение — "
                    "результат нужно сохранить."
                ),
                'wrong': 'fillna(m, 0)',
                'right': 'm = fillna(m, 0)',
                'explanation': (
                    "fillna НЕ изменяет исходную матрицу.\n"
                    "Он ВОЗВРАЩАЕТ НОВУЮ.\n"
                    "\n"
                    "Правильно:\n"
                    "  r = fillna(...)      — в новую переменную\n"
                    "  m = fillna(...)      — мутация"
                ),
                'variants': [
                    'r = fillna(m, 0)',
                    'm = fillna(m, 0)',
                ],
            },
        },
    },

    # ============================================================
    # DROPNA
    # ============================================================
    'dropna': {
        'name': 'dropna',
        'category': 'null',
        'signature': 'dropna(данные)',
        'description': (
            'Удаляет строки, содержащие None.\n'
            '  • Для вектора — удаляет None-элементы.\n'
            '  • Для матрицы — удаляет строки, где есть None.\n'
            '  • Возвращает НОВЫЙ объект — результат нужно сохранить.'
        ),
        'examples': [
            'r = dropna([1, None, 3, None, 5])',
            'm = dropna(m)',
        ],
        'errors': {
            'DROPNA_BAD_SYNTAX': {
                'message': (
                    "dropna: неверный синтаксис.\n"
                    "  Нужен ровно один аргумент."
                ),
                'wrong': 'dropna()',
                'right': 'dropna(v)',
                'explanation': (
                    "dropna принимает ОДИН аргумент:\n"
                    "     dropna(данные)\n"
                    "\n"
                    "Правильно:\n"
                    "     dropna(v)\n"
                    "     dropna(m)"
                ),
                'variants': [
                    'r = dropna(v)',
                    'm = dropna(m)',
                ],
            },
            'DROPNA_REQUIRES_ASSIGNMENT': {
                'message': (
                    "dropna() возвращает значение — "
                    "результат нужно сохранить."
                ),
                'wrong': 'dropna(m)',
                'right': 'm = dropna(m)',
                'explanation': (
                    "dropna НЕ изменяет исходную матрицу.\n"
                    "Он ВОЗВРАЩАЕТ НОВУЮ.\n"
                    "\n"
                    "Правильно:\n"
                    "  r = dropna(...)      — в новую переменную\n"
                    "  m = dropna(...)      — мутация"
                ),
                'variants': [
                    'r = dropna(m)',
                    'm = dropna(m)',
                ],
            },
        },
    },

    # ============================================================
    # COALESCE
    # ============================================================
    'coalesce': {
        'name': 'coalesce',
        'category': 'null',
        'signature': 'coalesce(знач1, знач2, ...)',
        'description': (
            'Возвращает первое значение, не равное None.\n'
            '  • Проверяет аргументы слева направо.\n'
            '  • Если все None — возвращает None.\n'
            '  • Принимает 2 и более аргументов.'
        ),
        'examples': [
            'r = coalesce(None, 5)           # 5',
            'r = coalesce(None, None, 10)    # 10',
            'r = coalesce(1, 2, 3)           # 1',
            'r = coalesce(m[:, "Моб"], m[:, "Раб"], m[:, "Дом"])',
        ],
        'errors': {
            'COALESCE_BAD_SYNTAX': {
                'message': (
                    "coalesce: неверный синтаксис.\n"
                    "  Нужно минимум два аргумента."
                ),
                'wrong': 'coalesce(None)',
                'right': 'coalesce(None, 5)',
                'explanation': (
                    "coalesce принимает МИНИМУМ ДВА аргумента:\n"
                    "     coalesce(знач1, знач2, ...)\n"
                    "\n"
                    "Неправильно:\n"
                    "     coalesce(None)\n"
                    "\n"
                    "Правильно:\n"
                    "     coalesce(None, 5)\n"
                    "     coalesce(None, None, 10)\n"
                    "     coalesce(1, 2, 3)"
                ),
                'variants': [
                    'r = coalesce(None, 5)',
                    'r = coalesce(None, None, 10)',
                    'r = coalesce(m[:, "Моб"], m[:, "Раб"], m[:, "Дом"])',
                ],
            },
        },
    },

    # ============================================================
    # NONEIF (бывший null_if)
    # ============================================================
    'noneif': {
        'name': 'noneif',
        'category': 'null',
        'signature': 'noneif(значение, условие)',
        'description': (
            'Возвращает None, если условие истинно.\n'
            '  • Если условие True  → None.\n'
            '  • Если условие False → исходное значение.\n'
            '  • Полезно для замены «магических» чисел на None.\n'
            '  • Раньше называлась null_if — теперь noneif.'
        ),
        'examples': [
            'r = noneif(5, 5 == 5)       # None',
            'r = noneif(5, 5 == 6)       # 5',
            'r = noneif(-1, -1 < 0)      # None',
        ],
        'errors': {
            'NONEIF_BAD_SYNTAX': {
                'message': (
                    "noneif: неверный синтаксис.\n"
                    "  Нужны значение и условие."
                ),
                'wrong': 'noneif(5)',
                'right': 'noneif(5, 5 == 5)',
                'explanation': (
                    "noneif принимает ДВА аргумента:\n"
                    "  1. значение\n"
                    "  2. условие\n"
                    "\n"
                    "Если условие истинно — вернуть None.\n"
                    "Если ложно          — вернуть значение.\n"
                    "\n"
                    "Неправильно:\n"
                    "     noneif(5)\n"
                    "\n"
                    "Правильно:\n"
                    "     noneif(5, 5 == 5)     # None\n"
                    "     noneif(5, 5 == 6)     # 5"
                ),
                'variants': [
                    'r = noneif(5, 5 == 5)',
                    'r = noneif(5, 5 == 6)',
                    'r = noneif(-1, -1 < 0)',
                ],
            },
            'NONEIF_ASSIGN_IN_CONDITION': {
                'message': (
                    "noneif: в условии нужен '==' (сравнение), "
                    "а не '=' (присваивание)."
                ),
                'wrong': 'r = noneif(5, 5 = 5)',
                'right': 'r = noneif(5, 5 == 5)',
                'explanation': (
                    "'=' — присваивание.\n"
                    "'==' — сравнение.\n"
                    "\n"
                    "В условии noneif ВСЕГДА '=='."
                ),
                'variants': [
                    'r = noneif(5, 5 == 5)',
                    'r = noneif(5, x > 10)',
                ],
            },
        },
    },
}


EN = {
    # ============================================================
    # LITERAL NONE — what it is and how to write it
    # ============================================================
    'none': {
        'name': 'None',
        'category': 'null',
        'signature': 'None',
        'description': (
            'Empty value (analog of null / NULL in other languages).\n'
            '  • Written as None (case-insensitive: None, none, NONE).\n'
            '  • Tested by isnone().\n'
            '  • Replaced by fillna().\n'
            '  • Removed by dropna().\n'
            '  • First non-None is taken by coalesce().'
        ),
        'examples': [
            'x = None',
            'r = isnone(None)         # True',
            'm = [1, None, 3]',
            'm = fillna(m, 0)',
            'r = coalesce(None, 5)    # 5',
        ],
        'errors': {
            'BANNED_NULL_LITERAL': {
                'message': (
                    "'null' is NOT used in ArrayVator.\n"
                    "  The correct literal is None."
                ),
                'wrong': 'x = null',
                'right': 'x = None',
                'explanation': (
                    "In ArrayVator, the empty value is called None.\n"
                    "\n"
                    "Case does NOT matter: None, none, NONE are the same.\n"
                    "The language is case-insensitive.\n"
                    "\n"
                    "But 'null' is NOT None. This word comes from other languages:\n"
                    "  • SQL, JavaScript — null\n"
                    "  • Pandas — NaN / nan\n"
                    "  • Go, Ruby — nil\n"
                    "\n"
                    "ArrayVator uses only None."
                ),
                'variants': [
                    'x = None',
                    'x = none',
                    'x = NONE',
                    'm = [1, None, 3]',
                    'r = isnone(None)              # True',
                    'm = fillna(m, 0)              # None → 0',
                    'r = coalesce(None, 5)         # 5',
                    'm = dropna(m)                 # remove rows with None',
                ],
            },
            'BANNED_NAN_LITERAL': {
                'message': (
                    "Literal 'nan' / 'NaN' is NOT used in ArrayVator.\n"
                    "  The correct literal is None."
                ),
                'wrong': 'x = nan',
                'right': 'x = None',
                'explanation': (
                    "In ArrayVator, the empty value is None.\n"
                    "\n"
                    "Case does NOT matter: None, none, NONE are the same.\n"
                    "The language is case-insensitive.\n"
                    "\n"
                    "No nan, NaN, NA, NULL, nil, undefined — only None.\n"
                    "\n"
                    "Check for empty — isnone(x).\n"
                    "Replace empty with a number — fillna(m, 0).\n"
                    "Remove empty rows — dropna(m)."
                ),
                'variants': [
                    'x = None',
                    'x = none',
                    'x = NONE',
                    'r = isnone(None)              # True',
                    'm = fillna(m, 0)              # None → 0',
                    'm = dropna(m)                 # remove rows with None',
                ],
            },
        },
    },

    # ============================================================
    # ISNONE
    # ============================================================
    'isnone': {
        'name': 'isnone',
        'category': 'null',
        'signature': 'isnone(value)',
        'description': (
            'Check for None.\n'
            '  • Returns True if the value equals None.\n'
            '  • Empty string "" — NOT None.\n'
            '  • Number 0 — NOT None.\n'
            '  • False — NOT None.\n'
            '  • Works with all types.'
        ),
        'examples': [
            'r = isnone(None)         # True',
            'r = isnone(5)            # False',
            'r = isnone("")           # False',
            'r = isnone(0)            # False',
            'r = isnone(false)        # False',
            'r = isnone(m[:, "X"])    # vector of True/False',
        ],
        'errors': {
            'ISNONE_BAD_SYNTAX': {
                'message': (
                    "isnone: invalid syntax.\n"
                    "  Exactly one argument is required."
                ),
                'wrong': 'isnone()',
                'right': 'isnone(None)',
                'explanation': (
                    "isnone takes ONE argument:\n"
                    "     isnone(value)\n"
                    "\n"
                    "Checks whether the value is None."
                ),
                'variants': [
                    'r = isnone(None)',
                    'r = isnone(5)',
                    'r = isnone(m[:, "X"])',
                ],
            },
        },
    },

    # ============================================================
    # FILLNA
    # ============================================================
    'fillna': {
        'name': 'fillna',
        'category': 'null',
        'signature': 'fillna(data, value)',
        'description': (
            'Replace None with the given value.\n'
            '  • Works with scalar, vector, matrix.\n'
            '  • None → the given value.\n'
            '  • Other values are not touched.\n'
            '  • Returns a NEW object — save the result.'
        ),
        'examples': [
            'r = fillna([1, None, 3], 0)',
            'm = fillna(m, 0)',
            'm = fillna(m, "-")',
        ],
        'errors': {
            'FILLNA_BAD_SYNTAX': {
                'message': (
                    "fillna: invalid syntax.\n"
                    "  Need data and a value to replace with."
                ),
                'wrong': 'fillna(m)',
                'right': 'fillna(m, 0)',
                'explanation': (
                    "fillna takes TWO arguments:\n"
                    "  1. data\n"
                    "  2. the value to replace None with\n"
                    "\n"
                    "Incorrect:\n"
                    "     fillna(m)\n"
                    "\n"
                    "Correct:\n"
                    "     fillna(m, 0)\n"
                    '     fillna(m, "-")'
                ),
                'variants': [
                    'r = fillna([1, None, 3], 0)',
                    'm = fillna(m, "-")',
                ],
            },
            'FILLNA_REQUIRES_ASSIGNMENT': {
                'message': (
                    "fillna() returns a value — "
                    "the result must be saved."
                ),
                'wrong': 'fillna(m, 0)',
                'right': 'm = fillna(m, 0)',
                'explanation': (
                    "fillna does NOT modify the source matrix.\n"
                    "It RETURNS a NEW one.\n"
                    "\n"
                    "Correct:\n"
                    "  r = fillna(...)      — to a new variable\n"
                    "  m = fillna(...)      — mutation"
                ),
                'variants': [
                    'r = fillna(m, 0)',
                    'm = fillna(m, 0)',
                ],
            },
        },
    },

    # ============================================================
    # DROPNA
    # ============================================================
    'dropna': {
        'name': 'dropna',
        'category': 'null',
        'signature': 'dropna(data)',
        'description': (
            'Remove rows that contain None.\n'
            '  • For a vector — removes None elements.\n'
            '  • For a matrix — removes rows where None occurs.\n'
            '  • Returns a NEW object — save the result.'
        ),
        'examples': [
            'r = dropna([1, None, 3, None, 5])',
            'm = dropna(m)',
        ],
        'errors': {
            'DROPNA_BAD_SYNTAX': {
                'message': (
                    "dropna: invalid syntax.\n"
                    "  Exactly one argument is required."
                ),
                'wrong': 'dropna()',
                'right': 'dropna(v)',
                'explanation': (
                    "dropna takes ONE argument:\n"
                    "     dropna(data)\n"
                    "\n"
                    "Correct:\n"
                    "     dropna(v)\n"
                    "     dropna(m)"
                ),
                'variants': [
                    'r = dropna(v)',
                    'm = dropna(m)',
                ],
            },
            'DROPNA_REQUIRES_ASSIGNMENT': {
                'message': (
                    "dropna() returns a value — "
                    "the result must be saved."
                ),
                'wrong': 'dropna(m)',
                'right': 'm = dropna(m)',
                'explanation': (
                    "dropna does NOT modify the source matrix.\n"
                    "It RETURNS a NEW one.\n"
                    "\n"
                    "Correct:\n"
                    "  r = dropna(...)      — to a new variable\n"
                    "  m = dropna(...)      — mutation"
                ),
                'variants': [
                    'r = dropna(m)',
                    'm = dropna(m)',
                ],
            },
        },
    },

    # ============================================================
    # COALESCE
    # ============================================================
    'coalesce': {
        'name': 'coalesce',
        'category': 'null',
        'signature': 'coalesce(val1, val2, ...)',
        'description': (
            'Returns the first value that is not None.\n'
            '  • Checks arguments left to right.\n'
            '  • If all are None — returns None.\n'
            '  • Takes 2 or more arguments.'
        ),
        'examples': [
            'r = coalesce(None, 5)           # 5',
            'r = coalesce(None, None, 10)    # 10',
            'r = coalesce(1, 2, 3)           # 1',
            'r = coalesce(m[:, "Mob"], m[:, "Work"], m[:, "Home"])',
        ],
        'errors': {
            'COALESCE_BAD_SYNTAX': {
                'message': (
                    "coalesce: invalid syntax.\n"
                    "  At least two arguments are required."
                ),
                'wrong': 'coalesce(None)',
                'right': 'coalesce(None, 5)',
                'explanation': (
                    "coalesce takes AT LEAST TWO arguments:\n"
                    "     coalesce(val1, val2, ...)\n"
                    "\n"
                    "Incorrect:\n"
                    "     coalesce(None)\n"
                    "\n"
                    "Correct:\n"
                    "     coalesce(None, 5)\n"
                    "     coalesce(None, None, 10)\n"
                    "     coalesce(1, 2, 3)"
                ),
                'variants': [
                    'r = coalesce(None, 5)',
                    'r = coalesce(None, None, 10)',
                    'r = coalesce(m[:, "Mob"], m[:, "Work"], m[:, "Home"])',
                ],
            },
        },
    },

    # ============================================================
    # NONEIF (formerly null_if)
    # ============================================================
    'noneif': {
        'name': 'noneif',
        'category': 'null',
        'signature': 'noneif(value, condition)',
        'description': (
            'Returns None if the condition is true.\n'
            '  • If condition is True  → None.\n'
            '  • If condition is False → the value itself.\n'
            '  • Useful to replace "magic" numbers with None.\n'
            '  • Previously called null_if — now noneif.'
        ),
        'examples': [
            'r = noneif(5, 5 == 5)       # None',
            'r = noneif(5, 5 == 6)       # 5',
            'r = noneif(-1, -1 < 0)      # None',
        ],
        'errors': {
            'NONEIF_BAD_SYNTAX': {
                'message': (
                    "noneif: invalid syntax.\n"
                    "  Need a value and a condition."
                ),
                'wrong': 'noneif(5)',
                'right': 'noneif(5, 5 == 5)',
                'explanation': (
                    "noneif takes TWO arguments:\n"
                    "  1. value\n"
                    "  2. condition\n"
                    "\n"
                    "If the condition is true  — return None.\n"
                    "If the condition is false — return the value.\n"
                    "\n"
                    "Incorrect:\n"
                    "     noneif(5)\n"
                    "\n"
                    "Correct:\n"
                    "     noneif(5, 5 == 5)     # None\n"
                    "     noneif(5, 5 == 6)     # 5"
                ),
                'variants': [
                    'r = noneif(5, 5 == 5)',
                    'r = noneif(5, 5 == 6)',
                    'r = noneif(-1, -1 < 0)',
                ],
            },
            'NONEIF_ASSIGN_IN_CONDITION': {
                'message': (
                    "noneif: use '==' (comparison) in the condition, "
                    "not '=' (assignment)."
                ),
                'wrong': 'r = noneif(5, 5 = 5)',
                'right': 'r = noneif(5, 5 == 5)',
                'explanation': (
                    "'=' — assignment.\n"
                    "'==' — comparison.\n"
                    "\n"
                    "In noneif condition ALWAYS use '=='."
                ),
                'variants': [
                    'r = noneif(5, 5 == 5)',
                    'r = noneif(5, x > 10)',
                ],
            },
        },
    },
}