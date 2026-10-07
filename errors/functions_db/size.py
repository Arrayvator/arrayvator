# errors/functions_db/size.py
"""
База ошибок для функций размера: len, lenrow, lencol.

СИНТАКСИС:
    len(значение)        — длина строки / числа / вектора
    lenrow(матрица)      — количество строк
    lencol(матрица)      — количество столбцов

Работает с Matrix и DuckDB.
"""


RU = {
    'len': {
        'name': 'len',
        'category': 'statistics',
        'signature': 'len(значение)',
        'description': (
            'Длина строки / числа / вектора.\n'
            '  • Строка — количество символов.\n'
            '  • Число — количество символов в строковом виде.\n'
            '  • Вектор — количество элементов.\n'
            '  • None → 0.\n'
            '  ⚠️  Для матрицы — ошибка, используйте lenrow() или lencol().'
        ),
        'examples': [
            'r = len("Привет")',
            'r = len(42)',
            'r = len(v)',
        ],
        'errors': {
            'LEN_MATRIX_ERROR': {
                'message': (
                    "len() не работает с двумерной матрицей.\n"
                    "  Используйте lenrow() для строк или lencol() для столбцов."
                ),
                'wrong': 'len(m)',
                'right': 'lenrow(m)',
                'explanation': (
                    "Для матрицы неоднозначно: длина строки или столбца?\n"
                    "\n"
                    "Неправильно:\n"
                    "     len(m)\n"
                    "\n"
                    "Правильно:\n"
                    "     lenrow(m)      — количество строк (включая заголовок)\n"
                    "     lencol(m)      — количество столбцов"
                ),
                'variants': [
                    'r = lenrow(m)',
                    'r = lencol(m)',
                ],
            },
            'LEN_BAD_ARG': {
                'message': (
                    "len: не работает с этим типом."
                ),
                'wrong': 'len(some_bad_type)',
                'right': 'len("Привет")',
                'explanation': (
                    "len работает с:\n"
                    "     строкой — len(\"Привет\")\n"
                    "     числом — len(42)\n"
                    "     вектором — len(v)\n"
                    "     None — len(None)  →  0\n"
                    "\n"
                    "НЕ работает с матрицей — используйте lenrow/lencol."
                ),
                'variants': [
                    'r = len("Привет")',
                    'r = len(42)',
                    'r = len(v)',
                    'r = len(None)',
                ],
            },
        },
    },

    'lenrow': {
        'name': 'lenrow',
        'category': 'statistics',
        'signature': 'lenrow(матрица)',
        'description': (
            'Количество строк.\n'
            '  • Включая заголовок.\n'
            '  • Работает с Matrix и DuckDB.'
        ),
        'examples': [
            'r = lenrow(m)',
            'r = lenrow(v)',
        ],
        'errors': {
            'LENROW_BAD_SYNTAX': {
                'message': (
                    "lenrow: неверный синтаксис.\n"
                    "  Нужен ровно один аргумент."
                ),
                'wrong': 'lenrow()',
                'right': 'lenrow(m)',
                'explanation': (
                    "lenrow принимает ОДИН аргумент:\n"
                    "     lenrow(m)      — матрица\n"
                    "     lenrow(v)      — вектор\n"
                    "\n"
                    "Неправильно:\n"
                    "     lenrow()\n"
                    "\n"
                    "Правильно:\n"
                    "     lenrow(m)"
                ),
                'variants': [
                    'r = lenrow(m)',
                    'r = lenrow(v)',
                ],
            },
            'LENROW_BAD_ARG': {
                'message': (
                    "lenrow: работает только с матрицами и векторами."
                ),
                'wrong': 'lenrow(42)',
                'right': 'lenrow(m)',
                'explanation': (
                    "lenrow работает с:\n"
                    "     матрицей — lenrow(m)\n"
                    "     вектором — lenrow(v)\n"
                    "\n"
                    "Неправильно:\n"
                    "     lenrow(42)\n"
                    "     lenrow(\"text\")\n"
                    "\n"
                    "Правильно:\n"
                    "     lenrow(m)"
                ),
                'variants': [
                    'r = lenrow(m)',
                    'r = lenrow(v)',
                ],
            },
        },
    },

    'lencol': {
        'name': 'lencol',
        'category': 'statistics',
        'signature': 'lencol(матрица)',
        'description': (
            'Количество столбцов.\n'
            '  • Работает с Matrix и DuckDB.\n'
            '  • Для вектора → 1.'
        ),
        'examples': [
            'r = lencol(m)',
            'r = lencol(v)',
        ],
        'errors': {
            'LENCOL_BAD_SYNTAX': {
                'message': (
                    "lencol: неверный синтаксис.\n"
                    "  Нужен ровно один аргумент."
                ),
                'wrong': 'lencol()',
                'right': 'lencol(m)',
                'explanation': (
                    "lencol принимает ОДИН аргумент:\n"
                    "     lencol(m)      — матрица\n"
                    "     lencol(v)      — вектор\n"
                    "\n"
                    "Неправильно:\n"
                    "     lencol()\n"
                    "\n"
                    "Правильно:\n"
                    "     lencol(m)"
                ),
                'variants': [
                    'r = lencol(m)',
                    'r = lencol(v)',
                ],
            },
            'LENCOL_BAD_ARG': {
                'message': (
                    "lencol: работает только с матрицами и векторами."
                ),
                'wrong': 'lencol(42)',
                'right': 'lencol(m)',
                'explanation': (
                    "lencol работает с:\n"
                    "     матрицей — lencol(m)\n"
                    "     вектором — lencol(v)\n"
                    "\n"
                    "Неправильно:\n"
                    "     lencol(42)\n"
                    "     lencol(\"text\")\n"
                    "\n"
                    "Правильно:\n"
                    "     lencol(m)"
                ),
                'variants': [
                    'r = lencol(m)',
                    'r = lencol(v)',
                ],
            },
        },
    },
}


EN = {
    'len': {
        'name': 'len',
        'category': 'statistics',
        'signature': 'len(value)',
        'description': (
            'Length of a string / number / vector.\n'
            '  • String — number of characters.\n'
            '  • Number — number of characters in string form.\n'
            '  • Vector — number of elements.\n'
            '  • None → 0.\n'
            '  ⚠️  For a matrix — error, use lenrow() or lencol().'
        ),
        'examples': [
            'r = len("Hello")',
            'r = len(42)',
            'r = len(v)',
        ],
        'errors': {
            'LEN_MATRIX_ERROR': {
                'message': (
                    "len() does not work with a 2D matrix.\n"
                    "  Use lenrow() for rows or lencol() for columns."
                ),
                'wrong': 'len(m)',
                'right': 'lenrow(m)',
                'explanation': (
                    "For a matrix it's ambiguous: length of row or column?\n"
                    "\n"
                    "Incorrect:\n"
                    "     len(m)\n"
                    "\n"
                    "Correct:\n"
                    "     lenrow(m)      — number of rows (including header)\n"
                    "     lencol(m)      — number of columns"
                ),
                'variants': [
                    'r = lenrow(m)',
                    'r = lencol(m)',
                ],
            },
            'LEN_BAD_ARG': {
                'message': (
                    "len: does not work with this type."
                ),
                'wrong': 'len(some_bad_type)',
                'right': 'len("Hello")',
                'explanation': (
                    "len works with:\n"
                    "     string — len(\"Hello\")\n"
                    "     number — len(42)\n"
                    "     vector — len(v)\n"
                    "     None — len(None)  →  0\n"
                    "\n"
                    "Does NOT work with a matrix — use lenrow/lencol."
                ),
                'variants': [
                    'r = len("Hello")',
                    'r = len(42)',
                    'r = len(v)',
                    'r = len(None)',
                ],
            },
        },
    },

    'lenrow': {
        'name': 'lenrow',
        'category': 'statistics',
        'signature': 'lenrow(matrix)',
        'description': (
            'Number of rows.\n'
            '  • Including header.\n'
            '  • Works with Matrix and DuckDB.'
        ),
        'examples': [
            'r = lenrow(m)',
            'r = lenrow(v)',
        ],
        'errors': {
            'LENROW_BAD_SYNTAX': {
                'message': (
                    "lenrow: invalid syntax.\n"
                    "  Need exactly one argument."
                ),
                'wrong': 'lenrow()',
                'right': 'lenrow(m)',
                'explanation': (
                    "lenrow takes ONE argument:\n"
                    "     lenrow(m)      — matrix\n"
                    "     lenrow(v)      — vector\n"
                    "\n"
                    "Incorrect:\n"
                    "     lenrow()\n"
                    "\n"
                    "Correct:\n"
                    "     lenrow(m)"
                ),
                'variants': [
                    'r = lenrow(m)',
                    'r = lenrow(v)',
                ],
            },
            'LENROW_BAD_ARG': {
                'message': (
                    "lenrow: works only with matrices and vectors."
                ),
                'wrong': 'lenrow(42)',
                'right': 'lenrow(m)',
                'explanation': (
                    "lenrow works with:\n"
                    "     matrix — lenrow(m)\n"
                    "     vector — lenrow(v)\n"
                    "\n"
                    "Incorrect:\n"
                    "     lenrow(42)\n"
                    "     lenrow(\"text\")\n"
                    "\n"
                    "Correct:\n"
                    "     lenrow(m)"
                ),
                'variants': [
                    'r = lenrow(m)',
                    'r = lenrow(v)',
                ],
            },
        },
    },

    'lencol': {
        'name': 'lencol',
        'category': 'statistics',
        'signature': 'lencol(matrix)',
        'description': (
            'Number of columns.\n'
            '  • Works with Matrix and DuckDB.\n'
            '  • For a vector → 1.'
        ),
        'examples': [
            'r = lencol(m)',
            'r = lencol(v)',
        ],
        'errors': {
            'LENCOL_BAD_SYNTAX': {
                'message': (
                    "lencol: invalid syntax.\n"
                    "  Need exactly one argument."
                ),
                'wrong': 'lencol()',
                'right': 'lencol(m)',
                'explanation': (
                    "lencol takes ONE argument:\n"
                    "     lencol(m)      — matrix\n"
                    "     lencol(v)      — vector\n"
                    "\n"
                    "Incorrect:\n"
                    "     lencol()\n"
                    "\n"
                    "Correct:\n"
                    "     lencol(m)"
                ),
                'variants': [
                    'r = lencol(m)',
                    'r = lencol(v)',
                ],
            },
            'LENCOL_BAD_ARG': {
                'message': (
                    "lencol: works only with matrices and vectors."
                ),
                'wrong': 'lencol(42)',
                'right': 'lencol(m)',
                'explanation': (
                    "lencol works with:\n"
                    "     matrix — lencol(m)\n"
                    "     vector — lencol(v)\n"
                    "\n"
                    "Incorrect:\n"
                    "     lencol(42)\n"
                    "     lencol(\"text\")\n"
                    "\n"
                    "Correct:\n"
                    "     lencol(m)"
                ),
                'variants': [
                    'r = lencol(m)',
                    'r = lencol(v)',
                ],
            },
        },
    },
}