# syntax/signatures_data/case.py
"""
Сигнатуры функций условного преобразования: case, applyif.
"""

SIGNATURES = {
    'case': {
        'name': 'case',
        'category': 'analytics',
        'args': ['срез или вектор', 'when ... then ...', 'else ...'],
        'examples': [
            'r = case(v, when < 18 then "Дитя", else "Взрослый")',
            'm = case(m[:, "Возраст"], when < 18 then "Дитя", else "Взрослый")',
        ],
    },

    'applyif': {
        'name': 'applyif',
        'category': 'analytics',
        'args': ['условие', 'm[:, "X"] = значение'],
        'examples': [
            'r = applyif(m[:, "Отдел"] == "IT", m[:, "Статус"] = "VIP")',
            'm = applyif(m[:, "Отдел"] == "IT", m[:, "Статус"] = "VIP")',
        ],
    },
}