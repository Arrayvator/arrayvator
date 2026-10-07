# errors/functions_db/matrixmod.py
"""
База ошибок для функции MATRIXMOD — модификация строк матрицы.

СИНТАКСИС:
    matrixmod(m, delete, N)              # удалить строки N
    matrixmod(m, insert, N, before)      # пустые строки перед N
    matrixmod(m, insert, N, after)       # пустые строки после N
    matrixmod(m, duplicate, N, before)   # копии строк перед N
    matrixmod(m, duplicate, N, after)    # копии строк после N
    matrixmod(m, clear, N)               # обнулить строки N
    matrixmod(m, keep, N)                # оставить только строки N
    matrixmod(m, swap, [a, b])           # поменять строки a и b местами

ДЕЙСТВИЯ: delete, insert, duplicate, clear, keep, swap.

⚠️  Работает ТОЛЬКО с Matrix (RAM).
    НЕ работает с BigData (DuckDB).
"""


RU = {
    'matrixmod': {
        'name': 'matrixmod',
        'category': 'modify',
        'signature': 'matrixmod(m, действие, N [, before|after])',
        'description': (
            'Модификация строк матрицы.\n'
            '  • Действия: delete, insert, duplicate, clear, keep, swap.\n'
            '  • N — число, вектор, last K, end.\n'
            '  • insert / duplicate требуют направление (before | after).\n'
            '  • Возвращает НОВУЮ матрицу — результат нужно сохранить.\n'
            '  ⚠️  Работает только с Matrix (RAM), не с BigData (DuckDB).'
        ),
        'examples': [
            'r = matrixmod(m, delete, 2)',
            'r = matrixmod(m, insert, 2, before)',
            'r = matrixmod(m, duplicate, [2, 4], after)',
            'r = matrixmod(m, clear, 3)',
            'r = matrixmod(m, keep, [2, 4, 5])',
            'r = matrixmod(m, swap, [2, 5])',
        ],
        'errors': {
            'MATRIXMOD_BAD_SYNTAX': {
                'message': (
                    "matrixmod: неверный синтаксис.\n"
                    "  Нужна матрица, действие и N."
                ),
                'wrong': 'matrixmod(m, 2)',
                'right': 'matrixmod(m, delete, 2)',
                'explanation': (
                    "matrixmod принимает минимум ТРИ аргумента:\n"
                    "  1. матрица\n"
                    "  2. действие — delete, insert, duplicate, clear, keep, swap\n"
                    "  3. N — номер(а) строк\n"
                    "\n"
                    "Неправильно:\n"
                    "     matrixmod(m, 2)\n"
                    "     matrixmod(m, [2, 4])\n"
                    "\n"
                    "Правильно:\n"
                    "     matrixmod(m, delete, 2)\n"
                    "     matrixmod(m, delete, [2, 4])"
                ),
                'variants': [
                    'r = matrixmod(m, delete, 2)',
                    'r = matrixmod(m, insert, 2, before)',
                    'r = matrixmod(m, swap, [2, 5])',
                ],
            },
            'MATRIXMOD_MISSING_ACTION': {
                'message': (
                    "matrixmod: не указано действие.\n"
                    "  Допустимо: delete, insert, duplicate, clear, keep, swap."
                ),
                'wrong': 'matrixmod(m, [2, 4])',
                'right': 'matrixmod(m, delete, [2, 4])',
                'explanation': (
                    "Второй аргумент — действие:\n"
                    "     delete      — удалить строки\n"
                    "     insert      — вставить пустые строки\n"
                    "     duplicate   — дублировать строки\n"
                    "     clear       — обнулить строки\n"
                    "     keep        — оставить только указанные\n"
                    "     swap        — поменять две строки местами\n"
                    "\n"
                    "Неправильно:\n"
                    "     matrixmod(m, [2, 4])\n"
                    "\n"
                    "Правильно:\n"
                    "     matrixmod(m, delete, [2, 4])\n"
                    "     matrixmod(m, swap, [2, 5])"
                ),
                'variants': [
                    'r = matrixmod(m, delete, 2)',
                    'r = matrixmod(m, insert, 2, before)',
                    'r = matrixmod(m, keep, [2, 4])',
                ],
            },
            'MATRIXMOD_BAD_ACTION': {
                'message': (
                    "matrixmod: неизвестное действие.\n"
                    "  Допустимо: delete, insert, duplicate, clear, keep, swap."
                ),
                'wrong': 'matrixmod(m, remove, 2)',
                'right': 'matrixmod(m, delete, 2)',
                'explanation': (
                    "Только шесть действий:\n"
                    "     delete      — удалить строки\n"
                    "     insert      — вставить пустые строки\n"
                    "     duplicate   — дублировать строки\n"
                    "     clear       — обнулить строки (заменить на None)\n"
                    "     keep        — оставить только указанные\n"
                    "     swap        — поменять две строки\n"
                    "\n"
                    "Неправильно:\n"
                    "     matrixmod(m, remove, 2)\n"
                    "     matrixmod(m, del, 2)\n"
                    "\n"
                    "Правильно:\n"
                    "     matrixmod(m, delete, 2)"
                ),
                'variants': [
                    'r = matrixmod(m, delete, 2)',
                    'r = matrixmod(m, insert, 2, before)',
                    'r = matrixmod(m, swap, [2, 5])',
                ],
            },
            'MATRIXMOD_MISSING_DIRECTION': {
                'message': (
                    "matrixmod: для insert / duplicate нужно направление.\n"
                    "  Укажите before или after."
                ),
                'wrong': 'matrixmod(m, insert, 2)',
                'right': 'matrixmod(m, insert, 2, before)',
                'explanation': (
                    "insert и duplicate требуют направление:\n"
                    "     before — ПЕРЕД указанной строкой\n"
                    "     after  — ПОСЛЕ указанной строки\n"
                    "\n"
                    "Неправильно:\n"
                    "     matrixmod(m, insert, 2)\n"
                    "     matrixmod(m, duplicate, [2, 4])\n"
                    "\n"
                    "Правильно:\n"
                    "     matrixmod(m, insert, 2, before)\n"
                    "     matrixmod(m, duplicate, [2, 4], after)"
                ),
                'variants': [
                    'r = matrixmod(m, insert, 2, before)',
                    'r = matrixmod(m, duplicate, [2, 4], after)',
                ],
            },
            'MATRIXMOD_SWAP_NEEDS_TWO': {
                'message': (
                    "matrixmod swap: нужно ровно ДВА номера строк.\n"
                    "  Пример: matrixmod(m, swap, [2, 5])"
                ),
                'wrong': 'matrixmod(m, swap, [2, 5, 7])',
                'right': 'matrixmod(m, swap, [2, 5])',
                'explanation': (
                    "swap меняет две строки местами.\n"
                    "Нужно указать ровно ДВА номера.\n"
                    "\n"
                    "Неправильно:\n"
                    "     matrixmod(m, swap, [2, 5, 7])\n"
                    "     matrixmod(m, swap, 2)\n"
                    "\n"
                    "Правильно:\n"
                    "     matrixmod(m, swap, [2, 5])\n"
                    "     matrixmod(m, swap, [1, 3])"
                ),
                'variants': [
                    'r = matrixmod(m, swap, [2, 5])',
                    'r = matrixmod(m, swap, [1, 10])',
                ],
            },
            'MATRIXMOD_DUCKDB': {
                'message': (
                    "matrixmod работает только с Matrix (RAM), "
                    "не с BigData (DuckDB).\n"
                    "  BigData — read-only view на файл."
                ),
                'wrong': 'r = matrixmod(bd, delete, 2)',
                'right': (
                    'm = ToMatrix(bd)\n'
                    'r = matrixmod(m, delete, 2)'
                ),
                'explanation': (
                    "BigData (DuckDB) — read-only view на файл.\n"
                    "Он НЕ поддерживает модификацию строк.\n"
                    "\n"
                    "Решение:\n"
                    "  1. Конвертировать BigData в Matrix:\n"
                    "        m = ToMatrix(bd)\n"
                    "        r = matrixmod(m, delete, 2)\n"
                    "\n"
                    "  2. Использовать SQL-аналог:\n"
                    "        filterif, deleteif, addrows"
                ),
                'variants': [
                    'm = ToMatrix(bd)\nr = matrixmod(m, delete, 2)',
                    'm = ToMatrix(bd)\nr = matrixmod(m, insert, 2, before)',
                    'm = ToMatrix(bd)\nr = matrixmod(m, swap, [2, 5])',
                ],
            },
            'MATRIXMOD_REQUIRES_ASSIGNMENT': {
                'message': (
                    "matrixmod() возвращает значение — "
                    "результат нужно сохранить."
                ),
                'wrong': 'matrixmod(m, delete, 2)',
                'right': 'r = matrixmod(m, delete, 2)',
                'explanation': (
                    "matrixmod НЕ изменяет исходную матрицу.\n"
                    "Он ВОЗВРАЩАЕТ НОВУЮ.\n"
                    "\n"
                    "Правильно:\n"
                    "  r = matrixmod(...)      — в новую переменную\n"
                    "  m = matrixmod(...)      — мутация"
                ),
                'variants': [
                    'r = matrixmod(m, delete, 2)',
                    'm = matrixmod(m, delete, 2)',
                ],
            },
        },
    },
}


EN = {
    'matrixmod': {
        'name': 'matrixmod',
        'category': 'modify',
        'signature': 'matrixmod(m, action, N [, before|after])',
        'description': (
            'Modify matrix rows.\n'
            '  • Actions: delete, insert, duplicate, clear, keep, swap.\n'
            '  • N — number, vector, last K, end.\n'
            '  • insert / duplicate require a direction (before | after).\n'
            '  • Returns a NEW matrix — save the result.\n'
            '  ⚠️  Works only with Matrix (RAM), not with BigData (DuckDB).'
        ),
        'examples': [
            'r = matrixmod(m, delete, 2)',
            'r = matrixmod(m, insert, 2, before)',
            'r = matrixmod(m, duplicate, [2, 4], after)',
            'r = matrixmod(m, clear, 3)',
            'r = matrixmod(m, keep, [2, 4, 5])',
            'r = matrixmod(m, swap, [2, 5])',
        ],
        'errors': {
            'MATRIXMOD_BAD_SYNTAX': {
                'message': (
                    "matrixmod: invalid syntax.\n"
                    "  Need matrix, action, and N."
                ),
                'wrong': 'matrixmod(m, 2)',
                'right': 'matrixmod(m, delete, 2)',
                'explanation': (
                    "matrixmod takes at least THREE arguments:\n"
                    "  1. matrix\n"
                    "  2. action — delete, insert, duplicate, clear, keep, swap\n"
                    "  3. N — row number(s)\n"
                    "\n"
                    "Incorrect:\n"
                    "     matrixmod(m, 2)\n"
                    "     matrixmod(m, [2, 4])\n"
                    "\n"
                    "Correct:\n"
                    "     matrixmod(m, delete, 2)\n"
                    "     matrixmod(m, delete, [2, 4])"
                ),
                'variants': [
                    'r = matrixmod(m, delete, 2)',
                    'r = matrixmod(m, insert, 2, before)',
                    'r = matrixmod(m, swap, [2, 5])',
                ],
            },
            'MATRIXMOD_MISSING_ACTION': {
                'message': (
                    "matrixmod: action is missing.\n"
                    "  Allowed: delete, insert, duplicate, clear, keep, swap."
                ),
                'wrong': 'matrixmod(m, [2, 4])',
                'right': 'matrixmod(m, delete, [2, 4])',
                'explanation': (
                    "Second argument is the action:\n"
                    "     delete      — delete rows\n"
                    "     insert      — insert empty rows\n"
                    "     duplicate   — duplicate rows\n"
                    "     clear       — clear rows\n"
                    "     keep        — keep only specified rows\n"
                    "     swap        — swap two rows\n"
                    "\n"
                    "Incorrect:\n"
                    "     matrixmod(m, [2, 4])\n"
                    "\n"
                    "Correct:\n"
                    "     matrixmod(m, delete, [2, 4])\n"
                    "     matrixmod(m, swap, [2, 5])"
                ),
                'variants': [
                    'r = matrixmod(m, delete, 2)',
                    'r = matrixmod(m, insert, 2, before)',
                    'r = matrixmod(m, keep, [2, 4])',
                ],
            },
            'MATRIXMOD_BAD_ACTION': {
                'message': (
                    "matrixmod: unknown action.\n"
                    "  Allowed: delete, insert, duplicate, clear, keep, swap."
                ),
                'wrong': 'matrixmod(m, remove, 2)',
                'right': 'matrixmod(m, delete, 2)',
                'explanation': (
                    "Only six actions:\n"
                    "     delete      — delete rows\n"
                    "     insert      — insert empty rows\n"
                    "     duplicate   — duplicate rows\n"
                    "     clear       — clear rows (replace with None)\n"
                    "     keep        — keep only specified rows\n"
                    "     swap        — swap two rows\n"
                    "\n"
                    "Incorrect:\n"
                    "     matrixmod(m, remove, 2)\n"
                    "     matrixmod(m, del, 2)\n"
                    "\n"
                    "Correct:\n"
                    "     matrixmod(m, delete, 2)"
                ),
                'variants': [
                    'r = matrixmod(m, delete, 2)',
                    'r = matrixmod(m, insert, 2, before)',
                    'r = matrixmod(m, swap, [2, 5])',
                ],
            },
            'MATRIXMOD_MISSING_DIRECTION': {
                'message': (
                    "matrixmod: insert / duplicate require a direction.\n"
                    "  Specify before or after."
                ),
                'wrong': 'matrixmod(m, insert, 2)',
                'right': 'matrixmod(m, insert, 2, before)',
                'explanation': (
                    "insert and duplicate require a direction:\n"
                    "     before — BEFORE the specified row\n"
                    "     after  — AFTER the specified row\n"
                    "\n"
                    "Incorrect:\n"
                    "     matrixmod(m, insert, 2)\n"
                    "     matrixmod(m, duplicate, [2, 4])\n"
                    "\n"
                    "Correct:\n"
                    "     matrixmod(m, insert, 2, before)\n"
                    "     matrixmod(m, duplicate, [2, 4], after)"
                ),
                'variants': [
                    'r = matrixmod(m, insert, 2, before)',
                    'r = matrixmod(m, duplicate, [2, 4], after)',
                ],
            },
            'MATRIXMOD_SWAP_NEEDS_TWO': {
                'message': (
                    "matrixmod swap: exactly TWO row numbers required.\n"
                    "  Example: matrixmod(m, swap, [2, 5])"
                ),
                'wrong': 'matrixmod(m, swap, [2, 5, 7])',
                'right': 'matrixmod(m, swap, [2, 5])',
                'explanation': (
                    "swap exchanges two rows.\n"
                    "Exactly TWO numbers required.\n"
                    "\n"
                    "Incorrect:\n"
                    "     matrixmod(m, swap, [2, 5, 7])\n"
                    "     matrixmod(m, swap, 2)\n"
                    "\n"
                    "Correct:\n"
                    "     matrixmod(m, swap, [2, 5])\n"
                    "     matrixmod(m, swap, [1, 3])"
                ),
                'variants': [
                    'r = matrixmod(m, swap, [2, 5])',
                    'r = matrixmod(m, swap, [1, 10])',
                ],
            },
            'MATRIXMOD_DUCKDB': {
                'message': (
                    "matrixmod works only with Matrix (RAM), "
                    "not with BigData (DuckDB).\n"
                    "  BigData is a read-only view on a file."
                ),
                'wrong': 'r = matrixmod(bd, delete, 2)',
                'right': (
                    'm = ToMatrix(bd)\n'
                    'r = matrixmod(m, delete, 2)'
                ),
                'explanation': (
                    "BigData (DuckDB) is a read-only view on a file.\n"
                    "It does NOT support row modification.\n"
                    "\n"
                    "Solution:\n"
                    "  1. Convert BigData to Matrix:\n"
                    "        m = ToMatrix(bd)\n"
                    "        r = matrixmod(m, delete, 2)\n"
                    "\n"
                    "  2. Use SQL analog:\n"
                    "        filterif, deleteif, addrows"
                ),
                'variants': [
                    'm = ToMatrix(bd)\nr = matrixmod(m, delete, 2)',
                    'm = ToMatrix(bd)\nr = matrixmod(m, insert, 2, before)',
                    'm = ToMatrix(bd)\nr = matrixmod(m, swap, [2, 5])',
                ],
            },
            'MATRIXMOD_REQUIRES_ASSIGNMENT': {
                'message': (
                    "matrixmod() returns a value — "
                    "the result must be saved."
                ),
                'wrong': 'matrixmod(m, delete, 2)',
                'right': 'r = matrixmod(m, delete, 2)',
                'explanation': (
                    "matrixmod does NOT modify the source matrix.\n"
                    "It RETURNS a NEW one.\n"
                    "\n"
                    "Correct:\n"
                    "  r = matrixmod(...)      — to a new variable\n"
                    "  m = matrixmod(...)      — mutation"
                ),
                'variants': [
                    'r = matrixmod(m, delete, 2)',
                    'm = matrixmod(m, delete, 2)',
                ],
            },
        },
    },
}