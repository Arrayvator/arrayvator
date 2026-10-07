# syntax/signatures_data/anomaly.py
"""
Сигнатуры функции anomaly (поиск аномалий).
"""

SIGNATURES = {
    'anomaly': {
        'name': 'anomaly',
        'category': 'analytics',
        'args': [
            'срез значений (m[:, "X"])',
            'iqr | zscore | percentile — метод (опц.)',
            'число — параметр метода (опц.)',
            'by m[:, "Y"] (опц.) — группировка',
            'only (опц.) — только аномалии',
            'approx (опц.) — приблизительные процентили (DuckDB)',
        ],
        'examples': [
            'r = anomaly(m[:, "Сумма"])',
            'r = anomaly(m[:, "Сумма"], zscore)',
            'r = anomaly(m[:, "Сумма"], zscore, 2)',
            'r = anomaly(m[:, "Сумма"], percentile, 5, 95)',
            'r = anomaly(m[:, "Сумма"], iqr, 3.0)',
            'r = anomaly(m[:, "Сумма"], by m[:, "Магазин"])',
            'r = anomaly(m[:, "Сумма"], only)',
            'r = anomaly(m[:, "Сумма"], by m[:, "Магазин"], iqr, approx, only)',
        ],
    },
}