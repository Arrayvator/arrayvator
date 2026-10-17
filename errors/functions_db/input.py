# errors/functions_db/input.py
"""
База ошибок для функций ввода:
    InputShow, InputShowForm, InputListShow, InputInMatrix.

СИНТАКСИС:
    InputShow([подпись] [, "матрица"])
    InputShowForm("Заголовок", "Поле1", "Поле2", ...)
    InputListShow([title: "..."], "подпись1", цель1, ...)
    InputInMatrix(матрица [, "Заголовок"] [, строк_контекста])
"""


RU = {
    # ============================================================
    # INPUTSHOW
    # ============================================================
    'InputShow': {
        'name': 'InputShow',
        'category': 'input',
        'signature': 'InputShow([подпись] [, "матрица"])',
        'description': (
            'Окно ввода одного значения.\n'
            '  • Без режима — одна строка ввода.\n'
            '  • "матрица" — многострочное текстовое поле.\n'
            '  • Возвращает число, строку, bool или None.\n'
            '  • Пустой ввод → "" (пустая строка).\n'
            '  • Ввод "none" / "null" → None.'
        ),
        'examples': [
            'x = InputShow("Введите число:")',
            'x = InputShow()',
            'm = InputShow("Матрица:", "матрица")',
        ],
        'errors': {
            'INPUTSHOW_BAD_MODE': {
                'message': (
                    "InputShow: неверный режим.\n"
                    "  Допустимо: 'текст', 'число', 'матрица'."
                ),
                'wrong': 'm = InputShow("X:", "table")',
                'right': 'm = InputShow("X:", "матрица")',
                'explanation': (
                    "Второй аргумент — режим, строка в кавычках.\n"
                    "  • \"матрица\" — многострочный ввод.\n"
                    "\n"
                    "Если режим не нужен — не указывайте второй аргумент."
                ),
                'variants': [
                    'x = InputShow("Введите число:")',
                    'm = InputShow("Матрица:", "матрица")',
                ],
            },
        },
    },

    # ============================================================
    # INPUTSHOWFORM
    # ============================================================
    'InputShowForm': {
        'name': 'InputShowForm',
        'category': 'input',
        'signature': 'InputShowForm("Заголовок", "Поле1", "Поле2", ...)',
        'description': (
            'Форма с несколькими полями ввода.\n'
            '  • Первый аргумент — заголовок окна.\n'
            '  • Далее — имена полей (по одному аргументу на поле).\n'
            '  • Возвращает ВЕКТОР значений.'
        ),
        'examples': [
            'data = InputShowForm("Анкета", "Имя", "Возраст", "Город")',
        ],
        'errors': {
            'INPUTSHOWFORM_NO_FIELDS': {
                'message': (
                    "InputShowForm: не указаны поля формы.\n"
                    "  Пример: InputShowForm(\"Анкета\", \"Имя\", \"Возраст\")"
                ),
                'wrong': 'data = InputShowForm("Анкета")',
                'right': 'data = InputShowForm("Анкета", "Имя", "Возраст")',
                'explanation': (
                    "После заголовка нужно указать хотя бы одно поле.\n"
                    "\n"
                    "Структура:\n"
                    "  InputShowForm(\"Заголовок\", \"Поле1\", \"Поле2\", ...)"
                ),
                'variants': [
                    'data = InputShowForm("Анкета", "Имя", "Возраст")',
                ],
            },
        },
    },

    # ============================================================
    # INPUTLISTSHOW
    # ============================================================
    'InputListShow': {
        'name': 'InputListShow',
        'category': 'input',
        'signature': 'InputListShow([title: "..."], "подпись1", цель1, ...)',
        'description': (
            'Последовательный ввод в несколько целей.\n'
            '  • Пары "подпись", цель.\n'
            '  • Цель — переменная или ячейка матрицы.\n'
            '  • Заголовок окна — опционально (title: "...").'
        ),
        'examples': [
            'InputListShow(title: "Анкета", "Имя:", x, "Возраст:", y)',
            'a = vector(3)\nInputListShow("A:", a[1], "B:", a[2], "C:", a[3])',
        ],
        'errors': {
            'INPUTLISTSHOW_ODD_ARGS': {
                'message': (
                    "InputListShow: непарное количество аргументов.\n"
                    "  Аргументы должны идти парами: \"подпись\", цель."
                ),
                'wrong': 'InputListShow("Имя:", x, "Возраст:")',
                'right': 'InputListShow("Имя:", x, "Возраст:", y)',
                'explanation': (
                    "Каждая подпись должна сопровождаться целью:\n"
                    "  InputListShow(\"подпись1\", цель1, \"подпись2\", цель2, ...)\n"
                    "\n"
                    "Опциональный заголовок:\n"
                    "  InputListShow(title: \"...\", ...)"
                ),
                'variants': [
                    'InputListShow("Имя:", x, "Возраст:", y)',
                    'InputListShow(title: "Анкета", "Имя:", x, "Возраст:", y)',
                ],
            },
            'INPUTLISTSHOW_BAD_TARGET': {
                'message': (
                    "InputListShow: неверная цель ввода.\n"
                    "  Цель должна быть переменной или ячейкой матрицы."
                ),
                'wrong': 'InputListShow("Имя:", "x")',
                'right': 'InputListShow("Имя:", x)',
                'explanation': (
                    "Цель — это ПЕРЕМЕННАЯ или ЯЧЕЙКА МАТРИЦЫ (m[i, j]),\n"
                    "а не строка.\n"
                    "\n"
                    "Неправильно:\n"
                    "     InputListShow(\"Имя:\", \"x\")\n"
                    "\n"
                    "Правильно:\n"
                    "     InputListShow(\"Имя:\", x)\n"
                    "     InputListShow(\"A[1]:\", m[1, 1])"
                ),
                'variants': [
                    'InputListShow("Имя:", x)',
                    'a = vector(3)\nInputListShow("A:", a[1], "B:", a[2])',
                ],
            },
        },
    },

    # ============================================================
    # INPUTINMATRIX
    # ============================================================
    'InputInMatrix': {
        'name': 'InputInMatrix',
        'category': 'input',
        'signature': 'InputInMatrix(матрица [, "Заголовок"] [, строк_контекста])',
        'description': (
            'Визуальное добавление строк в матрицу.\n'
            '  • Открывает окно с последними N строками (контекст).\n'
            '  • Поля ввода ПО ЧИСЛУ СТОЛБЦОВ, горизонтально.\n'
            '  • «Добавить» (Enter) — строка появляется в таблице (жёлтая).\n'
            '  • «Завершить» (Ctrl+Enter) — вернуть новую матрицу.\n'
            '  • «Убрать последнюю» (Ctrl+Z) — отменить.\n'
            '  • Крестик / Esc — отмена, вернуть ИСХОДНУЮ матрицу.\n'
            '  • Работает только с 2D-матрицами (не с вектором).\n'
            '  • Возвращает НОВУЮ матрицу — результат нужно сохранить.'
        ),
        'examples': [
            'm = InputInMatrix(m)',
            'm = InputInMatrix(m, "Сотрудники")',
            'm = InputInMatrix(m, "Сотрудники", 5)',
            'm = InputInMatrix(m, "Товары", 20)',
        ],
        'errors': {
            'INPUTINMATRIX_NOT_MATRIX': {
                'message': (
                    "InputInMatrix: ожидается 2D-матрица.\n"
                    "  Функция добавляет СТРОКИ в матрицу, а не в вектор."
                ),
                'wrong': 'm = InputInMatrix(v)',
                'right': 'm = InputInMatrix(m)',
                'explanation': (
                    "InputInMatrix работает только с двумерными матрицами:\n"
                    "     m = [\"Имя\", \"Отдел\";\n"
                    "          \"Аня\", \"IT\"]\n"
                    "     m = InputInMatrix(m)\n"
                    "\n"
                    "Вектор — одномерный, у него нет столбцов,\n"
                    "поэтому поля ввода построить невозможно."
                ),
                'variants': [
                    'm = InputInMatrix(m)',
                    'm = InputInMatrix(m, "Сотрудники")',
                ],
            },
            'INPUTINMATRIX_BAD_TITLE': {
                'message': (
                    "InputInMatrix: заголовок окна должен быть строкой."
                ),
                'wrong': 'm = InputInMatrix(m, 42)',
                'right': 'm = InputInMatrix(m, "Сотрудники")',
                'explanation': (
                    "Второй аргумент — заголовок окна, строка в кавычках:\n"
                    "     m = InputInMatrix(m, \"Сотрудники\")\n"
                    "     m = InputInMatrix(m, \"Товары\")\n"
                    "\n"
                    "Неправильно:\n"
                    "     m = InputInMatrix(m, 42)\n"
                    "     m = InputInMatrix(m, Сотрудники)"
                ),
                'variants': [
                    'm = InputInMatrix(m)',
                    'm = InputInMatrix(m, "Сотрудники")',
                ],
            },
            'INPUTINMATRIX_BAD_PREVIEW': {
                'message': (
                    "InputInMatrix: количество строк контекста — число >= 0."
                ),
                'wrong': 'm = InputInMatrix(m, "Сотрудники", "много")',
                'right': 'm = InputInMatrix(m, "Сотрудники", 5)',
                'explanation': (
                    "Третий аргумент — сколько последних строк показать:\n"
                    "     m = InputInMatrix(m, \"Сотрудники\", 5)\n"
                    "     m = InputInMatrix(m, \"Сотрудники\", 20)\n"
                    "\n"
                    "По умолчанию — 10.\n"
                    "\n"
                    "Неправильно:\n"
                    "     m = InputInMatrix(m, \"Сотрудники\", \"много\")"
                ),
                'variants': [
                    'm = InputInMatrix(m, "Сотрудники")',
                    'm = InputInMatrix(m, "Сотрудники", 5)',
                    'm = InputInMatrix(m, "Сотрудники", 20)',
                ],
            },
            'INPUTINMATRIX_BAD_ARGS': {
                'message': (
                    "InputInMatrix: неверные аргументы.\n"
                    "  Ожидается: InputInMatrix(матрица [, \"Заголовок\" [, число]])"
                ),
                'wrong': 'm = InputInMatrix()',
                'right': 'm = InputInMatrix(m)',
                'explanation': (
                    "Структура:\n"
                    "  InputInMatrix(матрица)\n"
                    "  InputInMatrix(матрица, \"Заголовок\")\n"
                    "  InputInMatrix(матрица, \"Заголовок\", строк_контекста)"
                ),
                'variants': [
                    'm = InputInMatrix(m)',
                    'm = InputInMatrix(m, "Сотрудники")',
                    'm = InputInMatrix(m, "Сотрудники", 5)',
                ],
            },
            'INPUTINMATRIX_REQUIRES_ASSIGNMENT': {
                'message': (
                    "InputInMatrix: результат нужно сохранить.\n"
                    "  Функция возвращает НОВУЮ матрицу с добавленными строками.\n"
                    "  Исходная матрица НЕ изменяется."
                ),
                'wrong': 'InputInMatrix(m, "Сотрудники")',
                'right': 'm = InputInMatrix(m, "Сотрудники")',
                'explanation': (
                    "Без присваивания результат теряется:\n"
                    "\n"
                    "  ❌  Неправильно:\n"
                    "     InputInMatrix(m, \"Сотрудники\")\n"
                    "\n"
                    "  ✅  Правильно:\n"
                    "     m = InputInMatrix(m, \"Сотрудники\")\n"
                    "\n"
                    "Правило то же, что у filterif, sort, addcolumn и др."
                ),
                'variants': [
                    'm = InputInMatrix(m)',
                    'm = InputInMatrix(m, "Сотрудники")',
                    'm = InputInMatrix(m, "Сотрудники", 5)',
                ],
            },
        },
    },
}


EN = {
    # ============================================================
    # INPUTSHOW
    # ============================================================
    'InputShow': {
        'name': 'InputShow',
        'category': 'input',
        'signature': 'InputShow([prompt] [, "matrix"])',
        'description': (
            'Dialog for entering a single value.\n'
            '  • No mode — single-line input.\n'
            '  • "matrix" — multi-line text field.\n'
            '  • Returns number, string, bool, or None.\n'
            '  • Empty input → "" (empty string).\n'
            '  • "none" / "null" input → None.'
        ),
        'examples': [
            'x = InputShow("Enter a number:")',
            'x = InputShow()',
            'm = InputShow("Matrix:", "matrix")',
        ],
        'errors': {
            'INPUTSHOW_BAD_MODE': {
                'message': (
                    "InputShow: invalid mode.\n"
                    "  Allowed: 'text', 'number', 'matrix'."
                ),
                'wrong': 'm = InputShow("X:", "table")',
                'right': 'm = InputShow("X:", "matrix")',
                'explanation': (
                    "Second argument is the mode, a quoted string.\n"
                    "  • \"matrix\" — multi-line input.\n"
                    "\n"
                    "If no mode is needed — omit the second argument."
                ),
                'variants': [
                    'x = InputShow("Enter a number:")',
                    'm = InputShow("Matrix:", "matrix")',
                ],
            },
        },
    },

    # ============================================================
    # INPUTSHOWFORM
    # ============================================================
    'InputShowForm': {
        'name': 'InputShowForm',
        'category': 'input',
        'signature': 'InputShowForm("Title", "Field1", "Field2", ...)',
        'description': (
            'Form with multiple input fields.\n'
            '  • First argument — window title.\n'
            '  • Then — field names (one argument per field).\n'
            '  • Returns a VECTOR of values.'
        ),
        'examples': [
            'data = InputShowForm("Form", "Name", "Age", "City")',
        ],
        'errors': {
            'INPUTSHOWFORM_NO_FIELDS': {
                'message': (
                    "InputShowForm: no form fields specified.\n"
                    "  Example: InputShowForm(\"Form\", \"Name\", \"Age\")"
                ),
                'wrong': 'data = InputShowForm("Form")',
                'right': 'data = InputShowForm("Form", "Name", "Age")',
                'explanation': (
                    "After the title, at least one field is required.\n"
                    "\n"
                    "Structure:\n"
                    "  InputShowForm(\"Title\", \"Field1\", \"Field2\", ...)"
                ),
                'variants': [
                    'data = InputShowForm("Form", "Name", "Age")',
                ],
            },
        },
    },

    # ============================================================
    # INPUTLISTSHOW
    # ============================================================
    'InputListShow': {
        'name': 'InputListShow',
        'category': 'input',
        'signature': 'InputListShow([title: "..."], "label1", target1, ...)',
        'description': (
            'Sequential input into multiple targets.\n'
            '  • Pairs: "label", target.\n'
            '  • Target — variable or matrix cell.\n'
            '  • Window title — optional (title: "...").'
        ),
        'examples': [
            'InputListShow(title: "Form", "Name:", x, "Age:", y)',
            'a = vector(3)\nInputListShow("A:", a[1], "B:", a[2], "C:", a[3])',
        ],
        'errors': {
            'INPUTLISTSHOW_ODD_ARGS': {
                'message': (
                    "InputListShow: odd number of arguments.\n"
                    "  Arguments must go in pairs: \"label\", target."
                ),
                'wrong': 'InputListShow("Name:", x, "Age:")',
                'right': 'InputListShow("Name:", x, "Age:", y)',
                'explanation': (
                    "Each label must be followed by a target:\n"
                    "  InputListShow(\"label1\", target1, \"label2\", target2, ...)\n"
                    "\n"
                    "Optional title:\n"
                    "  InputListShow(title: \"...\", ...)"
                ),
                'variants': [
                    'InputListShow("Name:", x, "Age:", y)',
                    'InputListShow(title: "Form", "Name:", x, "Age:", y)',
                ],
            },
            'INPUTLISTSHOW_BAD_TARGET': {
                'message': (
                    "InputListShow: invalid target.\n"
                    "  Target must be a variable or a matrix cell."
                ),
                'wrong': 'InputListShow("Name:", "x")',
                'right': 'InputListShow("Name:", x)',
                'explanation': (
                    "Target is a VARIABLE or a MATRIX CELL (m[i, j]),\n"
                    "not a string.\n"
                    "\n"
                    "Incorrect:\n"
                    "     InputListShow(\"Name:\", \"x\")\n"
                    "\n"
                    "Correct:\n"
                    "     InputListShow(\"Name:\", x)\n"
                    "     InputListShow(\"A[1]:\", m[1, 1])"
                ),
                'variants': [
                    'InputListShow("Name:", x)',
                    'a = vector(3)\nInputListShow("A:", a[1], "B:", a[2])',
                ],
            },
        },
    },

    # ============================================================
    # INPUTINMATRIX
    # ============================================================
    'InputInMatrix': {
        'name': 'InputInMatrix',
        'category': 'input',
        'signature': 'InputInMatrix(matrix [, "Title"] [, preview_rows])',
        'description': (
            'Visually add rows to a matrix.\n'
            '  • Opens a window with the last N rows (context).\n'
            '  • Input fields PER COLUMN, horizontally.\n'
            '  • "Add" (Enter) — row appears in the table (yellow).\n'
            '  • "Finish" (Ctrl+Enter) — return the new matrix.\n'
            '  • "Undo last" (Ctrl+Z) — undo.\n'
            '  • Close / Esc — cancel, return the SOURCE matrix.\n'
            '  • Works only with 2D matrices (not vectors).\n'
            '  • Returns a NEW matrix — save the result.'
        ),
        'examples': [
            'm = InputInMatrix(m)',
            'm = InputInMatrix(m, "Employees")',
            'm = InputInMatrix(m, "Employees", 5)',
            'm = InputInMatrix(m, "Products", 20)',
        ],
        'errors': {
            'INPUTINMATRIX_NOT_MATRIX': {
                'message': (
                    "InputInMatrix: a 2D matrix is expected.\n"
                    "  The function adds ROWS to a matrix, not to a vector."
                ),
                'wrong': 'm = InputInMatrix(v)',
                'right': 'm = InputInMatrix(m)',
                'explanation': (
                    "InputInMatrix works only with 2D matrices:\n"
                    "     m = [\"Name\", \"Dept\";\n"
                    "          \"Anna\", \"IT\"]\n"
                    "     m = InputInMatrix(m)\n"
                    "\n"
                    "A vector is 1D and has no columns,\n"
                    "so input fields cannot be built."
                ),
                'variants': [
                    'm = InputInMatrix(m)',
                    'm = InputInMatrix(m, "Employees")',
                ],
            },
            'INPUTINMATRIX_BAD_TITLE': {
                'message': (
                    "InputInMatrix: window title must be a string."
                ),
                'wrong': 'm = InputInMatrix(m, 42)',
                'right': 'm = InputInMatrix(m, "Employees")',
                'explanation': (
                    "Second argument — window title, a quoted string:\n"
                    "     m = InputInMatrix(m, \"Employees\")\n"
                    "     m = InputInMatrix(m, \"Products\")\n"
                    "\n"
                    "Incorrect:\n"
                    "     m = InputInMatrix(m, 42)\n"
                    "     m = InputInMatrix(m, Employees)"
                ),
                'variants': [
                    'm = InputInMatrix(m)',
                    'm = InputInMatrix(m, "Employees")',
                ],
            },
            'INPUTINMATRIX_BAD_PREVIEW': {
                'message': (
                    "InputInMatrix: preview row count must be a number >= 0."
                ),
                'wrong': 'm = InputInMatrix(m, "Employees", "many")',
                'right': 'm = InputInMatrix(m, "Employees", 5)',
                'explanation': (
                    "Third argument — how many last rows to show:\n"
                    "     m = InputInMatrix(m, \"Employees\", 5)\n"
                    "     m = InputInMatrix(m, \"Employees\", 20)\n"
                    "\n"
                    "Default — 10.\n"
                    "\n"
                    "Incorrect:\n"
                    "     m = InputInMatrix(m, \"Employees\", \"many\")"
                ),
                'variants': [
                    'm = InputInMatrix(m, "Employees")',
                    'm = InputInMatrix(m, "Employees", 5)',
                    'm = InputInMatrix(m, "Employees", 20)',
                ],
            },
            'INPUTINMATRIX_BAD_ARGS': {
                'message': (
                    "InputInMatrix: invalid arguments.\n"
                    "  Expected: InputInMatrix(matrix [, \"Title\" [, count]])"
                ),
                'wrong': 'm = InputInMatrix()',
                'right': 'm = InputInMatrix(m)',
                'explanation': (
                    "Structure:\n"
                    "  InputInMatrix(matrix)\n"
                    "  InputInMatrix(matrix, \"Title\")\n"
                    "  InputInMatrix(matrix, \"Title\", preview_rows)"
                ),
                'variants': [
                    'm = InputInMatrix(m)',
                    'm = InputInMatrix(m, "Employees")',
                    'm = InputInMatrix(m, "Employees", 5)',
                ],
            },
            'INPUTINMATRIX_REQUIRES_ASSIGNMENT': {
                'message': (
                    "InputInMatrix: the result must be saved.\n"
                    "  The function returns a NEW matrix with added rows.\n"
                    "  The source matrix is NOT modified."
                ),
                'wrong': 'InputInMatrix(m, "Employees")',
                'right': 'm = InputInMatrix(m, "Employees")',
                'explanation': (
                    "Without assignment the result is lost:\n"
                    "\n"
                    "  ❌  Incorrect:\n"
                    "     InputInMatrix(m, \"Employees\")\n"
                    "\n"
                    "  ✅  Correct:\n"
                    "     m = InputInMatrix(m, \"Employees\")\n"
                    "\n"
                    "Same rule as for filterif, sort, addcolumn, etc."
                ),
                'variants': [
                    'm = InputInMatrix(m)',
                    'm = InputInMatrix(m, "Employees")',
                    'm = InputInMatrix(m, "Employees", 5)',
                ],
            },
        },
    },
}