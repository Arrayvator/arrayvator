# syntax/autocomplete/items_anomaly.py
"""
Описания функции anomaly (поиск аномалий).
"""

RU = {
    'anomaly': {
        'signature': (
            'anomaly(срез [, iqr|zscore|percentile] [, N] '
            '[, by ...] [, only] [, approx])'
        ),
        'description': (
            '🔍 ПОИСК АНОМАЛИЙ (выбросов)\n'
            '\n'
            'ЗАЧЕМ НУЖНА:\n'
            '  • Найти значения, которые "выбиваются" из общего ряда.\n'
            '  • Классика: "какие продажи — фрод, а какие норма".\n'
            '  • Контроль качества, безопасность, финансы.\n'
            '\n'
            'ТРИ МЕТОДА:\n'
            '\n'
            '  ▸ iqr (по умолчанию, k=1.5)\n'
            '    Межквартильный размах. Работает без предположений\n'
            '    о распределении. Устойчив к выбросам.\n'
            '    Границы: Q1 − k·IQR и Q3 + k·IQR.\n'
            '\n'
            '  ▸ zscore (N=3 по умолчанию)\n'
            '    Отклонение от среднего. Предполагает нормальное\n'
            '    распределение. N=2 — мягче, N=3 — строже.\n'
            '\n'
            '  ▸ percentile (1, 99 по умолчанию)\n'
            '    Значения ниже lo% или выше hi% — аномалии.\n'
            '\n'
            'РЕЖИМЫ:\n'
            '  • by — искать аномалии ВНУТРИ каждой группы.\n'
            '  • only — вернуть ТОЛЬКО аномальные строки.\n'
            '  • approx — приблизительные процентили (быстро, DuckDB).\n'
            '\n'
            'СТОЛБЕЦ РЕЗУЛЬТАТА __anomaly:\n'
            '  • 0    — норма\n'
            '  • 1    — ВЫШЕ верхней границы\n'
            '  • -1   — НИЖЕ нижней границы\n'
            '  • None — если в группе меньше 4 значений\n'
            '\n'
            'ВАЖНО:\n'
            '  • Для групп < 4 значений аномалии не считаются (None).\n'
            '  • Если IQR = 0 (все значения одинаковые) → все 0.\n'
            '  • Работает с Matrix и DuckDB.'
        ),
        'example': (
            'r = anomaly(m[:, "Сумма"])                        # iqr\n'
            'r = anomaly(m[:, "Сумма"], zscore, 2)              # zscore\n'
            'r = anomaly(m[:, "Сумма"], percentile, 5, 95)      # percentile\n'
            'r = anomaly(m[:, "Сумма"], by m[:, "Магазин"])     # по группам\n'
            'r = anomaly(m[:, "Сумма"], only, approx)           # только аномалии'
        ),
        'matrix_example': (
            '# ДАНО:\n'
            '#\n'
            '#   m = ["Магазин", "Сумма";\n'
            '#        "М1", 1500;\n'
            '#        "М1", 1800;\n'
            '#        "М1", 2000;\n'
            '#        "М1", 500000;     ← явная аномалия\n'
            '#        "М2", 300000;\n'
            '#        "М2", 320000;\n'
            '#        "М2", 310000;\n'
            '#        "М2", 305000]\n'
            '\n'
            '# ЗАДАЧА: найти аномалии ВНУТРИ каждого магазина\n'
            '#         (у М1 — один масштаб, у М2 — другой)\n'
            'r = anomaly(m[:, "Сумма"], by m[:, "Магазин"])\n'
            'print(r)\n'
            '\n'
            '# ВЫВОД:\n'
            '#\n'
            '#   Магазин  Сумма    __anomaly\n'
            '#   М1       1500     0\n'
            '#   М1       1800     0\n'
            '#   М1       2000     0\n'
            '#   М1       500000   1     ← аномалия для М1\n'
            '#   М2       300000   0\n'
            '#   М2       320000   0\n'
            '#   М2       310000   0\n'
            '#   М2       305000   0\n'
            '\n'
            '# БЕЗ by функция сравнила бы 500000 и 320000\n'
            '# в одной группе — и не нашла бы ничего.\n'
            '# С by — масштаб М1 и М2 независимый. 500000 — аномалия.'
        ),
    },
}


EN = {
    'anomaly': {
        'signature': (
            'anomaly(slice [, iqr|zscore|percentile] [, N] '
            '[, by ...] [, only] [, approx])'
        ),
        'description': (
            '🔍 OUTLIER DETECTION\n'
            '\n'
            'WHY NEEDED:\n'
            '  • Find values that "stand out" from the general series.\n'
            '  • Classic: "which sales are fraud, which are normal".\n'
            '  • Quality control, security, finance.\n'
            '\n'
            'THREE METHODS:\n'
            '\n'
            '  ▸ iqr (default, k=1.5)\n'
            '    Interquartile range. No distribution assumptions.\n'
            '    Robust to outliers.\n'
            '    Bounds: Q1 − k·IQR and Q3 + k·IQR.\n'
            '\n'
            '  ▸ zscore (N=3 default)\n'
            '    Deviation from mean. Assumes normal distribution.\n'
            '    N=2 — softer, N=3 — stricter.\n'
            '\n'
            '  ▸ percentile (1, 99 default)\n'
            '    Values below lo% or above hi% are anomalies.\n'
            '\n'
            'MODES:\n'
            '  • by — find anomalies WITHIN each group.\n'
            '  • only — return ONLY anomalous rows.\n'
            '  • approx — approximate percentiles (fast, DuckDB).\n'
            '\n'
            'RESULT COLUMN __anomaly:\n'
            '  • 0    — normal\n'
            '  • 1    — ABOVE upper bound\n'
            '  • -1   — BELOW lower bound\n'
            '  • None — if group has fewer than 4 values\n'
            '\n'
            'IMPORTANT:\n'
            '  • For groups < 4 values, anomalies are not computed (None).\n'
            '  • If IQR = 0 (all values equal) → all 0.\n'
            '  • Works with Matrix and DuckDB.'
        ),
        'example': (
            'r = anomaly(m[:, "Amount"])                        # iqr\n'
            'r = anomaly(m[:, "Amount"], zscore, 2)              # zscore\n'
            'r = anomaly(m[:, "Amount"], percentile, 5, 95)      # percentile\n'
            'r = anomaly(m[:, "Amount"], by m[:, "Store"])       # by group\n'
            'r = anomaly(m[:, "Amount"], only, approx)           # only anomalies'
        ),
    },
}