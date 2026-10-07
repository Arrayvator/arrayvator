# syntax/autocomplete/items_statistics.py
"""
Описания статистических функций:
sum, min, max, avg, count, median, std,
len, lenrow, lencol, CountDistinct.

У каждой функции — два режима:
  • без by → скаляр (одно число)
  • с by   → вектор (по группам, длина = число строк)
"""

RU = {
    # ============================================================
    # SUM
    # ============================================================
    'sum': {
        'signature': 'sum(значение [, by m[:, "X"]])',
        'description': (
            'Сумма.\n'
            '  • Без by — одно число.\n'
            '  • С by — сумма группы для каждой строки (вектор).\n'
            '  • None, строки, bool — игнорируются.\n'
            '  • Пустой ввод → 0.'
        ),
        'example': (
            'r = sum(m[:, "Зарплата"])                       # одно число\n'
            'r = sum(m[:, "Зарплата"], by m[:, "Отдел"])      # вектор'
        ),
        'matrix_example': (
            '# ДАНО:\n'
            '#\n'
            '#   m = ["Отдел", "Зарплата";\n'
            '#        "IT",    85000;\n'
            '#        "HR",    65000;\n'
            '#        "IT",    95000;\n'
            '#        "Sales", 80000]\n'
            '\n'
            '# Скаляр:\n'
            'print(sum(m[:, "Зарплата"]))\n'
            '# 325000\n'
            '\n'
            '# Вектор по группам:\n'
            'print(sum(m[:, "Зарплата"], by m[:, "Отдел"]))\n'
            '# [180000, 65000, 180000, 80000]'
        ),
    },

    # ============================================================
    # MIN
    # ============================================================
    'min': {
        'signature': 'min(значение [, by m[:, "X"]])',
        'description': (
            'Минимум.\n'
            '  • Без by — одно число.\n'
            '  • С by — минимум группы для каждой строки (вектор).'
        ),
        'example': (
            'r = min(m[:, "Зарплата"])                       # одно число\n'
            'r = min(m[:, "Зарплата"], by m[:, "Отдел"])      # вектор'
        ),
        'matrix_example': (
            '# ДАНО:\n'
            '#\n'
            '#   m = ["Отдел", "Зарплата";\n'
            '#        "IT",    85000;\n'
            '#        "HR",    65000;\n'
            '#        "IT",    95000;\n'
            '#        "Sales", 80000;\n'
            '#        "HR",    72000;\n'
            '#        "IT",    78000]\n'
            '\n'
            '# Скаляр:\n'
            'print(min(m[:, "Зарплата"]))\n'
            '# 65000\n'
            '\n'
            '# Вектор по группам:\n'
            'print(min(m[:, "Зарплата"], by m[:, "Отдел"]))\n'
            '# [78000, 65000, 78000, 80000, 65000, 78000]'
        ),
    },

    # ============================================================
    # MAX
    # ============================================================
    'max': {
        'signature': 'max(значение [, by m[:, "X"]])',
        'description': (
            'Максимум.\n'
            '  • Без by — одно число.\n'
            '  • С by — максимум группы для каждой строки (вектор).'
        ),
        'example': (
            'r = max(m[:, "Зарплата"])                       # одно число\n'
            'r = max(m[:, "Зарплата"], by m[:, "Отдел"])      # вектор'
        ),
        'matrix_example': (
            '# ДАНО:\n'
            '#\n'
            '#   m = ["Отдел", "Зарплата";\n'
            '#        "IT",    85000;\n'
            '#        "HR",    65000;\n'
            '#        "IT",    95000;\n'
            '#        "Sales", 80000;\n'
            '#        "HR",    72000;\n'
            '#        "IT",    78000]\n'
            '\n'
            '# Скаляр:\n'
            'print(max(m[:, "Зарплата"]))\n'
            '# 95000\n'
            '\n'
            '# Вектор по группам:\n'
            'print(max(m[:, "Зарплата"], by m[:, "Отдел"]))\n'
            '# [95000, 72000, 95000, 80000, 72000, 95000]'
        ),
    },

    # ============================================================
    # AVG
    # ============================================================
    'avg': {
        'signature': 'avg(значение [, by m[:, "X"]])',
        'description': (
            'Среднее.\n'
            '  • Без by — одно число.\n'
            '  • С by — среднее группы для каждой строки (вектор).'
        ),
        'example': (
            'r = avg(m[:, "Зарплата"])                       # одно число\n'
            'r = avg(m[:, "Зарплата"], by m[:, "Отдел"])      # вектор'
        ),
        'matrix_example': (
            '# ДАНО:\n'
            '#\n'
            '#   m = ["Отдел", "Зарплата";\n'
            '#        "IT",    85000;\n'
            '#        "HR",    65000;\n'
            '#        "IT",    95000;\n'
            '#        "Sales", 80000;\n'
            '#        "HR",    72000;\n'
            '#        "IT",    78000]\n'
            '\n'
            '# Скаляр:\n'
            'print(avg(m[:, "Зарплата"]))\n'
            '# 81666.67\n'
            '\n'
            '# Вектор по группам:\n'
            'print(avg(m[:, "Зарплата"], by m[:, "Отдел"]))\n'
            '# [86000.0, 68500.0, 86000.0, 80000.0, 68500.0, 86000.0]'
        ),
    },

    # ============================================================
    # COUNT
    # ============================================================
    'count': {
        'signature': 'count([значение] [, by m[:, "X"]])',
        'description': (
            'Количество.\n'
            '  • count(m[:, "X"]) — непустые значения (одно число).\n'
            '  • count(m[:, "X"], by m[:, "Y"]) — непустые в группе (вектор).\n'
            '  • count(by m[:, "Y"]) — количество строк в группе (вектор).'
        ),
        'example': (
            'r = count(m[:, "Зарплата"])                       # непустые\n'
            'r = count(m[:, "Зарплата"], by m[:, "Отдел"])      # вектор\n'
            'r = count(by m[:, "Отдел"])                        # строк в группе'
        ),
        'matrix_example': (
            '# ДАНО:\n'
            '#\n'
            '#   m = ["Отдел", "Зарплата";\n'
            '#        "IT",    85000;\n'
            '#        "HR",    None;\n'
            '#        "IT",    95000;\n'
            '#        "HR",    65000]\n'
            '\n'
            '# Непустые значения:\n'
            'print(count(m[:, "Зарплата"]))              # 3\n'
            '\n'
            '# По группам (непустые):\n'
            'print(count(m[:, "Зарплата"], by m[:, "Отдел"]))\n'
            '# [2, 1, 2, 1]\n'
            '\n'
            '# По группам (всего строк):\n'
            'print(count(by m[:, "Отдел"]))\n'
            '# [2, 2, 2, 2]'
        ),
    },

    # ============================================================
    # MEDIAN
    # ============================================================
    'median': {
        'signature': 'median(значение [, by m[:, "X"]])',
        'description': (
            'Медиана.\n'
            '  • Без by — одно число.\n'
            '  • С by — медиана группы для каждой строки (вектор).'
        ),
        'example': (
            'r = median(m[:, "Зарплата"])                       # одно число\n'
            'r = median(m[:, "Зарплата"], by m[:, "Отдел"])      # вектор'
        ),
        'matrix_example': (
            '# ДАНО:\n'
            '#\n'
            '#   m = ["Отдел", "Зарплата";\n'
            '#        "IT",    85000;\n'
            '#        "HR",    65000;\n'
            '#        "IT",    95000;\n'
            '#        "Sales", 80000;\n'
            '#        "HR",    72000;\n'
            '#        "IT",    78000]\n'
            '\n'
            '# Скаляр:\n'
            'print(median(m[:, "Зарплата"]))\n'
            '# 81500.0\n'
            '\n'
            '# Вектор по группам:\n'
            'print(median(m[:, "Зарплата"], by m[:, "Отдел"]))\n'
            '# [85000.0, 68500.0, 85000.0, 80000.0, 68500.0, 85000.0]'
        ),
    },

    # ============================================================
    # STD
    # ============================================================
    'std': {
        'signature': 'std(значение [, by m[:, "X"]])',
        'description': (
            'Стандартное отклонение (population, делитель N).\n'
            '  • Без by — одно число.\n'
            '  • С by — отклонение группы для каждой строки (вектор).'
        ),
        'example': (
            'r = std(m[:, "Зарплата"])                       # одно число\n'
            'r = std(m[:, "Зарплата"], by m[:, "Отдел"])      # вектор'
        ),
        'matrix_example': (
            '# ДАНО (упрощённые числа):\n'
            '#\n'
            '#   m = ["Отдел", "Зарплата";\n'
            '#        "IT",    2;\n'
            '#        "HR",    4;\n'
            '#        "IT",    4;\n'
            '#        "Sales", 6;\n'
            '#        "HR",    8;\n'
            '#        "IT",    4]\n'
            '\n'
            '# Скаляр:\n'
            'print(std(m[:, "Зарплата"]))\n'
            '# 1.4907...\n'
            '\n'
            '# Вектор по группам:\n'
            'print(std(m[:, "Зарплата"], by m[:, "Отдел"]))\n'
            '# [0.9428..., 2.0, 0.9428..., 0.0, 2.0, 0.9428...]'
        ),
    },

    # ============================================================
    # LEN / LENROW / LENCOL
    # ============================================================
    'len': {
        'signature': 'len(значение)',
        'description': (
            'Длина строки, числа или вектора.\n'
            '  • Для строки — количество символов.\n'
            '  • Для числа — длина строкового представления.\n'
            '  • Для вектора — количество элементов.\n'
            '  • None → 0.'
        ),
        'example': 'r = len("Привет")    # 6',
    },
    'lenrow': {
        'signature': 'lenrow(матрица)',
        'description': (
            'Количество строк в матрице или векторе.\n'
            '  • Для DuckDB — COUNT(*) через SQL.'
        ),
        'example': 'r = lenrow(m)',
    },
    'lencol': {
        'signature': 'lencol(матрица)',
        'description': (
            'Количество столбцов в матрице или векторе.\n'
            '  • Для DuckDB — количество столбцов через SQL.'
        ),
        'example': 'r = lencol(m)',
    },

    # ============================================================
    # COUNTDISTINCT
    # ============================================================
    'CountDistinct': {
        'signature': 'CountDistinct(срез)',
        'description': (
            'Количество уникальных значений в столбце или векторе.\n'
            '  • Возвращает СКАЛЯР (число).'
        ),
        'example': 'r = CountDistinct(m[:, "Отдел"])',
        'matrix_example': (
            '# ДАНО:\n'
            '#\n'
            '#   m = ["Отдел";\n'
            '#        "IT";\n'
            '#        "IT";\n'
            '#        "HR";\n'
            '#        "IT"]\n'
            '\n'
            'r = CountDistinct(m[:, "Отдел"])\n'
            'print(r)\n'
            '\n'
            '# ВЫВОД:\n'
            '#\n'
            '#   2'
        ),
    },
}


EN = {
    # ============================================================
    # SUM
    # ============================================================
    'sum': {
        'signature': 'sum(value [, by m[:, "X"]])',
        'description': (
            'Sum.\n'
            '  • Without by — single number.\n'
            '  • With by — group sum for each row (vector).\n'
            '  • None, strings, bool — ignored.\n'
            '  • Empty input → 0.'
        ),
        'example': (
            'r = sum(m[:, "Salary"])                       # single number\n'
            'r = sum(m[:, "Salary"], by m[:, "Department"]) # vector'
        ),
        'matrix_example': (
            '# INPUT:\n'
            '#\n'
            '#   m = ["Department", "Salary";\n'
            '#        "IT",         85000;\n'
            '#        "HR",         65000;\n'
            '#        "IT",         95000;\n'
            '#        "Sales",      80000]\n'
            '\n'
            '# Scalar:\n'
            'print(sum(m[:, "Salary"]))\n'
            '# 325000\n'
            '\n'
            '# Vector by groups:\n'
            'print(sum(m[:, "Salary"], by m[:, "Department"]))\n'
            '# [180000, 65000, 180000, 80000]'
        ),
    },

    # ============================================================
    # MIN
    # ============================================================
    'min': {
        'signature': 'min(value [, by m[:, "X"]])',
        'description': (
            'Minimum.\n'
            '  • Without by — single number.\n'
            '  • With by — group minimum for each row (vector).'
        ),
        'example': (
            'r = min(m[:, "Salary"])                       # single number\n'
            'r = min(m[:, "Salary"], by m[:, "Department"]) # vector'
        ),
        'matrix_example': (
            '# INPUT:\n'
            '#\n'
            '#   m = ["Department", "Salary";\n'
            '#        "IT",         85000;\n'
            '#        "HR",         65000;\n'
            '#        "IT",         95000;\n'
            '#        "Sales",      80000;\n'
            '#        "HR",         72000;\n'
            '#        "IT",         78000]\n'
            '\n'
            '# Scalar:\n'
            'print(min(m[:, "Salary"]))\n'
            '# 65000\n'
            '\n'
            '# Vector by groups:\n'
            'print(min(m[:, "Salary"], by m[:, "Department"]))\n'
            '# [78000, 65000, 78000, 80000, 65000, 78000]'
        ),
    },

    # ============================================================
    # MAX
    # ============================================================
    'max': {
        'signature': 'max(value [, by m[:, "X"]])',
        'description': (
            'Maximum.\n'
            '  • Without by — single number.\n'
            '  • With by — group maximum for each row (vector).'
        ),
        'example': (
            'r = max(m[:, "Salary"])                       # single number\n'
            'r = max(m[:, "Salary"], by m[:, "Department"]) # vector'
        ),
        'matrix_example': (
            '# INPUT:\n'
            '#\n'
            '#   m = ["Department", "Salary";\n'
            '#        "IT",         85000;\n'
            '#        "HR",         65000;\n'
            '#        "IT",         95000;\n'
            '#        "Sales",      80000;\n'
            '#        "HR",         72000;\n'
            '#        "IT",         78000]\n'
            '\n'
            '# Scalar:\n'
            'print(max(m[:, "Salary"]))\n'
            '# 95000\n'
            '\n'
            '# Vector by groups:\n'
            'print(max(m[:, "Salary"], by m[:, "Department"]))\n'
            '# [95000, 72000, 95000, 80000, 72000, 95000]'
        ),
    },

    # ============================================================
    # AVG
    # ============================================================
    'avg': {
        'signature': 'avg(value [, by m[:, "X"]])',
        'description': (
            'Average.\n'
            '  • Without by — single number.\n'
            '  • With by — group average for each row (vector).'
        ),
        'example': (
            'r = avg(m[:, "Salary"])                       # single number\n'
            'r = avg(m[:, "Salary"], by m[:, "Department"]) # vector'
        ),
        'matrix_example': (
            '# INPUT:\n'
            '#\n'
            '#   m = ["Department", "Salary";\n'
            '#        "IT",         85000;\n'
            '#        "HR",         65000;\n'
            '#        "IT",         95000;\n'
            '#        "Sales",      80000;\n'
            '#        "HR",         72000;\n'
            '#        "IT",         78000]\n'
            '\n'
            '# Scalar:\n'
            'print(avg(m[:, "Salary"]))\n'
            '# 81666.67\n'
            '\n'
            '# Vector by groups:\n'
            'print(avg(m[:, "Salary"], by m[:, "Department"]))\n'
            '# [86000.0, 68500.0, 86000.0, 80000.0, 68500.0, 86000.0]'
        ),
    },

    # ============================================================
    # COUNT
    # ============================================================
    'count': {
        'signature': 'count([value] [, by m[:, "X"]])',
        'description': (
            'Count.\n'
            '  • count(m[:, "X"]) — non-empty values (single number).\n'
            '  • count(m[:, "X"], by m[:, "Y"]) — non-empty in group (vector).\n'
            '  • count(by m[:, "Y"]) — rows per group (vector).'
        ),
        'example': (
            'r = count(m[:, "Salary"])                       # non-empty\n'
            'r = count(m[:, "Salary"], by m[:, "Department"]) # vector\n'
            'r = count(by m[:, "Department"])                 # rows per group'
        ),
        'matrix_example': (
            '# INPUT:\n'
            '#\n'
            '#   m = ["Department", "Salary";\n'
            '#        "IT",         85000;\n'
            '#        "HR",         None;\n'
            '#        "IT",         95000;\n'
            '#        "HR",         65000]\n'
            '\n'
            '# Non-empty values:\n'
            'print(count(m[:, "Salary"]))              # 3\n'
            '\n'
            '# By groups (non-empty):\n'
            'print(count(m[:, "Salary"], by m[:, "Department"]))\n'
            '# [2, 1, 2, 1]\n'
            '\n'
            '# By groups (total rows):\n'
            'print(count(by m[:, "Department"]))\n'
            '# [2, 2, 2, 2]'
        ),
    },

    # ============================================================
    # MEDIAN
    # ============================================================
    'median': {
        'signature': 'median(value [, by m[:, "X"]])',
        'description': (
            'Median.\n'
            '  • Without by — single number.\n'
            '  • With by — group median for each row (vector).'
        ),
        'example': (
            'r = median(m[:, "Salary"])                       # single number\n'
            'r = median(m[:, "Salary"], by m[:, "Department"]) # vector'
        ),
        'matrix_example': (
            '# INPUT:\n'
            '#\n'
            '#   m = ["Department", "Salary";\n'
            '#        "IT",         85000;\n'
            '#        "HR",         65000;\n'
            '#        "IT",         95000;\n'
            '#        "Sales",      80000;\n'
            '#        "HR",         72000;\n'
            '#        "IT",         78000]\n'
            '\n'
            '# Scalar:\n'
            'print(median(m[:, "Salary"]))\n'
            '# 81500.0\n'
            '\n'
            '# Vector by groups:\n'
            'print(median(m[:, "Salary"], by m[:, "Department"]))\n'
            '# [85000.0, 68500.0, 85000.0, 80000.0, 68500.0, 85000.0]'
        ),
    },

    # ============================================================
    # STD
    # ============================================================
    'std': {
        'signature': 'std(value [, by m[:, "X"]])',
        'description': (
            'Standard deviation (population, divisor N).\n'
            '  • Without by — single number.\n'
            '  • With by — group deviation for each row (vector).'
        ),
        'example': (
            'r = std(m[:, "Salary"])                       # single number\n'
            'r = std(m[:, "Salary"], by m[:, "Department"]) # vector'
        ),
        'matrix_example': (
            '# INPUT (simplified numbers):\n'
            '#\n'
            '#   m = ["Department", "Salary";\n'
            '#        "IT",         2;\n'
            '#        "HR",         4;\n'
            '#        "IT",         4;\n'
            '#        "Sales",      6;\n'
            '#        "HR",         8;\n'
            '#        "IT",         4]\n'
            '\n'
            '# Scalar:\n'
            'print(std(m[:, "Salary"]))\n'
            '# 1.4907...\n'
            '\n'
            '# Vector by groups:\n'
            'print(std(m[:, "Salary"], by m[:, "Department"]))\n'
            '# [0.9428..., 2.0, 0.9428..., 0.0, 2.0, 0.9428...]'
        ),
    },

    # ============================================================
    # LEN / LENROW / LENCOL
    # ============================================================
    'len': {
        'signature': 'len(value)',
        'description': (
            'Length of a string, number, or vector.\n'
            '  • String — number of characters.\n'
            '  • Number — length of string representation.\n'
            '  • Vector — number of elements.\n'
            '  • None → 0.'
        ),
        'example': 'r = len("Hello")    # 5',
    },
    'lenrow': {
        'signature': 'lenrow(matrix)',
        'description': (
            'Number of rows in a matrix or vector.\n'
            '  • For DuckDB — COUNT(*) via SQL.'
        ),
        'example': 'r = lenrow(m)',
    },
    'lencol': {
        'signature': 'lencol(matrix)',
        'description': (
            'Number of columns in a matrix or vector.\n'
            '  • For DuckDB — column count via SQL.'
        ),
        'example': 'r = lencol(m)',
    },

    # ============================================================
    # COUNTDISTINCT
    # ============================================================
    'CountDistinct': {
        'signature': 'CountDistinct(slice)',
        'description': (
            'Number of unique values in a column or vector.\n'
            '  • Returns a SCALAR (number).'
        ),
        'example': 'r = CountDistinct(m[:, "Department"])',
        'matrix_example': (
            '# INPUT:\n'
            '#\n'
            '#   m = ["Department";\n'
            '#        "IT";\n'
            '#        "IT";\n'
            '#        "HR";\n'
            '#        "IT"]\n'
            '\n'
            'r = CountDistinct(m[:, "Department"])\n'
            'print(r)\n'
            '\n'
            '# OUTPUT:\n'
            '#\n'
            '#   2'
        ),
    },
}