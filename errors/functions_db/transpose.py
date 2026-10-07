# errors/functions_db/transpose.py
"""
База ошибок для функции TRANSPOSE — транспонирование матрицы.

СИНТАКСИС:
    r = transpose(m)
    m = transpose(m)

⚠️  Работает ТОЛЬКО с Matrix (RAM).
    НЕ работает с BigData (DuckDB).
"""


RU = {
    'transpose': {
        'name': 'transpose',
        'category': 'create',
        'signature': 'transpose(матрица)',
        'description': (
            'Транспонирует матрицу: строки ↔ столбцы.\n'
            '  • Было R×C → стало C×R.\n'
            '  • Возвращает НОВУЮ матрицу — результат нужно сохранить.\n'
            '  ⚠️  Работает только с Matrix (RAM), не с BigData (DuckDB).'
        ),
        'examples': [
            'r = transpose(m)',
            'm = transpose(m)',
        ],
        'errors': {
            'TRANSPOSE_BAD_SYNTAX': {
                'message': (
                    "transpose: неверный синтаксис.\n"
                    "  Нужна матрица или вектор."
                ),
                'wrong': 'transpose()',
                'right': 'transpose(m)',
                'explanation': (
                    "transpose принимает ОДИН аргумент — матрицу.\n"
                    "\n"
                    "Структура:\n"
                    "  transpose(матрица)\n"
                    "  transpose(вектор)"
                ),
                'variants': [
                    'r = transpose(m)',
                    'm = transpose(m)',
                ],
            },
            'TRANSPOSE_NOT_MATRIX': {
                'message': (
                    "transpose: ожидается матрица или вектор."
                ),
                'wrong': 'transpose(42)',
                'right': 'transpose(m)',
                'explanation': (
                    "transpose работает только с 2D-матрицами\n"
                    "и векторами.\n"
                    "\n"
                    "Неправильно: transpose(42)\n"
                    "Неправильно: transpose(\"text\")\n"
                    "Правильно: transpose(m)\n"
                    "Правильно: transpose(v)"
                ),
                'variants': [
                    'r = transpose(m)',
                    'r = transpose(v)',
                ],
            },
            'TRANSPOSE_DUCKDB': {
                'message': (
                    "transpose работает только с Matrix (RAM), "
                    "не с BigData (DuckDB).\n"
                    "  BigData — read-only view на файл."
                ),
                'wrong': 'r = transpose(bd)',
                'right': (
                    'm = ToMatrix(bd)\n'
                    'r = transpose(m)'
                ),
                'explanation': (
                    "BigData (DuckDB) — read-only view на файл.\n"
                    "Он НЕ поддерживает транспонирование.\n"
                    "\n"
                    "Решение:\n"
                    "  1. Конвертировать BigData в Matrix:\n"
                    "        m = ToMatrix(bd)\n"
                    "        r = transpose(m)\n"
                    "\n"
                    "  2. Работать напрямую с Matrix."
                ),
                'variants': [
                    'm = ToMatrix(bd)\nr = transpose(m)',
                    'm = ToMatrix(bd)\nm = transpose(m)',
                ],
            },
            'TRANSPOSE_REQUIRES_ASSIGNMENT': {
                'message': (
                    "transpose() возвращает значение — "
                    "результат нужно сохранить."
                ),
                'wrong': 'transpose(m)',
                'right': 'r = transpose(m)',
                'explanation': (
                    "transpose НЕ изменяет исходную матрицу.\n"
                    "Он ВОЗВРАЩАЕТ НОВУЮ.\n"
                    "\n"
                    "Правильно:\n"
                    "  r = transpose(m)      — в новую переменную\n"
                    "  m = transpose(m)      — мутация"
                ),
                'variants': [
                    'r = transpose(m)',
                    'm = transpose(m)',
                ],
            },
        },
    },
}


EN = {
    'transpose': {
        'name': 'transpose',
        'category': 'create',
        'signature': 'transpose(matrix)',
        'description': (
            'Transpose a matrix: rows ↔ columns.\n'
            '  • Was R×C → became C×R.\n'
            '  • Returns a NEW matrix — save the result.\n'
            '  ⚠️  Works only with Matrix (RAM), not with BigData (DuckDB).'
        ),
        'examples': [
            'r = transpose(m)',
            'm = transpose(m)',
        ],
        'errors': {
            'TRANSPOSE_BAD_SYNTAX': {
                'message': (
                    "transpose: invalid syntax.\n"
                    "  Need a matrix or vector."
                ),
                'wrong': 'transpose()',
                'right': 'transpose(m)',
                'explanation': (
                    "transpose takes ONE argument — a matrix.\n"
                    "\n"
                    "Structure:\n"
                    "  transpose(matrix)\n"
                    "  transpose(vector)"
                ),
                'variants': [
                    'r = transpose(m)',
                    'm = transpose(m)',
                ],
            },
            'TRANSPOSE_NOT_MATRIX': {
                'message': (
                    "transpose: matrix or vector expected."
                ),
                'wrong': 'transpose(42)',
                'right': 'transpose(m)',
                'explanation': (
                    "transpose works only with 2D matrices\n"
                    "and vectors.\n"
                    "\n"
                    "Неправильно: transpose(42)\n"
                    "Неправильно: transpose(\"text\")\n"
                    "Правильно: transpose(m)\n"
                    "Правильно: transpose(v)"
                ),
                'variants': [
                    'r = transpose(m)',
                    'r = transpose(v)',
                ],
            },
            'TRANSPOSE_DUCKDB': {
                'message': (
                    "transpose works only with Matrix (RAM), "
                    "not with BigData (DuckDB).\n"
                    "  BigData is a read-only view on a file."
                ),
                'wrong': 'r = transpose(bd)',
                'right': (
                    'm = ToMatrix(bd)\n'
                    'r = transpose(m)'
                ),
                'explanation': (
                    "BigData (DuckDB) is a read-only view on a file.\n"
                    "It does NOT support transposition.\n"
                    "\n"
                    "Solution:\n"
                    "  1. Convert BigData to Matrix:\n"
                    "        m = ToMatrix(bd)\n"
                    "        r = transpose(m)\n"
                    "\n"
                    "  2. Work directly with Matrix."
                ),
                'variants': [
                    'm = ToMatrix(bd)\nr = transpose(m)',
                    'm = ToMatrix(bd)\nm = transpose(m)',
                ],
            },
            'TRANSPOSE_REQUIRES_ASSIGNMENT': {
                'message': (
                    "transpose() returns a value — "
                    "the result must be saved."
                ),
                'wrong': 'transpose(m)',
                'right': 'r = transpose(m)',
                'explanation': (
                    "transpose does NOT modify the source matrix.\n"
                    "It RETURNS a NEW one.\n"
                    "\n"
                    "Correct:\n"
                    "  r = transpose(m)      — to a new variable\n"
                    "  m = transpose(m)      — mutation"
                ),
                'variants': [
                    'r = transpose(m)',
                    'm = transpose(m)',
                ],
            },
        },
    },
}