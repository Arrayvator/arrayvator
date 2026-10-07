# errors/functions_db/insert.py
"""
База ошибок для функции INSERT — вставка пустой строки/столбца.

СИНТАКСИС:
    insert(s[2, :], before)         # пустая строка перед строкой 2
    insert(s[2, :], after)          # пустая строка после строки 2
    insert(s[:, 3], before)         # пустой столбец перед столбцом 3
    insert(s[:, "Имя"], before)     # пустой столбец перед столбцом "Имя"
    insert(s[:, end], after)        # пустой столбец после последнего
    insert(v, 3, after)             # пустой элемент после позиции 3 (вектор)

⚠️  Работает ТОЛЬКО с Matrix (RAM).
    НЕ работает с BigData (DuckDB).
"""


RU = {
    'insert': {
        'name': 'insert',
        'category': 'modify',
        'signature': 'insert(индекс, before | after)',
        'description': (
            'Вставляет ПУСТУЮ строку или столбец.\n'
            '  • insert(m[2, :], before)       — строка перед 2\n'
            '  • insert(m[:, 3], after)        — столбец после 3\n'
            '  • insert(m[:, "Имя"], before)   — столбец по имени\n'
            '  • insert(v, 3, after)           — элемент вектора\n'
            '  • Направление: before | after.\n'
            '  • Возвращает НОВУЮ матрицу — результат нужно сохранить.\n'
            '  ⚠️  Работает только с Matrix (RAM), не с BigData (DuckDB).'
        ),
        'examples': [
            'r = insert(m[2, :], before)',
            'r = insert(m[:, 3], after)',
            'r = insert(v, 3, after)',
        ],
        'errors': {
            'INSERT_BAD_SYNTAX': {
                'message': (
                    "insert: неверный синтаксис.\n"
                    "  Нужен индекс и направление."
                ),
                'wrong': 'insert(m[2, :])',
                'right': 'insert(m[2, :], before)',
                'explanation': (
                    "insert принимает индекс и направление:\n"
                    "  insert(m[N, :], before | after)  — строка\n"
                    "  insert(m[:, N], before | after)  — столбец\n"
                    "  insert(v, N, before | after)     — вектор\n"
                    "\n"
                    "Неправильно:\n"
                    "     insert(m[2, :])\n"
                    "\n"
                    "Правильно:\n"
                    "     insert(m[2, :], before)\n"
                    "     insert(m[2, :], after)"
                ),
                'variants': [
                    'r = insert(m[2, :], before)',
                    'r = insert(m[:, 3], after)',
                    'r = insert(v, 3, after)',
                ],
            },
            'INSERT_MISSING_DIRECTION': {
                'message': (
                    "insert: не указано направление — before или after."
                ),
                'wrong': 'insert(m[2, :])',
                'right': 'insert(m[2, :], before)',
                'explanation': (
                    "insert принимает направление: before или after.\n"
                    "\n"
                    "Неправильно:\n"
                    "     insert(m[2, :])\n"
                    "\n"
                    "Правильно:\n"
                    "     insert(m[2, :], before)\n"
                    "     insert(m[2, :], after)\n"
                    "\n"
                    "Направление указывается БЕЗ кавычек:\n"
                    "     insert(m[2, :], before)\n"
                    "     insert(m[2, :], after)"
                ),
                'variants': [
                    'r = insert(m[2, :], before)',
                    'r = insert(m[2, :], after)',
                    'r = insert(m[:, 3], before)',
                ],
            },
            'INSERT_BAD_INDEX': {
                'message': (
                    "insert: неверный индекс.\n"
                    "  Нужен срез m[N, :], m[:, N] или вектор."
                ),
                'wrong': 'insert(42, before)',
                'right': 'insert(m[2, :], before)',
                'explanation': (
                    "Индекс — это срез матрицы или вектор:\n"
                    "     m[N, :]       — строка N\n"
                    "     m[:, N]       — столбец N\n"
                    "     m[:, \"Имя\"]   — столбец по имени\n"
                    "     m[:, end]     — последний столбец\n"
                    "     v             — вектор\n"
                    "\n"
                    "Неправильно:\n"
                    "     insert(42, before)\n"
                    "\n"
                    "Правильно:\n"
                    "     insert(m[2, :], before)\n"
                    "     insert(m[:, 3], after)"
                ),
                'variants': [
                    'r = insert(m[2, :], before)',
                    'r = insert(m[:, "Имя"], before)',
                    'r = insert(v, 3, after)',
                ],
            },
            'INSERT_BAD_DIRECTION': {
                'message': (
                    "insert: направление должно быть before или after."
                ),
                'wrong': 'insert(m[2, :], middle)',
                'right': 'insert(m[2, :], before)',
                'explanation': (
                    "Допустимо только два направления:\n"
                    "     before — ПЕРЕД целью\n"
                    "     after  — ПОСЛЕ цели\n"
                    "\n"
                    "Неправильно:\n"
                    "     insert(m[2, :], middle)\n"
                    "     insert(m[2, :], \"before\")   — кавычки\n"
                    "\n"
                    "Правильно:\n"
                    "     insert(m[2, :], before)\n"
                    "     insert(m[2, :], after)"
                ),
                'variants': [
                    'r = insert(m[2, :], before)',
                    'r = insert(m[2, :], after)',
                ],
            },
            'INSERT_DUCKDB': {
                'message': (
                    "insert работает только с Matrix (RAM), "
                    "не с BigData (DuckDB).\n"
                    "  BigData — read-only view на файл."
                ),
                'wrong': 'r = insert(bd[2, :], before)',
                'right': (
                    'm = ToMatrix(bd)\n'
                    'r = insert(m[2, :], before)'
                ),
                'explanation': (
                    "BigData (DuckDB) — read-only view на файл.\n"
                    "Он НЕ поддерживает вставку строк/столбцов.\n"
                    "\n"
                    "Решение:\n"
                    "  1. Конвертировать BigData в Matrix:\n"
                    "        m = ToMatrix(bd)\n"
                    "        r = insert(m[2, :], before)\n"
                    "\n"
                    "  2. Работать напрямую с Matrix."
                ),
                'variants': [
                    'm = ToMatrix(bd)\nr = insert(m[2, :], before)',
                    'm = ToMatrix(bd)\nr = insert(m[:, 3], after)',
                ],
            },
            'INSERT_REQUIRES_ASSIGNMENT': {
                'message': (
                    "insert() возвращает значение — "
                    "результат нужно сохранить."
                ),
                'wrong': 'insert(m[2, :], before)',
                'right': 'r = insert(m[2, :], before)',
                'explanation': (
                    "insert НЕ изменяет исходную матрицу.\n"
                    "Он ВОЗВРАЩАЕТ НОВУЮ.\n"
                    "\n"
                    "Правильно:\n"
                    "  r = insert(...)      — в новую переменную\n"
                    "  m = insert(...)      — мутация"
                ),
                'variants': [
                    'r = insert(m[2, :], before)',
                    'm = insert(m[2, :], before)',
                ],
            },
        },
    },
}


EN = {
    'insert': {
        'name': 'insert',
        'category': 'modify',
        'signature': 'insert(index, before | after)',
        'description': (
            'Insert an EMPTY row or column.\n'
            '  • insert(m[2, :], before)       — row before 2\n'
            '  • insert(m[:, 3], after)        — column after 3\n'
            '  • insert(m[:, "Name"], before)   — column by name\n'
            '  • insert(v, 3, after)           — vector element\n'
            '  • Direction: before | after.\n'
            '  • Returns a NEW matrix — save the result.\n'
            '  ⚠️  Works only with Matrix (RAM), not with BigData (DuckDB).'
        ),
        'examples': [
            'r = insert(m[2, :], before)',
            'r = insert(m[:, 3], after)',
            'r = insert(v, 3, after)',
        ],
        'errors': {
            'INSERT_BAD_SYNTAX': {
                'message': (
                    "insert: invalid syntax.\n"
                    "  Need an index and a direction."
                ),
                'wrong': 'insert(m[2, :])',
                'right': 'insert(m[2, :], before)',
                'explanation': (
                    "insert takes an index and a direction:\n"
                    "  insert(m[N, :], before | after)  — row\n"
                    "  insert(m[:, N], before | after)  — column\n"
                    "  insert(v, N, before | after)     — vector\n"
                    "\n"
                    "Incorrect:\n"
                    "     insert(m[2, :])\n"
                    "\n"
                    "Correct:\n"
                    "     insert(m[2, :], before)\n"
                    "     insert(m[2, :], after)"
                ),
                'variants': [
                    'r = insert(m[2, :], before)',
                    'r = insert(m[:, 3], after)',
                    'r = insert(v, 3, after)',
                ],
            },
            'INSERT_MISSING_DIRECTION': {
                'message': (
                    "insert: direction is missing — before or after."
                ),
                'wrong': 'insert(m[2, :])',
                'right': 'insert(m[2, :], before)',
                'explanation': (
                    "insert takes a direction: before or after.\n"
                    "\n"
                    "Incorrect:\n"
                    "     insert(m[2, :])\n"
                    "\n"
                    "Correct:\n"
                    "     insert(m[2, :], before)\n"
                    "     insert(m[2, :], after)\n"
                    "\n"
                    "Direction is given WITHOUT quotes:\n"
                    "     insert(m[2, :], before)\n"
                    "     insert(m[2, :], after)"
                ),
                'variants': [
                    'r = insert(m[2, :], before)',
                    'r = insert(m[2, :], after)',
                    'r = insert(m[:, 3], before)',
                ],
            },
            'INSERT_BAD_INDEX': {
                'message': (
                    "insert: invalid index.\n"
                    "  Need a slice m[N, :], m[:, N] or a vector."
                ),
                'wrong': 'insert(42, before)',
                'right': 'insert(m[2, :], before)',
                'explanation': (
                    "Index is a matrix slice or a vector:\n"
                    "     m[N, :]       — row N\n"
                    "     m[:, N]       — column N\n"
                    "     m[:, \"Name\"]  — column by name\n"
                    "     m[:, end]     — last column\n"
                    "     v             — vector\n"
                    "\n"
                    "Incorrect:\n"
                    "     insert(42, before)\n"
                    "\n"
                    "Correct:\n"
                    "     insert(m[2, :], before)\n"
                    "     insert(m[:, 3], after)"
                ),
                'variants': [
                    'r = insert(m[2, :], before)',
                    'r = insert(m[:, "Name"], before)',
                    'r = insert(v, 3, after)',
                ],
            },
            'INSERT_BAD_DIRECTION': {
                'message': (
                    "insert: direction must be before or after."
                ),
                'wrong': 'insert(m[2, :], middle)',
                'right': 'insert(m[2, :], before)',
                'explanation': (
                    "Only two directions are allowed:\n"
                    "     before — BEFORE the target\n"
                    "     after  — AFTER the target\n"
                    "\n"
                    "Incorrect:\n"
                    "     insert(m[2, :], middle)\n"
                    "     insert(m[2, :], \"before\")   — quotes\n"
                    "\n"
                    "Correct:\n"
                    "     insert(m[2, :], before)\n"
                    "     insert(m[2, :], after)"
                ),
                'variants': [
                    'r = insert(m[2, :], before)',
                    'r = insert(m[2, :], after)',
                ],
            },
            'INSERT_DUCKDB': {
                'message': (
                    "insert works only with Matrix (RAM), "
                    "not with BigData (DuckDB).\n"
                    "  BigData is a read-only view on a file."
                ),
                'wrong': 'r = insert(bd[2, :], before)',
                'right': (
                    'm = ToMatrix(bd)\n'
                    'r = insert(m[2, :], before)'
                ),
                'explanation': (
                    "BigData (DuckDB) is a read-only view on a file.\n"
                    "It does NOT support inserting rows/columns.\n"
                    "\n"
                    "Solution:\n"
                    "  1. Convert BigData to Matrix:\n"
                    "        m = ToMatrix(bd)\n"
                    "        r = insert(m[2, :], before)\n"
                    "\n"
                    "  2. Work directly with Matrix."
                ),
                'variants': [
                    'm = ToMatrix(bd)\nr = insert(m[2, :], before)',
                    'm = ToMatrix(bd)\nr = insert(m[:, 3], after)',
                ],
            },
            'INSERT_REQUIRES_ASSIGNMENT': {
                'message': (
                    "insert() returns a value — "
                    "the result must be saved."
                ),
                'wrong': 'insert(m[2, :], before)',
                'right': 'r = insert(m[2, :], before)',
                'explanation': (
                    "insert does NOT modify the source matrix.\n"
                    "It RETURNS a NEW one.\n"
                    "\n"
                    "Correct:\n"
                    "  r = insert(...)      — to a new variable\n"
                    "  m = insert(...)      — mutation"
                ),
                'variants': [
                    'r = insert(m[2, :], before)',
                    'm = insert(m[2, :], before)',
                ],
            },
        },
    },
}