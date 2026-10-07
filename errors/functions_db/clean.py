# errors/functions_db/clean.py
"""
База ошибок для функции CLEAN — очистка текста.

СИНТАКСИС:
    clean(данные, "digits")    — оставить только цифры
    clean(данные, "letters")   — оставить только буквы
    clean(данные, "special")   — оставить только спецсимволы
    clean(данные, "alnum")     — оставить только буквы и цифры

Работает с Matrix и DuckDB.
"""


RU = {
    'clean': {
        'name': 'clean',
        'category': 'string',
        'signature': 'clean(данные, "режим")',
        'description': (
            'Очистка текста: удаляет всё, кроме указанного типа символов.\n'
            '  • "digits"  — только цифры 0-9\n'
            '  • "letters" — только буквы\n'
            '  • "special" — только спецсимволы\n'
            '  • "alnum"   — буквы И цифры\n'
            '  • Работает с Matrix и DuckDB.\n'
            '  • Возвращает НОВУЮ матрицу — результат нужно сохранить.'
        ),
        'examples': [
            'm = clean(m[:, "Код"], "digits")',
            'm = clean(m[:, "Имя"], "letters")',
            'r = clean("+7 (999) 123-45-67", "digits")',
        ],
        'errors': {
            'CLEAN_BAD_SYNTAX': {
                'message': (
                    "clean: неверный синтаксис.\n"
                    "  Нужны данные и режим очистки."
                ),
                'wrong': 'clean(m)',
                'right': 'clean(m[:, "Код"], "digits")',
                'explanation': (
                    "clean принимает ДВА аргумента:\n"
                    "  1. данные\n"
                    "  2. режим — строка в кавычках\n"
                    "\n"
                    "Неправильно:\n"
                    "     clean(m)\n"
                    "     clean(m[:, \"Код\"])\n"
                    "\n"
                    "Правильно:\n"
                    "     clean(m[:, \"Код\"], \"digits\")"
                ),
                'variants': [
                    'm = clean(m[:, "Код"], "digits")',
                    'm = clean(m[:, "Имя"], "letters")',
                ],
            },
            'CLEAN_BAD_MODE': {
                'message': (
                    "clean: неверный режим.\n"
                    "  Допустимо: digits, letters, special, alnum."
                ),
                'wrong': 'clean(m[:, "Код"], "numbers")',
                'right': 'clean(m[:, "Код"], "digits")',
                'explanation': (
                    "Только четыре режима:\n"
                    "     \"digits\"    — только цифры 0-9\n"
                    "     \"letters\"   — только буквы\n"
                    "     \"special\"   — только спецсимволы\n"
                    "     \"alnum\"     — буквы И цифры\n"
                    "\n"
                    "Неправильно:\n"
                    "     clean(m[:, \"X\"], \"numbers\")\n"
                    "     clean(m[:, \"X\"], \"text\")\n"
                    "\n"
                    "Правильно:\n"
                    "     clean(m[:, \"X\"], \"digits\")"
                ),
                'variants': [
                    'm = clean(m[:, "Код"], "digits")',
                    'm = clean(m[:, "Имя"], "letters")',
                    'm = clean(m[:, "Тел"], "alnum")',
                ],
            },
            'CLEAN_MODE_NOT_STRING': {
                'message': (
                    "clean: режим должен быть строкой в кавычках."
                ),
                'wrong': 'clean(m[:, "Код"], digits)',
                'right': 'clean(m[:, "Код"], "digits")',
                'explanation': (
                    "Режим — строка В КАВЫЧКАХ:\n"
                    "     clean(m[:, \"X\"], \"digits\")\n"
                    "     clean(m[:, \"X\"], \"letters\")\n"
                    "\n"
                    "Неправильно:\n"
                    "     clean(m[:, \"X\"], digits)     — без кавычек\n"
                    "\n"
                    "Правильно:\n"
                    "     clean(m[:, \"X\"], \"digits\")"
                ),
                'variants': [
                    'm = clean(m[:, "Код"], "digits")',
                    'm = clean(m[:, "Код"], "alnum")',
                ],
            },
            'CLEAN_DUCKDB_MODE': {
                'message': (
                    "clean: неверный режим для BigData (DuckDB)."
                ),
                'wrong': 'r = clean(bd[:, "X"], "unknown")',
                'right': 'r = clean(bd[:, "X"], "digits")',
                'explanation': (
                    "Для BigData (DuckDB) — те же четыре режима:\n"
                    "     \"digits\"    — только цифры\n"
                    "     \"letters\"   — только буквы\n"
                    "     \"special\"   — только спецсимволы\n"
                    "     \"alnum\"     — буквы И цифры\n"
                    "\n"
                    "Правильно:\n"
                    "     clean(bd[:, \"X\"], \"digits\")"
                ),
                'variants': [
                    'r = clean(bd[:, "X"], "digits")',
                    'r = clean(bd[:, "X"], "letters")',
                ],
            },
            'CLEAN_REQUIRES_ASSIGNMENT': {
                'message': (
                    "clean() возвращает значение — "
                    "результат нужно сохранить."
                ),
                'wrong': 'clean(m[:, "Код"], "digits")',
                'right': 'm = clean(m[:, "Код"], "digits")',
                'explanation': (
                    "clean НЕ изменяет исходную матрицу.\n"
                    "Он ВОЗВРАЩАЕТ НОВУЮ.\n"
                    "\n"
                    "Правильно:\n"
                    "  r = clean(...)      — в новую переменную\n"
                    "  m = clean(...)      — мутация"
                ),
                'variants': [
                    'r = clean(m[:, "Код"], "digits")',
                    'm = clean(m[:, "Код"], "digits")',
                ],
            },
        },
    },
}


EN = {
    'clean': {
        'name': 'clean',
        'category': 'string',
        'signature': 'clean(data, "mode")',
        'description': (
            'Clean text: remove everything except the specified character type.\n'
            '  • "digits"  — only digits 0-9\n'
            '  • "letters" — only letters\n'
            '  • "special" — only special characters\n'
            '  • "alnum"   — letters AND digits\n'
            '  • Works with Matrix and DuckDB.\n'
            '  • Returns a NEW matrix — save the result.'
        ),
        'examples': [
            'm = clean(m[:, "Code"], "digits")',
            'm = clean(m[:, "Name"], "letters")',
            'r = clean("+1 (555) 123-45-67", "digits")',
        ],
        'errors': {
            'CLEAN_BAD_SYNTAX': {
                'message': (
                    "clean: invalid syntax.\n"
                    "  Need data and a cleaning mode."
                ),
                'wrong': 'clean(m)',
                'right': 'clean(m[:, "Code"], "digits")',
                'explanation': (
                    "clean takes TWO arguments:\n"
                    "  1. data\n"
                    "  2. mode — string in quotes\n"
                    "\n"
                    "Incorrect:\n"
                    "     clean(m)\n"
                    "     clean(m[:, \"Code\"])\n"
                    "\n"
                    "Correct:\n"
                    "     clean(m[:, \"Code\"], \"digits\")"
                ),
                'variants': [
                    'm = clean(m[:, "Code"], "digits")',
                    'm = clean(m[:, "Name"], "letters")',
                ],
            },
            'CLEAN_BAD_MODE': {
                'message': (
                    "clean: invalid mode.\n"
                    "  Allowed: digits, letters, special, alnum."
                ),
                'wrong': 'clean(m[:, "Code"], "numbers")',
                'right': 'clean(m[:, "Code"], "digits")',
                'explanation': (
                    "Only four modes:\n"
                    "     \"digits\"    — only digits 0-9\n"
                    "     \"letters\"   — only letters\n"
                    "     \"special\"   — only special characters\n"
                    "     \"alnum\"     — letters AND digits\n"
                    "\n"
                    "Incorrect:\n"
                    "     clean(m[:, \"X\"], \"numbers\")\n"
                    "     clean(m[:, \"X\"], \"text\")\n"
                    "\n"
                    "Correct:\n"
                    "     clean(m[:, \"X\"], \"digits\")"
                ),
                'variants': [
                    'm = clean(m[:, "Code"], "digits")',
                    'm = clean(m[:, "Name"], "letters")',
                    'm = clean(m[:, "Phone"], "alnum")',
                ],
            },
            'CLEAN_MODE_NOT_STRING': {
                'message': (
                    "clean: mode must be a string in quotes."
                ),
                'wrong': 'clean(m[:, "Code"], digits)',
                'right': 'clean(m[:, "Code"], "digits")',
                'explanation': (
                    "Mode is a string IN QUOTES:\n"
                    "     clean(m[:, \"X\"], \"digits\")\n"
                    "     clean(m[:, \"X\"], \"letters\")\n"
                    "\n"
                    "Incorrect:\n"
                    "     clean(m[:, \"X\"], digits)     — no quotes\n"
                    "\n"
                    "Correct:\n"
                    "     clean(m[:, \"X\"], \"digits\")"
                ),
                'variants': [
                    'm = clean(m[:, "Code"], "digits")',
                    'm = clean(m[:, "Code"], "alnum")',
                ],
            },
            'CLEAN_DUCKDB_MODE': {
                'message': (
                    "clean: invalid mode for BigData (DuckDB)."
                ),
                'wrong': 'r = clean(bd[:, "X"], "unknown")',
                'right': 'r = clean(bd[:, "X"], "digits")',
                'explanation': (
                    "For BigData (DuckDB) — the same four modes:\n"
                    "     \"digits\"    — only digits\n"
                    "     \"letters\"   — only letters\n"
                    "     \"special\"   — only special characters\n"
                    "     \"alnum\"     — letters AND digits\n"
                    "\n"
                    "Correct:\n"
                    "     clean(bd[:, \"X\"], \"digits\")"
                ),
                'variants': [
                    'r = clean(bd[:, "X"], "digits")',
                    'r = clean(bd[:, "X"], "letters")',
                ],
            },
            'CLEAN_REQUIRES_ASSIGNMENT': {
                'message': (
                    "clean() returns a value — "
                    "the result must be saved."
                ),
                'wrong': 'clean(m[:, "Code"], "digits")',
                'right': 'm = clean(m[:, "Code"], "digits")',
                'explanation': (
                    "clean does NOT modify the source matrix.\n"
                    "It RETURNS a NEW one.\n"
                    "\n"
                    "Correct:\n"
                    "  r = clean(...)      — to a new variable\n"
                    "  m = clean(...)      — mutation"
                ),
                'variants': [
                    'r = clean(m[:, "Code"], "digits")',
                    'm = clean(m[:, "Code"], "digits")',
                ],
            },
        },
    },
}