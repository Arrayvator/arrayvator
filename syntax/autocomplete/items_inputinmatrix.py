# syntax/autocomplete/items_inputinmatrix.py
"""
Описания функции InputInMatrix.
"""

RU = {
    'InputInMatrix': {
        'signature': 'InputInMatrix(матрица [, "Заголовок"] [, строк_контекста])',
        'description': (
            'Визуальное добавление строк в матрицу.\n'
            '  • Открывает окно с контекстом (последние N строк).\n'
            '  • Поля ввода ПО ЧИСЛУ СТОЛБЦОВ, горизонтально.\n'
            '  • «Добавить» (Enter) — строка появляется в таблице.\n'
            '  • «Завершить» (Ctrl+Enter) — вернуть новую матрицу.\n'
            '  • Крестик / Esc — отмена, вернуть ИСХОДНУЮ матрицу.\n'
            '  • Работает только с 2D-матрицами.\n'
            '  • Возвращает НОВУЮ матрицу — результат нужно сохранить.'
        ),
        'example': (
            'm = InputInMatrix(m)\n'
            'm = InputInMatrix(m, "Сотрудники")\n'
            'm = InputInMatrix(m, "Сотрудники", 5)'
        ),
        'matrix_example': (
            '# ДАНО:\n'
            '#   m = ["Имя", "Отдел";\n'
            '#        "Аня", "IT"]\n'
            '\n'
            '# Окно с полями: Имя, Отдел\n'
            'm = InputInMatrix(m, "Сотрудники")\n'
            'print(m)'
        ),
    },
}

EN = {
    'InputInMatrix': {
        'signature': 'InputInMatrix(matrix [, "Title"] [, preview_rows])',
        'description': (
            'Visual row addition to a matrix.\n'
            '  • Opens a window with context (last N rows).\n'
            '  • Input fields PER COLUMN, horizontally.\n'
            '  • "Add" (Enter) — row appears in the table.\n'
            '  • "Finish" (Ctrl+Enter) — return the new matrix.\n'
            '  • Close / Esc — cancel, return the SOURCE matrix.\n'
            '  • Works only with 2D matrices.\n'
            '  • Returns a NEW matrix — save the result.'
        ),
        'example': (
            'm = InputInMatrix(m)\n'
            'm = InputInMatrix(m, "Employees")\n'
            'm = InputInMatrix(m, "Employees", 5)'
        ),
        'matrix_example': (
            '# INPUT:\n'
            '#   m = ["Name", "Dept";\n'
            '#        "Anna", "IT"]\n'
            '\n'
            '# Window with fields: Name, Dept\n'
            'm = InputInMatrix(m, "Employees")\n'
            'print(m)'
        ),
    },
}