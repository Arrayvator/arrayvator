# errors/functions_db/statistical.py
"""
База ошибок для статистических функций:
    sum, min, max, avg,
    count, median, std.

У КАЖДОЙ ФУНКЦИИ ДВА РЕЖИМА:
    Без by → скаляр.
    С by   → вектор по группам.

ЭТОТ ФАЙЛ — только данные (словари RU и EN).
Никаких классов, импортов, функций.
"""


RU = {
    # ============================================================
    # SUM
    # ============================================================
    'sum': {
        'name': 'sum',
        'category': 'statistics',
        'signature': 'sum(значение [, by m[:, "X"]])',
        'description': (
            'Сумма чисел.\n'
            '  • Работает с вектором, матрицей, срезом.\n'
            '  • Работает с Matrix и DuckDB.\n'
            '  • None, строки, bool — игнорируются.\n'
            '  • Пустой ввод → 0.\n'
            '  • Без by — одно число.\n'
            '  • С by — вектор: сумма группы для каждой строки.'
        ),
        'examples': [
            'r = sum(v)',
            'r = sum(m[:, "Зарплата"])',
            'r = sum(m[:, "Зарплата"], by m[:, "Отдел"])',
            'r = sum(m)',
        ],
        'errors': {
            'SUM_BAD_SYNTAX': {
                'message': (
                    "sum: неверный синтаксис.\n"
                    "  Нужен ровно один аргумент (или аргумент + by)."
                ),
                'wrong': 'sum()',
                'right': 'sum(v)',
                'explanation': (
                    "sum принимает 1 или 2 аргумента:\n"
                    "     sum(v)                                        — скаляр\n"
                    "     sum(m[:, \"Зарплата\"])                       — скаляр\n"
                    "     sum(m[:, \"Зарплата\"], by m[:, \"Отдел\"])     — вектор\n"
                    "\n"
                    "Неправильно:\n"
                    "     sum()\n"
                    "     sum(v, m)\n"
                    "\n"
                    "Правильно:\n"
                    "     sum(v)\n"
                    "     sum(v, by m[:, \"Отдел\"])"
                ),
                'variants': [
                    'r = sum(v)',
                    'r = sum(m[:, "Зарплата"])',
                    'r = sum(m[:, "Зарплата"], by m[:, "Отдел"])',
                ],
            },
            'SUM_NEED_BY': {
                'message': (
                    "sum: после запятой ожидается ключевое слово 'by'."
                ),
                'wrong': 'sum(m[:, "Зарплата"], m[:, "Отдел"])',
                'right': 'sum(m[:, "Зарплата"], by m[:, "Отдел"])',
                'explanation': (
                    "Если указана запятая — вторым аргументом должно идти\n"
                    "'by m[:, \"X\"]'.\n"
                    "\n"
                    "Неправильно:\n"
                    "     sum(m[:, \"Зарплата\"], m[:, \"Отдел\"])\n"
                    "\n"
                    "Правильно:\n"
                    "     sum(m[:, \"Зарплата\"], by m[:, \"Отдел\"])"
                ),
                'variants': [
                    'r = sum(m[:, "Зарплата"], by m[:, "Отдел"])',
                ],
            },
            'SUM_BAD_BY': {
                'message': (
                    "sum: by должен быть срезом m[:, \"X\"]."
                ),
                'wrong': 'sum(m[:, "Зарплата"], by "Отдел")',
                'right': 'sum(m[:, "Зарплата"], by m[:, "Отдел"])',
                'explanation': (
                    "by принимает СРЕЗ столбца:\n"
                    "     by m[:, \"Отдел\"]\n"
                    "     by m[:, 3]\n"
                    "\n"
                    "Неправильно:\n"
                    "     by \"Отдел\"\n"
                    "     by 3"
                ),
                'variants': [
                    'r = sum(m[:, "Зарплата"], by m[:, "Отдел"])',
                    'r = sum(m[:, "Зарплата"], by m[:, 3])',
                ],
            },
            'SUM_BAD_ARG': {
                'message': (
                    "sum: нельзя применить к этому типу."
                ),
                'wrong': 'sum(None)',
                'right': 'sum(v)',
                'explanation': (
                    "sum работает с числами, векторами, матрицами:\n"
                    "     sum(v)                       — вектор\n"
                    "     sum(m)                       — матрица\n"
                    "     sum(m[:, \"X\"])              — срез\n"
                    "\n"
                    "Неправильно:\n"
                    "     sum(None)\n"
                    "     sum(\"text\")\n"
                    "\n"
                    "Правильно:\n"
                    "     sum(v)"
                ),
                'variants': [
                    'r = sum(v)',
                    'r = sum(m)',
                ],
            },
        },
    },

    # ============================================================
    # MIN
    # ============================================================
    'min': {
        'name': 'min',
        'category': 'statistics',
        'signature': 'min(значение [, by m[:, "X"]])',
        'description': (
            'Минимум среди чисел.\n'
            '  • Без by — одно число.\n'
            '  • С by — вектор: минимум группы для каждой строки.'
        ),
        'examples': [
            'r = min(v)',
            'r = min(m[:, "Зарплата"])',
            'r = min(m[:, "Зарплата"], by m[:, "Отдел"])',
        ],
        'errors': {
            'MIN_BAD_SYNTAX': {
                'message': (
                    "min: неверный синтаксис.\n"
                    "  Нужен ровно один аргумент (или аргумент + by)."
                ),
                'wrong': 'min()',
                'right': 'min(v)',
                'explanation': (
                    "min принимает 1 или 2 аргумента:\n"
                    "     min(v)                                 — скаляр\n"
                    "     min(m[:, \"Зарплата\"])                — скаляр\n"
                    "     min(m[:, \"Зарплата\"], by m[:, \"Отдел\"]) — вектор"
                ),
                'variants': [
                    'r = min(v)',
                    'r = min(m[:, "Зарплата"])',
                    'r = min(m[:, "Зарплата"], by m[:, "Отдел"])',
                ],
            },
            'MIN_NEED_BY': {
                'message': (
                    "min: после запятой ожидается ключевое слово 'by'."
                ),
                'wrong': 'min(m[:, "Зарплата"], m[:, "Отдел"])',
                'right': 'min(m[:, "Зарплата"], by m[:, "Отдел"])',
                'explanation': (
                    "Если указана запятая — вторым аргументом должно идти\n"
                    "'by m[:, \"X\"]'."
                ),
                'variants': [
                    'r = min(m[:, "Зарплата"], by m[:, "Отдел"])',
                ],
            },
            'MIN_BAD_BY': {
                'message': 'min: by должен быть срезом m[:, "X"].',
                'wrong': 'min(m[:, "Зарплата"], by "Отдел")',
                'right': 'min(m[:, "Зарплата"], by m[:, "Отдел"])',
                'explanation': (
                    "by принимает СРЕЗ столбца:\n"
                    "     by m[:, \"Отдел\"]"
                ),
                'variants': [
                    'r = min(m[:, "Зарплата"], by m[:, "Отдел"])',
                ],
            },
            'MIN_BAD_ARG': {
                'message': 'min: нельзя применить к этому типу.',
                'wrong': 'min(None)',
                'right': 'min(v)',
                'explanation': (
                    "min работает с числами, векторами, матрицами."
                ),
                'variants': [
                    'r = min(v)',
                    'r = min(m)',
                ],
            },
        },
    },

    # ============================================================
    # MAX
    # ============================================================
    'max': {
        'name': 'max',
        'category': 'statistics',
        'signature': 'max(значение [, by m[:, "X"]])',
        'description': (
            'Максимум среди чисел.\n'
            '  • Без by — одно число.\n'
            '  • С by — вектор: максимум группы для каждой строки.'
        ),
        'examples': [
            'r = max(v)',
            'r = max(m[:, "Зарплата"])',
            'r = max(m[:, "Зарплата"], by m[:, "Отдел"])',
        ],
        'errors': {
            'MAX_BAD_SYNTAX': {
                'message': (
                    "max: неверный синтаксис.\n"
                    "  Нужен ровно один аргумент (или аргумент + by)."
                ),
                'wrong': 'max()',
                'right': 'max(v)',
                'explanation': (
                    "max принимает 1 или 2 аргумента:\n"
                    "     max(v)                                 — скаляр\n"
                    "     max(m[:, \"Зарплата\"], by m[:, \"Отдел\"]) — вектор"
                ),
                'variants': [
                    'r = max(v)',
                    'r = max(m[:, "Зарплата"])',
                    'r = max(m[:, "Зарплата"], by m[:, "Отдел"])',
                ],
            },
            'MAX_NEED_BY': {
                'message': (
                    "max: после запятой ожидается ключевое слово 'by'."
                ),
                'wrong': 'max(m[:, "Зарплата"], m[:, "Отдел"])',
                'right': 'max(m[:, "Зарплата"], by m[:, "Отдел"])',
                'explanation': (
                    "Если указана запятая — вторым аргументом должно идти\n"
                    "'by m[:, \"X\"]'."
                ),
                'variants': [
                    'r = max(m[:, "Зарплата"], by m[:, "Отдел"])',
                ],
            },
            'MAX_BAD_BY': {
                'message': 'max: by должен быть срезом m[:, "X"].',
                'wrong': 'max(m[:, "Зарплата"], by "Отдел")',
                'right': 'max(m[:, "Зарплата"], by m[:, "Отдел"])',
                'explanation': (
                    "by принимает СРЕЗ столбца:\n"
                    "     by m[:, \"Отдел\"]"
                ),
                'variants': [
                    'r = max(m[:, "Зарплата"], by m[:, "Отдел"])',
                ],
            },
            'MAX_BAD_ARG': {
                'message': 'max: нельзя применить к этому типу.',
                'wrong': 'max(None)',
                'right': 'max(v)',
                'explanation': (
                    "max работает с числами, векторами, матрицами."
                ),
                'variants': [
                    'r = max(v)',
                    'r = max(m)',
                ],
            },
        },
    },

    # ============================================================
    # AVG
    # ============================================================
    'avg': {
        'name': 'avg',
        'category': 'statistics',
        'signature': 'avg(значение [, by m[:, "X"]])',
        'description': (
            'Среднее чисел.\n'
            '  • Без by — одно число.\n'
            '  • С by — вектор: среднее группы для каждой строки.'
        ),
        'examples': [
            'r = avg(v)',
            'r = avg(m[:, "Зарплата"])',
            'r = avg(m[:, "Зарплата"], by m[:, "Отдел"])',
        ],
        'errors': {
            'AVG_BAD_SYNTAX': {
                'message': (
                    "avg: неверный синтаксис.\n"
                    "  Нужен ровно один аргумент (или аргумент + by)."
                ),
                'wrong': 'avg()',
                'right': 'avg(v)',
                'explanation': (
                    "avg принимает 1 или 2 аргумента:\n"
                    "     avg(v)                                 — скаляр\n"
                    "     avg(m[:, \"Зарплата\"], by m[:, \"Отдел\"]) — вектор"
                ),
                'variants': [
                    'r = avg(v)',
                    'r = avg(m[:, "Зарплата"])',
                    'r = avg(m[:, "Зарплата"], by m[:, "Отдел"])',
                ],
            },
            'AVG_NEED_BY': {
                'message': (
                    "avg: после запятой ожидается ключевое слово 'by'."
                ),
                'wrong': 'avg(m[:, "Зарплата"], m[:, "Отдел"])',
                'right': 'avg(m[:, "Зарплата"], by m[:, "Отдел"])',
                'explanation': (
                    "Если указана запятая — вторым аргументом должно идти\n"
                    "'by m[:, \"X\"]'."
                ),
                'variants': [
                    'r = avg(m[:, "Зарплата"], by m[:, "Отдел"])',
                ],
            },
            'AVG_BAD_BY': {
                'message': 'avg: by должен быть срезом m[:, "X"].',
                'wrong': 'avg(m[:, "Зарплата"], by "Отдел")',
                'right': 'avg(m[:, "Зарплата"], by m[:, "Отдел"])',
                'explanation': (
                    "by принимает СРЕЗ столбца:\n"
                    "     by m[:, \"Отдел\"]"
                ),
                'variants': [
                    'r = avg(m[:, "Зарплата"], by m[:, "Отдел"])',
                ],
            },
            'AVG_BAD_ARG': {
                'message': 'avg: нельзя применить к этому типу.',
                'wrong': 'avg(None)',
                'right': 'avg(v)',
                'explanation': (
                    "avg работает с числами, векторами, матрицами."
                ),
                'variants': [
                    'r = avg(v)',
                    'r = avg(m)',
                ],
            },
        },
    },

    # ============================================================
    # COUNT
    # ============================================================
    'count': {
        'name': 'count',
        'category': 'statistics',
        'signature': 'count([значение] [, by m[:, "X"]])',
        'description': (
            'Количество.\n'
            '  • count(m[:, "X"])                    — непустые значения (скаляр).\n'
            '  • count(m[:, "X"], by m[:, "Y"])       — непустые в группе (вектор).\n'
            '  • count(by m[:, "Y"])                 — строк в группе (вектор).'
        ),
        'examples': [
            'r = count(m[:, "Зарплата"])',
            'r = count(m[:, "Зарплата"], by m[:, "Отдел"])',
            'r = count(by m[:, "Отдел"])',
        ],
        'errors': {
            'COUNT_BAD_SYNTAX': {
                'message': (
                    "count: неверный синтаксис.\n"
                    "  Нужен аргумент или ключ by."
                ),
                'wrong': 'count()',
                'right': 'count(m[:, "Зарплата"])',
                'explanation': (
                    "count без аргумента невозможен, потому что\n"
                    "неизвестно, что считать.\n"
                    "\n"
                    "Правильно:\n"
                    "     count(m[:, \"Зарплата\"])                     — непустые\n"
                    "     count(by m[:, \"Отдел\"])                     — строки в группе\n"
                    "     count(m[:, \"Зарплата\"], by m[:, \"Отдел\"])    — непустые в группе"
                ),
                'variants': [
                    'r = count(m[:, "Зарплата"])',
                    'r = count(by m[:, "Отдел"])',
                    'r = count(m[:, "Зарплата"], by m[:, "Отдел"])',
                ],
            },
            'COUNT_NEED_BY': {
                'message': (
                    "count: после запятой ожидается ключевое слово 'by'."
                ),
                'wrong': 'count(m[:, "Зарплата"], m[:, "Отдел"])',
                'right': 'count(m[:, "Зарплата"], by m[:, "Отдел"])',
                'explanation': (
                    "Если указана запятая — вторым аргументом должно идти\n"
                    "'by m[:, \"X\"]'."
                ),
                'variants': [
                    'r = count(m[:, "Зарплата"], by m[:, "Отдел"])',
                ],
            },
            'COUNT_BAD_BY': {
                'message': 'count: by должен быть срезом m[:, "X"].',
                'wrong': 'count(by "Отдел")',
                'right': 'count(by m[:, "Отдел"])',
                'explanation': (
                    "by принимает СРЕЗ столбца:\n"
                    "     by m[:, \"Отдел\"]\n"
                    "     by m[:, 3]"
                ),
                'variants': [
                    'r = count(by m[:, "Отдел"])',
                    'r = count(m[:, "Зарплата"], by m[:, "Отдел"])',
                ],
            },
        },
    },

    # ============================================================
    # MEDIAN
    # ============================================================
    'median': {
        'name': 'median',
        'category': 'statistics',
        'signature': 'median(значение [, by m[:, "X"]])',
        'description': (
            'Медиана.\n'
            '  • Без by — одно число.\n'
            '  • С by — вектор: медиана группы для каждой строки.'
        ),
        'examples': [
            'r = median(m[:, "Зарплата"])',
            'r = median(m[:, "Зарплата"], by m[:, "Отдел"])',
        ],
        'errors': {
            'MEDIAN_BAD_SYNTAX': {
                'message': (
                    "median: неверный синтаксис.\n"
                    "  Нужен ровно один аргумент (или аргумент + by)."
                ),
                'wrong': 'median()',
                'right': 'median(m[:, "Зарплата"])',
                'explanation': (
                    "median принимает 1 или 2 аргумента:\n"
                    "     median(m[:, \"Зарплата\"])                     — скаляр\n"
                    "     median(m[:, \"Зарплата\"], by m[:, \"Отдел\"])    — вектор"
                ),
                'variants': [
                    'r = median(m[:, "Зарплата"])',
                    'r = median(m[:, "Зарплата"], by m[:, "Отдел"])',
                ],
            },
            'MEDIAN_NEED_BY': {
                'message': (
                    "median: после запятой ожидается ключевое слово 'by'."
                ),
                'wrong': 'median(m[:, "Зарплата"], m[:, "Отдел"])',
                'right': 'median(m[:, "Зарплата"], by m[:, "Отдел"])',
                'explanation': (
                    "Если указана запятая — вторым аргументом должно идти\n"
                    "'by m[:, \"X\"]'."
                ),
                'variants': [
                    'r = median(m[:, "Зарплата"], by m[:, "Отдел"])',
                ],
            },
            'MEDIAN_BAD_BY': {
                'message': 'median: by должен быть срезом m[:, "X"].',
                'wrong': 'median(m[:, "Зарплата"], by "Отдел")',
                'right': 'median(m[:, "Зарплата"], by m[:, "Отдел"])',
                'explanation': (
                    "by принимает СРЕЗ столбца:\n"
                    "     by m[:, \"Отдел\"]"
                ),
                'variants': [
                    'r = median(m[:, "Зарплата"], by m[:, "Отдел"])',
                ],
            },
        },
    },

    # ============================================================
    # STD
    # ============================================================
    'std': {
        'name': 'std',
        'category': 'statistics',
        'signature': 'std(значение [, by m[:, "X"]])',
        'description': (
            'Стандартное отклонение (population, делитель N).\n'
            '  • Без by — одно число.\n'
            '  • С by — вектор: отклонение группы для каждой строки.'
        ),
        'examples': [
            'r = std(m[:, "Зарплата"])',
            'r = std(m[:, "Зарплата"], by m[:, "Отдел"])',
        ],
        'errors': {
            'STD_BAD_SYNTAX': {
                'message': (
                    "std: неверный синтаксис.\n"
                    "  Нужен ровно один аргумент (или аргумент + by)."
                ),
                'wrong': 'std()',
                'right': 'std(m[:, "Зарплата"])',
                'explanation': (
                    "std принимает 1 или 2 аргумента:\n"
                    "     std(m[:, \"Зарплата\"])                     — скаляр\n"
                    "     std(m[:, \"Зарплата\"], by m[:, \"Отдел\"])    — вектор"
                ),
                'variants': [
                    'r = std(m[:, "Зарплата"])',
                    'r = std(m[:, "Зарплата"], by m[:, "Отдел"])',
                ],
            },
            'STD_NEED_BY': {
                'message': (
                    "std: после запятой ожидается ключевое слово 'by'."
                ),
                'wrong': 'std(m[:, "Зарплата"], m[:, "Отдел"])',
                'right': 'std(m[:, "Зарплата"], by m[:, "Отдел"])',
                'explanation': (
                    "Если указана запятая — вторым аргументом должно идти\n"
                    "'by m[:, \"X\"]'."
                ),
                'variants': [
                    'r = std(m[:, "Зарплата"], by m[:, "Отдел"])',
                ],
            },
            'STD_BAD_BY': {
                'message': 'std: by должен быть срезом m[:, "X"].',
                'wrong': 'std(m[:, "Зарплата"], by "Отдел")',
                'right': 'std(m[:, "Зарплата"], by m[:, "Отдел"])',
                'explanation': (
                    "by принимает СРЕЗ столбца:\n"
                    "     by m[:, \"Отдел\"]"
                ),
                'variants': [
                    'r = std(m[:, "Зарплата"], by m[:, "Отдел"])',
                ],
            },
        },
    },
}


EN = {
    # ============================================================
    # SUM
    # ============================================================
    'sum': {
        'name': 'sum',
        'category': 'statistics',
        'signature': 'sum(value [, by m[:, "X"]])',
        'description': (
            'Sum of numbers.\n'
            '  • Works with vector, matrix, slice.\n'
            '  • Works with Matrix and DuckDB.\n'
            '  • None, strings, bool — ignored.\n'
            '  • Empty input → 0.\n'
            '  • Without by — single number.\n'
            '  • With by — vector: group sum for each row.'
        ),
        'examples': [
            'r = sum(v)',
            'r = sum(m[:, "Salary"])',
            'r = sum(m[:, "Salary"], by m[:, "Department"])',
            'r = sum(m)',
        ],
        'errors': {
            'SUM_BAD_SYNTAX': {
                'message': (
                    "sum: invalid syntax.\n"
                    "  Exactly one argument is required (or an argument + by)."
                ),
                'wrong': 'sum()',
                'right': 'sum(v)',
                'explanation': (
                    "sum takes 1 or 2 arguments:\n"
                    "     sum(v)                                        — scalar\n"
                    "     sum(m[:, \"Salary\"])                         — scalar\n"
                    "     sum(m[:, \"Salary\"], by m[:, \"Department\"])   — vector\n"
                    "\n"
                    "Incorrect:\n"
                    "     sum()\n"
                    "     sum(v, m)\n"
                    "\n"
                    "Correct:\n"
                    "     sum(v)\n"
                    "     sum(v, by m[:, \"Department\"])"
                ),
                'variants': [
                    'r = sum(v)',
                    'r = sum(m[:, "Salary"])',
                    'r = sum(m[:, "Salary"], by m[:, "Department"])',
                ],
            },
            'SUM_NEED_BY': {
                'message': (
                    "sum: after the comma, keyword 'by' is expected."
                ),
                'wrong': 'sum(m[:, "Salary"], m[:, "Department"])',
                'right': 'sum(m[:, "Salary"], by m[:, "Department"])',
                'explanation': (
                    "If a comma is given, the second argument must be\n"
                    "'by m[:, \"X\"]'.\n"
                    "\n"
                    "Incorrect:\n"
                    "     sum(m[:, \"Salary\"], m[:, \"Department\"])\n"
                    "\n"
                    "Correct:\n"
                    "     sum(m[:, \"Salary\"], by m[:, \"Department\"])"
                ),
                'variants': [
                    'r = sum(m[:, "Salary"], by m[:, "Department"])',
                ],
            },
            'SUM_BAD_BY': {
                'message': (
                    "sum: by must be a slice m[:, \"X\"]."
                ),
                'wrong': 'sum(m[:, "Salary"], by "Department")',
                'right': 'sum(m[:, "Salary"], by m[:, "Department"])',
                'explanation': (
                    "by takes a column SLICE:\n"
                    "     by m[:, \"Department\"]\n"
                    "     by m[:, 3]"
                ),
                'variants': [
                    'r = sum(m[:, "Salary"], by m[:, "Department"])',
                ],
            },
            'SUM_BAD_ARG': {
                'message': 'sum: cannot be applied to this type.',
                'wrong': 'sum(None)',
                'right': 'sum(v)',
                'explanation': (
                    "sum works with numbers, vectors, matrices."
                ),
                'variants': [
                    'r = sum(v)',
                    'r = sum(m)',
                ],
            },
        },
    },

    # ============================================================
    # MIN
    # ============================================================
    'min': {
        'name': 'min',
        'category': 'statistics',
        'signature': 'min(value [, by m[:, "X"]])',
        'description': (
            'Minimum among numbers.\n'
            '  • Without by — single number.\n'
            '  • With by — vector: group minimum for each row.'
        ),
        'examples': [
            'r = min(v)',
            'r = min(m[:, "Salary"])',
            'r = min(m[:, "Salary"], by m[:, "Department"])',
        ],
        'errors': {
            'MIN_BAD_SYNTAX': {
                'message': (
                    "min: invalid syntax.\n"
                    "  Exactly one argument is required (or an argument + by)."
                ),
                'wrong': 'min()',
                'right': 'min(v)',
                'explanation': (
                    "min takes 1 or 2 arguments:\n"
                    "     min(v)                                 — scalar\n"
                    "     min(m[:, \"Salary\"], by m[:, \"Department\"]) — vector"
                ),
                'variants': [
                    'r = min(v)',
                    'r = min(m[:, "Salary"], by m[:, "Department"])',
                ],
            },
            'MIN_NEED_BY': {
                'message': "min: after the comma, keyword 'by' is expected.",
                'wrong': 'min(m[:, "Salary"], m[:, "Department"])',
                'right': 'min(m[:, "Salary"], by m[:, "Department"])',
                'explanation': (
                    "If a comma is given, the second argument must be\n"
                    "'by m[:, \"X\"]'."
                ),
                'variants': [
                    'r = min(m[:, "Salary"], by m[:, "Department"])',
                ],
            },
            'MIN_BAD_BY': {
                'message': 'min: by must be a slice m[:, "X"].',
                'wrong': 'min(m[:, "Salary"], by "Department")',
                'right': 'min(m[:, "Salary"], by m[:, "Department"])',
                'explanation': (
                    "by takes a column SLICE:\n"
                    "     by m[:, \"Department\"]"
                ),
                'variants': [
                    'r = min(m[:, "Salary"], by m[:, "Department"])',
                ],
            },
            'MIN_BAD_ARG': {
                'message': 'min: cannot be applied to this type.',
                'wrong': 'min(None)',
                'right': 'min(v)',
                'explanation': "min works with numbers, vectors, matrices.",
                'variants': [
                    'r = min(v)',
                    'r = min(m)',
                ],
            },
        },
    },

    # ============================================================
    # MAX
    # ============================================================
    'max': {
        'name': 'max',
        'category': 'statistics',
        'signature': 'max(value [, by m[:, "X"]])',
        'description': (
            'Maximum among numbers.\n'
            '  • Without by — single number.\n'
            '  • With by — vector: group maximum for each row.'
        ),
        'examples': [
            'r = max(v)',
            'r = max(m[:, "Salary"])',
            'r = max(m[:, "Salary"], by m[:, "Department"])',
        ],
        'errors': {
            'MAX_BAD_SYNTAX': {
                'message': (
                    "max: invalid syntax.\n"
                    "  Exactly one argument is required (or an argument + by)."
                ),
                'wrong': 'max()',
                'right': 'max(v)',
                'explanation': (
                    "max takes 1 or 2 arguments:\n"
                    "     max(v)                                 — scalar\n"
                    "     max(m[:, \"Salary\"], by m[:, \"Department\"]) — vector"
                ),
                'variants': [
                    'r = max(v)',
                    'r = max(m[:, "Salary"], by m[:, "Department"])',
                ],
            },
            'MAX_NEED_BY': {
                'message': "max: after the comma, keyword 'by' is expected.",
                'wrong': 'max(m[:, "Salary"], m[:, "Department"])',
                'right': 'max(m[:, "Salary"], by m[:, "Department"])',
                'explanation': (
                    "If a comma is given, the second argument must be\n"
                    "'by m[:, \"X\"]'."
                ),
                'variants': [
                    'r = max(m[:, "Salary"], by m[:, "Department"])',
                ],
            },
            'MAX_BAD_BY': {
                'message': 'max: by must be a slice m[:, "X"].',
                'wrong': 'max(m[:, "Salary"], by "Department")',
                'right': 'max(m[:, "Salary"], by m[:, "Department"])',
                'explanation': (
                    "by takes a column SLICE:\n"
                    "     by m[:, \"Department\"]"
                ),
                'variants': [
                    'r = max(m[:, "Salary"], by m[:, "Department"])',
                ],
            },
            'MAX_BAD_ARG': {
                'message': 'max: cannot be applied to this type.',
                'wrong': 'max(None)',
                'right': 'max(v)',
                'explanation': "max works with numbers, vectors, matrices.",
                'variants': [
                    'r = max(v)',
                    'r = max(m)',
                ],
            },
        },
    },

    # ============================================================
    # AVG
    # ============================================================
    'avg': {
        'name': 'avg',
        'category': 'statistics',
        'signature': 'avg(value [, by m[:, "X"]])',
        'description': (
            'Average of numbers.\n'
            '  • Without by — single number.\n'
            '  • With by — vector: group average for each row.'
        ),
        'examples': [
            'r = avg(v)',
            'r = avg(m[:, "Salary"])',
            'r = avg(m[:, "Salary"], by m[:, "Department"])',
        ],
        'errors': {
            'AVG_BAD_SYNTAX': {
                'message': (
                    "avg: invalid syntax.\n"
                    "  Exactly one argument is required (or an argument + by)."
                ),
                'wrong': 'avg()',
                'right': 'avg(v)',
                'explanation': (
                    "avg takes 1 or 2 arguments:\n"
                    "     avg(v)                                 — scalar\n"
                    "     avg(m[:, \"Salary\"], by m[:, \"Department\"]) — vector"
                ),
                'variants': [
                    'r = avg(v)',
                    'r = avg(m[:, "Salary"], by m[:, "Department"])',
                ],
            },
            'AVG_NEED_BY': {
                'message': "avg: after the comma, keyword 'by' is expected.",
                'wrong': 'avg(m[:, "Salary"], m[:, "Department"])',
                'right': 'avg(m[:, "Salary"], by m[:, "Department"])',
                'explanation': (
                    "If a comma is given, the second argument must be\n"
                    "'by m[:, \"X\"]'."
                ),
                'variants': [
                    'r = avg(m[:, "Salary"], by m[:, "Department"])',
                ],
            },
            'AVG_BAD_BY': {
                'message': 'avg: by must be a slice m[:, "X"].',
                'wrong': 'avg(m[:, "Salary"], by "Department")',
                'right': 'avg(m[:, "Salary"], by m[:, "Department"])',
                'explanation': (
                    "by takes a column SLICE:\n"
                    "     by m[:, \"Department\"]"
                ),
                'variants': [
                    'r = avg(m[:, "Salary"], by m[:, "Department"])',
                ],
            },
            'AVG_BAD_ARG': {
                'message': 'avg: cannot be applied to this type.',
                'wrong': 'avg(None)',
                'right': 'avg(v)',
                'explanation': "avg works with numbers, vectors, matrices.",
                'variants': [
                    'r = avg(v)',
                    'r = avg(m)',
                ],
            },
        },
    },

    # ============================================================
    # COUNT
    # ============================================================
    'count': {
        'name': 'count',
        'category': 'statistics',
        'signature': 'count([value] [, by m[:, "X"]])',
        'description': (
            'Count.\n'
            '  • count(m[:, "X"])                    — non-empty values (scalar).\n'
            '  • count(m[:, "X"], by m[:, "Y"])       — non-empty in group (vector).\n'
            '  • count(by m[:, "Y"])                 — rows per group (vector).'
        ),
        'examples': [
            'r = count(m[:, "Salary"])',
            'r = count(m[:, "Salary"], by m[:, "Department"])',
            'r = count(by m[:, "Department"])',
        ],
        'errors': {
            'COUNT_BAD_SYNTAX': {
                'message': (
                    "count: invalid syntax.\n"
                    "  Either an argument or a by-key is required."
                ),
                'wrong': 'count()',
                'right': 'count(m[:, "Salary"])',
                'explanation': (
                    "count without an argument is impossible because\n"
                    "it's unclear what to count.\n"
                    "\n"
                    "Correct:\n"
                    "     count(m[:, \"Salary\"])                     — non-empty\n"
                    "     count(by m[:, \"Department\"])               — rows per group\n"
                    "     count(m[:, \"Salary\"], by m[:, \"Department\"]) — non-empty in group"
                ),
                'variants': [
                    'r = count(m[:, "Salary"])',
                    'r = count(by m[:, "Department"])',
                    'r = count(m[:, "Salary"], by m[:, "Department"])',
                ],
            },
            'COUNT_NEED_BY': {
                'message': "count: after the comma, keyword 'by' is expected.",
                'wrong': 'count(m[:, "Salary"], m[:, "Department"])',
                'right': 'count(m[:, "Salary"], by m[:, "Department"])',
                'explanation': (
                    "If a comma is given, the second argument must be\n"
                    "'by m[:, \"X\"]'."
                ),
                'variants': [
                    'r = count(m[:, "Salary"], by m[:, "Department"])',
                ],
            },
            'COUNT_BAD_BY': {
                'message': 'count: by must be a slice m[:, "X"].',
                'wrong': 'count(by "Department")',
                'right': 'count(by m[:, "Department"])',
                'explanation': (
                    "by takes a column SLICE:\n"
                    "     by m[:, \"Department\"]\n"
                    "     by m[:, 3]"
                ),
                'variants': [
                    'r = count(by m[:, "Department"])',
                    'r = count(m[:, "Salary"], by m[:, "Department"])',
                ],
            },
        },
    },

    # ============================================================
    # MEDIAN
    # ============================================================
    'median': {
        'name': 'median',
        'category': 'statistics',
        'signature': 'median(value [, by m[:, "X"]])',
        'description': (
            'Median.\n'
            '  • Without by — single number.\n'
            '  • With by — vector: group median for each row.'
        ),
        'examples': [
            'r = median(m[:, "Salary"])',
            'r = median(m[:, "Salary"], by m[:, "Department"])',
        ],
        'errors': {
            'MEDIAN_BAD_SYNTAX': {
                'message': (
                    "median: invalid syntax.\n"
                    "  Exactly one argument is required (or an argument + by)."
                ),
                'wrong': 'median()',
                'right': 'median(m[:, "Salary"])',
                'explanation': (
                    "median takes 1 or 2 arguments:\n"
                    "     median(m[:, \"Salary\"])                     — scalar\n"
                    "     median(m[:, \"Salary\"], by m[:, \"Department\"]) — vector"
                ),
                'variants': [
                    'r = median(m[:, "Salary"])',
                    'r = median(m[:, "Salary"], by m[:, "Department"])',
                ],
            },
            'MEDIAN_NEED_BY': {
                'message': "median: after the comma, keyword 'by' is expected.",
                'wrong': 'median(m[:, "Salary"], m[:, "Department"])',
                'right': 'median(m[:, "Salary"], by m[:, "Department"])',
                'explanation': (
                    "If a comma is given, the second argument must be\n"
                    "'by m[:, \"X\"]'."
                ),
                'variants': [
                    'r = median(m[:, "Salary"], by m[:, "Department"])',
                ],
            },
            'MEDIAN_BAD_BY': {
                'message': 'median: by must be a slice m[:, "X"].',
                'wrong': 'median(m[:, "Salary"], by "Department")',
                'right': 'median(m[:, "Salary"], by m[:, "Department"])',
                'explanation': (
                    "by takes a column SLICE:\n"
                    "     by m[:, \"Department\"]"
                ),
                'variants': [
                    'r = median(m[:, "Salary"], by m[:, "Department"])',
                ],
            },
        },
    },

    # ============================================================
    # STD
    # ============================================================
    'std': {
        'name': 'std',
        'category': 'statistics',
        'signature': 'std(value [, by m[:, "X"]])',
        'description': (
            'Standard deviation (population, divisor N).\n'
            '  • Without by — single number.\n'
            '  • With by — vector: group deviation for each row.'
        ),
        'examples': [
            'r = std(m[:, "Salary"])',
            'r = std(m[:, "Salary"], by m[:, "Department"])',
        ],
        'errors': {
            'STD_BAD_SYNTAX': {
                'message': (
                    "std: invalid syntax.\n"
                    "  Exactly one argument is required (or an argument + by)."
                ),
                'wrong': 'std()',
                'right': 'std(m[:, "Salary"])',
                'explanation': (
                    "std takes 1 or 2 arguments:\n"
                    "     std(m[:, \"Salary\"])                     — scalar\n"
                    "     std(m[:, \"Salary\"], by m[:, \"Department\"]) — vector"
                ),
                'variants': [
                    'r = std(m[:, "Salary"])',
                    'r = std(m[:, "Salary"], by m[:, "Department"])',
                ],
            },
            'STD_NEED_BY': {
                'message': "std: after the comma, keyword 'by' is expected.",
                'wrong': 'std(m[:, "Salary"], m[:, "Department"])',
                'right': 'std(m[:, "Salary"], by m[:, "Department"])',
                'explanation': (
                    "If a comma is given, the second argument must be\n"
                    "'by m[:, \"X\"]'."
                ),
                'variants': [
                    'r = std(m[:, "Salary"], by m[:, "Department"])',
                ],
            },
            'STD_BAD_BY': {
                'message': 'std: by must be a slice m[:, "X"].',
                'wrong': 'std(m[:, "Salary"], by "Department")',
                'right': 'std(m[:, "Salary"], by m[:, "Department"])',
                'explanation': (
                    "by takes a column SLICE:\n"
                    "     by m[:, \"Department\"]"
                ),
                'variants': [
                    'r = std(m[:, "Salary"], by m[:, "Department"])',
                ],
            },
        },
    },
}