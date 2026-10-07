# errors/functions_db/math.py
"""
База ошибок для математических функций: round, int, frac, frac_digits.

СИНТАКСИС:
    round(значение [, знаков])     — округление
    int(значение)                  — целая часть
    frac(значение [, знаков])      — дробная часть
    frac_digits(значение)          — дробная часть как целое

Работает с числами, векторами, матрицами.
"""


RU = {
    'round': {
        'name': 'round',
        'category': 'math',
        'signature': 'round(значение [, знаков])',
        'description': (
            'Округление чисел.\n'
            '  • Без второго аргумента — до целого.\n'
            '  • Со вторым — до указанного числа знаков.\n'
            '  • Работает с числами, векторами, матрицами.\n'
            '  • Банковское округление (2.5 → 2, 3.5 → 4).'
        ),
        'examples': [
            'r = round(3.14159)',
            'r = round(3.14159, 2)',
            'r = round(v, 2)',
        ],
        'errors': {
            'ROUND_BAD_SYNTAX': {
                'message': (
                    "round: неверный синтаксис.\n"
                    "  Нужно значение и, опционально, число знаков."
                ),
                'wrong': 'round()',
                'right': 'round(3.14)',
                'explanation': (
                    "round принимает 1 или 2 аргумента:\n"
                    "     round(значение)              — до целого\n"
                    "     round(значение, знаков)      — до N знаков\n"
                    "\n"
                    "Неправильно:\n"
                    "     round()\n"
                    "     round(\"text\")\n"
                    "\n"
                    "Правильно:\n"
                    "     round(3.14159)\n"
                    "     round(3.14159, 2)"
                ),
                'variants': [
                    'r = round(3.14159)',
                    'r = round(3.14159, 2)',
                ],
            },
            'ROUND_BAD_DIGITS': {
                'message': (
                    "round: количество знаков должно быть числом."
                ),
                'wrong': 'round(3.14, "2")',
                'right': 'round(3.14, 2)',
                'explanation': (
                    "Второй аргумент — число знаков, БЕЗ кавычек:\n"
                    "     round(3.14, 2)      — 2 знака\n"
                    "     round(3.14, 0)      — целое\n"
                    "\n"
                    "Неправильно:\n"
                    "     round(3.14, \"2\")\n"
                    "\n"
                    "Правильно:\n"
                    "     round(3.14, 2)"
                ),
                'variants': [
                    'r = round(3.14, 2)',
                    'r = round(3.14)',
                ],
            },
        },
    },

    'int': {
        'name': 'int',
        'category': 'math',
        'signature': 'int(значение)',
        'description': (
            'Целая часть числа (отсечение к нулю).\n'
            '  • int(3.7) → 3\n'
            '  • int(-3.7) → -3\n'
            '  • Работает с числами, векторами, матрицами.'
        ),
        'examples': [
            'r = int(3.7)',
            'r = int(-3.7)',
            'r = int(v)',
        ],
        'errors': {
            'INT_BAD_SYNTAX': {
                'message': (
                    "int: неверный синтаксис.\n"
                    "  Нужно ровно одно значение."
                ),
                'wrong': 'int()',
                'right': 'int(3.7)',
                'explanation': (
                    "int принимает ОДИН аргумент:\n"
                    "     int(3.7)      — целая часть\n"
                    "     int(v)        — вектор\n"
                    "\n"
                    "Неправильно:\n"
                    "     int()\n"
                    "     int(3.7, 2)\n"
                    "\n"
                    "Правильно:\n"
                    "     int(3.7)"
                ),
                'variants': [
                    'r = int(3.7)',
                    'r = int(v)',
                ],
            },
        },
    },

    'frac': {
        'name': 'frac',
        'category': 'math',
        'signature': 'frac(значение [, знаков])',
        'description': (
            'Дробная часть числа.\n'
            '  • frac(3.7) → 0.7\n'
            '  • frac(-3.7) → -0.7\n'
            '  • Со вторым аргументом — до указанного числа знаков.\n'
            '  • Работает с числами, векторами, матрицами.'
        ),
        'examples': [
            'r = frac(3.7)',
            'r = frac(-3.7)',
            'r = frac(3.14159, 2)',
        ],
        'errors': {
            'FRAC_BAD_SYNTAX': {
                'message': (
                    "frac: неверный синтаксис.\n"
                    "  Нужно значение и, опционально, число знаков."
                ),
                'wrong': 'frac()',
                'right': 'frac(3.7)',
                'explanation': (
                    "frac принимает 1 или 2 аргумента:\n"
                    "     frac(значение)              — вся дробная часть\n"
                    "     frac(значение, знаков)      — до N знаков\n"
                    "\n"
                    "Неправильно:\n"
                    "     frac()\n"
                    "\n"
                    "Правильно:\n"
                    "     frac(3.7)\n"
                    "     frac(3.14159, 2)"
                ),
                'variants': [
                    'r = frac(3.7)',
                    'r = frac(3.14159, 2)',
                ],
            },
            'FRAC_BAD_DIGITS': {
                'message': (
                    "frac: количество знаков должно быть числом."
                ),
                'wrong': 'frac(3.14, "2")',
                'right': 'frac(3.14, 2)',
                'explanation': (
                    "Второй аргумент — число знаков, БЕЗ кавычек:\n"
                    "     frac(3.14, 2)      — 2 знака\n"
                    "\n"
                    "Неправильно:\n"
                    "     frac(3.14, \"2\")\n"
                    "\n"
                    "Правильно:\n"
                    "     frac(3.14, 2)"
                ),
                'variants': [
                    'r = frac(3.14, 2)',
                    'r = frac(3.14)',
                ],
            },
        },
    },

    'frac_digits': {
        'name': 'frac_digits',
        'category': 'math',
        'signature': 'frac_digits(значение)',
        'description': (
            'Дробная часть как целое число.\n'
            '  • frac_digits(3.456) → 456\n'
            '  • frac_digits(3.14) → 14\n'
            '  • frac_digits(3.0) → 0\n'
            '  • Работает с числами, векторами, матрицами.'
        ),
        'examples': [
            'r = frac_digits(3.456)',
            'r = frac_digits(3.14)',
        ],
        'errors': {
            'FRAC_DIGITS_BAD_SYNTAX': {
                'message': (
                    "frac_digits: неверный синтаксис.\n"
                    "  Нужно ровно одно значение."
                ),
                'wrong': 'frac_digits()',
                'right': 'frac_digits(3.456)',
                'explanation': (
                    "frac_digits принимает ОДИН аргумент:\n"
                    "     frac_digits(3.456)   — 456\n"
                    "     frac_digits(3.14)    — 14\n"
                    "\n"
                    "Неправильно:\n"
                    "     frac_digits()\n"
                    "     frac_digits(3.14, 2)\n"
                    "\n"
                    "Правильно:\n"
                    "     frac_digits(3.456)"
                ),
                'variants': [
                    'r = frac_digits(3.456)',
                    'r = frac_digits(3.14)',
                ],
            },
        },
    },
}


EN = {
    'round': {
        'name': 'round',
        'category': 'math',
        'signature': 'round(value [, digits])',
        'description': (
            'Round numbers.\n'
            '  • Without second argument — to integer.\n'
            '  • With second — to the specified number of digits.\n'
            '  • Works with numbers, vectors, matrices.\n'
            '  • Banker\'s rounding (2.5 → 2, 3.5 → 4).'
        ),
        'examples': [
            'r = round(3.14159)',
            'r = round(3.14159, 2)',
            'r = round(v, 2)',
        ],
        'errors': {
            'ROUND_BAD_SYNTAX': {
                'message': (
                    "round: invalid syntax.\n"
                    "  Need a value and optionally the number of digits."
                ),
                'wrong': 'round()',
                'right': 'round(3.14)',
                'explanation': (
                    "round takes 1 or 2 arguments:\n"
                    "     round(value)              — to integer\n"
                    "     round(value, digits)      — to N digits\n"
                    "\n"
                    "Incorrect:\n"
                    "     round()\n"
                    "     round(\"text\")\n"
                    "\n"
                    "Correct:\n"
                    "     round(3.14159)\n"
                    "     round(3.14159, 2)"
                ),
                'variants': [
                    'r = round(3.14159)',
                    'r = round(3.14159, 2)',
                ],
            },
            'ROUND_BAD_DIGITS': {
                'message': (
                    "round: number of digits must be a number."
                ),
                'wrong': 'round(3.14, "2")',
                'right': 'round(3.14, 2)',
                'explanation': (
                    "Second argument — number of digits, WITHOUT quotes:\n"
                    "     round(3.14, 2)      — 2 digits\n"
                    "     round(3.14, 0)      — integer\n"
                    "\n"
                    "Incorrect:\n"
                    "     round(3.14, \"2\")\n"
                    "\n"
                    "Correct:\n"
                    "     round(3.14, 2)"
                ),
                'variants': [
                    'r = round(3.14, 2)',
                    'r = round(3.14)',
                ],
            },
        },
    },

    'int': {
        'name': 'int',
        'category': 'math',
        'signature': 'int(value)',
        'description': (
            'Integer part of a number (truncation toward zero).\n'
            '  • int(3.7) → 3\n'
            '  • int(-3.7) → -3\n'
            '  • Works with numbers, vectors, matrices.'
        ),
        'examples': [
            'r = int(3.7)',
            'r = int(-3.7)',
            'r = int(v)',
        ],
        'errors': {
            'INT_BAD_SYNTAX': {
                'message': (
                    "int: invalid syntax.\n"
                    "  Need exactly one value."
                ),
                'wrong': 'int()',
                'right': 'int(3.7)',
                'explanation': (
                    "int takes ONE argument:\n"
                    "     int(3.7)      — integer part\n"
                    "     int(v)        — vector\n"
                    "\n"
                    "Incorrect:\n"
                    "     int()\n"
                    "     int(3.7, 2)\n"
                    "\n"
                    "Correct:\n"
                    "     int(3.7)"
                ),
                'variants': [
                    'r = int(3.7)',
                    'r = int(v)',
                ],
            },
        },
    },

    'frac': {
        'name': 'frac',
        'category': 'math',
        'signature': 'frac(value [, digits])',
        'description': (
            'Fractional part of a number.\n'
            '  • frac(3.7) → 0.7\n'
            '  • frac(-3.7) → -0.7\n'
            '  • With second argument — to the specified number of digits.\n'
            '  • Works with numbers, vectors, matrices.'
        ),
        'examples': [
            'r = frac(3.7)',
            'r = frac(-3.7)',
            'r = frac(3.14159, 2)',
        ],
        'errors': {
            'FRAC_BAD_SYNTAX': {
                'message': (
                    "frac: invalid syntax.\n"
                    "  Need a value and optionally the number of digits."
                ),
                'wrong': 'frac()',
                'right': 'frac(3.7)',
                'explanation': (
                    "frac takes 1 or 2 arguments:\n"
                    "     frac(value)              — full fractional part\n"
                    "     frac(value, digits)      — to N digits\n"
                    "\n"
                    "Incorrect:\n"
                    "     frac()\n"
                    "\n"
                    "Correct:\n"
                    "     frac(3.7)\n"
                    "     frac(3.14159, 2)"
                ),
                'variants': [
                    'r = frac(3.7)',
                    'r = frac(3.14159, 2)',
                ],
            },
            'FRAC_BAD_DIGITS': {
                'message': (
                    "frac: number of digits must be a number."
                ),
                'wrong': 'frac(3.14, "2")',
                'right': 'frac(3.14, 2)',
                'explanation': (
                    "Second argument — number of digits, WITHOUT quotes:\n"
                    "     frac(3.14, 2)      — 2 digits\n"
                    "\n"
                    "Incorrect:\n"
                    "     frac(3.14, \"2\")\n"
                    "\n"
                    "Correct:\n"
                    "     frac(3.14, 2)"
                ),
                'variants': [
                    'r = frac(3.14, 2)',
                    'r = frac(3.14)',
                ],
            },
        },
    },

    'frac_digits': {
        'name': 'frac_digits',
        'category': 'math',
        'signature': 'frac_digits(value)',
        'description': (
            'Fractional part as an integer.\n'
            '  • frac_digits(3.456) → 456\n'
            '  • frac_digits(3.14) → 14\n'
            '  • frac_digits(3.0) → 0\n'
            '  • Works with numbers, vectors, matrices.'
        ),
        'examples': [
            'r = frac_digits(3.456)',
            'r = frac_digits(3.14)',
        ],
        'errors': {
            'FRAC_DIGITS_BAD_SYNTAX': {
                'message': (
                    "frac_digits: invalid syntax.\n"
                    "  Need exactly one value."
                ),
                'wrong': 'frac_digits()',
                'right': 'frac_digits(3.456)',
                'explanation': (
                    "frac_digits takes ONE argument:\n"
                    "     frac_digits(3.456)   — 456\n"
                    "     frac_digits(3.14)    — 14\n"
                    "\n"
                    "Incorrect:\n"
                    "     frac_digits()\n"
                    "     frac_digits(3.14, 2)\n"
                    "\n"
                    "Correct:\n"
                    "     frac_digits(3.456)"
                ),
                'variants': [
                    'r = frac_digits(3.456)',
                    'r = frac_digits(3.14)',
                ],
            },
        },
    },
}