# syntax/signatures_data/percentof.py
"""
Сигнатуры функции percentof (доля от итога).
"""

SIGNATURES = {
    'percentof': {
        'name': 'percentof',
        'category': 'analytics',
        'args': [
            'срез значений (m[:, "X"])',
            'coef (опц.) — коэффициент вместо процентов',
            'by m[:, "Y"] (опц.) — группировка',
        ],
        'examples': [
            'r = percentof(m[:, "Продажи"])',
            'r = percentof(m[:, "Продажи"], coef)',
            'r = percentof(m[:, "Продажи"], by m[:, "Категория"])',
            'r = percentof(m[:, "Продажи"], by m[:, "Категория"], coef)',
            'm = addcolumn(m, "Доля_%", percentof(m[:, "Продажи"]))',
        ],
    },
}