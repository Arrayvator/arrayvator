# errors/functions_db/filterif.py
"""
База ошибок для функции FILTERIF (фильтрация).
"""

RU = {
    'filterif': {
        'name': 'filterif',
        'category': 'filter',
        'signature': 'filterif(m[:, "X"] == "Y")',
        'description': (
            'Оставляет строки, где условие истинно.\n'
            '  • Работает с Matrix и DuckDB.\n'
            '  • Заголовок НЕ удаляется.\n'
            '  • Порядок строк сохраняется.\n'
            '  • Возвращает НОВУЮ матрицу — результат нужно сохранить.'
        ),
        'examples': [
            'r = filterif(m[:, "Пол"] == "Ж")',
            'm = filterif(m[:, "Пол"] == "Ж")',
            'r = filterif(m[2:10, "Возраст"] > 25)',
            'r = filterif(m[:, "Возраст"] > 25 and m[:, "Отдел"] == "IT")',
            'r = filterif(m[:, "Отдел"] == "IT" or m[:, "Отдел"] == "HR")',
            'r = filterif(not (m[:, "Отдел"] == "IT"))',
            'r = filterif(v > 20)',
        ],
        'errors': {
            'FILTERIF_BAD_SYNTAX': {
                'message': (
                    "filterif: неверный синтаксис.\n"
                    "  Нужен срез m[:, \"X\"] со сравнением."
                ),
                'wrong': 'filterif(m, "Пол" == "Ж")',
                'right': 'filterif(m[:, "Пол"] == "Ж")',
                'explanation': (
                    "Первый аргумент — СРЕЗ m[:, \"X\"],\n"
                    "внутри которого уже условие сравнения.\n"
                    "\n"
                    "Структура:\n"
                    "  filterif(m[:, \"X\"] == \"Y\")\n"
                    "  filterif(m[:, \"X\"] > 10)\n"
                    "  filterif(m[:, \"X\"] == \"Y\" and m[:, \"Z\"] == \"W\")"
                ),
                'variants': [
                    'r = filterif(m[:, "Пол"] == "Ж")',
                    'r = filterif(m[2:10, "Возраст"] > 25)',
                    'r = filterif(m[:, "Возраст"] > 25 and m[:, "Отдел"] == "IT")',
                    'r = filterif(v > 20)',
                ],
            },
            'FILTERIF_ASSIGN_IN_CONDITION': {
                'message': (
                    "filterif: в условии используется '=' (присваивание), "
                    "а нужно '==' (сравнение)."
                ),
                'wrong': 'filterif(m[:, "Пол"] = "Ж")',
                'right': 'filterif(m[:, "Пол"] == "Ж")',
                'explanation': (
                    "'=' — присваивает значение.\n"
                    "'==' — сравнивает значения.\n"
                    "\n"
                    "В условии filterif ВСЕГДА '=='."
                ),
                'variants': [
                    'r = filterif(m[:, "Пол"] == "Ж")',
                    'r = filterif(m[2:10, "Возраст"] > 25)',
                    'r = filterif(m[:, "Отдел"] != "HR")',
                ],
            },
            'FILTERIF_AND_OPERATOR': {
                'message': (
                    "filterif: логическое И пишется как 'and', а не '&&'."
                ),
                'wrong': 'filterif(m[:, "Пол"] == "Ж" && m[:, "Возраст"] > 25)',
                'right': 'filterif(m[:, "Пол"] == "Ж" and m[:, "Возраст"] > 25)',
                'explanation': (
                    "ArrayVator использует СЛОВА:\n"
                    "  'and' — И\n"
                    "  'or'  — ИЛИ\n"
                    "  'not' — НЕ"
                ),
                'variants': [
                    'r = filterif(m[:, "Пол"] == "Ж" and m[:, "Возраст"] > 25)',
                    'r = filterif(m[2:10, "Отдел"] == "IT" or m[2:10, "Отдел"] == "HR")',
                ],
            },
            'FILTERIF_OR_OPERATOR': {
                'message': (
                    "filterif: логическое ИЛИ пишется как 'or', а не '||'."
                ),
                'wrong': 'filterif(m[:, "Отдел"] == "IT" || m[:, "Отдел"] == "HR")',
                'right': 'filterif(m[:, "Отдел"] == "IT" or m[:, "Отдел"] == "HR")',
                'explanation': (
                    "ArrayVator использует СЛОВА:\n"
                    "  'and' — И\n"
                    "  'or'  — ИЛИ\n"
                    "  'not' — НЕ"
                ),
                'variants': [
                    'r = filterif(m[:, "Отдел"] == "IT" or m[:, "Отдел"] == "HR")',
                    'r = filterif(m[2:10, "Пол"] == "Ж" or m[2:10, "Пол"] == "М")',
                ],
            },
            'FILTERIF_NO_SLICE': {
                'message': (
                    "filterif: нет среза.\n"
                    "  Условие должно быть на срезе m[:, \"X\"]."
                ),
                'wrong': 'filterif("Пол" == "Ж")',
                'right': 'filterif(m[:, "Пол"] == "Ж")',
                'explanation': (
                    "Срез указывает, к какому столбцу применяется условие.\n"
                    "\n"
                    "Неправильно: filterif(\"Пол\" == \"Ж\")\n"
                    "Правильно: filterif(m[:, \"Пол\"] == \"Ж\")"
                ),
                'variants': [
                    'r = filterif(m[:, "Пол"] == "Ж")',
                    'r = filterif(m[2:10, "Пол"] == "Ж")',
                ],
            },
            'FILTERIF_REQUIRES_ASSIGNMENT': {
                'message': (
                    "filterif() возвращает значение — "
                    "результат нужно сохранить."
                ),
                'wrong': 'filterif(m[:, "Пол"] == "Ж")',
                'right': 'r = filterif(m[:, "Пол"] == "Ж")',
                'explanation': (
                    "filterif НЕ изменяет исходную матрицу.\n"
                    "Он ВОЗВРАЩАЕТ НОВУЮ.\n"
                    "\n"
                    "Правильно:\n"
                    "  r = filterif(...)     — в новую переменную\n"
                    "  m = filterif(m, ...)  — мутация\n"
                    "  print(filterif(...))  — вывод"
                ),
                'variants': [
                    'r = filterif(m[:, "Пол"] == "Ж")',
                    'm = filterif(m[:, "Пол"] == "Ж")',
                    'r = filterif(m[2:10, "Пол"] == "Ж")',
                ],
            },
            'FILTERIF_FUNCTION_IN_CONDITION': {
                'message': (
                    "filterif: в условии используется ФУНКЦИЯ — "
                    "так нельзя.\n"
                    "  filterif работает только с ГОТОВЫМ столбцом."
                ),
                'wrong': 'filterif(year(m[:, "Дата"]) == 2025)',
                'right': (
                    'm2 = addcolumn(m, "Год", year(m[:, "Дата"]))\n'
                    'r = filterif(m2[:, "Год"] == 2025)'
                ),
                'explanation': (
                    "filterif строит маску \"построчно\" по срезу.\n"
                    "Результат функции — это ВЕКТОР, его нельзя\n"
                    "сравнивать со скаляром построчно.\n"
                    "\n"
                    "РЕШЕНИЕ: материализуйте вектор в столбец\n"
                    "через addcolumn, потом фильтруйте по нему.\n"
                    "\n"
                    "  ❌  filterif(year(m[:, \"Дата\"]) == 2025)\n"
                    "\n"
                    "  ✅  m2 = addcolumn(m, \"Год\", year(m[:, \"Дата\"]))\n"
                    "      r = filterif(m2[:, \"Год\"] == 2025)\n"
                    "\n"
                    "Работает то же самое для:\n"
                    "  • month, day, quarter, hour, minute, second\n"
                    "  • round, int, frac, len\n"
                    "  • case, isnone, coalesce\n"
                    "  • trim, replacetext, clean"
                ),
                'variants': [
                    (
                        'm2 = addcolumn(m, "Год", year(m[:, "Дата"]))\n'
                        'r = filterif(m2[:, "Год"] == 2025)'
                    ),
                    (
                        'm2 = addcolumn(m, "Час", hour(m[:, "Время"]))\n'
                        'r = filterif(m2[:, "Час"] >= 18)'
                    ),
                    (
                        'm2 = addcolumn(m, "Цена_окр", round(m[:, "Цена"], 2))\n'
                        'r = filterif(m2[:, "Цена_окр"] > 100)'
                    ),
                ],
            },
        },
    },
}


EN = {
    'filterif': {
        'name': 'filterif',
        'category': 'filter',
        'signature': 'filterif(m[:, "X"] == "Y")',
        'description': (
            'Keep rows where the condition is true.\n'
            '  • Works with Matrix and DuckDB.\n'
            '  • Header is NOT removed.\n'
            '  • Row order is preserved.\n'
            '  • Returns a NEW matrix — save the result.'
        ),
        'examples': [
            'r = filterif(m[:, "Gender"] == "F")',
            'm = filterif(m[:, "Gender"] == "F")',
            'r = filterif(m[2:10, "Age"] > 25)',
            'r = filterif(m[:, "Age"] > 25 and m[:, "Dept"] == "IT")',
            'r = filterif(m[:, "Dept"] == "IT" or m[:, "Dept"] == "HR")',
            'r = filterif(not (m[:, "Dept"] == "IT"))',
            'r = filterif(v > 20)',
        ],
        'errors': {
            'FILTERIF_BAD_SYNTAX': {
                'message': (
                    "filterif: invalid syntax.\n"
                    "  Need a slice m[:, \"X\"] with a comparison."
                ),
                'wrong': 'filterif(m, "Gender" == "F")',
                'right': 'filterif(m[:, "Gender"] == "F")',
                'explanation': (
                    "First argument is a SLICE m[:, \"X\"],\n"
                    "which already contains the comparison condition.\n"
                    "\n"
                    "Structure:\n"
                    "  filterif(m[:, \"X\"] == \"Y\")\n"
                    "  filterif(m[:, \"X\"] > 10)\n"
                    "  filterif(m[:, \"X\"] == \"Y\" and m[:, \"Z\"] == \"W\")"
                ),
                'variants': [
                    'r = filterif(m[:, "Gender"] == "F")',
                    'r = filterif(m[2:10, "Age"] > 25)',
                    'r = filterif(m[:, "Age"] > 25 and m[:, "Dept"] == "IT")',
                    'r = filterif(v > 20)',
                ],
            },
            'FILTERIF_ASSIGN_IN_CONDITION': {
                'message': (
                    "filterif: '=' (assignment) is used "
                    "instead of '==' (comparison)."
                ),
                'wrong': 'filterif(m[:, "Gender"] = "F")',
                'right': 'filterif(m[:, "Gender"] == "F")',
                'explanation': (
                    "'=' — assigns.\n"
                    "'==' — compares.\n"
                    "\n"
                    "In filterif condition ALWAYS '=='."
                ),
                'variants': [
                    'r = filterif(m[:, "Gender"] == "F")',
                    'r = filterif(m[2:10, "Age"] > 25)',
                    'r = filterif(m[:, "Dept"] != "HR")',
                ],
            },
            'FILTERIF_AND_OPERATOR': {
                'message': "filterif: logical AND is 'and', not '&&'.",
                'wrong': 'filterif(m[:, "Gender"] == "F" && m[:, "Age"] > 25)',
                'right': 'filterif(m[:, "Gender"] == "F" and m[:, "Age"] > 25)',
                'explanation': (
                    "ArrayVator uses WORDS:\n"
                    "  'and' — AND\n"
                    "  'or'  — OR\n"
                    "  'not' — NOT"
                ),
                'variants': [
                    'r = filterif(m[:, "Gender"] == "F" and m[:, "Age"] > 25)',
                    'r = filterif(m[2:10, "Dept"] == "IT" or m[2:10, "Dept"] == "HR")',
                ],
            },
            'FILTERIF_OR_OPERATOR': {
                'message': "filterif: logical OR is 'or', not '||'.",
                'wrong': 'filterif(m[:, "Dept"] == "IT" || m[:, "Dept"] == "HR")',
                'right': 'filterif(m[:, "Dept"] == "IT" or m[:, "Dept"] == "HR")',
                'explanation': (
                    "ArrayVator uses WORDS:\n"
                    "  'and' — AND\n"
                    "  'or'  — OR\n"
                    "  'not' — NOT"
                ),
                'variants': [
                    'r = filterif(m[:, "Dept"] == "IT" or m[:, "Dept"] == "HR")',
                    'r = filterif(m[2:10, "Gender"] == "F" or m[2:10, "Gender"] == "M")',
                ],
            },
            'FILTERIF_NO_SLICE': {
                'message': (
                    "filterif: no slice.\n"
                    "  The condition must be on a slice m[:, \"X\"]."
                ),
                'wrong': 'filterif("Gender" == "F")',
                'right': 'filterif(m[:, "Gender"] == "F")',
                'explanation': (
                    "The slice specifies which column the condition applies to.\n"
                    "\n"
                    "Incorrect: filterif(\"Gender\" == \"F\")\n"
                    "Correct: filterif(m[:, \"Gender\"] == \"F\")"
                ),
                'variants': [
                    'r = filterif(m[:, "Gender"] == "F")',
                    'r = filterif(m[2:10, "Gender"] == "F")',
                ],
            },
            'FILTERIF_REQUIRES_ASSIGNMENT': {
                'message': (
                    "filterif() returns a value — "
                    "the result must be saved."
                ),
                'wrong': 'filterif(m[:, "Gender"] == "F")',
                'right': 'r = filterif(m[:, "Gender"] == "F")',
                'explanation': (
                    "filterif does NOT modify the source matrix.\n"
                    "It RETURNS a NEW one.\n"
                    "\n"
                    "Correct:\n"
                    "  r = filterif(...)     — to a new variable\n"
                    "  m = filterif(m, ...)  — mutation\n"
                    "  print(filterif(...))  — output"
                ),
                'variants': [
                    'r = filterif(m[:, "Gender"] == "F")',
                    'm = filterif(m[:, "Gender"] == "F")',
                    'r = filterif(m[2:10, "Gender"] == "F")',
                ],
            },
            'FILTERIF_FUNCTION_IN_CONDITION': {
                'message': (
                    "filterif: a FUNCTION is used in the condition — "
                    "this is not allowed.\n"
                    "  filterif works only with a READY column."
                ),
                'wrong': 'filterif(year(m[:, "Date"]) == 2025)',
                'right': (
                    'm2 = addcolumn(m, "Year", year(m[:, "Date"]))\n'
                    'r = filterif(m2[:, "Year"] == 2025)'
                ),
                'explanation': (
                    "filterif builds the mask \"row by row\" over the slice.\n"
                    "The result of a function is a VECTOR, it cannot be\n"
                    "compared to a scalar row by row.\n"
                    "\n"
                    "SOLUTION: materialize the vector into a column\n"
                    "via addcolumn, then filter by it.\n"
                    "\n"
                    "  ❌  filterif(year(m[:, \"Date\"]) == 2025)\n"
                    "\n"
                    "  ✅  m2 = addcolumn(m, \"Year\", year(m[:, \"Date\"]))\n"
                    "      r = filterif(m2[:, \"Year\"] == 2025)\n"
                    "\n"
                    "Works the same for:\n"
                    "  • month, day, quarter, hour, minute, second\n"
                    "  • round, int, frac, len\n"
                    "  • case, isnone, coalesce\n"
                    "  • trim, replacetext, clean"
                ),
                'variants': [
                    (
                        'm2 = addcolumn(m, "Year", year(m[:, "Date"]))\n'
                        'r = filterif(m2[:, "Year"] == 2025)'
                    ),
                    (
                        'm2 = addcolumn(m, "Hour", hour(m[:, "Time"]))\n'
                        'r = filterif(m2[:, "Hour"] >= 18)'
                    ),
                    (
                        'm2 = addcolumn(m, "Price_r", round(m[:, "Price"], 2))\n'
                        'r = filterif(m2[:, "Price_r"] > 100)'
                    ),
                ],
            },
        },
    },
}