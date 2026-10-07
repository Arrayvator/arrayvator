# errors/functions_db/create.py
"""
База ошибок для функций создания матриц, векторов и последовательностей:
    matrix, vector, zeros, ones, fill, range, Number.

СИНТАКСИС:
    matrix(R, C)                    — матрица R×C из None
    vector(N)                       — вектор из N элементов None
    zeros(R [, C])                  — матрица/вектор с нулями
    ones(R [, C])                   — матрица/вектор с единицами
    fill(матрица, значение)         — заполнить матрицу
    range(N) | range(a:b) | range(a:b, step S)  — числовая последовательность
    Number(...)                     — то же, что range

ПРАВИЛА:
    - range / Number работают ТОЛЬКО в присваивании.
    - Оба конца диапазона ВКЛЮЧИТЕЛЬНО.
    - step может быть отрицательным (обратный порядок).
"""


RU = {
    # ============================================================
    # MATRIX — создание матрицы R×C
    # ============================================================
    'matrix': {
        'name': 'matrix',
        'category': 'create',
        'signature': 'matrix(R, C)',
        'description': (
            'Создаёт матрицу R×C из None.\n'
            '  • R — количество строк\n'
            '  • C — количество столбцов\n'
            '  • Оба аргумента обязательны.\n'
            '  • Все ячейки заполнены None.\n'
            '  • R и C — целые числа >= 0.'
        ),
        'examples': [
            'm = matrix(3, 3)',
            'm = matrix(2, 5)',
            'm = matrix(0, 0)      # пустая',
        ],
        'errors': {
            'MATRIX_BAD_SYNTAX': {
                'message': (
                    "matrix: неверный синтаксис.\n"
                    "  Нужны ДВА аргумента: строки и столбцы."
                ),
                'wrong': 'matrix(3)',
                'right': 'matrix(3, 3)',
                'explanation': (
                    "matrix принимает РОВНО ДВА аргумента:\n"
                    "  1. R — количество строк\n"
                    "  2. C — количество столбцов\n"
                    "\n"
                    "Неправильно:\n"
                    "     matrix(3)\n"
                    "     matrix()\n"
                    "     matrix(3, 3, 3)\n"
                    "\n"
                    "Правильно:\n"
                    "     matrix(3, 3)         # 3 строки × 3 столбца\n"
                    "     matrix(2, 5)\n"
                    "     matrix(0, 0)         # пустая"
                ),
                'variants': [
                    'm = matrix(3, 3)',
                    'm = matrix(2, 5)',
                    'm = matrix(0, 0)',
                ],
            },
            'MATRIX_BAD_ROWS': {
                'message': (
                    "matrix: количество строк должно быть числом >= 0."
                ),
                'wrong': 'matrix("3", 3)',
                'right': 'matrix(3, 3)',
                'explanation': (
                    "R — ЧИСЛО без кавычек:\n"
                    "     matrix(3, 3)\n"
                    "     matrix(5, 2)\n"
                    "\n"
                    "Неправильно:\n"
                    "     matrix(\"3\", 3)\n"
                    "\n"
                    "Правильно:\n"
                    "     matrix(3, 3)"
                ),
                'variants': [
                    'm = matrix(3, 3)',
                    'm = matrix(5, 2)',
                ],
            },
            'MATRIX_BAD_COLS': {
                'message': (
                    "matrix: количество столбцов должно быть числом >= 0."
                ),
                'wrong': 'matrix(3, "3")',
                'right': 'matrix(3, 3)',
                'explanation': (
                    "C — ЧИСЛО без кавычек:\n"
                    "     matrix(3, 3)\n"
                    "     matrix(5, 2)\n"
                    "\n"
                    "Неправильно:\n"
                    "     matrix(3, \"3\")\n"
                    "\n"
                    "Правильно:\n"
                    "     matrix(3, 3)"
                ),
                'variants': [
                    'm = matrix(3, 3)',
                    'm = matrix(5, 2)',
                ],
            },
            'MATRIX_NEGATIVE': {
                'message': (
                    "matrix: количество не может быть отрицательным."
                ),
                'wrong': 'matrix(-1, 3)',
                'right': 'matrix(3, 3)',
                'explanation': (
                    "R и C — целые числа >= 0.\n"
                    "\n"
                    "Неправильно:\n"
                    "     matrix(-1, 3)\n"
                    "     matrix(3, -2)\n"
                    "\n"
                    "Правильно:\n"
                    "     matrix(3, 3)\n"
                    "     matrix(0, 0)         # пустая"
                ),
                'variants': [
                    'm = matrix(3, 3)',
                    'm = matrix(0, 0)',
                ],
            },
        },
    },

    # ============================================================
    # VECTOR — создание вектора
    # ============================================================
    'vector': {
        'name': 'vector',
        'category': 'create',
        'signature': 'vector(N)',
        'description': (
            'Создаёт вектор из N элементов None.\n'
            '  • N — целое число >= 0.\n'
            '  • Возвращает вектор (1D).'
        ),
        'examples': [
            'v = vector(5)',
            'v = vector(0)      # пустой',
        ],
        'errors': {
            'VECTOR_BAD_SYNTAX': {
                'message': (
                    "vector: неверный синтаксис.\n"
                    "  Нужен ОДИН аргумент — размер."
                ),
                'wrong': 'vector()',
                'right': 'vector(5)',
                'explanation': (
                    "vector принимает РОВНО ОДИН аргумент:\n"
                    "  N — размер вектора (целое >= 0)\n"
                    "\n"
                    "Неправильно:\n"
                    "     vector()\n"
                    "     vector(3, 5)\n"
                    "\n"
                    "Правильно:\n"
                    "     vector(5)         # [None, None, None, None, None]\n"
                    "     vector(0)         # []"
                ),
                'variants': [
                    'v = vector(5)',
                    'v = vector(0)',
                ],
            },
            'VECTOR_BAD_SIZE': {
                'message': (
                    "vector: размер должен быть числом >= 0."
                ),
                'wrong': 'vector("5")',
                'right': 'vector(5)',
                'explanation': (
                    "N — ЧИСЛО без кавычек:\n"
                    "     vector(5)\n"
                    "     vector(10)\n"
                    "\n"
                    "Неправильно:\n"
                    "     vector(\"5\")\n"
                    "\n"
                    "Правильно:\n"
                    "     vector(5)"
                ),
                'variants': [
                    'v = vector(5)',
                    'v = vector(10)',
                ],
            },
            'VECTOR_NEGATIVE': {
                'message': (
                    "vector: размер не может быть отрицательным."
                ),
                'wrong': 'vector(-3)',
                'right': 'vector(3)',
                'explanation': (
                    "N — целое число >= 0.\n"
                    "\n"
                    "Неправильно:\n"
                    "     vector(-3)\n"
                    "\n"
                    "Правильно:\n"
                    "     vector(3)\n"
                    "     vector(0)         # пустой"
                ),
                'variants': [
                    'v = vector(3)',
                    'v = vector(0)',
                ],
            },
        },
    },

    # ============================================================
    # ZEROS — матрица/вектор из нулей
    # ============================================================
    'zeros': {
        'name': 'zeros',
        'category': 'create',
        'signature': 'zeros(R [, C])',
        'description': (
            'Создаёт матрицу или вектор с нулями.\n'
            '  • zeros(R, C) → матрица R×C из нулей\n'
            '  • zeros(N)    → вектор из N нулей\n'
            '  • Оба аргумента — целые >= 0.'
        ),
        'examples': [
            'm = zeros(3, 3)',
            'v = zeros(5)',
        ],
        'errors': {
            'ZEROS_BAD_SYNTAX': {
                'message': (
                    "zeros: неверный синтаксис.\n"
                    "  Нужен 1 или 2 аргумента."
                ),
                'wrong': 'zeros()',
                'right': 'zeros(3, 3)',
                'explanation': (
                    "zeros принимает 1 или 2 аргумента:\n"
                    "     zeros(R, C)        # матрица R×C из нулей\n"
                    "     zeros(N)           # вектор из N нулей\n"
                    "\n"
                    "Неправильно:\n"
                    "     zeros()\n"
                    "     zeros(3, 3, 3)\n"
                    "\n"
                    "Правильно:\n"
                    "     zeros(3, 3)        # матрица 3×3\n"
                    "     zeros(5)           # вектор из 5 нулей"
                ),
                'variants': [
                    'm = zeros(3, 3)',
                    'v = zeros(5)',
                ],
            },
            'ZEROS_BAD_ARGS': {
                'message': (
                    "zeros: аргументы должны быть числами >= 0."
                ),
                'wrong': 'zeros("3", 3)',
                'right': 'zeros(3, 3)',
                'explanation': (
                    "Все аргументы — ЧИСЛА без кавычек:\n"
                    "     zeros(3, 3)\n"
                    "     zeros(5)\n"
                    "\n"
                    "Неправильно:\n"
                    "     zeros(\"3\", 3)\n"
                    "\n"
                    "Правильно:\n"
                    "     zeros(3, 3)"
                ),
                'variants': [
                    'm = zeros(3, 3)',
                    'v = zeros(5)',
                ],
            },
        },
    },

    # ============================================================
    # ONES — матрица/вектор из единиц
    # ============================================================
    'ones': {
        'name': 'ones',
        'category': 'create',
        'signature': 'ones(R [, C])',
        'description': (
            'Создаёт матрицу или вектор с единицами.\n'
            '  • ones(R, C) → матрица R×C из единиц\n'
            '  • ones(N)    → вектор из N единиц\n'
            '  • Оба аргумента — целые >= 0.'
        ),
        'examples': [
            'm = ones(3, 3)',
            'v = ones(5)',
        ],
        'errors': {
            'ONES_BAD_SYNTAX': {
                'message': (
                    "ones: неверный синтаксис.\n"
                    "  Нужен 1 или 2 аргумента."
                ),
                'wrong': 'ones()',
                'right': 'ones(3, 3)',
                'explanation': (
                    "ones принимает 1 или 2 аргумента:\n"
                    "     ones(R, C)         # матрица R×C из единиц\n"
                    "     ones(N)            # вектор из N единиц\n"
                    "\n"
                    "Неправильно:\n"
                    "     ones()\n"
                    "     ones(3, 3, 3)\n"
                    "\n"
                    "Правильно:\n"
                    "     ones(3, 3)\n"
                    "     ones(5)"
                ),
                'variants': [
                    'm = ones(3, 3)',
                    'v = ones(5)',
                ],
            },
            'ONES_BAD_ARGS': {
                'message': (
                    "ones: аргументы должны быть числами >= 0."
                ),
                'wrong': 'ones("3", 3)',
                'right': 'ones(3, 3)',
                'explanation': (
                    "Все аргументы — ЧИСЛА без кавычек:\n"
                    "     ones(3, 3)\n"
                    "     ones(5)\n"
                    "\n"
                    "Правильно:\n"
                    "     ones(3, 3)"
                ),
                'variants': [
                    'm = ones(3, 3)',
                    'v = ones(5)',
                ],
            },
        },
    },

    # ============================================================
    # FILL — заполнение матрицы
    # ============================================================
    'fill': {
        'name': 'fill',
        'category': 'create',
        'signature': 'fill(матрица, значение)',
        'description': (
            'Заполняет матрицу указанным значением.\n'
            '  • Работает с матрицей и вектором.\n'
            '  • Заменяет ВСЕ ячейки.\n'
            '  • Возвращает НОВУЮ матрицу — результат нужно сохранить.'
        ),
        'examples': [
            'm = fill(m, 0)',
            'm = fill(m, "—")',
            'v = fill(v, 42)',
        ],
        'errors': {
            'FILL_BAD_SYNTAX': {
                'message': (
                    "fill: неверный синтаксис.\n"
                    "  Нужны матрица и значение."
                ),
                'wrong': 'fill(m)',
                'right': 'fill(m, 0)',
                'explanation': (
                    "fill принимает ДВА аргумента:\n"
                    "  1. матрица или вектор\n"
                    "  2. значение для заполнения\n"
                    "\n"
                    "Неправильно:\n"
                    "     fill(m)\n"
                    "\n"
                    "Правильно:\n"
                    "     fill(m, 0)\n"
                    '     fill(m, "—")\n'
                    "     fill(v, 42)"
                ),
                'variants': [
                    'm = fill(m, 0)',
                    'm = fill(m, "—")',
                    'v = fill(v, 42)',
                ],
            },
            'FILL_REQUIRES_ASSIGNMENT': {
                'message': (
                    "fill() возвращает значение — "
                    "результат нужно сохранить."
                ),
                'wrong': 'fill(m, 0)',
                'right': 'm = fill(m, 0)',
                'explanation': (
                    "fill НЕ изменяет исходную матрицу.\n"
                    "Он ВОЗВРАЩАЕТ НОВУЮ.\n"
                    "\n"
                    "Правильно:\n"
                    "  r = fill(m, 0)      — в новую переменную\n"
                    "  m = fill(m, 0)      — мутация"
                ),
                'variants': [
                    'r = fill(m, 0)',
                    'm = fill(m, 0)',
                ],
            },
        },
    },

    # ============================================================
    # RANGE — числовая последовательность
    # ============================================================
    'range': {
        'name': 'range',
        'category': 'create',
        'signature': 'range(N) | range(a:b) | range(a:b, step S)',
        'description': (
            'Числовая последовательность.\n'
            '  • range(N)          → [1, 2, ..., N]\n'
            '  • range(end)        → [1, ..., длина среза]\n'
            '  • range(2:end)      → [2, ..., длина среза]\n'
            '  • range(a:b)        → [a, ..., b]\n'
            '  • range(a:b, step S) → с шагом S\n'
            '  • Оба конца ВКЛЮЧИТЕЛЬНО.\n'
            '  • step 0 → ошибка.\n'
            '  • Работает только в ПРИСВАИВАНИИ.'
        ),
        'examples': [
            'm = matrix(5, 1)',
            'm[:, 1] = range(5)              # [1,2,3,4,5]',
            'm[:, 1] = range(1:5)            # [1,2,3,4,5]',
            'm[:, 1] = range(1:10, step 2)   # [1,3,5,7,9]',
            'm[:, 1] = range(10:1, step -1)  # [10,9,...,1]',
            'm[2:end, 1] = range(2:end)',
        ],
        'errors': {
            'RANGE_BAD_SYNTAX': {
                'message': (
                    "range: неверный синтаксис.\n"
                    "  Нужно N или диапазон a:b."
                ),
                'wrong': 'range()',
                'right': 'range(5)',
                'explanation': (
                    "range принимает:\n"
                    "     range(N)              # [1, 2, ..., N]\n"
                    "     range(a:b)            # [a, ..., b]\n"
                    "     range(a:b, step S)    # с шагом S\n"
                    "\n"
                    "Неправильно:\n"
                    "     range()\n"
                    "     range(1, 5)\n"
                    "\n"
                    "Правильно:\n"
                    "     range(5)\n"
                    "     range(1:5)\n"
                    "     range(1:10, step 2)"
                ),
                'variants': [
                    'm[:, 1] = range(5)',
                    'm[:, 1] = range(1:5)',
                    'm[:, 1] = range(1:10, step 2)',
                ],
            },
            'RANGE_ZERO_STEP': {
                'message': (
                    "range: step не может быть 0."
                ),
                'wrong': 'range(1:10, step 0)',
                'right': 'range(1:10, step 1)',
                'explanation': (
                    "step 0 — бесконечный цикл. Запрещено.\n"
                    "\n"
                    "Неправильно:\n"
                    "     range(1:10, step 0)\n"
                    "\n"
                    "Правильно:\n"
                    "     range(1:10)             # шаг 1\n"
                    "     range(1:10, step 2)\n"
                    "     range(10:1, step -1)"
                ),
                'variants': [
                    'm[:, 1] = range(1:10)',
                    'm[:, 1] = range(1:10, step 2)',
                ],
            },
            'RANGE_WRONG_STEP_SIGN': {
                'message': (
                    "range: знак step должен соответствовать направлению.\n"
                    "  a <= b → step > 0; a > b → step < 0."
                ),
                'wrong': 'range(1:10, step -1)',
                'right': 'range(1:10, step 1)',
                'explanation': (
                    "Правила:\n"
                    "  • Если начало < конца → step > 0\n"
                    "  • Если начало > конца → step < 0\n"
                    "\n"
                    "Неправильно:\n"
                    "     range(1:10, step -1)\n"
                    "     range(10:1, step 1)\n"
                    "\n"
                    "Правильно:\n"
                    "     range(1:10, step 2)      # вверх\n"
                    "     range(10:1, step -2)     # вниз"
                ),
                'variants': [
                    'm[:, 1] = range(1:10, step 2)',
                    'm[:, 1] = range(10:1, step -2)',
                ],
            },
            'RANGE_REQUIRES_ASSIGNMENT': {
                'message': (
                    "range() можно использовать только в присваивании.\n"
                    "  Например: m[:, 1] = range(5)"
                ),
                'wrong': 'print(range(5))',
                'right': 'm[:, 1] = range(5)\nprint(m[:, 1])',
                'explanation': (
                    "range — последовательность, а не значение.\n"
                    "Её нужно куда-то положить.\n"
                    "\n"
                    "Неправильно:\n"
                    "     print(range(5))\n"
                    "\n"
                    "Правильно:\n"
                    "     m = matrix(5, 1)\n"
                    "     m[:, 1] = range(5)\n"
                    "     print(m[:, 1])"
                ),
                'variants': [
                    'm = matrix(5, 1)\nm[:, 1] = range(5)',
                    'm = matrix(10, 1)\nm[:, 1] = range(1:10, step 2)',
                ],
            },
        },
    },

    # ============================================================
    # NUMBER (синоним range)
    # ============================================================
    'Number': {
        'name': 'Number',
        'category': 'create',
        'signature': 'Number(N) | Number(a:b) | Number(a:b, step S)',
        'description': (
            'То же, что range.\n'
            '  • Number(N)          → [1, 2, ..., N]\n'
            '  • Number(a:b)        → [a, ..., b]\n'
            '  • Number(a:b, step S) → с шагом S\n'
            '  • Работает только в ПРИСВАИВАНИИ.'
        ),
        'examples': [
            'm = matrix(41, 1)',
            'm[:, 1] = Number(-10:10, step 0.5)',
        ],
        'errors': {
            'NUMBER_BAD_SYNTAX': {
                'message': (
                    "Number: неверный синтаксис.\n"
                    "  Нужно N или диапазон a:b."
                ),
                'wrong': 'Number()',
                'right': 'Number(5)',
                'explanation': (
                    "Number — синоним range:\n"
                    "     Number(N)\n"
                    "     Number(a:b)\n"
                    "     Number(a:b, step S)\n"
                    "\n"
                    "Правильно:\n"
                    "     m[:, 1] = Number(5)\n"
                    "     m[:, 1] = Number(1:10, step 0.5)"
                ),
                'variants': [
                    'm[:, 1] = Number(5)',
                    'm[:, 1] = Number(1:10, step 0.5)',
                ],
            },
            'NUMBER_ZERO_STEP': {
                'message': "Number: step не может быть 0.",
                'wrong': 'Number(1:10, step 0)',
                'right': 'Number(1:10, step 1)',
                'explanation': (
                    "step 0 запрещён — бесконечный цикл.\n"
                    "\n"
                    "Правильно:\n"
                    "     Number(1:10)\n"
                    "     Number(1:10, step 2)"
                ),
                'variants': [
                    'm[:, 1] = Number(1:10)',
                    'm[:, 1] = Number(1:10, step 2)',
                ],
            },
        },
    },
}


EN = {
    # ============================================================
    # MATRIX
    # ============================================================
    'matrix': {
        'name': 'matrix',
        'category': 'create',
        'signature': 'matrix(R, C)',
        'description': (
            'Creates an R×C matrix filled with None.\n'
            '  • R — number of rows\n'
            '  • C — number of columns\n'
            '  • Both arguments are required.\n'
            '  • All cells are None.\n'
            '  • R and C — integers >= 0.'
        ),
        'examples': [
            'm = matrix(3, 3)',
            'm = matrix(2, 5)',
            'm = matrix(0, 0)      # empty',
        ],
        'errors': {
            'MATRIX_BAD_SYNTAX': {
                'message': (
                    "matrix: invalid syntax.\n"
                    "  TWO arguments required: rows and columns."
                ),
                'wrong': 'matrix(3)',
                'right': 'matrix(3, 3)',
                'explanation': (
                    "matrix takes EXACTLY TWO arguments:\n"
                    "  1. R — number of rows\n"
                    "  2. C — number of columns\n"
                    "\n"
                    "Incorrect:\n"
                    "     matrix(3)\n"
                    "     matrix()\n"
                    "     matrix(3, 3, 3)\n"
                    "\n"
                    "Correct:\n"
                    "     matrix(3, 3)\n"
                    "     matrix(2, 5)\n"
                    "     matrix(0, 0)         # empty"
                ),
                'variants': [
                    'm = matrix(3, 3)',
                    'm = matrix(2, 5)',
                    'm = matrix(0, 0)',
                ],
            },
            'MATRIX_BAD_ROWS': {
                'message': (
                    "matrix: number of rows must be a number >= 0."
                ),
                'wrong': 'matrix("3", 3)',
                'right': 'matrix(3, 3)',
                'explanation': (
                    "R — a NUMBER without quotes:\n"
                    "     matrix(3, 3)\n"
                    "     matrix(5, 2)\n"
                    "\n"
                    "Correct:\n"
                    "     matrix(3, 3)"
                ),
                'variants': [
                    'm = matrix(3, 3)',
                    'm = matrix(5, 2)',
                ],
            },
            'MATRIX_BAD_COLS': {
                'message': (
                    "matrix: number of columns must be a number >= 0."
                ),
                'wrong': 'matrix(3, "3")',
                'right': 'matrix(3, 3)',
                'explanation': (
                    "C — a NUMBER without quotes:\n"
                    "     matrix(3, 3)\n"
                    "     matrix(5, 2)\n"
                    "\n"
                    "Correct:\n"
                    "     matrix(3, 3)"
                ),
                'variants': [
                    'm = matrix(3, 3)',
                    'm = matrix(5, 2)',
                ],
            },
            'MATRIX_NEGATIVE': {
                'message': (
                    "matrix: count cannot be negative."
                ),
                'wrong': 'matrix(-1, 3)',
                'right': 'matrix(3, 3)',
                'explanation': (
                    "R and C — integers >= 0.\n"
                    "\n"
                    "Incorrect:\n"
                    "     matrix(-1, 3)\n"
                    "     matrix(3, -2)\n"
                    "\n"
                    "Correct:\n"
                    "     matrix(3, 3)\n"
                    "     matrix(0, 0)         # empty"
                ),
                'variants': [
                    'm = matrix(3, 3)',
                    'm = matrix(0, 0)',
                ],
            },
        },
    },

    # ============================================================
    # VECTOR
    # ============================================================
    'vector': {
        'name': 'vector',
        'category': 'create',
        'signature': 'vector(N)',
        'description': (
            'Creates a vector of N None values.\n'
            '  • N — integer >= 0.\n'
            '  • Returns a vector (1D).'
        ),
        'examples': [
            'v = vector(5)',
            'v = vector(0)      # empty',
        ],
        'errors': {
            'VECTOR_BAD_SYNTAX': {
                'message': (
                    "vector: invalid syntax.\n"
                    "  Need ONE argument — size."
                ),
                'wrong': 'vector()',
                'right': 'vector(5)',
                'explanation': (
                    "vector takes EXACTLY ONE argument:\n"
                    "  N — vector size (integer >= 0)\n"
                    "\n"
                    "Incorrect:\n"
                    "     vector()\n"
                    "     vector(3, 5)\n"
                    "\n"
                    "Correct:\n"
                    "     vector(5)         # [None, None, None, None, None]\n"
                    "     vector(0)         # []"
                ),
                'variants': [
                    'v = vector(5)',
                    'v = vector(0)',
                ],
            },
            'VECTOR_BAD_SIZE': {
                'message': (
                    "vector: size must be a number >= 0."
                ),
                'wrong': 'vector("5")',
                'right': 'vector(5)',
                'explanation': (
                    "N — a NUMBER without quotes:\n"
                    "     vector(5)\n"
                    "     vector(10)\n"
                    "\n"
                    "Correct:\n"
                    "     vector(5)"
                ),
                'variants': [
                    'v = vector(5)',
                    'v = vector(10)',
                ],
            },
            'VECTOR_NEGATIVE': {
                'message': (
                    "vector: size cannot be negative."
                ),
                'wrong': 'vector(-3)',
                'right': 'vector(3)',
                'explanation': (
                    "N — integer >= 0.\n"
                    "\n"
                    "Incorrect:\n"
                    "     vector(-3)\n"
                    "\n"
                    "Correct:\n"
                    "     vector(3)\n"
                    "     vector(0)         # empty"
                ),
                'variants': [
                    'v = vector(3)',
                    'v = vector(0)',
                ],
            },
        },
    },

    # ============================================================
    # ZEROS
    # ============================================================
    'zeros': {
        'name': 'zeros',
        'category': 'create',
        'signature': 'zeros(R [, C])',
        'description': (
            'Creates a matrix or vector filled with zeros.\n'
            '  • zeros(R, C) → R×C matrix of zeros\n'
            '  • zeros(N)    → vector of N zeros\n'
            '  • Both arguments — integers >= 0.'
        ),
        'examples': [
            'm = zeros(3, 3)',
            'v = zeros(5)',
        ],
        'errors': {
            'ZEROS_BAD_SYNTAX': {
                'message': (
                    "zeros: invalid syntax.\n"
                    "  Need 1 or 2 arguments."
                ),
                'wrong': 'zeros()',
                'right': 'zeros(3, 3)',
                'explanation': (
                    "zeros takes 1 or 2 arguments:\n"
                    "     zeros(R, C)        # R×C matrix of zeros\n"
                    "     zeros(N)           # vector of N zeros\n"
                    "\n"
                    "Incorrect:\n"
                    "     zeros()\n"
                    "     zeros(3, 3, 3)\n"
                    "\n"
                    "Correct:\n"
                    "     zeros(3, 3)\n"
                    "     zeros(5)"
                ),
                'variants': [
                    'm = zeros(3, 3)',
                    'v = zeros(5)',
                ],
            },
            'ZEROS_BAD_ARGS': {
                'message': (
                    "zeros: arguments must be numbers >= 0."
                ),
                'wrong': 'zeros("3", 3)',
                'right': 'zeros(3, 3)',
                'explanation': (
                    "All arguments — NUMBERS without quotes:\n"
                    "     zeros(3, 3)\n"
                    "     zeros(5)\n"
                    "\n"
                    "Correct:\n"
                    "     zeros(3, 3)"
                ),
                'variants': [
                    'm = zeros(3, 3)',
                    'v = zeros(5)',
                ],
            },
        },
    },

    # ============================================================
    # ONES
    # ============================================================
    'ones': {
        'name': 'ones',
        'category': 'create',
        'signature': 'ones(R [, C])',
        'description': (
            'Creates a matrix or vector filled with ones.\n'
            '  • ones(R, C) → R×C matrix of ones\n'
            '  • ones(N)    → vector of N ones\n'
            '  • Both arguments — integers >= 0.'
        ),
        'examples': [
            'm = ones(3, 3)',
            'v = ones(5)',
        ],
        'errors': {
            'ONES_BAD_SYNTAX': {
                'message': (
                    "ones: invalid syntax.\n"
                    "  Need 1 or 2 arguments."
                ),
                'wrong': 'ones()',
                'right': 'ones(3, 3)',
                'explanation': (
                    "ones takes 1 or 2 arguments:\n"
                    "     ones(R, C)         # R×C matrix of ones\n"
                    "     ones(N)            # vector of N ones\n"
                    "\n"
                    "Incorrect:\n"
                    "     ones()\n"
                    "     ones(3, 3, 3)\n"
                    "\n"
                    "Correct:\n"
                    "     ones(3, 3)\n"
                    "     ones(5)"
                ),
                'variants': [
                    'm = ones(3, 3)',
                    'v = ones(5)',
                ],
            },
            'ONES_BAD_ARGS': {
                'message': (
                    "ones: arguments must be numbers >= 0."
                ),
                'wrong': 'ones("3", 3)',
                'right': 'ones(3, 3)',
                'explanation': (
                    "All arguments — NUMBERS without quotes.\n"
                    "\n"
                    "Correct:\n"
                    "     ones(3, 3)"
                ),
                'variants': [
                    'm = ones(3, 3)',
                    'v = ones(5)',
                ],
            },
        },
    },

    # ============================================================
    # FILL
    # ============================================================
    'fill': {
        'name': 'fill',
        'category': 'create',
        'signature': 'fill(matrix, value)',
        'description': (
            'Fills a matrix with the given value.\n'
            '  • Works with a matrix and a vector.\n'
            '  • Replaces ALL cells.\n'
            '  • Returns a NEW matrix — save the result.'
        ),
        'examples': [
            'm = fill(m, 0)',
            'm = fill(m, "-")',
            'v = fill(v, 42)',
        ],
        'errors': {
            'FILL_BAD_SYNTAX': {
                'message': (
                    "fill: invalid syntax.\n"
                    "  Need a matrix and a value."
                ),
                'wrong': 'fill(m)',
                'right': 'fill(m, 0)',
                'explanation': (
                    "fill takes TWO arguments:\n"
                    "  1. matrix or vector\n"
                    "  2. value to fill with\n"
                    "\n"
                    "Incorrect:\n"
                    "     fill(m)\n"
                    "\n"
                    "Correct:\n"
                    "     fill(m, 0)\n"
                    '     fill(m, "-")\n'
                    "     fill(v, 42)"
                ),
                'variants': [
                    'm = fill(m, 0)',
                    'm = fill(m, "-")',
                    'v = fill(v, 42)',
                ],
            },
            'FILL_REQUIRES_ASSIGNMENT': {
                'message': (
                    "fill() returns a value — "
                    "the result must be saved."
                ),
                'wrong': 'fill(m, 0)',
                'right': 'm = fill(m, 0)',
                'explanation': (
                    "fill does NOT modify the source matrix.\n"
                    "It RETURNS a NEW one.\n"
                    "\n"
                    "Correct:\n"
                    "  r = fill(m, 0)      — to a new variable\n"
                    "  m = fill(m, 0)      — mutation"
                ),
                'variants': [
                    'r = fill(m, 0)',
                    'm = fill(m, 0)',
                ],
            },
        },
    },

    # ============================================================
    # RANGE
    # ============================================================
    'range': {
        'name': 'range',
        'category': 'create',
        'signature': 'range(N) | range(a:b) | range(a:b, step S)',
        'description': (
            'Numeric sequence.\n'
            '  • range(N)          → [1, 2, ..., N]\n'
            '  • range(end)        → [1, ..., slice length]\n'
            '  • range(2:end)      → [2, ..., slice length]\n'
            '  • range(a:b)        → [a, ..., b]\n'
            '  • range(a:b, step S) → with step S\n'
            '  • Both ends INCLUSIVE.\n'
            '  • step 0 → error.\n'
            '  • Works ONLY in assignment.'
        ),
        'examples': [
            'm = matrix(5, 1)',
            'm[:, 1] = range(5)              # [1,2,3,4,5]',
            'm[:, 1] = range(1:5)            # [1,2,3,4,5]',
            'm[:, 1] = range(1:10, step 2)   # [1,3,5,7,9]',
            'm[:, 1] = range(10:1, step -1)  # [10,9,...,1]',
            'm[2:end, 1] = range(2:end)',
        ],
        'errors': {
            'RANGE_BAD_SYNTAX': {
                'message': (
                    "range: invalid syntax.\n"
                    "  Need N or a range a:b."
                ),
                'wrong': 'range()',
                'right': 'range(5)',
                'explanation': (
                    "range takes:\n"
                    "     range(N)              # [1, 2, ..., N]\n"
                    "     range(a:b)            # [a, ..., b]\n"
                    "     range(a:b, step S)    # with step S\n"
                    "\n"
                    "Incorrect:\n"
                    "     range()\n"
                    "     range(1, 5)\n"
                    "\n"
                    "Correct:\n"
                    "     range(5)\n"
                    "     range(1:5)\n"
                    "     range(1:10, step 2)"
                ),
                'variants': [
                    'm[:, 1] = range(5)',
                    'm[:, 1] = range(1:5)',
                    'm[:, 1] = range(1:10, step 2)',
                ],
            },
            'RANGE_ZERO_STEP': {
                'message': (
                    "range: step cannot be 0."
                ),
                'wrong': 'range(1:10, step 0)',
                'right': 'range(1:10, step 1)',
                'explanation': (
                    "step 0 — infinite loop. Forbidden.\n"
                    "\n"
                    "Incorrect:\n"
                    "     range(1:10, step 0)\n"
                    "\n"
                    "Correct:\n"
                    "     range(1:10)             # step 1\n"
                    "     range(1:10, step 2)\n"
                    "     range(10:1, step -1)"
                ),
                'variants': [
                    'm[:, 1] = range(1:10)',
                    'm[:, 1] = range(1:10, step 2)',
                ],
            },
            'RANGE_WRONG_STEP_SIGN': {
                'message': (
                    "range: sign of step must match direction.\n"
                    "  a <= b → step > 0; a > b → step < 0."
                ),
                'wrong': 'range(1:10, step -1)',
                'right': 'range(1:10, step 1)',
                'explanation': (
                    "Rules:\n"
                    "  • If start < end → step > 0\n"
                    "  • If start > end → step < 0\n"
                    "\n"
                    "Incorrect:\n"
                    "     range(1:10, step -1)\n"
                    "     range(10:1, step 1)\n"
                    "\n"
                    "Correct:\n"
                    "     range(1:10, step 2)      # up\n"
                    "     range(10:1, step -2)     # down"
                ),
                'variants': [
                    'm[:, 1] = range(1:10, step 2)',
                    'm[:, 1] = range(10:1, step -2)',
                ],
            },
            'RANGE_REQUIRES_ASSIGNMENT': {
                'message': (
                    "range() can only be used in an assignment.\n"
                    "  Example: m[:, 1] = range(5)"
                ),
                'wrong': 'print(range(5))',
                'right': 'm[:, 1] = range(5)\nprint(m[:, 1])',
                'explanation': (
                    "range — a sequence, not a value.\n"
                    "It must be placed somewhere.\n"
                    "\n"
                    "Incorrect:\n"
                    "     print(range(5))\n"
                    "\n"
                    "Correct:\n"
                    "     m = matrix(5, 1)\n"
                    "     m[:, 1] = range(5)\n"
                    "     print(m[:, 1])"
                ),
                'variants': [
                    'm = matrix(5, 1)\nm[:, 1] = range(5)',
                    'm = matrix(10, 1)\nm[:, 1] = range(1:10, step 2)',
                ],
            },
        },
    },

    # ============================================================
    # NUMBER (synonym of range)
    # ============================================================
    'Number': {
        'name': 'Number',
        'category': 'create',
        'signature': 'Number(N) | Number(a:b) | Number(a:b, step S)',
        'description': (
            'Same as range.\n'
            '  • Number(N)          → [1, 2, ..., N]\n'
            '  • Number(a:b)        → [a, ..., b]\n'
            '  • Number(a:b, step S) → with step S\n'
            '  • Works ONLY in assignment.'
        ),
        'examples': [
            'm = matrix(41, 1)',
            'm[:, 1] = Number(-10:10, step 0.5)',
        ],
        'errors': {
            'NUMBER_BAD_SYNTAX': {
                'message': (
                    "Number: invalid syntax.\n"
                    "  Need N or a range a:b."
                ),
                'wrong': 'Number()',
                'right': 'Number(5)',
                'explanation': (
                    "Number is a synonym of range:\n"
                    "     Number(N)\n"
                    "     Number(a:b)\n"
                    "     Number(a:b, step S)\n"
                    "\n"
                    "Correct:\n"
                    "     m[:, 1] = Number(5)\n"
                    "     m[:, 1] = Number(1:10, step 0.5)"
                ),
                'variants': [
                    'm[:, 1] = Number(5)',
                    'm[:, 1] = Number(1:10, step 0.5)',
                ],
            },
            'NUMBER_ZERO_STEP': {
                'message': "Number: step cannot be 0.",
                'wrong': 'Number(1:10, step 0)',
                'right': 'Number(1:10, step 1)',
                'explanation': (
                    "step 0 is forbidden — infinite loop.\n"
                    "\n"
                    "Correct:\n"
                    "     Number(1:10)\n"
                    "     Number(1:10, step 2)"
                ),
                'variants': [
                    'm[:, 1] = Number(1:10)',
                    'm[:, 1] = Number(1:10, step 2)',
                ],
            },
        },
    },
}