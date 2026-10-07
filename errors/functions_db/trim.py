# errors/functions_db/trim.py
"""
База ошибок для функций trim / trimleft / trimright.

СИНТАКСИС:
    trim(данные [, "символы"])         — убрать с ОБЕИХ сторон
    trimleft(данные [, "символы"])     — убрать СЛЕВА
    trimright(данные [, "символы"])    — убрать СПРАВА

Без второго аргумента убираются ВСЕ пробелы (пробел, таб, перевод строки).
Со строкой — только указанные символы.

Работает с Matrix и DuckDB.
"""


RU = {
    'trim': {
        'name': 'trim',
        'category': 'string',
        'signature': 'trim(данные [, "символы"])',
        'description': (
            'Убирает пробелы (или указанные символы) с ОБЕИХ сторон.\n'
            '  • Без аргумента — все whitespace: " \\t\\n\\r".\n'
            '  • Со строкой — только эти символы.\n'
            '  • None → None. Числа не трогает.\n'
            '  • Работает с Matrix и DuckDB (TRIM).'
        ),
        'examples': [
            'r = trim("  hello  ")',
            'm = trim(m[:, "Имя"])',
            'm = trim(m[:, "Телефон"], "+- ()")',
        ],
        'errors': {
            'TRIM_BAD_SYNTAX': {
                'message': (
                    "trim: неверный синтаксис.\n"
                    "  Нужны данные и, опционально, строка символов."
                ),
                'wrong': 'trim()',
                'right': 'trim("  hello  ")',
                'explanation': (
                    "trim принимает 1 или 2 аргумента:\n"
                    "     trim(данные)                 — убрать пробелы\n"
                    "     trim(данные, \"символы\")       — убрать указанные символы\n"
                    "\n"
                    "Неправильно:\n"
                    "     trim()\n"
                    "\n"
                    "Правильно:\n"
                    "     trim(\"  hello  \")\n"
                    "     trim(m[:, \"Имя\"], \"+-\")"
                ),
                'variants': [
                    'r = trim("  hello  ")',
                    'm = trim(m[:, "Имя"])',
                    'm = trim(m[:, "Телефон"], "+- ()")',
                ],
            },
            'TRIM_BAD_CHARS': {
                'message': (
                    "trim: символы должны быть строкой в кавычках."
                ),
                'wrong': 'trim("  hello  ", 0)',
                'right': 'trim("  hello  ", "0")',
                'explanation': (
                    "Строка символов — В КАВЫЧКАХ:\n"
                    "     trim(данные, \"+-\")\n"
                    "     trim(данные, \"0\")\n"
                    "     trim(данные, \".,!? \")\n"
                    "\n"
                    "Неправильно:\n"
                    "     trim(\"  hello  \", 0)\n"
                    "\n"
                    "Правильно:\n"
                    "     trim(\"  hello  \", \"0\")"
                ),
                'variants': [
                    'r = trim("  hello  ")',
                    'm = trim(m[:, "Код"], "0")',
                ],
            },
            'TRIM_REQUIRES_ASSIGNMENT': {
                'message': (
                    "trim() возвращает значение — "
                    "результат нужно сохранить."
                ),
                'wrong': 'trim(m[:, "Имя"])',
                'right': 'm = trim(m[:, "Имя"])',
                'explanation': (
                    "trim НЕ изменяет исходную матрицу.\n"
                    "Он ВОЗВРАЩАЕТ НОВУЮ.\n"
                    "\n"
                    "Правильно:\n"
                    "  r = trim(...)      — в новую переменную\n"
                    "  m = trim(...)      — мутация"
                ),
                'variants': [
                    'r = trim(m[:, "Имя"])',
                    'm = trim(m[:, "Имя"])',
                ],
            },
        },
    },

    'trimleft': {
        'name': 'trimleft',
        'category': 'string',
        'signature': 'trimleft(данные [, "символы"])',
        'description': (
            'Убирает пробелы (или указанные символы) СЛЕВА.\n'
            '  • Без аргумента — все whitespace.\n'
            '  • Со строкой — только эти символы.\n'
            '  • None → None. Числа не трогает.\n'
            '  • Работает с Matrix и DuckDB (LTRIM).'
        ),
        'examples': [
            'r = trimleft("  hello")',
            'm = trimleft(m[:, "Код"], "0")',
        ],
        'errors': {
            'TRIMLEFT_BAD_SYNTAX': {
                'message': (
                    "trimleft: неверный синтаксис.\n"
                    "  Нужны данные и, опционально, строка символов."
                ),
                'wrong': 'trimleft()',
                'right': 'trimleft("  hello")',
                'explanation': (
                    "trimleft принимает 1 или 2 аргумента:\n"
                    "     trimleft(данные)                 — убрать пробелы\n"
                    "     trimleft(данные, \"символы\")       — убрать указанные символы\n"
                    "\n"
                    "Правильно:\n"
                    "     trimleft(\"  hello\")\n"
                    "     trimleft(m[:, \"Код\"], \"0\")"
                ),
                'variants': [
                    'r = trimleft("  hello")',
                    'm = trimleft(m[:, "Код"], "0")',
                ],
            },
            'TRIMLEFT_BAD_CHARS': {
                'message': (
                    "trimleft: символы должны быть строкой в кавычках."
                ),
                'wrong': 'trimleft("  42", 0)',
                'right': 'trimleft("  42", "0")',
                'explanation': (
                    "Строка символов — В КАВЫЧКАХ:\n"
                    "     trimleft(данные, \"0\")\n"
                    "     trimleft(данные, \"+-\")\n"
                    "\n"
                    "Правильно:\n"
                    "     trimleft(\"  42\", \"0\")"
                ),
                'variants': [
                    'r = trimleft("  hello")',
                    'm = trimleft(m[:, "Код"], "0")',
                ],
            },
            'TRIMLEFT_REQUIRES_ASSIGNMENT': {
                'message': (
                    "trimleft() возвращает значение — "
                    "результат нужно сохранить."
                ),
                'wrong': 'trimleft(m[:, "Код"])',
                'right': 'm = trimleft(m[:, "Код"])',
                'explanation': (
                    "trimleft НЕ изменяет исходную матрицу.\n"
                    "Он ВОЗВРАЩАЕТ НОВУЮ.\n"
                    "\n"
                    "Правильно:\n"
                    "  r = trimleft(...)      — в новую переменную\n"
                    "  m = trimleft(...)      — мутация"
                ),
                'variants': [
                    'r = trimleft(m[:, "Код"])',
                    'm = trimleft(m[:, "Код"])',
                ],
            },
        },
    },

    'trimright': {
        'name': 'trimright',
        'category': 'string',
        'signature': 'trimright(данные [, "символы"])',
        'description': (
            'Убирает пробелы (или указанные символы) СПРАВА.\n'
            '  • Без аргумента — все whitespace.\n'
            '  • Со строкой — только эти символы.\n'
            '  • None → None. Числа не трогает.\n'
            '  • Работает с Matrix и DuckDB (RTRIM).'
        ),
        'examples': [
            'r = trimright("hello  ")',
            'm = trimright(m[:, "Хвост"], "0")',
        ],
        'errors': {
            'TRIMRIGHT_BAD_SYNTAX': {
                'message': (
                    "trimright: неверный синтаксис.\n"
                    "  Нужны данные и, опционально, строка символов."
                ),
                'wrong': 'trimright()',
                'right': 'trimright("hello  ")',
                'explanation': (
                    "trimright принимает 1 или 2 аргумента:\n"
                    "     trimright(данные)                 — убрать пробелы\n"
                    "     trimright(данные, \"символы\")       — убрать указанные символы\n"
                    "\n"
                    "Правильно:\n"
                    "     trimright(\"hello  \")\n"
                    "     trimright(m[:, \"Хвост\"], \"0\")"
                ),
                'variants': [
                    'r = trimright("hello  ")',
                    'm = trimright(m[:, "Хвост"], "0")',
                ],
            },
            'TRIMRIGHT_BAD_CHARS': {
                'message': (
                    "trimright: символы должны быть строкой в кавычках."
                ),
                'wrong': 'trimright("42  ", 0)',
                'right': 'trimright("42  ", "0")',
                'explanation': (
                    "Строка символов — В КАВЫЧКАХ:\n"
                    "     trimright(данные, \"0\")\n"
                    "     trimright(данные, \"+-\")\n"
                    "\n"
                    "Правильно:\n"
                    "     trimright(\"42  \", \"0\")"
                ),
                'variants': [
                    'r = trimright("hello  ")',
                    'm = trimright(m[:, "Хвост"], "0")',
                ],
            },
            'TRIMRIGHT_REQUIRES_ASSIGNMENT': {
                'message': (
                    "trimright() возвращает значение — "
                    "результат нужно сохранить."
                ),
                'wrong': 'trimright(m[:, "Хвост"])',
                'right': 'm = trimright(m[:, "Хвост"])',
                'explanation': (
                    "trimright НЕ изменяет исходную матрицу.\n"
                    "Он ВОЗВРАЩАЕТ НОВУЮ.\n"
                    "\n"
                    "Правильно:\n"
                    "  r = trimright(...)      — в новую переменную\n"
                    "  m = trimright(...)      — мутация"
                ),
                'variants': [
                    'r = trimright(m[:, "Хвост"])',
                    'm = trimright(m[:, "Хвост"])',
                ],
            },
        },
    },
}


EN = {
    'trim': {
        'name': 'trim',
        'category': 'string',
        'signature': 'trim(data [, "chars"])',
        'description': (
            'Remove spaces (or given characters) from BOTH sides.\n'
            '  • No argument — all whitespace: " \\t\\n\\r".\n'
            '  • With string — only these characters.\n'
            '  • None → None. Numbers are not touched.\n'
            '  • Works with Matrix and DuckDB (TRIM).'
        ),
        'examples': [
            'r = trim("  hello  ")',
            'm = trim(m[:, "Name"])',
            'm = trim(m[:, "Phone"], "+- ()")',
        ],
        'errors': {
            'TRIM_BAD_SYNTAX': {
                'message': (
                    "trim: invalid syntax.\n"
                    "  Need data and optionally a character string."
                ),
                'wrong': 'trim()',
                'right': 'trim("  hello  ")',
                'explanation': (
                    "trim takes 1 or 2 arguments:\n"
                    "     trim(data)                 — remove spaces\n"
                    "     trim(data, \"chars\")        — remove given characters\n"
                    "\n"
                    "Incorrect:\n"
                    "     trim()\n"
                    "\n"
                    "Correct:\n"
                    "     trim(\"  hello  \")\n"
                    "     trim(m[:, \"Name\"], \"+-\")"
                ),
                'variants': [
                    'r = trim("  hello  ")',
                    'm = trim(m[:, "Name"])',
                    'm = trim(m[:, "Phone"], "+- ()")',
                ],
            },
            'TRIM_BAD_CHARS': {
                'message': (
                    "trim: chars must be a string in quotes."
                ),
                'wrong': 'trim("  hello  ", 0)',
                'right': 'trim("  hello  ", "0")',
                'explanation': (
                    "Character string is IN QUOTES:\n"
                    "     trim(data, \"+-\")\n"
                    "     trim(data, \"0\")\n"
                    "     trim(data, \".,!? \")\n"
                    "\n"
                    "Incorrect:\n"
                    "     trim(\"  hello  \", 0)\n"
                    "\n"
                    "Correct:\n"
                    "     trim(\"  hello  \", \"0\")"
                ),
                'variants': [
                    'r = trim("  hello  ")',
                    'm = trim(m[:, "Code"], "0")',
                ],
            },
            'TRIM_REQUIRES_ASSIGNMENT': {
                'message': (
                    "trim() returns a value — "
                    "the result must be saved."
                ),
                'wrong': 'trim(m[:, "Name"])',
                'right': 'm = trim(m[:, "Name"])',
                'explanation': (
                    "trim does NOT modify the source matrix.\n"
                    "It RETURNS a NEW one.\n"
                    "\n"
                    "Correct:\n"
                    "  r = trim(...)      — to a new variable\n"
                    "  m = trim(...)      — mutation"
                ),
                'variants': [
                    'r = trim(m[:, "Name"])',
                    'm = trim(m[:, "Name"])',
                ],
            },
        },
    },

    'trimleft': {
        'name': 'trimleft',
        'category': 'string',
        'signature': 'trimleft(data [, "chars"])',
        'description': (
            'Remove spaces (or given characters) from the LEFT.\n'
            '  • No argument — all whitespace.\n'
            '  • With string — only these characters.\n'
            '  • None → None. Numbers are not touched.\n'
            '  • Works with Matrix and DuckDB (LTRIM).'
        ),
        'examples': [
            'r = trimleft("  hello")',
            'm = trimleft(m[:, "Code"], "0")',
        ],
        'errors': {
            'TRIMLEFT_BAD_SYNTAX': {
                'message': (
                    "trimleft: invalid syntax.\n"
                    "  Need data and optionally a character string."
                ),
                'wrong': 'trimleft()',
                'right': 'trimleft("  hello")',
                'explanation': (
                    "trimleft takes 1 or 2 arguments:\n"
                    "     trimleft(data)                 — remove spaces\n"
                    "     trimleft(data, \"chars\")        — remove given characters\n"
                    "\n"
                    "Correct:\n"
                    "     trimleft(\"  hello\")\n"
                    "     trimleft(m[:, \"Code\"], \"0\")"
                ),
                'variants': [
                    'r = trimleft("  hello")',
                    'm = trimleft(m[:, "Code"], "0")',
                ],
            },
            'TRIMLEFT_BAD_CHARS': {
                'message': (
                    "trimleft: chars must be a string in quotes."
                ),
                'wrong': 'trimleft("  42", 0)',
                'right': 'trimleft("  42", "0")',
                'explanation': (
                    "Character string is IN QUOTES:\n"
                    "     trimleft(data, \"0\")\n"
                    "     trimleft(data, \"+-\")\n"
                    "\n"
                    "Correct:\n"
                    "     trimleft(\"  42\", \"0\")"
                ),
                'variants': [
                    'r = trimleft("  hello")',
                    'm = trimleft(m[:, "Code"], "0")',
                ],
            },
            'TRIMLEFT_REQUIRES_ASSIGNMENT': {
                'message': (
                    "trimleft() returns a value — "
                    "the result must be saved."
                ),
                'wrong': 'trimleft(m[:, "Code"])',
                'right': 'm = trimleft(m[:, "Code"])',
                'explanation': (
                    "trimleft does NOT modify the source matrix.\n"
                    "It RETURNS a NEW one.\n"
                    "\n"
                    "Correct:\n"
                    "  r = trimleft(...)      — to a new variable\n"
                    "  m = trimleft(...)      — mutation"
                ),
                'variants': [
                    'r = trimleft(m[:, "Code"])',
                    'm = trimleft(m[:, "Code"])',
                ],
            },
        },
    },

    'trimright': {
        'name': 'trimright',
        'category': 'string',
        'signature': 'trimright(data [, "chars"])',
        'description': (
            'Remove spaces (or given characters) from the RIGHT.\n'
            '  • No argument — all whitespace.\n'
            '  • With string — only these characters.\n'
            '  • None → None. Numbers are not touched.\n'
            '  • Works with Matrix and DuckDB (RTRIM).'
        ),
        'examples': [
            'r = trimright("hello  ")',
            'm = trimright(m[:, "Tail"], "0")',
        ],
        'errors': {
            'TRIMRIGHT_BAD_SYNTAX': {
                'message': (
                    "trimright: invalid syntax.\n"
                    "  Need data and optionally a character string."
                ),
                'wrong': 'trimright()',
                'right': 'trimright("hello  ")',
                'explanation': (
                    "trimright takes 1 or 2 arguments:\n"
                    "     trimright(data)                 — remove spaces\n"
                    "     trimright(data, \"chars\")        — remove given characters\n"
                    "\n"
                    "Correct:\n"
                    "     trimright(\"hello  \")\n"
                    "     trimright(m[:, \"Tail\"], \"0\")"
                ),
                'variants': [
                    'r = trimright("hello  ")',
                    'm = trimright(m[:, "Tail"], "0")',
                ],
            },
            'TRIMRIGHT_BAD_CHARS': {
                'message': (
                    "trimright: chars must be a string in quotes."
                ),
                'wrong': 'trimright("42  ", 0)',
                'right': 'trimright("42  ", "0")',
                'explanation': (
                    "Character string is IN QUOTES:\n"
                    "     trimright(data, \"0\")\n"
                    "     trimright(data, \"+-\")\n"
                    "\n"
                    "Correct:\n"
                    "     trimright(\"42  \", \"0\")"
                ),
                'variants': [
                    'r = trimright("hello  ")',
                    'm = trimright(m[:, "Tail"], "0")',
                ],
            },
            'TRIMRIGHT_REQUIRES_ASSIGNMENT': {
                'message': (
                    "trimright() returns a value — "
                    "the result must be saved."
                ),
                'wrong': 'trimright(m[:, "Tail"])',
                'right': 'm = trimright(m[:, "Tail"])',
                'explanation': (
                    "trimright does NOT modify the source matrix.\n"
                    "It RETURNS a NEW one.\n"
                    "\n"
                    "Correct:\n"
                    "  r = trimright(...)      — to a new variable\n"
                    "  m = trimright(...)      — mutation"
                ),
                'variants': [
                    'r = trimright(m[:, "Tail"])',
                    'm = trimright(m[:, "Tail"])',
                ],
            },
        },
    },
}