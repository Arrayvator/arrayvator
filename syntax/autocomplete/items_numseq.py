# syntax/autocomplete/items_numseq.py
"""
Описания функций range / Number — числовая последовательность.
"""

RU = {
    'range': {
        'signature': 'range(N) | range(a:b) | range(a:b, step S)',
        'description': (
            '🔢 ЧИСЛОВАЯ ПОСЛЕДОВАТЕЛЬНОСТЬ\n'
            '\n'
            'ЗАЧЕМ НУЖНА:\n'
            '  • Создать вектор чисел 1, 2, 3, ...\n'
            '  • Работает ТОЛЬКО в присваивании:\n'
            '      m[:, 1] = range(5)\n'
            '\n'
            'ФОРМАТЫ:\n'
            '  • range(N)          → [1, 2, ..., N]\n'
            '  • range(end)        → [1, ..., длина среза]\n'
            '  • range(2:end)      → [2, ..., длина среза]\n'
            '  • range(a:b)        → [a, ..., b]\n'
            '  • range(a:b, step S) → с шагом S\n'
            '  • range(10:1, step -1) → обратный порядок\n'
            '\n'
            'ПРАВИЛА:\n'
            '  • ОБА конца ВКЛЮЧИТЕЛЬНО.\n'
            '  • step > 0 для a<b, step < 0 для a>b.\n'
            '  • step 0 — ошибка.\n'
            '\n'
            'КАКИЕ ЗАДАЧИ РЕШАТЬ:\n'
            '  • Заполнить столбец номерами 1, 2, 3, ...\n'
            '  • Создать диапазон для for.\n'
            '  • Заполнить матрицу последовательностью.'
        ),
        'example': (
            'm = matrix(5, 1)\n'
            'm[:, 1] = range(5)              # [1,2,3,4,5]\n'
            'm[2:end, 1] = range(2:end)      # [2,3,4,5]\n'
            'm[:, 1] = range(1:10, step 2)   # [1,3,5,7,9]\n'
            'm[:, 1] = range(10:1, step -1)  # [10,9,...,1]'
        ),
        'matrix_example': (
            '# ДАНО:\n'
            '#\n'
            '#   m = matrix(5, 1)   — матрица 5×1 из None\n'
            '\n'
            '# ЗАДАЧА: заполнить столбец номерами 1..5\n'
            'm[:, 1] = range(1:5)\n'
            'print(m)\n'
            '\n'
            '# ВЫВОД:\n'
            '#\n'
            '#   1\n'
            '#   2\n'
            '#   3\n'
            '#   4\n'
            '#   5'
        ),
    },
    'Number': {
        'signature': 'Number(N) | Number(a:b) | Number(a:b, step S)',
        'description': (
            '🔢 ТО ЖЕ, ЧТО range\n'
            '\n'
            'Number — это синоним range.\n'
            'Полезно для читаемости, когда нужна именно\n'
            '"числовая последовательность", а не "диапазон".\n'
            '\n'
            'ФОРМАТЫ:\n'
            '  • Number(N)          → [1, 2, ..., N]\n'
            '  • Number(a:b)        → [a, ..., b]\n'
            '  • Number(a:b, step S) → с шагом S\n'
            '\n'
            '  • Работает только в присваивании.'
        ),
        'example': (
            'm = matrix(41, 1)\n'
            'm[:, 1] = Number(-10:10, step 0.5)'
        ),
    },
}


EN = {
    'range': {
        'signature': 'range(N) | range(a:b) | range(a:b, step S)',
        'description': (
            '🔢 NUMERIC SEQUENCE\n'
            '\n'
            'WHY NEEDED:\n'
            '  • Create a vector of numbers 1, 2, 3, ...\n'
            '  • Works ONLY in assignment:\n'
            '      m[:, 1] = range(5)\n'
            '\n'
            'FORMATS:\n'
            '  • range(N)          → [1, 2, ..., N]\n'
            '  • range(end)        → [1, ..., slice length]\n'
            '  • range(2:end)      → [2, ..., slice length]\n'
            '  • range(a:b)        → [a, ..., b]\n'
            '  • range(a:b, step S) → with step S\n'
            '  • range(10:1, step -1) → reverse order\n'
            '\n'
            'RULES:\n'
            '  • Both ends INCLUSIVE.\n'
            '  • step > 0 for a<b, step < 0 for a>b.\n'
            '  • step 0 — error.'
        ),
        'example': (
            'm = matrix(5, 1)\n'
            'm[:, 1] = range(5)\n'
            'm[:, 1] = range(1:10, step 2)'
        ),
    },
    'Number': {
        'signature': 'Number(N) | Number(a:b) | Number(a:b, step S)',
        'description': (
            '🔢 SAME AS range\n'
            '\n'
            'Number is a synonym for range.'
        ),
        'example': (
            'm = matrix(41, 1)\n'
            'm[:, 1] = Number(-10:10, step 0.5)'
        ),
    },
}