# errors/functions_db/_statements.py
"""
База ошибок для операторов управления:
    if, for, while, break, try/catch, error
"""


RU = {
    'if': {
        'name': 'if-then-else',
        'category': 'statement',
        'signature': 'if условие then { ... } [else { ... }]',
        'description': (
            'Условная конструкция.\n'
            '  • Блок в фигурных скобках.\n'
            '  • else — опционально.\n'
            '  • elif НЕТ — используйте вложенные if.'
        ),
        'examples': [
            'if x > 5 then { print("больше") }',
            'if x > 5 then { ... } else { ... }',
        ],
        'errors': {
            'IF_NO_THEN': {
                'message': "После условия if нужно ключевое слово 'then'.",
                'wrong': 'if x > 5 { print("X") }',
                'right': 'if x > 5 then { print("X") }',
                'explanation': (
                    "'then' отделяет условие от тела.\n"
                    "После условия ВСЕГДА идёт 'then'.\n"
                    "\n"
                    "Структура:\n"
                    "  if <условие> then <тело> [else <тело>]"
                ),
                'variants': [
                    'if x > 5 then { print("больше") }',
                    'if x > 5 then { ... } else { ... }',
                ],
            },
            'IF_ASSIGN_IN_CONDITION': {
                'message': "В условии нужно '==', а не '='.",
                'wrong': 'if x = 5 then',
                'right': 'if x == 5 then',
                'explanation': (
                    "'=' — присваивание.\n"
                    "'==' — сравнение.\n"
                    "\n"
                    "В условии if только '=='."
                ),
                'variants': [
                    'if x == 5 then { ... }',
                    'if m[:, "Отдел"] == "IT" then { ... }',
                ],
            },
            'IF_AND_OPERATOR': {
                'message': "Логическое И — 'and', а не '&&'.",
                'wrong': 'if x > 5 && y < 10 then',
                'right': 'if x > 5 and y < 10 then',
                'explanation': (
                    "ArrayVator использует СЛОВА:\n"
                    "  'and' — И\n"
                    "  'or'  — ИЛИ\n"
                    "  'not' — НЕ"
                ),
                'variants': [
                    'if x > 5 and y < 10 then { ... }',
                    'if m[:, "Отдел"] == "IT" and m[:, "Возраст"] > 25 then { ... }',
                ],
            },
        },
    },
    'for': {
        'name': 'for',
        'category': 'statement',
        'signature': 'for i = начало to конец [step S] do { ... }',
        'description': (
            'Цикл по диапазону.\n'
            '  • Оба конца включительно.\n'
            '  • Если начало > конца — идём вниз.\n'
            '  • step — опционально (по умолчанию 1).'
        ),
        'examples': [
            'for i = 1 to 10 do { print(i) }',
            'for i = 1 to 10 do print(i)',
            'for i = 10 to 1 do { print(i) }',
            'for i = 1 to 10 step 2 do { print(i) }',
        ],
        'errors': {
            'FOR_BAD_VAR': {
                'message': "for: после 'for' ожидается имя переменной.",
                'wrong': 'for = 1 to 10 do',
                'right': 'for i = 1 to 10 do',
                'explanation': (
                    "for требует ИМЯ переменной, а не число и не знак.\n"
                    "\n"
                    "Структура:\n"
                    "  for i = 1 to 10 do\n"
                    "      ^\n"
                    "      имя переменной"
                ),
                'variants': [
                    'for i = 1 to 10 do { print(i) }',
                    'for n = 1 to 10 do { print(n) }',
                    'for idx = 2 to 10 do { print(idx) }',
                ],
            },
            'FOR_OLD_SYNTAX': {
                'message': "Синтаксис for изменился.",
                'wrong': 'for i(1:10) { print(i) }',
                'right': 'for i = 1 to 10 do { print(i) }',
                'explanation': (
                    "Старый синтаксис со скобками больше не работает.\n"
                    "\n"
                    "Новый формат:\n"
                    "  for <переменная> = <начало> to <конец> [step N] do <тело>"
                ),
                'variants': [
                    'for i = 1 to 10 do { print(i) }',
                    'for i = 10 to 1 do { print(i) }',
                    'for i = 1 to 10 step 2 do { print(i) }',
                ],
            },
            'FOR_NO_ASSIGN': {
                'message': "После переменной в for нужен '='.",
                'wrong': 'for i 1:10 do',
                'right': 'for i = 1 to 10 do',
                'explanation': (
                    "Структура:\n"
                    "  for i = 1 to 10 do\n"
                    "       ^\n"
                    "       тут '='"
                ),
                'variants': [
                    'for i = 1 to 10 do { print(i) }',
                    'for i = 1 to 5 do { print(i) }',
                ],
            },
            'FOR_NO_TO': {
                'message': "В for нужен 'to' между началом и концом.",
                'wrong': 'for i = 1:10 do',
                'right': 'for i = 1 to 10 do',
                'explanation': (
                    "Структура:\n"
                    "  for i = 1 to 10 do\n"
                    "            ^\n"
                    "            тут 'to'"
                ),
                'variants': [
                    'for i = 1 to 10 do { print(i) }',
                    'for i = 1 to 5 do { print(i) }',
                ],
            },
            'FOR_NO_DO': {
                'message': "После диапазона в for нужен 'do'.",
                'wrong': 'for i = 1 to 10 { ... }',
                'right': 'for i = 1 to 10 do { ... }',
                'explanation': (
                    "Структура:\n"
                    "  for i = 1 to 10 do <тело>\n"
                    "                  ^\n"
                    "                  тут 'do'"
                ),
                'variants': [
                    'for i = 1 to 10 do { print(i) }',
                    'for i = 1 to 10 do print(i)',
                ],
            },
            'FOR_IN_SYNTAX': {
                'message': "В for не используется 'in'.",
                'wrong': 'for i in 1:10',
                'right': 'for i = 1 to 10 do { ... }',
                'explanation': (
                    "ArrayVator использует другой синтаксис:\n"
                    "  for i = 1 to 10 do"
                ),
                'variants': [
                    'for i = 1 to 10 do { print(i) }',
                    'for i = 1 to 5 do { print(i) }',
                ],
            },
        },
    },
    'while': {
        'name': 'while',
        'category': 'statement',
        'signature': 'while условие { ... }',
        'description': (
            'Цикл с условием.\n'
            '  • Выполняется, пока условие истинно.\n'
            '  • Внутри должен быть код, меняющий условие.'
        ),
        'examples': [
            'i = 1\nwhile i <= 5 { print(i); i = i + 1 }',
        ],
        'errors': {
            'WHILE_ASSIGN_IN_CONDITION': {
                'message': "В условии while нужно '==', а не '='.",
                'wrong': 'while i = 5',
                'right': 'while i == 5',
                'explanation': (
                    "'=' — присваивание.\n"
                    "'==' — сравнение.\n"
                    "\n"
                    "В условии while только '=='."
                ),
                'variants': [
                    'while i == 5 { i = i + 1 }',
                    'while i < 5 { i = i + 1 }',
                ],
            },
        },
    },
    'break': {
        'name': 'break',
        'category': 'statement',
        'signature': 'break',
        'description': 'Выход из цикла.',
        'examples': [
            'for i = 1 to 100 do { if i > 5 then { break } }',
        ],
        'errors': {
            'BREAK_OUTSIDE_LOOP': {
                'message': "break можно использовать только внутри цикла.",
                'wrong': 'break',
                'right': 'for i = 1 to 10 do { break }',
                'explanation': (
                    "break работает только внутри for или while.\n"
                    "Вне цикла — ошибка."
                ),
                'variants': [
                    'for i = 1 to 10 do { break }',
                    'while true { break }',
                ],
            },
        },
    },
    'try': {
        'name': 'try / catch',
        'category': 'statement',
        'signature': 'try { ... } catch { ... }',
        'description': (
            'Обработка ошибок.\n'
            '  • В try — код, который может упасть.\n'
            '  • В catch — код обработки.\n'
            '  • После catch переменная error сбрасывается в None.\n'
            '  • Можно указать переменную: catch (e) { ... }'
        ),
        'examples': [
            'try { m = OpenCSV("file.csv") } catch { print("Ошибка:", error) }',
            'try { ... } catch (e) { print("Поймано:", e) }',
        ],
        'errors': {
            'TRY_BAD_SYNTAX': {
                'message': (
                    "Неверный синтаксис try/catch.\n"
                    "  Формат: try { ... } catch { ... }\n"
                    "  Или:    try { ... } catch (e) { ... }"
                ),
                'wrong': 'try { ... }',
                'right': 'try { ... } catch { ... }',
                'explanation': (
                    "try ВСЕГДА идёт в паре с catch.\n"
                    "\n"
                    "Правильно:\n"
                    "  try\n"
                    "  {\n"
                    "      m = OpenCSV(\"file.csv\")\n"
                    "  }\n"
                    "  catch\n"
                    "  {\n"
                    "      print(\"Ошибка:\", error)\n"
                    "  }"
                ),
                'variants': [
                    'try { ... } catch { ... }',
                    'try { ... } catch (e) { ... }',
                ],
            },
            'MISSING_CATCH': {
                'message': "После try { ... } ожидается catch { ... }.",
                'wrong': 'try { ... }',
                'right': 'try { ... } catch { ... }',
                'explanation': (
                    "try без catch — ошибка.\n"
                    "catch обязателен."
                ),
                'variants': [
                    'try { ... } catch { ... }',
                    'try { ... } catch (e) { ... }',
                ],
            },
        },
    },
    'error': {
        'name': 'error (встроенная переменная)',
        'category': 'statement',
        'signature': 'error',
        'description': (
            'Текст последней ошибки (или None).\n'
            '  • Только для чтения.\n'
            '  • После успешного оператора — None.\n'
            '  • После упавшего — текст ошибки.'
        ),
        'examples': [
            'm = OpenCSV("missing.csv")\nif error then { print("Ошибка:", error) }',
        ],
        'errors': {
            'ERROR_RESERVED': {
                'message': (
                    "Имя 'error' зарезервировано.\n"
                    "  Используется для обработки ошибок."
                ),
                'wrong': 'error = 5',
                'right': 'err = 5',
                'explanation': (
                    "Переменная 'error' доступна ТОЛЬКО ДЛЯ ЧТЕНИЯ.\n"
                    "\n"
                    "Правильно: if error then { print(error) }\n"
                    "Неправильно: error = \"test\""
                ),
                'variants': [
                    'if error then { print("Ошибка:", error) }',
                    'err = 5',
                ],
            },
        },
    },
}


EN = {
    'if': {
        'name': 'if-then-else',
        'category': 'statement',
        'signature': 'if condition then { ... } [else { ... }]',
        'description': (
            'Conditional statement.\n'
            '  • Block in curly braces.\n'
            '  • else — optional.\n'
            '  • elif — NOT supported, use nested if.'
        ),
        'examples': [
            'if x > 5 then { print("greater") }',
            'if x > 5 then { ... } else { ... }',
        ],
        'errors': {
            'IF_NO_THEN': {
                'message': "After if condition, keyword 'then' is needed.",
                'wrong': 'if x > 5 { print("X") }',
                'right': 'if x > 5 then { print("X") }',
                'explanation': (
                    "'then' separates condition from body.\n"
                    "Always use 'then' after the condition.\n"
                    "\n"
                    "Structure:\n"
                    "  if <condition> then <body> [else <body>]"
                ),
                'variants': [
                    'if x > 5 then { print("greater") }',
                    'if x > 5 then { ... } else { ... }',
                ],
            },
            'IF_ASSIGN_IN_CONDITION': {
                'message': "In condition use '==', not '='.",
                'wrong': 'if x = 5 then',
                'right': 'if x == 5 then',
                'explanation': (
                    "'=' — assignment.\n"
                    "'==' — comparison.\n"
                    "\n"
                    "In if condition only '=='."
                ),
                'variants': [
                    'if x == 5 then { ... }',
                    'if m[:, "Dept"] == "IT" then { ... }',
                ],
            },
            'IF_AND_OPERATOR': {
                'message': "Logical AND is 'and', not '&&'.",
                'wrong': 'if x > 5 && y < 10 then',
                'right': 'if x > 5 and y < 10 then',
                'explanation': (
                    "ArrayVator uses WORDS:\n"
                    "  'and' — AND\n"
                    "  'or'  — OR\n"
                    "  'not' — NOT"
                ),
                'variants': [
                    'if x > 5 and y < 10 then { ... }',
                    'if m[:, "Dept"] == "IT" and m[:, "Age"] > 25 then { ... }',
                ],
            },
        },
    },
    'for': {
        'name': 'for',
        'category': 'statement',
        'signature': 'for i = start to end [step S] do { ... }',
        'description': (
            'Loop over a range.\n'
            '  • Both ends inclusive.\n'
            '  • If start > end — goes down.\n'
            '  • step — optional (default 1).'
        ),
        'examples': [
            'for i = 1 to 10 do { print(i) }',
            'for i = 1 to 10 do print(i)',
            'for i = 10 to 1 do { print(i) }',
            'for i = 1 to 10 step 2 do { print(i) }',
        ],
        'errors': {
            'FOR_BAD_VAR': {
                'message': "for: a variable name is expected after 'for'.",
                'wrong': 'for = 1 to 10 do',
                'right': 'for i = 1 to 10 do',
                'explanation': (
                    "for requires a VARIABLE NAME, not a number or sign.\n"
                    "\n"
                    "Structure:\n"
                    "  for i = 1 to 10 do\n"
                    "      ^\n"
                    "      variable name"
                ),
                'variants': [
                    'for i = 1 to 10 do { print(i) }',
                    'for n = 1 to 10 do { print(n) }',
                    'for idx = 2 to 10 do { print(idx) }',
                ],
            },
            'FOR_OLD_SYNTAX': {
                'message': "The 'for' syntax has changed.",
                'wrong': 'for i(1:10) { print(i) }',
                'right': 'for i = 1 to 10 do { print(i) }',
                'explanation': (
                    "The old syntax with parentheses no longer works.\n"
                    "\n"
                    "New format:\n"
                    "  for <variable> = <start> to <end> [step N] do <body>"
                ),
                'variants': [
                    'for i = 1 to 10 do { print(i) }',
                    'for i = 10 to 1 do { print(i) }',
                    'for i = 1 to 10 step 2 do { print(i) }',
                ],
            },
            'FOR_NO_ASSIGN': {
                'message': "After the variable in for, '=' is needed.",
                'wrong': 'for i 1:10 do',
                'right': 'for i = 1 to 10 do',
                'explanation': (
                    "Structure:\n"
                    "  for i = 1 to 10 do\n"
                    "       ^\n"
                    "       '=' here"
                ),
                'variants': [
                    'for i = 1 to 10 do { print(i) }',
                    'for i = 1 to 5 do { print(i) }',
                ],
            },
            'FOR_NO_TO': {
                'message': "In for, 'to' is needed between start and end.",
                'wrong': 'for i = 1:10 do',
                'right': 'for i = 1 to 10 do',
                'explanation': (
                    "Structure:\n"
                    "  for i = 1 to 10 do\n"
                    "            ^\n"
                    "            'to' here"
                ),
                'variants': [
                    'for i = 1 to 10 do { print(i) }',
                    'for i = 1 to 5 do { print(i) }',
                ],
            },
            'FOR_NO_DO': {
                'message': "After the range in for, 'do' is needed.",
                'wrong': 'for i = 1 to 10 { ... }',
                'right': 'for i = 1 to 10 do { ... }',
                'explanation': (
                    "Structure:\n"
                    "  for i = 1 to 10 do <body>\n"
                    "                  ^\n"
                    "                  'do' here"
                ),
                'variants': [
                    'for i = 1 to 10 do { print(i) }',
                    'for i = 1 to 10 do print(i)',
                ],
            },
            'FOR_IN_SYNTAX': {
                'message': "'in' is not used in for.",
                'wrong': 'for i in 1:10',
                'right': 'for i = 1 to 10 do { ... }',
                'explanation': (
                    "ArrayVator uses a different syntax:\n"
                    "  for i = 1 to 10 do"
                ),
                'variants': [
                    'for i = 1 to 10 do { print(i) }',
                    'for i = 1 to 5 do { print(i) }',
                ],
            },
        },
    },
    'while': {
        'name': 'while',
        'category': 'statement',
        'signature': 'while condition { ... }',
        'description': (
            'Loop with condition.\n'
            '  • Runs while condition is true.\n'
            '  • There must be code that changes the condition.'
        ),
        'examples': [
            'i = 1\nwhile i <= 5 { print(i); i = i + 1 }',
        ],
        'errors': {
            'WHILE_ASSIGN_IN_CONDITION': {
                'message': "In while condition, '==' is needed, not '='.",
                'wrong': 'while i = 5',
                'right': 'while i == 5',
                'explanation': (
                    "'=' — assignment.\n"
                    "'==' — comparison.\n"
                    "\n"
                    "In while condition only '=='."
                ),
                'variants': [
                    'while i == 5 { i = i + 1 }',
                    'while i < 5 { i = i + 1 }',
                ],
            },
        },
    },
    'break': {
        'name': 'break',
        'category': 'statement',
        'signature': 'break',
        'description': 'Exit the loop.',
        'examples': [
            'for i = 1 to 100 do { if i > 5 then { break } }',
        ],
        'errors': {
            'BREAK_OUTSIDE_LOOP': {
                'message': 'break can only be used inside a loop.',
                'wrong': 'break',
                'right': 'for i = 1 to 10 do { break }',
                'explanation': (
                    "break works only inside for or while.\n"
                    "Outside a loop — error."
                ),
                'variants': [
                    'for i = 1 to 10 do { break }',
                    'while true { break }',
                ],
            },
        },
    },
    'try': {
        'name': 'try / catch',
        'category': 'statement',
        'signature': 'try { ... } catch { ... }',
        'description': (
            'Error handling.\n'
            '  • In try — code that may fail.\n'
            '  • In catch — handler code.\n'
            '  • After catch, variable error is reset to None.\n'
            '  • You can specify a variable: catch (e) { ... }'
        ),
        'examples': [
            'try { m = OpenCSV("file.csv") } catch { print("Error:", error) }',
            'try { ... } catch (e) { print("Caught:", e) }',
        ],
        'errors': {
            'TRY_BAD_SYNTAX': {
                'message': (
                    "Invalid try/catch syntax.\n"
                    "  Format: try { ... } catch { ... }\n"
                    "  Or:     try { ... } catch (e) { ... }"
                ),
                'wrong': 'try { ... }',
                'right': 'try { ... } catch { ... }',
                'explanation': (
                    "try ALWAYS comes with catch.\n"
                    "\n"
                    "Correct:\n"
                    "  try\n"
                    "  {\n"
                    "      m = OpenCSV(\"file.csv\")\n"
                    "  }\n"
                    "  catch\n"
                    "  {\n"
                    "      print(\"Error:\", error)\n"
                    "  }"
                ),
                'variants': [
                    'try { ... } catch { ... }',
                    'try { ... } catch (e) { ... }',
                ],
            },
            'MISSING_CATCH': {
                'message': "After try { ... }, catch { ... } is expected.",
                'wrong': 'try { ... }',
                'right': 'try { ... } catch { ... }',
                'explanation': "try without catch — error. catch is mandatory.",
                'variants': [
                    'try { ... } catch { ... }',
                    'try { ... } catch (e) { ... }',
                ],
            },
        },
    },
    'error': {
        'name': 'error (built-in variable)',
        'category': 'statement',
        'signature': 'error',
        'description': (
            'Text of the last error (or None).\n'
            '  • Read-only.\n'
            '  • After a successful statement — None.\n'
            '  • After a failed one — the error text.'
        ),
        'examples': [
            'm = OpenCSV("missing.csv")\nif error then { print("Error:", error) }',
        ],
        'errors': {
            'ERROR_RESERVED': {
                'message': (
                    "The name 'error' is reserved.\n"
                    "  It is used for error handling."
                ),
                'wrong': 'error = 5',
                'right': 'err = 5',
                'explanation': (
                    "'error' is READ-ONLY.\n"
                    "\n"
                    "Правильно: if error then { print(error) }\n"
                    "Неправильно: error = \"test\""
                ),
                'variants': [
                    'if error then { print("Error:", error) }',
                    'err = 5',
                ],
            },
        },
    },
}