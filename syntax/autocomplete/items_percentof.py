# syntax/autocomplete/items_percentof.py
"""
Описания функции percentof (доля от итога).
"""

RU = {
    'percentof': {
        'signature': 'percentof(срез [, coef] [, by m[:, "Y"]])',
        'description': (
            '💯 ДОЛЯ ОТ ИТОГА\n'
            '\n'
            'ЗАЧЕМ НУЖНА:\n'
            '  • Показать, какую ЧАСТЬ от общей суммы составляет каждое значение.\n'
            '  • Классика: "доля товара в общей выручке".\n'
            '  • Основа ABC-анализа и Парето 80/20.\n'
            '\n'
            'ДВА ФОРМАТА:\n'
            '  • Без coef — ПРОЦЕНТЫ (0–100), округление 2 знака.\n'
            '  • С coef — КОЭФФИЦИЕНТ (0.0–1.0), округление 4 знака.\n'
            '\n'
            'С ГРУППИРОВКОЙ (by):\n'
            '  • Без by — доля от ОБЩЕГО итога.\n'
            '  • С by — доля от итога внутри ГРУППЫ.\n'
            '\n'
            'КАКИЕ ЗАДАЧИ РЕШАЕТ:\n'
            '  • "Какую долю в продажах занимает каждый товар".\n'
            '  • "Процент брака от общего производства".\n'
            '  • "Доля каждого магазина внутри своего региона".\n'
            '  • ABC-анализ: где 80% выручки — там ключевые товары.\n'
            '\n'
            'ПРАВИЛА:\n'
            '  • Возвращает ВЕКТОР той же длины, что и срез.\n'
            '  • Записывается в столбец через addcolumn.\n'
            '  • Работает с Matrix и DuckDB.'
        ),
        'example': (
            'm = addcolumn(m, "Доля_%", percentof(m[:, "Продажи"]))\n'
            'm = addcolumn(m, "Доля_кат_%",\n'
            '              percentof(m[:, "Продажи"], by m[:, "Категория"]))\n'
            'r = percentof(m[:, "Продажи"], coef)'
        ),
        'matrix_example': (
            '# ДАНО:\n'
            '#\n'
            '#   m = ["Товар",   "Категория", "Продажи";\n'
            '#        "Молоко",  "Молочка",   800;\n'
            '#        "Сыр",     "Молочка",   200;\n'
            '#        "Батон",   "Хлеб",      500]\n'
            '\n'
            '# ЗАДАЧА 1: доля от ОБЩЕГО итога\n'
            'r1 = percentof(m[:, "Продажи"])\n'
            'print(r1)\n'
            '#\n'
            '# ВЫВОД: [53.33, 13.33, 33.33]\n'
            '# Общая сумма = 1500\n'
            '# 800/1500 = 53.33%, 200/1500 = 13.33%, 500/1500 = 33.33%\n'
            '\n'
            '# ЗАДАЧА 2: доля ВНУТРИ КАТЕГОРИИ\n'
            'r2 = percentof(m[:, "Продажи"], by m[:, "Категория"])\n'
            'print(r2)\n'
            '#\n'
            '# ВЫВОД: [80.0, 20.0, 100.0]\n'
            '# Молочка: 800+200 = 1000 → 800/1000=80%, 200/1000=20%\n'
            '# Хлеб: 500 → 500/500=100%'
        ),
    },
}


EN = {
    'percentof': {
        'signature': 'percentof(slice [, coef] [, by m[:, "Y"]])',
        'description': (
            '💯 SHARE OF TOTAL\n'
            '\n'
            'WHY NEEDED:\n'
            '  • Show what PART of the total each value represents.\n'
            '  • Classic: "product share in total revenue".\n'
            '  • Base of ABC analysis and Pareto 80/20.\n'
            '\n'
            'TWO FORMATS:\n'
            '  • Without coef — PERCENT (0–100), 2 decimals.\n'
            '  • With coef — RATIO (0.0–1.0), 4 decimals.\n'
            '\n'
            'WITH GROUPING (by):\n'
            '  • Without by — share of GRAND total.\n'
            '  • With by — share within GROUP.\n'
            '\n'
            'TASKS IT SOLVES:\n'
            '  • "What share of sales does each product have".\n'
            '  • "Defect percentage of total production".\n'
            '  • "Share of each store within its region".\n'
            '  • ABC analysis: where 80% of revenue is.\n'
            '\n'
            'RULES:\n'
            '  • Returns a VECTOR of the same length as the slice.\n'
            '  • Write to a column via addcolumn.\n'
            '  • Works with Matrix and DuckDB.'
        ),
        'example': (
            'm = addcolumn(m, "Share_%", percentof(m[:, "Sales"]))\n'
            'm = addcolumn(m, "Cat_share_%",\n'
            '              percentof(m[:, "Sales"], by m[:, "Category"]))\n'
            'r = percentof(m[:, "Sales"], coef)'
        ),
    },
}