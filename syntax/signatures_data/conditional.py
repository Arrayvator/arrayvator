# syntax/signatures_data/conditional.py
"""
Сигнатуры условных агрегатов:
sumif, countif, avgif, minif, maxif, medianif, countuniqueif, sumproduct.
"""

SIGNATURES = {
    'sumif': {
        'name': 'sumif',
        'category': 'analytics',
        'args': [
            'условие',
            'срез суммирования',
            'или by m[:, "X"] — группировка',
        ],
        'examples': [
            'r = sumif(m[:, "Отдел"] == "IT", m[:, "Зарплата"])',
            'r = sumif(by m[:, "Отдел"], m[:, "Зарплата"])',
        ],
    },

    'countif': {
        'name': 'countif',
        'category': 'analytics',
        'args': [
            'условие',
            'или by m[:, "X"] — группировка',
        ],
        'examples': [
            'r = countif(m[:, "Отдел"] == "IT")',
            'r = countif(by m[:, "Отдел"])',
        ],
    },

    'avgif': {
        'name': 'avgif',
        'category': 'analytics',
        'args': [
            'условие',
            'срез усреднения',
            'или by m[:, "X"] — группировка',
        ],
        'examples': [
            'r = avgif(m[:, "Отдел"] == "IT", m[:, "Зарплата"])',
            'r = avgif(by m[:, "Отдел"], m[:, "Зарплата"])',
        ],
    },

    'minif': {
        'name': 'minif',
        'category': 'analytics',
        'args': [
            'условие',
            'срез',
            'или by m[:, "X"] — группировка',
        ],
        'examples': [
            'r = minif(m[:, "Отдел"] == "IT", m[:, "Зарплата"])',
            'r = minif(by m[:, "Отдел"], m[:, "Зарплата"])',
        ],
    },

    'maxif': {
        'name': 'maxif',
        'category': 'analytics',
        'args': [
            'условие',
            'срез',
            'или by m[:, "X"] — группировка',
        ],
        'examples': [
            'r = maxif(m[:, "Отдел"] == "IT", m[:, "Зарплата"])',
            'r = maxif(by m[:, "Отдел"], m[:, "Зарплата"])',
        ],
    },

    'medianif': {
        'name': 'medianif',
        'category': 'analytics',
        'args': [
            'условие',
            'срез',
        ],
        'examples': [
            'r = medianif(m[:, "Отдел"] == "IT", m[:, "Зарплата"])',
        ],
    },

    'countuniqueif': {
        'name': 'countuniqueif',
        'category': 'analytics',
        'args': [
            'условие',
            'срез',
        ],
        'examples': [
            'r = countuniqueif(m[:, "Отдел"] == "IT", m[:, "Город"])',
        ],
    },

    'sumproduct': {
        'name': 'sumproduct',
        'category': 'analytics',
        'args': [
            'срез1',
            'срез2',
            '... (опц.)',
        ],
        'examples': [
            'r = sumproduct(m[:, "Цена"], m[:, "Количество"])',
            'r = sumproduct(m[:, "A"], m[:, "B"], m[:, "C"])',
        ],
    },
}