# errors/functions_db/unpivot.py
"""
База ошибок для функции UNPIVOT — разворот широкой таблицы в длинную.

СИНТАКСИС:
    unpivot(срез, by срез)
    unpivot(срез, by срез, names "Имя1", "Имя2")

ПРАВИЛА:
    - Первый срез — столбцы, которые складываем.
    - by — столбцы-идентификаторы.
    - by и data НЕ должны пересекаться.
    - names — имена двух новых колонок (опционально).
    - Работает с Matrix (RAM) и DuckDB (BigData).
"""

RU = {
    'unpivot': {
        'name': 'unpivot',
        'category': 'analytics',
        'signature': 'unpivot(срез, by срез [, names "Имя1", "Имя2"])',
        'description': (
            'Разворачивает широкую таблицу в длинную.\n'
            '  • Первый срез — столбцы, которые складываем.\n'
            '  • by — столбцы-идентификаторы (не пересекаются с data).\n'
            '  • names — имена двух новых колонок (опц.).\n'
            '  • По умолчанию: "Переменная" и "Значение".\n'
            '  • Работает с Matrix (RAM) и DuckDB (BigData).\n'
            '  • Возвращает НОВУЮ таблицу — результат нужно сохранить.'
        ),
        'examples': [
            'r = unpivot(m[:, 2:end], by m[:, "Страна"])',
            'r = unpivot(m[:, 2:end], by m[:, "Страна"], names "Год", "Население")',
        ],
        'errors': {
            'UNPIVOT_BAD_SYNTAX': {
                'message': (
                    "unpivot: неверный синтаксис.\n"
                    "  Нужен срез данных и параметр 'by'."
                ),
                'wrong': 'r = unpivot(m[:, 2:end])',
                'right': 'r = unpivot(m[:, 2:end], by m[:, "Страна"])',
                'explanation': (
                    "unpivot принимает минимум ДВА аргумента:\n"
                    "  1. срез данных — что складываем\n"
                    "  2. by срез — идентификаторы\n"
                    "\n"
                    "Структура:\n"
                    "  unpivot(срез, by срез)\n"
                    "  unpivot(срез, by срез, names \"Имя1\", \"Имя2\")"
                ),
                'variants': [
                    'r = unpivot(m[:, 2:end], by m[:, "Страна"])',
                    'r = unpivot(m[:, 2:end], by m[:, "Страна"], names "Год", "Население")',
                ],
            },
            'UNPIVOT_NEED_BY': {
                'message': (
                    "unpivot: пропущено ключевое слово 'by'.\n"
                    "  Без него неясно, какие столбцы считать идентификаторами."
                ),
                'wrong': 'r = unpivot(m[:, 2:end], m[:, "Страна"])',
                'right': 'r = unpivot(m[:, 2:end], by m[:, "Страна"])',
                'explanation': (
                    "'by' — обязательный маркер блока идентификаторов.\n"
                    "\n"
                    "Структура:\n"
                    "  unpivot(срез, by срез)\n"
                    "                ^^\n"
                    "                тут 'by'"
                ),
                'variants': [
                    'r = unpivot(m[:, 2:end], by m[:, "Страна"])',
                    'r = unpivot(m[:, 2:end], by m[:, "Страна"], names "Год", "Население")',
                ],
            },
            'UNPIVOT_BAD_DATA_SLICE': {
                'message': (
                    "unpivot: 1-й аргумент — срез столбцов m[:, ...].\n"
                    "  Нельзя передать целую матрицу или скаляр."
                ),
                'wrong': 'r = unpivot(m, by m[:, "Страна"])',
                'right': 'r = unpivot(m[:, 2:end], by m[:, "Страна"])',
                'explanation': (
                    "Первый аргумент — это СРЕЗ столбцов, которые надо сложить.\n"
                    "\n"
                    "Неправильно:\n"
                    "     unpivot(m, by m[:, \"Страна\"])\n"
                    "     unpivot(m[:, \"Страна\"], by m[:, \"Страна\"])\n"
                    "\n"
                    "Правильно:\n"
                    "     unpivot(m[:, 2:end], by m[:, \"Страна\"])"
                ),
                'variants': [
                    'r = unpivot(m[:, 2:end], by m[:, "Страна"])',
                    'r = unpivot(m[:, 2:5], by m[:, 1])',
                ],
            },
            'UNPIVOT_BAD_BY_SLICE': {
                'message': (
                    "unpivot: 'by' должен быть срезом m[:, ...].\n"
                    "  Не строкой и не числом."
                ),
                'wrong': 'r = unpivot(m[:, 2:end], by "Страна")',
                'right': 'r = unpivot(m[:, 2:end], by m[:, "Страна"])',
                'explanation': (
                    "by принимает СРЕЗ столбца-идентификатора:\n"
                    "     by m[:, \"Страна\"]\n"
                    "     by m[:, 1]\n"
                    "\n"
                    "Неправильно:\n"
                    "     by \"Страна\"\n"
                    "     by 1"
                ),
                'variants': [
                    'r = unpivot(m[:, 2:end], by m[:, "Страна"])',
                    'r = unpivot(m[:, 2:end], by m[:, 1])',
                ],
            },
            'UNPIVOT_COLUMN_OVERLAP': {
                'message': (
                    "unpivot: колонки не должны пересекаться между "
                    "'складываем' и 'by'."
                ),
                'wrong': (
                    'r = unpivot(m[:, 1:end], by m[:, "Страна"])'
                ),
                'right': (
                    'r = unpivot(m[:, 2:end], by m[:, "Страна"])'
                ),
                'explanation': (
                    "Столбец-идентификатор не может одновременно\n"
                    "быть в 'складываем' и в 'by'.\n"
                    "\n"
                    "Неправильно:\n"
                    "     unpivot(m[:, 1:end], by m[:, \"Страна\"])\n"
                    "     ↑ тут \"Страна\" и в data, и в by\n"
                    "\n"
                    "Правильно:\n"
                    "     unpivot(m[:, 2:end], by m[:, \"Страна\"])"
                ),
                'variants': [
                    'r = unpivot(m[:, 2:end], by m[:, "Страна"])',
                    'r = unpivot(m[:, 3:end], by m[:, 1:2])',
                ],
            },
            'UNPIVOT_BAD_NAMES': {
                'message': (
                    "unpivot: names требует РОВНО ДВА имени.\n"
                    "  Пример: names \"Год\", \"Население\"."
                ),
                'wrong': 'r = unpivot(m[:, 2:end], by m[:, "Страна"], names "Год")',
                'right': 'r = unpivot(m[:, 2:end], by m[:, "Страна"], names "Год", "Население")',
                'explanation': (
                    "names принимает ДВА имени через запятую:\n"
                    "     names \"Имя1\", \"Имя2\"\n"
                    "\n"
                    "Первое — для колонки с именами переменных.\n"
                    "Второе — для колонки со значениями.\n"
                    "\n"
                    "Неправильно:\n"
                    "     names \"Год\"\n"
                    "     names \"Год\", \"Население\", \"Ещё\""
                ),
                'variants': [
                    'r = unpivot(m[:, 2:end], by m[:, "Страна"])',
                    'r = unpivot(m[:, 2:end], by m[:, "Страна"], names "Год", "Население")',
                ],
            },
            'UNPIVOT_REQUIRES_ASSIGNMENT': {
                'message': (
                    "unpivot() возвращает значение — "
                    "результат нужно сохранить."
                ),
                'wrong': 'unpivot(m[:, 2:end], by m[:, "Страна"])',
                'right': 'r = unpivot(m[:, 2:end], by m[:, "Страна"])',
                'explanation': (
                    "unpivot НЕ изменяет исходную таблицу.\n"
                    "Он ВОЗВРАЩАЕТ НОВУЮ.\n"
                    "\n"
                    "Правильно:\n"
                    "  r = unpivot(...)      — в новую переменную\n"
                    "  m = unpivot(...)      — мутация"
                ),
                'variants': [
                    'r = unpivot(m[:, 2:end], by m[:, "Страна"])',
                    'm = unpivot(m[:, 2:end], by m[:, "Страна"])',
                ],
            },
        },
    },
}


EN = {
    'unpivot': {
        'name': 'unpivot',
        'category': 'analytics',
        'signature': 'unpivot(slice, by slice [, names "Name1", "Name2"])',
        'description': (
            'Unpivot a wide table into a long one.\n'
            '  • First slice — columns to unpivot.\n'
            '  • by — identifier columns (must not overlap with data).\n'
            '  • names — names of two new columns (optional).\n'
            '  • Defaults: "Переменная" and "Значение".\n'
            '  • Works with Matrix (RAM) and DuckDB (BigData).\n'
            '  • Returns a NEW table — save the result.'
        ),
        'examples': [
            'r = unpivot(m[:, 2:end], by m[:, "Country"])',
            'r = unpivot(m[:, 2:end], by m[:, "Country"], names "Year", "Population")',
        ],
        'errors': {
            'UNPIVOT_BAD_SYNTAX': {
                'message': (
                    "unpivot: invalid syntax.\n"
                    "  Need a data slice and the 'by' parameter."
                ),
                'wrong': 'r = unpivot(m[:, 2:end])',
                'right': 'r = unpivot(m[:, 2:end], by m[:, "Country"])',
                'explanation': (
                    "unpivot takes at least TWO arguments:\n"
                    "  1. data slice — what to unpivot\n"
                    "  2. by slice — identifiers\n"
                    "\n"
                    "Structure:\n"
                    "  unpivot(slice, by slice)\n"
                    "  unpivot(slice, by slice, names \"Name1\", \"Name2\")"
                ),
                'variants': [
                    'r = unpivot(m[:, 2:end], by m[:, "Country"])',
                    'r = unpivot(m[:, 2:end], by m[:, "Country"], names "Year", "Population")',
                ],
            },
            'UNPIVOT_NEED_BY': {
                'message': (
                    "unpivot: keyword 'by' is missing.\n"
                    "  Without it, it's unclear which columns are identifiers."
                ),
                'wrong': 'r = unpivot(m[:, 2:end], m[:, "Country"])',
                'right': 'r = unpivot(m[:, 2:end], by m[:, "Country"])',
                'explanation': (
                    "'by' is a required marker for the identifiers block.\n"
                    "\n"
                    "Structure:\n"
                    "  unpivot(slice, by slice)\n"
                    "                ^^\n"
                    "                here 'by'"
                ),
                'variants': [
                    'r = unpivot(m[:, 2:end], by m[:, "Country"])',
                    'r = unpivot(m[:, 2:end], by m[:, "Country"], names "Year", "Population")',
                ],
            },
            'UNPIVOT_BAD_DATA_SLICE': {
                'message': (
                    "unpivot: 1st argument must be a slice m[:, ...].\n"
                    "  Cannot pass the whole matrix or a scalar."
                ),
                'wrong': 'r = unpivot(m, by m[:, "Country"])',
                'right': 'r = unpivot(m[:, 2:end], by m[:, "Country"])',
                'explanation': (
                    "First argument is a SLICE of columns to unpivot.\n"
                    "\n"
                    "Incorrect:\n"
                    "     unpivot(m, by m[:, \"Country\"])\n"
                    "     unpivot(m[:, \"Country\"], by m[:, \"Country\"])\n"
                    "\n"
                    "Correct:\n"
                    "     unpivot(m[:, 2:end], by m[:, \"Country\"])"
                ),
                'variants': [
                    'r = unpivot(m[:, 2:end], by m[:, "Country"])',
                    'r = unpivot(m[:, 2:5], by m[:, 1])',
                ],
            },
            'UNPIVOT_BAD_BY_SLICE': {
                'message': (
                    "unpivot: 'by' must be a slice m[:, ...].\n"
                    "  Not a string, not a number."
                ),
                'wrong': 'r = unpivot(m[:, 2:end], by "Country")',
                'right': 'r = unpivot(m[:, 2:end], by m[:, "Country"])',
                'explanation': (
                    "by takes a column SLICE of the identifier:\n"
                    "     by m[:, \"Country\"]\n"
                    "     by m[:, 1]\n"
                    "\n"
                    "Incorrect:\n"
                    "     by \"Country\"\n"
                    "     by 1"
                ),
                'variants': [
                    'r = unpivot(m[:, 2:end], by m[:, "Country"])',
                    'r = unpivot(m[:, 2:end], by m[:, 1])',
                ],
            },
            'UNPIVOT_COLUMN_OVERLAP': {
                'message': (
                    "unpivot: columns must not overlap between "
                    "'data' and 'by'."
                ),
                'wrong': (
                    'r = unpivot(m[:, 1:end], by m[:, "Country"])'
                ),
                'right': (
                    'r = unpivot(m[:, 2:end], by m[:, "Country"])'
                ),
                'explanation': (
                    "An identifier column cannot be BOTH\n"
                    "in 'data' and in 'by'.\n"
                    "\n"
                    "Incorrect:\n"
                    "     unpivot(m[:, 1:end], by m[:, \"Country\"])\n"
                    "     ↑ \"Country\" in both data and by\n"
                    "\n"
                    "Correct:\n"
                    "     unpivot(m[:, 2:end], by m[:, \"Country\"])"
                ),
                'variants': [
                    'r = unpivot(m[:, 2:end], by m[:, "Country"])',
                    'r = unpivot(m[:, 3:end], by m[:, 1:2])',
                ],
            },
            'UNPIVOT_BAD_NAMES': {
                'message': (
                    "unpivot: names requires EXACTLY TWO names.\n"
                    "  Example: names \"Year\", \"Population\"."
                ),
                'wrong': 'r = unpivot(m[:, 2:end], by m[:, "Country"], names "Year")',
                'right': 'r = unpivot(m[:, 2:end], by m[:, "Country"], names "Year", "Population")',
                'explanation': (
                    "names takes TWO names separated by comma:\n"
                    "     names \"Name1\", \"Name2\"\n"
                    "\n"
                    "First — for the column with variable names.\n"
                    "Second — for the column with values.\n"
                    "\n"
                    "Incorrect:\n"
                    "     names \"Year\"\n"
                    "     names \"Year\", \"Population\", \"Extra\""
                ),
                'variants': [
                    'r = unpivot(m[:, 2:end], by m[:, "Country"])',
                    'r = unpivot(m[:, 2:end], by m[:, "Country"], names "Year", "Population")',
                ],
            },
            'UNPIVOT_REQUIRES_ASSIGNMENT': {
                'message': (
                    "unpivot() returns a value — "
                    "the result must be saved."
                ),
                'wrong': 'unpivot(m[:, 2:end], by m[:, "Country"])',
                'right': 'r = unpivot(m[:, 2:end], by m[:, "Country"])',
                'explanation': (
                    "unpivot does NOT modify the source table.\n"
                    "It RETURNS a NEW one.\n"
                    "\n"
                    "Correct:\n"
                    "  r = unpivot(...)      — to a new variable\n"
                    "  m = unpivot(...)      — mutation"
                ),
                'variants': [
                    'r = unpivot(m[:, 2:end], by m[:, "Country"])',
                    'm = unpivot(m[:, 2:end], by m[:, "Country"])',
                ],
            },
        },
    },
}