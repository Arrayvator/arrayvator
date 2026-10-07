# errors/functions_db/replace.py
"""
База ошибок для функции REPLACETEXT — замена текста.

СИНТАКСИС:
    replacetext(data, "что", "на_что")
    replacetext(data, "что", "на_что", ignore)
    replacetext(m[:, "X"], "что", "на_что")
    replacetext(m[:, 3], "что", "на_что")

ПРАВИЛА:
    - Работает с Matrix и DuckDB.
    - ignore — без учёта регистра.
    - Возвращает НОВУЮ матрицу — результат нужно сохранить.
    - Один столбец → вектор.
    - Несколько столбцов → матрица.
    - Одна ячейка → скаляр.
"""

RU = {
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