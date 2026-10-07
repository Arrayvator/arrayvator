# syntax/signatures_data/sort.py
"""
Сигнатуры функции сортировки.
"""

SIGNATURES = {
    'sort': {
        'name': 'sort',
        'category': 'analytics',
        'args': ['срез столбца', 'AZ | ZA'],
        'examples': [
            'r = sort(m[:, "Имя"], AZ)',
            'm = sort(m[:, 3], ZA)',
            'r = sort(v, AZ)',
        ],
    },
}