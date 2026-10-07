# syntax/autocomplete/items_pivot.py
"""
Описания функции pivot (сводная таблица).
"""

RU = {
    'pivot': {
        'signature': (
            'pivot(ключ, значения, агрегат)\n'
            'pivot(ключ_строк, ключ_столбцов, значения, агрегат)'
        ),
        'description': (
            '📊 СВОДНАЯ ТАБЛИЦА (аналог Excel Pivot)\n'
            '\n'
            'ЗАЧЕМ НУЖНА:\n'
            '  • Превратить длинные данные в широкий крест-отчёт.\n'
            '  • "Одна строка на ключ, столбцы = значения второго ключа".\n'
            '  • Классика Excel: "продажи по месяцам × товарам".\n'
            '\n'
            'МНЕМОНИКА (один ключ):\n'
            '     pivot( ключ , значения , агрегат )\n'
            '            └─a─┘   └──b───┘   └──c──┘\n'
            '            группы  что считать как считать\n'
            '\n'
            'МНЕМОНИКА (два ключа):\n'
            '     pivot( ключ_строк , ключ_столбцов , значения , агрегат )\n'
            '            └────a────┘  └─────b──────┘   └──c───┘   └──d───┘\n'
            '            строки        столбцы          что считать как считать\n'
            '\n'
            'ДВА РЕЖИМА:\n'
            '  • 3 аргумента — один ключ. Простая сводка (2 столбца).\n'
            '  • 4 аргумента — два ключа. Крест-таблица (строки × столбцы).\n'
            '\n'
            'ДОСТУПНЫЕ АГРЕГАТЫ:\n'
            '  sum, avg, count, min, max, median, first, last, std\n'
            '\n'
            'КАКИЕ ЗАДАЧИ РЕШАЕТ:\n'
            '  • "Продажи по отделам × годам".\n'
            '  • "Количество сотрудников по отделам × городам".\n'
            '  • "Средний чек по магазинам × дням недели".\n'
            '  • Крест-отчёт для руководства.\n'
            '\n'
            'ПРАВИЛА:\n'
            '  • Порядок строк/столбцов — по первому появлению.\n'
            '  • Пустые ячейки → None.\n'
            '  • Все аргументы — срезы m[:, "X"], кроме агрегата.\n'
            '  • Работает с Matrix и DuckDB.'
        ),
        'example': (
            '# Один ключ — простая сводка\n'
            'r = pivot(m[:, "Отдел"], m[:, "Зарплата"], sum)\n'
            '\n'
            '# Два ключа — pivot-таблица\n'
            'r = pivot(m[:, "Отдел"], m[:, "Год"], m[:, "Зарплата"], sum)'
        ),
        'matrix_example': (
            '# ДАНО:\n'
            '#\n'
            '#   m = ["Отдел", "Год",  "Зарплата";\n'
            '#        "IT",     2023, 85000;\n'
            '#        "IT",     2023, 95000;\n'
            '#        "IT",     2024, 70000;\n'
            '#        "HR",     2023, 65000;\n'
            '#        "HR",     2024, 72000;\n'
            '#        "Sales",  2023, 80000;\n'
            '#        "Sales",  2024, 88000;\n'
            '#        "Sales",  2024, 60000]\n'
            '\n'
            '# ЗАДАЧА 1: простая сводка — один ключ\n'
            'r1 = pivot(m[:, "Отдел"], m[:, "Зарплата"], sum)\n'
            'print(r1)\n'
            '#\n'
            '# ВЫВОД:\n'
            '#   Отдел   Значение\n'
            '#   IT      250000\n'
            '#   HR      137000\n'
            '#   Sales   228000\n'
            '\n'
            '# ЗАДАЧА 2: крест-таблица — два ключа\n'
            'r2 = pivot(m[:, "Отдел"], m[:, "Год"], m[:, "Зарплата"], sum)\n'
            'print(r2)\n'
            '#\n'
            '# ВЫВОД (строки × столбцы):\n'
            '#   Отдел   2023     2024\n'
            '#   IT      180000   70000\n'
            '#   HR      65000    72000\n'
            '#   Sales   80000    148000'
        ),
    },
}


EN = {
    'pivot': {
        'signature': (
            'pivot(key, values, agg)\n'
            'pivot(row_key, col_key, values, agg)'
        ),
        'description': (
            '📊 PIVOT TABLE (analog of Excel Pivot)\n'
            '\n'
            'WHY NEEDED:\n'
            '  • Turn long data into a wide cross-report.\n'
            '  • "One row per key, columns = second key values".\n'
            '  • Excel classic: "sales by months × products".\n'
            '\n'
            'MNEMONIC (one key):\n'
            '     pivot( key , values , agg )\n'
            '            └─a─┘  └──b───┘  └─c─┘\n'
            '            groups  what     how\n'
            '\n'
            'MNEMONIC (two keys):\n'
            '     pivot( row_key , col_key , values , agg )\n'
            '            └───a───┘  └──b───┘  └──c───┘  └─d─┘\n'
            '            rows       columns  what     how\n'
            '\n'
            'TWO MODES:\n'
            '  • 3 args — one key. Simple summary (2 columns).\n'
            '  • 4 args — two keys. Cross-table (rows × columns).\n'
            '\n'
            'AVAILABLE AGGREGATES:\n'
            '  sum, avg, count, min, max, median, first, last, std\n'
            '\n'
            'TASKS IT SOLVES:\n'
            '  • "Sales by departments × years".\n'
            '  • "Employee count by departments × cities".\n'
            '  • "Average check by stores × weekdays".\n'
            '  • Cross-report for management.\n'
            '\n'
            'RULES:\n'
            '  • Row/column order — first appearance.\n'
            '  • Empty cells → None.\n'
            '  • All args — slices m[:, "X"], except agg.\n'
            '  • Works with Matrix and DuckDB.'
        ),
        'example': (
            '# One key — simple summary\n'
            'r = pivot(m[:, "Department"], m[:, "Salary"], sum)\n'
            '\n'
            '# Two keys — pivot table\n'
            'r = pivot(m[:, "Department"], m[:, "Year"], m[:, "Salary"], sum)'
        ),
    },
}