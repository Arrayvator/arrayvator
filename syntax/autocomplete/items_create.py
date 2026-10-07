# syntax/autocomplete/items_create.py
"""
Описания функций создания: matrix, vector, zeros, ones, fill, range, random.
"""

RU = {
    'matrix': {
        'signature': 'matrix(R, C)',
        'description': 'Матрица R×C из None.',
        'example': 'm = matrix(3, 3)',
    },
    'vector': {
        'signature': 'vector(N)',
        'description': 'Вектор из N элементов None.',
        'example': 'v = vector(5)',
    },
    'zeros': {
        'signature': 'zeros(R [, C])',
        'description': 'Матрица/вектор с нулями.',
        'example': 'm = zeros(3, 3)',
    },
    'ones': {
        'signature': 'ones(R [, C])',
        'description': 'Матрица/вектор с единицами.',
        'example': 'm = ones(3, 3)',
    },
    'range': {
        'signature': 'range(start, end [, step])',
        'description': 'Диапазон чисел.',
        'example': 'v = range(1, 5)',
    },
    'fill': {
        'signature': 'fill(матрица, значение)',
        'description': 'Заполняет матрицу.',
        'example': 'm = fill(m, 0)',
    },
    'random': {
        'signature': 'random(начало:конец, точность)',
        'description': 'Случайные числа. ТОЛЬКО в присваивании!',
        'example': 'x = random(0:10, 0)\nm[all, all] = random(0:10, 0)',
    },
}


EN = {
    'matrix': {
        'signature': 'matrix(R, C)',
        'description': 'Matrix R×C filled with None.',
        'example': 'm = matrix(3, 3)',
    },
    'vector': {
        'signature': 'vector(N)',
        'description': 'Vector of N None values.',
        'example': 'v = vector(5)',
    },
    'zeros': {
        'signature': 'zeros(R [, C])',
        'description': 'Matrix/vector with zeros.',
        'example': 'm = zeros(3, 3)',
    },
    'ones': {
        'signature': 'ones(R [, C])',
        'description': 'Matrix/vector with ones.',
        'example': 'm = ones(3, 3)',
    },
    'range': {
        'signature': 'range(start, end [, step])',
        'description': 'Range of numbers.',
        'example': 'v = range(1, 5)',
    },
    'fill': {
        'signature': 'fill(matrix, value)',
        'description': 'Fill matrix with value.',
        'example': 'm = fill(m, 0)',
    },
    'random': {
        'signature': 'random(start:end, precision)',
        'description': 'Random numbers. ONLY inside an assignment!',
        'example': 'x = random(0:10, 0)\nm[all, all] = random(0:10, 0)',
    },
}