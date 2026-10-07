# syntax/signatures_data/types.py
"""
Сигнатуры функций типов:
type, is_number, is_integer, is_float, is_string, is_boolean,
to_string, to_number.
"""

SIGNATURES = {
    'type': {
        'name': 'type',
        'category': 'types',
        'args': ['значение'],
        'examples': [
            'r = type(42)',
            'r = type("abc")',
            'r = type(3.14)',
        ],
    },

    'is_number': {
        'name': 'is_number',
        'category': 'types',
        'args': ['значение'],
        'examples': [
            'r = is_number(42)',
            'r = is_number("abc")',
        ],
    },

    'is_integer': {
        'name': 'is_integer',
        'category': 'types',
        'args': ['значение'],
        'examples': [
            'r = is_integer(42)',
            'r = is_integer(3.14)',
        ],
    },

    'is_float': {
        'name': 'is_float',
        'category': 'types',
        'args': ['значение'],
        'examples': [
            'r = is_float(3.14)',
            'r = is_float(42)',
        ],
    },

    'is_string': {
        'name': 'is_string',
        'category': 'types',
        'args': ['значение'],
        'examples': [
            'r = is_string("abc")',
            'r = is_string(42)',
        ],
    },

    'is_boolean': {
        'name': 'is_boolean',
        'category': 'types',
        'args': ['значение'],
        'examples': [
            'r = is_boolean(true)',
            'r = is_boolean(0)',
        ],
    },

    'to_string': {
        'name': 'to_string',
        'category': 'types',
        'args': ['значение'],
        'examples': [
            'r = to_string(42)',
            'r = to_string(3.14)',
        ],
    },

    'to_number': {
        'name': 'to_number',
        'category': 'types',
        'args': ['значение'],
        'examples': [
            'r = to_number("42")',
            'r = to_number("3.14")',
        ],
    },
}