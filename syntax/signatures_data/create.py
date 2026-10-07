# syntax/signatures_data/create.py
"""
Сигнатуры функций создания:
matrix, vector, zeros, ones, fill, range, random.
"""

SIGNATURES = {
    'matrix': {
        'name': 'matrix',
        'category': 'create',
        'args': ['rows', 'cols'],
        'examples': [
            'm = matrix(3, 3)',
            'm = matrix(2, 5)',
        ],
    },

    'vector': {
        'name': 'vector',
        'category': 'create',
        'args': ['size'],
        'examples': [
            'v = vector(5)',
            'v = vector(10)',
        ],
    },

    'zeros': {
        'name': 'zeros',
        'category': 'create',
        'args': ['rows', 'cols (опц.)'],
        'examples': [
            'm = zeros(3, 3)',
            'v = zeros(5)',
        ],
    },

    'ones': {
        'name': 'ones',
        'category': 'create',
        'args': ['rows', 'cols (опц.)'],
        'examples': [
            'm = ones(3, 3)',
            'v = ones(5)',
        ],
    },

    'fill': {
        'name': 'fill',
        'category': 'create',
        'args': ['матрица', 'значение'],
        'examples': [
            'r = fill(m, 0)',
            'm = fill(m, "—")',
        ],
    },

    'range': {
        'name': 'range',
        'category': 'create',
        'args': ['начало', 'конец', 'шаг (опц.)'],
        'examples': [
            'r = range(1, 5)',
            'r = range(0, 10, 2)',
        ],
    },

    'random': {
        'name': 'random',
        'category': 'create',
        'args': ['диапазон (начало:конец)', 'точность'],
        'examples': [
            'x = random(0:10, 0)',
            'm[all, all] = random(-10:10, 2)',
        ],
    },
}