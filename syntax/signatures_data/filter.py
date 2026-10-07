# syntax/signatures_data/filter.py
"""
Сигнатуры функций фильтрации и удаления.
"""

SIGNATURES = {
    'filterif': {
        'name': 'filterif',
        'category': 'analytics',
        'args': ['m[:, "X"] == "Y"', 'and/or', 'not'],
        'examples': [
            'r = filterif(m[:, "Пол"] == "Ж")',
            'm = filterif(m[:, "Пол"] == "Ж")',
            'r = filterif(m[:, "Возраст"] > 25 and m[:, "Отдел"] == "IT")',
        ],
    },

    'deleteif': {
        'name': 'deleteif',
        'category': 'analytics',
        'args': ['m[:, "X"] == "Y"'],
        'examples': [
            'r = deleteif(m[:, "Пол"] == "Ж")',
            'm = deleteif(m[:, "Пол"] == "Ж")',
        ],
    },

    'delete': {
        'name': 'delete',
        'category': 'analytics',
        'args': [
            'm[N, :]      — удалить строку',
            'm[:, N]      — удалить столбец',
            'm[range, :]  — диапазон строк',
            'm[:, range]  — диапазон столбцов',
        ],
        'examples': [
            'r = delete(m[2, :])',
            'm = delete(m[:, 3])',
            'r = delete(m[10:end, :])',
            'm = delete(m[:, "Имя"])',
        ],
    },
}