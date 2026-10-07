# syntax/signatures_data/sample.py
"""
Сигнатуры функции sample.
"""

SIGNATURES = {
    'sample': {
        'name': 'sample',
        'category': 'analytics',
        'args': ['данные', 'N (количество строк)', 'seed (опц.)'],
        'examples': [
            'r = sample(m, 1000)',
            'r = sample(m, 100, 42)',
        ],
    },
}