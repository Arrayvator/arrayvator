# errors/functions_db/joinarray.py
"""
База ошибок для функции JOINARRAY — объединение матриц.

СИНТАКСИС:
    joinarray(m1, m2, vertical)              — строки вниз
    joinarray(m1, m2, horizontal)            — столбцы вправо
    joinarray(m1, m2, m3, vertical)          — несколько матриц
    joinarray(m1, m2, m3, m4, horizontal)

ПРАВИЛА:
    - Работает только с ЦЕЛЫМИ матрицами (не срезами).
    - vertical — строки вниз (одинаковое число столбцов).
    - horizontal — столбцы вправо (одинаковое число строк).
    - Возвращает НОВУЮ матрицу.
    - Работает с Matrix и DuckDB.
"""


RU = {
    'joinarray': {
        'name': 'joinarray',
        'category': 'analytics',
        'signature': 'joinarray(m1, m2 [, m3, ...], vertical | horizontal)',
        'description': (
            'Объединяет матрицы.\n'
            '  • vertical — строки вниз (одинаковое число столбцов).\n'
            '  • horizontal — столбцы вправо (одинаковое число строк).\n'
            '  • Работает с Matrix и DuckDB.\n'
            '  • Возвращает НОВУЮ матрицу.\n'
            '  ⚠️  Нельзя объединять срезы (части матриц) — только целые.'
        ),
        'examples': [
            'r = joinarray(a, b, vertical)',
            'r = joinarray(a, b, horizontal)',
            'r = joinarray(a, b, c, vertical)',
        ],
        'errors': {
            'JOINARRAY_BAD_SYNTAX': {
                'message': (
                    "joinarray: неверный синтаксис.\n"
                    "  Нужно минимум ДВЕ матрицы и направление."
                ),
                'wrong': 'joinarray(a)',
                'right': 'joinarray(a, b, vertical)',
                'explanation': (
                    "joinarray принимает:\n"
                    "  • минимум ДВЕ матрицы\n"
                    "  • направление vertical или horizontal (последним аргументом)\n"
                    "\n"
                    "Неправильно:\n"
                    "     joinarray(a)\n"
                    "     joinarray(a, b)\n"
                    "     joinarray(a, b, c)         — нет направления\n"
                    "\n"
                    "Правильно:\n"
                    "     joinarray(a, b, vertical)\n"
                    "     joinarray(a, b, horizontal)\n"
                    "     joinarray(a, b, c, vertical)"
                ),
                'variants': [
                    'r = joinarray(a, b, vertical)',
                    'r = joinarray(a, b, horizontal)',
                    'r = joinarray(a, b, c, vertical)',
                ],
            },
            'JOINARRAY_NO_SLICES': {
                'message': (
                    "Нельзя объединять частичные диапазоны.\n"
                    "  joinarray() работает только с ЦЕЛЫМИ матрицами."
                ),
                'wrong': 'r = joinarray(a[:, 1:3], b, vertical)',
                'right': (
                    'col1 = a[:, 1]\n'
                    'col2 = b[:, 1]\n'
                    'r = joinarray(col1, col2, horizontal)'
                ),
                'explanation': (
                    "joinarray принимает ТОЛЬКО целые матрицы.\n"
                    "Срез — это часть матрицы, его нельзя передать.\n"
                    "\n"
                    "РЕШЕНИЕ 1 — извлеките срез в переменную:\n"
                    "     col1 = a[:, 1:3]        — вектор/матрица\n"
                    "     col2 = b[:, 1:3]\n"
                    "     r = joinarray(col1, col2, horizontal)\n"
                    "\n"
                    "РЕШЕНИЕ 2 — объединяйте целые матрицы:\n"
                    "     r = joinarray(a, b, horizontal)"
                ),
                'variants': [
                    'r = joinarray(a, b, vertical)',
                    'r = joinarray(a, b, horizontal)',
                    'col1 = a[:, 1:3]\nr = joinarray(col1, b, horizontal)',
                ],
            },
            'JOINARRAY_BAD_AXIS': {
                'message': (
                    "joinarray: направление должно быть vertical или horizontal."
                ),
                'wrong': 'joinarray(a, b, diag)',
                'right': 'joinarray(a, b, vertical)',
                'explanation': (
                    "Только два направления:\n"
                    "     vertical    — строки ВНИЗ\n"
                    "     horizontal  — столбцы ВПРАВО\n"
                    "\n"
                    "Неправильно:\n"
                    "     joinarray(a, b, diag)\n"
                    "     joinarray(a, b, \"vertical\")   — кавычки\n"
                    "\n"
                    "Правильно:\n"
                    "     joinarray(a, b, vertical)\n"
                    "     joinarray(a, b, horizontal)"
                ),
                'variants': [
                    'r = joinarray(a, b, vertical)',
                    'r = joinarray(a, b, horizontal)',
                ],
            },
            'JOINARRAY_SIZE_MISMATCH': {
                'message': (
                    "joinarray: размеры матриц не совпадают.\n"
                    "  vertical → одинаковое число столбцов.\n"
                    "  horizontal → одинаковое число строк."
                ),
                'wrong': 'joinarray(a, b, vertical)   # разное число столбцов',
                'right': 'joinarray(a, b, vertical)   # одинаковое число столбцов',
                'explanation': (
                    "Правила объединения:\n"
                    "  • vertical   — число СТОЛБЦОВ должно совпадать\n"
                    "  • horizontal — число СТРОК должно совпадать\n"
                    "\n"
                    "Проверьте размеры:\n"
                    "     print(lencol(a), lencol(b))   # для vertical\n"
                    "     print(lenrow(a), lenrow(b))   # для horizontal\n"
                    "\n"
                    "Если размеры разные — используйте addrows или addcolumn\n"
                    "для выравнивания."
                ),
                'variants': [
                    'r = joinarray(a, b, vertical)',
                    'r = joinarray(a, b, horizontal)',
                ],
            },
            'JOINARRAY_NOT_MATRIX': {
                'message': (
                    "joinarray: аргументы должны быть матрицами или DuckDB."
                ),
                'wrong': 'joinarray(42, b, vertical)',
                'right': 'joinarray(a, b, vertical)',
                'explanation': (
                    "joinarray работает с:\n"
                    "     m1, m2  — Matrix (RAM)\n"
                    "     bd1, bd2 — DuckDB (BigData)\n"
                    "\n"
                    "Неправильно:\n"
                    "     joinarray(42, b, vertical)\n"
                    "     joinarray(\"text\", b, vertical)\n"
                    "\n"
                    "Правильно:\n"
                    "     joinarray(a, b, vertical)"
                ),
                'variants': [
                    'r = joinarray(a, b, vertical)',
                    'r = joinarray(bd1, bd2, vertical)',
                ],
            },
            'JOINARRAY_MIXED_TYPES': {
                'message': (
                    "joinarray: нельзя смешивать Matrix и DuckDB."
                ),
                'wrong': 'joinarray(m, bd, vertical)',
                'right': 'joinarray(m1, m2, vertical)',
                'explanation': (
                    "Все матрицы должны быть одного типа:\n"
                    "     Matrix + Matrix\n"
                    "     DuckDB + DuckDB\n"
                    "\n"
                    "РЕШЕНИЕ 1 — конвертировать в DuckDB:\n"
                    "     bd2 = ToBigData(m2)\n"
                    "     r = joinarray(bd1, bd2, vertical)\n"
                    "\n"
                    "РЕШЕНИЕ 2 — конвертировать в Matrix:\n"
                    "     m2 = ToMatrix(bd2)\n"
                    "     r = joinarray(m1, m2, vertical)"
                ),
                'variants': [
                    'r = joinarray(m1, m2, vertical)',
                    'bd2 = ToBigData(m2)\nr = joinarray(bd1, bd2, vertical)',
                    'm2 = ToMatrix(bd2)\nr = joinarray(m1, m2, vertical)',
                ],
            },
            'JOINARRAY_REQUIRES_ASSIGNMENT': {
                'message': (
                    "joinarray() возвращает значение — "
                    "результат нужно сохранить."
                ),
                'wrong': 'joinarray(a, b, vertical)',
                'right': 'r = joinarray(a, b, vertical)',
                'explanation': (
                    "joinarray НЕ изменяет исходные матрицы.\n"
                    "Он ВОЗВРАЩАЕТ НОВУЮ.\n"
                    "\n"
                    "Правильно:\n"
                    "  r = joinarray(...)      — в новую переменную\n"
                    "  a = joinarray(a, b, vertical)  — перезапись\n"
                    "  print(joinarray(...))   — вывод"
                ),
                'variants': [
                    'r = joinarray(a, b, vertical)',
                    'a = joinarray(a, b, vertical)',
                    'print(joinarray(a, b, vertical))',
                ],
            },
        },
    },
}


EN = {
    'joinarray': {
        'name': 'joinarray',
        'category': 'analytics',
        'signature': 'joinarray(m1, m2 [, m3, ...], vertical | horizontal)',
        'description': (
            'Joins matrices.\n'
            '  • vertical — rows downward (same column count).\n'
            '  • horizontal — columns rightward (same row count).\n'
            '  • Works with Matrix and DuckDB.\n'
            '  • Returns a NEW matrix.\n'
            '  ⚠️  Cannot join slices (parts of matrices) — only whole ones.'
        ),
        'examples': [
            'r = joinarray(a, b, vertical)',
            'r = joinarray(a, b, horizontal)',
            'r = joinarray(a, b, c, vertical)',
        ],
        'errors': {
            'JOINARRAY_BAD_SYNTAX': {
                'message': (
                    "joinarray: invalid syntax.\n"
                    "  Need at least TWO matrices and a direction."
                ),
                'wrong': 'joinarray(a)',
                'right': 'joinarray(a, b, vertical)',
                'explanation': (
                    "joinarray takes:\n"
                    "  • at least TWO matrices\n"
                    "  • direction vertical or horizontal (last argument)\n"
                    "\n"
                    "Incorrect:\n"
                    "     joinarray(a)\n"
                    "     joinarray(a, b)\n"
                    "     joinarray(a, b, c)         — no direction\n"
                    "\n"
                    "Correct:\n"
                    "     joinarray(a, b, vertical)\n"
                    "     joinarray(a, b, horizontal)\n"
                    "     joinarray(a, b, c, vertical)"
                ),
                'variants': [
                    'r = joinarray(a, b, vertical)',
                    'r = joinarray(a, b, horizontal)',
                    'r = joinarray(a, b, c, vertical)',
                ],
            },
            'JOINARRAY_NO_SLICES': {
                'message': (
                    "Cannot join partial ranges.\n"
                    "  joinarray() works only with WHOLE matrices."
                ),
                'wrong': 'r = joinarray(a[:, 1:3], b, vertical)',
                'right': (
                    'col1 = a[:, 1]\n'
                    'col2 = b[:, 1]\n'
                    'r = joinarray(col1, col2, horizontal)'
                ),
                'explanation': (
                    "joinarray takes ONLY whole matrices.\n"
                    "A slice is a part of a matrix and cannot be passed.\n"
                    "\n"
                    "SOLUTION 1 — extract the slice into a variable:\n"
                    "     col1 = a[:, 1:3]\n"
                    "     col2 = b[:, 1:3]\n"
                    "     r = joinarray(col1, col2, horizontal)\n"
                    "\n"
                    "SOLUTION 2 — join whole matrices:\n"
                    "     r = joinarray(a, b, horizontal)"
                ),
                'variants': [
                    'r = joinarray(a, b, vertical)',
                    'r = joinarray(a, b, horizontal)',
                    'col1 = a[:, 1:3]\nr = joinarray(col1, b, horizontal)',
                ],
            },
            'JOINARRAY_BAD_AXIS': {
                'message': (
                    "joinarray: direction must be vertical or horizontal."
                ),
                'wrong': 'joinarray(a, b, diag)',
                'right': 'joinarray(a, b, vertical)',
                'explanation': (
                    "Only two directions:\n"
                    "     vertical    — rows DOWN\n"
                    "     horizontal  — columns RIGHT\n"
                    "\n"
                    "Incorrect:\n"
                    "     joinarray(a, b, diag)\n"
                    "     joinarray(a, b, \"vertical\")   — quotes\n"
                    "\n"
                    "Correct:\n"
                    "     joinarray(a, b, vertical)\n"
                    "     joinarray(a, b, horizontal)"
                ),
                'variants': [
                    'r = joinarray(a, b, vertical)',
                    'r = joinarray(a, b, horizontal)',
                ],
            },
            'JOINARRAY_SIZE_MISMATCH': {
                'message': (
                    "joinarray: matrix sizes do not match.\n"
                    "  vertical → same column count.\n"
                    "  horizontal → same row count."
                ),
                'wrong': 'joinarray(a, b, vertical)   # different column count',
                'right': 'joinarray(a, b, vertical)   # same column count',
                'explanation': (
                    "Joining rules:\n"
                    "  • vertical   — COLUMN count must match\n"
                    "  • horizontal — ROW count must match\n"
                    "\n"
                    "Check sizes:\n"
                    "     print(lencol(a), lencol(b))   # for vertical\n"
                    "     print(lenrow(a), lenrow(b))   # for horizontal\n"
                    "\n"
                    "If sizes differ — use addrows or addcolumn to align."
                ),
                'variants': [
                    'r = joinarray(a, b, vertical)',
                    'r = joinarray(a, b, horizontal)',
                ],
            },
            'JOINARRAY_NOT_MATRIX': {
                'message': (
                    "joinarray: arguments must be matrices or DuckDB."
                ),
                'wrong': 'joinarray(42, b, vertical)',
                'right': 'joinarray(a, b, vertical)',
                'explanation': (
                    "joinarray works with:\n"
                    "     m1, m2   — Matrix (RAM)\n"
                    "     bd1, bd2 — DuckDB (BigData)\n"
                    "\n"
                    "Incorrect:\n"
                    "     joinarray(42, b, vertical)\n"
                    "     joinarray(\"text\", b, vertical)\n"
                    "\n"
                    "Correct:\n"
                    "     joinarray(a, b, vertical)"
                ),
                'variants': [
                    'r = joinarray(a, b, vertical)',
                    'r = joinarray(bd1, bd2, vertical)',
                ],
            },
            'JOINARRAY_MIXED_TYPES': {
                'message': (
                    "joinarray: cannot mix Matrix and DuckDB."
                ),
                'wrong': 'joinarray(m, bd, vertical)',
                'right': 'joinarray(m1, m2, vertical)',
                'explanation': (
                    "All matrices must be of the same type:\n"
                    "     Matrix + Matrix\n"
                    "     DuckDB + DuckDB\n"
                    "\n"
                    "SOLUTION 1 — convert to DuckDB:\n"
                    "     bd2 = ToBigData(m2)\n"
                    "     r = joinarray(bd1, bd2, vertical)\n"
                    "\n"
                    "SOLUTION 2 — convert to Matrix:\n"
                    "     m2 = ToMatrix(bd2)\n"
                    "     r = joinarray(m1, m2, vertical)"
                ),
                'variants': [
                    'r = joinarray(m1, m2, vertical)',
                    'bd2 = ToBigData(m2)\nr = joinarray(bd1, bd2, vertical)',
                    'm2 = ToMatrix(bd2)\nr = joinarray(m1, m2, vertical)',
                ],
            },
            'JOINARRAY_REQUIRES_ASSIGNMENT': {
                'message': (
                    "joinarray() returns a value — "
                    "the result must be saved."
                ),
                'wrong': 'joinarray(a, b, vertical)',
                'right': 'r = joinarray(a, b, vertical)',
                'explanation': (
                    "joinarray does NOT modify the source matrices.\n"
                    "It RETURNS a NEW one.\n"
                    "\n"
                    "Correct:\n"
                    "  r = joinarray(...)      — to a new variable\n"
                    "  a = joinarray(a, b, vertical)  — overwrite\n"
                    "  print(joinarray(...))   — output"
                ),
                'variants': [
                    'r = joinarray(a, b, vertical)',
                    'a = joinarray(a, b, vertical)',
                    'print(joinarray(a, b, vertical))',
                ],
            },
        },
    },
}