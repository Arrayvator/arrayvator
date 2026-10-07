# syntax/signatures_data/pivot.py
"""
Сигнатуры функции pivot.
"""

SIGNATURES = {
    'pivot': {
        'name': 'pivot',
        'category': 'analytics',
        'args': ['column', 'values', 'agg'],
        'examples': [
            'r = pivot(m[:, "Отдел"], m[:, "Зарплата"], sum)',
            'r = pivot(m[:, "Отдел"], m[:, "Зарплата"], avg)',
            'r = pivot(m[:, "Отдел"], m[:, "Сотрудник"], count)',
        ],
    },
}