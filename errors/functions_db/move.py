# errors/functions_db/move.py
"""
База ошибок для функции MOVE — перемещение строки/столбца внутри матрицы.

СИНТАКСИС:
    move(s[:, 1], s[:, 10], after)       # столбец
    move(s[:, 1:3], s[:, 10], after)     # диапазон столбцов
    move(s[:, end], s[:, 10], after)     # последний столбец
    move(s[2, :], s[10, :], before)      # строка
    move(s[1:10, :], s[end, :], after)   # диапазон строк

⚠️  Работает ТОЛЬКО с Matrix (RAM).
    НЕ работает с BigData (DuckDB).
"""


RU = {
    'move': {
        'name': 'move',
        'category': 'modify',
        'signature': 'move(источник, цель, before | after)',
        'description': (
            'Перемещает строку или столбец внутри матрицы.\n'
            '  • Источник и цель — срезы одной матрицы.\n'
            '  • Направление: before | after.\n'
            '  • Цель НЕ может быть внутри источника.\n'
            '  • Возвращает НОВУЮ матрицу — результат нужно сохранить.\n'
            '  ⚠️  Работает только с Matrix (RAM), не с BigData (DuckDB).'
        ),
        'examples': [
            'r = move(m[:, 1], m[:, 4], after)',
            'r = move(m[1:3, :], m[end, :], after)',
        ],
        'errors': {
            'MOVE_BAD_SYNTAX': {
                'message': (
                    "move: неверный синтаксис.\n"
                    "  Нужны источник, цель и направление."
                ),
                'wrong': 'move(m[:, 1], m[:, 4])',
                'right': 'move(m[:, 1], m[:, 4], after)',
                'explanation': (
                    "move принимает ТРИ аргумента:\n"
                    "  1. источник — срез m[:, ...] или m[N, :]\n"
                    "  2. цель — срез той же матрицы\n"
                    "  3. направление — before | after\n"
                    "\n"
                    "Неправильно:\n"
                    "     move(m[:, 1], m[:, 4])\n"
                    "\n"
                    "Правильно:\n"
                    "     move(m[:, 1], m[:, 4], after)\n"
                    "     move(m[:, 1], m[:, 4], before)"
                ),
                'variants': [
                    'r = move(m[:, 1], m[:, 4], after)',
                    'r = move(m[1:10, :], m[end, :], after)',
                ],
            },
            'MOVE_MISSING_DIRECTION': {
                'message': (
                    "move: не указано направление — before или after."
                ),
                'wrong': 'move(m[:, 1], m[:, 4])',
                'right': 'move(m[:, 1], m[:, 4], after)',
                'explanation': (
                    "move принимает ТРИ аргумента.\n"
                    "Третий — направление: before или after.\n"
                    "\n"
                    "Неправильно:\n"
                    "     move(m[:, 1], m[:, 4])\n"
                    "\n"
                    "Правильно:\n"
                    "     move(m[:, 1], m[:, 4], after)\n"
                    "     move(m[:, 1], m[:, 4], before)\n"
                    "\n"
                    "Направление указывается БЕЗ кавычек:\n"
                    "     move(m[:, 1], m[:, 4], after)\n"
                    "     move(m[:, 1], m[:, 4], before)"
                ),
                'variants': [
                    'r = move(m[:, 1], m[:, 4], after)',
                    'r = move(m[:, 1], m[:, 4], before)',
                ],
            },
            'MOVE_BAD_SOURCE': {
                'message': (
                    "move: источник должен быть срезом матрицы."
                ),
                'wrong': 'move(42, m[:, 4], after)',
                'right': 'move(m[:, 1], m[:, 4], after)',
                'explanation': (
                    "Источник — срез одной и той же матрицы:\n"
                    "     m[:, N]       — столбец N\n"
                    "     m[:, \"Имя\"]   — столбец по имени\n"
                    "     m[:, 1:3]     — диапазон столбцов\n"
                    "     m[N, :]       — строка N\n"
                    "     m[2:5, :]     — диапазон строк\n"
                    "\n"
                    "Неправильно:\n"
                    "     move(42, m[:, 4], after)\n"
                    "\n"
                    "Правильно:\n"
                    "     move(m[:, 1], m[:, 4], after)"
                ),
                'variants': [
                    'r = move(m[:, 1], m[:, 4], after)',
                    'r = move(m[2, :], m[10, :], before)',
                ],
            },
            'MOVE_BAD_TARGET': {
                'message': (
                    "move: цель должна быть срезом матрицы."
                ),
                'wrong': 'move(m[:, 1], 42, after)',
                'right': 'move(m[:, 1], m[:, 4], after)',
                'explanation': (
                    "Цель — срез одной и той же матрицы.\n"
                    "Цель НЕ может быть диапазоном.\n"
                    "\n"
                    "Неправильно:\n"
                    "     move(m[:, 1], m[:, 3:5], after)   — цель диапазон\n"
                    "     move(m[:, 1], 42, after)          — не срез\n"
                    "\n"
                    "Правильно:\n"
                    "     move(m[:, 1], m[:, 4], after)"
                ),
                'variants': [
                    'r = move(m[:, 1], m[:, 4], after)',
                    'r = move(m[2, :], m[10, :], before)',
                ],
            },
            'MOVE_TYPE_MISMATCH': {
                'message': (
                    "move: источник и цель должны быть одного типа.\n"
                    "  Нельзя смешивать строки и столбцы."
                ),
                'wrong': 'move(m[:, 1], m[2, :], after)',
                'right': 'move(m[:, 1], m[:, 4], after)',
                'explanation': (
                    "Если источник — СТОЛБЕЦ, то цель тоже СТОЛБЕЦ.\n"
                    "Если источник — СТРОКА, то цель тоже СТРОКА.\n"
                    "\n"
                    "Неправильно:\n"
                    "     move(m[:, 1], m[2, :], after)\n"
                    "\n"
                    "Правильно:\n"
                    "     move(m[:, 1], m[:, 4], after)   — оба столбца\n"
                    "     move(m[2, :], m[10, :], before) — обе строки"
                ),
                'variants': [
                    'r = move(m[:, 1], m[:, 4], after)',
                    'r = move(m[2, :], m[10, :], before)',
                ],
            },
            'MOVE_TARGET_IS_RANGE': {
                'message': (
                    "move: цель не может быть диапазоном.\n"
                    "  Цель — конкретный столбец или строка."
                ),
                'wrong': 'move(m[:, 1], m[:, 3:5], after)',
                'right': 'move(m[:, 1], m[:, 5], after)',
                'explanation': (
                    "Цель должна быть ОДИН столбец или ОДНА строка.\n"
                    "\n"
                    "Неправильно:\n"
                    "     move(m[:, 1], m[:, 3:5], after)\n"
                    "\n"
                    "Правильно:\n"
                    "     move(m[:, 1], m[:, 5], after)"
                ),
                'variants': [
                    'r = move(m[:, 1], m[:, 5], after)',
                    'r = move(m[2, :], m[10, :], before)',
                ],
            },
            'MOVE_TARGET_INSIDE_SOURCE': {
                'message': (
                    "move: цель находится ВНУТРИ источника.\n"
                    "  Нельзя переместить диапазон внутрь самого себя."
                ),
                'wrong': 'move(m[:, 1:5], m[:, 3], after)',
                'right': 'move(m[:, 1:5], m[:, 7], after)',
                'explanation': (
                    "Когда цель — внутри диапазона-источника,\n"
                    "непонятно, что и куда перемещать.\n"
                    "\n"
                    "Неправильно:\n"
                    "     move(m[:, 1:5], m[:, 3], after)\n"
                    "\n"
                    "Правильно (цель ВНЕ источника):\n"
                    "     move(m[:, 1:5], m[:, 7], after)\n"
                    "     move(m[:, 1:5], m[:, 10], before)"
                ),
                'variants': [
                    'r = move(m[:, 1:5], m[:, 7], after)',
                    'r = move(m[:, 1:5], m[:, 10], before)',
                ],
            },
            'MOVE_DUCKDB': {
                'message': (
                    "move работает только с Matrix (RAM), "
                    "не с BigData (DuckDB).\n"
                    "  BigData — read-only view на файл."
                ),
                'wrong': 'r = move(bd[:, 1], bd[:, 4], after)',
                'right': (
                    'm = ToMatrix(bd)\n'
                    'r = move(m[:, 1], m[:, 4], after)'
                ),
                'explanation': (
                    "BigData (DuckDB) — read-only view на файл.\n"
                    "Он НЕ поддерживает перемещение столбцов/строк.\n"
                    "\n"
                    "Решение:\n"
                    "  1. Конвертировать BigData в Matrix:\n"
                    "        m = ToMatrix(bd)\n"
                    "        r = move(m[:, 1], m[:, 4], after)\n"
                    "\n"
                    "  2. Работать напрямую с Matrix."
                ),
                'variants': [
                    'm = ToMatrix(bd)\nr = move(m[:, 1], m[:, 4], after)',
                    'm = ToMatrix(bd)\nr = move(m[2, :], m[10, :], before)',
                ],
            },
            'MOVE_REQUIRES_ASSIGNMENT': {
                'message': (
                    "move() возвращает значение — "
                    "результат нужно сохранить."
                ),
                'wrong': 'move(m[:, 1], m[:, 4], after)',
                'right': 'r = move(m[:, 1], m[:, 4], after)',
                'explanation': (
                    "move НЕ изменяет исходную матрицу.\n"
                    "Он ВОЗВРАЩАЕТ НОВУЮ.\n"
                    "\n"
                    "Правильно:\n"
                    "  r = move(...)      — в новую переменную\n"
                    "  m = move(...)      — мутация"
                ),
                'variants': [
                    'r = move(m[:, 1], m[:, 4], after)',
                    'm = move(m[:, 1], m[:, 4], after)',
                ],
            },
        },
    },
}


EN = {
    'move': {
        'name': 'move',
        'category': 'modify',
        'signature': 'move(source, target, before | after)',
        'description': (
            'Move a row or column inside a matrix.\n'
            '  • Source and target are slices of the same matrix.\n'
            '  • Direction: before | after.\n'
            '  • Target CANNOT be inside the source.\n'
            '  • Returns a NEW matrix — save the result.\n'
            '  ⚠️  Works only with Matrix (RAM), not with BigData (DuckDB).'
        ),
        'examples': [
            'r = move(m[:, 1], m[:, 4], after)',
            'r = move(m[1:3, :], m[end, :], after)',
        ],
        'errors': {
            'MOVE_BAD_SYNTAX': {
                'message': (
                    "move: invalid syntax.\n"
                    "  Need source, target, and direction."
                ),
                'wrong': 'move(m[:, 1], m[:, 4])',
                'right': 'move(m[:, 1], m[:, 4], after)',
                'explanation': (
                    "move takes THREE arguments:\n"
                    "  1. source — slice m[:, ...] or m[N, :]\n"
                    "  2. target — slice of the same matrix\n"
                    "  3. direction — before | after\n"
                    "\n"
                    "Incorrect:\n"
                    "     move(m[:, 1], m[:, 4])\n"
                    "\n"
                    "Correct:\n"
                    "     move(m[:, 1], m[:, 4], after)\n"
                    "     move(m[:, 1], m[:, 4], before)"
                ),
                'variants': [
                    'r = move(m[:, 1], m[:, 4], after)',
                    'r = move(m[1:10, :], m[end, :], after)',
                ],
            },
            'MOVE_MISSING_DIRECTION': {
                'message': (
                    "move: direction is missing — before or after."
                ),
                'wrong': 'move(m[:, 1], m[:, 4])',
                'right': 'move(m[:, 1], m[:, 4], after)',
                'explanation': (
                    "move takes THREE arguments.\n"
                    "The third is the direction: before or after.\n"
                    "\n"
                    "Incorrect:\n"
                    "     move(m[:, 1], m[:, 4])\n"
                    "\n"
                    "Correct:\n"
                    "     move(m[:, 1], m[:, 4], after)\n"
                    "     move(m[:, 1], m[:, 4], before)\n"
                    "\n"
                    "Direction is given WITHOUT quotes:\n"
                    "     move(m[:, 1], m[:, 4], after)\n"
                    "     move(m[:, 1], m[:, 4], before)"
                ),
                'variants': [
                    'r = move(m[:, 1], m[:, 4], after)',
                    'r = move(m[:, 1], m[:, 4], before)',
                ],
            },
            'MOVE_BAD_SOURCE': {
                'message': (
                    "move: source must be a matrix slice."
                ),
                'wrong': 'move(42, m[:, 4], after)',
                'right': 'move(m[:, 1], m[:, 4], after)',
                'explanation': (
                    "Source is a slice of the same matrix:\n"
                    "     m[:, N]       — column N\n"
                    "     m[:, \"Name\"]  — column by name\n"
                    "     m[:, 1:3]     — column range\n"
                    "     m[N, :]       — row N\n"
                    "     m[2:5, :]     — row range\n"
                    "\n"
                    "Incorrect:\n"
                    "     move(42, m[:, 4], after)\n"
                    "\n"
                    "Correct:\n"
                    "     move(m[:, 1], m[:, 4], after)"
                ),
                'variants': [
                    'r = move(m[:, 1], m[:, 4], after)',
                    'r = move(m[2, :], m[10, :], before)',
                ],
            },
            'MOVE_BAD_TARGET': {
                'message': (
                    "move: target must be a matrix slice."
                ),
                'wrong': 'move(m[:, 1], 42, after)',
                'right': 'move(m[:, 1], m[:, 4], after)',
                'explanation': (
                    "Target is a slice of the same matrix.\n"
                    "Target CANNOT be a range.\n"
                    "\n"
                    "Incorrect:\n"
                    "     move(m[:, 1], m[:, 3:5], after)   — target is range\n"
                    "     move(m[:, 1], 42, after)          — not a slice\n"
                    "\n"
                    "Correct:\n"
                    "     move(m[:, 1], m[:, 4], after)"
                ),
                'variants': [
                    'r = move(m[:, 1], m[:, 4], after)',
                    'r = move(m[2, :], m[10, :], before)',
                ],
            },
            'MOVE_TYPE_MISMATCH': {
                'message': (
                    "move: source and target must be the same type.\n"
                    "  Cannot mix rows and columns."
                ),
                'wrong': 'move(m[:, 1], m[2, :], after)',
                'right': 'move(m[:, 1], m[:, 4], after)',
                'explanation': (
                    "If source is a COLUMN, target must be a COLUMN.\n"
                    "If source is a ROW, target must be a ROW.\n"
                    "\n"
                    "Incorrect:\n"
                    "     move(m[:, 1], m[2, :], after)\n"
                    "\n"
                    "Correct:\n"
                    "     move(m[:, 1], m[:, 4], after)   — both columns\n"
                    "     move(m[2, :], m[10, :], before) — both rows"
                ),
                'variants': [
                    'r = move(m[:, 1], m[:, 4], after)',
                    'r = move(m[2, :], m[10, :], before)',
                ],
            },
            'MOVE_TARGET_IS_RANGE': {
                'message': (
                    "move: target cannot be a range.\n"
                    "  Target is a single column or row."
                ),
                'wrong': 'move(m[:, 1], m[:, 3:5], after)',
                'right': 'move(m[:, 1], m[:, 5], after)',
                'explanation': (
                    "Target must be ONE column or ONE row.\n"
                    "\n"
                    "Incorrect:\n"
                    "     move(m[:, 1], m[:, 3:5], after)\n"
                    "\n"
                    "Correct:\n"
                    "     move(m[:, 1], m[:, 5], after)"
                ),
                'variants': [
                    'r = move(m[:, 1], m[:, 5], after)',
                    'r = move(m[2, :], m[10, :], before)',
                ],
            },
            'MOVE_TARGET_INSIDE_SOURCE': {
                'message': (
                    "move: target is INSIDE the source.\n"
                    "  Cannot move a range into itself."
                ),
                'wrong': 'move(m[:, 1:5], m[:, 3], after)',
                'right': 'move(m[:, 1:5], m[:, 7], after)',
                'explanation': (
                    "When the target is inside the source range,\n"
                    "it's unclear what to move where.\n"
                    "\n"
                    "Incorrect:\n"
                    "     move(m[:, 1:5], m[:, 3], after)\n"
                    "\n"
                    "Correct (target OUTSIDE source):\n"
                    "     move(m[:, 1:5], m[:, 7], after)\n"
                    "     move(m[:, 1:5], m[:, 10], before)"
                ),
                'variants': [
                    'r = move(m[:, 1:5], m[:, 7], after)',
                    'r = move(m[:, 1:5], m[:, 10], before)',
                ],
            },
            'MOVE_DUCKDB': {
                'message': (
                    "move works only with Matrix (RAM), "
                    "not with BigData (DuckDB).\n"
                    "  BigData is a read-only view on a file."
                ),
                'wrong': 'r = move(bd[:, 1], bd[:, 4], after)',
                'right': (
                    'm = ToMatrix(bd)\n'
                    'r = move(m[:, 1], m[:, 4], after)'
                ),
                'explanation': (
                    "BigData (DuckDB) is a read-only view on a file.\n"
                    "It does NOT support moving columns/rows.\n"
                    "\n"
                    "Solution:\n"
                    "  1. Convert BigData to Matrix:\n"
                    "        m = ToMatrix(bd)\n"
                    "        r = move(m[:, 1], m[:, 4], after)\n"
                    "\n"
                    "  2. Work directly with Matrix."
                ),
                'variants': [
                    'm = ToMatrix(bd)\nr = move(m[:, 1], m[:, 4], after)',
                    'm = ToMatrix(bd)\nr = move(m[2, :], m[10, :], before)',
                ],
            },
            'MOVE_REQUIRES_ASSIGNMENT': {
                'message': (
                    "move() returns a value — "
                    "the result must be saved."
                ),
                'wrong': 'move(m[:, 1], m[:, 4], after)',
                'right': 'r = move(m[:, 1], m[:, 4], after)',
                'explanation': (
                    "move does NOT modify the source matrix.\n"
                    "It RETURNS a NEW one.\n"
                    "\n"
                    "Correct:\n"
                    "  r = move(...)      — to a new variable\n"
                    "  m = move(...)      — mutation"
                ),
                'variants': [
                    'r = move(m[:, 1], m[:, 4], after)',
                    'm = move(m[:, 1], m[:, 4], after)',
                ],
            },
        },
    },
}