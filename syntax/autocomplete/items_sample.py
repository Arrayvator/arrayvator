# syntax/autocomplete/items_sample.py
"""
Описания функции sample.
"""

RU = {
    'sample': {
        'signature': 'sample(m, N [, seed])',
        'description': (
            'Возвращает N случайных строк из таблицы.\n'
            '  • seed — для воспроизводимости результата (опционально).\n'
            '  • Работает с Matrix и DuckDB (мгновенно).'
        ),
        'example': (
            'r = sample(m, 1000)          # 1000 случайных строк\n'
            'r = sample(m, 100, 42)       # 100 строк, seed=42'
        ),
        'matrix_example': (
            '# ДАНО:\n'
            '#\n'
            '#   m = ["A", "B";\n'
            '#        1, 2;\n'
            '#        3, 4;\n'
            '#        5, 6;\n'
            '#        7, 8;\n'
            '#        9, 10]\n'
            '\n'
            '# Получить 3 случайные строки с seed для воспроизводимости\n'
            'r = sample(m, 3, 42)\n'
            'print(r)\n'
            '\n'
            '# ВЫВОД (примерный, зависит от seed):\n'
            '#\n'
            '#   A  B\n'
            '#   3  4\n'
            '#   9  10\n'
            '#   1  2'
        ),
    },
}


EN = {
    'sample': {
        'signature': 'sample(m, N [, seed])',
        'description': (
            'Returns N random rows from the table.\n'
            '  • seed — for reproducibility (optional).\n'
            '  • Works with Matrix and DuckDB (instantly).'
        ),
        'example': (
            'r = sample(m, 1000)          # 1000 random rows\n'
            'r = sample(m, 100, 42)       # 100 rows, seed=42'
        ),
        'matrix_example': (
            '# INPUT:\n'
            '#\n'
            '#   m = ["A", "B";\n'
            '#        1, 2;\n'
            '#        3, 4;\n'
            '#        5, 6;\n'
            '#        7, 8;\n'
            '#        9, 10]\n'
            '\n'
            '# Get 3 random rows with a seed for reproducibility\n'
            'r = sample(m, 3, 42)\n'
            'print(r)\n'
            '\n'
            '# OUTPUT (example, depends on seed):\n'
            '#\n'
            '#   A  B\n'
            '#   3  4\n'
            '#   9  10\n'
            '#   1  2'
        ),
    },
}