# errors/functions_db/random.py
"""
База ошибок для функции RANDOM — генерация случайных чисел.

СИНТАКСИС:
    random(начало:конец, точность)

ПРИМЕРЫ:
    x = random(0:10, 0)              # одно число
    m[all, all] = random(0:10, 0)    # вся матрица
    m[1, all] = random(0:10, 0)      # строка
    m[2:4, 2:4] = random(0:10, 0)    # диапазон

ПРАВИЛА:
    - random() работает ТОЛЬКО в присваивании.
    - Диапазон: начало:конец (оба включительно).
    - Точность: 0 — целые, N > 0 — float с N знаками.
    - Начало < конец обязательно.
    - random() нельзя использовать в print, filterif, sort и др.
"""


RU = {
    'random': {
        'name': 'random',
        'category': 'create',
        'signature': 'random(начало:конец, точность)',
        'description': (
            'Генерирует случайные числа.\n'
            '  • Работает ТОЛЬКО в присваивании.\n'
            '  • диапазон: начало:конец (оба включительно).\n'
            '  • точность: 0 — целые, N > 0 — float с N знаками.\n'
            '  • Каждая ячейка — новое случайное число.\n'
            '  • Начало < конец обязательно.'
        ),
        'examples': [
            'x = random(0:10, 0)              # одно число',
            'm[all, all] = random(0:10, 0)    # вся матрица',
            'm[1, all] = random(0:10, 0)      # строка',
            'm[2:4, 2:4] = random(0:10, 0)    # диапазон',
            'm[:, 1] = random(-5:5, 2)        # float с 2 знаками',
        ],
        'errors': {
            'RANDOM_MISUSE': {
                'message': (
                    "random() нельзя использовать здесь.\n"
                    "  Только в присваивании."
                ),
                'wrong': 'print(random(0:10, 0))',
                'right': 'x = random(0:10, 0)\nprint(x)',
                'explanation': (
                    "random() возвращает ГЕНЕРАТОР, а не число.\n"
                    "Числа создаются только при присваивании.\n"
                    "\n"
                    "Неправильно:\n"
                    "     print(random(0:10, 0))\n"
                    "     filterif(random(0:10, 0) > 5)\n"
                    "     sort(random(0:10, 0), AZ)\n"
                    "\n"
                    "Правильно:\n"
                    "     x = random(0:10, 0)\n"
                    "     print(x)\n"
                    "\n"
                    "     m[all, all] = random(0:10, 0)\n"
                    "     m[1, :] = random(0:10, 0)\n"
                    "     m[2:4, 2:4] = random(0:10, 0)"
                ),
                'variants': [
                    'x = random(0:10, 0)\nprint(x)',
                    'm[all, all] = random(0:10, 0)',
                    'm[1, :] = random(0:10, 0)',
                    'm[2:4, 2:4] = random(0:10, 0)',
                ],
            },
            'RANDOM_BAD_SYNTAX': {
                'message': (
                    "random: неверный синтаксис.\n"
                    "  Нужен диапазон и точность."
                ),
                'wrong': 'random()',
                'right': 'random(0:10, 0)',
                'explanation': (
                    "random принимает ДВА аргумента:\n"
                    "  1. диапазон — начало:конец\n"
                    "  2. точность — 0 для целых, N для float\n"
                    "\n"
                    "Неправильно:\n"
                    "     random()\n"
                    "     random(10)\n"
                    "     random(0:10)\n"
                    "\n"
                    "Правильно:\n"
                    "     random(0:10, 0)         # целые 0..10\n"
                    "     random(0:10, 2)         # float 0.00..10.00\n"
                    "     random(-5:5, 1)         # float -5.0..5.0"
                ),
                'variants': [
                    'x = random(0:10, 0)',
                    'x = random(0:10, 2)',
                    'x = random(-5:5, 1)',
                ],
            },
            'RANDOM_BAD_RANGE': {
                'message': (
                    "random: диапазон указывается через ':'."
                ),
                'wrong': 'random(0, 10, 0)',
                'right': 'random(0:10, 0)',
                'explanation': (
                    "Диапазон — ЧЕРЕЗ ДВОЕТОЧИЕ:\n"
                    "     random(0:10, 0)\n"
                    "     random(-5:5, 2)\n"
                    "\n"
                    "Неправильно:\n"
                    "     random(0, 10, 0)\n"
                    "     random(0 to 10, 0)\n"
                    "\n"
                    "Правильно:\n"
                    "     random(0:10, 0)"
                ),
                'variants': [
                    'x = random(0:10, 0)',
                    'x = random(-5:5, 2)',
                ],
            },
            'RANDOM_BAD_PRECISION': {
                'message': (
                    "random: точность должна быть целым числом >= 0."
                ),
                'wrong': 'random(0:10, "2")',
                'right': 'random(0:10, 2)',
                'explanation': (
                    "Точность — ЧИСЛО без кавычек:\n"
                    "     random(0:10, 0)         # целые\n"
                    "     random(0:10, 2)         # 2 знака\n"
                    "     random(0:10, 4)         # 4 знака\n"
                    "\n"
                    "Неправильно:\n"
                    "     random(0:10, \"2\")\n"
                    "     random(0:10, -1)\n"
                    "\n"
                    "Правильно:\n"
                    "     random(0:10, 2)"
                ),
                'variants': [
                    'x = random(0:10, 0)',
                    'x = random(0:10, 2)',
                ],
            },
            'RANDOM_NEGATIVE_PRECISION': {
                'message': (
                    "random: точность не может быть отрицательной."
                ),
                'wrong': 'random(0:10, -1)',
                'right': 'random(0:10, 0)',
                'explanation': (
                    "Точность — целое число >= 0:\n"
                    "     0  → целые числа\n"
                    "     2  → float с 2 знаками\n"
                    "\n"
                    "Неправильно:\n"
                    "     random(0:10, -1)\n"
                    "\n"
                    "Правильно:\n"
                    "     random(0:10, 0)\n"
                    "     random(0:10, 2)"
                ),
                'variants': [
                    'x = random(0:10, 0)',
                    'x = random(0:10, 2)',
                ],
            },
            'RANDOM_START_GREATER_END': {
                'message': (
                    "random: начало должно быть МЕНЬШЕ конца."
                ),
                'wrong': 'random(10:0, 0)',
                'right': 'random(0:10, 0)',
                'explanation': (
                    "Диапазон указывается от меньшего к большему:\n"
                    "     random(0:10, 0)\n"
                    "     random(-5:5, 2)\n"
                    "\n"
                    "Неправильно:\n"
                    "     random(10:0, 0)\n"
                    "\n"
                    "Правильно:\n"
                    "     random(0:10, 0)"
                ),
                'variants': [
                    'x = random(0:10, 0)',
                    'x = random(-5:5, 2)',
                ],
            },
            'RANDOM_EMPTY_TARGET': {
                'message': (
                    "random: нельзя заполнить пустую матрицу/вектор.\n"
                    "  Сначала создайте матрицу через matrix()."
                ),
                'wrong': (
                    'm = []\n'
                    'm[all, all] = random(0:10, 0)'
                ),
                'right': (
                    'm = matrix(3, 3)\n'
                    'm[all, all] = random(0:10, 0)'
                ),
                'explanation': (
                    "random заполняет СУЩЕСТВУЮЩИЕ ячейки.\n"
                    "Если матрица пуста — неизвестен размер.\n"
                    "\n"
                    "Неправильно:\n"
                    "     m = []\n"
                    "     m[all, all] = random(0:10, 0)\n"
                    "\n"
                    "Правильно:\n"
                    "     m = matrix(3, 3)\n"
                    "     m[all, all] = random(0:10, 0)\n"
                    "\n"
                    "Или через vector:\n"
                    "     v = vector(5)\n"
                    "     v[all] = random(0:10, 0)"
                ),
                'variants': [
                    'm = matrix(3, 3)\nm[all, all] = random(0:10, 0)',
                    'v = vector(5)\nv[all] = random(0:10, 0)',
                ],
            },
        },
    },
}


EN = {
    'random': {
        'name': 'random',
        'category': 'create',
        'signature': 'random(start:end, precision)',
        'description': (
            'Generates random numbers.\n'
            '  • Works ONLY in assignment.\n'
            '  • range: start:end (both inclusive).\n'
            '  • precision: 0 — integers, N > 0 — float with N digits.\n'
            '  • Each cell gets a new random number.\n'
            '  • start < end is required.'
        ),
        'examples': [
            'x = random(0:10, 0)              # single number',
            'm[all, all] = random(0:10, 0)    # whole matrix',
            'm[1, all] = random(0:10, 0)      # row',
            'm[2:4, 2:4] = random(0:10, 0)    # range',
            'm[:, 1] = random(-5:5, 2)        # float with 2 digits',
        ],
        'errors': {
            'RANDOM_MISUSE': {
                'message': (
                    "random() cannot be used here.\n"
                    "  Only in assignment."
                ),
                'wrong': 'print(random(0:10, 0))',
                'right': 'x = random(0:10, 0)\nprint(x)',
                'explanation': (
                    "random() returns a GENERATOR, not a number.\n"
                    "Numbers are created only on assignment.\n"
                    "\n"
                    "Incorrect:\n"
                    "     print(random(0:10, 0))\n"
                    "     filterif(random(0:10, 0) > 5)\n"
                    "     sort(random(0:10, 0), AZ)\n"
                    "\n"
                    "Correct:\n"
                    "     x = random(0:10, 0)\n"
                    "     print(x)\n"
                    "\n"
                    "     m[all, all] = random(0:10, 0)\n"
                    "     m[1, :] = random(0:10, 0)\n"
                    "     m[2:4, 2:4] = random(0:10, 0)"
                ),
                'variants': [
                    'x = random(0:10, 0)\nprint(x)',
                    'm[all, all] = random(0:10, 0)',
                    'm[1, :] = random(0:10, 0)',
                    'm[2:4, 2:4] = random(0:10, 0)',
                ],
            },
            'RANDOM_BAD_SYNTAX': {
                'message': (
                    "random: invalid syntax.\n"
                    "  Need a range and precision."
                ),
                'wrong': 'random()',
                'right': 'random(0:10, 0)',
                'explanation': (
                    "random takes TWO arguments:\n"
                    "  1. range — start:end\n"
                    "  2. precision — 0 for integers, N for float\n"
                    "\n"
                    "Incorrect:\n"
                    "     random()\n"
                    "     random(10)\n"
                    "     random(0:10)\n"
                    "\n"
                    "Correct:\n"
                    "     random(0:10, 0)         # integers 0..10\n"
                    "     random(0:10, 2)         # float 0.00..10.00\n"
                    "     random(-5:5, 1)         # float -5.0..5.0"
                ),
                'variants': [
                    'x = random(0:10, 0)',
                    'x = random(0:10, 2)',
                    'x = random(-5:5, 1)',
                ],
            },
            'RANDOM_BAD_RANGE': {
                'message': (
                    "random: range is specified via ':'."
                ),
                'wrong': 'random(0, 10, 0)',
                'right': 'random(0:10, 0)',
                'explanation': (
                    "Range — via COLON:\n"
                    "     random(0:10, 0)\n"
                    "     random(-5:5, 2)\n"
                    "\n"
                    "Incorrect:\n"
                    "     random(0, 10, 0)\n"
                    "     random(0 to 10, 0)\n"
                    "\n"
                    "Correct:\n"
                    "     random(0:10, 0)"
                ),
                'variants': [
                    'x = random(0:10, 0)',
                    'x = random(-5:5, 2)',
                ],
            },
            'RANDOM_BAD_PRECISION': {
                'message': (
                    "random: precision must be an integer >= 0."
                ),
                'wrong': 'random(0:10, "2")',
                'right': 'random(0:10, 2)',
                'explanation': (
                    "Precision — a NUMBER without quotes:\n"
                    "     random(0:10, 0)         # integers\n"
                    "     random(0:10, 2)         # 2 digits\n"
                    "     random(0:10, 4)         # 4 digits\n"
                    "\n"
                    "Incorrect:\n"
                    "     random(0:10, \"2\")\n"
                    "     random(0:10, -1)\n"
                    "\n"
                    "Correct:\n"
                    "     random(0:10, 2)"
                ),
                'variants': [
                    'x = random(0:10, 0)',
                    'x = random(0:10, 2)',
                ],
            },
            'RANDOM_NEGATIVE_PRECISION': {
                'message': (
                    "random: precision cannot be negative."
                ),
                'wrong': 'random(0:10, -1)',
                'right': 'random(0:10, 0)',
                'explanation': (
                    "Precision — integer >= 0:\n"
                    "     0  → integers\n"
                    "     2  → float with 2 digits\n"
                    "\n"
                    "Incorrect:\n"
                    "     random(0:10, -1)\n"
                    "\n"
                    "Correct:\n"
                    "     random(0:10, 0)\n"
                    "     random(0:10, 2)"
                ),
                'variants': [
                    'x = random(0:10, 0)',
                    'x = random(0:10, 2)',
                ],
            },
            'RANDOM_START_GREATER_END': {
                'message': (
                    "random: start must be LESS than end."
                ),
                'wrong': 'random(10:0, 0)',
                'right': 'random(0:10, 0)',
                'explanation': (
                    "Range is specified from smaller to larger:\n"
                    "     random(0:10, 0)\n"
                    "     random(-5:5, 2)\n"
                    "\n"
                    "Incorrect:\n"
                    "     random(10:0, 0)\n"
                    "\n"
                    "Correct:\n"
                    "     random(0:10, 0)"
                ),
                'variants': [
                    'x = random(0:10, 0)',
                    'x = random(-5:5, 2)',
                ],
            },
            'RANDOM_EMPTY_TARGET': {
                'message': (
                    "random: cannot fill an empty matrix/vector.\n"
                    "  First create a matrix via matrix()."
                ),
                'wrong': (
                    'm = []\n'
                    'm[all, all] = random(0:10, 0)'
                ),
                'right': (
                    'm = matrix(3, 3)\n'
                    'm[all, all] = random(0:10, 0)'
                ),
                'explanation': (
                    "random fills EXISTING cells.\n"
                    "If the matrix is empty — the size is unknown.\n"
                    "\n"
                    "Incorrect:\n"
                    "     m = []\n"
                    "     m[all, all] = random(0:10, 0)\n"
                    "\n"
                    "Correct:\n"
                    "     m = matrix(3, 3)\n"
                    "     m[all, all] = random(0:10, 0)\n"
                    "\n"
                    "Or via vector:\n"
                    "     v = vector(5)\n"
                    "     v[all] = random(0:10, 0)"
                ),
                'variants': [
                    'm = matrix(3, 3)\nm[all, all] = random(0:10, 0)',
                    'v = vector(5)\nv[all] = random(0:10, 0)',
                ],
            },
        },
    },
}