# syntax/autocomplete/items_sort.py
"""
Описания функции сортировки: sort.
"""

RU = {
    'sort': {
        'signature': 'sort(m[:, "X"], AZ | ZA)',
        'description': (
            'Сортирует строки таблицы по указанному столбцу.\n'
            '  • Работает с Matrix и DuckDB.\n'
            '  • AZ — по возрастанию, ZA — по убыванию.\n'
            '  • Возвращает НОВУЮ матрицу. Для мутации: `m = sort(...)`.'
        ),
        'example': (
            'r = sort(m[:, "Имя"], AZ)\n'
            'm = sort(m[:, "Имя"], AZ)'
        ),
        'matrix_example': (
            '# ДАНО:\n'
            '#\n'
            '#   m = ["Имя", "Возраст";\n'
            '#        "Света", 28;\n'
            '#        "Аня",   25;\n'
            '#        "Боб",   32]\n'
            '\n'
            '# Сортировка по возрасту по возрастанию\n'
            'r = sort(m[:, "Возраст"], AZ)\n'
            'print(r)\n'
            '\n'
            '# ВЫВОД:\n'
            '#\n'
            '#   Имя    Возраст\n'
            '#   Аня    25\n'
            '#   Света  28\n'
            '#   Боб    32'
        ),
    },
}


EN = {
    'sort': {
        'signature': 'sort(m[:, "X"], AZ | ZA)',
        'description': (
            'Sorts rows of the table by the specified column.\n'
            '  • Works with Matrix and DuckDB.\n'
            '  • AZ — ascending, ZA — descending.\n'
            '  • Returns a NEW matrix. For mutation: `m = sort(...)`.'
        ),
        'example': (
            'r = sort(m[:, "Name"], AZ)\n'
            'm = sort(m[:, "Name"], AZ)'
        ),
        'matrix_example': (
            '# INPUT:\n'
            '#\n'
            '#   m = ["Name", "Age";\n'
            '#        "Eve",  28;\n'
            '#        "Anna", 25;\n'
            '#        "Bob",  32]\n'
            '\n'
            '# Sort by age ascending\n'
            'r = sort(m[:, "Age"], AZ)\n'
            'print(r)\n'
            '\n'
            '# OUTPUT:\n'
            '#\n'
            '#   Name  Age\n'
            '#   Anna  25\n'
            '#   Eve   28\n'
            '#   Bob   32'
        ),
    },
}