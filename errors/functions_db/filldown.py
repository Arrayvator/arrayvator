# errors/functions_db/filldown.py
"""
База ошибок для функции FILLDOWN — заполнение пустых значений вниз.

СИНТАКСИС:
    filldown(m[:, "Клиент"])
    filldown(m[:, "Клиент"], "-")

⚠️  Работает ТОЛЬКО с Matrix (RAM).
    НЕ работает с BigData (DuckDB).
"""


RU = {
    'filldown': {
        'name': 'filldown',
        'category': 'modify',
        'signature': 'filldown(m[:, "X"] [, маркер])',
        'description': (
            'Заполняет None/пустые значения вниз предыдущим непустым.\n'
            '  • Идёт по столбцу сверху вниз.\n'
            '  • Если значение пустое — берёт предыдущее непустое.\n'
            '  • Первая строка, если пустая — остаётся пустой.\n'
            '  • Возвращает НОВУЮ матрицу — результат нужно сохранить.\n'
            '  ⚠️  Работает только с Matrix (RAM), не с BigData (DuckDB).'
        ),
        'examples': [
            'r = filldown(m[:, "Клиент"])',
            'r = filldown(m[:, "Клиент"], "-")',
            'm = filldown(m[:, "Клиент"])',
        ],
        'errors': {
            'FILLDOWN_BAD_SYNTAX': {
                'message': (
                    "filldown: неверный синтаксис.\n"
                    "  Нужен срез столбца m[:, \"X\"]."
                ),
                'wrong': 'filldown(m)',
                'right': 'filldown(m[:, "Клиент"])',
                'explanation': (
                    "filldown принимает срез столбца:\n"
                    "     filldown(m[:, \"X\"])\n"
                    "     filldown(m[:, \"X\"], маркер)\n"
                    "\n"
                    "Неправильно:\n"
                    "     filldown(m)\n"
                    "     filldown(m, \"X\")\n"
                    "\n"
                    "Правильно:\n"
                    "     filldown(m[:, \"Клиент\"])"
                ),
                'variants': [
                    'r = filldown(m[:, "Клиент"])',
                    'r = filldown(m[:, "Клиент"], "-")',
                ],
            },
            'FILLDOWN_NOT_SLICE': {
                'message': (
                    "filldown: нужен срез столбца m[:, \"X\"]."
                ),
                'wrong': 'filldown(42)',
                'right': 'filldown(m[:, "Клиент"])',
                'explanation': (
                    "filldown работает со срезом одного столбца:\n"
                    "     m[:, \"Имя\"]     — по имени\n"
                    "     m[:, 3]         — по номеру\n"
                    "     m[:, end]       — последний\n"
                    "\n"
                    "Неправильно:\n"
                    "     filldown(42)\n"
                    "     filldown(m)\n"
                    "\n"
                    "Правильно:\n"
                    "     filldown(m[:, \"Клиент\"])"
                ),
                'variants': [
                    'r = filldown(m[:, "Клиент"])',
                    'r = filldown(m[:, 3])',
                ],
            },
            'FILLDOWN_DUCKDB': {
                'message': (
                    "filldown работает только с Matrix (RAM), "
                    "не с BigData (DuckDB).\n"
                    "  BigData — read-only view на файл."
                ),
                'wrong': 'r = filldown(bd[:, "Клиент"])',
                'right': (
                    'm = ToMatrix(bd)\n'
                    'r = filldown(m[:, "Клиент"])'
                ),
                'explanation': (
                    "BigData (DuckDB) — read-only view на файл.\n"
                    "Он НЕ поддерживает заполнение вниз.\n"
                    "\n"
                    "Решение:\n"
                    "  1. Конвертировать BigData в Matrix:\n"
                    "        m = ToMatrix(bd)\n"
                    "        r = filldown(m[:, \"Клиент\"])\n"
                    "\n"
                    "  2. Использовать SQL-аналог (оконные функции):\n"
                    "        winsum, winmax"
                ),
                'variants': [
                    'm = ToMatrix(bd)\nr = filldown(m[:, "Клиент"])',
                    'm = ToMatrix(bd)\nm = filldown(m[:, "Клиент"], "-")',
                ],
            },
            'FILLDOWN_REQUIRES_ASSIGNMENT': {
                'message': (
                    "filldown() возвращает значение — "
                    "результат нужно сохранить."
                ),
                'wrong': 'filldown(m[:, "Клиент"])',
                'right': 'r = filldown(m[:, "Клиент"])',
                'explanation': (
                    "filldown НЕ изменяет исходную матрицу.\n"
                    "Он ВОЗВРАЩАЕТ НОВУЮ.\n"
                    "\n"
                    "Правильно:\n"
                    "  r = filldown(...)      — в новую переменную\n"
                    "  m = filldown(...)      — мутация"
                ),
                'variants': [
                    'r = filldown(m[:, "Клиент"])',
                    'm = filldown(m[:, "Клиент"])',
                ],
            },
        },
    },
}


EN = {
    'filldown': {
        'name': 'filldown',
        'category': 'modify',
        'signature': 'filldown(m[:, "X"] [, marker])',
        'description': (
            'Fill None/empty values downward with previous non-empty.\n'
            '  • Walks the column top-down.\n'
            '  • If empty — takes the previous non-empty.\n'
            '  • First row, if empty — stays empty.\n'
            '  • Returns a NEW matrix — save the result.\n'
            '  ⚠️  Works only with Matrix (RAM), not with BigData (DuckDB).'
        ),
        'examples': [
            'r = filldown(m[:, "Client"])',
            'r = filldown(m[:, "Client"], "-")',
            'm = filldown(m[:, "Client"])',
        ],
        'errors': {
            'FILLDOWN_BAD_SYNTAX': {
                'message': (
                    "filldown: invalid syntax.\n"
                    "  Need a column slice m[:, \"X\"]."
                ),
                'wrong': 'filldown(m)',
                'right': 'filldown(m[:, "Client"])',
                'explanation': (
                    "filldown takes a column slice:\n"
                    "     filldown(m[:, \"X\"])\n"
                    "     filldown(m[:, \"X\"], marker)\n"
                    "\n"
                    "Incorrect:\n"
                    "     filldown(m)\n"
                    "     filldown(m, \"X\")\n"
                    "\n"
                    "Correct:\n"
                    "     filldown(m[:, \"Client\"])"
                ),
                'variants': [
                    'r = filldown(m[:, "Client"])',
                    'r = filldown(m[:, "Client"], "-")',
                ],
            },
            'FILLDOWN_NOT_SLICE': {
                'message': (
                    "filldown: need a column slice m[:, \"X\"]."
                ),
                'wrong': 'filldown(42)',
                'right': 'filldown(m[:, "Client"])',
                'explanation': (
                    "filldown works with a single column slice:\n"
                    "     m[:, \"Name\"]    — by name\n"
                    "     m[:, 3]         — by number\n"
                    "     m[:, end]       — last\n"
                    "\n"
                    "Incorrect:\n"
                    "     filldown(42)\n"
                    "     filldown(m)\n"
                    "\n"
                    "Correct:\n"
                    "     filldown(m[:, \"Client\"])"
                ),
                'variants': [
                    'r = filldown(m[:, "Client"])',
                    'r = filldown(m[:, 3])',
                ],
            },
            'FILLDOWN_DUCKDB': {
                'message': (
                    "filldown works only with Matrix (RAM), "
                    "not with BigData (DuckDB).\n"
                    "  BigData is a read-only view on a file."
                ),
                'wrong': 'r = filldown(bd[:, "Client"])',
                'right': (
                    'm = ToMatrix(bd)\n'
                    'r = filldown(m[:, "Client"])'
                ),
                'explanation': (
                    "BigData (DuckDB) is a read-only view on a file.\n"
                    "It does NOT support filling down.\n"
                    "\n"
                    "Solution:\n"
                    "  1. Convert BigData to Matrix:\n"
                    "        m = ToMatrix(bd)\n"
                    "        r = filldown(m[:, \"Client\"])\n"
                    "\n"
                    "  2. Use SQL analog (window functions):\n"
                    "        winsum, winmax"
                ),
                'variants': [
                    'm = ToMatrix(bd)\nr = filldown(m[:, "Client"])',
                    'm = ToMatrix(bd)\nm = filldown(m[:, "Client"], "-")',
                ],
            },
            'FILLDOWN_REQUIRES_ASSIGNMENT': {
                'message': (
                    "filldown() returns a value — "
                    "the result must be saved."
                ),
                'wrong': 'filldown(m[:, "Client"])',
                'right': 'r = filldown(m[:, "Client"])',
                'explanation': (
                    "filldown does NOT modify the source matrix.\n"
                    "It RETURNS a NEW one.\n"
                    "\n"
                    "Correct:\n"
                    "  r = filldown(...)      — to a new variable\n"
                    "  m = filldown(...)      — mutation"
                ),
                'variants': [
                    'r = filldown(m[:, "Client"])',
                    'm = filldown(m[:, "Client"])',
                ],
            },
        },
    },
}