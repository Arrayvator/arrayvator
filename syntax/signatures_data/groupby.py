# syntax/signatures_data/groupby.py
"""
Сигнатуры функций группировки: groupby, groupagg, filldown.
"""

SIGNATURES = {
    'groupby': {
        'name': 'groupby',
        'category': 'analytics',
        'args': [
            'by срез-ключ [,...]',
            'agg агрегат [, ...]',
            'having агрегат ОП значение (опц.)',
        ],
        'examples': [
            'r = groupby(by m[:, "Отдел"], agg sum(m[:, "Зарплата"]))',
            'r = groupby(by m[:, "Отдел"], m[:, "Год"], agg sum(m[:, "Продажи"]))',
            'r = groupby(by m[:, "Отдел"], agg sum(m[:, "X"]), avg(m[:, "Y"]), count())',
            'r = groupby(by m[:, "Отдел"], agg sum(m[:, "X"]), having sum(m[:, "X"]) > 100)',
        ],
    },

    'groupagg': {
        'name': 'groupagg',
        'category': 'analytics',
        'args': [
            'ключ-срез',
            'значение-срез',
            'agg',
            'имя (опц.)',
            'fill | exact (опц.)',
        ],
        'examples': [
            'r = groupagg(m[:, "Клиент"], m[:, "Сумма"], sum)',
            'r = groupagg(m[:, "Клиент"], m[:, "Сумма"], sum, "ИТОГО")',
        ],
    },

    'filldown': {
        'name': 'filldown',
        'category': 'analytics',
        'args': ['срез', 'маркер пустоты (опц.)'],
        'examples': [
            'r = filldown(m[:, "Клиент"])',
            'r = filldown(m[:, "Клиент"], "-")',
        ],
    },
}