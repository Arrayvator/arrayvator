# errors/functions_db/percentof.py
"""
База ошибок для функции PERCENTOF — доля от итога.

СИНТАКСИС:
    percentof(срез)
    percentof(срез, coef)
    percentof(срез, by m[:, "Категория"])
    percentof(срез, by m[:, "Категория"], coef)

ПРАВИЛА:
    - Возвращает ВЕКТОР (не матрицу).
    - Без coef — проценты (0–100), 2 знака после запятой.
    - С coef — коэффициент (0.0–1.0), 4 знака после запятой.
    - by — доля внутри группы (PARTITION BY).
    - Запись в столбец — через addcolumn.
    - Порядок аргументов — ЛЮБОЙ.
    - Работает с Matrix (RAM) и DuckDB (BigData).
"""

RU = {
    'percentof': {
        'name': 'percentof',
        'category': 'analytics',
        'signature': 'percentof(срез [, coef] [, by m[:, "Y"]])',
        'description': (
            'Доля от итога (общей суммы или суммы группы).\n'
            '  • Без coef — проценты (0–100), 2 знака.\n'
            '  • С coef — коэффициент (0.0–1.0), 4 знака.\n'
            '  • by — доля внутри группы.\n'
            '  • Возвращает ВЕКТОР — запись через addcolumn.\n'
            '  • Порядок аргументов — ЛЮБОЙ.\n'
            '  • Работает с Matrix (RAM) и DuckDB (BigData).'
        ),
        'examples': [
            'r = percentof(m[:, "Продажи"])',
            'r = percentof(m[:, "Продажи"], coef)',
            'r = percentof(m[:, "Продажи"], by m[:, "Категория"])',
            'm = addcolumn(m, "Доля_%", percentof(m[:, "Продажи"]))',
            'm = addcolumn(m, "Доля_кат_%",\n'
            '              percentof(m[:, "Продажи"], by m[:, "Категория"]))',
        ],
        'errors': {
            'PERCENTOF_BAD_SYNTAX': {
                'message': (
                    "percentof: неверный синтаксис.\n"
                    "  Первый аргумент — срез m[:, \"X\"].\n"
                    "  Остальные — coef и/или by m[:, \"Y\"]."
                ),
                'wrong': 'r = percentof("Продажи")',
                'right': 'r = percentof(m[:, "Продажи"])',
                'explanation': (
                    "percentof принимает срез и опционально:\n"
                    "  • coef — коэффициент (0.0–1.0)\n"
                    "  • by m[:, \"Y\"] — группировка\n"
                    "\n"
                    "Порядок аргументов — ЛЮБОЙ."
                ),
                'variants': [
                    'r = percentof(m[:, "Продажи"])',
                    'r = percentof(m[:, "Продажи"], coef)',
                    'r = percentof(m[:, "Продажи"], by m[:, "Категория"])',
                    'r = percentof(m[:, "Продажи"], by m[:, "Категория"], coef)',
                ],
            },
            'PERCENTOF_NEED_SLICE': {
                'message': (
                    "percentof: первый аргумент — срез m[:, \"X\"].\n"
                    "  Нельзя передать целую матрицу или скаляр."
                ),
                'wrong': 'r = percentof(m)',
                'right': 'r = percentof(m[:, "Продажи"])',
                'explanation': (
                    "percentof работает с ОДНИМ числовым столбцом.\n"
                    "Нужно указать срез:\n"
                    "     m[:, \"Продажи\"]      — по имени\n"
                    "     m[:, 3]             — по номеру\n"
                    "     m[:, end]           — последний\n"
                    "\n"
                    "Неправильно:\n"
                    "     percentof(m)              — вся матрица\n"
                    "     percentof(v)              — вектор (без имени)\n"
                    "\n"
                    "Правильно:\n"
                    "     percentof(m[:, \"Продажи\"])"
                ),
                'variants': [
                    'r = percentof(m[:, "Продажи"])',
                    'r = percentof(m[:, 3])',
                    'r = percentof(m[:, end])',
                ],
            },
            'PERCENTOF_BAD_BY': {
                'message': (
                    "percentof: by должен быть срезом m[:, \"X\"].\n"
                    "  Не строкой и не числом."
                ),
                'wrong': 'r = percentof(m[:, "Продажи"], by "Категория")',
                'right': 'r = percentof(m[:, "Продажи"], by m[:, "Категория"])',
                'explanation': (
                    "by принимает СРЕЗ столбца-группировки:\n"
                    "     by m[:, \"Категория\"]\n"
                    "     by m[:, 1]\n"
                    "\n"
                    "Неправильно:\n"
                    "     by \"Категория\"\n"
                    "     by 1"
                ),
                'variants': [
                    'r = percentof(m[:, "Продажи"], by m[:, "Категория"])',
                    'r = percentof(m[:, "Продажи"], by m[:, 1])',
                ],
            },
            'PERCENTOF_TOO_MANY_OPTIONS': {
                'message': (
                    "percentof: coef указан больше одного раза."
                ),
                'wrong': 'r = percentof(m[:, "Продажи"], coef, coef)',
                'right': 'r = percentof(m[:, "Продажи"], coef)',
                'explanation': (
                    "Опция coef — только ОДНА.\n"
                    "\n"
                    "Неправильно:\n"
                    "     percentof(m[:, \"X\"], coef, coef)\n"
                    "\n"
                    "Правильно:\n"
                    "     percentof(m[:, \"X\"], coef)\n"
                    "     percentof(m[:, \"X\"], by m[:, \"Y\"], coef)"
                ),
                'variants': [
                    'r = percentof(m[:, "Продажи"], coef)',
                    'r = percentof(m[:, "Продажи"], by m[:, "Категория"], coef)',
                ],
            },
            'PERCENTOF_TOO_MANY_BY': {
                'message': (
                    "percentof: by указан больше одного раза."
                ),
                'wrong': 'r = percentof(m[:, "Продажи"], by m[:, "A"], by m[:, "B"])',
                'right': 'r = percentof(m[:, "Продажи"], by m[:, "Категория"])',
                'explanation': (
                    "Опция by — только ОДНА.\n"
                    "\n"
                    "Неправильно:\n"
                    "     percentof(m[:, \"X\"], by m[:, \"A\"], by m[:, \"B\"])\n"
                    "\n"
                    "Если нужно несколько ключей — используйте диапазон:\n"
                    "     percentof(m[:, \"X\"], by m[:, 1:2])"
                ),
                'variants': [
                    'r = percentof(m[:, "Продажи"], by m[:, "Категория"])',
                    'r = percentof(m[:, "Продажи"], by m[:, 1:2])',
                ],
            },
            'PERCENTOF_BAD_ARG': {
                'message': (
                    "percentof: неожиданный аргумент.\n"
                    "  Ожидается: coef или by m[:, \"X\"].\n"
                    "  Порядок аргументов — ЛЮБОЙ."
                ),
                'wrong': 'r = percentof(m[:, "Продажи"], "лишнее")',
                'right': 'r = percentof(m[:, "Продажи"], coef)',
                'explanation': (
                    "После первого среза допустимо ТОЛЬКО:\n"
                    "     coef                — коэффициент\n"
                    "     by m[:, \"X\"]       — группировка\n"
                    "\n"
                    "Порядок аргументов — ЛЮБОЙ."
                ),
                'variants': [
                    'r = percentof(m[:, "Продажи"])',
                    'r = percentof(m[:, "Продажи"], coef)',
                    'r = percentof(m[:, "Продажи"], by m[:, "Категория"])',
                    'r = percentof(m[:, "Продажи"], by m[:, "Категория"], coef)',
                    'r = percentof(m[:, "Продажи"], coef, by m[:, "Категория"])',
                ],
            },
            'PERCENTOF_NOT_NUMERIC': {
                'message': (
                    "percentof: столбец должен содержать ЧИСЛА."
                ),
                'wrong': 'r = percentof(m[:, "Имя"])',
                'right': 'r = percentof(m[:, "Продажи"])',
                'explanation': (
                    "percentof работает только с ЧИСЛОВЫМИ значениями.\n"
                    "Текстовые столбцы не подходят.\n"
                    "\n"
                    "Проверьте столбец:\n"
                    "     print(m[1:5, \"Имя\"])"
                ),
                'variants': [
                    'r = percentof(m[:, "Продажи"])',
                    'r = percentof(m[:, "Выручка"])',
                ],
            },
            'PERCENTOF_ZERO_SUM': {
                'message': (
                    "percentof: сумма значений = 0. Деление на 0."
                ),
                'wrong': 'r = percentof(m[:, "Продажи"])   # все нули',
                'right': 'r = percentof(m[:, "Продажи"])   # есть ненулевые',
                'explanation': (
                    "percentof считает ДОЛЮ:\n"
                    "     доля[i] = значение[i] / сумма\n"
                    "\n"
                    "Если сумма = 0 — деление невозможно.\n"
                    "В результате будут None.\n"
                    "\n"
                    "Проверьте столбец:\n"
                    "     s = sum(m[:, \"Продажи\"])\n"
                    "     print(s)"
                ),
                'variants': [
                    'r = percentof(m[:, "Продажи"])',
                    'r = percentof(m[:, "Выручка"])',
                ],
            },
            'PERCENTOF_DUCKDB_ROW_RANGE': {
                'message': (
                    "percentof: DuckDB не поддерживает диапазоны строк."
                ),
                'wrong': 'r = percentof(bd[2:10, "Продажи"])',
                'right': 'r = percentof(bd[:, "Продажи"])',
                'explanation': (
                    "BigData (DuckDB) — read-only view на файл.\n"
                    "Диапазоны строк на нём не поддерживаются.\n"
                    "\n"
                    "Используйте полный срез:\n"
                    "     percentof(bd[:, \"Продажи\"])\n"
                    "\n"
                    "Если нужен диапазон — сначала отфильтруйте:\n"
                    "     bd2 = filterif(bd[:, \"Год\"] == 2025)\n"
                    "     r = percentof(bd2[:, \"Продажи\"])"
                ),
                'variants': [
                    'r = percentof(bd[:, "Продажи"])',
                    'bd2 = filterif(bd[:, "Год"] == 2025)\nr = percentof(bd2[:, "Продажи"])',
                ],
            },
        },
    },
}


EN = {
    'percentof': {
        'name': 'percentof',
        'category': 'analytics',
        'signature': 'percentof(slice [, coef] [, by m[:, "Y"]])',
        'description': (
            'Share of total (grand total or group total).\n'
            '  • Without coef — percent (0–100), 2 decimals.\n'
            '  • With coef — ratio (0.0–1.0), 4 decimals.\n'
            '  • by — share within group.\n'
            '  • Returns a VECTOR — write via addcolumn.\n'
            '  • Argument order — ANY.\n'
            '  • Works with Matrix (RAM) and DuckDB (BigData).'
        ),
        'examples': [
            'r = percentof(m[:, "Sales"])',
            'r = percentof(m[:, "Sales"], coef)',
            'r = percentof(m[:, "Sales"], by m[:, "Category"])',
            'm = addcolumn(m, "Share_%", percentof(m[:, "Sales"]))',
            'm = addcolumn(m, "Cat_share_%",\n'
            '              percentof(m[:, "Sales"], by m[:, "Category"]))',
        ],
        'errors': {
            'PERCENTOF_BAD_SYNTAX': {
                'message': (
                    "percentof: invalid syntax.\n"
                    "  First argument — slice m[:, \"X\"].\n"
                    "  Others — coef and/or by m[:, \"Y\"]."
                ),
                'wrong': 'r = percentof("Sales")',
                'right': 'r = percentof(m[:, "Sales"])',
                'explanation': (
                    "percentof takes a slice and optionally:\n"
                    "  • coef — ratio (0.0–1.0)\n"
                    "  • by m[:, \"Y\"] — grouping\n"
                    "\n"
                    "Argument order — ANY."
                ),
                'variants': [
                    'r = percentof(m[:, "Sales"])',
                    'r = percentof(m[:, "Sales"], coef)',
                    'r = percentof(m[:, "Sales"], by m[:, "Category"])',
                    'r = percentof(m[:, "Sales"], by m[:, "Category"], coef)',
                ],
            },
            'PERCENTOF_NEED_SLICE': {
                'message': (
                    "percentof: first argument must be a slice m[:, \"X\"].\n"
                    "  Cannot pass the whole matrix or a scalar."
                ),
                'wrong': 'r = percentof(m)',
                'right': 'r = percentof(m[:, "Sales"])',
                'explanation': (
                    "percentof works with ONE NUMERIC column.\n"
                    "Specify a slice:\n"
                    "     m[:, \"Sales\"]      — by name\n"
                    "     m[:, 3]             — by number\n"
                    "     m[:, end]           — last\n"
                    "\n"
                    "Incorrect:\n"
                    "     percentof(m)              — whole matrix\n"
                    "     percentof(v)              — vector (no name)\n"
                    "\n"
                    "Correct:\n"
                    "     percentof(m[:, \"Sales\"])"
                ),
                'variants': [
                    'r = percentof(m[:, "Sales"])',
                    'r = percentof(m[:, 3])',
                    'r = percentof(m[:, end])',
                ],
            },
            'PERCENTOF_BAD_BY': {
                'message': (
                    "percentof: by must be a slice m[:, \"X\"].\n"
                    "  Not a string, not a number."
                ),
                'wrong': 'r = percentof(m[:, "Sales"], by "Category")',
                'right': 'r = percentof(m[:, "Sales"], by m[:, "Category"])',
                'explanation': (
                    "by takes a column SLICE of the grouping column:\n"
                    "     by m[:, \"Category\"]\n"
                    "     by m[:, 1]\n"
                    "\n"
                    "Incorrect:\n"
                    "     by \"Category\"\n"
                    "     by 1"
                ),
                'variants': [
                    'r = percentof(m[:, "Sales"], by m[:, "Category"])',
                    'r = percentof(m[:, "Sales"], by m[:, 1])',
                ],
            },
            'PERCENTOF_TOO_MANY_OPTIONS': {
                'message': (
                    "percentof: coef specified more than once."
                ),
                'wrong': 'r = percentof(m[:, "Sales"], coef, coef)',
                'right': 'r = percentof(m[:, "Sales"], coef)',
                'explanation': (
                    "Option coef — only ONCE.\n"
                    "\n"
                    "Incorrect:\n"
                    "     percentof(m[:, \"X\"], coef, coef)\n"
                    "\n"
                    "Correct:\n"
                    "     percentof(m[:, \"X\"], coef)\n"
                    "     percentof(m[:, \"X\"], by m[:, \"Y\"], coef)"
                ),
                'variants': [
                    'r = percentof(m[:, "Sales"], coef)',
                    'r = percentof(m[:, "Sales"], by m[:, "Category"], coef)',
                ],
            },
            'PERCENTOF_TOO_MANY_BY': {
                'message': (
                    "percentof: by specified more than once."
                ),
                'wrong': 'r = percentof(m[:, "Sales"], by m[:, "A"], by m[:, "B"])',
                'right': 'r = percentof(m[:, "Sales"], by m[:, "Category"])',
                'explanation': (
                    "Option by — only ONCE.\n"
                    "\n"
                    "Incorrect:\n"
                    "     percentof(m[:, \"X\"], by m[:, \"A\"], by m[:, \"B\"])\n"
                    "\n"
                    "For multiple keys — use a range:\n"
                    "     percentof(m[:, \"X\"], by m[:, 1:2])"
                ),
                'variants': [
                    'r = percentof(m[:, "Sales"], by m[:, "Category"])',
                    'r = percentof(m[:, "Sales"], by m[:, 1:2])',
                ],
            },
            'PERCENTOF_BAD_ARG': {
                'message': (
                    "percentof: unexpected argument.\n"
                    "  Expected: coef or by m[:, \"X\"].\n"
                    "  Argument order — ANY."
                ),
                'wrong': 'r = percentof(m[:, "Sales"], "extra")',
                'right': 'r = percentof(m[:, "Sales"], coef)',
                'explanation': (
                    "After the first slice, only these are allowed:\n"
                    "     coef                — ratio\n"
                    "     by m[:, \"X\"]       — grouping\n"
                    "\n"
                    "Argument order — ANY."
                ),
                'variants': [
                    'r = percentof(m[:, "Sales"])',
                    'r = percentof(m[:, "Sales"], coef)',
                    'r = percentof(m[:, "Sales"], by m[:, "Category"])',
                    'r = percentof(m[:, "Sales"], by m[:, "Category"], coef)',
                    'r = percentof(m[:, "Sales"], coef, by m[:, "Category"])',
                ],
            },
            'PERCENTOF_NOT_NUMERIC': {
                'message': (
                    "percentof: column must contain NUMBERS."
                ),
                'wrong': 'r = percentof(m[:, "Name"])',
                'right': 'r = percentof(m[:, "Sales"])',
                'explanation': (
                    "percentof works only with NUMERIC values.\n"
                    "Text columns do not fit.\n"
                    "\n"
                    "Check the column:\n"
                    "     print(m[1:5, \"Name\"])"
                ),
                'variants': [
                    'r = percentof(m[:, "Sales"])',
                    'r = percentof(m[:, "Revenue"])',
                ],
            },
            'PERCENTOF_ZERO_SUM': {
                'message': (
                    "percentof: sum of values = 0. Division by zero."
                ),
                'wrong': 'r = percentof(m[:, "Sales"])   # all zeros',
                'right': 'r = percentof(m[:, "Sales"])   # has non-zeros',
                'explanation': (
                    "percentof computes the SHARE:\n"
                    "     share[i] = value[i] / sum\n"
                    "\n"
                    "If sum = 0 — division is impossible.\n"
                    "Result will be None.\n"
                    "\n"
                    "Check the column:\n"
                    "     s = sum(m[:, \"Sales\"])\n"
                    "     print(s)"
                ),
                'variants': [
                    'r = percentof(m[:, "Sales"])',
                    'r = percentof(m[:, "Revenue"])',
                ],
            },
            'PERCENTOF_DUCKDB_ROW_RANGE': {
                'message': (
                    "percentof: DuckDB does not support row ranges."
                ),
                'wrong': 'r = percentof(bd[2:10, "Sales"])',
                'right': 'r = percentof(bd[:, "Sales"])',
                'explanation': (
                    "BigData (DuckDB) is a read-only view on a file.\n"
                    "Row ranges are not supported.\n"
                    "\n"
                    "Use a full slice:\n"
                    "     percentof(bd[:, \"Sales\"])\n"
                    "\n"
                    "If you need a range — filter first:\n"
                    "     bd2 = filterif(bd[:, \"Year\"] == 2025)\n"
                    "     r = percentof(bd2[:, \"Sales\"])"
                ),
                'variants': [
                    'r = percentof(bd[:, "Sales"])',
                    'bd2 = filterif(bd[:, "Year"] == 2025)\nr = percentof(bd2[:, "Sales"])',
                ],
            },
        },
    },
}