# errors/functions_db/pivot.py
"""
База ошибок для функции PIVOT.
"""

RU = {
    'pivot': {
        'name': 'pivot',
        'category': 'analytics',
        'signature': 'pivot(ключ, значения, агрегат)\n'
                     'pivot(ключ_строк, ключ_столбцов, значения, агрегат)',
        'description': (
            'Сводная таблица.\n'
            '  • 3 аргумента — один ключ (2 столбца).\n'
            '  • 4 аргумента — два ключа (pivot-таблица).'
        ),
        'examples': [
            'r = pivot(m[:, "Отдел"], m[:, "Зарплата"], sum)',
            'r = pivot(m[:, "Отдел"], m[:, "Год"], m[:, "Зарплата"], sum)',
        ],
        'errors': {
            'PIVOT_BAD_SYNTAX': {
                'message': (
                    "pivot: неверный синтаксис.\n"
                    "  Ожидается 3 или 4 аргумента."
                ),
                'wrong': 'pivot(m[:, "Отдел"])',
                'right': 'pivot(m[:, "Отдел"], m[:, "Зарплата"], sum)',
                'explanation': (
                    "pivot принимает 3 или 4 аргумента:\n"
                    "\n"
                    "  3 аргумента (один ключ):\n"
                    "     pivot(ключ, значения, агрегат)\n"
                    "\n"
                    "  4 аргумента (два ключа):\n"
                    "     pivot(ключ_строк, ключ_столбцов, значения, агрегат)"
                ),
                'variants': [
                    'pivot(m[:, "Отдел"], m[:, "Зарплата"], sum)',
                    'pivot(m[:, "Отдел"], m[:, "Год"], m[:, "Зарплата"], sum)',
                ],
            },
            'PIVOT_MISSING_AGG': {
                'message': (
                    "pivot: не указан агрегат.\n"
                    "  Последний аргумент — sum, avg, count, min, max,\n"
                    "                          median, first, last, std."
                ),
                'wrong': 'pivot(m[:, "Отдел"], m[:, "Зарплата"])',
                'right': 'pivot(m[:, "Отдел"], m[:, "Зарплата"], sum)',
                'explanation': (
                    "pivot всегда требует агрегат последним аргументом.\n"
                    "\n"
                    "Доступные:\n"
                    "     sum, avg, count, min, max,\n"
                    "     median, first, last, std"
                ),
                'variants': [
                    'pivot(m[:, "Отдел"], m[:, "Зарплата"], sum)',
                    'pivot(m[:, "Отдел"], m[:, "Зарплата"], avg)',
                    'pivot(m[:, "Отдел"], m[:, "Зарплата"], count)',
                ],
            },
            'PIVOT_BAD_AGG': {
                'message': (
                    "pivot: неверный агрегат.\n"
                    "  Допустимо: sum, avg, count, min, max,\n"
                    "             median, first, last, std."
                ),
                'wrong': 'pivot(m[:, "Отдел"], m[:, "Зарплата"], average)',
                'right': 'pivot(m[:, "Отдел"], m[:, "Зарплата"], avg)',
                'explanation': (
                    "Допустимо только:\n"
                    "     sum, avg, count, min, max,\n"
                    "     median, first, last, std"
                ),
                'variants': [
                    'pivot(m[:, "Отдел"], m[:, "Зарплата"], sum)',
                    'pivot(m[:, "Отдел"], m[:, "Зарплата"], avg)',
                ],
            },
            'PIVOT_BAD_KEY': {
                'message': (
                    "pivot: ключ должен быть срезом m[:, \"X\"]."
                ),
                'wrong': 'pivot("Отдел", m[:, "Зарплата"], sum)',
                'right': 'pivot(m[:, "Отдел"], m[:, "Зарплата"], sum)',
                'explanation': (
                    "Все ключи — срезы столбцов:\n"
                    "     pivot(m[:, \"Отдел\"], m[:, \"Зарплата\"], sum)"
                ),
                'variants': [
                    'pivot(m[:, "Отдел"], m[:, "Зарплата"], sum)',
                    'pivot(m[:, 1], m[:, 3], sum)',
                ],
            },
        },
    },
}


EN = {
    'pivot': {
        'name': 'pivot',
        'category': 'analytics',
        'signature': 'pivot(key, values, agg)\n'
                     'pivot(row_key, col_key, values, agg)',
        'description': (
            'Pivot table.\n'
            '  • 3 args — one key (2 columns).\n'
            '  • 4 args — two keys (pivot table).'
        ),
        'examples': [
            'r = pivot(m[:, "Dept"], m[:, "Salary"], sum)',
            'r = pivot(m[:, "Dept"], m[:, "Year"], m[:, "Salary"], sum)',
        ],
        'errors': {
            'PIVOT_BAD_SYNTAX': {
                'message': (
                    "pivot: invalid syntax.\n"
                    "  Expected 3 or 4 arguments."
                ),
                'wrong': 'pivot(m[:, "Dept"])',
                'right': 'pivot(m[:, "Dept"], m[:, "Salary"], sum)',
                'explanation': (
                    "pivot takes 3 or 4 arguments:\n"
                    "\n"
                    "  3 args (one key):\n"
                    "     pivot(key, values, agg)\n"
                    "\n"
                    "  4 args (two keys):\n"
                    "     pivot(row_key, col_key, values, agg)"
                ),
                'variants': [
                    'pivot(m[:, "Dept"], m[:, "Salary"], sum)',
                    'pivot(m[:, "Dept"], m[:, "Year"], m[:, "Salary"], sum)',
                ],
            },
            'PIVOT_MISSING_AGG': {
                'message': (
                    "pivot: aggregate is missing.\n"
                    "  Last argument — sum, avg, count, min, max,\n"
                    "                   median, first, last, std."
                ),
                'wrong': 'pivot(m[:, "Dept"], m[:, "Salary"])',
                'right': 'pivot(m[:, "Dept"], m[:, "Salary"], sum)',
                'explanation': (
                    "pivot always requires an aggregate as the last argument.\n"
                    "\n"
                    "Available:\n"
                    "     sum, avg, count, min, max,\n"
                    "     median, first, last, std"
                ),
                'variants': [
                    'pivot(m[:, "Dept"], m[:, "Salary"], sum)',
                    'pivot(m[:, "Dept"], m[:, "Salary"], avg)',
                ],
            },
            'PIVOT_BAD_AGG': {
                'message': (
                    "pivot: invalid aggregate.\n"
                    "  Allowed: sum, avg, count, min, max,\n"
                    "           median, first, last, std."
                ),
                'wrong': 'pivot(m[:, "Dept"], m[:, "Salary"], average)',
                'right': 'pivot(m[:, "Dept"], m[:, "Salary"], avg)',
                'explanation': (
                    "Only these are allowed:\n"
                    "     sum, avg, count, min, max,\n"
                    "     median, first, last, std"
                ),
                'variants': [
                    'pivot(m[:, "Dept"], m[:, "Salary"], sum)',
                    'pivot(m[:, "Dept"], m[:, "Salary"], avg)',
                ],
            },
            'PIVOT_BAD_KEY': {
                'message': (
                    "pivot: key must be a slice m[:, \"X\"]."
                ),
                'wrong': 'pivot("Dept", m[:, "Salary"], sum)',
                'right': 'pivot(m[:, "Dept"], m[:, "Salary"], sum)',
                'explanation': (
                    "All keys are column slices:\n"
                    "     pivot(m[:, \"Dept\"], m[:, \"Salary\"], sum)"
                ),
                'variants': [
                    'pivot(m[:, "Dept"], m[:, "Salary"], sum)',
                    'pivot(m[:, 1], m[:, 3], sum)',
                ],
            },
        },
    },
}