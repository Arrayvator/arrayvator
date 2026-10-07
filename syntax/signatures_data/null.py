# syntax/signatures_data/null.py
"""
Сигнатуры функций работы с None:
isnone, fillna, dropna, coalesce, null_if.
"""

SIGNATURES = {
    'isnone': {
        'name': 'isnone',
        'category': 'null',
        'args': ['значение'],
        'examples': [
            'r = isnone(None)',
            'r = isnone(5)',
        ],
    },

    'fillna': {
        'name': 'fillna',
        'category': 'null',
        'args': ['данные', 'значение'],
        'examples': [
            'r = fillna(v, 0)',
            'r = fillna(m, "—")',
        ],
    },

    'dropna': {
        'name': 'dropna',
        'category': 'null',
        'args': ['данные'],
        'examples': [
            'r = dropna(v)',
            'r = dropna(m)',
        ],
    },

    'coalesce': {
        'name': 'coalesce',
        'category': 'null',
        'args': ['значение1', 'значение2', '...'],
        'examples': [
            'r = coalesce(None, 5)',
            'r = coalesce(None, None, 10)',
        ],
    },

    'null_if': {
        'name': 'null_if',
        'category': 'null',
        'args': ['значение', 'условие'],
        'examples': [
            'r = null_if(value, condition)',
        ],
    },
}