# errors/functions_db/sort.py
"""
База ошибок для функции SORT.
"""

RU = {
    'sort': {
        'name': 'sort',
        'category': 'sort',
        'signature': 'sort(m[диапазон, "X"], AZ | ZA)',
        'description': (
            'Сортировка строк матрицы по столбцу.\n'
            '  • Срез m[:, "X"] или m[2:10, "X"].\n'
            '  • Вектор v или v[3:6].\n'
            '  • Направление: AZ (возрастание) или ZA (убывание).\n'
            '  • Возвращает НОВУЮ матрицу — результат нужно сохранить.'
        ),
        'examples': [
            'r = sort(m[:, "Имя"], AZ)',
            'm = sort(m[:, "Возраст"], ZA)',
            'r = sort(m[2:10, "Возраст"], AZ)',
            'r = sort(m[last 100, "Имя"], ZA)',
            'r = sort(v, AZ)',
            'r = sort(v[3:6], AZ)',
        ],
        'errors': {
            'SORT_BAD_FIRST_ARG': {
                'message': (
                    "sort работает только со срезом m[:, \"X\"], "
                    "m[2:10, \"X\"] или вектором.\n"
                    "  Указана вся матрица без выбора столбца."
                ),
                'wrong': 'sort(m, AZ)',
                'right': 'sort(m[:, "Имя"], AZ)',
                'explanation': (
                    "Первый аргумент — это СРЕЗ, а не вся матрица.\n"
                    "В срезе обязательно указывается столбец."
                ),
                'variants': [
                    'sort(m[:, "Имя"], AZ)',
                    'sort(m[2:10, "Возраст"], AZ)',
                    'sort(v, AZ)',
                ],
            },
            'SORT_BAD_DIRECTION': {
                'message': "Направление сортировки должно быть AZ или ZA.",
                'wrong': 'sort(m[:, "Имя"], UP)',
                'right': 'sort(m[:, "Имя"], AZ)',
                'explanation': (
                    "AZ — по возрастанию (А→Я, 1→9).\n"
                    "ZA — по убыванию (Я→А, 9→1)."
                ),
                'variants': [
                    'sort(m[:, "Имя"], AZ)',
                    'sort(m[:, "Имя"], ZA)',
                ],
            },
            'SORT_MISSING_DIRECTION': {
                'message': "Не указано направление сортировки.",
                'wrong': 'sort(m[:, "Имя"])',
                'right': 'sort(m[:, "Имя"], AZ)',
                'explanation': "sort ВСЕГДА требует направление: AZ или ZA.",
            },
            'SORT_BAD_RANGE': {
                'message': (
                    "sort: неверный диапазон строк.\n"
                    "  Нельзя использовать ':' для столбцов."
                ),
                'wrong': 'sort(m[:, :], AZ)',
                'right': 'sort(m[:, "Имя"], AZ)',
                'explanation': (
                    "В первом индексе — строки:\n"
                    "  m[:, ...]          — все строки\n"
                    "  m[2:10, ...]       — строки 2..10\n"
                    "  m[last 5, ...]     — последние 5"
                ),
            },
        },
    },
}


EN = {
    'sort': {
        'name': 'sort',
        'category': 'sort',
        'signature': 'sort(m[range, "X"], AZ | ZA)',
        'description': (
            'Sort matrix rows by a column.\n'
            '  • Slice m[:, "X"] or m[2:10, "X"].\n'
            '  • Vector v or v[3:6].\n'
            '  • Direction: AZ (ascending) or ZA (descending).\n'
            '  • Returns a NEW matrix — save the result.'
        ),
        'examples': [
            'r = sort(m[:, "Name"], AZ)',
            'm = sort(m[:, "Age"], ZA)',
            'r = sort(m[2:10, "Age"], AZ)',
            'r = sort(m[last 100, "Name"], ZA)',
            'r = sort(v, AZ)',
            'r = sort(v[3:6], AZ)',
        ],
        'errors': {
            'SORT_BAD_FIRST_ARG': {
                'message': (
                    "sort works only with slice m[:, \"X\"], "
                    "m[2:10, \"X\"], or a vector.\n"
                    "  Whole matrix without column specified."
                ),
                'wrong': 'sort(m, AZ)',
                'right': 'sort(m[:, "Name"], AZ)',
                'explanation': (
                    "First argument must be a SLICE, not the whole matrix.\n"
                    "The slice must specify a column."
                ),
                'variants': [
                    'sort(m[:, "Name"], AZ)',
                    'sort(m[2:10, "Age"], AZ)',
                    'sort(v, AZ)',
                ],
            },
            'SORT_BAD_DIRECTION': {
                'message': "Sort direction must be AZ or ZA.",
                'wrong': 'sort(m[:, "Name"], UP)',
                'right': 'sort(m[:, "Name"], AZ)',
                'explanation': (
                    "AZ — ascending (A→Z, 1→9).\n"
                    "ZA — descending (Z→A, 9→1)."
                ),
                'variants': [
                    'sort(m[:, "Name"], AZ)',
                    'sort(m[:, "Name"], ZA)',
                ],
            },
            'SORT_MISSING_DIRECTION': {
                'message': "Sort direction is missing.",
                'wrong': 'sort(m[:, "Name"])',
                'right': 'sort(m[:, "Name"], AZ)',
                'explanation': "sort ALWAYS requires AZ or ZA.",
            },
            'SORT_BAD_RANGE': {
                'message': (
                    "sort: invalid row range.\n"
                    "  Cannot use ':' for columns."
                ),
                'wrong': 'sort(m[:, :], AZ)',
                'right': 'sort(m[:, "Name"], AZ)',
                'explanation': (
                    "First index is rows:\n"
                    "  m[:, ...]          — all rows\n"
                    "  m[2:10, ...]       — rows 2..10\n"
                    "  m[last 5, ...]     — last 5"
                ),
            },
        },
    },
}