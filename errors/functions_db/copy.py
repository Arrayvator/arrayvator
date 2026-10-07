# errors/functions_db/copy.py
"""
База ошибок для функции COPY — копирование строки/столбца внутри матрицы.

СИНТАКСИС:
    copy(s[:, 1], s[:, 10], after)       # столбец
    copy(s[:, 1:3], s[:, 10], after)     # диапазон столбцов
    copy(s[:, end], s[:, 10], after)     # последний столбец
    copy(s[2, :], s[10, :], before)      # строка
    copy(s[2:5, :], s[10, :], after)     # диапазон строк
    copy(s["Боб", :], s["Гоша", :], after)   # строка по имени

⚠️  Работает ТОЛЬКО с Matrix (RAM).
    НЕ работает с BigData (DuckDB).
"""


RU = {
    'copy': {
        'name': 'copy',
        'category': 'modify',
        'signature': 'copy(источник, цель, before | after)',
        'description': (
            'Копирует строку или столбец внутри матрицы.\n'
            '  • Источник и цель — срезы одной матрицы.\n'
            '  • Направление: before | after.\n'
            '  • Возвращает НОВУЮ матрицу — результат нужно сохранить.\n'
            '  ⚠️  Работает только с Matrix (RAM), не с BigData (DuckDB).'
        ),
        'examples': [
            'r = copy(m[:, 1], m[:, 3], after)',
            'r = copy(m[:, 1:3], m[:, 5], after)',
            'r = copy(m[2, :], m[4, :], before)',
        ],
        'errors': {
            'COPY_BAD_SYNTAX': {
                'message': (
                    "copy: неверный синтаксис.\n"
                    "  Нужны источник, цель и направление."
                ),
                'wrong': 'copy(m[:, 1], m[:, 3])',
                'right': 'copy(m[:, 1], m[:, 3], after)',
                'explanation': (
                    "copy принимает ТРИ аргумента:\n"
                    "  1. источник — срез m[:, ...] или m[N, :]\n"
                    "  2. цель — срез той же матрицы\n"
                    "  3. направление — before | after\n"
                    "\n"
                    "Неправильно:\n"
                    "     copy(m[:, 1], m[:, 3])\n"
                    "\n"
                    "Правильно:\n"
                    "     copy(m[:, 1], m[:, 3], after)\n"
                    "     copy(m[:, 1], m[:, 3], before)"
                ),
                'variants': [
                    'r = copy(m[:, 1], m[:, 3], after)',
                    'r = copy(m[:, 1:3], m[:, 5], after)',
                    'r = copy(m[2, :], m[4, :], before)',
                ],
            },
            'COPY_MISSING_DIRECTION': {
                'message': (
                    "copy: не указано направление — before или after."
                ),
                'wrong': 'copy(m[:, 1], m[:, 3])',
                'right': 'copy(m[:, 1], m[:, 3], after)',
                'explanation': (
                    "copy принимает ТРИ аргумента.\n"
                    "Третий — направление: before или after.\n"
                    "\n"
                    "Неправильно:\n"
                    "     copy(m[:, 1], m[:, 3])\n"
                    "\n"
                    "Правильно:\n"
                    "     copy(m[:, 1], m[:, 3], after)\n"
                    "     copy(m[:, 1], m[:, 3], before)\n"
                    "\n"
                    "Направление указывается БЕЗ кавычек:\n"
                    "     copy(m[:, 1], m[:, 3], after)\n"
                    "     copy(m[:, 1], m[:, 3], before)"
                ),
                'variants': [
                    'r = copy(m[:, 1], m[:, 3], after)',
                    'r = copy(m[:, 1], m[:, 3], before)',
                ],
            },
            'COPY_BAD_SOURCE': {
                'message': (
                    "copy: источник должен быть срезом матрицы."
                ),
                'wrong': 'copy(42, m[:, 3], after)',
                'right': 'copy(m[:, 1], m[:, 3], after)',
                'explanation': (
                    "Источник — срез одной и той же матрицы:\n"
                    "     m[:, N]       — столбец N\n"
                    "     m[:, \"Имя\"]   — столбец по имени\n"
                    "     m[:, 1:3]     — диапазон столбцов\n"
                    "     m[N, :]       — строка N\n"
                    "     m[2:5, :]     — диапазон строк\n"
                    "\n"
                    "Неправильно:\n"
                    "     copy(42, m[:, 3], after)\n"
                    "\n"
                    "Правильно:\n"
                    "     copy(m[:, 1], m[:, 3], after)"
                ),
                'variants': [
                    'r = copy(m[:, 1], m[:, 3], after)',
                    'r = copy(m[2, :], m[4, :], before)',
                ],
            },
            'COPY_BAD_TARGET': {
                'message': (
                    "copy: цель должна быть срезом матрицы."
                ),
                'wrong': 'copy(m[:, 1], 42, after)',
                'right': 'copy(m[:, 1], m[:, 3], after)',
                'explanation': (
                    "Цель — срез одной и той же матрицы.\n"
                    "Цель НЕ может быть диапазоном.\n"
                    "\n"
                    "Неправильно:\n"
                    "     copy(m[:, 1], m[:, 3:5], after)   — цель диапазон\n"
                    "     copy(m[:, 1], 42, after)          — не срез\n"
                    "\n"
                    "Правильно:\n"
                    "     copy(m[:, 1], m[:, 3], after)"
                ),
                'variants': [
                    'r = copy(m[:, 1], m[:, 3], after)',
                    'r = copy(m[2, :], m[4, :], before)',
                ],
            },
            'COPY_TYPE_MISMATCH': {
                'message': (
                    "copy: источник и цель должны быть одного типа.\n"
                    "  Нельзя смешивать строки и столбцы."
                ),
                'wrong': 'copy(m[:, 1], m[2, :], after)',
                'right': 'copy(m[:, 1], m[:, 3], after)',
                'explanation': (
                    "Если источник — СТОЛБЕЦ, то цель тоже СТОЛБЕЦ.\n"
                    "Если источник — СТРОКА, то цель тоже СТРОКА.\n"
                    "\n"
                    "Неправильно:\n"
                    "     copy(m[:, 1], m[2, :], after)\n"
                    "\n"
                    "Правильно:\n"
                    "     copy(m[:, 1], m[:, 3], after)   — оба столбца\n"
                    "     copy(m[2, :], m[4, :], before)  — обе строки"
                ),
                'variants': [
                    'r = copy(m[:, 1], m[:, 3], after)',
                    'r = copy(m[2, :], m[4, :], before)',
                ],
            },
            'COPY_TARGET_IS_RANGE': {
                'message': (
                    "copy: цель не может быть диапазоном.\n"
                    "  Цель — конкретный столбец или строка."
                ),
                'wrong': 'copy(m[:, 1], m[:, 3:5], after)',
                'right': 'copy(m[:, 1], m[:, 5], after)',
                'explanation': (
                    "Цель должна быть ОДИН столбец или ОДНА строка.\n"
                    "\n"
                    "Неправильно:\n"
                    "     copy(m[:, 1], m[:, 3:5], after)\n"
                    "\n"
                    "Правильно:\n"
                    "     copy(m[:, 1], m[:, 5], after)"
                ),
                'variants': [
                    'r = copy(m[:, 1], m[:, 5], after)',
                    'r = copy(m[2, :], m[10, :], before)',
                ],
            },
            'COPY_DUCKDB': {
                'message': (
                    "copy работает только с Matrix (RAM), "
                    "не с BigData (DuckDB).\n"
                    "  BigData — read-only view на файл."
                ),
                'wrong': 'r = copy(bd[:, 1], bd[:, 3], after)',
                'right': (
                    'm = ToMatrix(bd)\n'
                    'r = copy(m[:, 1], m[:, 3], after)'
                ),
                'explanation': (
                    "BigData (DuckDB) — read-only view на файл.\n"
                    "Он НЕ поддерживает копирование столбцов/строк.\n"
                    "\n"
                    "Решение:\n"
                    "  1. Конвертировать BigData в Matrix:\n"
                    "        m = ToMatrix(bd)\n"
                    "        r = copy(m[:, 1], m[:, 3], after)\n"
                    "\n"
                    "  2. Работать напрямую с Matrix."
                ),
                'variants': [
                    'm = ToMatrix(bd)\nr = copy(m[:, 1], m[:, 3], after)',
                    'm = ToMatrix(bd)\nr = copy(m[2, :], m[4, :], before)',
                ],
            },
            'COPY_REQUIRES_ASSIGNMENT': {
                'message': (
                    "copy() возвращает значение — "
                    "результат нужно сохранить."
                ),
                'wrong': 'copy(m[:, 1], m[:, 3], after)',
                'right': 'r = copy(m[:, 1], m[:, 3], after)',
                'explanation': (
                    "copy НЕ изменяет исходную матрицу.\n"
                    "Он ВОЗВРАЩАЕТ НОВУЮ.\n"
                    "\n"
                    "Правильно:\n"
                    "  r = copy(...)      — в новую переменную\n"
                    "  m = copy(...)      — мутация"
                ),
                'variants': [
                    'r = copy(m[:, 1], m[:, 3], after)',
                    'm = copy(m[:, 1], m[:, 3], after)',
                ],
            },
        },
    },
}


EN = {
    'copy': {
        'name': 'copy',
        'category': 'modify',
        'signature': 'copy(source, target, before | after)',
        'description': (
            'Copy a row or column inside a matrix.\n'
            '  • Source and target are slices of the same matrix.\n'
            '  • Direction: before | after.\n'
            '  • Returns a NEW matrix — save the result.\n'
            '  ⚠️  Works only with Matrix (RAM), not with BigData (DuckDB).'
        ),
        'examples': [
            'r = copy(m[:, 1], m[:, 3], after)',
            'r = copy(m[:, 1:3], m[:, 5], after)',
            'r = copy(m[2, :], m[4, :], before)',
        ],
        'errors': {
            'COPY_BAD_SYNTAX': {
                'message': (
                    "copy: invalid syntax.\n"
                    "  Need source, target, and direction."
                ),
                'wrong': 'copy(m[:, 1], m[:, 3])',
                'right': 'copy(m[:, 1], m[:, 3], after)',
                'explanation': (
                    "copy takes THREE arguments:\n"
                    "  1. source — slice m[:, ...] or m[N, :]\n"
                    "  2. target — slice of the same matrix\n"
                    "  3. direction — before | after\n"
                    "\n"
                    "Incorrect:\n"
                    "     copy(m[:, 1], m[:, 3])\n"
                    "\n"
                    "Correct:\n"
                    "     copy(m[:, 1], m[:, 3], after)\n"
                    "     copy(m[:, 1], m[:, 3], before)"
                ),
                'variants': [
                    'r = copy(m[:, 1], m[:, 3], after)',
                    'r = copy(m[:, 1:3], m[:, 5], after)',
                    'r = copy(m[2, :], m[4, :], before)',
                ],
            },
            'COPY_MISSING_DIRECTION': {
                'message': (
                    "copy: direction is missing — before or after."
                ),
                'wrong': 'copy(m[:, 1], m[:, 3])',
                'right': 'copy(m[:, 1], m[:, 3], after)',
                'explanation': (
                    "copy takes THREE arguments.\n"
                    "The third is the direction: before or after.\n"
                    "\n"
                    "Incorrect:\n"
                    "     copy(m[:, 1], m[:, 3])\n"
                    "\n"
                    "Correct:\n"
                    "     copy(m[:, 1], m[:, 3], after)\n"
                    "     copy(m[:, 1], m[:, 3], before)\n"
                    "\n"
                    "Direction is given WITHOUT quotes:\n"
                    "     copy(m[:, 1], m[:, 3], after)\n"
                    "     copy(m[:, 1], m[:, 3], before)"
                ),
                'variants': [
                    'r = copy(m[:, 1], m[:, 3], after)',
                    'r = copy(m[:, 1], m[:, 3], before)',
                ],
            },
            'COPY_BAD_SOURCE': {
                'message': (
                    "copy: source must be a matrix slice."
                ),
                'wrong': 'copy(42, m[:, 3], after)',
                'right': 'copy(m[:, 1], m[:, 3], after)',
                'explanation': (
                    "Source is a slice of the same matrix:\n"
                    "     m[:, N]       — column N\n"
                    "     m[:, \"Name\"]  — column by name\n"
                    "     m[:, 1:3]     — column range\n"
                    "     m[N, :]       — row N\n"
                    "     m[2:5, :]     — row range\n"
                    "\n"
                    "Incorrect:\n"
                    "     copy(42, m[:, 3], after)\n"
                    "\n"
                    "Correct:\n"
                    "     copy(m[:, 1], m[:, 3], after)"
                ),
                'variants': [
                    'r = copy(m[:, 1], m[:, 3], after)',
                    'r = copy(m[2, :], m[4, :], before)',
                ],
            },
            'COPY_BAD_TARGET': {
                'message': (
                    "copy: target must be a matrix slice."
                ),
                'wrong': 'copy(m[:, 1], 42, after)',
                'right': 'copy(m[:, 1], m[:, 3], after)',
                'explanation': (
                    "Target is a slice of the same matrix.\n"
                    "Target CANNOT be a range.\n"
                    "\n"
                    "Incorrect:\n"
                    "     copy(m[:, 1], m[:, 3:5], after)   — target is range\n"
                    "     copy(m[:, 1], 42, after)          — not a slice\n"
                    "\n"
                    "Correct:\n"
                    "     copy(m[:, 1], m[:, 3], after)"
                ),
                'variants': [
                    'r = copy(m[:, 1], m[:, 3], after)',
                    'r = copy(m[2, :], m[4, :], before)',
                ],
            },
            'COPY_TYPE_MISMATCH': {
                'message': (
                    "copy: source and target must be the same type.\n"
                    "  Cannot mix rows and columns."
                ),
                'wrong': 'copy(m[:, 1], m[2, :], after)',
                'right': 'copy(m[:, 1], m[:, 3], after)',
                'explanation': (
                    "If source is a COLUMN, target must be a COLUMN.\n"
                    "If source is a ROW, target must be a ROW.\n"
                    "\n"
                    "Incorrect:\n"
                    "     copy(m[:, 1], m[2, :], after)\n"
                    "\n"
                    "Correct:\n"
                    "     copy(m[:, 1], m[:, 3], after)   — both columns\n"
                    "     copy(m[2, :], m[4, :], before)  — both rows"
                ),
                'variants': [
                    'r = copy(m[:, 1], m[:, 3], after)',
                    'r = copy(m[2, :], m[4, :], before)',
                ],
            },
            'COPY_TARGET_IS_RANGE': {
                'message': (
                    "copy: target cannot be a range.\n"
                    "  Target is a single column or row."
                ),
                'wrong': 'copy(m[:, 1], m[:, 3:5], after)',
                'right': 'copy(m[:, 1], m[:, 5], after)',
                'explanation': (
                    "Target must be ONE column or ONE row.\n"
                    "\n"
                    "Incorrect:\n"
                    "     copy(m[:, 1], m[:, 3:5], after)\n"
                    "\n"
                    "Correct:\n"
                    "     copy(m[:, 1], m[:, 5], after)"
                ),
                'variants': [
                    'r = copy(m[:, 1], m[:, 5], after)',
                    'r = copy(m[2, :], m[10, :], before)',
                ],
            },
            'COPY_DUCKDB': {
                'message': (
                    "copy works only with Matrix (RAM), "
                    "not with BigData (DuckDB).\n"
                    "  BigData is a read-only view on a file."
                ),
                'wrong': 'r = copy(bd[:, 1], bd[:, 3], after)',
                'right': (
                    'm = ToMatrix(bd)\n'
                    'r = copy(m[:, 1], m[:, 3], after)'
                ),
                'explanation': (
                    "BigData (DuckDB) is a read-only view on a file.\n"
                    "It does NOT support copying columns/rows.\n"
                    "\n"
                    "Solution:\n"
                    "  1. Convert BigData to Matrix:\n"
                    "        m = ToMatrix(bd)\n"
                    "        r = copy(m[:, 1], m[:, 3], after)\n"
                    "\n"
                    "  2. Work directly with Matrix."
                ),
                'variants': [
                    'm = ToMatrix(bd)\nr = copy(m[:, 1], m[:, 3], after)',
                    'm = ToMatrix(bd)\nr = copy(m[2, :], m[4, :], before)',
                ],
            },
            'COPY_REQUIRES_ASSIGNMENT': {
                'message': (
                    "copy() returns a value — "
                    "the result must be saved."
                ),
                'wrong': 'copy(m[:, 1], m[:, 3], after)',
                'right': 'r = copy(m[:, 1], m[:, 3], after)',
                'explanation': (
                    "copy does NOT modify the source matrix.\n"
                    "It RETURNS a NEW one.\n"
                    "\n"
                    "Correct:\n"
                    "  r = copy(...)      — to a new variable\n"
                    "  m = copy(...)      — mutation"
                ),
                'variants': [
                    'r = copy(m[:, 1], m[:, 3], after)',
                    'm = copy(m[:, 1], m[:, 3], after)',
                ],
            },
        },
    },
}