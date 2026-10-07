# syntax/autocomplete/items_charts.py
"""
Описания функции chart (графики).
"""

RU = {
    'chart': {
        'signature': 'chart(тип, x, y [, title "..." , ...])',
        'description': (
            'Построение графиков.\n'
            '  Типы: bar, line, pie, hist, scatter, box, heatmap, pair.\n'
            '  Опции: title, xlabel, ylabel, color, save, bins, plotly, static.\n'
            '  Правый клик в окне — меню сохранения (PNG, PDF, SVG, JPG).'
        ),
        'example': (
            'chart(bar, m[:, "Отдел"], m[:, "Зарплата"],\n'
            '      title "Зарплаты по отделам")\n'
            'chart(line, m[:, "Месяц"], m[:, "Продажи"])'
        ),
        'matrix_example': (
            'm = ["Отдел", "Зарплата";\n'
            '     "IT", 175000;\n'
            '     "HR", 115000]\n'
            'chart(bar, m[:, "Отдел"], m[:, "Зарплата"],\n'
            '      title "Зарплаты",\n'
            '      save "chart.png")'
        ),
    },
}


EN = {
    'chart': {
        'signature': 'chart(kind, x, y [, title "..." , ...])',
        'description': (
            'Build charts.\n'
            '  Kinds: bar, line, pie, hist, scatter, box, heatmap, pair.\n'
            '  Options: title, xlabel, ylabel, color, save, bins, plotly, static.\n'
            '  Right-click in the chart window — save menu (PNG, PDF, SVG, JPG).'
        ),
        'example': (
            'chart(bar, m[:, "Department"], m[:, "Salary"],\n'
            '      title "Salaries by department")\n'
            'chart(line, m[:, "Month"], m[:, "Sales"])'
        ),
        'matrix_example': (
            'm = ["Department", "Salary";\n'
            '     "IT", 175000;\n'
            '     "HR", 115000]\n'
            'chart(bar, m[:, "Department"], m[:, "Salary"],\n'
            '      title "Salaries",\n'
            '      save "chart.png")'
        ),
    },
}