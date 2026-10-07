# errors/functions_db/control.py
"""
База ошибок для управляющих конструкций:
    for, while, break, try/catch.

Каждая функция описана в двух языках: RU и EN.

ВАЖНО: этот файл — только данные. Никаких import.
"""


RU = {
    # ============================================================
    # FOR
    # ============================================================
    'for': {
        'name': 'for',
        'category': 'control',
        'signature': 'for i = начало to конец [step S] do { ... }',
        'description': (
            'Цикл по диапазону.\n'
            '  • Оба конца ВКЛЮЧИТЕЛЬНО.\n'
            '  • Если начало > конца — идём вниз.\n'
            '  • step — опционально (по умолчанию 1).\n'
            '  • step 0 — ошибка.\n'
            '  • Тело — в фигурных скобках { ... }.'
        ),
        'examples': [
            'for i = 1 to 10 do { print(i) }',
            'for i = 10 to 1 do { print(i) }',
            'for i = 1 to 10 step 2 do { print(i) }',
            'for i = 2 to lenrow(m) do { print(m[i, 1]) }',
        ],
        'errors': {
            'FOR_END_KEYWORD': {
                'message': (
                    "for: ключевое слово 'end' нельзя использовать "
                    "в цикле for.\n"
                    "\n"
                    "  'end' — это указатель на конец КОНКРЕТНОГО "
                    "среза или массива.\n"
                    "  Но в for непонятно, конец ЧЕГО именно:\n"
                    "    • строк матрицы?\n"
                    "    • столбцов?\n"
                    "    • элементов вектора?\n"
                    "  Поэтому 'end' в for запрещён."
                ),
                'wrong': 'for i = 2 to end do { ... }',
                'right': (
                    'for i = 2 to lenrow(m) do { ... }   # строки\n'
                    'for j = 1 to lencol(m) do { ... }   # столбцы\n'
                    'for k = 1 to len(v) do { ... }      # вектор'
                ),
                'explanation': (
                    "ВЫБЕРИТЕ ПРАВИЛЬНУЮ ФУНКЦИЮ:\n"
                    "\n"
                    "  lenrow(m)  — количество СТРОК в матрице m\n"
                    "  lencol(m)  — количество СТОЛБЦОВ в матрице m\n"
                    "  len(v)     — длина ВЕКТОРА v\n"
                    "  len(s)     — длина СТРОКИ s\n"
                    "\n"
                    "  'end' работает только в срезах:\n"
                    "     m[:, end]        — последний столбец\n"
                    "     m[end, :]        — последняя строка\n"
                    "     m[2:end, :]      — от 2-й до последней\n"
                    "     v[end-1]         — предпоследний элемент\n"
                    "\n"
                    "  В цикле for 'end' не работает — используйте "
                    "lenrow/lencol/len."
                ),
                'variants': [
                    '# Обход строк матрицы\n'
                    'for i = 2 to lenrow(m) do {\n'
                    '    print(m[i, 1])\n'
                    '}',

                    '# Обход столбцов матрицы\n'
                    'for j = 1 to lencol(m) do {\n'
                    '    print(m[1, j])\n'
                    '}',

                    '# Обход вектора\n'
                    'for k = 1 to len(v) do {\n'
                    '    print(v[k])\n'
                    '}',
                ],
            },

            'FOR_BAD_VAR': {
                'message': (
                    "for: после 'for' ожидается ИМЯ переменной."
                ),
                'wrong': 'for = 1 to 10 do { ... }',
                'right': 'for i = 1 to 10 do { ... }',
                'explanation': (
                    "for требует ИМЯ переменной (i, j, k, n, ...).\n"
                    "\n"
                    "  for i = 1 to 10 do { ... }\n"
                    "       ^\n"
                    "       имя переменной"
                ),
                'variants': [
                    'for i = 1 to 10 do { print(i) }',
                    'for j = 1 to 5 do { print(j) }',
                ],
            },

            'FOR_NO_ASSIGN': {
                'message': "for: после переменной нужен '='.",
                'wrong': 'for i 1:10 do { ... }',
                'right': 'for i = 1 to 10 do { ... }',
                'explanation': (
                    "Правильная структура:\n"
                    "  for i = 1 to 10 do { ... }\n"
                    "       ^   ^  ^\n"
                    "       имя = начало to конец"
                ),
                'variants': [
                    'for i = 1 to 10 do { print(i) }',
                ],
            },

            'FOR_NO_TO': {
                'message': "for: в диапазоне нужно ключевое слово 'to'.",
                'wrong': 'for i = 1:10 do { ... }',
                'right': 'for i = 1 to 10 do { ... }',
                'explanation': (
                    "Правильная структура:\n"
                    "  for i = 1 to 10 do { ... }\n"
                    "            ^^\n"
                    "            тут 'to'"
                ),
                'variants': [
                    'for i = 1 to 10 do { print(i) }',
                ],
            },

            'FOR_NO_DO': {
                'message': "for: после диапазона нужно ключевое слово 'do'.",
                'wrong': 'for i = 1 to 10 { print(i) }',
                'right': 'for i = 1 to 10 do { print(i) }',
                'explanation': (
                    "Правильная структура:\n"
                    "  for i = 1 to 10 do { ... }\n"
                    "                  ^^\n"
                    "                  тут 'do'"
                ),
                'variants': [
                    'for i = 1 to 10 do { print(i) }',
                ],
            },

            'FOR_OLD_SYNTAX': {
                'message': (
                    "for: используется СТАРЫЙ синтаксис.\n"
                    "  Скобки в for больше не нужны."
                ),
                'wrong': 'for i(1:10) { print(i) }',
                'right': 'for i = 1 to 10 do { print(i) }',
                'explanation': (
                    "Синтаксис for изменился:\n"
                    "  БЫЛО:  for i(1:10) { ... }\n"
                    "  СТАЛО: for i = 1 to 10 do { ... }"
                ),
                'variants': [
                    'for i = 1 to 10 do { print(i) }',
                ],
            },

            'FOR_IN_SYNTAX': {
                'message': "for: слово 'in' в ArrayVator НЕ используется.",
                'wrong': 'for i in 1:10 { ... }',
                'right': 'for i = 1 to 10 do { ... }',
                'explanation': (
                    "Правильно:\n"
                    "  for i = 1 to 10 do { ... }"
                ),
                'variants': [
                    'for i = 1 to 10 do { print(i) }',
                ],
            },

            'FOR_NO_STEP': {
                'message': "for: после 'step' ожидается число.",
                'wrong': 'for i = 1 to 10 step do { ... }',
                'right': 'for i = 1 to 10 step 2 do { ... }',
                'explanation': (
                    "Правильная структура с шагом:\n"
                    "  for i = 1 to 10 step 2 do { ... }\n"
                    "                   ^^\n"
                    "                   шаг"
                ),
                'variants': [
                    'for i = 1 to 10 step 2 do { print(i) }',
                ],
            },

            'FOR_ZERO_STEP': {
                'message': "for: 'step 0' — бесконечный цикл. Запрещено.",
                'wrong': 'for i = 1 to 10 step 0 do { ... }',
                'right': 'for i = 1 to 10 do { ... }',
                'explanation': (
                    "Шаг не может быть нулём.\n"
                    "Если шаг не нужен — не указывайте 'step'."
                ),
                'variants': [
                    'for i = 1 to 10 do { print(i) }',
                ],
            },

            'FOR_WRONG_STEP_SIGN': {
                'message': "for: знак шага не совпадает с направлением.",
                'wrong': 'for i = 1 to 10 step -1 do { ... }',
                'right': 'for i = 1 to 10 step 1 do { ... }',
                'explanation': (
                    "Если начало <= конца → step > 0\n"
                    "Если начало > конца → step < 0"
                ),
                'variants': [
                    'for i = 1 to 10 step 2 do { print(i) }',
                    'for i = 10 to 1 step -2 do { print(i) }',
                ],
            },
        },
    },

    # ============================================================
    # WHILE
    # ============================================================
    'while': {
        'name': 'while',
        'category': 'control',
        'signature': 'while условие { ... }',
        'description': (
            'Цикл с условием.\n'
            '  • Выполняется, пока условие ИСТИННО.\n'
            '  • Тело — в фигурных скобках { ... }.'
        ),
        'examples': [
            'i = 1\nwhile i <= 5 { print(i); i = i + 1 }',
        ],
        'errors': {
            'WHILE_BAD_SYNTAX': {
                'message': (
                    "while: неверный синтаксис.\n"
                    "  Формат: while условие { ... }"
                ),
                'wrong': 'while { ... }',
                'right': 'while i <= 5 { print(i); i = i + 1 }',
                'explanation': (
                    "Правильная структура:\n"
                    "  while условие { ... }"
                ),
                'variants': [
                    'i = 1\nwhile i <= 5 { print(i); i = i + 1 }',
                ],
            },

            'WHILE_ASSIGN_IN_CONDITION': {
                'message': (
                    "while: в условии нужен '==' (сравнение), "
                    "а не '=' (присваивание)."
                ),
                'wrong': 'while i = 5 { ... }',
                'right': 'while i == 5 { ... }',
                'explanation': (
                    "'=' — присваивание.\n"
                    "'==' — сравнение."
                ),
                'variants': [
                    'while i == 5 { i = i + 1 }',
                    'while i < 5 { i = i + 1 }',
                ],
            },

            'WHILE_END_KEYWORD': {
                'message': (
                    "while: ключевое слово 'end' нельзя использовать "
                    "в цикле while.\n"
                    "\n"
                    "  'end' — это указатель на конец КОНКРЕТНОГО "
                    "среза или массива.\n"
                    "  В while непонятно, конец ЧЕГО именно.\n"
                    "  Используйте lenrow/lencol/len."
                ),
                'wrong': 'while i <= end { ... }',
                'right': (
                    'while i <= lenrow(m) { ... }\n'
                    'while j <= lencol(m) { ... }\n'
                    'while k <= len(v) { ... }'
                ),
                'explanation': (
                    "ВЫБЕРИТЕ ПРАВИЛЬНУЮ ФУНКЦИЮ:\n"
                    "\n"
                    "  lenrow(m)  — количество СТРОК в матрице m\n"
                    "  lencol(m)  — количество СТОЛБЦОВ в матрице m\n"
                    "  len(v)     — длина ВЕКТОРА v\n"
                    "  len(s)     — длина СТРОКИ s\n"
                    "\n"
                    "  'end' работает только в срезах:\n"
                    "     m[:, end]        — последний столбец\n"
                    "     m[end, :]        — последняя строка"
                ),
                'variants': [
                    'i = 2\nwhile i <= lenrow(m) {\n'
                    '    print(m[i, 1])\n'
                    '    i = i + 1\n'
                    '}',

                    'j = 1\nwhile j <= lencol(m) {\n'
                    '    print(m[1, j])\n'
                    '    j = j + 1\n'
                    '}',
                ],
            },
        },
    },

    # ============================================================
    # BREAK
    # ============================================================
    'break': {
        'name': 'break',
        'category': 'control',
        'signature': 'break',
        'description': 'Выход из цикла. Только внутри for или while.',
        'examples': [
            'for i = 1 to 100 do { if i > 5 then { break } }',
        ],
        'errors': {
            'BREAK_OUTSIDE_LOOP': {
                'message': "break можно использовать только внутри цикла.",
                'wrong': 'break',
                'right': 'for i = 1 to 10 do { break }',
                'explanation': "break работает только внутри for или while.",
                'variants': [
                    'for i = 1 to 10 do { break }',
                    'while true { break }',
                ],
            },
        },
    },

    # ============================================================
    # TRY / CATCH
    # ============================================================
    'try': {
        'name': 'try / catch',
        'category': 'control',
        'signature': 'try { ... } catch { ... }',
        'description': 'Обработка ошибок.',
        'examples': [
            'try { m = OpenCSV("file.csv") } '
            'catch { print("Ошибка:", error) }',
        ],
        'errors': {
            'TRY_BAD_SYNTAX': {
                'message': "try: неверный синтаксис.",
                'wrong': 'try { ... }',
                'right': 'try { ... } catch { ... }',
                'explanation': "try ВСЕГДА идёт в паре с catch.",
                'variants': [
                    'try { ... } catch { ... }',
                ],
            },
            'MISSING_CATCH': {
                'message': "try: после блока try нужен catch.",
                'wrong': 'try { ... }',
                'right': 'try { ... } catch { ... }',
                'explanation': "try без catch — ошибка.",
                'variants': [
                    'try { ... } catch { ... }',
                ],
            },
        },
    },
}


EN = {
    'for': {
        'name': 'for',
        'category': 'control',
        'signature': 'for i = start to end [step S] do { ... }',
        'description': (
            'Loop over a range.\n'
            '  • Both ends INCLUSIVE.\n'
            '  • If start > end — goes down.\n'
            '  • step — optional (default 1).'
        ),
        'examples': [
            'for i = 1 to 10 do { print(i) }',
            'for i = 10 to 1 do { print(i) }',
            'for i = 1 to 10 step 2 do { print(i) }',
        ],
        'errors': {
            'FOR_END_KEYWORD': {
                'message': (
                    "for: the keyword 'end' cannot be used "
                    "in a for loop.\n"
                    "\n"
                    "  'end' is a pointer to the end of a SPECIFIC "
                    "slice or array.\n"
                    "  But in for it's unclear WHICH one.\n"
                    "  That's why 'end' is forbidden in for."
                ),
                'wrong': 'for i = 2 to end do { ... }',
                'right': (
                    'for i = 2 to lenrow(m) do { ... }   # rows\n'
                    'for j = 1 to lencol(m) do { ... }   # columns\n'
                    'for k = 1 to len(v) do { ... }      # vector'
                ),
                'explanation': (
                    "CHOOSE THE RIGHT FUNCTION:\n"
                    "\n"
                    "  lenrow(m)  — number of ROWS in matrix m\n"
                    "  lencol(m)  — number of COLUMNS in matrix m\n"
                    "  len(v)     — length of VECTOR v\n"
                    "  len(s)     — length of STRING s\n"
                    "\n"
                    "  In a for loop 'end' does not work — "
                    "use lenrow/lencol/len."
                ),
                'variants': [
                    'for i = 2 to lenrow(m) do { print(m[i, 1]) }',
                    'for j = 1 to lencol(m) do { print(m[1, j]) }',
                    'for k = 1 to len(v) do { print(v[k]) }',
                ],
            },
            'FOR_BAD_VAR': {
                'message': "for: a VARIABLE NAME is expected after 'for'.",
                'wrong': 'for = 1 to 10 do { ... }',
                'right': 'for i = 1 to 10 do { ... }',
                'explanation': "for requires a variable name (i, j, k, n, ...).",
                'variants': [
                    'for i = 1 to 10 do { print(i) }',
                ],
            },
            'FOR_NO_ASSIGN': {
                'message': "for: '=' is required after the variable.",
                'wrong': 'for i 1:10 do { ... }',
                'right': 'for i = 1 to 10 do { ... }',
                'explanation': "Correct: for i = 1 to 10 do { ... }",
                'variants': [
                    'for i = 1 to 10 do { print(i) }',
                ],
            },
            'FOR_NO_TO': {
                'message': "for: keyword 'to' is required in the range.",
                'wrong': 'for i = 1:10 do { ... }',
                'right': 'for i = 1 to 10 do { ... }',
                'explanation': "Colon ':' is NOT used in for.",
                'variants': [
                    'for i = 1 to 10 do { print(i) }',
                ],
            },
            'FOR_NO_DO': {
                'message': "for: keyword 'do' is required after the range.",
                'wrong': 'for i = 1 to 10 { print(i) }',
                'right': 'for i = 1 to 10 do { print(i) }',
                'explanation': "'do' separates the range from the body.",
                'variants': [
                    'for i = 1 to 10 do { print(i) }',
                ],
            },
            'FOR_OLD_SYNTAX': {
                'message': "for: OLD syntax is used.",
                'wrong': 'for i(1:10) { print(i) }',
                'right': 'for i = 1 to 10 do { print(i) }',
                'explanation': "WAS: for i(1:10) { ... }\nNOW: for i = 1 to 10 do { ... }",
                'variants': [
                    'for i = 1 to 10 do { print(i) }',
                ],
            },
            'FOR_IN_SYNTAX': {
                'message': "for: the word 'in' is NOT used in ArrayVator.",
                'wrong': 'for i in 1:10 { ... }',
                'right': 'for i = 1 to 10 do { ... }',
                'explanation': "No 'for i in ...' construct.",
                'variants': [
                    'for i = 1 to 10 do { print(i) }',
                ],
            },
            'FOR_NO_STEP': {
                'message': "for: a number is expected after 'step'.",
                'wrong': 'for i = 1 to 10 step do { ... }',
                'right': 'for i = 1 to 10 step 2 do { ... }',
                'explanation': "Step is a number.",
                'variants': [
                    'for i = 1 to 10 step 2 do { print(i) }',
                ],
            },
            'FOR_ZERO_STEP': {
                'message': "for: 'step 0' is an infinite loop. Forbidden.",
                'wrong': 'for i = 1 to 10 step 0 do { ... }',
                'right': 'for i = 1 to 10 do { ... }',
                'explanation': "Step cannot be zero.",
                'variants': [
                    'for i = 1 to 10 do { print(i) }',
                ],
            },
            'FOR_WRONG_STEP_SIGN': {
                'message': "for: step sign does not match direction.",
                'wrong': 'for i = 1 to 10 step -1 do { ... }',
                'right': 'for i = 1 to 10 step 1 do { ... }',
                'explanation': "If start <= end → step > 0; if start > end → step < 0.",
                'variants': [
                    'for i = 1 to 10 step 2 do { print(i) }',
                ],
            },
        },
    },

    'while': {
        'name': 'while',
        'category': 'control',
        'signature': 'while condition { ... }',
        'description': 'Loop with a condition.',
        'examples': [
            'i = 1\nwhile i <= 5 { print(i); i = i + 1 }',
        ],
        'errors': {
            'WHILE_BAD_SYNTAX': {
                'message': "while: invalid syntax.",
                'wrong': 'while { ... }',
                'right': 'while i <= 5 { print(i); i = i + 1 }',
                'explanation': "Format: while condition { ... }",
                'variants': [
                    'i = 1\nwhile i <= 5 { print(i); i = i + 1 }',
                ],
            },
            'WHILE_ASSIGN_IN_CONDITION': {
                'message': "while: use '==' in the condition, not '='.",
                'wrong': 'while i = 5 { ... }',
                'right': 'while i == 5 { ... }',
                'explanation': "'=' — assignment, '==' — comparison.",
                'variants': [
                    'while i == 5 { i = i + 1 }',
                ],
            },
            'WHILE_END_KEYWORD': {
                'message': (
                    "while: the keyword 'end' cannot be used "
                    "in a while loop.\n"
                    "  Use lenrow/lencol/len."
                ),
                'wrong': 'while i <= end { ... }',
                'right': (
                    'while i <= lenrow(m) { ... }\n'
                    'while j <= lencol(m) { ... }\n'
                    'while k <= len(v) { ... }'
                ),
                'explanation': (
                    "CHOOSE THE RIGHT FUNCTION:\n"
                    "  lenrow(m)  — number of ROWS\n"
                    "  lencol(m)  — number of COLUMNS\n"
                    "  len(v)     — length of VECTOR\n"
                    "  len(s)     — length of STRING"
                ),
                'variants': [
                    'i = 2\nwhile i <= lenrow(m) {\n'
                    '    print(m[i, 1])\n'
                    '    i = i + 1\n'
                    '}',
                ],
            },
        },
    },

    'break': {
        'name': 'break',
        'category': 'control',
        'signature': 'break',
        'description': 'Exit the loop.',
        'examples': [
            'for i = 1 to 100 do { if i > 5 then { break } }',
        ],
        'errors': {
            'BREAK_OUTSIDE_LOOP': {
                'message': "break can only be used inside a loop.",
                'wrong': 'break',
                'right': 'for i = 1 to 10 do { break }',
                'explanation': "break works only inside for or while.",
                'variants': [
                    'for i = 1 to 10 do { break }',
                ],
            },
        },
    },

    'try': {
        'name': 'try / catch',
        'category': 'control',
        'signature': 'try { ... } catch { ... }',
        'description': 'Error handling.',
        'examples': [
            'try { m = OpenCSV("file.csv") } catch { print(error) }',
        ],
        'errors': {
            'TRY_BAD_SYNTAX': {
                'message': "try: invalid syntax.",
                'wrong': 'try { ... }',
                'right': 'try { ... } catch { ... }',
                'explanation': "try ALWAYS comes with catch.",
                'variants': [
                    'try { ... } catch { ... }',
                ],
            },
            'MISSING_CATCH': {
                'message': "try: catch is required.",
                'wrong': 'try { ... }',
                'right': 'try { ... } catch { ... }',
                'explanation': "try without catch is an error.",
                'variants': [
                    'try { ... } catch { ... }',
                ],
            },
        },
    },
}