# errors/functions_db/string.py
"""
База ошибок для строковых функций: split, joinvector, replacetext.

СИНТАКСИС:
    split(текст [, разделитель] [, skip])           — разбить строку
    joinvector(вектор [, разделитель])              — собрать вектор
    replacetext(данные, "что", "на_что" [, ignore]) — замена текста

split и joinvector работают только со строками/векторами в RAM.
replacetext работает с Matrix и DuckDB.
"""


RU = {
    'split': {
        'name': 'split',
        'category': 'string',
        'signature': 'split(текст [, разделитель] [, skip])',
        'description': (
            'Разбивает строку на вектор.\n'
            '  • Без разделителя — по символам.\n'
            '  • С разделителем — по указанному разделителю.\n'
            '  • skip — пропускать пустые элементы.\n'
            '  • Возвращает ВЕКТОР.'
        ),
        'examples': [
            'r = split("a,b,c", ",")',
            'r = split("Hello")',
            'r = split("a,,b,,c", ",", skip)',
        ],
        'errors': {
            'SPLIT_BAD_SYNTAX': {
                'message': (
                    "split: неверный синтаксис.\n"
                    "  Нужен текст и, опционально, разделитель."
                ),
                'wrong': 'split()',
                'right': 'split("a,b,c", ",")',
                'explanation': (
                    "split принимает 1-3 аргумента:\n"
                    "     split(текст)                          — по символам\n"
                    "     split(текст, \"разделитель\")            — по разделителю\n"
                    "     split(текст, \"разделитель\", skip)      — пропускать пустые\n"
                    "\n"
                    "Неправильно:\n"
                    "     split()\n"
                    "     split(42)\n"
                    "\n"
                    "Правильно:\n"
                    "     split(\"a,b,c\", \",\")"
                ),
                'variants': [
                    'r = split("a,b,c", ",")',
                    'r = split("Hello")',
                    'r = split("a,,b,,c", ",", skip)',
                ],
            },
            'SPLIT_NOT_STRING': {
                'message': (
                    "split: текст должен быть строкой."
                ),
                'wrong': 'split(42)',
                'right': 'split("Hello")',
                'explanation': (
                    "split работает только со строками:\n"
                    "     split(\"Hello\")           — по символам\n"
                    "     split(\"a,b,c\", \",\")     — по разделителю\n"
                    "\n"
                    "Неправильно:\n"
                    "     split(42)\n"
                    "     split(v)\n"
                    "\n"
                    "Правильно:\n"
                    "     split(\"Hello\")"
                ),
                'variants': [
                    'r = split("Hello")',
                    'r = split("a,b,c", ",")',
                ],
            },
            'SPLIT_BAD_DELIMITER': {
                'message': (
                    "split: разделитель должен быть строкой."
                ),
                'wrong': 'split("a,b,c", 42)',
                'right': 'split("a,b,c", ",")',
                'explanation': (
                    "Разделитель — строка в кавычках:\n"
                    "     split(\"a,b,c\", \",\")\n"
                    "     split(\"a;b;c\", \";\")\n"
                    "     split(\"a\\tb\\tc\", \"\\t\")\n"
                    "\n"
                    "Неправильно:\n"
                    "     split(\"a,b,c\", 42)\n"
                    "\n"
                    "Правильно:\n"
                    "     split(\"a,b,c\", \",\")"
                ),
                'variants': [
                    'r = split("a,b,c", ",")',
                    'r = split("a;b;c", ";")',
                ],
            },
        },
    },

    'joinvector': {
        'name': 'joinvector',
        'category': 'string',
        'signature': 'joinvector(вектор [, разделитель])',
        'description': (
            'Собирает вектор в строку.\n'
            '  • Без разделителя — просто склейка.\n'
            '  • С разделителем — между элементами.\n'
            '  • Возвращает СТРОКУ.'
        ),
        'examples': [
            'r = joinvector(["a", "b"], "-")',
            'r = joinvector(v)',
            'r = joinvector([10, 20, 30], ", ")',
        ],
        'errors': {
            'JOINVECTOR_BAD_SYNTAX': {
                'message': (
                    "joinvector: неверный синтаксис.\n"
                    "  Нужен вектор и, опционально, разделитель."
                ),
                'wrong': 'joinvector()',
                'right': 'joinvector(["a", "b"], "-")',
                'explanation': (
                    "joinvector принимает 1 или 2 аргумента:\n"
                    "     joinvector(вектор)                — склейка\n"
                    "     joinvector(вектор, \"разделитель\")  — с разделителем\n"
                    "\n"
                    "Неправильно:\n"
                    "     joinvector()\n"
                    "     joinvector(m)\n"
                    "\n"
                    "Правильно:\n"
                    "     joinvector([\"a\", \"b\"], \"-\")"
                ),
                'variants': [
                    'r = joinvector(["a", "b"], "-")',
                    'r = joinvector(v)',
                ],
            },
            'JOINVECTOR_NOT_VECTOR': {
                'message': (
                    "joinvector: нужен вектор, не матрица."
                ),
                'wrong': 'joinvector(m)',
                'right': 'joinvector(v)',
                'explanation': (
                    "joinvector работает с ОДНОМЕРНЫМИ данными:\n"
                    "     joinvector([\"a\", \"b\", \"c\"], \"-\")\n"
                    "     joinvector(v)\n"
                    "     joinvector(m[:, \"Имя\"])\n"
                    "\n"
                    "Неправильно:\n"
                    "     joinvector(m)              — матрица\n"
                    "\n"
                    "Правильно:\n"
                    "     joinvector(v)\n"
                    "     joinvector(m[:, \"X\"])"
                ),
                'variants': [
                    'r = joinvector(v)',
                    'r = joinvector(m[:, "X"])',
                ],
            },
        },
    },

    'replacetext': {
        'name': 'replacetext',
        'category': 'string',
        'signature': 'replacetext(данные, "что", "на_что" [, ignore])',
        'description': (
            'Заменяет текст на другой.\n'
            '  • Ищет подстроку и заменяет её.\n'
            '  • ignore — без учёта регистра.\n'
            '  • Работает с Matrix и DuckDB.\n'
            '  • Возвращает НОВУЮ матрицу — результат нужно сохранить.'
        ),
        'examples': [
            'r = replacetext("Hello", "l", "L")',
            'm = replacetext(m[:, "Отдел"], "IT", "--")',
            'm = replacetext(m, "it", "--", ignore)',
        ],
        'errors': {
            'REPLACETEXT_BAD_SYNTAX': {
                'message': (
                    "replacetext: неверный синтаксис.\n"
                    "  Нужны данные, что искать и на что заменить."
                ),
                'wrong': 'replacetext("Hello", "l")',
                'right': 'replacetext("Hello", "l", "L")',
                'explanation': (
                    "replacetext принимает 3-4 аргумента:\n"
                    "     replacetext(данные, \"что\", \"на_что\")\n"
                    "     replacetext(данные, \"что\", \"на_что\", ignore)\n"
                    "\n"
                    "Неправильно:\n"
                    "     replacetext(\"Hello\", \"l\")\n"
                    "\n"
                    "Правильно:\n"
                    "     replacetext(\"Hello\", \"l\", \"L\")"
                ),
                'variants': [
                    'r = replacetext("Hello", "l", "L")',
                    'm = replacetext(m[:, "Отдел"], "IT", "--")',
                ],
            },
            'REPLACETEXT_NEEDS_ASSIGNMENT': {
                'message': (
                    "replacetext() возвращает значение — "
                    "результат нужно сохранить."
                ),
                'wrong': 'replacetext(m, "IT", "--")',
                'right': 'm = replacetext(m, "IT", "--")',
                'explanation': (
                    "replacetext НЕ изменяет исходную матрицу.\n"
                    "Он ВОЗВРАЩАЕТ НОВУЮ.\n"
                    "\n"
                    "Правильно:\n"
                    "  r = replacetext(...)      — в новую переменную\n"
                    "  m = replacetext(...)      — мутация"
                ),
                'variants': [
                    'r = replacetext(m, "IT", "--")',
                    'm = replacetext(m, "IT", "--")',
                ],
            },
        },
    },
}


EN = {
    'split': {
        'name': 'split',
        'category': 'string',
        'signature': 'split(text [, delimiter] [, skip])',
        'description': (
            'Split a string into a vector.\n'
            '  • Without delimiter — by characters.\n'
            '  • With delimiter — by the specified delimiter.\n'
            '  • skip — skip empty elements.\n'
            '  • Returns a VECTOR.'
        ),
        'examples': [
            'r = split("a,b,c", ",")',
            'r = split("Hello")',
            'r = split("a,,b,,c", ",", skip)',
        ],
        'errors': {
            'SPLIT_BAD_SYNTAX': {
                'message': (
                    "split: invalid syntax.\n"
                    "  Need text and optionally a delimiter."
                ),
                'wrong': 'split()',
                'right': 'split("a,b,c", ",")',
                'explanation': (
                    "split takes 1-3 arguments:\n"
                    "     split(text)                          — by characters\n"
                    "     split(text, \"delimiter\")             — by delimiter\n"
                    "     split(text, \"delimiter\", skip)       — skip empty\n"
                    "\n"
                    "Incorrect:\n"
                    "     split()\n"
                    "     split(42)\n"
                    "\n"
                    "Correct:\n"
                    "     split(\"a,b,c\", \",\")"
                ),
                'variants': [
                    'r = split("a,b,c", ",")',
                    'r = split("Hello")',
                    'r = split("a,,b,,c", ",", skip)',
                ],
            },
            'SPLIT_NOT_STRING': {
                'message': (
                    "split: text must be a string."
                ),
                'wrong': 'split(42)',
                'right': 'split("Hello")',
                'explanation': (
                    "split works only with strings:\n"
                    "     split(\"Hello\")           — by characters\n"
                    "     split(\"a,b,c\", \",\")     — by delimiter\n"
                    "\n"
                    "Incorrect:\n"
                    "     split(42)\n"
                    "     split(v)\n"
                    "\n"
                    "Correct:\n"
                    "     split(\"Hello\")"
                ),
                'variants': [
                    'r = split("Hello")',
                    'r = split("a,b,c", ",")',
                ],
            },
            'SPLIT_BAD_DELIMITER': {
                'message': (
                    "split: delimiter must be a string."
                ),
                'wrong': 'split("a,b,c", 42)',
                'right': 'split("a,b,c", ",")',
                'explanation': (
                    "Delimiter is a string in quotes:\n"
                    "     split(\"a,b,c\", \",\")\n"
                    "     split(\"a;b;c\", \";\")\n"
                    "     split(\"a\\tb\\tc\", \"\\t\")\n"
                    "\n"
                    "Incorrect:\n"
                    "     split(\"a,b,c\", 42)\n"
                    "\n"
                    "Correct:\n"
                    "     split(\"a,b,c\", \",\")"
                ),
                'variants': [
                    'r = split("a,b,c", ",")',
                    'r = split("a;b;c", ";")',
                ],
            },
        },
    },

    'joinvector': {
        'name': 'joinvector',
        'category': 'string',
        'signature': 'joinvector(vector [, delimiter])',
        'description': (
            'Join a vector into a string.\n'
            '  • Without delimiter — plain concatenation.\n'
            '  • With delimiter — between elements.\n'
            '  • Returns a STRING.'
        ),
        'examples': [
            'r = joinvector(["a", "b"], "-")',
            'r = joinvector(v)',
            'r = joinvector([10, 20, 30], ", ")',
        ],
        'errors': {
            'JOINVECTOR_BAD_SYNTAX': {
                'message': (
                    "joinvector: invalid syntax.\n"
                    "  Need a vector and optionally a delimiter."
                ),
                'wrong': 'joinvector()',
                'right': 'joinvector(["a", "b"], "-")',
                'explanation': (
                    "joinvector takes 1 or 2 arguments:\n"
                    "     joinvector(vector)                — concatenation\n"
                    "     joinvector(vector, \"delimiter\")   — with delimiter\n"
                    "\n"
                    "Incorrect:\n"
                    "     joinvector()\n"
                    "     joinvector(m)\n"
                    "\n"
                    "Correct:\n"
                    "     joinvector([\"a\", \"b\"], \"-\")"
                ),
                'variants': [
                    'r = joinvector(["a", "b"], "-")',
                    'r = joinvector(v)',
                ],
            },
            'JOINVECTOR_NOT_VECTOR': {
                'message': (
                    "joinvector: need a vector, not a matrix."
                ),
                'wrong': 'joinvector(m)',
                'right': 'joinvector(v)',
                'explanation': (
                    "joinvector works with 1D data:\n"
                    "     joinvector([\"a\", \"b\", \"c\"], \"-\")\n"
                    "     joinvector(v)\n"
                    "     joinvector(m[:, \"Name\"])\n"
                    "\n"
                    "Incorrect:\n"
                    "     joinvector(m)              — matrix\n"
                    "\n"
                    "Correct:\n"
                    "     joinvector(v)\n"
                    "     joinvector(m[:, \"X\"])"
                ),
                'variants': [
                    'r = joinvector(v)',
                    'r = joinvector(m[:, "X"])',
                ],
            },
        },
    },

    'replacetext': {
        'name': 'replacetext',
        'category': 'string',
        'signature': 'replacetext(data, "what", "with" [, ignore])',
        'description': (
            'Replace text with another.\n'
            '  • Searches for a substring and replaces it.\n'
            '  • ignore — case-insensitive.\n'
            '  • Works with Matrix and DuckDB.\n'
            '  • Returns a NEW matrix — save the result.'
        ),
        'examples': [
            'r = replacetext("Hello", "l", "L")',
            'm = replacetext(m[:, "Dept"], "IT", "--")',
            'm = replacetext(m, "it", "--", ignore)',
        ],
        'errors': {
            'REPLACETEXT_BAD_SYNTAX': {
                'message': (
                    "replacetext: invalid syntax.\n"
                    "  Need data, what to find, and what to replace with."
                ),
                'wrong': 'replacetext("Hello", "l")',
                'right': 'replacetext("Hello", "l", "L")',
                'explanation': (
                    "replacetext takes 3-4 arguments:\n"
                    "     replacetext(data, \"what\", \"with\")\n"
                    "     replacetext(data, \"what\", \"with\", ignore)\n"
                    "\n"
                    "Incorrect:\n"
                    "     replacetext(\"Hello\", \"l\")\n"
                    "\n"
                    "Correct:\n"
                    "     replacetext(\"Hello\", \"l\", \"L\")"
                ),
                'variants': [
                    'r = replacetext("Hello", "l", "L")',
                    'm = replacetext(m[:, "Dept"], "IT", "--")',
                ],
            },
            'REPLACETEXT_NEEDS_ASSIGNMENT': {
                'message': (
                    "replacetext() returns a value — "
                    "the result must be saved."
                ),
                'wrong': 'replacetext(m, "IT", "--")',
                'right': 'm = replacetext(m, "IT", "--")',
                'explanation': (
                    "replacetext does NOT modify the source matrix.\n"
                    "It RETURNS a NEW one.\n"
                    "\n"
                    "Correct:\n"
                    "  r = replacetext(...)      — to a new variable\n"
                    "  m = replacetext(...)      — mutation"
                ),
                'variants': [
                    'r = replacetext(m, "IT", "--")',
                    'm = replacetext(m, "IT", "--")',
                ],
            },
        },
    },
}