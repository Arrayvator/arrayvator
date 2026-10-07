# syntax/signatures_data/addcolumn.py
"""
Сигнатуры функций addcolumn, addrows.
"""

SIGNATURES = {
    'addcolumn': {
        'name': 'addcolumn',
        'category': 'analytics',
        'args': [
            'таблица (Matrix или DuckDB)',
            '"Имя нового столбца"',
            'выражение',
        ],
        'examples': [
            'm2 = addcolumn(m, "Сумма", m[:, "ID"] + m[:, "ID_10"])',
            'm2 = addcolumn(m, "Год", 2024)',
            'm2 = addcolumn(m, "Статус", "новый")',
            'm2 = addcolumn(m, "Цена_НДС", round(m[:, "Цена"] * 1.2, 2))',
        ],
    },

    'addrows': {
        'name': 'addrows',
        'category': 'analytics',
        'args': ['таблица', 'N', 'fill (опц.)'],
        'examples': [
            'm2 = addrows(m, 5)',
            'm2 = addrows(m, 3, 0)',
            'm2 = addrows(m, 2, "-")',
        ],
    },
}