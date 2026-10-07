# syntax/signatures_data/control.py
"""
Сигнатуры управляющих конструкций.
"""

SIGNATURES = {
    'if': {
        'name': 'if',
        'category': 'control',
        'args': ['условие', 'then { ... }', 'else { ... } (опц.)'],
        'examples': [
            'if x > 5 then { print("X") }',
            'if x > 5 then { ... } else { ... }',
        ],
    },

    'while': {
        'name': 'while',
        'category': 'control',
        'args': ['условие', '{ ... }'],
        'examples': [
            'while i <= 5 { i = i + 1 }',
        ],
    },

    'for': {
        'name': 'for',
        'category': 'control',
        'args': ['переменная', '(начало:конец)', '{ ... }'],
        'examples': [
            'for i(1:5) { print(i) }',
        ],
    },
}