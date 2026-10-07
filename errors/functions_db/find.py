# errors/functions_db/find.py
"""
База ошибок для функций find и findif.

СИНТАКСИС:
    find(m[:, "X"] == "Y")                  — координаты
    find(m[:, "X"] == "Y", rows)            — номера строк
    find(m[:, "X"] == "Y", cols)            — номера столбцов
    find(m[:, "X"] == "Y", inside)          — подстрока
    find(m[:, "X"] == "Y", ignore)          — без регистра
    find(m[:, "X"] == "Y", inside, ignore)  — вместе
    find(v == 5)                            — вектор

Работает с Matrix и DuckDB.
"""


RU = {
    'find': {
        'name': 'find',
        'category': 'search',
        'signature': 'find(условие [, inside] [, ignore] [, rows|cols])',
        'description': (
            'Поиск значений в матрице или векторе.\n'
            '  • По умолчанию — координаты [[строка, столбец], ...].\n'
            '  • rows — только номера строк.\n'
            '  • cols — только номера столбцов.\n'
            '  • inside — поиск подстроки.\n'
            '  • ignore — без учёта регистра.\n'
            '  • Работает с Matrix и DuckDB.'
        ),
        'examples': [
            'r = find(m[:, "Имя"] == "Аня")',
            'r = find(m[:, "Имя"] == "ов", inside)',
            'r = find(m[:, "Имя"] == "аня", ignore)',
            'r = find(m[:, "Отдел"] == "IT", rows)',
            'r = find(v == 5)',
        ],
        'errors': {
            'FIND_BAD_SYNTAX': {
                'message': (
                    "find: неверный синтаксис.\n"
                    "  Нужно условие m[:, \"X\"] == \"Y\"."
                ),
                'wrong': 'find()',
                'right': 'find(m[:, "Имя"] == "Аня")',
                'explanation': (
                    "find принимает условие-сравнение:\n"
                    "     find(m[:, \"X\"] == \"Y\")\n"
                    "     find(m[:, \"X\"] > 10)\n"
                    "     find(v == 5)\n"
                    "\n"
                    "Неправильно:\n"
                    "     find()\n"
                    "     find(m)\n"
                    "\n"
                    "Правильно:\n"
                    "     find(m[:, \"Имя\"] == \"Аня\")"
                ),
                'variants': [
                    'r = find(m[:, "Имя"] == "Аня")',
                    'r = find(v == 5)',
                ],
            },
            'FIND_ASSIGN_IN_CONDITION': {
                'message': (
                    "find: в условии используется '=' (присваивание), "
                    "а нужно '==' (сравнение)."
                ),
                'wrong': 'find(m[:, "Имя"] = "Аня")',
                'right': 'find(m[:, "Имя"] == "Аня")',
                'explanation': (
                    "'=' — присваивает значение.\n"
                    "'==' — сравнивает значения.\n"
                    "\n"
                    "В условии find ВСЕГДА '=='."
                ),
                'variants': [
                    'r = find(m[:, "Имя"] == "Аня")',
                    'r = find(v == 5)',
                ],
            },
            'FIND_AND_OPERATOR': {
                'message': (
                    "find: логическое И пишется как 'and', а не '&&'."
                ),
                'wrong': 'find(m[:, "Имя"] == "Аня" && m[:, "Отдел"] == "IT")',
                'right': 'find(m[:, "Имя"] == "Аня" and m[:, "Отдел"] == "IT")',
                'explanation': (
                    "ArrayVator использует СЛОВА:\n"
                    "  'and' — И\n"
                    "  'or'  — ИЛИ\n"
                    "  'not' — НЕ"
                ),
                'variants': [
                    'r = find(m[:, "Имя"] == "Аня" and m[:, "Отдел"] == "IT")',
                ],
            },
            'FIND_OR_OPERATOR': {
                'message': (
                    "find: логическое ИЛИ пишется как 'or', а не '||'."
                ),
                'wrong': 'find(m[:, "Отдел"] == "IT" || m[:, "Отдел"] == "HR")',
                'right': 'find(m[:, "Отдел"] == "IT" or m[:, "Отдел"] == "HR")',
                'explanation': (
                    "ArrayVator использует СЛОВА:\n"
                    "  'and' — И\n"
                    "  'or'  — ИЛИ\n"
                    "  'not' — НЕ"
                ),
                'variants': [
                    'r = find(m[:, "Отдел"] == "IT" or m[:, "Отдел"] == "HR")',
                ],
            },
            'FIND_NO_SLICE': {
                'message': (
                    "find: нет среза.\n"
                    "  Условие должно быть на срезе m[:, \"X\"]."
                ),
                'wrong': 'find("Имя" == "Аня")',
                'right': 'find(m[:, "Имя"] == "Аня")',
                'explanation': (
                    "Срез указывает, где искать.\n"
                    "\n"
                    "Неправильно:\n"
                    "     find(\"Имя\" == \"Аня\")\n"
                    "\n"
                    "Правильно:\n"
                    "     find(m[:, \"Имя\"] == \"Аня\")"
                ),
                'variants': [
                    'r = find(m[:, "Имя"] == "Аня")',
                    'r = find(m[2:10, "Имя"] == "Аня")',
                ],
            },
            'FIND_BOTH_ROWS_COLS': {
                'message': (
                    "find: нельзя одновременно указать rows и cols."
                ),
                'wrong': 'find(m[:, "Имя"] == "Аня", rows, cols)',
                'right': 'find(m[:, "Имя"] == "Аня", rows)',
                'explanation': (
                    "Выберите что-то одно:\n"
                    "     find(m[:, \"X\"] == \"Y\")            — координаты\n"
                    "     find(m[:, \"X\"] == \"Y\", rows)      — номера строк\n"
                    "     find(m[:, \"X\"] == \"Y\", cols)      — номера столбцов"
                ),
                'variants': [
                    'r = find(m[:, "Имя"] == "Аня")',
                    'r = find(m[:, "Имя"] == "Аня", rows)',
                    'r = find(m[:, "Имя"] == "Аня", cols)',
                ],
            },
            'FIND_REQUIRES_ASSIGNMENT': {
                'message': (
                    "find() возвращает значение — "
                    "результат нужно сохранить."
                ),
                'wrong': 'find(m[:, "Имя"] == "Аня")',
                'right': 'r = find(m[:, "Имя"] == "Аня")',
                'explanation': (
                    "find НЕ изменяет исходную матрицу.\n"
                    "Он ВОЗВРАЩАЕТ НОВУЮ.\n"
                    "\n"
                    "Правильно:\n"
                    "  r = find(...)      — в новую переменную\n"
                    "  print(find(...))   — вывод"
                ),
                'variants': [
                    'r = find(m[:, "Имя"] == "Аня")',
                    'print(find(m[:, "Имя"] == "Аня"))',
                ],
            },
        },
    },
}


EN = {
    'find': {
        'name': 'find',
        'category': 'search',
        'signature': 'find(condition [, inside] [, ignore] [, rows|cols])',
        'description': (
            'Find values in a matrix or vector.\n'
            '  • Default — coordinates [[row, col], ...].\n'
            '  • rows — row numbers only.\n'
            '  • cols — column numbers only.\n'
            '  • inside — substring search.\n'
            '  • ignore — case-insensitive.\n'
            '  • Works with Matrix and DuckDB.'
        ),
        'examples': [
            'r = find(m[:, "Name"] == "Anna")',
            'r = find(m[:, "Name"] == "ov", inside)',
            'r = find(m[:, "Name"] == "anna", ignore)',
            'r = find(m[:, "Dept"] == "IT", rows)',
            'r = find(v == 5)',
        ],
        'errors': {
            'FIND_BAD_SYNTAX': {
                'message': (
                    "find: invalid syntax.\n"
                    "  Need a condition m[:, \"X\"] == \"Y\"."
                ),
                'wrong': 'find()',
                'right': 'find(m[:, "Name"] == "Anna")',
                'explanation': (
                    "find takes a comparison condition:\n"
                    "     find(m[:, \"X\"] == \"Y\")\n"
                    "     find(m[:, \"X\"] > 10)\n"
                    "     find(v == 5)\n"
                    "\n"
                    "Incorrect:\n"
                    "     find()\n"
                    "     find(m)\n"
                    "\n"
                    "Correct:\n"
                    "     find(m[:, \"Name\"] == \"Anna\")"
                ),
                'variants': [
                    'r = find(m[:, "Name"] == "Anna")',
                    'r = find(v == 5)',
                ],
            },
            'FIND_ASSIGN_IN_CONDITION': {
                'message': (
                    "find: '=' (assignment) is used "
                    "instead of '==' (comparison)."
                ),
                'wrong': 'find(m[:, "Name"] = "Anna")',
                'right': 'find(m[:, "Name"] == "Anna")',
                'explanation': (
                    "'=' — assigns.\n"
                    "'==' — compares.\n"
                    "\n"
                    "In find condition ALWAYS '=='."
                ),
                'variants': [
                    'r = find(m[:, "Name"] == "Anna")',
                    'r = find(v == 5)',
                ],
            },
            'FIND_AND_OPERATOR': {
                'message': (
                    "find: logical AND is 'and', not '&&'."
                ),
                'wrong': 'find(m[:, "Name"] == "Anna" && m[:, "Dept"] == "IT")',
                'right': 'find(m[:, "Name"] == "Anna" and m[:, "Dept"] == "IT")',
                'explanation': (
                    "ArrayVator uses WORDS:\n"
                    "  'and' — AND\n"
                    "  'or'  — OR\n"
                    "  'not' — NOT"
                ),
                'variants': [
                    'r = find(m[:, "Name"] == "Anna" and m[:, "Dept"] == "IT")',
                ],
            },
            'FIND_OR_OPERATOR': {
                'message': (
                    "find: logical OR is 'or', not '||'."
                ),
                'wrong': 'find(m[:, "Dept"] == "IT" || m[:, "Dept"] == "HR")',
                'right': 'find(m[:, "Dept"] == "IT" or m[:, "Dept"] == "HR")',
                'explanation': (
                    "ArrayVator uses WORDS:\n"
                    "  'and' — AND\n"
                    "  'or'  — OR\n"
                    "  'not' — NOT"
                ),
                'variants': [
                    'r = find(m[:, "Dept"] == "IT" or m[:, "Dept"] == "HR")',
                ],
            },
            'FIND_NO_SLICE': {
                'message': (
                    "find: no slice.\n"
                    "  Condition must be on a slice m[:, \"X\"]."
                ),
                'wrong': 'find("Name" == "Anna")',
                'right': 'find(m[:, "Name"] == "Anna")',
                'explanation': (
                    "The slice specifies where to search.\n"
                    "\n"
                    "Incorrect:\n"
                    "     find(\"Name\" == \"Anna\")\n"
                    "\n"
                    "Correct:\n"
                    "     find(m[:, \"Name\"] == \"Anna\")"
                ),
                'variants': [
                    'r = find(m[:, "Name"] == "Anna")',
                    'r = find(m[2:10, "Name"] == "Anna")',
                ],
            },
            'FIND_BOTH_ROWS_COLS': {
                'message': (
                    "find: cannot specify both rows and cols."
                ),
                'wrong': 'find(m[:, "Name"] == "Anna", rows, cols)',
                'right': 'find(m[:, "Name"] == "Anna", rows)',
                'explanation': (
                    "Pick one:\n"
                    "     find(m[:, \"X\"] == \"Y\")            — coordinates\n"
                    "     find(m[:, \"X\"] == \"Y\", rows)      — row numbers\n"
                    "     find(m[:, \"X\"] == \"Y\", cols)      — column numbers"
                ),
                'variants': [
                    'r = find(m[:, "Name"] == "Anna")',
                    'r = find(m[:, "Name"] == "Anna", rows)',
                    'r = find(m[:, "Name"] == "Anna", cols)',
                ],
            },
            'FIND_REQUIRES_ASSIGNMENT': {
                'message': (
                    "find() returns a value — "
                    "the result must be saved."
                ),
                'wrong': 'find(m[:, "Name"] == "Anna")',
                'right': 'r = find(m[:, "Name"] == "Anna")',
                'explanation': (
                    "find does NOT modify the source matrix.\n"
                    "It RETURNS a NEW one.\n"
                    "\n"
                    "Correct:\n"
                    "  r = find(...)      — to a new variable\n"
                    "  print(find(...))   — output"
                ),
                'variants': [
                    'r = find(m[:, "Name"] == "Anna")',
                    'print(find(m[:, "Name"] == "Anna"))',
                ],
            },
        },
    },
}