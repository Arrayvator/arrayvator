# errors/functions_db/anomaly.py
"""
База ошибок для функции ANOMALY — поиск аномалий (выбросов).

СИНТАКСИС (порядок аргументов ЛЮБОЙ):
    anomaly(срез)
    anomaly(срез, iqr)
    anomaly(срез, iqr, 3.0)
    anomaly(срез, zscore)
    anomaly(срез, zscore, 2)
    anomaly(срез, percentile)
    anomaly(срез, percentile, 5, 95)
    anomaly(срез, by m[:, "Магазин"])
    anomaly(срез, only)
    anomaly(срез, only, approx)
    anomaly(срез, by m[:, "Магазин"], iqr, 3.0, approx, only)

МЕТОДЫ:
    iqr        — межквартильный размах (по умолчанию, k=1.5)
    zscore     — z-отклонение (N=3)
    percentile — процентили (lo=1, hi=99)

ПРАВИЛА:
    - Возвращает МАТРИЦУ в исходном порядке строк.
    - Новый столбец __anomaly справа от исходного среза:
        0  — норма
        -1 — ниже нижней границы
        1  — выше верхней границы
        None — значение None / не число / мало данных в группе (< 4)
    - Работает с Matrix (RAM) и DuckDB (BigData).
"""

RU = {
    'anomaly': {
        'name': 'anomaly',
        'category': 'analytics',
        'signature': (
            'anomaly(срез [, iqr|zscore|percentile] [, N] '
            '[, by m[:, "Y"]] [, only] [, approx])'
        ),
        'description': (
            'Поиск аномалий (выбросов) в числовом столбце.\n'
            '  • iqr (по умолчанию, k=1.5) — межквартильный размах.\n'
            '  • zscore (N=3) — z-отклонение.\n'
            '  • percentile (1, 99) — процентили.\n'
            '  • by — аномалия внутри группы.\n'
            '  • only — только аномальные строки.\n'
            '  • approx — приблизительные процентили (DuckDB).\n'
            '  • Столбец __anomaly: 0 / -1 / 1 / None.\n'
            '  • Порядок аргументов — ЛЮБОЙ.\n'
            '  • Работает с Matrix (RAM) и DuckDB (BigData).'
        ),
        'examples': [
            'r = anomaly(m[:, "Сумма"])',
            'r = anomaly(m[:, "Сумма"], zscore, 2)',
            'r = anomaly(m[:, "Сумма"], percentile, 5, 95)',
            'r = anomaly(m[:, "Сумма"], iqr, 3.0)',
            'r = anomaly(m[:, "Сумма"], by m[:, "Магазин"])',
            'r = anomaly(m[:, "Сумма"], only, approx)',
            'r = anomaly(m[:, "Сумма"], by m[:, "Магазин"], iqr, approx, only)',
        ],
        'errors': {
            'ANOMALY_BAD_SYNTAX': {
                'message': (
                    "anomaly: неверный синтаксис.\n"
                    "  Первый аргумент — срез m[:, \"X\"].\n"
                    "  Остальные — метод, параметры, by, only, approx."
                ),
                'wrong': 'r = anomaly()',
                'right': 'r = anomaly(m[:, "Сумма"])',
                'explanation': (
                    "anomaly принимает срез и опционально:\n"
                    "  • метод — iqr / zscore / percentile\n"
                    "  • параметры метода (числа, макс. 2)\n"
                    "  • by m[:, \"Y\"] — группировка\n"
                    "  • only — только аномалии\n"
                    "  • approx — приблизительные процентили\n"
                    "\n"
                    "Порядок аргументов — ЛЮБОЙ."
                ),
                'variants': [
                    'r = anomaly(m[:, "Сумма"])',
                    'r = anomaly(m[:, "Сумма"], zscore, 2)',
                    'r = anomaly(m[:, "Сумма"], by m[:, "Магазин"], iqr, approx, only)',
                ],
            },
            'ANOMALY_NEED_SLICE': {
                'message': (
                    "anomaly: первый аргумент — срез m[:, \"X\"].\n"
                    "  Нельзя передать целую матрицу или скаляр."
                ),
                'wrong': 'r = anomaly(m)',
                'right': 'r = anomaly(m[:, "Сумма"])',
                'explanation': (
                    "anomaly работает с ОДНИМ числовым столбцом.\n"
                    "Нужно указать срез:\n"
                    "     m[:, \"Сумма\"]      — по имени\n"
                    "     m[:, 3]            — по номеру\n"
                    "     m[:, end]          — последний\n"
                    "\n"
                    "Неправильно:\n"
                    "     anomaly(m)              — вся матрица\n"
                    "     anomaly(v)              — вектор (без имени)\n"
                    "\n"
                    "Правильно:\n"
                    "     anomaly(m[:, \"Сумма\"])"
                ),
                'variants': [
                    'r = anomaly(m[:, "Сумма"])',
                    'r = anomaly(m[:, 3])',
                    'r = anomaly(m[:, end])',
                ],
            },
            'ANOMALY_BAD_METHOD': {
                'message': (
                    "anomaly: неверный метод или метод указан дважды.\n"
                    "  Допустимо: iqr, zscore, percentile."
                ),
                'wrong': 'r = anomaly(m[:, "Сумма"], median)',
                'right': 'r = anomaly(m[:, "Сумма"], iqr)',
                'explanation': (
                    "Только ТРИ метода:\n"
                    "     iqr         — межквартильный размах (по умолчанию)\n"
                    "     zscore      — z-отклонение\n"
                    "     percentile  — процентили\n"
                    "\n"
                    "Метод указывается ОДИН РАЗ.\n"
                    "\n"
                    "Неправильно:\n"
                    "     anomaly(m[:, \"X\"], median)\n"
                    "     anomaly(m[:, \"X\"], iqr, zscore)\n"
                    "\n"
                    "Правильно:\n"
                    "     anomaly(m[:, \"X\"], iqr)\n"
                    "     anomaly(m[:, \"X\"], zscore, 2)"
                ),
                'variants': [
                    'r = anomaly(m[:, "Сумма"])',
                    'r = anomaly(m[:, "Сумма"], iqr, 3.0)',
                    'r = anomaly(m[:, "Сумма"], zscore, 2)',
                    'r = anomaly(m[:, "Сумма"], percentile, 5, 95)',
                ],
            },
            'ANOMALY_BAD_PARAM': {
                'message': (
                    "anomaly: параметр метода должен быть числом."
                ),
                'wrong': 'r = anomaly(m[:, "Сумма"], zscore, "2")',
                'right': 'r = anomaly(m[:, "Сумма"], zscore, 2)',
                'explanation': (
                    "Параметры метода — ЧИСЛА без кавычек:\n"
                    "     anomaly(m[:, \"X\"], iqr, 3.0)          — k=3.0\n"
                    "     anomaly(m[:, \"X\"], zscore, 2)         — N=2\n"
                    "     anomaly(m[:, \"X\"], percentile, 5, 95) — 5%, 95%\n"
                    "\n"
                    "Неправильно:\n"
                    "     anomaly(m[:, \"X\"], zscore, \"2\")"
                ),
                'variants': [
                    'r = anomaly(m[:, "Сумма"], iqr, 3.0)',
                    'r = anomaly(m[:, "Сумма"], zscore, 2)',
                    'r = anomaly(m[:, "Сумма"], percentile, 5, 95)',
                ],
            },
            'ANOMALY_TOO_MANY_PARAMS': {
                'message': (
                    "anomaly: не больше ДВУХ числовых параметров."
                ),
                'wrong': 'r = anomaly(m[:, "Сумма"], percentile, 5, 95, 99)',
                'right': 'r = anomaly(m[:, "Сумма"], percentile, 5, 95)',
                'explanation': (
                    "Максимум ДВА параметра:\n"
                    "     iqr          → k (1 параметр)\n"
                    "     zscore       → N (1 параметр)\n"
                    "     percentile   → lo, hi (2 параметра)\n"
                    "\n"
                    "Неправильно:\n"
                    "     anomaly(m[:, \"X\"], percentile, 5, 95, 99)\n"
                    "\n"
                    "Правильно:\n"
                    "     anomaly(m[:, \"X\"], percentile, 5, 95)"
                ),
                'variants': [
                    'r = anomaly(m[:, "Сумма"], iqr, 3.0)',
                    'r = anomaly(m[:, "Сумма"], zscore, 2)',
                    'r = anomaly(m[:, "Сумма"], percentile, 5, 95)',
                ],
            },
            'ANOMALY_PERCENTILE_NEEDS_TWO': {
                'message': (
                    "anomaly: метод percentile требует ДВА параметра.\n"
                    "  Пример: percentile, 5, 95."
                ),
                'wrong': 'r = anomaly(m[:, "Сумма"], percentile, 5)',
                'right': 'r = anomaly(m[:, "Сумма"], percentile, 5, 95)',
                'explanation': (
                    "percentile требует РОВНО ДВА параметра:\n"
                    "     anomaly(m[:, \"X\"], percentile)         — 1, 99 (по умолч.)\n"
                    "     anomaly(m[:, \"X\"], percentile, 5)      — ошибка\n"
                    "     anomaly(m[:, \"X\"], percentile, 5, 95)  — правильно"
                ),
                'variants': [
                    'r = anomaly(m[:, "Сумма"], percentile)',
                    'r = anomaly(m[:, "Сумма"], percentile, 1, 99)',
                    'r = anomaly(m[:, "Сумма"], percentile, 5, 95)',
                ],
            },
            'ANOMALY_BAD_BY': {
                'message': (
                    "anomaly: by должен быть срезом m[:, \"X\"]."
                ),
                'wrong': 'r = anomaly(m[:, "Сумма"], by "Магазин")',
                'right': 'r = anomaly(m[:, "Сумма"], by m[:, "Магазин"])',
                'explanation': (
                    "by принимает СРЕЗ столбца-группировки:\n"
                    "     by m[:, \"Магазин\"]\n"
                    "     by m[:, 1]\n"
                    "\n"
                    "Неправильно:\n"
                    "     by \"Магазин\"\n"
                    "     by 1"
                ),
                'variants': [
                    'r = anomaly(m[:, "Сумма"], by m[:, "Магазин"])',
                    'r = anomaly(m[:, "Сумма"], by m[:, 1])',
                ],
            },
            'ANOMALY_TOO_MANY_BY': {
                'message': (
                    "anomaly: by указан больше одного раза."
                ),
                'wrong': 'r = anomaly(m[:, "Сумма"], by m[:, "A"], by m[:, "B"])',
                'right': 'r = anomaly(m[:, "Сумма"], by m[:, "Магазин"])',
                'explanation': (
                    "Опция by — только ОДНА.\n"
                    "\n"
                    "Неправильно:\n"
                    "     anomaly(m[:, \"X\"], by m[:, \"A\"], by m[:, \"B\"])\n"
                    "\n"
                    "Правильно:\n"
                    "     anomaly(m[:, \"X\"], by m[:, \"Магазин\"])"
                ),
                'variants': [
                    'r = anomaly(m[:, "Сумма"], by m[:, "Магазин"])',
                    'r = anomaly(m[:, "Сумма"], by m[:, 1])',
                ],
            },
            'ANOMALY_BAD_ARG': {
                'message': (
                    "anomaly: неожиданный аргумент.\n"
                    "  Ожидается: iqr|zscore|percentile, число, "
                    "by m[:, \"X\"], only, approx."
                ),
                'wrong': 'r = anomaly(m[:, "Сумма"], "лишнее")',
                'right': 'r = anomaly(m[:, "Сумма"], iqr)',
                'explanation': (
                    "После первого среза допустимо:\n"
                    "     iqr / zscore / percentile   — метод\n"
                    "     число                       — параметр\n"
                    "     by m[:, \"X\"]                — группировка\n"
                    "     only                        — только аномалии\n"
                    "     approx                      — приближённые\n"
                    "\n"
                    "Порядок аргументов — ЛЮБОЙ."
                ),
                'variants': [
                    'r = anomaly(m[:, "Сумма"])',
                    'r = anomaly(m[:, "Сумма"], iqr)',
                    'r = anomaly(m[:, "Сумма"], by m[:, "Магазин"])',
                    'r = anomaly(m[:, "Сумма"], only)',
                    'r = anomaly(m[:, "Сумма"], only, approx)',
                ],
            },
            'ANOMALY_NOT_NUMERIC': {
                'message': (
                    "anomaly: столбец должен содержать ЧИСЛА."
                ),
                'wrong': 'r = anomaly(m[:, "Имя"])',
                'right': 'r = anomaly(m[:, "Сумма"])',
                'explanation': (
                    "anomaly работает только с ЧИСЛОВЫМИ значениями.\n"
                    "Текстовые столбцы не подходят.\n"
                    "\n"
                    "Проверьте столбец:\n"
                    "     print(m[1:5, \"Имя\"])"
                ),
                'variants': [
                    'r = anomaly(m[:, "Сумма"])',
                    'r = anomaly(m[:, "Выручка"])',
                ],
            },
            'ANOMALY_DUCKDB_ROW_RANGE': {
                'message': (
                    "anomaly: DuckDB не поддерживает диапазоны строк."
                ),
                'wrong': 'r = anomaly(bd[2:10, "Сумма"])',
                'right': 'r = anomaly(bd[:, "Сумма"])',
                'explanation': (
                    "BigData (DuckDB) — read-only view на файл.\n"
                    "Диапазоны строк на нём не поддерживаются.\n"
                    "\n"
                    "Используйте полный срез:\n"
                    "     anomaly(bd[:, \"Сумма\"])\n"
                    "\n"
                    "Если нужен диапазон — сначала отфильтруйте:\n"
                    "     bd2 = filterif(bd[:, \"Год\"] == 2025)\n"
                    "     r = anomaly(bd2[:, \"Сумма\"])"
                ),
                'variants': [
                    'r = anomaly(bd[:, "Сумма"])',
                    'bd2 = filterif(bd[:, "Год"] == 2025)\nr = anomaly(bd2[:, "Сумма"])',
                ],
            },
            'ANOMALY_REQUIRES_ASSIGNMENT': {
                'message': (
                    "anomaly() возвращает значение — "
                    "результат нужно сохранить."
                ),
                'wrong': 'anomaly(m[:, "Сумма"])',
                'right': 'r = anomaly(m[:, "Сумма"])',
                'explanation': (
                    "anomaly НЕ изменяет исходную матрицу.\n"
                    "Он ВОЗВРАЩАЕТ НОВУЮ с добавленным столбцом __anomaly.\n"
                    "\n"
                    "Правильно:\n"
                    "  r = anomaly(...)       — в новую переменную\n"
                    "  m = anomaly(...)       — мутация\n"
                    "  print(anomaly(...))    — вывод"
                ),
                'variants': [
                    'r = anomaly(m[:, "Сумма"])',
                    'm = anomaly(m[:, "Сумма"])',
                    'print(anomaly(m[:, "Сумма"]))',
                ],
            },
        },
    },
}


EN = {
    'anomaly': {
        'name': 'anomaly',
        'category': 'analytics',
        'signature': (
            'anomaly(slice [, iqr|zscore|percentile] [, N] '
            '[, by m[:, "Y"]] [, only] [, approx])'
        ),
        'description': (
            'Detect anomalies (outliers) in a numeric column.\n'
            '  • iqr (default, k=1.5) — interquartile range.\n'
            '  • zscore (N=3) — z-score.\n'
            '  • percentile (1, 99) — percentiles.\n'
            '  • by — anomaly within group.\n'
            '  • only — only anomalous rows.\n'
            '  • approx — approximate percentiles (DuckDB).\n'
            '  • Column __anomaly: 0 / -1 / 1 / None.\n'
            '  • Argument order — ANY.\n'
            '  • Works with Matrix (RAM) and DuckDB (BigData).'
        ),
        'examples': [
            'r = anomaly(m[:, "Amount"])',
            'r = anomaly(m[:, "Amount"], zscore, 2)',
            'r = anomaly(m[:, "Amount"], percentile, 5, 95)',
            'r = anomaly(m[:, "Amount"], iqr, 3.0)',
            'r = anomaly(m[:, "Amount"], by m[:, "Store"])',
            'r = anomaly(m[:, "Amount"], only, approx)',
            'r = anomaly(m[:, "Amount"], by m[:, "Store"], iqr, approx, only)',
        ],
        'errors': {
            'ANOMALY_BAD_SYNTAX': {
                'message': (
                    "anomaly: invalid syntax.\n"
                    "  First argument — slice m[:, \"X\"].\n"
                    "  Others — method, params, by, only, approx."
                ),
                'wrong': 'r = anomaly()',
                'right': 'r = anomaly(m[:, "Amount"])',
                'explanation': (
                    "anomaly takes a slice and optionally:\n"
                    "  • method — iqr / zscore / percentile\n"
                    "  • method params (numbers, max 2)\n"
                    "  • by m[:, \"Y\"] — grouping\n"
                    "  • only — anomalous only\n"
                    "  • approx — approximate percentiles\n"
                    "\n"
                    "Argument order — ANY."
                ),
                'variants': [
                    'r = anomaly(m[:, "Amount"])',
                    'r = anomaly(m[:, "Amount"], zscore, 2)',
                    'r = anomaly(m[:, "Amount"], by m[:, "Store"], iqr, approx, only)',
                ],
            },
            'ANOMALY_NEED_SLICE': {
                'message': (
                    "anomaly: first argument must be a slice m[:, \"X\"].\n"
                    "  Cannot pass the whole matrix or a scalar."
                ),
                'wrong': 'r = anomaly(m)',
                'right': 'r = anomaly(m[:, "Amount"])',
                'explanation': (
                    "anomaly works with ONE NUMERIC column.\n"
                    "Specify a slice:\n"
                    "     m[:, \"Amount\"]      — by name\n"
                    "     m[:, 3]              — by number\n"
                    "     m[:, end]            — last\n"
                    "\n"
                    "Incorrect:\n"
                    "     anomaly(m)              — whole matrix\n"
                    "     anomaly(v)              — vector (no name)\n"
                    "\n"
                    "Correct:\n"
                    "     anomaly(m[:, \"Amount\"])"
                ),
                'variants': [
                    'r = anomaly(m[:, "Amount"])',
                    'r = anomaly(m[:, 3])',
                    'r = anomaly(m[:, end])',
                ],
            },
            'ANOMALY_BAD_METHOD': {
                'message': (
                    "anomaly: invalid method or method specified twice.\n"
                    "  Allowed: iqr, zscore, percentile."
                ),
                'wrong': 'r = anomaly(m[:, "Amount"], median)',
                'right': 'r = anomaly(m[:, "Amount"], iqr)',
                'explanation': (
                    "Only THREE methods:\n"
                    "     iqr         — interquartile range (default)\n"
                    "     zscore      — z-score\n"
                    "     percentile  — percentiles\n"
                    "\n"
                    "Method — only ONCE.\n"
                    "\n"
                    "Incorrect:\n"
                    "     anomaly(m[:, \"X\"], median)\n"
                    "     anomaly(m[:, \"X\"], iqr, zscore)\n"
                    "\n"
                    "Correct:\n"
                    "     anomaly(m[:, \"X\"], iqr)\n"
                    "     anomaly(m[:, \"X\"], zscore, 2)"
                ),
                'variants': [
                    'r = anomaly(m[:, "Amount"])',
                    'r = anomaly(m[:, "Amount"], iqr, 3.0)',
                    'r = anomaly(m[:, "Amount"], zscore, 2)',
                    'r = anomaly(m[:, "Amount"], percentile, 5, 95)',
                ],
            },
            'ANOMALY_BAD_PARAM': {
                'message': (
                    "anomaly: method parameter must be a number."
                ),
                'wrong': 'r = anomaly(m[:, "Amount"], zscore, "2")',
                'right': 'r = anomaly(m[:, "Amount"], zscore, 2)',
                'explanation': (
                    "Method params are NUMBERS without quotes:\n"
                    "     anomaly(m[:, \"X\"], iqr, 3.0)          — k=3.0\n"
                    "     anomaly(m[:, \"X\"], zscore, 2)         — N=2\n"
                    "     anomaly(m[:, \"X\"], percentile, 5, 95) — 5%, 95%\n"
                    "\n"
                    "Incorrect:\n"
                    "     anomaly(m[:, \"X\"], zscore, \"2\")"
                ),
                'variants': [
                    'r = anomaly(m[:, "Amount"], iqr, 3.0)',
                    'r = anomaly(m[:, "Amount"], zscore, 2)',
                    'r = anomaly(m[:, "Amount"], percentile, 5, 95)',
                ],
            },
            'ANOMALY_TOO_MANY_PARAMS': {
                'message': (
                    "anomaly: at most TWO numeric parameters."
                ),
                'wrong': 'r = anomaly(m[:, "Amount"], percentile, 5, 95, 99)',
                'right': 'r = anomaly(m[:, "Amount"], percentile, 5, 95)',
                'explanation': (
                    "At most TWO params:\n"
                    "     iqr          → k (1 param)\n"
                    "     zscore       → N (1 param)\n"
                    "     percentile   → lo, hi (2 params)\n"
                    "\n"
                    "Incorrect:\n"
                    "     anomaly(m[:, \"X\"], percentile, 5, 95, 99)\n"
                    "\n"
                    "Correct:\n"
                    "     anomaly(m[:, \"X\"], percentile, 5, 95)"
                ),
                'variants': [
                    'r = anomaly(m[:, "Amount"], iqr, 3.0)',
                    'r = anomaly(m[:, "Amount"], zscore, 2)',
                    'r = anomaly(m[:, "Amount"], percentile, 5, 95)',
                ],
            },
            'ANOMALY_PERCENTILE_NEEDS_TWO': {
                'message': (
                    "anomaly: percentile method requires TWO parameters.\n"
                    "  Example: percentile, 5, 95."
                ),
                'wrong': 'r = anomaly(m[:, "Amount"], percentile, 5)',
                'right': 'r = anomaly(m[:, "Amount"], percentile, 5, 95)',
                'explanation': (
                    "percentile requires EXACTLY TWO params:\n"
                    "     anomaly(m[:, \"X\"], percentile)         — 1, 99 (default)\n"
                    "     anomaly(m[:, \"X\"], percentile, 5)      — error\n"
                    "     anomaly(m[:, \"X\"], percentile, 5, 95)  — correct"
                ),
                'variants': [
                    'r = anomaly(m[:, "Amount"], percentile)',
                    'r = anomaly(m[:, "Amount"], percentile, 1, 99)',
                    'r = anomaly(m[:, "Amount"], percentile, 5, 95)',
                ],
            },
            'ANOMALY_BAD_BY': {
                'message': (
                    "anomaly: by must be a slice m[:, \"X\"]."
                ),
                'wrong': 'r = anomaly(m[:, "Amount"], by "Store")',
                'right': 'r = anomaly(m[:, "Amount"], by m[:, "Store"])',
                'explanation': (
                    "by takes a column SLICE:\n"
                    "     by m[:, \"Store\"]\n"
                    "     by m[:, 1]\n"
                    "\n"
                    "Incorrect:\n"
                    "     by \"Store\"\n"
                    "     by 1"
                ),
                'variants': [
                    'r = anomaly(m[:, "Amount"], by m[:, "Store"])',
                    'r = anomaly(m[:, "Amount"], by m[:, 1])',
                ],
            },
            'ANOMALY_TOO_MANY_BY': {
                'message': (
                    "anomaly: by specified more than once."
                ),
                'wrong': 'r = anomaly(m[:, "Amount"], by m[:, "A"], by m[:, "B"])',
                'right': 'r = anomaly(m[:, "Amount"], by m[:, "Store"])',
                'explanation': (
                    "Option by — only ONCE.\n"
                    "\n"
                    "Incorrect:\n"
                    "     anomaly(m[:, \"X\"], by m[:, \"A\"], by m[:, \"B\"])\n"
                    "\n"
                    "Correct:\n"
                    "     anomaly(m[:, \"X\"], by m[:, \"Store\"])"
                ),
                'variants': [
                    'r = anomaly(m[:, "Amount"], by m[:, "Store"])',
                    'r = anomaly(m[:, "Amount"], by m[:, 1])',
                ],
            },
            'ANOMALY_BAD_ARG': {
                'message': (
                    "anomaly: unexpected argument.\n"
                    "  Expected: iqr|zscore|percentile, number, "
                    "by m[:, \"X\"], only, approx."
                ),
                'wrong': 'r = anomaly(m[:, "Amount"], "extra")',
                'right': 'r = anomaly(m[:, "Amount"], iqr)',
                'explanation': (
                    "After the first slice, only these are allowed:\n"
                    "     iqr / zscore / percentile   — method\n"
                    "     number                       — param\n"
                    "     by m[:, \"X\"]                — grouping\n"
                    "     only                         — anomalous only\n"
                    "     approx                       — approximate\n"
                    "\n"
                    "Argument order — ANY."
                ),
                'variants': [
                    'r = anomaly(m[:, "Amount"])',
                    'r = anomaly(m[:, "Amount"], iqr)',
                    'r = anomaly(m[:, "Amount"], by m[:, "Store"])',
                    'r = anomaly(m[:, "Amount"], only)',
                    'r = anomaly(m[:, "Amount"], only, approx)',
                ],
            },
            'ANOMALY_NOT_NUMERIC': {
                'message': (
                    "anomaly: column must contain NUMBERS."
                ),
                'wrong': 'r = anomaly(m[:, "Name"])',
                'right': 'r = anomaly(m[:, "Amount"])',
                'explanation': (
                    "anomaly works only with NUMERIC values.\n"
                    "Text columns do not fit.\n"
                    "\n"
                    "Check the column:\n"
                    "     print(m[1:5, \"Name\"])"
                ),
                'variants': [
                    'r = anomaly(m[:, "Amount"])',
                    'r = anomaly(m[:, "Revenue"])',
                ],
            },
            'ANOMALY_DUCKDB_ROW_RANGE': {
                'message': (
                    "anomaly: DuckDB does not support row ranges."
                ),
                'wrong': 'r = anomaly(bd[2:10, "Amount"])',
                'right': 'r = anomaly(bd[:, "Amount"])',
                'explanation': (
                    "BigData (DuckDB) is a read-only view on a file.\n"
                    "Row ranges are not supported.\n"
                    "\n"
                    "Use a full slice:\n"
                    "     anomaly(bd[:, \"Amount\"])\n"
                    "\n"
                    "If you need a range — filter first:\n"
                    "     bd2 = filterif(bd[:, \"Year\"] == 2025)\n"
                    "     r = anomaly(bd2[:, \"Amount\"])"
                ),
                'variants': [
                    'r = anomaly(bd[:, "Amount"])',
                    'bd2 = filterif(bd[:, "Year"] == 2025)\nr = anomaly(bd2[:, "Amount"])',
                ],
            },
            'ANOMALY_REQUIRES_ASSIGNMENT': {
                'message': (
                    "anomaly() returns a value — "
                    "the result must be saved."
                ),
                'wrong': 'anomaly(m[:, "Amount"])',
                'right': 'r = anomaly(m[:, "Amount"])',
                'explanation': (
                    "anomaly does NOT modify the source matrix.\n"
                    "It RETURNS a NEW one with column __anomaly.\n"
                    "\n"
                    "Correct:\n"
                    "  r = anomaly(...)       — to a new variable\n"
                    "  m = anomaly(...)       — mutation\n"
                    "  print(anomaly(...))    — output"
                ),
                'variants': [
                    'r = anomaly(m[:, "Amount"])',
                    'm = anomaly(m[:, "Amount"])',
                    'print(anomaly(m[:, "Amount"]))',
                ],
            },
        },
    },
}