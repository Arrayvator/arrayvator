# syntax/autocomplete/items_addcolumn.py
"""
Описания функций addcolumn, addrows.
"""

RU = {
    'addcolumn': {
        'signature': 'addcolumn(m, "Имя", выражение)',
        'description': (
            'Добавляет новый столбец в таблицу.\n'
            '  • Работает с Matrix и DuckDB\n'
            '  • Всегда возвращает НОВУЮ таблицу\n'
            '  • Выражение — арифметика, скаляр, функция'
        ),
        'example': (
            'm2 = addcolumn(m, "Сумма", m[:, "ID"] + m[:, "ID_10"])\n'
            'm2 = addcolumn(m, "Год", 2024)\n'
            'm2 = addcolumn(m, "Цена_НДС", round(m[:, "Цена"] * 1.2, 2))'
        ),
        'matrix_example': (
            'm = ["ID", "ID_10"; 1, 11; 2, 12; 3, 13]\n'
            'm2 = addcolumn(m, "Сумма", m[:, "ID"] + m[:, "ID_10"])\n'
            'print(m2)'
        ),
    },
    'addrows': {
        'signature': 'addrows(таблица, N [, fill])',
        'description': (
            'Добавляет N строк в конец таблицы.\n'
            '  • без fill — строки пустые (None)\n'
            '  • с fill — заполнены указанным значением'
        ),
        'example': (
            'm2 = addrows(m, 5)\n'
            'm2 = addrows(m, 3, 0)\n'
            'm2 = addrows(m, 2, "-")'
        ),
        'matrix_example': (
            'm = ["A", "B"; 1, 2; 3, 4]\n'
            'm2 = addrows(m, 2, 0)\n'
            'print(m2)'
        ),
    },
}


EN = {
    'addcolumn': {
        'signature': 'addcolumn(m, "Name", expression)',
        'description': (
            'Add a new column to the table.\n'
            '  • Works with Matrix and DuckDB\n'
            '  • Always returns a NEW table\n'
            '  • Expression — arithmetic, scalar, function'
        ),
        'example': (
            'm2 = addcolumn(m, "Sum", m[:, "ID"] + m[:, "ID_10"])\n'
            'm2 = addcolumn(m, "Year", 2024)\n'
            'm2 = addcolumn(m, "Price_VAT", round(m[:, "Price"] * 1.2, 2))'
        ),
        'matrix_example': (
            'm = ["ID", "ID_10"; 1, 11; 2, 12; 3, 13]\n'
            'm2 = addcolumn(m, "Sum", m[:, "ID"] + m[:, "ID_10"])\n'
            'print(m2)'
        ),
    },
    'addrows': {
        'signature': 'addrows(table, N [, fill])',
        'description': (
            'Add N rows to the end of the table.\n'
            '  • without fill — empty rows (None)\n'
            '  • with fill — filled with the specified value'
        ),
        'example': (
            'm2 = addrows(m, 5)\n'
            'm2 = addrows(m, 3, 0)\n'
            'm2 = addrows(m, 2, "-")'
        ),
        'matrix_example': (
            'm = ["A", "B"; 1, 2; 3, 4]\n'
            'm2 = addrows(m, 2, 0)\n'
            'print(m2)'
        ),
    },
}