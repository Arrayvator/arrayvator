# errors/functions_db/addcolumn.py
"""
База ошибок для функций ADDCOLUMN и ADDROWS.

ADDCOLUMN:
    addcolumn(таблица, "Имя", выражение)

ADDROWS:
    addrows(таблица, N [, fill])

ВАЖНО:
    Этот файл — БАЗА ОШИБОК. В нём только словари RU и EN.
    Никаких классов, импортов, функций.
"""


RU = {
    'addcolumn': {
        'name': 'addcolumn',
        'category': 'analytics',
        'signature': 'addcolumn(таблица, "Имя", выражение)',
        'description': (
            'Добавляет новый столбец в таблицу.\n'
            '  • Работает с Matrix (RAM) и DuckDB (BigData).\n'
            '  • Всегда возвращает НОВУЮ таблицу.\n'
            '  • Выражение — скаляр, вектор, арифметика, функция.'
        ),
        'examples': [
            'm2 = addcolumn(m, "Сумма", m[:, "ID"] + m[:, "ID_10"])',
            'm2 = addcolumn(m, "Год", 2024)',
            'm2 = addcolumn(m, "Статус", "новый")',
            'm2 = addcolumn(m, "Цена_НДС", round(m[:, "Цена"] * 1.2, 2))',
        ],
        'errors': {
            'ADDCOLUMN_BAD_SYNTAX': {
                'message': (
                    "addcolumn: неверное количество аргументов.\n"
                    "  Нужно ровно ТРИ: таблица, имя столбца, выражение."
                ),
                'wrong': 'addcolumn(m, "Сумма")',
                'right': 'addcolumn(m, "Сумма", m[:, "A"] + m[:, "B"])',
                'explanation': (
                    "addcolumn принимает ТРИ аргумента:\n"
                    "  1. таблица — Matrix или DuckDB\n"
                    "  2. \"Имя\" — имя нового столбца (строка в кавычках)\n"
                    "  3. выражение — что положить в столбец\n"
                    "\n"
                    "Выражение может быть:\n"
                    "  • скаляром: 2024, \"новый\", 0\n"
                    "  • арифметикой: m[:, \"A\"] + m[:, \"B\"]\n"
                    "  • функцией: round(m[:, \"Цена\"] * 1.2, 2)"
                ),
                'variants': [
                    'm2 = addcolumn(m, "Сумма", m[:, "A"] + m[:, "B"])',
                    'm2 = addcolumn(m, "Год", 2024)',
                    'm2 = addcolumn(m, "Статус", "новый")',
                ],
            },
            'ADDCOLUMN_NAME_NOT_STRING': {
                'message': (
                    "addcolumn: имя столбца должно быть строкой в кавычках."
                ),
                'wrong': 'addcolumn(m, Сумма, m[:, "A"] + m[:, "B"])',
                'right': 'addcolumn(m, "Сумма", m[:, "A"] + m[:, "B"])',
                'explanation': (
                    "Имя нового столбца — СТРОКА В КАВЫЧКАХ:\n"
                    "     addcolumn(m, \"Сумма\", ...)\n"
                    "     addcolumn(m, \"Цена_НДС\", ...)\n"
                    "\n"
                    "Без кавычек парсер думает, что это переменная.\n"
                    "Если переменной с таким именем нет — ошибка."
                ),
                'variants': [
                    'm2 = addcolumn(m, "Сумма", m[:, "A"] + m[:, "B"])',
                    'm2 = addcolumn(m, "Год", 2024)',
                ],
            },
            'ADDCOLUMN_NAME_NOT_TEXT': {
                'message': (
                    "addcolumn: имя столбца должно быть СТРОКОЙ, "
                    "а не числом или другим типом."
                ),
                'wrong': 'addcolumn(m, 5, m[:, "A"] + m[:, "B"])',
                'right': 'addcolumn(m, "Сумма", m[:, "A"] + m[:, "B"])',
                'explanation': (
                    "Имя нового столбца — это ТЕКСТ:\n"
                    "     addcolumn(m, \"Сумма\", ...)\n"
                    "     addcolumn(m, \"Итого\", ...)\n"
                    "\n"
                    "Число в качестве имени — ошибка.\n"
                    "Если нужно имя-число — используйте строку: \"5\"."
                ),
                'variants': [
                    'm2 = addcolumn(m, "Сумма", m[:, "A"] + m[:, "B"])',
                    'm2 = addcolumn(m, "5", m[:, "A"] + m[:, "B"])',
                ],
            },
            'ADDCOLUMN_NOT_TABLE': {
                'message': (
                    "addcolumn: первый аргумент — таблица (Matrix или DuckDB)."
                ),
                'wrong': 'addcolumn(42, "Сумма", 0)',
                'right': 'addcolumn(m, "Сумма", m[:, "A"] + m[:, "B"])',
                'explanation': (
                    "Первый аргумент — ТАБЛИЦА:\n"
                    "     m — переменная-матрица\n"
                    "     bd — переменная-DuckDB\n"
                    "\n"
                    "Нельзя передать число, строку или срез.\n"
                    "\n"
                    "Неправильно:\n"
                    "     addcolumn(42, \"Сумма\", 0)\n"
                    "     addcolumn(m[:, \"A\"], \"Сумма\", 0)\n"
                    "\n"
                    "Правильно:\n"
                    "     addcolumn(m, \"Сумма\", m[:, \"A\"] + m[:, \"B\"])"
                ),
                'variants': [
                    'm2 = addcolumn(m, "Сумма", m[:, "A"] + m[:, "B"])',
                    'bd2 = addcolumn(bd, "Сумма", bd[:, "A"] + bd[:, "B"])',
                ],
            },
            'ADDCOLUMN_EXPR_ERROR': {
                'message': (
                    "addcolumn: не удалось вычислить выражение.\n"
                    "  Проверьте, что столбцы существуют и совместимы."
                ),
                'wrong': 'addcolumn(m, "Сумма", m[:, "НетТакого"] + m[:, "A"])',
                'right': 'addcolumn(m, "Сумма", m[:, "A"] + m[:, "B"])',
                'explanation': (
                    "Выражение в третьем аргументе вычисляется построчно.\n"
                    "\n"
                    "Возможные причины ошибки:\n"
                    "  • столбец не найден\n"
                    "  • разные типы (число + строка)\n"
                    "  • деление на 0\n"
                    "\n"
                    "Проверьте, что столбцы существуют:\n"
                    "     print(m[0, :])"
                ),
                'variants': [
                    'm2 = addcolumn(m, "Сумма", m[:, "A"] + m[:, "B"])',
                    'm2 = addcolumn(m, "Цена_НДС", round(m[:, "Цена"] * 1.2, 2))',
                ],
            },
        },
    },

    'addrows': {
        'name': 'addrows',
        'category': 'analytics',
        'signature': 'addrows(таблица, N [, fill])',
        'description': (
            'Добавляет N строк в конец таблицы.\n'
            '  • Без fill — строки пустые (None).\n'
            '  • С fill — заполнены указанным значением.\n'
            '  • Работает с Matrix (RAM) и DuckDB (BigData).\n'
            '  • Возвращает НОВУЮ таблицу.'
        ),
        'examples': [
            'm2 = addrows(m, 5)',
            'm2 = addrows(m, 3, 0)',
            'm2 = addrows(m, 2, "-")',
        ],
        'errors': {
            'ADDROWS_BAD_COUNT': {
                'message': (
                    "addrows: количество должно быть числом."
                ),
                'wrong': 'addrows(m, "5")',
                'right': 'addrows(m, 5)',
                'explanation': (
                    "Второй аргумент — ЧИСЛО БЕЗ КАВЫЧЕК:\n"
                    "     addrows(m, 5)\n"
                    "     addrows(m, 3)\n"
                    "\n"
                    "Неправильно:\n"
                    "     addrows(m, \"5\")\n"
                    "\n"
                    "Правильно:\n"
                    "     addrows(m, 5)"
                ),
                'variants': [
                    'm2 = addrows(m, 5)',
                    'm2 = addrows(m, 3, 0)',
                ],
            },
            'ADDROWS_NEGATIVE': {
                'message': (
                    "addrows: количество не может быть отрицательным."
                ),
                'wrong': 'addrows(m, -2)',
                'right': 'addrows(m, 2)',
                'explanation': (
                    "N — количество СТРОК, которые нужно добавить.\n"
                    "Не может быть отрицательным.\n"
                    "\n"
                    "Неправильно:\n"
                    "     addrows(m, -2)\n"
                    "\n"
                    "Правильно:\n"
                    "     addrows(m, 2)\n"
                    "     addrows(m, 0)   — ничего не добавит"
                ),
                'variants': [
                    'm2 = addrows(m, 2)',
                    'm2 = addrows(m, 0)',
                ],
            },
            'ADDROWS_BAD_FILL': {
                'message': (
                    "addrows: fill должен быть скаляром "
                    "(число, строка, None)."
                ),
                'wrong': 'addrows(m, 3, [1, 2, 3])',
                'right': 'addrows(m, 3, 0)',
                'explanation': (
                    "Третий аргумент — ЗНАЧЕНИЕ для заполнения всех ячеек.\n"
                    "Это должен быть СКАЛЯР:\n"
                    "     addrows(m, 3, 0)\n"
                    "     addrows(m, 2, \"—\")\n"
                    "     addrows(m, 5, None)\n"
                    "\n"
                    "Неправильно — вектор:\n"
                    "     addrows(m, 3, [1, 2, 3])\n"
                    "\n"
                    "Если хотите вектор разных значений — используйте\n"
                    "отдельное присваивание после addrows."
                ),
                'variants': [
                    'm2 = addrows(m, 3, 0)',
                    'm2 = addrows(m, 2, "-")',
                    'm2 = addrows(m, 5, None)',
                ],
            },
            'ADDROWS_NOT_TABLE': {
                'message': (
                    "addrows: первый аргумент — таблица (Matrix или DuckDB)."
                ),
                'wrong': 'addrows(42, 5)',
                'right': 'addrows(m, 5)',
                'explanation': (
                    "Первый аргумент — ТАБЛИЦА:\n"
                    "     m — переменная-матрица\n"
                    "     bd — переменная-DuckDB\n"
                    "\n"
                    "Неправильно:\n"
                    "     addrows(42, 5)\n"
                    "     addrows(m[:, \"A\"], 5)\n"
                    "\n"
                    "Правильно:\n"
                    "     addrows(m, 5)"
                ),
                'variants': [
                    'm2 = addrows(m, 5)',
                    'bd2 = addrows(bd, 5)',
                ],
            },
        },
    },
}


EN = {
    'addcolumn': {
        'name': 'addcolumn',
        'category': 'analytics',
        'signature': 'addcolumn(table, "Name", expression)',
        'description': (
            'Add a new column to the table.\n'
            '  • Works with Matrix (RAM) and DuckDB (BigData).\n'
            '  • Always returns a NEW table.\n'
            '  • Expression — scalar, vector, arithmetic, function.'
        ),
        'examples': [
            'm2 = addcolumn(m, "Sum", m[:, "ID"] + m[:, "ID_10"])',
            'm2 = addcolumn(m, "Year", 2024)',
            'm2 = addcolumn(m, "Status", "new")',
            'm2 = addcolumn(m, "Price_VAT", round(m[:, "Price"] * 1.2, 2))',
        ],
        'errors': {
            'ADDCOLUMN_BAD_SYNTAX': {
                'message': (
                    "addcolumn: wrong number of arguments.\n"
                    "  Exactly THREE are required: table, column name, expression."
                ),
                'wrong': 'addcolumn(m, "Sum")',
                'right': 'addcolumn(m, "Sum", m[:, "A"] + m[:, "B"])',
                'explanation': (
                    "addcolumn takes THREE arguments:\n"
                    "  1. table — Matrix or DuckDB\n"
                    "  2. \"Name\" — new column name (quoted string)\n"
                    "  3. expression — what to put into the column\n"
                    "\n"
                    "Expression can be:\n"
                    "  • scalar: 2024, \"new\", 0\n"
                    "  • arithmetic: m[:, \"A\"] + m[:, \"B\"]\n"
                    "  • function: round(m[:, \"Price\"] * 1.2, 2)"
                ),
                'variants': [
                    'm2 = addcolumn(m, "Sum", m[:, "A"] + m[:, "B"])',
                    'm2 = addcolumn(m, "Year", 2024)',
                    'm2 = addcolumn(m, "Status", "new")',
                ],
            },
            'ADDCOLUMN_NAME_NOT_STRING': {
                'message': (
                    "addcolumn: column name must be a quoted string."
                ),
                'wrong': 'addcolumn(m, Sum, m[:, "A"] + m[:, "B"])',
                'right': 'addcolumn(m, "Sum", m[:, "A"] + m[:, "B"])',
                'explanation': (
                    "New column name is a STRING IN QUOTES:\n"
                    "     addcolumn(m, \"Sum\", ...)\n"
                    "     addcolumn(m, \"Price_VAT\", ...)\n"
                    "\n"
                    "Without quotes the parser thinks it is a variable.\n"
                    "If no such variable exists — error."
                ),
                'variants': [
                    'm2 = addcolumn(m, "Sum", m[:, "A"] + m[:, "B"])',
                    'm2 = addcolumn(m, "Year", 2024)',
                ],
            },
            'ADDCOLUMN_NAME_NOT_TEXT': {
                'message': (
                    "addcolumn: column name must be a STRING, "
                    "not a number or other type."
                ),
                'wrong': 'addcolumn(m, 5, m[:, "A"] + m[:, "B"])',
                'right': 'addcolumn(m, "Sum", m[:, "A"] + m[:, "B"])',
                'explanation': (
                    "New column name is TEXT:\n"
                    "     addcolumn(m, \"Sum\", ...)\n"
                    "     addcolumn(m, \"Total\", ...)\n"
                    "\n"
                    "A number as a name is an error.\n"
                    "If you need a numeric name — use a string: \"5\"."
                ),
                'variants': [
                    'm2 = addcolumn(m, "Sum", m[:, "A"] + m[:, "B"])',
                    'm2 = addcolumn(m, "5", m[:, "A"] + m[:, "B"])',
                ],
            },
            'ADDCOLUMN_NOT_TABLE': {
                'message': (
                    "addcolumn: first argument — table (Matrix or DuckDB)."
                ),
                'wrong': 'addcolumn(42, "Sum", 0)',
                'right': 'addcolumn(m, "Sum", m[:, "A"] + m[:, "B"])',
                'explanation': (
                    "First argument is a TABLE:\n"
                    "     m — matrix variable\n"
                    "     bd — DuckDB variable\n"
                    "\n"
                    "You cannot pass a number, string, or slice.\n"
                    "\n"
                    "Incorrect:\n"
                    "     addcolumn(42, \"Sum\", 0)\n"
                    "     addcolumn(m[:, \"A\"], \"Sum\", 0)\n"
                    "\n"
                    "Correct:\n"
                    "     addcolumn(m, \"Sum\", m[:, \"A\"] + m[:, \"B\"])"
                ),
                'variants': [
                    'm2 = addcolumn(m, "Sum", m[:, "A"] + m[:, "B"])',
                    'bd2 = addcolumn(bd, "Sum", bd[:, "A"] + bd[:, "B"])',
                ],
            },
            'ADDCOLUMN_EXPR_ERROR': {
                'message': (
                    "addcolumn: failed to evaluate the expression.\n"
                    "  Check that columns exist and are compatible."
                ),
                'wrong': 'addcolumn(m, "Sum", m[:, "NoSuch"] + m[:, "A"])',
                'right': 'addcolumn(m, "Sum", m[:, "A"] + m[:, "B"])',
                'explanation': (
                    "The expression in the third argument is evaluated row by row.\n"
                    "\n"
                    "Possible causes:\n"
                    "  • column not found\n"
                    "  • different types (number + string)\n"
                    "  • division by 0\n"
                    "\n"
                    "Check that columns exist:\n"
                    "     print(m[0, :])"
                ),
                'variants': [
                    'm2 = addcolumn(m, "Sum", m[:, "A"] + m[:, "B"])',
                    'm2 = addcolumn(m, "Price_VAT", round(m[:, "Price"] * 1.2, 2))',
                ],
            },
        },
    },

    'addrows': {
        'name': 'addrows',
        'category': 'analytics',
        'signature': 'addrows(table, N [, fill])',
        'description': (
            'Add N rows to the end of the table.\n'
            '  • Without fill — empty rows (None).\n'
            '  • With fill — filled with the specified value.\n'
            '  • Works with Matrix (RAM) and DuckDB (BigData).\n'
            '  • Returns a NEW table.'
        ),
        'examples': [
            'm2 = addrows(m, 5)',
            'm2 = addrows(m, 3, 0)',
            'm2 = addrows(m, 2, "-")',
        ],
        'errors': {
            'ADDROWS_BAD_COUNT': {
                'message': (
                    "addrows: count must be a number."
                ),
                'wrong': 'addrows(m, "5")',
                'right': 'addrows(m, 5)',
                'explanation': (
                    "Second argument is a NUMBER WITHOUT quotes:\n"
                    "     addrows(m, 5)\n"
                    "     addrows(m, 3)\n"
                    "\n"
                    "Incorrect:\n"
                    "     addrows(m, \"5\")\n"
                    "\n"
                    "Correct:\n"
                    "     addrows(m, 5)"
                ),
                'variants': [
                    'm2 = addrows(m, 5)',
                    'm2 = addrows(m, 3, 0)',
                ],
            },
            'ADDROWS_NEGATIVE': {
                'message': (
                    "addrows: count cannot be negative."
                ),
                'wrong': 'addrows(m, -2)',
                'right': 'addrows(m, 2)',
                'explanation': (
                    "N is the number of ROWS to add.\n"
                    "It cannot be negative.\n"
                    "\n"
                    "Incorrect:\n"
                    "     addrows(m, -2)\n"
                    "\n"
                    "Correct:\n"
                    "     addrows(m, 2)\n"
                    "     addrows(m, 0)   — adds nothing"
                ),
                'variants': [
                    'm2 = addrows(m, 2)',
                    'm2 = addrows(m, 0)',
                ],
            },
            'ADDROWS_BAD_FILL': {
                'message': (
                    "addrows: fill must be a scalar "
                    "(number, string, None)."
                ),
                'wrong': 'addrows(m, 3, [1, 2, 3])',
                'right': 'addrows(m, 3, 0)',
                'explanation': (
                    "Third argument is a VALUE to fill all cells.\n"
                    "It must be a SCALAR:\n"
                    "     addrows(m, 3, 0)\n"
                    "     addrows(m, 2, \"—\")\n"
                    "     addrows(m, 5, None)\n"
                    "\n"
                    "Incorrect — a vector:\n"
                    "     addrows(m, 3, [1, 2, 3])\n"
                    "\n"
                    "If you want a vector of different values — use\n"
                    "a separate assignment after addrows."
                ),
                'variants': [
                    'm2 = addrows(m, 3, 0)',
                    'm2 = addrows(m, 2, "-")',
                    'm2 = addrows(m, 5, None)',
                ],
            },
            'ADDROWS_NOT_TABLE': {
                'message': (
                    "addrows: first argument — table (Matrix or DuckDB)."
                ),
                'wrong': 'addrows(42, 5)',
                'right': 'addrows(m, 5)',
                'explanation': (
                    "First argument is a TABLE:\n"
                    "     m — matrix variable\n"
                    "     bd — DuckDB variable\n"
                    "\n"
                    "Incorrect:\n"
                    "     addrows(42, 5)\n"
                    "     addrows(m[:, \"A\"], 5)\n"
                    "\n"
                    "Correct:\n"
                    "     addrows(m, 5)"
                ),
                'variants': [
                    'm2 = addrows(m, 5)',
                    'bd2 = addrows(bd, 5)',
                ],
            },
        },
    },
}