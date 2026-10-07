# syntax/signatures_data/math.py
"""
Сигнатуры математических функций.
"""

SIGNATURES = {
    'round': {
        'name': 'round',
        'category': 'math',
        'args': ['значение', 'знаков (опц.)'],
        'examples': [
            'r = round(3.14)',
            'r = round(3.14159, 2)',
            'm = round(m, 2)',
        ],
    },

    'int': {
        'name': 'int',
        'category': 'math',
        'args': ['значение'],
        'examples': ['r = int(3.7)', 'm = int(m)'],
    },

    'frac': {
        'name': 'frac',
        'category': 'math',
        'args': ['значение', 'знаков (опц.)'],
        'examples': ['r = frac(3.7)', 'm = frac(m)'],
    },

    'frac_digits': {
        'name': 'frac_digits',
        'category': 'math',
        'args': ['значение'],
        'examples': ['r = frac_digits(3.456)', 'm = frac_digits(m)'],
    },
}