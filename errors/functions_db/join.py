# errors/functions_db/join.py
"""
База ошибок для функции JOIN — соединение двух таблиц по ключу.

СИНТАКСИС:
    join(m1, m2, on "ID")
    join(m1, m2, on "ID", how "left")
    join(m1, m2, on ["ID", "Дата"])
    join(m1, m2, on "ID" == "Код")
    join(m1, m2, on "ID", suffixes ["_1", "_2"])

РЕЖИМЫ HOW:
    "left"  (по умолчанию) — все строки левой + совпадения
    "inner" — только совпадения
    "right" — все строки правой
    "outer" — все строки обеих

⚠️  Работает с Matrix (RAM) и DuckDB (BigData).
"""


RU = {
    'join': {
        'name': 'join',
        'category': 'join',
        'signature': 'join(m1, m2, on "ID" [, how "left"] [, suffixes [...]])',
        'description': (
            'Соединение двух таблиц по ключу.\n'
            '  • on — обязательный параметр.\n'
            '  • how — left (по умолчанию), inner, right, outer.\n'
            '  • suffixes — суффиксы для конфликтующих имён.\n'
            '  • Работает с Matrix и DuckDB.\n'
            '  • Возвращает НОВУЮ матрицу.'
        ),
        'examples': [
            'r = join(m1, m2, on "ID")',
            'r = join(m1, m2, on "ID", how "inner")',
            'r = join(m1, m2, on ["ID", "Дата"])',
            'r = join(m1, m2, on "ID" == "Код")',
            'r = join(m1, m2, on "ID", suffixes ["_1", "_2"])',
        ],
        'errors': {
            'JOIN_BAD_SYNTAX': {
                'message': (
                    "join: неверный синтаксис.\n"
                    "  Нужно две таблицы и параметр 'on'."
                ),
                'wrong': 'join(m1, m2)',
                'right': 'join(m1, m2, on "ID")',
                'explanation': (
                    "join принимает минимум ТРИ аргумента:\n"
                    "  1. m1 — левая таблица\n"
                    "  2. m2 — правая таблица\n"
                    "  3. on \"ID\" — ключ соединения\n"
                    "\n"
                    "Структура:\n"
                    "  join(m1, m2, on \"ID\")\n"
                    "  join(m1, m2, on \"ID\", how \"inner\")\n"
                    "  join(m1, m2, on [\"ID\", \"Дата\"])"
                ),
                'variants': [
                    'r = join(m1, m2, on "ID")',
                    'r = join(m1, m2, on "ID", how "inner")',
                ],
            },
            'JOIN_NEED_ON': {
                'message': (
                    "join: пропущено ключевое слово 'on'.\n"
                    "  Без него неясно, по какому столбцу соединять."
                ),
                'wrong': 'join(m1, m2, "ID")',
                'right': 'join(m1, m2, on "ID")',
                'explanation': (
                    "'on' — обязательный маркер начала ключей соединения.\n"
                    "\n"
                    "Структура:\n"
                    "  join(m1, m2, on \"ID\")\n"
                    "             ^^^\n"
                    "             тут 'on'"
                ),
                'variants': [
                    'r = join(m1, m2, on "ID")',
                    'r = join(m1, m2, on ["ID", "Дата"])',
                ],
            },
            'JOIN_NEED_TWO_TABLES': {
                'message': (
                    "join: нужно ДВЕ таблицы.\n"
                    "  Получена одна или больше."
                ),
                'wrong': 'join(m1, on "ID")',
                'right': 'join(m1, m2, on "ID")',
                'explanation': (
                    "join соединяет ДВЕ таблицы:\n"
                    "  join(m1, m2, on \"ID\")\n"
                    "       ^^  ^^"
                ),
                'variants': [
                    'r = join(m1, m2, on "ID")',
                    'r = join(s, c, on "Город")',
                ],
            },
            'JOIN_BAD_KEY': {
                'message': (
                    "join: ключ должен быть строкой в кавычках.\n"
                    "  Например: on \"ID\"."
                ),
                'wrong': 'join(m1, m2, on ID)',
                'right': 'join(m1, m2, on "ID")',
                'explanation': (
                    "Ключ — это ИМЯ СТОЛБЦА в кавычках:\n"
                    "     on \"ID\"\n"
                    "     on \"Город\"\n"
                    "\n"
                    "Несколько ключей:\n"
                    "     on [\"ID\", \"Дата\"]"
                ),
                'variants': [
                    'r = join(m1, m2, on "ID")',
                    'r = join(m1, m2, on "Город")',
                    'r = join(m1, m2, on ["ID", "Дата"])',
                ],
            },
            'JOIN_KEY_NOT_FOUND': {
                'message': (
                    "join: столбец-ключ не найден в таблице.\n"
                    "  Проверьте имя."
                ),
                'wrong': 'join(m1, m2, on "ID")',
                'right': 'join(m1, m2, on "ID")',
                'explanation': (
                    "Столбец-ключ должен существовать в ОБЕИХ таблицах\n"
                    "(или быть указан через == для разных имён).\n"
                    "\n"
                    "Проверьте:\n"
                    "  • есть ли столбец \"ID\" в m1\n"
                    "  • есть ли столбец \"ID\" в m2\n"
                    "\n"
                    "Если имена разные:\n"
                    "  join(m1, m2, on \"ID\" == \"Код\")"
                ),
                'variants': [
                    'r = join(m1, m2, on "ID")',
                    'r = join(m1, m2, on "ID" == "Код")',
                ],
            },
            'JOIN_DIFFERENT_KEYS': {
                'message': (
                    "join: разные имена ключей указываются через '=='.\n"
                    "  Пример: on \"ID\" == \"Код\"."
                ),
                'wrong': 'join(m1, m2, on "ID", "Код")',
                'right': 'join(m1, m2, on "ID" == "Код")',
                'explanation': (
                    "Если столбцы называются по-разному, используйте '==':\n"
                    "     on \"ID\" == \"Код\"\n"
                    "     on \"Город\" == \"City\"\n"
                    "\n"
                    "Если одинаково — просто:\n"
                    "     on \"ID\""
                ),
                'variants': [
                    'r = join(m1, m2, on "ID" == "Код")',
                    'r = join(m1, m2, on "Город" == "City")',
                ],
            },
            'JOIN_BAD_HOW': {
                'message': (
                    "join: how должен быть: left, inner, right или outer."
                ),
                'wrong': 'join(m1, m2, on "ID", how "outer_right")',
                'right': 'join(m1, m2, on "ID", how "outer")',
                'explanation': (
                    "Допустимо четыре режима:\n"
                    "     \"left\"  — все строки левой + совпадения (по умолчанию)\n"
                    "     \"inner\" — только совпадения\n"
                    "     \"right\" — все строки правой\n"
                    "     \"outer\" — все строки обеих\n"
                    "\n"
                    "НЕ:\n"
                    "     \"outer_right\"  ❌\n"
                    "     \"full\"         ❌ → \"outer\"  ✅\n"
                    "     \"cross\"        ❌"
                ),
                'variants': [
                    'r = join(m1, m2, on "ID", how "left")',
                    'r = join(m1, m2, on "ID", how "inner")',
                    'r = join(m1, m2, on "ID", how "right")',
                    'r = join(m1, m2, on "ID", how "outer")',
                ],
            },
            'JOIN_BAD_SUFFIXES': {
                'message': (
                    "join: suffixes требует список из ДВУХ строк.\n"
                    "  Пример: suffixes [\"_1\", \"_2\"]."
                ),
                'wrong': 'join(m1, m2, on "ID", suffixes "_left")',
                'right': 'join(m1, m2, on "ID", suffixes ["_1", "_2"])',
                'explanation': (
                    "suffixes принимает МАССИВ из ДВУХ строк:\n"
                    "     suffixes [\"_1\", \"_2\"]\n"
                    "     suffixes [\"_left\", \"_right\"]\n"
                    "\n"
                    "Они используются, если в обеих таблицах\n"
                    "есть одинаково названные НЕключевые столбцы."
                ),
                'variants': [
                    'r = join(m1, m2, on "ID", suffixes ["_1", "_2"])',
                    'r = join(m1, m2, on "ID", suffixes ["_left", "_right"])',
                ],
            },
            'JOIN_MIXED_TYPES': {
                'message': (
                    "join: обе таблицы должны быть одного типа.\n"
                    "  Matrix + Matrix или DuckDB + DuckDB."
                ),
                'wrong': 'join(m1, bd2, on "ID")',
                'right': 'join(m1, m2, on "ID")',
                'explanation': (
                    "Нельзя смешивать Matrix и DuckDB в одном join.\n"
                    "\n"
                    "Решение 1. Конвертировать одну из таблиц:\n"
                    "     bd2 = ToBigData(m2)\n"
                    "     r = join(bd1, bd2, on \"ID\")\n"
                    "\n"
                    "Решение 2. Конвертировать в Matrix:\n"
                    "     m2 = ToMatrix(bd2)\n"
                    "     r = join(m1, m2, on \"ID\")"
                ),
                'variants': [
                    'bd2 = ToBigData(m2)\nr = join(bd1, bd2, on "ID")',
                    'm2 = ToMatrix(bd2)\nr = join(m1, m2, on "ID")',
                ],
            },
            'JOIN_DUCKDB_HINT': {
                'message': (
                    "join: для BigData используйте DuckDB-таблицы.\n"
                    "  Matrix + DuckDB не поддерживается."
                ),
                'wrong': 'join(m1, bd2, on "ID")',
                'right': 'bd1 = ToBigData(m1)\nr = join(bd1, bd2, on "ID")',
                'explanation': (
                    "join работает либо с двумя Matrix,\n"
                    "либо с двумя DuckDB.\n"
                    "\n"
                    "Для больших таблиц:\n"
                    "     bd1 = OpenParquet(\"a.parquet\")\n"
                    "     bd2 = OpenParquet(\"b.parquet\")\n"
                    "     r = join(bd1, bd2, on \"ID\")"
                ),
                'variants': [
                    'bd1 = ToBigData(m1)\nr = join(bd1, bd2, on "ID")',
                ],
            },
            'JOIN_REQUIRES_ASSIGNMENT': {
                'message': (
                    "join() возвращает значение — сохраните результат."
                ),
                'wrong': 'join(m1, m2, on "ID")',
                'right': 'r = join(m1, m2, on "ID")',
                'explanation': (
                    "join НЕ изменяет исходные таблицы.\n"
                    "Он ВОЗВРАЩАЕТ НОВУЮ.\n"
                    "\n"
                    "Правильно:\n"
                    "  r = join(...)      — в новую переменную\n"
                    "  m1 = join(...)     — перезаписать левую\n"
                    "  print(join(...))   — вывод"
                ),
                'variants': [
                    'r = join(m1, m2, on "ID")',
                    'm1 = join(m1, m2, on "ID")',
                    'print(join(m1, m2, on "ID"))',
                ],
            },
        },
    },
}


EN = {
    'join': {
        'name': 'join',
        'category': 'join',
        'signature': 'join(m1, m2, on "ID" [, how "left"] [, suffixes [...]])',
        'description': (
            'Join two tables by a key.\n'
            '  • on — required parameter.\n'
            '  • how — left (default), inner, right, outer.\n'
            '  • suffixes — suffixes for conflicting names.\n'
            '  • Works with Matrix and DuckDB.\n'
            '  • Returns a NEW matrix.'
        ),
        'examples': [
            'r = join(m1, m2, on "ID")',
            'r = join(m1, m2, on "ID", how "inner")',
            'r = join(m1, m2, on ["ID", "Date"])',
            'r = join(m1, m2, on "ID" == "Code")',
            'r = join(m1, m2, on "ID", suffixes ["_1", "_2"])',
        ],
        'errors': {
            'JOIN_BAD_SYNTAX': {
                'message': (
                    "join: invalid syntax.\n"
                    "  Need two tables and the 'on' parameter."
                ),
                'wrong': 'join(m1, m2)',
                'right': 'join(m1, m2, on "ID")',
                'explanation': (
                    "join takes at least THREE arguments:\n"
                    "  1. m1 — left table\n"
                    "  2. m2 — right table\n"
                    "  3. on \"ID\" — join key\n"
                    "\n"
                    "Structure:\n"
                    "  join(m1, m2, on \"ID\")\n"
                    "  join(m1, m2, on \"ID\", how \"inner\")\n"
                    "  join(m1, m2, on [\"ID\", \"Date\"])"
                ),
                'variants': [
                    'r = join(m1, m2, on "ID")',
                    'r = join(m1, m2, on "ID", how "inner")',
                ],
            },
            'JOIN_NEED_ON': {
                'message': (
                    "join: keyword 'on' is missing.\n"
                    "  Without it, it's unclear which column to join by."
                ),
                'wrong': 'join(m1, m2, "ID")',
                'right': 'join(m1, m2, on "ID")',
                'explanation': (
                    "'on' is a required marker for the join keys block.\n"
                    "\n"
                    "Structure:\n"
                    "  join(m1, m2, on \"ID\")\n"
                    "             ^^^\n"
                    "             here 'on'"
                ),
                'variants': [
                    'r = join(m1, m2, on "ID")',
                    'r = join(m1, m2, on ["ID", "Date"])',
                ],
            },
            'JOIN_NEED_TWO_TABLES': {
                'message': (
                    "join: need TWO tables.\n"
                    "  Got one or more."
                ),
                'wrong': 'join(m1, on "ID")',
                'right': 'join(m1, m2, on "ID")',
                'explanation': (
                    "join joins TWO tables:\n"
                    "  join(m1, m2, on \"ID\")\n"
                    "       ^^  ^^"
                ),
                'variants': [
                    'r = join(m1, m2, on "ID")',
                    'r = join(s, c, on "City")',
                ],
            },
            'JOIN_BAD_KEY': {
                'message': (
                    "join: key must be a quoted string.\n"
                    "  Example: on \"ID\"."
                ),
                'wrong': 'join(m1, m2, on ID)',
                'right': 'join(m1, m2, on "ID")',
                'explanation': (
                    "A key is a COLUMN NAME in quotes:\n"
                    "     on \"ID\"\n"
                    "     on \"City\"\n"
                    "\n"
                    "Multiple keys:\n"
                    "     on [\"ID\", \"Date\"]"
                ),
                'variants': [
                    'r = join(m1, m2, on "ID")',
                    'r = join(m1, m2, on "City")',
                    'r = join(m1, m2, on ["ID", "Date"])',
                ],
            },
            'JOIN_KEY_NOT_FOUND': {
                'message': (
                    "join: key column not found in the table.\n"
                    "  Check the name."
                ),
                'wrong': 'join(m1, m2, on "ID")',
                'right': 'join(m1, m2, on "ID")',
                'explanation': (
                    "The key column must exist in BOTH tables\n"
                    "(or be specified via == for different names).\n"
                    "\n"
                    "Check:\n"
                    "  • does m1 have column \"ID\"\n"
                    "  • does m2 have column \"ID\"\n"
                    "\n"
                    "If names differ:\n"
                    "  join(m1, m2, on \"ID\" == \"Code\")"
                ),
                'variants': [
                    'r = join(m1, m2, on "ID")',
                    'r = join(m1, m2, on "ID" == "Code")',
                ],
            },
            'JOIN_DIFFERENT_KEYS': {
                'message': (
                    "join: different key names are specified via '=='.\n"
                    "  Example: on \"ID\" == \"Code\"."
                ),
                'wrong': 'join(m1, m2, on "ID", "Code")',
                'right': 'join(m1, m2, on "ID" == "Code")',
                'explanation': (
                    "If the columns have different names, use '==':\n"
                    "     on \"ID\" == \"Code\"\n"
                    "     on \"City\" == \"Town\"\n"
                    "\n"
                    "If they have the same name — just:\n"
                    "     on \"ID\""
                ),
                'variants': [
                    'r = join(m1, m2, on "ID" == "Code")',
                    'r = join(m1, m2, on "City" == "Town")',
                ],
            },
            'JOIN_BAD_HOW': {
                'message': (
                    "join: how must be: left, inner, right, or outer."
                ),
                'wrong': 'join(m1, m2, on "ID", how "outer_right")',
                'right': 'join(m1, m2, on "ID", how "outer")',
                'explanation': (
                    "Only four modes are allowed:\n"
                    "     \"left\"  — all rows of left + matches (default)\n"
                    "     \"inner\" — only matches\n"
                    "     \"right\" — all rows of right\n"
                    "     \"outer\" — all rows of both\n"
                    "\n"
                    "NOT:\n"
                    "     \"outer_right\"  ❌\n"
                    "     \"full\"         ❌ → \"outer\"  ✅\n"
                    "     \"cross\"        ❌"
                ),
                'variants': [
                    'r = join(m1, m2, on "ID", how "left")',
                    'r = join(m1, m2, on "ID", how "inner")',
                    'r = join(m1, m2, on "ID", how "right")',
                    'r = join(m1, m2, on "ID", how "outer")',
                ],
            },
            'JOIN_BAD_SUFFIXES': {
                'message': (
                    "join: suffixes requires an array of TWO strings.\n"
                    "  Example: suffixes [\"_1\", \"_2\"]."
                ),
                'wrong': 'join(m1, m2, on "ID", suffixes "_left")',
                'right': 'join(m1, m2, on "ID", suffixes ["_1", "_2"])',
                'explanation': (
                    "suffixes takes an ARRAY of TWO strings:\n"
                    "     suffixes [\"_1\", \"_2\"]\n"
                    "     suffixes [\"_left\", \"_right\"]\n"
                    "\n"
                    "They are used if both tables have\n"
                    "identically named NON-key columns."
                ),
                'variants': [
                    'r = join(m1, m2, on "ID", suffixes ["_1", "_2"])',
                    'r = join(m1, m2, on "ID", suffixes ["_left", "_right"])',
                ],
            },
            'JOIN_MIXED_TYPES': {
                'message': (
                    "join: both tables must be the same type.\n"
                    "  Matrix + Matrix or DuckDB + DuckDB."
                ),
                'wrong': 'join(m1, bd2, on "ID")',
                'right': 'join(m1, m2, on "ID")',
                'explanation': (
                    "Cannot mix Matrix and DuckDB in one join.\n"
                    "\n"
                    "Solution 1. Convert one of the tables:\n"
                    "     bd2 = ToBigData(m2)\n"
                    "     r = join(bd1, bd2, on \"ID\")\n"
                    "\n"
                    "Solution 2. Convert to Matrix:\n"
                    "     m2 = ToMatrix(bd2)\n"
                    "     r = join(m1, m2, on \"ID\")"
                ),
                'variants': [
                    'bd2 = ToBigData(m2)\nr = join(bd1, bd2, on "ID")',
                    'm2 = ToMatrix(bd2)\nr = join(m1, m2, on "ID")',
                ],
            },
            'JOIN_DUCKDB_HINT': {
                'message': (
                    "join: for BigData use DuckDB tables.\n"
                    "  Matrix + DuckDB is not supported."
                ),
                'wrong': 'join(m1, bd2, on "ID")',
                'right': 'bd1 = ToBigData(m1)\nr = join(bd1, bd2, on "ID")',
                'explanation': (
                    "join works either with two Matrix or two DuckDB.\n"
                    "\n"
                    "For large tables:\n"
                    "     bd1 = OpenParquet(\"a.parquet\")\n"
                    "     bd2 = OpenParquet(\"b.parquet\")\n"
                    "     r = join(bd1, bd2, on \"ID\")"
                ),
                'variants': [
                    'bd1 = ToBigData(m1)\nr = join(bd1, bd2, on "ID")',
                ],
            },
            'JOIN_REQUIRES_ASSIGNMENT': {
                'message': (
                    "join() returns a value — save the result."
                ),
                'wrong': 'join(m1, m2, on "ID")',
                'right': 'r = join(m1, m2, on "ID")',
                'explanation': (
                    "join does NOT modify the source tables.\n"
                    "It RETURNS a NEW one.\n"
                    "\n"
                    "Correct:\n"
                    "  r = join(...)      — to a new variable\n"
                    "  m1 = join(...)     — overwrite the left one\n"
                    "  print(join(...))   — output"
                ),
                'variants': [
                    'r = join(m1, m2, on "ID")',
                    'm1 = join(m1, m2, on "ID")',
                    'print(join(m1, m2, on "ID"))',
                ],
            },
        },
    },
}