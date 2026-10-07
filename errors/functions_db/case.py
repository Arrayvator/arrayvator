# errors/functions_db/case.py
"""
База ошибок для функции CASE — условное преобразование.

СИНТАКСИС:
    case(срез,
         when <условие> then <значение>,
         when <условие> then <значение>,
         else <значение>)

ОПЕРАТОРЫ В WHEN:
    < 18
    > 50
    <= 30
    >= 18
    == "IT"
    != "X"
"""


RU = {
    'case': {
        'name': 'case',
        'category': 'case',
        'signature': (
            'case(срез, when <условие> then <значение>, ..., '
            'else <значение>)'
        ),
        'description': (
            'Условное преобразование значений.\n'
            '  • Работает с Matrix и DuckDB.\n'
            '  • Условия проверяются СВЕРХУ ВНИЗ.\n'
            '  • Если ни одно не подошло и нет else — None.\n'
            '  • Возвращает МАТРИЦУ с заменённым столбцом.'
        ),
        'examples': [
            'r = case(m[:, "Возраст"], when < 18 then "Дитя", else "Взрослый")',
            'r = case(m[:, "Отдел"], when == "IT" then "Технический", else "Другой")',
            'm = case(m[:, "Возраст"], when < 18 then "Дитя", else "Взрослый")',
            'r = case(m[2:10, "Возраст"], when < 18 then "Дитя", else "Взрослый")',
        ],
        'errors': {
            'CASE_BAD_SYNTAX': {
                'message': (
                    "case: неверный синтаксис.\n"
                    "  Нужен срез и хотя бы один блок when ... then."
                ),
                'wrong': 'r = case(m[:, "Возраст"])',
                'right': (
                    'r = case(m[:, "Возраст"], '
                    'when < 18 then "Дитя", else "Взрослый")'
                ),
                'explanation': (
                    "case принимает СРЕЗ и хотя бы ОДИН блок when.\n"
                    "\n"
                    "Структура:\n"
                    "  case(срез,\n"
                    "       when <условие> then <значение>,\n"
                    "       ...,\n"
                    "       else <значение>)"
                ),
                'variants': [
                    'r = case(m[:, "Возраст"], when < 18 then "Дитя", else "Взрослый")',
                    'r = case(m[2:10, "Возраст"], when < 18 then "Дитя", else "Взрослый")',
                    'r = case(m[:, "Отдел"], when == "IT" then "Технический", else "Другой")',
                ],
            },
            'CASE_NO_WHEN': {
                'message': (
                    "case: нужен хотя бы один блок when ... then."
                ),
                'wrong': 'r = case(m[:, "Возраст"], else "Взрослый")',
                'right': (
                    'r = case(m[:, "Возраст"], '
                    'when < 18 then "Дитя", else "Взрослый")'
                ),
                'explanation': (
                    "else сам по себе не работает — нужен хотя бы\n"
                    "один блок when, который преобразует значение.\n"
                    "\n"
                    "Порядок:\n"
                    "  when <условие> then <значение>,\n"
                    "  ...,\n"
                    "  else <значение>"
                ),
                'variants': [
                    'r = case(m[:, "Возраст"], when < 18 then "Дитя", else "Взрослый")',
                    'r = case(m[2:10, "Возраст"], when < 18 then "Дитя", else "Взрослый")',
                ],
            },
            'CASE_NO_THEN': {
                'message': (
                    "case: после условия when нужно ключевое слово 'then'."
                ),
                'wrong': 'r = case(m[:, "Возраст"], when < 18 "Дитя", else "Взрослый")',
                'right': (
                    'r = case(m[:, "Возраст"], '
                    'when < 18 then "Дитя", else "Взрослый")'
                ),
                'explanation': (
                    "'then' отделяет условие when от результата.\n"
                    "\n"
                    "Структура:\n"
                    "  when <условие> then <значение>"
                ),
                'variants': [
                    'r = case(m[:, "Возраст"], when < 18 then "Дитя", else "Взрослый")',
                    'r = case(m[2:10, "Возраст"], when < 18 then "Дитя", else "Взрослый")',
                    'r = case(m[:, "Отдел"], when == "IT" then "Технический", else "Другой")',
                ],
            },
            'CASE_ASSIGN_IN_CONDITION': {
                'message': (
                    "case: в условии when используется '=' (присваивание), "
                    "а нужно '==' (сравнение)."
                ),
                'wrong': 'r = case(m[:, "Отдел"], when = "IT" then "Технический", else "Другой")',
                'right': 'r = case(m[:, "Отдел"], when == "IT" then "Технический", else "Другой")',
                'explanation': (
                    "'=' — присваивание.\n"
                    "'==' — сравнение.\n"
                    "\n"
                    "В when для проверки равенства пишите '=='."
                ),
                'variants': [
                    'r = case(m[:, "Отдел"], when == "IT" then "Технический", else "Другой")',
                    'r = case(m[2:10, "Отдел"], when == "IT" then "Технический", else "Другой")',
                ],
            },
            'CASE_BAD_ELSE': {
                'message': (
                    "case: else должен быть последним и идти без when."
                ),
                'wrong': 'r = case(m[:, "Возраст"], else "Взрослый", when < 18 then "Дитя")',
                'right': (
                    'r = case(m[:, "Возраст"], '
                    'when < 18 then "Дитя", else "Взрослый")'
                ),
                'explanation': (
                    "else — завершающий блок.\n"
                    "Все when должны идти ДО else.\n"
                    "\n"
                    "Порядок:\n"
                    "  when ..., when ..., else ..."
                ),
                'variants': [
                    'r = case(m[:, "Возраст"], when < 18 then "Дитя", else "Взрослый")',
                    'r = case(m[2:10, "Возраст"], when < 18 then "Дитя", else "Взрослый")',
                ],
            },
        },
    },
}


EN = {
    'case': {
        'name': 'case',
        'category': 'case',
        'signature': (
            'case(slice, when <condition> then <value>, ..., '
            'else <value>)'
        ),
        'description': (
            'Conditional transformation of values.\n'
            '  • Works with Matrix and DuckDB.\n'
            '  • Conditions are checked TOP-DOWN.\n'
            '  • If none matched and no else — None.\n'
            '  • Returns a MATRIX with the replaced column.'
        ),
        'examples': [
            'r = case(m[:, "Age"], when < 18 then "Child", else "Adult")',
            'r = case(m[:, "Dept"], when == "IT" then "Technical", else "Other")',
            'm = case(m[:, "Age"], when < 18 then "Child", else "Adult")',
            'r = case(m[2:10, "Age"], when < 18 then "Child", else "Adult")',
        ],
        'errors': {
            'CASE_BAD_SYNTAX': {
                'message': (
                    "case: invalid syntax.\n"
                    "  Need a slice and at least one when ... then block."
                ),
                'wrong': 'r = case(m[:, "Age"])',
                'right': (
                    'r = case(m[:, "Age"], '
                    'when < 18 then "Child", else "Adult")'
                ),
                'explanation': (
                    "case accepts a SLICE and at least ONE when block.\n"
                    "\n"
                    "Structure:\n"
                    "  case(slice,\n"
                    "       when <condition> then <value>,\n"
                    "       ...,\n"
                    "       else <value>)"
                ),
                'variants': [
                    'r = case(m[:, "Age"], when < 18 then "Child", else "Adult")',
                    'r = case(m[2:10, "Age"], when < 18 then "Child", else "Adult")',
                    'r = case(m[:, "Dept"], when == "IT" then "Technical", else "Other")',
                ],
            },
            'CASE_NO_WHEN': {
                'message': (
                    "case: at least one when ... then block is required."
                ),
                'wrong': 'r = case(m[:, "Age"], else "Adult")',
                'right': (
                    'r = case(m[:, "Age"], '
                    'when < 18 then "Child", else "Adult")'
                ),
                'explanation': (
                    "else alone does not work — need at least\n"
                    "one when block that transforms the value.\n"
                    "\n"
                    "Order:\n"
                    "  when <condition> then <value>,\n"
                    "  ...,\n"
                    "  else <value>"
                ),
                'variants': [
                    'r = case(m[:, "Age"], when < 18 then "Child", else "Adult")',
                    'r = case(m[2:10, "Age"], when < 18 then "Child", else "Adult")',
                ],
            },
            'CASE_NO_THEN': {
                'message': (
                    "case: after when condition, keyword 'then' is needed."
                ),
                'wrong': 'r = case(m[:, "Age"], when < 18 "Child", else "Adult")',
                'right': (
                    'r = case(m[:, "Age"], '
                    'when < 18 then "Child", else "Adult")'
                ),
                'explanation': (
                    "'then' separates the when condition from the result.\n"
                    "\n"
                    "Structure:\n"
                    "  when <condition> then <value>"
                ),
                'variants': [
                    'r = case(m[:, "Age"], when < 18 then "Child", else "Adult")',
                    'r = case(m[2:10, "Age"], when < 18 then "Child", else "Adult")',
                    'r = case(m[:, "Dept"], when == "IT" then "Technical", else "Other")',
                ],
            },
            'CASE_ASSIGN_IN_CONDITION': {
                'message': (
                    "case: in when condition, '=' (assignment) is used "
                    "instead of '==' (comparison)."
                ),
                'wrong': 'r = case(m[:, "Dept"], when = "IT" then "Technical", else "Other")',
                'right': 'r = case(m[:, "Dept"], when == "IT" then "Technical", else "Other")',
                'explanation': (
                    "'=' — assignment.\n"
                    "'==' — comparison.\n"
                    "\n"
                    "In when, use '==' to test equality."
                ),
                'variants': [
                    'r = case(m[:, "Dept"], when == "IT" then "Technical", else "Other")',
                    'r = case(m[2:10, "Dept"], when == "IT" then "Technical", else "Other")',
                ],
            },
            'CASE_BAD_ELSE': {
                'message': (
                    "case: else must be the last block, without when."
                ),
                'wrong': 'r = case(m[:, "Age"], else "Adult", when < 18 then "Child")',
                'right': (
                    'r = case(m[:, "Age"], '
                    'when < 18 then "Child", else "Adult")'
                ),
                'explanation': (
                    "else is the terminating block.\n"
                    "All when blocks must come BEFORE else.\n"
                    "\n"
                    "Order:\n"
                    "  when ..., when ..., else ..."
                ),
                'variants': [
                    'r = case(m[:, "Age"], when < 18 then "Child", else "Adult")',
                    'r = case(m[2:10, "Age"], when < 18 then "Child", else "Adult")',
                ],
            },
        },
    },
}