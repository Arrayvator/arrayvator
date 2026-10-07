# errors/functions_db/conditional_agg.py
"""
База ошибок для условных агрегатов.

ФУНКЦИИ:
    sumif, countif, avgif, minif, maxif,
    medianif, countuniqueif, sumproduct

ДВА РЕЖИМА КАЖДОЙ:
    sumif(условие, срез)              — скаляр
    sumif(by m[:, "X"], срез)        — вектор

⚠️  Работает с Matrix (RAM) и DuckDB (BigData).
"""


RU = {
    # ============================================================
    # SUMIF
    # ============================================================
    'sumif': {
        'name': 'sumif',
        'category': 'conditional_agg',
        'signature': 'sumif(условие, срез) | sumif(by m[:, "X"], срез)',
        'description': (
            'Сумма по условию.\n'
            '  • Без by — скаляр (одно число).\n'
            '  • С by — вектор (для каждой строки сумма её группы).\n'
            '  • Работает с Matrix и DuckDB.\n'
            '  • Возвращает значение — сохраните результат.'
        ),
        'examples': [
            'r = sumif(m[:, "Отдел"] == "IT", m[:, "Зарплата"])',
            'r = sumif(m[:, "Возраст"] > 25, m[:, "Зарплата"])',
            'm = addcolumn(m, "Итого_отдел", sumif(by m[:, "Отдел"], m[:, "Зарплата"]))',
        ],
        'errors': {
            'SUMIF_BAD_SYNTAX': {
                'message': (
                    "sumif: неверный синтаксис.\n"
                    "  Нужно условие и срез значений."
                ),
                'wrong': 'sumif(m[:, "Отдел"] == "IT")',
                'right': 'sumif(m[:, "Отдел"] == "IT", m[:, "Зарплата"])',
                'explanation': (
                    "sumif принимает ДВА аргумента:\n"
                    "  1. условие\n"
                    "  2. срез значений\n"
                    "\n"
                    "Структура (скаляр):\n"
                    "  sumif(<условие>, <срез-значений>)\n"
                    "\n"
                    "Структура (вектор):\n"
                    "  sumif(by <срез-группы>, <срез-значений>)"
                ),
                'variants': [
                    'r = sumif(m[:, "Отдел"] == "IT", m[:, "Зарплата"])',
                    'r = sumif(by m[:, "Отдел"], m[:, "Зарплата"])',
                ],
            },
            'SUMIF_ASSIGN_IN_CONDITION': {
                'message': (
                    "sumif: в условии нужен '==' (сравнение), а не '=' (присваивание)."
                ),
                'wrong': 'sumif(m[:, "Отдел"] = "IT", m[:, "Зарплата"])',
                'right': 'sumif(m[:, "Отдел"] == "IT", m[:, "Зарплата"])',
                'explanation': (
                    "'=' — присваивает значение.\n"
                    "'==' — сравнивает значения.\n"
                    "\n"
                    "В условии sumif ВСЕГДА '=='."
                ),
                'variants': [
                    'r = sumif(m[:, "Отдел"] == "IT", m[:, "Зарплата"])',
                    'r = sumif(m[:, "Возраст"] > 25, m[:, "Зарплата"])',
                ],
            },
            'SUMIF_AND_OPERATOR': {
                'message': (
                    "sumif: логическое И пишется как 'and', а не '&&'."
                ),
                'wrong': 'sumif(m[:, "Отдел"] == "IT" && m[:, "Возраст"] > 25, m[:, "Зарплата"])',
                'right': 'sumif(m[:, "Отдел"] == "IT" and m[:, "Возраст"] > 25, m[:, "Зарплата"])',
                'explanation': (
                    "ArrayVator использует СЛОВА:\n"
                    "  'and' — И\n"
                    "  'or'  — ИЛИ\n"
                    "  'not' — НЕ"
                ),
                'variants': [
                    'r = sumif(m[:, "Отдел"] == "IT" and m[:, "Возраст"] > 25, m[:, "Зарплата"])',
                ],
            },
            'SUMIF_OR_OPERATOR': {
                'message': (
                    "sumif: логическое ИЛИ пишется как 'or', а не '||'."
                ),
                'wrong': 'sumif(m[:, "Отдел"] == "IT" || m[:, "Отдел"] == "HR", m[:, "Зарплата"])',
                'right': 'sumif(m[:, "Отдел"] == "IT" or m[:, "Отдел"] == "HR", m[:, "Зарплата"])',
                'explanation': (
                    "ArrayVator использует СЛОВА:\n"
                    "  'and' — И\n"
                    "  'or'  — ИЛИ\n"
                    "  'not' — НЕ"
                ),
                'variants': [
                    'r = sumif(m[:, "Отдел"] == "IT" or m[:, "Отдел"] == "HR", m[:, "Зарплата"])',
                ],
            },
            'SUMIF_NO_SLICE': {
                'message': (
                    "sumif: нет среза.\n"
                    "  Условие должно быть на срезе m[:, \"X\"]."
                ),
                'wrong': 'sumif("Отдел" == "IT", m[:, "Зарплата"])',
                'right': 'sumif(m[:, "Отдел"] == "IT", m[:, "Зарплата"])',
                'explanation': (
                    "Срез указывает, к какому столбцу применяется условие.\n"
                    "\n"
                    "Неправильно: sumif(\"Отдел\" == \"IT\", ...)\n"
                    "Правильно: sumif(m[:, \"Отдел\"] == \"IT\", ...)"
                ),
                'variants': [
                    'r = sumif(m[:, "Отдел"] == "IT", m[:, "Зарплата"])',
                    'r = sumif(m[2:10, "Отдел"] == "IT", m[:, "Зарплата"])',
                ],
            },
            'SUMIF_BAD_VALUE': {
                'message': (
                    "sumif: второй аргумент должен быть срезом m[:, \"X\"].\n"
                    "  Не имя строкой и не число."
                ),
                'wrong': 'sumif(m[:, "Отдел"] == "IT", "Зарплата")',
                'right': 'sumif(m[:, "Отдел"] == "IT", m[:, "Зарплата"])',
                'explanation': (
                    "Срез значений — это СРЕЗ, а не имя столбца.\n"
                    "\n"
                    "Неправильно:\n"
                    "     sumif(..., \"Зарплата\")\n"
                    "     sumif(..., 5)\n"
                    "\n"
                    "Правильно:\n"
                    "     sumif(..., m[:, \"Зарплата\"])\n"
                    "     sumif(..., m[:, 5])"
                ),
                'variants': [
                    'r = sumif(m[:, "Отдел"] == "IT", m[:, "Зарплата"])',
                    'r = sumif(m[:, "Отдел"] == "IT", m[:, 5])',
                ],
            },
            'SUMIF_BY_NOT_SLICE': {
                'message': (
                    "sumif: by требует срез m[:, \"X\"]."
                ),
                'wrong': 'sumif(by "Отдел", m[:, "Зарплата"])',
                'right': 'sumif(by m[:, "Отдел"], m[:, "Зарплата"])',
                'explanation': (
                    "by принимает СРЕЗ столбца-группировки:\n"
                    "     by m[:, \"Отдел\"]\n"
                    "     by m[:, 3]"
                ),
                'variants': [
                    'r = sumif(by m[:, "Отдел"], m[:, "Зарплата"])',
                    'r = sumif(by m[:, 3], m[:, 5])',
                ],
            },
            'SUMIF_REQUIRES_ASSIGNMENT': {
                'message': (
                    "sumif() возвращает значение — сохраните результат."
                ),
                'wrong': 'sumif(m[:, "Отдел"] == "IT", m[:, "Зарплата"])',
                'right': 'r = sumif(m[:, "Отдел"] == "IT", m[:, "Зарплата"])',
                'explanation': (
                    "sumif возвращает значение (скаляр или вектор).\n"
                    "Без присваивания результат теряется.\n"
                    "\n"
                    "Правильно:\n"
                    "  r = sumif(...)                            — в переменную\n"
                    "  m = addcolumn(m, \"X\", sumif(...))         — в столбец\n"
                    "  print(sumif(...))                          — вывод"
                ),
                'variants': [
                    'r = sumif(m[:, "Отдел"] == "IT", m[:, "Зарплата"])',
                    'm = addcolumn(m, "Итого", sumif(by m[:, "Отдел"], m[:, "Зарплата"]))',
                ],
            },
        },
    },

    # ============================================================
    # COUNTIF
    # ============================================================
    'countif': {
        'name': 'countif',
        'category': 'conditional_agg',
        'signature': 'countif(условие) | countif(by m[:, "X"])',
        'description': (
            'Количество строк по условию.\n'
            '  • Без by — скаляр (сколько строк удовлетворяют).\n'
            '  • С by — вектор (количество строк в группе).\n'
            '  • Работает с Matrix и DuckDB.'
        ),
        'examples': [
            'r = countif(m[:, "Отдел"] == "IT")',
            'r = countif(by m[:, "Отдел"])',
            'm = addcolumn(m, "Всего_в_отделе", countif(by m[:, "Отдел"]))',
        ],
        'errors': {
            'COUNTIF_BAD_SYNTAX': {
                'message': (
                    "countif: неверный синтаксис.\n"
                    "  Нужно условие или by."
                ),
                'wrong': 'countif()',
                'right': 'countif(m[:, "Отдел"] == "IT")',
                'explanation': (
                    "countif принимает ОДИН аргумент:\n"
                    "  • условие → скаляр\n"
                    "  • by m[:, \"X\"] → вектор\n"
                    "\n"
                    "Структура:\n"
                    "  countif(<условие>)\n"
                    "  countif(by <срез-группы>)"
                ),
                'variants': [
                    'r = countif(m[:, "Отдел"] == "IT")',
                    'r = countif(by m[:, "Отдел"])',
                ],
            },
            'COUNTIF_ASSIGN_IN_CONDITION': {
                'message': "countif: в условии нужен '==', а не '='.",
                'wrong': 'countif(m[:, "Отдел"] = "IT")',
                'right': 'countif(m[:, "Отдел"] == "IT")',
                'explanation': "'=' — присваивание, '==' — сравнение.",
                'variants': [
                    'r = countif(m[:, "Отдел"] == "IT")',
                    'r = countif(m[:, "Возраст"] > 25)',
                ],
            },
            'COUNTIF_NO_SLICE': {
                'message': (
                    "countif: нет среза.\n"
                    "  Условие должно быть на срезе m[:, \"X\"]."
                ),
                'wrong': 'countif("Отдел" == "IT")',
                'right': 'countif(m[:, "Отдел"] == "IT")',
                'explanation': (
                    "Срез указывает, к какому столбцу применяется условие.\n"
                    "\n"
                    "Неправильно: countif(\"Отдел\" == \"IT\")\n"
                    "Правильно: countif(m[:, \"Отдел\"] == \"IT\")"
                ),
                'variants': [
                    'r = countif(m[:, "Отдел"] == "IT")',
                    'r = countif(m[2:10, "Отдел"] == "IT")',
                ],
            },
            'COUNTIF_AND_OPERATOR': {
                'message': "countif: логическое И — 'and', не '&&'.",
                'wrong': 'countif(m[:, "Отдел"] == "IT" && m[:, "Возраст"] > 25)',
                'right': 'countif(m[:, "Отдел"] == "IT" and m[:, "Возраст"] > 25)',
                'explanation': "ArrayVator использует СЛОВА: and / or / not.",
                'variants': [
                    'r = countif(m[:, "Отдел"] == "IT" and m[:, "Возраст"] > 25)',
                ],
            },
            'COUNTIF_OR_OPERATOR': {
                'message': "countif: логическое ИЛИ — 'or', не '||'.",
                'wrong': 'countif(m[:, "Отдел"] == "IT" || m[:, "Отдел"] == "HR")',
                'right': 'countif(m[:, "Отдел"] == "IT" or m[:, "Отдел"] == "HR")',
                'explanation': "ArrayVator использует СЛОВА: and / or / not.",
                'variants': [
                    'r = countif(m[:, "Отдел"] == "IT" or m[:, "Отдел"] == "HR")',
                ],
            },
            'COUNTIF_REQUIRES_ASSIGNMENT': {
                'message': (
                    "countif() возвращает значение — сохраните результат."
                ),
                'wrong': 'countif(m[:, "Отдел"] == "IT")',
                'right': 'r = countif(m[:, "Отдел"] == "IT")',
                'explanation': (
                    "countif возвращает значение (скаляр или вектор).\n"
                    "Без присваивания результат теряется."
                ),
                'variants': [
                    'r = countif(m[:, "Отдел"] == "IT")',
                    'm = addcolumn(m, "Всего", countif(by m[:, "Отдел"]))',
                ],
            },
        },
    },

    # ============================================================
    # AVGIF
    # ============================================================
    'avgif': {
        'name': 'avgif',
        'category': 'conditional_agg',
        'signature': 'avgif(условие, срез) | avgif(by m[:, "X"], срез)',
        'description': (
            'Среднее по условию.\n'
            '  • Без by — скаляр.\n'
            '  • С by — вектор (среднее группы для каждой строки).'
        ),
        'examples': [
            'r = avgif(m[:, "Отдел"] == "IT", m[:, "Зарплата"])',
            'm = addcolumn(m, "Среднее_отдел", avgif(by m[:, "Отдел"], m[:, "Зарплата"]))',
        ],
        'errors': {
            'AVGIF_BAD_SYNTAX': {
                'message': (
                    "avgif: неверный синтаксис.\n"
                    "  Нужно условие и срез значений."
                ),
                'wrong': 'avgif(m[:, "Отдел"] == "IT")',
                'right': 'avgif(m[:, "Отдел"] == "IT", m[:, "Зарплата"])',
                'explanation': (
                    "avgif принимает ДВА аргумента:\n"
                    "  1. условие\n"
                    "  2. срез значений\n"
                    "\n"
                    "Структура:\n"
                    "  avgif(<условие>, <срез>)\n"
                    "  avgif(by <срез-группы>, <срез>)"
                ),
                'variants': [
                    'r = avgif(m[:, "Отдел"] == "IT", m[:, "Зарплата"])',
                    'r = avgif(by m[:, "Отдел"], m[:, "Зарплата"])',
                ],
            },
            'AVGIF_ASSIGN_IN_CONDITION': {
                'message': "avgif: в условии нужен '==', а не '='.",
                'wrong': 'avgif(m[:, "Отдел"] = "IT", m[:, "Зарплата"])',
                'right': 'avgif(m[:, "Отдел"] == "IT", m[:, "Зарплата"])',
                'explanation': "'=' — присваивание, '==' — сравнение.",
                'variants': [
                    'r = avgif(m[:, "Отдел"] == "IT", m[:, "Зарплата"])',
                ],
            },
            'AVGIF_BAD_VALUE': {
                'message': (
                    "avgif: второй аргумент должен быть срезом m[:, \"X\"]."
                ),
                'wrong': 'avgif(m[:, "Отдел"] == "IT", "Зарплата")',
                'right': 'avgif(m[:, "Отдел"] == "IT", m[:, "Зарплата"])',
                'explanation': "Второй аргумент — СРЕЗ значений.",
                'variants': [
                    'r = avgif(m[:, "Отдел"] == "IT", m[:, "Зарплата"])',
                ],
            },
            'AVGIF_REQUIRES_ASSIGNMENT': {
                'message': "avgif() возвращает значение — сохраните результат.",
                'wrong': 'avgif(m[:, "Отдел"] == "IT", m[:, "Зарплата"])',
                'right': 'r = avgif(m[:, "Отдел"] == "IT", m[:, "Зарплата"])',
                'explanation': "Без присваивания результат теряется.",
                'variants': [
                    'r = avgif(m[:, "Отдел"] == "IT", m[:, "Зарплата"])',
                    'm = addcolumn(m, "Среднее", avgif(by m[:, "Отдел"], m[:, "Зарплата"]))',
                ],
            },
        },
    },

    # ============================================================
    # MINIF
    # ============================================================
    'minif': {
        'name': 'minif',
        'category': 'conditional_agg',
        'signature': 'minif(условие, срез) | minif(by m[:, "X"], срез)',
        'description': (
            'Минимум по условию.\n'
            '  • Без by — скаляр.\n'
            '  • С by — вектор.'
        ),
        'examples': [
            'r = minif(m[:, "Отдел"] == "IT", m[:, "Зарплата"])',
        ],
        'errors': {
            'MINIF_BAD_SYNTAX': {
                'message': (
                    "minif: неверный синтаксис.\n"
                    "  Нужно условие и срез значений."
                ),
                'wrong': 'minif(m[:, "Отдел"] == "IT")',
                'right': 'minif(m[:, "Отдел"] == "IT", m[:, "Зарплата"])',
                'explanation': (
                    "minif принимает ДВА аргумента:\n"
                    "  1. условие\n"
                    "  2. срез значений"
                ),
                'variants': [
                    'r = minif(m[:, "Отдел"] == "IT", m[:, "Зарплата"])',
                ],
            },
            'MINIF_ASSIGN_IN_CONDITION': {
                'message': "minif: в условии нужен '==', а не '='.",
                'wrong': 'minif(m[:, "Отдел"] = "IT", m[:, "Зарплата"])',
                'right': 'minif(m[:, "Отдел"] == "IT", m[:, "Зарплата"])',
                'explanation': "'=' — присваивание, '==' — сравнение.",
                'variants': ['r = minif(m[:, "Отдел"] == "IT", m[:, "Зарплата"])'],
            },
            'MINIF_REQUIRES_ASSIGNMENT': {
                'message': "minif() возвращает значение — сохраните результат.",
                'wrong': 'minif(m[:, "Отдел"] == "IT", m[:, "Зарплата"])',
                'right': 'r = minif(m[:, "Отдел"] == "IT", m[:, "Зарплата"])',
                'explanation': "Без присваивания результат теряется.",
                'variants': [
                    'r = minif(m[:, "Отдел"] == "IT", m[:, "Зарплата"])',
                ],
            },
        },
    },

    # ============================================================
    # MAXIF
    # ============================================================
    'maxif': {
        'name': 'maxif',
        'category': 'conditional_agg',
        'signature': 'maxif(условие, срез) | maxif(by m[:, "X"], срез)',
        'description': (
            'Максимум по условию.\n'
            '  • Без by — скаляр.\n'
            '  • С by — вектор.'
        ),
        'examples': [
            'r = maxif(m[:, "Отдел"] == "IT", m[:, "Зарплата"])',
        ],
        'errors': {
            'MAXIF_BAD_SYNTAX': {
                'message': (
                    "maxif: неверный синтаксис.\n"
                    "  Нужно условие и срез значений."
                ),
                'wrong': 'maxif(m[:, "Отдел"] == "IT")',
                'right': 'maxif(m[:, "Отдел"] == "IT", m[:, "Зарплата"])',
                'explanation': "maxif(условие, срез-значений)",
                'variants': [
                    'r = maxif(m[:, "Отдел"] == "IT", m[:, "Зарплата"])',
                ],
            },
            'MAXIF_ASSIGN_IN_CONDITION': {
                'message': "maxif: в условии нужен '==', а не '='.",
                'wrong': 'maxif(m[:, "Отдел"] = "IT", m[:, "Зарплата"])',
                'right': 'maxif(m[:, "Отдел"] == "IT", m[:, "Зарплата"])',
                'explanation': "'=' — присваивание, '==' — сравнение.",
                'variants': ['r = maxif(m[:, "Отдел"] == "IT", m[:, "Зарплата"])'],
            },
            'MAXIF_REQUIRES_ASSIGNMENT': {
                'message': "maxif() возвращает значение — сохраните результат.",
                'wrong': 'maxif(m[:, "Отдел"] == "IT", m[:, "Зарплата"])',
                'right': 'r = maxif(m[:, "Отдел"] == "IT", m[:, "Зарплата"])',
                'explanation': "Без присваивания результат теряется.",
                'variants': [
                    'r = maxif(m[:, "Отдел"] == "IT", m[:, "Зарплата"])',
                ],
            },
        },
    },

    # ============================================================
    # MEDIANIF
    # ============================================================
    'medianif': {
        'name': 'medianif',
        'category': 'conditional_agg',
        'signature': 'medianif(условие, срез)',
        'description': (
            'Медиана по условию.\n'
            '  • Возвращает скаляр.\n'
            '  • Работает с Matrix и DuckDB.'
        ),
        'examples': [
            'r = medianif(m[:, "Отдел"] == "IT", m[:, "Зарплата"])',
        ],
        'errors': {
            'MEDIANIF_BAD_SYNTAX': {
                'message': (
                    "medianif: неверный синтаксис.\n"
                    "  Нужно условие и срез значений."
                ),
                'wrong': 'medianif(m[:, "Отдел"] == "IT")',
                'right': 'medianif(m[:, "Отдел"] == "IT", m[:, "Зарплата"])',
                'explanation': (
                    "medianif(условие, срез-значений)\n"
                    "  Возвращает скаляр (медиану)."
                ),
                'variants': [
                    'r = medianif(m[:, "Отдел"] == "IT", m[:, "Зарплата"])',
                ],
            },
            'MEDIANIF_ASSIGN_IN_CONDITION': {
                'message': "medianif: в условии нужен '==', а не '='.",
                'wrong': 'medianif(m[:, "Отдел"] = "IT", m[:, "Зарплата"])',
                'right': 'medianif(m[:, "Отдел"] == "IT", m[:, "Зарплата"])',
                'explanation': "'=' — присваивание, '==' — сравнение.",
                'variants': ['r = medianif(m[:, "Отдел"] == "IT", m[:, "Зарплата"])'],
            },
            'MEDIANIF_REQUIRES_ASSIGNMENT': {
                'message': "medianif() возвращает значение — сохраните результат.",
                'wrong': 'medianif(m[:, "Отдел"] == "IT", m[:, "Зарплата"])',
                'right': 'r = medianif(m[:, "Отдел"] == "IT", m[:, "Зарплата"])',
                'explanation': "Без присваивания результат теряется.",
                'variants': [
                    'r = medianif(m[:, "Отдел"] == "IT", m[:, "Зарплата"])',
                ],
            },
        },
    },

    # ============================================================
    # COUNTUNIQUEIF
    # ============================================================
    'countuniqueif': {
        'name': 'countuniqueif',
        'category': 'conditional_agg',
        'signature': 'countuniqueif(условие, срез)',
        'description': (
            'Количество уникальных значений по условию.\n'
            '  • Возвращает скаляр.'
        ),
        'examples': [
            'r = countuniqueif(m[:, "Отдел"] == "IT", m[:, "Город"])',
        ],
        'errors': {
            'COUNTUNIQUEIF_BAD_SYNTAX': {
                'message': (
                    "countuniqueif: неверный синтаксис.\n"
                    "  Нужно условие и срез значений."
                ),
                'wrong': 'countuniqueif(m[:, "Отдел"] == "IT")',
                'right': 'countuniqueif(m[:, "Отдел"] == "IT", m[:, "Город"])',
                'explanation': (
                    "countuniqueif(условие, срез-значений)\n"
                    "  Считает УНИКАЛЬНЫЕ значения."
                ),
                'variants': [
                    'r = countuniqueif(m[:, "Отдел"] == "IT", m[:, "Город"])',
                ],
            },
            'COUNTUNIQUEIF_ASSIGN_IN_CONDITION': {
                'message': "countuniqueif: в условии нужен '==', а не '='.",
                'wrong': 'countuniqueif(m[:, "Отдел"] = "IT", m[:, "Город"])',
                'right': 'countuniqueif(m[:, "Отдел"] == "IT", m[:, "Город"])',
                'explanation': "'=' — присваивание, '==' — сравнение.",
                'variants': [
                    'r = countuniqueif(m[:, "Отдел"] == "IT", m[:, "Город"])',
                ],
            },
            'COUNTUNIQUEIF_REQUIRES_ASSIGNMENT': {
                'message': "countuniqueif() возвращает значение — сохраните результат.",
                'wrong': 'countuniqueif(m[:, "Отдел"] == "IT", m[:, "Город"])',
                'right': 'r = countuniqueif(m[:, "Отдел"] == "IT", m[:, "Город"])',
                'explanation': "Без присваивания результат теряется.",
                'variants': [
                    'r = countuniqueif(m[:, "Отдел"] == "IT", m[:, "Город"])',
                ],
            },
        },
    },

    # ============================================================
    # SUMPRODUCT
    # ============================================================
    'sumproduct': {
        'name': 'sumproduct',
        'category': 'conditional_agg',
        'signature': 'sumproduct(срез1, срез2 [, срез3, ...])',
        'description': (
            'Сумма произведений элементов по строкам.\n'
            '  • Возвращает скаляр.\n'
            '  • Срезы должны быть из одной таблицы.'
        ),
        'examples': [
            'r = sumproduct(m[:, "Цена"], m[:, "Количество"])',
            'r = sumproduct(m[:, "A"], m[:, "B"], m[:, "C"])',
        ],
        'errors': {
            'SUMPRODUCT_BAD_SYNTAX': {
                'message': (
                    "sumproduct: неверный синтаксис.\n"
                    "  Нужно минимум два среза."
                ),
                'wrong': 'sumproduct(m[:, "Цена"])',
                'right': 'sumproduct(m[:, "Цена"], m[:, "Количество"])',
                'explanation': (
                    "sumproduct принимает МИНИМУМ ДВА среза:\n"
                    "  sumproduct(срез1, срез2)\n"
                    "  sumproduct(срез1, срез2, срез3, ...)\n"
                    "\n"
                    "Для каждой строки перемножает значения,\n"
                    "затем суммирует все произведения."
                ),
                'variants': [
                    'r = sumproduct(m[:, "Цена"], m[:, "Количество"])',
                    'r = sumproduct(m[:, "A"], m[:, "B"], m[:, "C"])',
                ],
            },
            'SUMPRODUCT_BAD_ARG': {
                'message': (
                    "sumproduct: аргументы — срезы m[:, \"X\"].\n"
                    "  Не строки, не числа."
                ),
                'wrong': 'sumproduct("Цена", "Количество")',
                'right': 'sumproduct(m[:, "Цена"], m[:, "Количество"])',
                'explanation': (
                    "Каждый аргумент — СРЕЗ столбца:\n"
                    "  sumproduct(m[:, \"Цена\"], m[:, \"Количество\"])"
                ),
                'variants': [
                    'r = sumproduct(m[:, "Цена"], m[:, "Количество"])',
                ],
            },
            'SUMPRODUCT_REQUIRES_ASSIGNMENT': {
                'message': "sumproduct() возвращает значение — сохраните результат.",
                'wrong': 'sumproduct(m[:, "Цена"], m[:, "Количество"])',
                'right': 'r = sumproduct(m[:, "Цена"], m[:, "Количество"])',
                'explanation': "Без присваивания результат теряется.",
                'variants': [
                    'r = sumproduct(m[:, "Цена"], m[:, "Количество"])',
                ],
            },
        },
    },
}


EN = {
    # SUMIF
    'sumif': {
        'name': 'sumif',
        'category': 'conditional_agg',
        'signature': 'sumif(condition, slice) | sumif(by m[:, "X"], slice)',
        'description': (
            'Sum by condition.\n'
            '  • Without by — scalar (one number).\n'
            '  • With by — vector (group sum for each row).\n'
            '  • Works with Matrix and DuckDB.\n'
            '  • Returns a value — save the result.'
        ),
        'examples': [
            'r = sumif(m[:, "Department"] == "IT", m[:, "Salary"])',
            'r = sumif(m[:, "Age"] > 25, m[:, "Salary"])',
            'm = addcolumn(m, "Total_by_dept", sumif(by m[:, "Department"], m[:, "Salary"]))',
        ],
        'errors': {
            'SUMIF_BAD_SYNTAX': {
                'message': (
                    "sumif: invalid syntax.\n"
                    "  Need a condition and a value slice."
                ),
                'wrong': 'sumif(m[:, "Department"] == "IT")',
                'right': 'sumif(m[:, "Department"] == "IT", m[:, "Salary"])',
                'explanation': (
                    "sumif takes TWO arguments:\n"
                    "  1. condition\n"
                    "  2. value slice\n"
                    "\n"
                    "Scalar structure:\n"
                    "  sumif(<condition>, <value-slice>)\n"
                    "\n"
                    "Vector structure:\n"
                    "  sumif(by <group-slice>, <value-slice>)"
                ),
                'variants': [
                    'r = sumif(m[:, "Department"] == "IT", m[:, "Salary"])',
                    'r = sumif(by m[:, "Department"], m[:, "Salary"])',
                ],
            },
            'SUMIF_ASSIGN_IN_CONDITION': {
                'message': (
                    "sumif: use '==' (comparison), not '=' (assignment)."
                ),
                'wrong': 'sumif(m[:, "Department"] = "IT", m[:, "Salary"])',
                'right': 'sumif(m[:, "Department"] == "IT", m[:, "Salary"])',
                'explanation': (
                    "'=' — assigns.\n"
                    "'==' — compares.\n"
                    "\n"
                    "In sumif condition ALWAYS '=='."
                ),
                'variants': [
                    'r = sumif(m[:, "Department"] == "IT", m[:, "Salary"])',
                    'r = sumif(m[:, "Age"] > 25, m[:, "Salary"])',
                ],
            },
            'SUMIF_AND_OPERATOR': {
                'message': "sumif: logical AND is 'and', not '&&'.",
                'wrong': 'sumif(m[:, "Department"] == "IT" && m[:, "Age"] > 25, m[:, "Salary"])',
                'right': 'sumif(m[:, "Department"] == "IT" and m[:, "Age"] > 25, m[:, "Salary"])',
                'explanation': "ArrayVator uses WORDS: and / or / not.",
                'variants': [
                    'r = sumif(m[:, "Department"] == "IT" and m[:, "Age"] > 25, m[:, "Salary"])',
                ],
            },
            'SUMIF_OR_OPERATOR': {
                'message': "sumif: logical OR is 'or', not '||'.",
                'wrong': 'sumif(m[:, "Department"] == "IT" || m[:, "Department"] == "HR", m[:, "Salary"])',
                'right': 'sumif(m[:, "Department"] == "IT" or m[:, "Department"] == "HR", m[:, "Salary"])',
                'explanation': "ArrayVator uses WORDS: and / or / not.",
                'variants': [
                    'r = sumif(m[:, "Department"] == "IT" or m[:, "Department"] == "HR", m[:, "Salary"])',
                ],
            },
            'SUMIF_NO_SLICE': {
                'message': (
                    "sumif: no slice.\n"
                    "  Condition must be on a slice m[:, \"X\"]."
                ),
                'wrong': 'sumif("Department" == "IT", m[:, "Salary"])',
                'right': 'sumif(m[:, "Department"] == "IT", m[:, "Salary"])',
                'explanation': (
                    "The slice specifies which column the condition applies to.\n"
                    "\n"
                    "Incorrect: sumif(\"Department\" == \"IT\", ...)\n"
                    "Correct: sumif(m[:, \"Department\"] == \"IT\", ...)"
                ),
                'variants': [
                    'r = sumif(m[:, "Department"] == "IT", m[:, "Salary"])',
                    'r = sumif(m[2:10, "Department"] == "IT", m[:, "Salary"])',
                ],
            },
            'SUMIF_BAD_VALUE': {
                'message': (
                    "sumif: 2nd argument must be a slice m[:, \"X\"].\n"
                    "  Not a string name, not a number."
                ),
                'wrong': 'sumif(m[:, "Department"] == "IT", "Salary")',
                'right': 'sumif(m[:, "Department"] == "IT", m[:, "Salary"])',
                'explanation': (
                    "Value slice is a SLICE, not a column name.\n"
                    "\n"
                    "Incorrect:\n"
                    "     sumif(..., \"Salary\")\n"
                    "     sumif(..., 5)\n"
                    "\n"
                    "Correct:\n"
                    "     sumif(..., m[:, \"Salary\"])\n"
                    "     sumif(..., m[:, 5])"
                ),
                'variants': [
                    'r = sumif(m[:, "Department"] == "IT", m[:, "Salary"])',
                    'r = sumif(m[:, "Department"] == "IT", m[:, 5])',
                ],
            },
            'SUMIF_BY_NOT_SLICE': {
                'message': "sumif: by requires a slice m[:, \"X\"].",
                'wrong': 'sumif(by "Department", m[:, "Salary"])',
                'right': 'sumif(by m[:, "Department"], m[:, "Salary"])',
                'explanation': (
                    "by takes a column SLICE of the grouping column:\n"
                    "     by m[:, \"Department\"]\n"
                    "     by m[:, 3]"
                ),
                'variants': [
                    'r = sumif(by m[:, "Department"], m[:, "Salary"])',
                    'r = sumif(by m[:, 3], m[:, 5])',
                ],
            },
            'SUMIF_REQUIRES_ASSIGNMENT': {
                'message': "sumif() returns a value — save the result.",
                'wrong': 'sumif(m[:, "Department"] == "IT", m[:, "Salary"])',
                'right': 'r = sumif(m[:, "Department"] == "IT", m[:, "Salary"])',
                'explanation': (
                    "sumif returns a value (scalar or vector).\n"
                    "Without assignment the result is lost.\n"
                    "\n"
                    "Correct:\n"
                    "  r = sumif(...)                            — to a variable\n"
                    "  m = addcolumn(m, \"X\", sumif(...))         — to a column\n"
                    "  print(sumif(...))                          — output"
                ),
                'variants': [
                    'r = sumif(m[:, "Department"] == "IT", m[:, "Salary"])',
                    'm = addcolumn(m, "Total", sumif(by m[:, "Department"], m[:, "Salary"]))',
                ],
            },
        },
    },

    # COUNTIF
    'countif': {
        'name': 'countif',
        'category': 'conditional_agg',
        'signature': 'countif(condition) | countif(by m[:, "X"])',
        'description': (
            'Count rows by condition.\n'
            '  • Without by — scalar (how many rows match).\n'
            '  • With by — vector (count per group).\n'
            '  • Works with Matrix and DuckDB.'
        ),
        'examples': [
            'r = countif(m[:, "Department"] == "IT")',
            'r = countif(by m[:, "Department"])',
            'm = addcolumn(m, "Total_in_dept", countif(by m[:, "Department"]))',
        ],
        'errors': {
            'COUNTIF_BAD_SYNTAX': {
                'message': (
                    "countif: invalid syntax.\n"
                    "  Need a condition or by."
                ),
                'wrong': 'countif()',
                'right': 'countif(m[:, "Department"] == "IT")',
                'explanation': (
                    "countif takes ONE argument:\n"
                    "  • condition → scalar\n"
                    "  • by m[:, \"X\"] → vector\n"
                    "\n"
                    "Structure:\n"
                    "  countif(<condition>)\n"
                    "  countif(by <group-slice>)"
                ),
                'variants': [
                    'r = countif(m[:, "Department"] == "IT")',
                    'r = countif(by m[:, "Department"])',
                ],
            },
            'COUNTIF_ASSIGN_IN_CONDITION': {
                'message': "countif: use '==', not '='.",
                'wrong': 'countif(m[:, "Department"] = "IT")',
                'right': 'countif(m[:, "Department"] == "IT")',
                'explanation': "'=' — assigns, '==' — compares.",
                'variants': [
                    'r = countif(m[:, "Department"] == "IT")',
                    'r = countif(m[:, "Age"] > 25)',
                ],
            },
            'COUNTIF_NO_SLICE': {
                'message': (
                    "countif: no slice.\n"
                    "  Condition must be on a slice m[:, \"X\"]."
                ),
                'wrong': 'countif("Department" == "IT")',
                'right': 'countif(m[:, "Department"] == "IT")',
                'explanation': (
                    "The slice specifies which column the condition applies to.\n"
                    "\n"
                    "Incorrect: countif(\"Department\" == \"IT\")\n"
                    "Correct: countif(m[:, \"Department\"] == \"IT\")"
                ),
                'variants': [
                    'r = countif(m[:, "Department"] == "IT")',
                    'r = countif(m[2:10, "Department"] == "IT")',
                ],
            },
            'COUNTIF_AND_OPERATOR': {
                'message': "countif: logical AND is 'and', not '&&'.",
                'wrong': 'countif(m[:, "Department"] == "IT" && m[:, "Age"] > 25)',
                'right': 'countif(m[:, "Department"] == "IT" and m[:, "Age"] > 25)',
                'explanation': "ArrayVator uses WORDS: and / or / not.",
                'variants': [
                    'r = countif(m[:, "Department"] == "IT" and m[:, "Age"] > 25)',
                ],
            },
            'COUNTIF_OR_OPERATOR': {
                'message': "countif: logical OR is 'or', not '||'.",
                'wrong': 'countif(m[:, "Department"] == "IT" || m[:, "Department"] == "HR")',
                'right': 'countif(m[:, "Department"] == "IT" or m[:, "Department"] == "HR")',
                'explanation': "ArrayVator uses WORDS: and / or / not.",
                'variants': [
                    'r = countif(m[:, "Department"] == "IT" or m[:, "Department"] == "HR")',
                ],
            },
            'COUNTIF_REQUIRES_ASSIGNMENT': {
                'message': "countif() returns a value — save the result.",
                'wrong': 'countif(m[:, "Department"] == "IT")',
                'right': 'r = countif(m[:, "Department"] == "IT")',
                'explanation': (
                    "countif returns a value (scalar or vector).\n"
                    "Without assignment the result is lost."
                ),
                'variants': [
                    'r = countif(m[:, "Department"] == "IT")',
                    'm = addcolumn(m, "Total", countif(by m[:, "Department"]))',
                ],
            },
        },
    },

    # AVGIF
    'avgif': {
        'name': 'avgif',
        'category': 'conditional_agg',
        'signature': 'avgif(condition, slice) | avgif(by m[:, "X"], slice)',
        'description': (
            'Average by condition.\n'
            '  • Without by — scalar.\n'
            '  • With by — vector (group average for each row).'
        ),
        'examples': [
            'r = avgif(m[:, "Department"] == "IT", m[:, "Salary"])',
            'm = addcolumn(m, "Avg_by_dept", avgif(by m[:, "Department"], m[:, "Salary"]))',
        ],
        'errors': {
            'AVGIF_BAD_SYNTAX': {
                'message': (
                    "avgif: invalid syntax.\n"
                    "  Need a condition and a value slice."
                ),
                'wrong': 'avgif(m[:, "Department"] == "IT")',
                'right': 'avgif(m[:, "Department"] == "IT", m[:, "Salary"])',
                'explanation': (
                    "avgif takes TWO arguments:\n"
                    "  1. condition\n"
                    "  2. value slice"
                ),
                'variants': [
                    'r = avgif(m[:, "Department"] == "IT", m[:, "Salary"])',
                    'r = avgif(by m[:, "Department"], m[:, "Salary"])',
                ],
            },
            'AVGIF_ASSIGN_IN_CONDITION': {
                'message': "avgif: use '==', not '='.",
                'wrong': 'avgif(m[:, "Department"] = "IT", m[:, "Salary"])',
                'right': 'avgif(m[:, "Department"] == "IT", m[:, "Salary"])',
                'explanation': "'=' — assigns, '==' — compares.",
                'variants': [
                    'r = avgif(m[:, "Department"] == "IT", m[:, "Salary"])',
                ],
            },
            'AVGIF_BAD_VALUE': {
                'message': "avgif: 2nd argument must be a slice m[:, \"X\"].",
                'wrong': 'avgif(m[:, "Department"] == "IT", "Salary")',
                'right': 'avgif(m[:, "Department"] == "IT", m[:, "Salary"])',
                'explanation': "2nd argument is a value SLICE.",
                'variants': [
                    'r = avgif(m[:, "Department"] == "IT", m[:, "Salary"])',
                ],
            },
            'AVGIF_REQUIRES_ASSIGNMENT': {
                'message': "avgif() returns a value — save the result.",
                'wrong': 'avgif(m[:, "Department"] == "IT", m[:, "Salary"])',
                'right': 'r = avgif(m[:, "Department"] == "IT", m[:, "Salary"])',
                'explanation': "Without assignment the result is lost.",
                'variants': [
                    'r = avgif(m[:, "Department"] == "IT", m[:, "Salary"])',
                    'm = addcolumn(m, "Avg", avgif(by m[:, "Department"], m[:, "Salary"]))',
                ],
            },
        },
    },

    # MINIF
    'minif': {
        'name': 'minif',
        'category': 'conditional_agg',
        'signature': 'minif(condition, slice) | minif(by m[:, "X"], slice)',
        'description': 'Minimum by condition. Scalar or vector.',
        'examples': ['r = minif(m[:, "Department"] == "IT", m[:, "Salary"])'],
        'errors': {
            'MINIF_BAD_SYNTAX': {
                'message': "minif: invalid syntax. Need condition and value slice.",
                'wrong': 'minif(m[:, "Department"] == "IT")',
                'right': 'minif(m[:, "Department"] == "IT", m[:, "Salary"])',
                'explanation': "minif(condition, value-slice)",
                'variants': ['r = minif(m[:, "Department"] == "IT", m[:, "Salary"])'],
            },
            'MINIF_ASSIGN_IN_CONDITION': {
                'message': "minif: use '==', not '='.",
                'wrong': 'minif(m[:, "Department"] = "IT", m[:, "Salary"])',
                'right': 'minif(m[:, "Department"] == "IT", m[:, "Salary"])',
                'explanation': "'=' — assigns, '==' — compares.",
                'variants': ['r = minif(m[:, "Department"] == "IT", m[:, "Salary"])'],
            },
            'MINIF_REQUIRES_ASSIGNMENT': {
                'message': "minif() returns a value — save the result.",
                'wrong': 'minif(m[:, "Department"] == "IT", m[:, "Salary"])',
                'right': 'r = minif(m[:, "Department"] == "IT", m[:, "Salary"])',
                'explanation': "Without assignment the result is lost.",
                'variants': ['r = minif(m[:, "Department"] == "IT", m[:, "Salary"])'],
            },
        },
    },

    # MAXIF
    'maxif': {
        'name': 'maxif',
        'category': 'conditional_agg',
        'signature': 'maxif(condition, slice) | maxif(by m[:, "X"], slice)',
        'description': 'Maximum by condition. Scalar or vector.',
        'examples': ['r = maxif(m[:, "Department"] == "IT", m[:, "Salary"])'],
        'errors': {
            'MAXIF_BAD_SYNTAX': {
                'message': "maxif: invalid syntax. Need condition and value slice.",
                'wrong': 'maxif(m[:, "Department"] == "IT")',
                'right': 'maxif(m[:, "Department"] == "IT", m[:, "Salary"])',
                'explanation': "maxif(condition, value-slice)",
                'variants': ['r = maxif(m[:, "Department"] == "IT", m[:, "Salary"])'],
            },
            'MAXIF_ASSIGN_IN_CONDITION': {
                'message': "maxif: use '==', not '='.",
                'wrong': 'maxif(m[:, "Department"] = "IT", m[:, "Salary"])',
                'right': 'maxif(m[:, "Department"] == "IT", m[:, "Salary"])',
                'explanation': "'=' — assigns, '==' — compares.",
                'variants': ['r = maxif(m[:, "Department"] == "IT", m[:, "Salary"])'],
            },
            'MAXIF_REQUIRES_ASSIGNMENT': {
                'message': "maxif() returns a value — save the result.",
                'wrong': 'maxif(m[:, "Department"] == "IT", m[:, "Salary"])',
                'right': 'r = maxif(m[:, "Department"] == "IT", m[:, "Salary"])',
                'explanation': "Without assignment the result is lost.",
                'variants': ['r = maxif(m[:, "Department"] == "IT", m[:, "Salary"])'],
            },
        },
    },

    # MEDIANIF
    'medianif': {
        'name': 'medianif',
        'category': 'conditional_agg',
        'signature': 'medianif(condition, slice)',
        'description': 'Median by condition. Returns a scalar.',
        'examples': ['r = medianif(m[:, "Department"] == "IT", m[:, "Salary"])'],
        'errors': {
            'MEDIANIF_BAD_SYNTAX': {
                'message': "medianif: invalid syntax. Need condition and value slice.",
                'wrong': 'medianif(m[:, "Department"] == "IT")',
                'right': 'medianif(m[:, "Department"] == "IT", m[:, "Salary"])',
                'explanation': "medianif(condition, value-slice) — returns a scalar.",
                'variants': ['r = medianif(m[:, "Department"] == "IT", m[:, "Salary"])'],
            },
            'MEDIANIF_ASSIGN_IN_CONDITION': {
                'message': "medianif: use '==', not '='.",
                'wrong': 'medianif(m[:, "Department"] = "IT", m[:, "Salary"])',
                'right': 'medianif(m[:, "Department"] == "IT", m[:, "Salary"])',
                'explanation': "'=' — assigns, '==' — compares.",
                'variants': ['r = medianif(m[:, "Department"] == "IT", m[:, "Salary"])'],
            },
            'MEDIANIF_REQUIRES_ASSIGNMENT': {
                'message': "medianif() returns a value — save the result.",
                'wrong': 'medianif(m[:, "Department"] == "IT", m[:, "Salary"])',
                'right': 'r = medianif(m[:, "Department"] == "IT", m[:, "Salary"])',
                'explanation': "Without assignment the result is lost.",
                'variants': ['r = medianif(m[:, "Department"] == "IT", m[:, "Salary"])'],
            },
        },
    },

    # COUNTUNIQUEIF
    'countuniqueif': {
        'name': 'countuniqueif',
        'category': 'conditional_agg',
        'signature': 'countuniqueif(condition, slice)',
        'description': 'Count unique values by condition. Scalar.',
        'examples': ['r = countuniqueif(m[:, "Department"] == "IT", m[:, "City"])'],
        'errors': {
            'COUNTUNIQUEIF_BAD_SYNTAX': {
                'message': "countuniqueif: invalid syntax. Need condition and value slice.",
                'wrong': 'countuniqueif(m[:, "Department"] == "IT")',
                'right': 'countuniqueif(m[:, "Department"] == "IT", m[:, "City"])',
                'explanation': "countuniqueif(condition, value-slice) — counts unique.",
                'variants': ['r = countuniqueif(m[:, "Department"] == "IT", m[:, "City"])'],
            },
            'COUNTUNIQUEIF_ASSIGN_IN_CONDITION': {
                'message': "countuniqueif: use '==', not '='.",
                'wrong': 'countuniqueif(m[:, "Department"] = "IT", m[:, "City"])',
                'right': 'countuniqueif(m[:, "Department"] == "IT", m[:, "City"])',
                'explanation': "'=' — assigns, '==' — compares.",
                'variants': ['r = countuniqueif(m[:, "Department"] == "IT", m[:, "City"])'],
            },
            'COUNTUNIQUEIF_REQUIRES_ASSIGNMENT': {
                'message': "countuniqueif() returns a value — save the result.",
                'wrong': 'countuniqueif(m[:, "Department"] == "IT", m[:, "City"])',
                'right': 'r = countuniqueif(m[:, "Department"] == "IT", m[:, "City"])',
                'explanation': "Without assignment the result is lost.",
                'variants': ['r = countuniqueif(m[:, "Department"] == "IT", m[:, "City"])'],
            },
        },
    },

    # SUMPRODUCT
    'sumproduct': {
        'name': 'sumproduct',
        'category': 'conditional_agg',
        'signature': 'sumproduct(slice1, slice2 [, slice3, ...])',
        'description': (
            'Sum of row-wise products. Scalar.\n'
            '  • Slices must be from the same table.'
        ),
        'examples': [
            'r = sumproduct(m[:, "Price"], m[:, "Quantity"])',
            'r = sumproduct(m[:, "A"], m[:, "B"], m[:, "C"])',
        ],
        'errors': {
            'SUMPRODUCT_BAD_SYNTAX': {
                'message': "sumproduct: invalid syntax. Need at least two slices.",
                'wrong': 'sumproduct(m[:, "Price"])',
                'right': 'sumproduct(m[:, "Price"], m[:, "Quantity"])',
                'explanation': (
                    "sumproduct takes at least TWO slices:\n"
                    "  sumproduct(slice1, slice2)\n"
                    "  sumproduct(slice1, slice2, slice3, ...)\n"
                    "\n"
                    "For each row multiplies values,\n"
                    "then sums all products."
                ),
                'variants': [
                    'r = sumproduct(m[:, "Price"], m[:, "Quantity"])',
                    'r = sumproduct(m[:, "A"], m[:, "B"], m[:, "C"])',
                ],
            },
            'SUMPRODUCT_BAD_ARG': {
                'message': "sumproduct: arguments must be slices m[:, \"X\"].",
                'wrong': 'sumproduct("Price", "Quantity")',
                'right': 'sumproduct(m[:, "Price"], m[:, "Quantity"])',
                'explanation': (
                    "Each argument is a column SLICE:\n"
                    "  sumproduct(m[:, \"Price\"], m[:, \"Quantity\"])"
                ),
                'variants': [
                    'r = sumproduct(m[:, "Price"], m[:, "Quantity"])',
                ],
            },
            'SUMPRODUCT_REQUIRES_ASSIGNMENT': {
                'message': "sumproduct() returns a value — save the result.",
                'wrong': 'sumproduct(m[:, "Price"], m[:, "Quantity"])',
                'right': 'r = sumproduct(m[:, "Price"], m[:, "Quantity"])',
                'explanation': "Without assignment the result is lost.",
                'variants': [
                    'r = sumproduct(m[:, "Price"], m[:, "Quantity"])',
                ],
            },
        },
    },
}