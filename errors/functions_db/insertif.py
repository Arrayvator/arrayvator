# errors/functions_db/insertif.py
"""
База ошибок для функции INSERTIF — условная вставка строк.

СИНТАКСИС:
    insertif(условие, before)
    insertif(условие, after)

ЛОГИКА:
    Вставляет ПУСТУЮ строку (все None)
    после/перед каждой строкой, где условие истинно.

⚠️  Работает ТОЛЬКО с Matrix (RAM).
    НЕ работает с BigData (DuckDB).
"""


RU = {
    'insertif': {
        'name': 'insertif',
        'category': 'case',
        'signature': 'insertif(условие, before | after)',
        'description': (
            'Условная вставка пустых строк.\n'
            '  • Вставляет пустую строку после/перед каждым совпадением.\n'
            '  • Обработка снизу вверх.\n'
            '  • Заголовок НЕ участвует в условии.\n'
            '  • Возвращает НОВУЮ матрицу.\n'
            '  ⚠️  Работает только с Matrix (RAM), не с BigData (DuckDB).'
        ),
        'examples': [
            'r = insertif(m[:, "Отдел"] == "IT", after)',
            'r = insertif(m[:, "Возраст"] > 25, before)',
            'm = insertif(m[:, "Отдел"] == "IT", after)',
            'r = insertif(m[2:10, "Отдел"] == "IT", after)',
        ],
        'errors': {
            'INSERTIF_BAD_SYNTAX': {
                'message': (
                    "insertif: неверный синтаксис.\n"
                    "  Нужно условие и направление (before или after)."
                ),
                'wrong': 'r = insertif(m[:, "Отдел"] == "IT")',
                'right': 'r = insertif(m[:, "Отдел"] == "IT", after)',
                'explanation': (
                    "insertif принимает ДВА аргумента:\n"
                    "  1. условие\n"
                    "  2. before или after\n"
                    "\n"
                    "Структура:\n"
                    "  insertif(условие, before|after)"
                ),
                'variants': [
                    'r = insertif(m[:, "Отдел"] == "IT", after)',
                    'r = insertif(m[:, "Возраст"] > 25, before)',
                    'r = insertif(m[2:10, "Отдел"] == "IT", after)',
                ],
            },
            'INSERTIF_MISSING_DIRECTION': {
                'message': (
                    "insertif: нужно указать направление — before или after."
                ),
                'wrong': 'r = insertif(m[:, "Отдел"] == "IT", "after")',
                'right': 'r = insertif(m[:, "Отдел"] == "IT", after)',
                'explanation': (
                    "'before' и 'after' — ключевые слова БЕЗ кавычек.\n"
                    "\n"
                    "Неправильно: insertif(..., \"after\")\n"
                    "Правильно: insertif(..., after)\n"
                    "Правильно: insertif(..., before)"
                ),
                'variants': [
                    'r = insertif(m[:, "Отдел"] == "IT", after)',
                    'r = insertif(m[:, "Возраст"] > 25, before)',
                ],
            },
            'INSERTIF_DUCKDB': {
                'message': (
                    "insertif работает только с Matrix (RAM), "
                    "не с BigData (DuckDB).\n"
                    "  BigData — read-only view на файл."
                ),
                'wrong': 'r = insertif(bd[:, "Отдел"] == "IT", after)',
                'right': (
                    'm = ToMatrix(bd)\n'
                    'r = insertif(m[:, "Отдел"] == "IT", after)'
                ),
                'explanation': (
                    "BigData (DuckDB) — read-only view на файл.\n"
                    "Он НЕ поддерживает вставку строк.\n"
                    "\n"
                    "Решение:\n"
                    "  1. Конвертировать BigData в Matrix:\n"
                    "        m = ToMatrix(bd)\n"
                    "        r = insertif(m[:, \"Отдел\"] == \"IT\", after)\n"
                    "\n"
                    "  2. Использовать SQL-аналог:\n"
                    "        filterif, addrows"
                ),
                'variants': [
                    'm = ToMatrix(bd)\nr = insertif(m[:, "Отдел"] == "IT", after)',
                    'm = ToMatrix(bd)\nr = insertif(m[:, "Возраст"] > 25, before)',
                    'm = ToMatrix(bd)\nm = insertif(m[:, "Отдел"] == "IT", after)',
                ],
            },
            'INSERTIF_REQUIRES_ASSIGNMENT': {
                'message': (
                    "insertif() возвращает значение — "
                    "результат нужно сохранить."
                ),
                'wrong': 'insertif(m[:, "Отдел"] == "IT", after)',
                'right': 'r = insertif(m[:, "Отдел"] == "IT", after)',
                'explanation': (
                    "insertif НЕ изменяет исходную матрицу.\n"
                    "Он ВОЗВРАЩАЕТ НОВУЮ.\n"
                    "\n"
                    "Правильно:\n"
                    "  r = insertif(...)    — в новую переменную\n"
                    "  m = insertif(...)    — мутация"
                ),
                'variants': [
                    'r = insertif(m[:, "Отдел"] == "IT", after)',
                    'm = insertif(m[:, "Отдел"] == "IT", after)',
                ],
            },
        },
    },
}


EN = {
    'insertif': {
        'name': 'insertif',
        'category': 'case',
        'signature': 'insertif(condition, before | after)',
        'description': (
            'Conditional insertion of empty rows.\n'
            '  • Inserts an empty row after/before each match.\n'
            '  • Processed bottom-up.\n'
            '  • Header is NOT involved in the condition.\n'
            '  • Returns a NEW matrix.\n'
            '  ⚠️  Works only with Matrix (RAM), not with BigData (DuckDB).'
        ),
        'examples': [
            'r = insertif(m[:, "Dept"] == "IT", after)',
            'r = insertif(m[:, "Age"] > 25, before)',
            'm = insertif(m[:, "Dept"] == "IT", after)',
            'r = insertif(m[2:10, "Dept"] == "IT", after)',
        ],
        'errors': {
            'INSERTIF_BAD_SYNTAX': {
                'message': (
                    "insertif: invalid syntax.\n"
                    "  Need a condition and a direction (before or after)."
                ),
                'wrong': 'r = insertif(m[:, "Dept"] == "IT")',
                'right': 'r = insertif(m[:, "Dept"] == "IT", after)',
                'explanation': (
                    "insertif takes TWO arguments:\n"
                    "  1. condition\n"
                    "  2. before or after\n"
                    "\n"
                    "Structure:\n"
                    "  insertif(condition, before|after)"
                ),
                'variants': [
                    'r = insertif(m[:, "Dept"] == "IT", after)',
                    'r = insertif(m[:, "Age"] > 25, before)',
                    'r = insertif(m[2:10, "Dept"] == "IT", after)',
                ],
            },
            'INSERTIF_MISSING_DIRECTION': {
                'message': (
                    "insertif: direction is required — before or after."
                ),
                'wrong': 'r = insertif(m[:, "Dept"] == "IT", "after")',
                'right': 'r = insertif(m[:, "Dept"] == "IT", after)',
                'explanation': (
                    "'before' and 'after' are KEYWORDS WITHOUT quotes.\n"
                    "\n"
                    "Неправильно: insertif(..., \"after\")\n"
                    "Правильно: insertif(..., after)\n"
                    "Правильно: insertif(..., before)"
                ),
                'variants': [
                    'r = insertif(m[:, "Dept"] == "IT", after)',
                    'r = insertif(m[:, "Age"] > 25, before)',
                ],
            },
            'INSERTIF_DUCKDB': {
                'message': (
                    "insertif works only with Matrix (RAM), "
                    "not with BigData (DuckDB).\n"
                    "  BigData is a read-only view on a file."
                ),
                'wrong': 'r = insertif(bd[:, "Dept"] == "IT", after)',
                'right': (
                    'm = ToMatrix(bd)\n'
                    'r = insertif(m[:, "Dept"] == "IT", after)'
                ),
                'explanation': (
                    "BigData (DuckDB) is a read-only view on a file.\n"
                    "It does NOT support inserting rows.\n"
                    "\n"
                    "Solution:\n"
                    "  1. Convert BigData to Matrix:\n"
                    "        m = ToMatrix(bd)\n"
                    "        r = insertif(m[:, \"Dept\"] == \"IT\", after)\n"
                    "\n"
                    "  2. Use SQL analog:\n"
                    "        filterif, addrows"
                ),
                'variants': [
                    'm = ToMatrix(bd)\nr = insertif(m[:, "Dept"] == "IT", after)',
                    'm = ToMatrix(bd)\nr = insertif(m[:, "Age"] > 25, before)',
                    'm = ToMatrix(bd)\nm = insertif(m[:, "Dept"] == "IT", after)',
                ],
            },
            'INSERTIF_REQUIRES_ASSIGNMENT': {
                'message': (
                    "insertif() returns a value — "
                    "the result must be saved."
                ),
                'wrong': 'insertif(m[:, "Dept"] == "IT", after)',
                'right': 'r = insertif(m[:, "Dept"] == "IT", after)',
                'explanation': (
                    "insertif does NOT modify the source matrix.\n"
                    "It RETURNS a NEW one.\n"
                    "\n"
                    "Correct:\n"
                    "  r = insertif(...)    — to a new variable\n"
                    "  m = insertif(...)    — mutation"
                ),
                'variants': [
                    'r = insertif(m[:, "Dept"] == "IT", after)',
                    'm = insertif(m[:, "Dept"] == "IT", after)',
                ],
            },
        },
    },
}