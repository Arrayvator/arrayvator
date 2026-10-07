# syntax/signatures_data/search.py
"""
Сигнатуры функций поиска: find, vlookup.
"""

SIGNATURES = {
    'find': {
        'name': 'find',
        'category': 'analytics',
        'args': [
            'm[:, "X"] == "Y"',
            'inside | ignore (опц.)',
            'rows | cols (опц.)',
        ],
        'examples': [
            'r = find(m[:, "Имя"] == "Иванов")             # координаты',
            'r = find(m[:, "Имя"] == "ов", inside)         # подстрока',
            'r = find(m[:, "Имя"] == "аня", ignore)        # без регистра',
            'r = find(m[:, "Отдел"] == "IT", rows)         # номера строк',
            'r = find(m[:, "Отдел"] == "IT", cols)         # номера столбцов',
        ],
    },

    'vlookup': {
        'name': 'vlookup',
        'category': 'analytics',
        'args': [
            'срез_поиска — где искать (a[:, "ID"])',
            'что_искать — скаляр или вектор (b[:, "ID"])',
            'срез_возврата — что вернуть (a[:, "Отдел"])',
        ],
        'examples': [
            '# Скалярный поиск',
            'r = vlookup(a[:, "ID"], 101, a[:, "Отдел"])',

            '# По имени',
            'r = vlookup(a[:, "Имя"], "Аня", a[:, "Отдел"])',

            '# Векторный поиск — обогащение таблицы',
            'b[:, end+1] = vlookup(a[:, "ID"], b[:, "ID"], a[:, "Отдел"])',
        ],
    },
}