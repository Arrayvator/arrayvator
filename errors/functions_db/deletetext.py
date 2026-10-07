# errors/functions_db/deletetext.py
"""
База ошибок для функций deletetextleft и deletetextright.

СИНТАКСИС:
    deletetextleft(данные, N)      — удалить N символов СЛЕВА
    deletetextright(данные, N)     — удалить N символов СПРАВА

Работает с Matrix и DuckDB.
"""


RU = {
    'deletetextleft': {
        'name': 'deletetextleft',
        'category': 'string',
        'signature': 'deletetextleft(данные, N)',
        'description': (
            'Удаляет N символов СЛЕВА от строки.\n'
            '  • Если N >= длины — результат None.\n'
            '  • N должно быть >= 0.\n'
            '  • Работает с Matrix и DuckDB.\n'
            '  • Возвращает НОВУЮ матрицу — результат нужно сохранить.'
        ),
        'examples': [
            'r = deletetextleft("PR-001", 3)',
            'm = deletetextleft(m[:, "Код"], 4)',
        ],
        'errors': {
            'DELETETEXTLEFT_BAD_SYNTAX': {
                'message': (
                    "deletetextleft: неверный синтаксис.\n"
                    "  Нужны данные и N — число символов."
                ),
                'wrong': 'deletetextleft("PR-001")',
                'right': 'deletetextleft("PR-001", 3)',
                'explanation': (
                    "deletetextleft принимает ДВА аргумента:\n"
                    "  1. данные — строка, вектор, срез\n"
                    "  2. N — число символов удалить слева\n"
                    "\n"
                    "Неправильно:\n"
                    "     deletetextleft(\"PR-001\")\n"
                    "\n"
                    "Правильно:\n"
                    "     deletetextleft(\"PR-001\", 3)      — \"001\""
                ),
                'variants': [
                    'r = deletetextleft("PR-001", 3)',
                    'm = deletetextleft(m[:, "Код"], 4)',
                ],
            },
            'DELETETEXTLEFT_NEGATIVE': {
                'message': (
                    "deletetextleft: N не может быть отрицательным."
                ),
                'wrong': 'deletetextleft("PR-001", -1)',
                'right': 'deletetextleft("PR-001", 3)',
                'explanation': (
                    "N — количество символов удалить.\n"
                    "Не может быть отрицательным.\n"
                    "\n"
                    "Неправильно:\n"
                    "     deletetextleft(\"PR-001\", -1)\n"
                    "\n"
                    "Правильно:\n"
                    "     deletetextleft(\"PR-001\", 3)\n"
                    "     deletetextleft(\"PR-001\", 0)     — ничего не удалить"
                ),
                'variants': [
                    'r = deletetextleft("PR-001", 3)',
                    'r = deletetextleft("PR-001", 0)',
                ],
            },
            'DELETETEXTLEFT_BAD_COUNT': {
                'message': (
                    "deletetextleft: N должно быть числом."
                ),
                'wrong': 'deletetextleft("PR-001", "3")',
                'right': 'deletetextleft("PR-001", 3)',
                'explanation': (
                    "N — число БЕЗ кавычек:\n"
                    "     deletetextleft(\"PR-001\", 3)\n"
                    "     deletetextleft(\"PR-001\", 4)\n"
                    "\n"
                    "Неправильно:\n"
                    "     deletetextleft(\"PR-001\", \"3\")\n"
                    "\n"
                    "Правильно:\n"
                    "     deletetextleft(\"PR-001\", 3)"
                ),
                'variants': [
                    'r = deletetextleft("PR-001", 3)',
                    'r = deletetextleft("PR-001", 4)',
                ],
            },
            'DELETETEXTLEFT_REQUIRES_ASSIGNMENT': {
                'message': (
                    "deletetextleft() возвращает значение — "
                    "результат нужно сохранить."
                ),
                'wrong': 'deletetextleft(m[:, "Код"], 3)',
                'right': 'm = deletetextleft(m[:, "Код"], 3)',
                'explanation': (
                    "deletetextleft НЕ изменяет исходную матрицу.\n"
                    "Он ВОЗВРАЩАЕТ НОВУЮ.\n"
                    "\n"
                    "Правильно:\n"
                    "  r = deletetextleft(...)      — в новую переменную\n"
                    "  m = deletetextleft(...)      — мутация"
                ),
                'variants': [
                    'r = deletetextleft(m[:, "Код"], 3)',
                    'm = deletetextleft(m[:, "Код"], 3)',
                ],
            },
        },
    },

    'deletetextright': {
        'name': 'deletetextright',
        'category': 'string',
        'signature': 'deletetextright(данные, N)',
        'description': (
            'Удаляет N символов СПРАВА от строки.\n'
            '  • Если N >= длины — результат None.\n'
            '  • N должно быть >= 0.\n'
            '  • Работает с Matrix и DuckDB.\n'
            '  • Возвращает НОВУЮ матрицу — результат нужно сохранить.'
        ),
        'examples': [
            'r = deletetextright("PR-001", 2)',
            'm = deletetextright(m[:, "Город"], 2)',
        ],
        'errors': {
            'DELETETEXTRIGHT_BAD_SYNTAX': {
                'message': (
                    "deletetextright: неверный синтаксис.\n"
                    "  Нужны данные и N — число символов."
                ),
                'wrong': 'deletetextright("PR-001")',
                'right': 'deletetextright("PR-001", 2)',
                'explanation': (
                    "deletetextright принимает ДВА аргумента:\n"
                    "  1. данные — строка, вектор, срез\n"
                    "  2. N — число символов удалить справа\n"
                    "\n"
                    "Неправильно:\n"
                    "     deletetextright(\"PR-001\")\n"
                    "\n"
                    "Правильно:\n"
                    "     deletetextright(\"PR-001\", 2)      — \"PR-0\""
                ),
                'variants': [
                    'r = deletetextright("PR-001", 2)',
                    'm = deletetextright(m[:, "Город"], 2)',
                ],
            },
            'DELETETEXTRIGHT_NEGATIVE': {
                'message': (
                    "deletetextright: N не может быть отрицательным."
                ),
                'wrong': 'deletetextright("PR-001", -1)',
                'right': 'deletetextright("PR-001", 2)',
                'explanation': (
                    "N — количество символов удалить.\n"
                    "Не может быть отрицательным.\n"
                    "\n"
                    "Неправильно:\n"
                    "     deletetextright(\"PR-001\", -1)\n"
                    "\n"
                    "Правильно:\n"
                    "     deletetextright(\"PR-001\", 2)"
                ),
                'variants': [
                    'r = deletetextright("PR-001", 2)',
                    'r = deletetextright("PR-001", 0)',
                ],
            },
            'DELETETEXTRIGHT_BAD_COUNT': {
                'message': (
                    "deletetextright: N должно быть числом."
                ),
                'wrong': 'deletetextright("PR-001", "2")',
                'right': 'deletetextright("PR-001", 2)',
                'explanation': (
                    "N — число БЕЗ кавычек:\n"
                    "     deletetextright(\"PR-001\", 2)\n"
                    "\n"
                    "Неправильно:\n"
                    "     deletetextright(\"PR-001\", \"2\")\n"
                    "\n"
                    "Правильно:\n"
                    "     deletetextright(\"PR-001\", 2)"
                ),
                'variants': [
                    'r = deletetextright("PR-001", 2)',
                    'r = deletetextright("PR-001", 3)',
                ],
            },
            'DELETETEXTRIGHT_REQUIRES_ASSIGNMENT': {
                'message': (
                    "deletetextright() возвращает значение — "
                    "результат нужно сохранить."
                ),
                'wrong': 'deletetextright(m[:, "Город"], 2)',
                'right': 'm = deletetextright(m[:, "Город"], 2)',
                'explanation': (
                    "deletetextright НЕ изменяет исходную матрицу.\n"
                    "Он ВОЗВРАЩАЕТ НОВУЮ.\n"
                    "\n"
                    "Правильно:\n"
                    "  r = deletetextright(...)      — в новую переменную\n"
                    "  m = deletetextright(...)      — мутация"
                ),
                'variants': [
                    'r = deletetextright(m[:, "Город"], 2)',
                    'm = deletetextright(m[:, "Город"], 2)',
                ],
            },
        },
    },
}


EN = {
    'deletetextleft': {
        'name': 'deletetextleft',
        'category': 'string',
        'signature': 'deletetextleft(data, N)',
        'description': (
            'Remove N characters from the LEFT of a string.\n'
            '  • If N >= length — result is None.\n'
            '  • N must be >= 0.\n'
            '  • Works with Matrix and DuckDB.\n'
            '  • Returns a NEW matrix — save the result.'
        ),
        'examples': [
            'r = deletetextleft("PR-001", 3)',
            'm = deletetextleft(m[:, "Code"], 4)',
        ],
        'errors': {
            'DELETETEXTLEFT_BAD_SYNTAX': {
                'message': (
                    "deletetextleft: invalid syntax.\n"
                    "  Need data and N — number of characters."
                ),
                'wrong': 'deletetextleft("PR-001")',
                'right': 'deletetextleft("PR-001", 3)',
                'explanation': (
                    "deletetextleft takes TWO arguments:\n"
                    "  1. data — string, vector, slice\n"
                    "  2. N — number of characters to remove from the left\n"
                    "\n"
                    "Incorrect:\n"
                    "     deletetextleft(\"PR-001\")\n"
                    "\n"
                    "Correct:\n"
                    "     deletetextleft(\"PR-001\", 3)      — \"001\""
                ),
                'variants': [
                    'r = deletetextleft("PR-001", 3)',
                    'm = deletetextleft(m[:, "Code"], 4)',
                ],
            },
            'DELETETEXTLEFT_NEGATIVE': {
                'message': (
                    "deletetextleft: N cannot be negative."
                ),
                'wrong': 'deletetextleft("PR-001", -1)',
                'right': 'deletetextleft("PR-001", 3)',
                'explanation': (
                    "N — number of characters to remove.\n"
                    "Cannot be negative.\n"
                    "\n"
                    "Incorrect:\n"
                    "     deletetextleft(\"PR-001\", -1)\n"
                    "\n"
                    "Correct:\n"
                    "     deletetextleft(\"PR-001\", 3)\n"
                    "     deletetextleft(\"PR-001\", 0)     — remove nothing"
                ),
                'variants': [
                    'r = deletetextleft("PR-001", 3)',
                    'r = deletetextleft("PR-001", 0)',
                ],
            },
            'DELETETEXTLEFT_BAD_COUNT': {
                'message': (
                    "deletetextleft: N must be a number."
                ),
                'wrong': 'deletetextleft("PR-001", "3")',
                'right': 'deletetextleft("PR-001", 3)',
                'explanation': (
                    "N — number WITHOUT quotes:\n"
                    "     deletetextleft(\"PR-001\", 3)\n"
                    "     deletetextleft(\"PR-001\", 4)\n"
                    "\n"
                    "Incorrect:\n"
                    "     deletetextleft(\"PR-001\", \"3\")\n"
                    "\n"
                    "Correct:\n"
                    "     deletetextleft(\"PR-001\", 3)"
                ),
                'variants': [
                    'r = deletetextleft("PR-001", 3)',
                    'r = deletetextleft("PR-001", 4)',
                ],
            },
            'DELETETEXTLEFT_REQUIRES_ASSIGNMENT': {
                'message': (
                    "deletetextleft() returns a value — "
                    "the result must be saved."
                ),
                'wrong': 'deletetextleft(m[:, "Code"], 3)',
                'right': 'm = deletetextleft(m[:, "Code"], 3)',
                'explanation': (
                    "deletetextleft does NOT modify the source matrix.\n"
                    "It RETURNS a NEW one.\n"
                    "\n"
                    "Correct:\n"
                    "  r = deletetextleft(...)      — to a new variable\n"
                    "  m = deletetextleft(...)      — mutation"
                ),
                'variants': [
                    'r = deletetextleft(m[:, "Code"], 3)',
                    'm = deletetextleft(m[:, "Code"], 3)',
                ],
            },
        },
    },

    'deletetextright': {
        'name': 'deletetextright',
        'category': 'string',
        'signature': 'deletetextright(data, N)',
        'description': (
            'Remove N characters from the RIGHT of a string.\n'
            '  • If N >= length — result is None.\n'
            '  • N must be >= 0.\n'
            '  • Works with Matrix and DuckDB.\n'
            '  • Returns a NEW matrix — save the result.'
        ),
        'examples': [
            'r = deletetextright("PR-001", 2)',
            'm = deletetextright(m[:, "City"], 2)',
        ],
        'errors': {
            'DELETETEXTRIGHT_BAD_SYNTAX': {
                'message': (
                    "deletetextright: invalid syntax.\n"
                    "  Need data and N — number of characters."
                ),
                'wrong': 'deletetextright("PR-001")',
                'right': 'deletetextright("PR-001", 2)',
                'explanation': (
                    "deletetextright takes TWO arguments:\n"
                    "  1. data — string, vector, slice\n"
                    "  2. N — number of characters to remove from the right\n"
                    "\n"
                    "Incorrect:\n"
                    "     deletetextright(\"PR-001\")\n"
                    "\n"
                    "Correct:\n"
                    "     deletetextright(\"PR-001\", 2)      — \"PR-0\""
                ),
                'variants': [
                    'r = deletetextright("PR-001", 2)',
                    'm = deletetextright(m[:, "City"], 2)',
                ],
            },
            'DELETETEXTRIGHT_NEGATIVE': {
                'message': (
                    "deletetextright: N cannot be negative."
                ),
                'wrong': 'deletetextright("PR-001", -1)',
                'right': 'deletetextright("PR-001", 2)',
                'explanation': (
                    "N — number of characters to remove.\n"
                    "Cannot be negative.\n"
                    "\n"
                    "Incorrect:\n"
                    "     deletetextright(\"PR-001\", -1)\n"
                    "\n"
                    "Correct:\n"
                    "     deletetextright(\"PR-001\", 2)"
                ),
                'variants': [
                    'r = deletetextright("PR-001", 2)',
                    'r = deletetextright("PR-001", 0)',
                ],
            },
            'DELETETEXTRIGHT_BAD_COUNT': {
                'message': (
                    "deletetextright: N must be a number."
                ),
                'wrong': 'deletetextright("PR-001", "2")',
                'right': 'deletetextright("PR-001", 2)',
                'explanation': (
                    "N — number WITHOUT quotes:\n"
                    "     deletetextright(\"PR-001\", 2)\n"
                    "\n"
                    "Incorrect:\n"
                    "     deletetextright(\"PR-001\", \"2\")\n"
                    "\n"
                    "Correct:\n"
                    "     deletetextright(\"PR-001\", 2)"
                ),
                'variants': [
                    'r = deletetextright("PR-001", 2)',
                    'r = deletetextright("PR-001", 3)',
                ],
            },
            'DELETETEXTRIGHT_REQUIRES_ASSIGNMENT': {
                'message': (
                    "deletetextright() returns a value — "
                    "the result must be saved."
                ),
                'wrong': 'deletetextright(m[:, "City"], 2)',
                'right': 'm = deletetextright(m[:, "City"], 2)',
                'explanation': (
                    "deletetextright does NOT modify the source matrix.\n"
                    "It RETURNS a NEW one.\n"
                    "\n"
                    "Correct:\n"
                    "  r = deletetextright(...)      — to a new variable\n"
                    "  m = deletetextright(...)      — mutation"
                ),
                'variants': [
                    'r = deletetextright(m[:, "City"], 2)',
                    'm = deletetextright(m[:, "City"], 2)',
                ],
            },
        },
    },
}