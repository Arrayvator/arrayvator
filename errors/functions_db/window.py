# errors/functions_db/window.py
"""
База ошибок для оконных функций.

ФУНКЦИИ НАД ТАБЛИЦЕЙ:
    rownumber, rank, denserank, percentrank, cumedist, ntile

ФУНКЦИИ НАД СТОЛБЦОМ:
    lag, lead, firstvalue, lastvalue, nthvalue,
    winsum, winavg, wincount, winmin, winmax,
    winmedian, winstdev

ФИЛЬТР:
    qualify

ОБЩИЕ ПРАВИЛА:
    by m[:, "X"]     — партиция (группа)
    order m[:, "Y"]  — сортировка внутри группы
    AZ / ZA          — направление сортировки
"""


RU = {
    # ============================================================
    # ROWNUMBER
    # ============================================================
    'rownumber': {
        'name': 'rownumber',
        'category': 'window',
        'signature': 'rownumber(m [, by m[:, "X"]] [, order m[:, "Y"]] [, AZ|ZA])',
        'description': (
            'Номер строки внутри группы.\n'
            '  • 1, 2, 3, 4, ...\n'
            '  • Без by — вся таблица одна группа.\n'
            '  • Без order — порядок строк как есть.\n'
            '  • Возвращает МАТРИЦУ с добавленным столбцом __rownumber.'
        ),
        'examples': [
            'r = rownumber(m)',
            'r = rownumber(m, by m[:, "Отдел"])',
            'r = rownumber(m, order m[:, "Зарплата"], ZA)',
            'r = rownumber(m, by m[:, "Отдел"], order m[:, "Зарплата"], ZA)',
        ],
        'errors': {
            'WINDOW_BAD_SYNTAX': {
                'message': (
                    "rownumber: неверный синтаксис.\n"
                    "  Нужна матрица и опциональные by/order."
                ),
                'wrong': 'rownumber()',
                'right': 'rownumber(m, by m[:, "Отдел"], order m[:, "Зарплата"], ZA)',
                'explanation': (
                    "Структура:\n"
                    "  rownumber(m)\n"
                    "  rownumber(m, by m[:, \"X\"])\n"
                    "  rownumber(m, order m[:, \"Y\"], ZA)\n"
                    "  rownumber(m, by m[:, \"X\"], order m[:, \"Y\"], ZA)"
                ),
                'variants': [
                    'r = rownumber(m)',
                    'r = rownumber(m, by m[:, "Отдел"], order m[:, "Зарплата"], ZA)',
                ],
            },
            'WINDOW_NEED_TABLE': {
                'message': (
                    "rownumber: 1-й аргумент — таблица (переменная).\n"
                    "  Не срез и не скаляр."
                ),
                'wrong': 'rownumber(m[:, "Отдел"])',
                'right': 'rownumber(m, by m[:, "Отдел"])',
                'explanation': (
                    "rownumber работает над ВСЕЙ таблицей,\n"
                    "поэтому первый аргумент — переменная-таблица.\n"
                    "А столбцы для партиции и сортировки указываются\n"
                    "внутри by и order.\n"
                    "\n"
                    "Неправильно:\n"
                    "     rownumber(m[:, \"Отдел\"])\n"
                    "\n"
                    "Правильно:\n"
                    "     rownumber(m, by m[:, \"Отдел\"])"
                ),
                'variants': [
                    'r = rownumber(m, by m[:, "Отдел"], order m[:, "Зарплата"], ZA)',
                    'r = rownumber(m)',
                ],
            },
            'WINDOW_BAD_BY': {
                'message': (
                    "rownumber: by должен быть срезом m[:, \"X\"]."
                ),
                'wrong': 'rownumber(m, by "Отдел")',
                'right': 'rownumber(m, by m[:, "Отдел"])',
                'explanation': (
                    "by принимает СРЕЗ столбца:\n"
                    "     by m[:, \"Отдел\"]\n"
                    "     by m[:, 3]\n"
                    "\n"
                    "Не строку и не число:\n"
                    "     by \"Отдел\"  ❌\n"
                    "     by 3         ❌"
                ),
                'variants': [
                    'r = rownumber(m, by m[:, "Отдел"])',
                    'r = rownumber(m, by m[:, 3])',
                ],
            },
            'WINDOW_BAD_ORDER': {
                'message': (
                    "rownumber: order должен быть срезом m[:, \"X\"]."
                ),
                'wrong': 'rownumber(m, order "Зарплата", ZA)',
                'right': 'rownumber(m, order m[:, "Зарплата"], ZA)',
                'explanation': (
                    "order принимает СРЕЗ столбца:\n"
                    "     order m[:, \"Зарплата\"]\n"
                    "     order m[:, 5]"
                ),
                'variants': [
                    'r = rownumber(m, order m[:, "Зарплата"], ZA)',
                    'r = rownumber(m, order m[:, 5], AZ)',
                ],
            },
            'WINDOW_BAD_DIRECTION': {
                'message': (
                    "rownumber: направление сортировки — AZ или ZA."
                ),
                'wrong': 'rownumber(m, order m[:, "Зарплата"], UP)',
                'right': 'rownumber(m, order m[:, "Зарплата"], ZA)',
                'explanation': (
                    "AZ — по возрастанию.\n"
                    "ZA — по убыванию.\n"
                    "\n"
                    "НЕ:\n"
                    "     UP, DOWN, ASC, DESC"
                ),
                'variants': [
                    'r = rownumber(m, order m[:, "Зарплата"], AZ)',
                    'r = rownumber(m, order m[:, "Зарплата"], ZA)',
                ],
            },
            'WINDOW_REQUIRES_ASSIGNMENT': {
                'message': (
                    "rownumber() возвращает значение — "
                    "результат нужно сохранить."
                ),
                'wrong': 'rownumber(m, by m[:, "Отдел"])',
                'right': 'r = rownumber(m, by m[:, "Отдел"])',
                'explanation': (
                    "Оконные функции НЕ изменяют исходную матрицу.\n"
                    "Они ВОЗВРАЩАЮТ НОВУЮ (с добавленным столбцом).\n"
                    "\n"
                    "Правильно:\n"
                    "  r = rownumber(...)     — в новую переменную\n"
                    "  m = rownumber(...)     — мутация"
                ),
                'variants': [
                    'r = rownumber(m, by m[:, "Отдел"])',
                    'm = rownumber(m, by m[:, "Отдел"])',
                ],
            },
        },
    },

    # ============================================================
    # RANK
    # ============================================================
    'rank': {
        'name': 'rank',
        'category': 'window',
        'signature': 'rank(m [, by m[:, "X"]] [, order m[:, "Y"]] [, AZ|ZA])',
        'description': (
            'Ранг строки внутри группы.\n'
            '  • 1, 2, 2, 4 — пропускает после повторов.\n'
            '  • Столбец результата: __rank.\n'
            '  • Возвращает МАТРИЦУ.'
        ),
        'examples': [
            'r = rank(m, by m[:, "Отдел"], order m[:, "Зарплата"], ZA)',
        ],
        'errors': {
            'WINDOW_BAD_SYNTAX': {
                'message': "rank: неверный синтаксис.",
                'wrong': 'rank()',
                'right': 'rank(m, by m[:, "Отдел"], order m[:, "Зарплата"], ZA)',
                'explanation': (
                    "Структура:\n"
                    "  rank(m, by m[:, \"X\"], order m[:, \"Y\"], ZA)"
                ),
                'variants': [
                    'r = rank(m, by m[:, "Отдел"], order m[:, "Зарплата"], ZA)',
                ],
            },
            'WINDOW_NEED_TABLE': {
                'message': "rank: 1-й аргумент — таблица.",
                'wrong': 'rank(m[:, "Отдел"])',
                'right': 'rank(m, by m[:, "Отдел"])',
                'explanation': "Первый аргумент — переменная-таблица.",
                'variants': [
                    'r = rank(m, by m[:, "Отдел"], order m[:, "Зарплата"], ZA)',
                ],
            },
            'WINDOW_REQUIRES_ASSIGNMENT': {
                'message': "rank() возвращает значение — результат нужно сохранить.",
                'wrong': 'rank(m, by m[:, "Отдел"])',
                'right': 'r = rank(m, by m[:, "Отдел"])',
                'explanation': "rank НЕ мутирует, возвращает новую матрицу.",
                'variants': [
                    'r = rank(m, by m[:, "Отдел"])',
                    'm = rank(m, by m[:, "Отдел"])',
                ],
            },
        },
    },

    # ============================================================
    # DENSERANK
    # ============================================================
    'denserank': {
        'name': 'denserank',
        'category': 'window',
        'signature': 'denserank(m [, by m[:, "X"]] [, order m[:, "Y"]] [, AZ|ZA])',
        'description': (
            'Плотный ранг (без пропусков).\n'
            '  • 1, 2, 2, 3 — не пропускает после повторов.\n'
            '  • Столбец результата: __denserank.\n'
            '  • Возвращает МАТРИЦУ.'
        ),
        'examples': [
            'r = denserank(m, by m[:, "Отдел"], order m[:, "Зарплата"], ZA)',
        ],
        'errors': {
            'WINDOW_BAD_SYNTAX': {
                'message': "denserank: неверный синтаксис.",
                'wrong': 'denserank()',
                'right': 'denserank(m, by m[:, "Отдел"], order m[:, "Зарплата"], ZA)',
                'explanation': "Структура: denserank(m, by ..., order ..., AZ|ZA)",
                'variants': ['r = denserank(m, by m[:, "Отдел"])'],
            },
            'WINDOW_REQUIRES_ASSIGNMENT': {
                'message': "denserank() возвращает значение — результат нужно сохранить.",
                'wrong': 'denserank(m)',
                'right': 'r = denserank(m)',
                'explanation': "denserank возвращает новую матрицу.",
                'variants': ['r = denserank(m)', 'm = denserank(m)'],
            },
        },
    },

    # ============================================================
    # PERCENTRANK
    # ============================================================
    'percentrank': {
        'name': 'percentrank',
        'category': 'window',
        'signature': 'percentrank(m [, by ...] [, order ...] [, AZ|ZA])',
        'description': (
            'Процентильный ранг (0.0 .. 1.0).\n'
            '  • Столбец результата: __percentrank.\n'
            '  • Возвращает МАТРИЦУ.'
        ),
        'examples': [
            'r = percentrank(m, by m[:, "Отдел"], order m[:, "Зарплата"], ZA)',
        ],
        'errors': {
            'WINDOW_BAD_SYNTAX': {
                'message': "percentrank: неверный синтаксис.",
                'wrong': 'percentrank()',
                'right': 'percentrank(m, by m[:, "Отдел"], order m[:, "Зарплата"], ZA)',
                'explanation': "Структура: percentrank(m, by ..., order ..., AZ|ZA)",
                'variants': ['r = percentrank(m, order m[:, "Зарплата"], ZA)'],
            },
            'WINDOW_REQUIRES_ASSIGNMENT': {
                'message': "percentrank() возвращает значение — сохраните результат.",
                'wrong': 'percentrank(m)',
                'right': 'r = percentrank(m)',
                'explanation': "Возвращает новую матрицу.",
                'variants': ['r = percentrank(m)'],
            },
        },
    },

    # ============================================================
    # CUMEDIST
    # ============================================================
    'cumedist': {
        'name': 'cumedist',
        'category': 'window',
        'signature': 'cumedist(m [, by ...] [, order ...] [, AZ|ZA])',
        'description': 'Накопленная доля. Столбец __cumedist. Возвращает МАТРИЦУ.',
        'examples': ['r = cumedist(m, order m[:, "X"], AZ)'],
        'errors': {
            'WINDOW_BAD_SYNTAX': {
                'message': "cumedist: неверный синтаксис.",
                'wrong': 'cumedist()',
                'right': 'cumedist(m, by m[:, "Отдел"], order m[:, "Зарплата"], AZ)',
                'explanation': "Структура: cumedist(m, by ..., order ..., AZ|ZA)",
                'variants': ['r = cumedist(m, order m[:, "X"], AZ)'],
            },
            'WINDOW_REQUIRES_ASSIGNMENT': {
                'message': "cumedist() возвращает значение — сохраните результат.",
                'wrong': 'cumedist(m)',
                'right': 'r = cumedist(m)',
                'explanation': "Возвращает новую матрицу.",
                'variants': ['r = cumedist(m)'],
            },
        },
    },

    # ============================================================
    # NTILE
    # ============================================================
    'ntile': {
        'name': 'ntile',
        'category': 'window',
        'signature': 'ntile(m, N [, by ...] [, order ...] [, AZ|ZA])',
        'description': (
            'Разбить на N корзин.\n'
            '  • Каждая строка получает номер корзины 1..N.\n'
            '  • Столбец __ntile.\n'
            '  • Возвращает МАТРИЦУ.'
        ),
        'examples': [
            'r = ntile(m, 4, by m[:, "Отдел"], order m[:, "Зарплата"], ZA)',
        ],
        'errors': {
            'WINDOW_BAD_SYNTAX': {
                'message': "ntile: неверный синтаксис.",
                'wrong': 'ntile(m, by m[:, "Отдел"])',
                'right': 'ntile(m, 4, by m[:, "Отдел"], order m[:, "Зарплата"], ZA)',
                'explanation': (
                    "ntile принимает N (число корзин) ВТОРЫМ аргументом.\n"
                    "\n"
                    "Структура:\n"
                    "  ntile(m, N, by ..., order ..., AZ|ZA)"
                ),
                'variants': [
                    'r = ntile(m, 4, order m[:, "Зарплата"], ZA)',
                    'r = ntile(m, 10, by m[:, "Отдел"])',
                ],
            },
            'WINDOW_BAD_N': {
                'message': "ntile: N должно быть числом >= 1.",
                'wrong': 'ntile(m, 0)',
                'right': 'ntile(m, 4)',
                'explanation': "N — количество корзин. Должно быть >= 1.",
                'variants': ['r = ntile(m, 4)', 'r = ntile(m, 10)'],
            },
            'WINDOW_REQUIRES_ASSIGNMENT': {
                'message': "ntile() возвращает значение — сохраните результат.",
                'wrong': 'ntile(m, 4)',
                'right': 'r = ntile(m, 4)',
                'explanation': "Возвращает новую матрицу.",
                'variants': ['r = ntile(m, 4)'],
            },
        },
    },

    # ============================================================
    # LAG
    # ============================================================
    'lag': {
        'name': 'lag',
        'category': 'window',
        'signature': 'lag(m[:, "X"] [, offset [, default]] [, by ...] [, order ...])',
        'description': (
            'Значение из ПРЕДЫДУЩЕЙ строки группы.\n'
            '  • offset — на сколько назад (по умолчанию 1).\n'
            '  • default — что подставить, если за пределами.\n'
            '  • Столбец __lag.\n'
            '  • Возвращает МАТРИЦУ.'
        ),
        'examples': [
            'r = lag(m[:, "Зарплата"], 1, 0)',
            'r = lag(m[:, "Продажи"], 1, 0, by m[:, "Отдел"], order m[:, "Дата"], AZ)',
        ],
        'errors': {
            'WINDOW_BAD_SYNTAX': {
                'message': (
                    "lag: неверный синтаксис.\n"
                    "  Первый аргумент — срез m[:, \"X\"]."
                ),
                'wrong': 'lag(m)',
                'right': 'lag(m[:, "Продажи"], 1, 0)',
                'explanation': (
                    "lag работает над ОДНИМ СТОЛБЦОМ.\n"
                    "Первый аргумент — срез столбца.\n"
                    "\n"
                    "Структура:\n"
                    "  lag(m[:, \"X\"], offset, default)\n"
                    "  lag(m[:, \"X\"], offset, default, by m[:, \"Y\"], order m[:, \"Z\"], AZ)"
                ),
                'variants': [
                    'r = lag(m[:, "Продажи"], 1, 0)',
                    'r = lag(m[:, "Продажи"], 2, None)',
                ],
            },
            'WINDOW_NEED_SLICE': {
                'message': (
                    "lag: 1-й аргумент должен быть срезом m[:, \"X\"]."
                ),
                'wrong': 'lag("Продажи", 1, 0)',
                'right': 'lag(m[:, "Продажи"], 1, 0)',
                'explanation': (
                    "lag принимает СРЕЗ столбца:\n"
                    "     lag(m[:, \"Продажи\"], 1, 0)"
                ),
                'variants': [
                    'r = lag(m[:, "Продажи"], 1, 0)',
                    'r = lag(m[:, 5], 1, 0)',
                ],
            },
            'WINDOW_REQUIRES_ASSIGNMENT': {
                'message': "lag() возвращает значение — сохраните результат.",
                'wrong': 'lag(m[:, "Продажи"], 1, 0)',
                'right': 'r = lag(m[:, "Продажи"], 1, 0)',
                'explanation': (
                    "lag НЕ изменяет исходную матрицу.\n"
                    "Он ВОЗВРАЩАЕТ НОВУЮ с дополнительным столбцом."
                ),
                'variants': [
                    'r = lag(m[:, "Продажи"], 1, 0)',
                    'm = lag(m[:, "Продажи"], 1, 0)',
                ],
            },
        },
    },

    # ============================================================
    # LEAD
    # ============================================================
    'lead': {
        'name': 'lead',
        'category': 'window',
        'signature': 'lead(m[:, "X"] [, offset [, default]] [, by ...] [, order ...])',
        'description': (
            'Значение из СЛЕДУЮЩЕЙ строки группы.\n'
            '  • Столбец __lead.\n'
            '  • Возвращает МАТРИЦУ.'
        ),
        'examples': [
            'r = lead(m[:, "Продажи"], 1, 0)',
        ],
        'errors': {
            'WINDOW_BAD_SYNTAX': {
                'message': "lead: неверный синтаксис.",
                'wrong': 'lead(m)',
                'right': 'lead(m[:, "Продажи"], 1, 0)',
                'explanation': "Структура: lead(m[:, \"X\"], offset, default)",
                'variants': ['r = lead(m[:, "Продажи"], 1, 0)'],
            },
            'WINDOW_NEED_SLICE': {
                'message': "lead: 1-й аргумент — срез m[:, \"X\"].",
                'wrong': 'lead("Продажи")',
                'right': 'lead(m[:, "Продажи"], 1, 0)',
                'explanation': "Срез столбца.",
                'variants': ['r = lead(m[:, "Продажи"], 1, 0)'],
            },
            'WINDOW_REQUIRES_ASSIGNMENT': {
                'message': "lead() возвращает значение — сохраните результат.",
                'wrong': 'lead(m[:, "Продажи"], 1, 0)',
                'right': 'r = lead(m[:, "Продажи"], 1, 0)',
                'explanation': "Возвращает новую матрицу.",
                'variants': ['r = lead(m[:, "Продажи"], 1, 0)'],
            },
        },
    },

    # ============================================================
    # FIRSTVALUE
    # ============================================================
    'firstvalue': {
        'name': 'firstvalue',
        'category': 'window',
        'signature': 'firstvalue(m[:, "X"] [, by ...] [, order ...] [, AZ|ZA])',
        'description': (
            'ПЕРВОЕ значение группы для каждой строки.\n'
            '  • Все строки группы получают ОДНО И ТО ЖЕ значение.\n'
            '  • Столбец __firstvalue.\n'
            '  • Возвращает МАТРИЦУ.'
        ),
        'examples': [
            'r = firstvalue(m[:, "Зарплата"], by m[:, "Отдел"], order m[:, "Зарплата"], ZA)',
        ],
        'errors': {
            'WINDOW_BAD_SYNTAX': {
                'message': "firstvalue: неверный синтаксис.",
                'wrong': 'firstvalue(m)',
                'right': 'firstvalue(m[:, "Зарплата"], by m[:, "Отдел"], order m[:, "Зарплата"], ZA)',
                'explanation': (
                    "Структура:\n"
                    "  firstvalue(m[:, \"X\"], by m[:, \"Y\"], order m[:, \"Z\"], AZ|ZA)"
                ),
                'variants': [
                    'r = firstvalue(m[:, "Зарплата"], by m[:, "Отдел"], order m[:, "Зарплата"], ZA)',
                ],
            },
            'WINDOW_NEED_SLICE': {
                'message': "firstvalue: 1-й аргумент — срез m[:, \"X\"].",
                'wrong': 'firstvalue("Зарплата")',
                'right': 'firstvalue(m[:, "Зарплата"], by m[:, "Отдел"], order m[:, "Зарплата"], ZA)',
                'explanation': "Срез столбца.",
                'variants': [
                    'r = firstvalue(m[:, "Зарплата"], by m[:, "Отдел"], order m[:, "Зарплата"], ZA)',
                ],
            },
            'WINDOW_REQUIRES_ASSIGNMENT': {
                'message': "firstvalue() возвращает значение — сохраните результат.",
                'wrong': 'firstvalue(m[:, "Зарплата"])',
                'right': 'r = firstvalue(m[:, "Зарплата"])',
                'explanation': "Возвращает новую матрицу.",
                'variants': ['r = firstvalue(m[:, "Зарплата"])'],
            },
        },
    },

    # ============================================================
    # LASTVALUE
    # ============================================================
    'lastvalue': {
        'name': 'lastvalue',
        'category': 'window',
        'signature': 'lastvalue(m[:, "X"] [, by ...] [, order ...] [, AZ|ZA])',
        'description': 'ПОСЛЕДНЕЕ значение группы. Столбец __lastvalue. Возвращает МАТРИЦУ.',
        'examples': ['r = lastvalue(m[:, "Зарплата"], by m[:, "Отдел"], order m[:, "Зарплата"], ZA)'],
        'errors': {
            'WINDOW_BAD_SYNTAX': {
                'message': "lastvalue: неверный синтаксис.",
                'wrong': 'lastvalue(m)',
                'right': 'lastvalue(m[:, "Зарплата"], by m[:, "Отдел"])',
                'explanation': "Структура: lastvalue(m[:, \"X\"], by ..., order ..., AZ|ZA)",
                'variants': ['r = lastvalue(m[:, "Зарплата"], by m[:, "Отдел"])'],
            },
            'WINDOW_REQUIRES_ASSIGNMENT': {
                'message': "lastvalue() возвращает значение — сохраните результат.",
                'wrong': 'lastvalue(m[:, "Зарплата"])',
                'right': 'r = lastvalue(m[:, "Зарплата"])',
                'explanation': "Возвращает новую матрицу.",
                'variants': ['r = lastvalue(m[:, "Зарплата"])'],
            },
        },
    },

    # ============================================================
    # NTHVALUE
    # ============================================================
    'nthvalue': {
        'name': 'nthvalue',
        'category': 'window',
        'signature': 'nthvalue(m[:, "X"], N [, by ...] [, order ...] [, AZ|ZA])',
        'description': 'N-е значение группы. Столбец __nthvalue. Возвращает МАТРИЦУ.',
        'examples': ['r = nthvalue(m[:, "Зарплата"], 2, by m[:, "Отдел"], order m[:, "Зарплата"], ZA)'],
        'errors': {
            'WINDOW_BAD_SYNTAX': {
                'message': "nthvalue: неверный синтаксис.",
                'wrong': 'nthvalue(m[:, "Зарплата"], by m[:, "Отдел"])',
                'right': 'nthvalue(m[:, "Зарплата"], 2, by m[:, "Отдел"])',
                'explanation': (
                    "nthvalue принимает N (номер значения) ВТОРЫМ аргументом.\n"
                    "\n"
                    "Структура:\n"
                    "  nthvalue(m[:, \"X\"], N, by ..., order ..., AZ|ZA)"
                ),
                'variants': [
                    'r = nthvalue(m[:, "Зарплата"], 2, by m[:, "Отдел"])',
                    'r = nthvalue(m[:, "Зарплата"], 3, order m[:, "Зарплата"], ZA)',
                ],
            },
            'WINDOW_BAD_N': {
                'message': "nthvalue: N должно быть числом >= 1.",
                'wrong': 'nthvalue(m[:, "X"], 0)',
                'right': 'nthvalue(m[:, "X"], 2)',
                'explanation': "N — номер значения в группе.",
                'variants': ['r = nthvalue(m[:, "X"], 2)'],
            },
            'WINDOW_REQUIRES_ASSIGNMENT': {
                'message': "nthvalue() возвращает значение — сохраните результат.",
                'wrong': 'nthvalue(m[:, "X"], 2)',
                'right': 'r = nthvalue(m[:, "X"], 2)',
                'explanation': "Возвращает новую матрицу.",
                'variants': ['r = nthvalue(m[:, "X"], 2)'],
            },
        },
    },

    # ============================================================
    # WINSUM
    # ============================================================
    'winsum': {
        'name': 'winsum',
        'category': 'window',
        'signature': 'winsum(m[:, "X"] [, by ...] [, order ...] [, AZ|ZA])',
        'description': (
            'Накопительная сумма.\n'
            '  • Каждая строка: сумма ВСЕХ предыдущих + текущей.\n'
            '  • Столбец __winsum.\n'
            '  • Возвращает МАТРИЦУ.'
        ),
        'examples': [
            'r = winsum(m[:, "Продажи"], by m[:, "Отдел"], order m[:, "Дата"], AZ)',
        ],
        'errors': {
            'WINDOW_BAD_SYNTAX': {
                'message': "winsum: неверный синтаксис.",
                'wrong': 'winsum(m)',
                'right': 'winsum(m[:, "Продажи"], by m[:, "Отдел"], order m[:, "Дата"], AZ)',
                'explanation': (
                    "winsum работает над ОДНИМ СТОЛБЦОМ.\n"
                    "\n"
                    "Структура:\n"
                    "  winsum(m[:, \"X\"], by ..., order ..., AZ|ZA)"
                ),
                'variants': [
                    'r = winsum(m[:, "Продажи"], order m[:, "Дата"], AZ)',
                    'r = winsum(m[:, "Продажи"], by m[:, "Отдел"])',
                ],
            },
            'WINDOW_NEED_SLICE': {
                'message': "winsum: 1-й аргумент — срез m[:, \"X\"].",
                'wrong': 'winsum("Продажи")',
                'right': 'winsum(m[:, "Продажи"])',
                'explanation': "Срез столбца.",
                'variants': ['r = winsum(m[:, "Продажи"])'],
            },
            'WINDOW_REQUIRES_ASSIGNMENT': {
                'message': "winsum() возвращает значение — сохраните результат.",
                'wrong': 'winsum(m[:, "Продажи"])',
                'right': 'r = winsum(m[:, "Продажи"])',
                'explanation': (
                    "winsum НЕ изменяет исходную матрицу.\n"
                    "Он ВОЗВРАЩАЕТ НОВУЮ."
                ),
                'variants': [
                    'r = winsum(m[:, "Продажи"])',
                    'm = winsum(m[:, "Продажи"])',
                ],
            },
        },
    },

    # ============================================================
    # WINAVG
    # ============================================================
    'winavg': {
        'name': 'winavg',
        'category': 'window',
        'signature': 'winavg(m[:, "X"] [, by ...] [, order ...] [, AZ|ZA])',
        'description': 'Накопительное среднее. Столбец __winavg. Возвращает МАТРИЦУ.',
        'examples': ['r = winavg(m[:, "Продажи"], by m[:, "Отдел"])'],
        'errors': {
            'WINDOW_BAD_SYNTAX': {
                'message': "winavg: неверный синтаксис.",
                'wrong': 'winavg(m)',
                'right': 'winavg(m[:, "Продажи"], by m[:, "Отдел"])',
                'explanation': "Структура: winavg(m[:, \"X\"], by ..., order ..., AZ|ZA)",
                'variants': ['r = winavg(m[:, "Продажи"])'],
            },
            'WINDOW_REQUIRES_ASSIGNMENT': {
                'message': "winavg() возвращает значение — сохраните результат.",
                'wrong': 'winavg(m[:, "Продажи"])',
                'right': 'r = winavg(m[:, "Продажи"])',
                'explanation': "Возвращает новую матрицу.",
                'variants': ['r = winavg(m[:, "Продажи"])'],
            },
        },
    },

    # ============================================================
    # WINCOUNT
    # ============================================================
    'wincount': {
        'name': 'wincount',
        'category': 'window',
        'signature': 'wincount(m[:, "X"] [, by ...] [, order ...])',
        'description': 'Накопительное количество. Столбец __wincount. Возвращает МАТРИЦУ.',
        'examples': ['r = wincount(m[:, "Продажи"])'],
        'errors': {
            'WINDOW_BAD_SYNTAX': {
                'message': "wincount: неверный синтаксис.",
                'wrong': 'wincount(m)',
                'right': 'wincount(m[:, "Продажи"])',
                'explanation': "Структура: wincount(m[:, \"X\"])",
                'variants': ['r = wincount(m[:, "Продажи"])'],
            },
            'WINDOW_REQUIRES_ASSIGNMENT': {
                'message': "wincount() возвращает значение — сохраните результат.",
                'wrong': 'wincount(m[:, "Продажи"])',
                'right': 'r = wincount(m[:, "Продажи"])',
                'explanation': "Возвращает новую матрицу.",
                'variants': ['r = wincount(m[:, "Продажи"])'],
            },
        },
    },

    # ============================================================
    # WINMIN
    # ============================================================
    'winmin': {
        'name': 'winmin',
        'category': 'window',
        'signature': 'winmin(m[:, "X"] [, by ...] [, order ...])',
        'description': 'Накопительный минимум. Столбец __winmin. Возвращает МАТРИЦУ.',
        'examples': ['r = winmin(m[:, "Продажи"], by m[:, "Отдел"])'],
        'errors': {
            'WINDOW_BAD_SYNTAX': {
                'message': "winmin: неверный синтаксис.",
                'wrong': 'winmin(m)',
                'right': 'winmin(m[:, "Продажи"], by m[:, "Отдел"])',
                'explanation': "Структура: winmin(m[:, \"X\"], by ...)",
                'variants': ['r = winmin(m[:, "Продажи"])'],
            },
            'WINDOW_REQUIRES_ASSIGNMENT': {
                'message': "winmin() возвращает значение — сохраните результат.",
                'wrong': 'winmin(m[:, "Продажи"])',
                'right': 'r = winmin(m[:, "Продажи"])',
                'explanation': "Возвращает новую матрицу.",
                'variants': ['r = winmin(m[:, "Продажи"])'],
            },
        },
    },

    # ============================================================
    # WINMAX
    # ============================================================
    'winmax': {
        'name': 'winmax',
        'category': 'window',
        'signature': 'winmax(m[:, "X"] [, by ...] [, order ...])',
        'description': 'Накопительный максимум. Столбец __winmax. Возвращает МАТРИЦУ.',
        'examples': ['r = winmax(m[:, "Продажи"], by m[:, "Отдел"])'],
        'errors': {
            'WINDOW_BAD_SYNTAX': {
                'message': "winmax: неверный синтаксис.",
                'wrong': 'winmax(m)',
                'right': 'winmax(m[:, "Продажи"], by m[:, "Отдел"])',
                'explanation': "Структура: winmax(m[:, \"X\"], by ...)",
                'variants': ['r = winmax(m[:, "Продажи"])'],
            },
            'WINDOW_REQUIRES_ASSIGNMENT': {
                'message': "winmax() возвращает значение — сохраните результат.",
                'wrong': 'winmax(m[:, "Продажи"])',
                'right': 'r = winmax(m[:, "Продажи"])',
                'explanation': "Возвращает новую матрицу.",
                'variants': ['r = winmax(m[:, "Продажи"])'],
            },
        },
    },

    # ============================================================
    # WINMEDIAN
    # ============================================================
    'winmedian': {
        'name': 'winmedian',
        'category': 'window',
        'signature': 'winmedian(m[:, "X"] [, by ...] [, order ...])',
        'description': 'Накопительная медиана. Столбец __winmedian. Возвращает МАТРИЦУ.',
        'examples': ['r = winmedian(m[:, "Продажи"])'],
        'errors': {
            'WINDOW_BAD_SYNTAX': {
                'message': "winmedian: неверный синтаксис.",
                'wrong': 'winmedian(m)',
                'right': 'winmedian(m[:, "Продажи"])',
                'explanation': "Структура: winmedian(m[:, \"X\"])",
                'variants': ['r = winmedian(m[:, "Продажи"])'],
            },
            'WINDOW_REQUIRES_ASSIGNMENT': {
                'message': "winmedian() возвращает значение — сохраните результат.",
                'wrong': 'winmedian(m[:, "Продажи"])',
                'right': 'r = winmedian(m[:, "Продажи"])',
                'explanation': "Возвращает новую матрицу.",
                'variants': ['r = winmedian(m[:, "Продажи"])'],
            },
        },
    },

    # ============================================================
    # WINSTDEV
    # ============================================================
    'winstdev': {
        'name': 'winstdev',
        'category': 'window',
        'signature': 'winstdev(m[:, "X"] [, by ...] [, order ...])',
        'description': 'Накопительное стандартное отклонение. Столбец __winstdev. Возвращает МАТРИЦУ.',
        'examples': ['r = winstdev(m[:, "Продажи"])'],
        'errors': {
            'WINDOW_BAD_SYNTAX': {
                'message': "winstdev: неверный синтаксис.",
                'wrong': 'winstdev(m)',
                'right': 'winstdev(m[:, "Продажи"])',
                'explanation': "Структура: winstdev(m[:, \"X\"])",
                'variants': ['r = winstdev(m[:, "Продажи"])'],
            },
            'WINDOW_REQUIRES_ASSIGNMENT': {
                'message': "winstdev() возвращает значение — сохраните результат.",
                'wrong': 'winstdev(m[:, "Продажи"])',
                'right': 'r = winstdev(m[:, "Продажи"])',
                'explanation': "Возвращает новую матрицу.",
                'variants': ['r = winstdev(m[:, "Продажи"])'],
            },
        },
    },

    # ============================================================
    # QUALIFY
    # ============================================================
    'qualify': {
        'name': 'qualify',
        'category': 'window',
        'signature': 'qualify(m, <оконная_функция> <ОП> <значение>)',
        'description': (
            'Фильтр строк по оконной функции.\n'
            '  • Аналог WHERE, но для окон.\n'
            '  • Пример: qualify(m, rownumber(...) <= 3).\n'
            '  • Работает с Matrix и DuckDB.\n'
            '  • Возвращает НОВУЮ МАТРИЦУ.'
        ),
        'examples': [
            'r = qualify(m, rownumber(m, by m[:, "Отдел"], order m[:, "Зарплата"], ZA) <= 2)',
            'r = qualify(m, rank(m, by m[:, "Отдел"], order m[:, "Зарплата"], ZA) == 1)',
        ],
        'errors': {
            'QUALIFY_BAD_SYNTAX': {
                'message': (
                    "qualify: неверный синтаксис.\n"
                    "  Нужна таблица и условие с оконной функцией."
                ),
                'wrong': 'qualify(m)',
                'right': 'qualify(m, rownumber(m, by m[:, "Отдел"], order m[:, "Зарплата"], ZA) <= 2)',
                'explanation': (
                    "qualify принимает ДВА аргумента:\n"
                    "  1. таблица\n"
                    "  2. условие с оконной функцией\n"
                    "\n"
                    "Структура:\n"
                    "  qualify(m, <оконная_функция> <ОП> <значение>)\n"
                    "\n"
                    "ОП: <, >, <=, >=, ==, !="
                ),
                'variants': [
                    'r = qualify(m, rownumber(m, by m[:, "Отдел"]) <= 3)',
                    'r = qualify(m, rank(m, by m[:, "Отдел"]) == 1)',
                ],
            },
            'QUALIFY_NO_WINDOW': {
                'message': (
                    "qualify: в условии должна быть ОКОННАЯ функция.\n"
                    "  Пример: rownumber, rank, lag, winsum."
                ),
                'wrong': 'qualify(m, m[:, "Отдел"] == "IT")',
                'right': 'qualify(m, rownumber(m, by m[:, "Отдел"]) == 1)',
                'explanation': (
                    "qualify фильтрует по результату оконной функции,\n"
                    "а не по обычному условию (для этого есть filterif).\n"
                    "\n"
                    "Допустимые оконные функции:\n"
                    "  rownumber, rank, denserank, percentrank,\n"
                    "  cumedist, ntile, lag, lead,\n"
                    "  firstvalue, lastvalue, nthvalue,\n"
                    "  winsum, winavg, wincount, winmin, winmax,\n"
                    "  winmedian, winstdev"
                ),
                'variants': [
                    'r = qualify(m, rownumber(m, by m[:, "Отдел"]) <= 3)',
                    'r = qualify(m, rank(m, order m[:, "Зарплата"], ZA) == 1)',
                ],
            },
            'QUALIFY_REQUIRES_ASSIGNMENT': {
                'message': (
                    "qualify() возвращает значение — сохраните результат."
                ),
                'wrong': 'qualify(m, rownumber(m, by m[:, "Отдел"]) <= 3)',
                'right': 'r = qualify(m, rownumber(m, by m[:, "Отдел"]) <= 3)',
                'explanation': (
                    "qualify возвращает НОВУЮ матрицу.\n"
                    "\n"
                    "Правильно:\n"
                    "  r = qualify(...)\n"
                    "  m = qualify(...)"
                ),
                'variants': [
                    'r = qualify(m, rownumber(m, by m[:, "Отдел"]) <= 3)',
                    'm = qualify(m, rownumber(m, by m[:, "Отдел"]) <= 3)',
                ],
            },
        },
    },
}


EN = {
    # ============================================================
    # ROWNUMBER
    # ============================================================
    'rownumber': {
        'name': 'rownumber',
        'category': 'window',
        'signature': 'rownumber(m [, by m[:, "X"]] [, order m[:, "Y"]] [, AZ|ZA])',
        'description': (
            'Row number within a group.\n'
            '  • 1, 2, 3, 4, ...\n'
            '  • Without by — the whole table is one group.\n'
            '  • Without order — rows as is.\n'
            '  • Returns a MATRIX with an added column __rownumber.'
        ),
        'examples': [
            'r = rownumber(m)',
            'r = rownumber(m, by m[:, "Department"])',
            'r = rownumber(m, order m[:, "Salary"], ZA)',
            'r = rownumber(m, by m[:, "Department"], order m[:, "Salary"], ZA)',
        ],
        'errors': {
            'WINDOW_BAD_SYNTAX': {
                'message': (
                    "rownumber: invalid syntax.\n"
                    "  Need a matrix and optional by/order."
                ),
                'wrong': 'rownumber()',
                'right': 'rownumber(m, by m[:, "Department"], order m[:, "Salary"], ZA)',
                'explanation': (
                    "Structure:\n"
                    "  rownumber(m)\n"
                    "  rownumber(m, by m[:, \"X\"])\n"
                    "  rownumber(m, order m[:, \"Y\"], ZA)\n"
                    "  rownumber(m, by m[:, \"X\"], order m[:, \"Y\"], ZA)"
                ),
                'variants': [
                    'r = rownumber(m)',
                    'r = rownumber(m, by m[:, "Department"], order m[:, "Salary"], ZA)',
                ],
            },
            'WINDOW_NEED_TABLE': {
                'message': (
                    "rownumber: 1st argument must be a table (variable).\n"
                    "  Not a slice, not a scalar."
                ),
                'wrong': 'rownumber(m[:, "Department"])',
                'right': 'rownumber(m, by m[:, "Department"])',
                'explanation': (
                    "rownumber works over the WHOLE table.\n"
                    "The first argument is a table variable.\n"
                    "Columns for partition and sort go inside by/order.\n"
                    "\n"
                    "Incorrect:\n"
                    "     rownumber(m[:, \"Department\"])\n"
                    "\n"
                    "Correct:\n"
                    "     rownumber(m, by m[:, \"Department\"])"
                ),
                'variants': [
                    'r = rownumber(m, by m[:, "Department"])',
                    'r = rownumber(m)',
                ],
            },
            'WINDOW_BAD_BY': {
                'message': "rownumber: by must be a slice m[:, \"X\"].",
                'wrong': 'rownumber(m, by "Department")',
                'right': 'rownumber(m, by m[:, "Department"])',
                'explanation': (
                    "by takes a column SLICE:\n"
                    "     by m[:, \"Department\"]\n"
                    "     by m[:, 3]"
                ),
                'variants': [
                    'r = rownumber(m, by m[:, "Department"])',
                    'r = rownumber(m, by m[:, 3])',
                ],
            },
            'WINDOW_BAD_ORDER': {
                'message': "rownumber: order must be a slice m[:, \"X\"].",
                'wrong': 'rownumber(m, order "Salary", ZA)',
                'right': 'rownumber(m, order m[:, "Salary"], ZA)',
                'explanation': "order takes a column SLICE.",
                'variants': [
                    'r = rownumber(m, order m[:, "Salary"], ZA)',
                    'r = rownumber(m, order m[:, 5], AZ)',
                ],
            },
            'WINDOW_BAD_DIRECTION': {
                'message': "rownumber: sort direction must be AZ or ZA.",
                'wrong': 'rownumber(m, order m[:, "Salary"], UP)',
                'right': 'rownumber(m, order m[:, "Salary"], ZA)',
                'explanation': (
                    "AZ — ascending.\n"
                    "ZA — descending.\n"
                    "\n"
                    "NOT:\n"
                    "     UP, DOWN, ASC, DESC"
                ),
                'variants': [
                    'r = rownumber(m, order m[:, "Salary"], AZ)',
                    'r = rownumber(m, order m[:, "Salary"], ZA)',
                ],
            },
            'WINDOW_REQUIRES_ASSIGNMENT': {
                'message': (
                    "rownumber() returns a value — "
                    "the result must be saved."
                ),
                'wrong': 'rownumber(m, by m[:, "Department"])',
                'right': 'r = rownumber(m, by m[:, "Department"])',
                'explanation': (
                    "Window functions do NOT modify the source matrix.\n"
                    "They RETURN a NEW one (with an added column).\n"
                    "\n"
                    "Correct:\n"
                    "  r = rownumber(...)     — to a new variable\n"
                    "  m = rownumber(...)     — mutation"
                ),
                'variants': [
                    'r = rownumber(m, by m[:, "Department"])',
                    'm = rownumber(m, by m[:, "Department"])',
                ],
            },
        },
    },

    # ============================================================
    # RANK
    # ============================================================
    'rank': {
        'name': 'rank',
        'category': 'window',
        'signature': 'rank(m [, by m[:, "X"]] [, order m[:, "Y"]] [, AZ|ZA])',
        'description': (
            'Rank within a group.\n'
            '  • 1, 2, 2, 4 — skips after duplicates.\n'
            '  • Result column: __rank.\n'
            '  • Returns a MATRIX.'
        ),
        'examples': [
            'r = rank(m, by m[:, "Department"], order m[:, "Salary"], ZA)',
        ],
        'errors': {
            'WINDOW_BAD_SYNTAX': {
                'message': "rank: invalid syntax.",
                'wrong': 'rank()',
                'right': 'rank(m, by m[:, "Department"], order m[:, "Salary"], ZA)',
                'explanation': "Structure: rank(m, by ..., order ..., AZ|ZA)",
                'variants': [
                    'r = rank(m, by m[:, "Department"], order m[:, "Salary"], ZA)',
                ],
            },
            'WINDOW_NEED_TABLE': {
                'message': "rank: 1st argument must be a table.",
                'wrong': 'rank(m[:, "Department"])',
                'right': 'rank(m, by m[:, "Department"])',
                'explanation': "First argument is a table variable.",
                'variants': [
                    'r = rank(m, by m[:, "Department"])',
                ],
            },
            'WINDOW_REQUIRES_ASSIGNMENT': {
                'message': "rank() returns a value — save the result.",
                'wrong': 'rank(m, by m[:, "Department"])',
                'right': 'r = rank(m, by m[:, "Department"])',
                'explanation': "rank does NOT mutate, returns a new matrix.",
                'variants': [
                    'r = rank(m, by m[:, "Department"])',
                    'm = rank(m, by m[:, "Department"])',
                ],
            },
        },
    },

    # ============================================================
    # DENSERANK
    # ============================================================
    'denserank': {
        'name': 'denserank',
        'category': 'window',
        'signature': 'denserank(m [, by ...] [, order ...] [, AZ|ZA])',
        'description': (
            'Dense rank (no skips).\n'
            '  • 1, 2, 2, 3.\n'
            '  • Column __denserank.\n'
            '  • Returns a MATRIX.'
        ),
        'examples': [
            'r = denserank(m, by m[:, "Department"], order m[:, "Salary"], ZA)',
        ],
        'errors': {
            'WINDOW_BAD_SYNTAX': {
                'message': "denserank: invalid syntax.",
                'wrong': 'denserank()',
                'right': 'denserank(m, by m[:, "Department"], order m[:, "Salary"], ZA)',
                'explanation': "Structure: denserank(m, by ..., order ..., AZ|ZA)",
                'variants': ['r = denserank(m, by m[:, "Department"])'],
            },
            'WINDOW_REQUIRES_ASSIGNMENT': {
                'message': "denserank() returns a value — save the result.",
                'wrong': 'denserank(m)',
                'right': 'r = denserank(m)',
                'explanation': "Returns a new matrix.",
                'variants': ['r = denserank(m)', 'm = denserank(m)'],
            },
        },
    },

    # ============================================================
    # PERCENTRANK
    # ============================================================
    'percentrank': {
        'name': 'percentrank',
        'category': 'window',
        'signature': 'percentrank(m [, by ...] [, order ...] [, AZ|ZA])',
        'description': 'Percentile rank (0.0 .. 1.0). Column __percentrank. Returns a MATRIX.',
        'examples': [
            'r = percentrank(m, by m[:, "Department"], order m[:, "Salary"], ZA)',
        ],
        'errors': {
            'WINDOW_BAD_SYNTAX': {
                'message': "percentrank: invalid syntax.",
                'wrong': 'percentrank()',
                'right': 'percentrank(m, by m[:, "Department"], order m[:, "Salary"], ZA)',
                'explanation': "Structure: percentrank(m, by ..., order ..., AZ|ZA)",
                'variants': ['r = percentrank(m, order m[:, "Salary"], ZA)'],
            },
            'WINDOW_REQUIRES_ASSIGNMENT': {
                'message': "percentrank() returns a value — save the result.",
                'wrong': 'percentrank(m)',
                'right': 'r = percentrank(m)',
                'explanation': "Returns a new matrix.",
                'variants': ['r = percentrank(m)'],
            },
        },
    },

    # ============================================================
    # CUMEDIST
    # ============================================================
    'cumedist': {
        'name': 'cumedist',
        'category': 'window',
        'signature': 'cumedist(m [, by ...] [, order ...] [, AZ|ZA])',
        'description': 'Cumulative distribution. Column __cumedist. Returns a MATRIX.',
        'examples': ['r = cumedist(m, order m[:, "X"], AZ)'],
        'errors': {
            'WINDOW_BAD_SYNTAX': {
                'message': "cumedist: invalid syntax.",
                'wrong': 'cumedist()',
                'right': 'cumedist(m, by m[:, "Department"], order m[:, "Salary"], AZ)',
                'explanation': "Structure: cumedist(m, by ..., order ..., AZ|ZA)",
                'variants': ['r = cumedist(m, order m[:, "X"], AZ)'],
            },
            'WINDOW_REQUIRES_ASSIGNMENT': {
                'message': "cumedist() returns a value — save the result.",
                'wrong': 'cumedist(m)',
                'right': 'r = cumedist(m)',
                'explanation': "Returns a new matrix.",
                'variants': ['r = cumedist(m)'],
            },
        },
    },

    # ============================================================
    # NTILE
    # ============================================================
    'ntile': {
        'name': 'ntile',
        'category': 'window',
        'signature': 'ntile(m, N [, by ...] [, order ...] [, AZ|ZA])',
        'description': 'Split into N buckets. Column __ntile. Returns a MATRIX.',
        'examples': ['r = ntile(m, 4, order m[:, "Salary"], ZA)'],
        'errors': {
            'WINDOW_BAD_SYNTAX': {
                'message': "ntile: invalid syntax.",
                'wrong': 'ntile(m, by m[:, "Department"])',
                'right': 'ntile(m, 4, by m[:, "Department"], order m[:, "Salary"], ZA)',
                'explanation': (
                    "ntile takes N (number of buckets) as 2nd argument.\n"
                    "\n"
                    "Structure:\n"
                    "  ntile(m, N, by ..., order ..., AZ|ZA)"
                ),
                'variants': [
                    'r = ntile(m, 4, order m[:, "Salary"], ZA)',
                    'r = ntile(m, 10, by m[:, "Department"])',
                ],
            },
            'WINDOW_BAD_N': {
                'message': "ntile: N must be a number >= 1.",
                'wrong': 'ntile(m, 0)',
                'right': 'ntile(m, 4)',
                'explanation': "N — number of buckets. Must be >= 1.",
                'variants': ['r = ntile(m, 4)', 'r = ntile(m, 10)'],
            },
            'WINDOW_REQUIRES_ASSIGNMENT': {
                'message': "ntile() returns a value — save the result.",
                'wrong': 'ntile(m, 4)',
                'right': 'r = ntile(m, 4)',
                'explanation': "Returns a new matrix.",
                'variants': ['r = ntile(m, 4)'],
            },
        },
    },

    # ============================================================
    # LAG
    # ============================================================
    'lag': {
        'name': 'lag',
        'category': 'window',
        'signature': 'lag(m[:, "X"] [, offset [, default]] [, by ...] [, order ...])',
        'description': (
            'Value from the PREVIOUS row of the group.\n'
            '  • offset — how many rows back (default 1).\n'
            '  • default — what to substitute if out of bounds.\n'
            '  • Column __lag.\n'
            '  • Returns a MATRIX.'
        ),
        'examples': [
            'r = lag(m[:, "Salary"], 1, 0)',
            'r = lag(m[:, "Sales"], 1, 0, by m[:, "Department"], order m[:, "Date"], AZ)',
        ],
        'errors': {
            'WINDOW_BAD_SYNTAX': {
                'message': (
                    "lag: invalid syntax.\n"
                    "  First argument must be a slice m[:, \"X\"]."
                ),
                'wrong': 'lag(m)',
                'right': 'lag(m[:, "Sales"], 1, 0)',
                'explanation': (
                    "lag works over a SINGLE COLUMN.\n"
                    "First argument is a column slice.\n"
                    "\n"
                    "Structure:\n"
                    "  lag(m[:, \"X\"], offset, default)"
                ),
                'variants': [
                    'r = lag(m[:, "Sales"], 1, 0)',
                    'r = lag(m[:, "Sales"], 2, None)',
                ],
            },
            'WINDOW_NEED_SLICE': {
                'message': "lag: 1st argument must be a slice m[:, \"X\"].",
                'wrong': 'lag("Sales", 1, 0)',
                'right': 'lag(m[:, "Sales"], 1, 0)',
                'explanation': "lag takes a column SLICE.",
                'variants': [
                    'r = lag(m[:, "Sales"], 1, 0)',
                    'r = lag(m[:, 5], 1, 0)',
                ],
            },
            'WINDOW_REQUIRES_ASSIGNMENT': {
                'message': "lag() returns a value — save the result.",
                'wrong': 'lag(m[:, "Sales"], 1, 0)',
                'right': 'r = lag(m[:, "Sales"], 1, 0)',
                'explanation': (
                    "lag does NOT modify the source matrix.\n"
                    "It RETURNS a NEW one with an added column."
                ),
                'variants': [
                    'r = lag(m[:, "Sales"], 1, 0)',
                    'm = lag(m[:, "Sales"], 1, 0)',
                ],
            },
        },
    },

    # ============================================================
    # LEAD
    # ============================================================
    'lead': {
        'name': 'lead',
        'category': 'window',
        'signature': 'lead(m[:, "X"] [, offset [, default]] [, by ...] [, order ...])',
        'description': 'Value from the NEXT row of the group. Column __lead. Returns a MATRIX.',
        'examples': ['r = lead(m[:, "Sales"], 1, 0)'],
        'errors': {
            'WINDOW_BAD_SYNTAX': {
                'message': "lead: invalid syntax.",
                'wrong': 'lead(m)',
                'right': 'lead(m[:, "Sales"], 1, 0)',
                'explanation': "Structure: lead(m[:, \"X\"], offset, default)",
                'variants': ['r = lead(m[:, "Sales"], 1, 0)'],
            },
            'WINDOW_NEED_SLICE': {
                'message': "lead: 1st argument must be a slice m[:, \"X\"].",
                'wrong': 'lead("Sales")',
                'right': 'lead(m[:, "Sales"], 1, 0)',
                'explanation': "Column slice.",
                'variants': ['r = lead(m[:, "Sales"], 1, 0)'],
            },
            'WINDOW_REQUIRES_ASSIGNMENT': {
                'message': "lead() returns a value — save the result.",
                'wrong': 'lead(m[:, "Sales"], 1, 0)',
                'right': 'r = lead(m[:, "Sales"], 1, 0)',
                'explanation': "Returns a new matrix.",
                'variants': ['r = lead(m[:, "Sales"], 1, 0)'],
            },
        },
    },

    # ============================================================
    # FIRSTVALUE
    # ============================================================
    'firstvalue': {
        'name': 'firstvalue',
        'category': 'window',
        'signature': 'firstvalue(m[:, "X"] [, by ...] [, order ...] [, AZ|ZA])',
        'description': (
            'FIRST value of the group for each row.\n'
            '  • All rows of the group get the SAME value.\n'
            '  • Column __firstvalue.\n'
            '  • Returns a MATRIX.'
        ),
        'examples': [
            'r = firstvalue(m[:, "Salary"], by m[:, "Department"], order m[:, "Salary"], ZA)',
        ],
        'errors': {
            'WINDOW_BAD_SYNTAX': {
                'message': "firstvalue: invalid syntax.",
                'wrong': 'firstvalue(m)',
                'right': 'firstvalue(m[:, "Salary"], by m[:, "Department"], order m[:, "Salary"], ZA)',
                'explanation': (
                    "Structure:\n"
                    "  firstvalue(m[:, \"X\"], by m[:, \"Y\"], order m[:, \"Z\"], AZ|ZA)"
                ),
                'variants': [
                    'r = firstvalue(m[:, "Salary"], by m[:, "Department"], order m[:, "Salary"], ZA)',
                ],
            },
            'WINDOW_NEED_SLICE': {
                'message': "firstvalue: 1st argument must be a slice m[:, \"X\"].",
                'wrong': 'firstvalue("Salary")',
                'right': 'firstvalue(m[:, "Salary"], by m[:, "Department"])',
                'explanation': "Column slice.",
                'variants': [
                    'r = firstvalue(m[:, "Salary"], by m[:, "Department"])',
                ],
            },
            'WINDOW_REQUIRES_ASSIGNMENT': {
                'message': "firstvalue() returns a value — save the result.",
                'wrong': 'firstvalue(m[:, "Salary"])',
                'right': 'r = firstvalue(m[:, "Salary"])',
                'explanation': "Returns a new matrix.",
                'variants': ['r = firstvalue(m[:, "Salary"])'],
            },
        },
    },

    # ============================================================
    # LASTVALUE
    # ============================================================
    'lastvalue': {
        'name': 'lastvalue',
        'category': 'window',
        'signature': 'lastvalue(m[:, "X"] [, by ...] [, order ...] [, AZ|ZA])',
        'description': 'LAST value of the group. Column __lastvalue. Returns a MATRIX.',
        'examples': ['r = lastvalue(m[:, "Salary"], by m[:, "Department"])'],
        'errors': {
            'WINDOW_BAD_SYNTAX': {
                'message': "lastvalue: invalid syntax.",
                'wrong': 'lastvalue(m)',
                'right': 'lastvalue(m[:, "Salary"], by m[:, "Department"])',
                'explanation': "Structure: lastvalue(m[:, \"X\"], by ..., order ..., AZ|ZA)",
                'variants': ['r = lastvalue(m[:, "Salary"], by m[:, "Department"])'],
            },
            'WINDOW_REQUIRES_ASSIGNMENT': {
                'message': "lastvalue() returns a value — save the result.",
                'wrong': 'lastvalue(m[:, "Salary"])',
                'right': 'r = lastvalue(m[:, "Salary"])',
                'explanation': "Returns a new matrix.",
                'variants': ['r = lastvalue(m[:, "Salary"])'],
            },
        },
    },

    # ============================================================
    # NTHVALUE
    # ============================================================
    'nthvalue': {
        'name': 'nthvalue',
        'category': 'window',
        'signature': 'nthvalue(m[:, "X"], N [, by ...] [, order ...] [, AZ|ZA])',
        'description': 'N-th value of the group. Column __nthvalue. Returns a MATRIX.',
        'examples': ['r = nthvalue(m[:, "Salary"], 2, by m[:, "Department"])'],
        'errors': {
            'WINDOW_BAD_SYNTAX': {
                'message': "nthvalue: invalid syntax.",
                'wrong': 'nthvalue(m[:, "Salary"], by m[:, "Department"])',
                'right': 'nthvalue(m[:, "Salary"], 2, by m[:, "Department"])',
                'explanation': (
                    "nthvalue takes N (value number) as 2nd argument.\n"
                    "\n"
                    "Structure:\n"
                    "  nthvalue(m[:, \"X\"], N, by ..., order ..., AZ|ZA)"
                ),
                'variants': [
                    'r = nthvalue(m[:, "Salary"], 2, by m[:, "Department"])',
                    'r = nthvalue(m[:, "Salary"], 3, order m[:, "Salary"], ZA)',
                ],
            },
            'WINDOW_BAD_N': {
                'message': "nthvalue: N must be a number >= 1.",
                'wrong': 'nthvalue(m[:, "X"], 0)',
                'right': 'nthvalue(m[:, "X"], 2)',
                'explanation': "N — value number in the group.",
                'variants': ['r = nthvalue(m[:, "X"], 2)'],
            },
            'WINDOW_REQUIRES_ASSIGNMENT': {
                'message': "nthvalue() returns a value — save the result.",
                'wrong': 'nthvalue(m[:, "X"], 2)',
                'right': 'r = nthvalue(m[:, "X"], 2)',
                'explanation': "Returns a new matrix.",
                'variants': ['r = nthvalue(m[:, "X"], 2)'],
            },
        },
    },

    # ============================================================
    # WINSUM
    # ============================================================
    'winsum': {
        'name': 'winsum',
        'category': 'window',
        'signature': 'winsum(m[:, "X"] [, by ...] [, order ...] [, AZ|ZA])',
        'description': 'Cumulative sum. Column __winsum. Returns a MATRIX.',
        'examples': ['r = winsum(m[:, "Sales"], by m[:, "Department"], order m[:, "Date"], AZ)'],
        'errors': {
            'WINDOW_BAD_SYNTAX': {
                'message': "winsum: invalid syntax.",
                'wrong': 'winsum(m)',
                'right': 'winsum(m[:, "Sales"], by m[:, "Department"])',
                'explanation': (
                    "winsum works over a SINGLE COLUMN.\n"
                    "\n"
                    "Structure:\n"
                    "  winsum(m[:, \"X\"], by ..., order ..., AZ|ZA)"
                ),
                'variants': ['r = winsum(m[:, "Sales"])'],
            },
            'WINDOW_REQUIRES_ASSIGNMENT': {
                'message': "winsum() returns a value — save the result.",
                'wrong': 'winsum(m[:, "Sales"])',
                'right': 'r = winsum(m[:, "Sales"])',
                'explanation': (
                    "winsum does NOT modify the source matrix.\n"
                    "It RETURNS a NEW one."
                ),
                'variants': [
                    'r = winsum(m[:, "Sales"])',
                    'm = winsum(m[:, "Sales"])',
                ],
            },
        },
    },

    # ============================================================
    # WINAVG
    # ============================================================
    'winavg': {
        'name': 'winavg',
        'category': 'window',
        'signature': 'winavg(m[:, "X"] [, by ...] [, order ...])',
        'description': 'Cumulative average. Column __winavg. Returns a MATRIX.',
        'examples': ['r = winavg(m[:, "Sales"], by m[:, "Department"])'],
        'errors': {
            'WINDOW_BAD_SYNTAX': {
                'message': "winavg: invalid syntax.",
                'wrong': 'winavg(m)',
                'right': 'winavg(m[:, "Sales"], by m[:, "Department"])',
                'explanation': "Structure: winavg(m[:, \"X\"], by ...)",
                'variants': ['r = winavg(m[:, "Sales"])'],
            },
            'WINDOW_REQUIRES_ASSIGNMENT': {
                'message': "winavg() returns a value — save the result.",
                'wrong': 'winavg(m[:, "Sales"])',
                'right': 'r = winavg(m[:, "Sales"])',
                'explanation': "Returns a new matrix.",
                'variants': ['r = winavg(m[:, "Sales"])'],
            },
        },
    },

    # ============================================================
    # WINCOUNT
    # ============================================================
    'wincount': {
        'name': 'wincount',
        'category': 'window',
        'signature': 'wincount(m[:, "X"] [, by ...] [, order ...])',
        'description': 'Cumulative count. Column __wincount. Returns a MATRIX.',
        'examples': ['r = wincount(m[:, "Sales"])'],
        'errors': {
            'WINDOW_BAD_SYNTAX': {
                'message': "wincount: invalid syntax.",
                'wrong': 'wincount(m)',
                'right': 'wincount(m[:, "Sales"])',
                'explanation': "Structure: wincount(m[:, \"X\"])",
                'variants': ['r = wincount(m[:, "Sales"])'],
            },
            'WINDOW_REQUIRES_ASSIGNMENT': {
                'message': "wincount() returns a value — save the result.",
                'wrong': 'wincount(m[:, "Sales"])',
                'right': 'r = wincount(m[:, "Sales"])',
                'explanation': "Returns a new matrix.",
                'variants': ['r = wincount(m[:, "Sales"])'],
            },
        },
    },

    # ============================================================
    # WINMIN
    # ============================================================
    'winmin': {
        'name': 'winmin',
        'category': 'window',
        'signature': 'winmin(m[:, "X"] [, by ...] [, order ...])',
        'description': 'Cumulative minimum. Column __winmin. Returns a MATRIX.',
        'examples': ['r = winmin(m[:, "Sales"], by m[:, "Department"])'],
        'errors': {
            'WINDOW_BAD_SYNTAX': {
                'message': "winmin: invalid syntax.",
                'wrong': 'winmin(m)',
                'right': 'winmin(m[:, "Sales"], by m[:, "Department"])',
                'explanation': "Structure: winmin(m[:, \"X\"], by ...)",
                'variants': ['r = winmin(m[:, "Sales"])'],
            },
            'WINDOW_REQUIRES_ASSIGNMENT': {
                'message': "winmin() returns a value — save the result.",
                'wrong': 'winmin(m[:, "Sales"])',
                'right': 'r = winmin(m[:, "Sales"])',
                'explanation': "Returns a new matrix.",
                'variants': ['r = winmin(m[:, "Sales"])'],
            },
        },
    },

    # ============================================================
    # WINMAX
    # ============================================================
    'winmax': {
        'name': 'winmax',
        'category': 'window',
        'signature': 'winmax(m[:, "X"] [, by ...] [, order ...])',
        'description': 'Cumulative maximum. Column __winmax. Returns a MATRIX.',
        'examples': ['r = winmax(m[:, "Sales"], by m[:, "Department"])'],
        'errors': {
            'WINDOW_BAD_SYNTAX': {
                'message': "winmax: invalid syntax.",
                'wrong': 'winmax(m)',
                'right': 'winmax(m[:, "Sales"], by m[:, "Department"])',
                'explanation': "Structure: winmax(m[:, \"X\"], by ...)",
                'variants': ['r = winmax(m[:, "Sales"])'],
            },
            'WINDOW_REQUIRES_ASSIGNMENT': {
                'message': "winmax() returns a value — save the result.",
                'wrong': 'winmax(m[:, "Sales"])',
                'right': 'r = winmax(m[:, "Sales"])',
                'explanation': "Returns a new matrix.",
                'variants': ['r = winmax(m[:, "Sales"])'],
            },
        },
    },

    # ============================================================
    # WINMEDIAN
    # ============================================================
    'winmedian': {
        'name': 'winmedian',
        'category': 'window',
        'signature': 'winmedian(m[:, "X"] [, by ...] [, order ...])',
        'description': 'Cumulative median. Column __winmedian. Returns a MATRIX.',
        'examples': ['r = winmedian(m[:, "Sales"])'],
        'errors': {
            'WINDOW_BAD_SYNTAX': {
                'message': "winmedian: invalid syntax.",
                'wrong': 'winmedian(m)',
                'right': 'winmedian(m[:, "Sales"])',
                'explanation': "Structure: winmedian(m[:, \"X\"])",
                'variants': ['r = winmedian(m[:, "Sales"])'],
            },
            'WINDOW_REQUIRES_ASSIGNMENT': {
                'message': "winmedian() returns a value — save the result.",
                'wrong': 'winmedian(m[:, "Sales"])',
                'right': 'r = winmedian(m[:, "Sales"])',
                'explanation': "Returns a new matrix.",
                'variants': ['r = winmedian(m[:, "Sales"])'],
            },
        },
    },

    # ============================================================
    # WINSTDEV
    # ============================================================
    'winstdev': {
        'name': 'winstdev',
        'category': 'window',
        'signature': 'winstdev(m[:, "X"] [, by ...] [, order ...])',
        'description': 'Cumulative standard deviation. Column __winstdev. Returns a MATRIX.',
        'examples': ['r = winstdev(m[:, "Sales"])'],
        'errors': {
            'WINDOW_BAD_SYNTAX': {
                'message': "winstdev: invalid syntax.",
                'wrong': 'winstdev(m)',
                'right': 'winstdev(m[:, "Sales"])',
                'explanation': "Structure: winstdev(m[:, \"X\"])",
                'variants': ['r = winstdev(m[:, "Sales"])'],
            },
            'WINDOW_REQUIRES_ASSIGNMENT': {
                'message': "winstdev() returns a value — save the result.",
                'wrong': 'winstdev(m[:, "Sales"])',
                'right': 'r = winstdev(m[:, "Sales"])',
                'explanation': "Returns a new matrix.",
                'variants': ['r = winstdev(m[:, "Sales"])'],
            },
        },
    },

    # ============================================================
    # QUALIFY
    # ============================================================
    'qualify': {
        'name': 'qualify',
        'category': 'window',
        'signature': 'qualify(m, <window_function> <OP> <value>)',
        'description': (
            'Filter rows by a window function.\n'
            '  • Analog of WHERE for window functions.\n'
            '  • Example: qualify(m, rownumber(...) <= 3).\n'
            '  • Works with Matrix and DuckDB.\n'
            '  • Returns a NEW MATRIX.'
        ),
        'examples': [
            'r = qualify(m, rownumber(m, by m[:, "Department"], order m[:, "Salary"], ZA) <= 2)',
            'r = qualify(m, rank(m, by m[:, "Department"], order m[:, "Salary"], ZA) == 1)',
        ],
        'errors': {
            'QUALIFY_BAD_SYNTAX': {
                'message': (
                    "qualify: invalid syntax.\n"
                    "  Need a table and a window-function condition."
                ),
                'wrong': 'qualify(m)',
                'right': 'qualify(m, rownumber(m, by m[:, "Department"]) <= 3)',
                'explanation': (
                    "qualify takes TWO arguments:\n"
                    "  1. table\n"
                    "  2. condition with a window function\n"
                    "\n"
                    "Structure:\n"
                    "  qualify(m, <window_function> <OP> <value>)\n"
                    "\n"
                    "OP: <, >, <=, >=, ==, !="
                ),
                'variants': [
                    'r = qualify(m, rownumber(m, by m[:, "Department"]) <= 3)',
                    'r = qualify(m, rank(m, by m[:, "Department"]) == 1)',
                ],
            },
            'QUALIFY_NO_WINDOW': {
                'message': (
                    "qualify: the condition must include a WINDOW function.\n"
                    "  Example: rownumber, rank, lag, winsum."
                ),
                'wrong': 'qualify(m, m[:, "Department"] == "IT")',
                'right': 'qualify(m, rownumber(m, by m[:, "Department"]) == 1)',
                'explanation': (
                    "qualify filters by the result of a window function,\n"
                    "not by a plain condition (use filterif for that).\n"
                    "\n"
                    "Allowed window functions:\n"
                    "  rownumber, rank, denserank, percentrank,\n"
                    "  cumedist, ntile, lag, lead,\n"
                    "  firstvalue, lastvalue, nthvalue,\n"
                    "  winsum, winavg, wincount, winmin, winmax,\n"
                    "  winmedian, winstdev"
                ),
                'variants': [
                    'r = qualify(m, rownumber(m, by m[:, "Department"]) <= 3)',
                    'r = qualify(m, rank(m, order m[:, "Salary"], ZA) == 1)',
                ],
            },
            'QUALIFY_REQUIRES_ASSIGNMENT': {
                'message': "qualify() returns a value — save the result.",
                'wrong': 'qualify(m, rownumber(m, by m[:, "Department"]) <= 3)',
                'right': 'r = qualify(m, rownumber(m, by m[:, "Department"]) <= 3)',
                'explanation': (
                    "qualify returns a NEW matrix.\n"
                    "\n"
                    "Correct:\n"
                    "  r = qualify(...)\n"
                    "  m = qualify(...)"
                ),
                'variants': [
                    'r = qualify(m, rownumber(m, by m[:, "Department"]) <= 3)',
                    'm = qualify(m, rownumber(m, by m[:, "Department"]) <= 3)',
                ],
            },
        },
    },
}