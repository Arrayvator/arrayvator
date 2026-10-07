# syntax/autocomplete/items_strings.py
"""
Описания строковых функций:
split, joinvector, replacetext, clean, deletetextleft, deletetextright,
trim, trimleft, trimright, transpose.

ПРАВИЛО ВОЗВРАТА:
    Один столбец   → вектор.
    Несколько столбцов → матрица.
    Одна ячейка   → скаляр.
"""

RU = {
    'split': {
        'signature': 'split(текст [, разделитель] [, skip])',
        'description': (
            'Разбивает строку на вектор.\n'
            '  • Без разделителя — по символам.\n'
            '  • С разделителем — по указанному разделителю.\n'
            '  • skip — пропускать пустые элементы.\n'
            '  • Возвращает ВЕКТОР.'
        ),
        'example': (
            'r = split("a,b,c", ",")\n'
            'r = split("Hello")\n'
            'r = split("a,,b,,c", ",", skip)'
        ),
    },
    'joinvector': {
        'signature': 'joinvector(вектор [, разделитель])',
        'description': (
            'Объединяет вектор в строку.\n'
            '  • Без разделителя — просто склейка.\n'
            '  • С разделителем — между элементами.\n'
            '  • Возвращает СТРОКУ.'
        ),
        'example': (
            'r = joinvector(["a", "b"], "-")\n'
            'r = joinvector(v)\n'
            'r = joinvector([10, 20, 30], ", ")'
        ),
    },
    'clean': {
        'signature': 'clean(данные, "digits"|"letters"|"special"|"alnum")',
        'description': (
            'Очистка текста.\n'
            '  • "digits"  — только цифры 0-9\n'
            '  • "letters" — только буквы\n'
            '  • "special" — только спецсимволы\n'
            '  • "alnum"   — буквы И цифры\n'
            '  • Работает с Matrix и DuckDB.\n'
            '  • Возвращает ВЕКТОР (если срез одного столбца).\n'
            '  • Возвращает МАТРИЦУ (если срез нескольких столбцов).'
        ),
        'example': (
            '# Вектор\n'
            'r = clean(m[:, "Код"], "digits")\n'
            '\n'
            '# Матрица — присваивание вектора обратно в столбец\n'
            'm[:, "Код"] = clean(m[:, "Код"], "digits")\n'
            '\n'
            '# Несколько столбцов — матрица\n'
            'r = clean(m[:, 2:4], "letters")'
        ),
        'matrix_example': (
            '# ДАНО:\n'
            '#\n'
            '#   m = ["Код"; "AB-123"; "CD-456"; "EF-789"]\n'
            '\n'
            'r = clean(m[:, "Код"], "digits")\n'
            'print(r)\n'
            '\n'
            '# ВЫВОД:\n'
            '#\n'
            '#   ["123", "456", "789"]'
        ),
    },
    'replacetext': {
        'signature': 'replacetext(данные, "что", "на_что" [, ignore])',
        'description': (
            'Заменяет подстроку в тексте.\n'
            '  • `ignore` — без учёта регистра.\n'
            '  • Работает с Matrix и DuckDB.\n'
            '  • НЕ мутирует исходную матрицу.'
        ),
        'example': (
            'r = replacetext(m[:, "Отдел"], "IT", "--")\n'
            'm[:, "Отдел"] = replacetext(m[:, "Отдел"], "IT", "--")'
        ),
        'matrix_example': (
            '# ДАНО:\n'
            '#\n'
            '#   m = ["Имя", "Отдел";\n'
            '#        "Аня", "IT";\n'
            '#        "Боб", "HR";\n'
            '#        "Света", "IT"]\n'
            '\n'
            '# Заменить "IT" на "--" в столбце Отдел\n'
            'm[:, "Отдел"] = replacetext(m[:, "Отдел"], "IT", "--")\n'
            'print(m)\n'
            '\n'
            '# ВЫВОД:\n'
            '#\n'
            '#   Имя    Отдел\n'
            '#   Аня    --\n'
            '#   Боб    HR\n'
            '#   Света  --'
        ),
    },
    'deletetextleft': {
        'signature': 'deletetextleft(данные, N)',
        'description': (
            'Удаляет N символов СЛЕВА.\n'
            '  • Если строка короче N, возвращает None.'
        ),
        'example': (
            'r = deletetextleft("PR-001", 3)          # "001"\n'
            'm[:, "Код"] = deletetextleft(m[:, "Код"], 4)'
        ),
        'matrix_example': (
            '# ДАНО:\n'
            '#\n'
            '#   m = ["Код";\n'
            '#        "PR-001";\n'
            '#        "PR-002"]\n'
            '\n'
            '# Удалить первые 3 символа\n'
            'r = deletetextleft(m[:, "Код"], 3)\n'
            'print(r)\n'
            '\n'
            '# ВЫВОД:\n'
            '#\n'
            '#   ["001", "002"]'
        ),
    },
    'deletetextright': {
        'signature': 'deletetextright(данные, N)',
        'description': (
            'Удаляет N символов СПРАВА.\n'
            '  • Если строка короче N, возвращает None.'
        ),
        'example': (
            'r = deletetextright("PR-001", 2)          # "PR-0"\n'
            'm[:, "Город"] = deletetextright(m[:, "Город"], 2)'
        ),
    },
    'trim': {
        'signature': 'trim(данные [, "символы"])',
        'description': (
            'Убирает пробелы (или указанные символы) с ОБЕИХ сторон.\n'
            '  • Без аргумента — все whitespace.\n'
            '  • Со строкой — только эти символы.\n'
            '  • None → None. Числа не трогает.'
        ),
        'example': (
            'r = trim("  hello  ")            # "hello"\n'
            'r = trim("...hello...", ".")     # "hello"'
        ),
        'matrix_example': (
            '# ДАНО:\n'
            '#\n'
            '#   m = ["Имя";\n'
            '#        "  Аня  ";\n'
            '#        " Боб "]\n'
            '\n'
            'r = trim(m[:, "Имя"])\n'
            'print(r)\n'
            '\n'
            '# ВЫВОД:\n'
            '#\n'
            '#   ["Аня", "Боб"]'
        ),
    },
    'trimleft': {
        'signature': 'trimleft(данные [, "символы"])',
        'description': (
            'Убирает пробелы (или указанные символы) СЛЕВА.\n'
            '  • Без аргумента — все whitespace.\n'
            '  • Со строкой — только эти символы.'
        ),
        'example': (
            'r = trimleft("  hello")             # "hello"\n'
            'r = trimleft(m[:, "Код"], "0")'
        ),
    },
    'trimright': {
        'signature': 'trimright(данные [, "символы"])',
        'description': (
            'Убирает пробелы (или указанные символы) СПРАВА.\n'
            '  • Без аргумента — все whitespace.\n'
            '  • Со строкой — только эти символы.'
        ),
        'example': (
            'r = trimright("hello  ")            # "hello"\n'
            'r = trimright(m[:, "Хвост"], "0")'
        ),
    },
    'transpose': {
        'signature': 'transpose(матрица)',
        'description': (
            'Транспонирует матрицу.\n'
            '  • Возвращает НОВУЮ матрицу.'
        ),
        'example': (
            'r = transpose(m)\n'
            'm = transpose(m)'
        ),
        'matrix_example': (
            '# ДАНО:\n'
            '#\n'
            '#   m = ["A", "B", "C";\n'
            '#        1,   2,   3]\n'
            '\n'
            'r = transpose(m)\n'
            'print(r)\n'
            '\n'
            '# ВЫВОД:\n'
            '#\n'
            '#   A  1\n'
            '#   B  2\n'
            '#   C  3'
        ),
    },
}


EN = {
    'split': {
        'signature': 'split(text [, delimiter] [, skip])',
        'description': (
            'Split a string into a vector.\n'
            '  • No delimiter — by characters.\n'
            '  • With delimiter — by the specified delimiter.\n'
            '  • skip — skip empty elements.\n'
            '  • Returns a VECTOR.'
        ),
        'example': (
            'r = split("a,b,c", ",")\n'
            'r = split("Hello")\n'
            'r = split("a,,b,,c", ",", skip)'
        ),
    },
    'joinvector': {
        'signature': 'joinvector(vector [, delimiter])',
        'description': (
            'Join a vector into a string.\n'
            '  • No delimiter — plain concatenation.\n'
            '  • With delimiter — between elements.\n'
            '  • Returns a STRING.'
        ),
        'example': (
            'r = joinvector(["a", "b"], "-")\n'
            'r = joinvector(v)\n'
            'r = joinvector([10, 20, 30], ", ")'
        ),
    },
    'clean': {
        'signature': 'clean(data, "digits"|"letters"|"special"|"alnum")',
        'description': (
            'Clean text.\n'
            '  • "digits"  — only digits 0-9\n'
            '  • "letters" — only letters\n'
            '  • "special" — only special characters\n'
            '  • "alnum"   — letters AND digits\n'
            '  • Works with Matrix and DuckDB.\n'
            '  • Returns a VECTOR (single column).\n'
            '  • Returns a MATRIX (multiple columns).'
        ),
        'example': (
            '# Vector\n'
            'r = clean(m[:, "Code"], "digits")\n'
            '\n'
            '# Matrix — assign the vector back into the column\n'
            'm[:, "Code"] = clean(m[:, "Code"], "digits")\n'
            '\n'
            '# Multiple columns — matrix\n'
            'r = clean(m[:, 2:4], "letters")'
        ),
        'matrix_example': (
            '# INPUT:\n'
            '#\n'
            '#   m = ["Code"; "AB-123"; "CD-456"; "EF-789"]\n'
            '\n'
            'r = clean(m[:, "Code"], "digits")\n'
            'print(r)\n'
            '\n'
            '# OUTPUT:\n'
            '#\n'
            '#   ["123", "456", "789"]'
        ),
    },
    'replacetext': {
        'signature': 'replacetext(data, "what", "with" [, ignore])',
        'description': (
            'Replace text.\n'
            '  • `ignore` — case-insensitive.\n'
            '  • Works with Matrix and DuckDB.\n'
            '  • Does NOT mutate the source matrix.'
        ),
        'example': (
            'r = replacetext(m[:, "Dept"], "IT", "--")\n'
            'm[:, "Dept"] = replacetext(m[:, "Dept"], "IT", "--")'
        ),
        'matrix_example': (
            '# INPUT:\n'
            '#\n'
            '#   m = ["Name", "Dept";\n'
            '#        "Anna", "IT";\n'
            '#        "Bob", "HR";\n'
            '#        "Eve", "IT"]\n'
            '\n'
            '# Replace "IT" with "--" in the Dept column\n'
            'm[:, "Dept"] = replacetext(m[:, "Dept"], "IT", "--")\n'
            'print(m)\n'
            '\n'
            '# OUTPUT:\n'
            '#\n'
            '#   Name  Dept\n'
            '#   Anna  --\n'
            '#   Bob   HR\n'
            '#   Eve   --'
        ),
    },
    'deletetextleft': {
        'signature': 'deletetextleft(data, N)',
        'description': (
            'Remove N characters from the LEFT.\n'
            '  • If the string is shorter than N, returns None.'
        ),
        'example': (
            'r = deletetextleft("PR-001", 3)          # "001"\n'
            'm[:, "Code"] = deletetextleft(m[:, "Code"], 4)'
        ),
        'matrix_example': (
            '# INPUT:\n'
            '#\n'
            '#   m = ["Code";\n'
            '#        "PR-001";\n'
            '#        "PR-002"]\n'
            '\n'
            '# Remove first 3 characters\n'
            'r = deletetextleft(m[:, "Code"], 3)\n'
            'print(r)\n'
            '\n'
            '# OUTPUT:\n'
            '#\n'
            '#   ["001", "002"]'
        ),
    },
    'deletetextright': {
        'signature': 'deletetextright(data, N)',
        'description': (
            'Remove N characters from the RIGHT.\n'
            '  • If the string is shorter than N, returns None.'
        ),
        'example': (
            'r = deletetextright("PR-001", 2)          # "PR-0"\n'
            'm[:, "City"] = deletetextright(m[:, "City"], 2)'
        ),
    },
    'trim': {
        'signature': 'trim(data [, "chars"])',
        'description': (
            'Remove spaces (or given characters) from BOTH sides.\n'
            '  • No argument — all whitespace.\n'
            '  • With string — only these characters.\n'
            '  • None → None. Numbers are not touched.'
        ),
        'example': (
            'r = trim("  hello  ")            # "hello"\n'
            'r = trim("...hello...", ".")     # "hello"'
        ),
        'matrix_example': (
            '# INPUT:\n'
            '#\n'
            '#   m = ["Name";\n'
            '#        "  Ann  ";\n'
            '#        " Bob "]\n'
            '\n'
            'r = trim(m[:, "Name"])\n'
            'print(r)\n'
            '\n'
            '# OUTPUT:\n'
            '#\n'
            '#   ["Ann", "Bob"]'
        ),
    },
    'trimleft': {
        'signature': 'trimleft(data [, "chars"])',
        'description': (
            'Remove spaces (or given characters) from the LEFT.\n'
            '  • No argument — all whitespace.\n'
            '  • With string — only these characters.'
        ),
        'example': (
            'r = trimleft("  hello")             # "hello"\n'
            'r = trimleft(m[:, "Code"], "0")'
        ),
    },
    'trimright': {
        'signature': 'trimright(data [, "chars"])',
        'description': (
            'Remove spaces (or given characters) from the RIGHT.\n'
            '  • No argument — all whitespace.\n'
            '  • With string — only these characters.'
        ),
        'example': (
            'r = trimright("hello  ")            # "hello"\n'
            'r = trimright(m[:, "Tail"], "0")'
        ),
    },
    'transpose': {
        'signature': 'transpose(matrix)',
        'description': (
            'Transpose a matrix.\n'
            '  • Returns a NEW matrix.'
        ),
        'example': (
            'r = transpose(m)\n'
            'm = transpose(m)'
        ),
        'matrix_example': (
            '# INPUT:\n'
            '#\n'
            '#   m = ["A", "B", "C";\n'
            '#        1,   2,   3]\n'
            '\n'
            'r = transpose(m)\n'
            'print(r)\n'
            '\n'
            '# OUTPUT:\n'
            '#\n'
            '#   A  1\n'
            '#   B  2\n'
            '#   C  3'
        ),
    },
}