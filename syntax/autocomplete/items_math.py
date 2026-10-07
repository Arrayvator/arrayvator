# syntax/autocomplete/items_math.py
"""
Описания математических функций: round, int, frac, frac_digits.
"""

RU = {
    'round': {
        'signature': 'round(значение [, знаков])',
        'description': (
            '🔄 ОКРУГЛЕНИЕ\n'
            '\n'
            'ЗАЧЕМ НУЖНА:\n'
            '  • Округлить число до N знаков после точки.\n'
            '  • Без N — до целого.\n'
            '\n'
            'ОСОБЕННОСТЬ PYTHON:\n'
            '  • round(2.5) → 2 (банковское округление).\n'
            '  • round(3.5) → 4.\n'
            '  • round(-3.7) → -4.\n'
            '\n'
            'КАКИЕ ЗАДАЧИ РЕШАЕТ:\n'
            '  • Округлить цены до копеек.\n'
            '  • Убрать "мусорные" хвосты float.\n'
            '  • Подготовить данные для отчёта.\n'
            '\n'
            '  • Работает со скалярами, векторами, матрицами.\n'
            '  • Поэлементно.'
        ),
        'example': (
            'r = round(3.14159)         # 3\n'
            'r = round(3.14159, 2)      # 3.14\n'
            'r = round(m[:, "Цена"], 2) # вектор округлённых'
        ),
        'matrix_example': (
            '# ДАНО:\n'
            '#\n'
            '#   m = ["Товар", "Цена"];\n'
            '#        "A", 1.234;\n'
            '#        "B", 5.678;\n'
            '#        "C", 9.111]\n'
            '\n'
            '# ЗАДАЧА: округлить цены до 1 знака\n'
            'r = round(m[:, "Цена"], 1)\n'
            'print(r)\n'
            '\n'
            '# ВЫВОД:\n'
            '#\n'
            '#   [1.2, 5.7, 9.1]'
        ),
    },
    'int': {
        'signature': 'int(значение)',
        'description': (
            '🔢 ЦЕЛАЯ ЧАСТЬ ЧИСЛА\n'
            '\n'
            'ЗАЧЕМ НУЖНА:\n'
            '  • Взять только целую часть, отбросив дробную.\n'
            '  • НЕ округляет! Просто отбрасывает.\n'
            '\n'
            'ВАЖНО:\n'
            '  • int(3.7)  → 3   (не 4!)\n'
            '  • int(-3.7) → -3  (отбрасывает в сторону нуля)\n'
            '\n'
            'ОТЛИЧИЕ ОТ round:\n'
            '  round(3.7) = 4   — округление.\n'
            '  int(3.7)   = 3   — только целая часть.\n'
            '\n'
            'КАКИЕ ЗАДАЧИ РЕШАЕТ:\n'
            '  • "Сколько полных лет".\n'
            '  • "Целые рубли без копеек".\n'
            '  • Определение "целая часть цены".'
        ),
        'example': (
            'r = int(3.7)     # 3\n'
            'r = int(-3.7)    # -3\n'
            'r = int(42)      # 42'
        ),
    },
    'frac': {
        'signature': 'frac(значение [, знаков])',
        'description': (
            '🔢 ДРОБНАЯ ЧАСТЬ ЧИСЛА\n'
            '\n'
            'ЗАЧЕМ НУЖНА:\n'
            '  • Взять только дробную часть (после точки).\n'
            '  • Классика: "копейки без рублей".\n'
            '\n'
            'КАК РАБОТАЕТ:\n'
            '  • frac(3.7)   → 0.7\n'
            '  • frac(-3.7)  → -0.7\n'
            '  • frac(3.14, 1) → 0.1 (с округлением до 1 знака)\n'
            '\n'
            'КАКИЕ ЗАДАЧИ РЕШАЕТ:\n'
            '  • Отделить "копейки" от рублей.\n'
            '  • Дробная часть времени.\n'
            '  • Разбор чисел на составляющие.'
        ),
        'example': (
            'r = frac(3.7)         # 0.7\n'
            'r = frac(-3.7)        # -0.7\n'
            'r = frac(3.14159, 2)  # 0.14'
        ),
    },
    'frac_digits': {
        'signature': 'frac_digits(значение)',
        'description': (
            '🔢 ДРОБНАЯ ЧАСТЬ КАК ЦЕЛОЕ\n'
            '\n'
            'ЗАЧЕМ НУЖНА:\n'
            '  • Взять ЦИФРЫ дробной части как целое число.\n'
            '  • frac(3.45) → 0.45, а frac_digits(3.45) → 45.\n'
            '\n'
            'КАК РАБОТАЕТ:\n'
            '  • frac_digits(3.456) → 456\n'
            '  • frac_digits(3.14)  → 14\n'
            '  • frac_digits(3.0)   → 0\n'
            '\n'
            'КАКИЕ ЗАДАЧИ РЕШАЕТ:\n'
            '  • Разбор "номера версии" (v2.15 → 15).\n'
            '  • Работа с кодами, где дробь — это часть кода.\n'
            '  • Извлечь "число копеек" из цены.'
        ),
        'example': (
            'r = frac_digits(3.456)   # 456\n'
            'r = frac_digits(3.14)    # 14\n'
            'r = frac_digits(3.0)     # 0'
        ),
    },
}


EN = {
    'round': {
        'signature': 'round(value [, digits])',
        'description': (
            '🔄 ROUNDING\n'
            '\n'
            'WHY NEEDED:\n'
            '  • Round a number to N decimal places.\n'
            '  • Without N — to an integer.\n'
            '\n'
            'PYTHON FEATURE:\n'
            '  • round(2.5) → 2 (banker\'s rounding).\n'
            '  • round(3.5) → 4.\n'
            '  • round(-3.7) → -4.\n'
            '\n'
            'TASKS IT SOLVES:\n'
            '  • Round prices to cents.\n'
            '  • Remove "garbage" tails of float.\n'
            '  • Prepare data for a report.'
        ),
        'example': (
            'r = round(3.14159)         # 3\n'
            'r = round(3.14159, 2)      # 3.14\n'
            'r = round(m[:, "Price"], 2) # vector of rounded'
        ),
    },
    'int': {
        'signature': 'int(value)',
        'description': (
            '🔢 INTEGER PART\n'
            '\n'
            'IMPORTANT:\n'
            '  • int(3.7)  → 3   (not 4!)\n'
            '  • int(-3.7) → -3  (truncated towards zero)\n'
            '\n'
            'DIFFERENCE FROM round:\n'
            '  round(3.7) = 4   — rounding.\n'
            '  int(3.7)   = 3   — integer part only.'
        ),
        'example': (
            'r = int(3.7)     # 3\n'
            'r = int(-3.7)    # -3\n'
            'r = int(42)      # 42'
        ),
    },
    'frac': {
        'signature': 'frac(value [, digits])',
        'description': (
            '🔢 FRACTIONAL PART\n'
            '\n'
            'HOW IT WORKS:\n'
            '  • frac(3.7)   → 0.7\n'
            '  • frac(-3.7)  → -0.7\n'
            '  • frac(3.14, 1) → 0.1'
        ),
        'example': (
            'r = frac(3.7)         # 0.7\n'
            'r = frac(-3.7)        # -0.7\n'
            'r = frac(3.14159, 2)  # 0.14'
        ),
    },
    'frac_digits': {
        'signature': 'frac_digits(value)',
        'description': (
            '🔢 FRACTIONAL PART AS INTEGER\n'
            '\n'
            'HOW IT WORKS:\n'
            '  • frac_digits(3.456) → 456\n'
            '  • frac_digits(3.14)  → 14\n'
            '  • frac_digits(3.0)   → 0'
        ),
        'example': (
            'r = frac_digits(3.456)   # 456\n'
            'r = frac_digits(3.14)    # 14\n'
            'r = frac_digits(3.0)     # 0'
        ),
    },
}