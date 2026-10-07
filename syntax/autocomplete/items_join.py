# syntax/autocomplete/items_join.py
"""
Описания функции join (соединение таблиц).
"""

RU = {
    'join': {
        'signature': 'join(m1, m2, on "ID" [, how "left"])',
        'description': (
            'Соединение таблиц по ключу.\n'
            'how: left (по умолчанию), inner, right, outer.'
        ),
        'example': (
            'r = join(m1, m2, on "ID")\n'
            'r = join(m1, m2, on "ID", how "inner")'
        ),
    },
}


EN = {
    'join': {
        'signature': 'join(m1, m2, on "ID" [, how "left"])',
        'description': (
            'Join tables by key.\n'
            'how: left (default), inner, right, outer.'
        ),
        'example': (
            'r = join(m1, m2, on "ID")\n'
            'r = join(m1, m2, on "ID", how "inner")'
        ),
    },
}