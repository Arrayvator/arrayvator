# syntax/signatures_data/dedup.py
"""
Сигнатуры функций работы с дубликатами.
"""

SIGNATURES = {
    'unique': {
        'name': 'Unique',
        'category': 'deduplicate',
        'args': ['срез или вектор'],
        'examples': [
            'r = Unique(v)',
            'm = Unique(m[:, "Отдел"])',
            'r = Unique(m)',
        ],
    },

    'countdistinct': {
        'name': 'CountDistinct',
        'category': 'deduplicate',
        'args': ['срез или вектор'],
        'examples': [
            'r = CountDistinct(v)',
            'r = CountDistinct(m[:, "Отдел"])',
        ],
    },

    'valuecounts': {
        'name': 'ValueCounts',
        'category': 'deduplicate',
        'args': ['срез или вектор'],
        'examples': [
            'r = ValueCounts(v)',
            'r = ValueCounts(m[:, "Отдел"])',
        ],
    },

    'deleteduplicate': {
        'name': 'DeleteDuplicate',
        'category': 'deduplicate',
        'args': ['срез или вектор'],
        'examples': [
            'r = DeleteDuplicate(v)',
            'm = DeleteDuplicate(m[:, "Отдел"])',
        ],
    },
}