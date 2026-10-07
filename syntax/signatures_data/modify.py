# syntax/signatures_data/modify.py
"""
Сигнатуры: вставка / копирование / перемещение / склейка / разворот.
"""

SIGNATURES = {
    'insert': {
        'name': 'insert',
        'category': 'analytics',
        'args': ['индекс', 'before | after'],
        'examples': [
            'r = insert(m[2, :], before)',
            'm = insert(m[:, 2], after)',
            'r = insert(v, 3, after)',
        ],
    },

    'copy': {
        'name': 'copy',
        'category': 'analytics',
        'args': ['источник', 'цель', 'before | after'],
        'examples': [
            'r = copy(m[:, 1], m[:, 10], after)',
            'm = copy(m[:, 1:3], m[:, 10], after)',
        ],
    },

    'move': {
        'name': 'move',
        'category': 'analytics',
        'args': ['источник', 'цель', 'before | after'],
        'examples': [
            'r = move(m[:, 1], m[:, 10], after)',
            'm = move(m[1:10, :], m[end, :], after)',
        ],
    },

    'joinarray': {
        'name': 'joinarray',
        'category': 'analytics',
        'args': ['m1', 'm2', '...', 'vertical | horizontal'],
        'examples': [
            'r = joinarray(m1, m2, vertical)',
            'a = joinarray(a, b, horizontal)',
        ],
    },

    'unpivot': {
        'name': 'unpivot',
        'category': 'analytics',
        'args': [
            'срез данных',
            'by срез-идентификатор',
            'names "A", "B" (опц.)',
        ],
        'examples': [
            'r = unpivot(m[:, 2:end], by m[:, "Страна"])',
            'r = unpivot(m[:, 2:end], by m[:, "Страна"], names "Год", "Население")',
        ],
    },

    'transpose': {
        'name': 'transpose',
        'category': 'create',
        'args': ['матрица или вектор'],
        'examples': [
            'r = transpose(m)',
            'm = transpose(m)',
        ],
    },
}