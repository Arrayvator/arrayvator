# syntax/autocomplete/items_abc.py
"""
Описания функции abc (ABC-анализ, Парето 80/20).
"""

RU = {
    'abc': {
        'signature': 'abc(срез [, 80, 95] [, %|coef] [, m[:, N]])',
        'description': (
            'ABC-анализ (Парето 80/20).\n'
            '  • Считает накопительную долю по убыванию.\n'
            '  • Присваивает "A" / "B" / "C".\n'
            '  • Порядок строк сохраняется.\n'
            '  • __abc вставляется справа от среза.\n'
            '  • % или coef — доля в отдельный столбец.\n'
            '  • Пороги по умолчанию: 80 / 95.'
        ),
        'example': (
            'r = abc(m[:, "Продажи"])\n'
            'r = abc(m[:, "Продажи"], %)\n'
            'r = abc(m[:, "Продажи"], 70, 90, %, m[:, end+1])'
        ),
        'matrix_example': (
            'm = ["Товар", "Продажи";\n'
            '     "A", 100;\n'
            '     "B", 300;\n'
            '     "C", 600]\n'
            'r = abc(m[:, "Продажи"])\n'
            'print(r)\n'
            '# Товар  Продажи  __abc\n'
            '# A      100      C\n'
            '# B      300      B\n'
            '# C      600      A'
        ),
    },
}


EN = {
    'abc': {
        'signature': 'abc(slice [, 80, 95] [, %|coef] [, m[:, N]])',
        'description': (
            'ABC analysis (Pareto 80/20).\n'
            '  • Cumulative share sorted descending.\n'
            '  • Assigns "A" / "B" / "C".\n'
            '  • Row order is preserved.\n'
            '  • __abc inserted right of the slice.\n'
            '  • % or coef — share into a separate column.\n'
            '  • Default thresholds: 80 / 95.'
        ),
        'example': (
            'r = abc(m[:, "Sales"])\n'
            'r = abc(m[:, "Sales"], %)\n'
            'r = abc(m[:, "Sales"], 70, 90, %, m[:, end+1])'
        ),
        'matrix_example': (
            'm = ["Product", "Sales";\n'
            '     "A", 100;\n'
            '     "B", 300;\n'
            '     "C", 600]\n'
            'r = abc(m[:, "Sales"])\n'
            'print(r)\n'
            '# Product  Sales  __abc\n'
            '# A        100    C\n'
            '# B        300    B\n'
            '# C        600    A'
        ),
    },
}