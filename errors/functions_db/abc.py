# errors/functions_db/abc.py
"""
База ошибок для функции ABC — ABC-анализ (Парето 80/20).

СИНТАКСИС:
    abc(срез)
    abc(срез, %)
    abc(срез, coef)
    abc(срез, %, m[:, 3])
    abc(срез, 70, 90)
    abc(срез, 70, 90, %, m[:, 3])
    abc(срез, m[:, 3], %)
    abc(срез, 90, %, m[:, 3], 70)

ПРАВИЛА:
    - Пороги по умолчанию: 80 / 95.
    - Если пользователь указал пороги в обратном порядке
      (например, 90, 70) — они АВТОМАТИЧЕСКИ меняются местами.
      Ошибки в этом случае НЕТ.
    - %     — проценты (0–100), округление 2 знака.
    - coef  — коэффициент (0.0–1.0), округление 4 знака.
    - Целевой столбец — срез m[:, N] или m[:, "Имя"] или m[:, end+1].
    - __abc вставляется СПРАВА от исходного среза.
    - Порядок аргументов — ЛЮБОЙ.
    - Порядок строк СОХРАНЯЕТСЯ.
"""


RU = {
    'abc': {
        'name': 'abc',
        'category': 'analytics',
        'signature': 'abc(срез [, порог1, порог2] [, %|coef] [, m[:, N]])',
        'description': (
            'ABC-анализ (Парето 80/20).\n'
            '  • Считает накопительную долю по убыванию.\n'
            '  • Присваивает "A" / "B" / "C".\n'
            '  • Порядок строк сохраняется.\n'
            '  • __abc вставляется справа от среза.\n'
            '  • % или coef — доля в отдельный столбец.\n'
            '  • Пороги по умолчанию: 80 / 95.\n'
            '  • Порядок аргументов — ЛЮБОЙ.\n'
            '  • Пороги автосортируются: 90, 70 → 70, 90.\n'
            '  • Работает с Matrix (RAM) и DuckDB (BigData).'
        ),
        'examples': [
            'r = abc(m[:, "Продажи"])',
            'r = abc(m[:, "Продажи"], %)',
            'r = abc(m[:, "Продажи"], coef)',
            'r = abc(m[:, "Продажи"], 70, 90, %)',
            'r = abc(m[:, "Продажи"], %, m[:, end+1])',
            'r = abc(m[:, "Продажи"], 70, 90, %, m[:, 3])',
        ],
        'errors': {
            'ABC_BAD_SYNTAX': {
                'message': (
                    "abc: неожиданный аргумент.\n"
                    "  Ожидается: порог (число), % или coef, срез m[:, N]."
                ),
                'wrong': 'r = abc(m[:, "Продажи"], "лишнее")',
                'right': 'r = abc(m[:, "Продажи"], %)',
                'explanation': (
                    "После среза допустимо:\n"
                    "     • числа — пороги (максимум 2)\n"
                    "     • % или coef — опция доли\n"
                    "     • m[:, N] — целевой столбец\n"
                    "\n"
                    "Порядок аргументов — ЛЮБОЙ."
                ),
                'variants': [
                    'r = abc(m[:, "Продажи"])',
                    'r = abc(m[:, "Продажи"], %)',
                    'r = abc(m[:, "Продажи"], 70, 90, %)',
                    'r = abc(m[:, "Продажи"], %, m[:, end+1])',
                ],
            },
            'ABC_NEED_SLICE': {
                'message': (
                    "abc: первый аргумент — срез m[:, \"X\"].\n"
                    "  Нельзя передать целую матрицу или вектор."
                ),
                'wrong': 'r = abc(m)',
                'right': 'r = abc(m[:, "Продажи"])',
                'explanation': (
                    "abc работает с ОДНИМ ЧИСЛОВЫМ столбцом.\n"
                    "Нужно указать срез:\n"
                    "     m[:, \"Продажи\"]      — по имени\n"
                    "     m[:, 3]             — по номеру\n"
                    "     m[:, end]           — последний\n"
                    "\n"
                    "Неправильно:\n"
                    "     abc(m)              — вся матрица\n"
                    "     abc(v)              — вектор (без имени)\n"
                    "\n"
                    "Правильно:\n"
                    "     abc(m[:, \"Продажи\"])"
                ),
                'variants': [
                    'r = abc(m[:, "Продажи"])',
                    'r = abc(m[:, 3])',
                    'r = abc(m[:, end])',
                ],
            },
            'ABC_TOO_MANY_THRESHOLDS': {
                'message': (
                    "abc: не больше ДВУХ порогов (границы A и AB)."
                ),
                'wrong': 'r = abc(m[:, "Продажи"], 60, 80, 95)',
                'right': 'r = abc(m[:, "Продажи"], 80, 95)',
                'explanation': (
                    "ABC-анализ использует РОВНО ДВА порога:\n"
                    "     порог1 — граница A\n"
                    "     порог2 — граница AB\n"
                    "\n"
                    "Третий порог не нужен — он не имеет смысла.\n"
                    "\n"
                    "Неправильно:\n"
                    "     abc(m[:, \"X\"], 60, 80, 95)\n"
                    "\n"
                    "Правильно:\n"
                    "     abc(m[:, \"X\"])              — 80 / 95\n"
                    "     abc(m[:, \"X\"], 80, 95)\n"
                    "     abc(m[:, \"X\"], 70, 90)"
                ),
                'variants': [
                    'r = abc(m[:, "Продажи"])',
                    'r = abc(m[:, "Продажи"], 70, 90)',
                ],
            },
            'ABC_TOO_MANY_OPTIONS': {
                'message': (
                    "abc: только ОДНА опция вывода доли — "
                    "% или coef."
                ),
                'wrong': 'r = abc(m[:, "Продажи"], %, coef)',
                'right': 'r = abc(m[:, "Продажи"], %)',
                'explanation': (
                    "Опция вывода доли — только одна:\n"
                    "     %     — проценты (0–100), 2 знака\n"
                    "     coef  — коэффициент (0.0–1.0), 4 знака\n"
                    "\n"
                    "Нельзя указать обе сразу.\n"
                    "\n"
                    "Неправильно:\n"
                    "     abc(m[:, \"X\"], %, coef)\n"
                    "\n"
                    "Правильно:\n"
                    "     abc(m[:, \"X\"], %)\n"
                    "     abc(m[:, \"X\"], coef)"
                ),
                'variants': [
                    'r = abc(m[:, "Продажи"], %)',
                    'r = abc(m[:, "Продажи"], coef)',
                ],
            },
            'ABC_TOO_MANY_TARGETS': {
                'message': (
                    "abc: только ОДИН целевой столбец."
                ),
                'wrong': 'r = abc(m[:, "Продажи"], %, m[:, 3], m[:, 4])',
                'right': 'r = abc(m[:, "Продажи"], %, m[:, 3])',
                'explanation': (
                    "Целевой столбец — куда положить значения доли.\n"
                    "Только ОДИН:\n"
                    "     m[:, 3]             — по номеру\n"
                    "     m[:, \"Доля_%\"]      — по имени\n"
                    "     m[:, end+1]         — новый столбец справа\n"
                    "\n"
                    "Неправильно:\n"
                    "     abc(m[:, \"X\"], %, m[:, 3], m[:, 4])\n"
                    "\n"
                    "Правильно:\n"
                    "     abc(m[:, \"X\"], %, m[:, end+1])"
                ),
                'variants': [
                    'r = abc(m[:, "Продажи"], %, m[:, end+1])',
                    'r = abc(m[:, "Продажи"], coef, m[:, 3])',
                ],
            },
            'ABC_TARGET_WITHOUT_OPTION': {
                'message': (
                    "abc: если указан целевой столбец — "
                    "нужно указать %, или coef."
                ),
                'wrong': 'r = abc(m[:, "Продажи"], m[:, 3])',
                'right': 'r = abc(m[:, "Продажи"], %, m[:, 3])',
                'explanation': (
                    "Целевой столбец принимает значения доли.\n"
                    "Но сама доля не считается без опции.\n"
                    "\n"
                    "Нужно указать ЧТО считать:\n"
                    "     %     — проценты (0–100)\n"
                    "     coef  — коэффициент (0.0–1.0)\n"
                    "\n"
                    "Неправильно:\n"
                    "     abc(m[:, \"X\"], m[:, 3])\n"
                    "\n"
                    "Правильно:\n"
                    "     abc(m[:, \"X\"], %, m[:, 3])\n"
                    "     abc(m[:, \"X\"], coef, m[:, end+1])"
                ),
                'variants': [
                    'r = abc(m[:, "Продажи"], %, m[:, 3])',
                    'r = abc(m[:, "Продажи"], coef, m[:, end+1])',
                ],
            },
            'ABC_BAD_TARGET': {
                'message': (
                    "abc: целевой столбец должен быть срезом m[:, N]."
                ),
                'wrong': 'r = abc(m[:, "Продажи"], %, 3)',
                'right': 'r = abc(m[:, "Продажи"], %, m[:, 3])',
                'explanation': (
                    "Целевой столбец — это СРЕЗ:\n"
                    "     m[:, 3]             — по номеру\n"
                    "     m[:, \"Доля\"]        — по имени\n"
                    "     m[:, end+1]         — новый справа\n"
                    "\n"
                    "Неправильно:\n"
                    "     abc(m[:, \"X\"], %, 3)        — просто число\n"
                    "     abc(m[:, \"X\"], %, \"Доля\")    — просто строка\n"
                    "\n"
                    "Правильно:\n"
                    "     abc(m[:, \"X\"], %, m[:, 3])\n"
                    "     abc(m[:, \"X\"], %, m[:, end+1])"
                ),
                'variants': [
                    'r = abc(m[:, "Продажи"], %, m[:, 3])',
                    'r = abc(m[:, "Продажи"], %, m[:, end+1])',
                ],
            },
            'ABC_NOT_NUMERIC': {
                'message': (
                    "abc: столбец должен содержать ЧИСЛА."
                ),
                'wrong': 'r = abc(m[:, "Имя"])',
                'right': 'r = abc(m[:, "Продажи"])',
                'explanation': (
                    "ABC-анализ работает только с ЧИСЛОВЫМИ значениями.\n"
                    "Текстовые столбцы не подходят.\n"
                    "\n"
                    "Проверьте столбец:\n"
                    "     print(m[1:5, \"Имя\"])\n"
                    "\n"
                    "Если нужно сгруппировать текст — используйте:\n"
                    "     groupby, pivot, ValueCounts"
                ),
                'variants': [
                    'r = abc(m[:, "Продажи"])',
                    'r = abc(m[:, "Выручка"])',
                ],
            },
            'ABC_ZERO_SUM': {
                'message': (
                    "abc: сумма значений = 0. ABC-анализ невозможен."
                ),
                'wrong': 'r = abc(m[:, "Продажи"])   # все нули',
                'right': 'r = abc(m[:, "Продажи"])   # есть ненулевые',
                'explanation': (
                    "ABC-анализ считает НАКОПИТЕЛЬНУЮ ДОЛЮ:\n"
                    "     доля[i] = сумма[i] / общая_сумма\n"
                    "\n"
                    "Если общая сумма = 0 — деление на 0 невозможно.\n"
                    "\n"
                    "Проверьте столбец:\n"
                    "     s = sum(m[:, \"Продажи\"])\n"
                    "     print(s)"
                ),
                'variants': [
                    'r = abc(m[:, "Продажи"])',
                    'r = abc(m[:, "Выручка"])',
                ],
            },
            'ABC_DUCKDB_ROW_RANGE': {
                'message': (
                    "abc: DuckDB не поддерживает диапазоны строк."
                ),
                'wrong': 'r = abc(bd[2:10, "Продажи"])',
                'right': 'r = abc(bd[:, "Продажи"])',
                'explanation': (
                    "BigData (DuckDB) — read-only view на файл.\n"
                    "Диапазоны строк на нём не поддерживаются.\n"
                    "\n"
                    "Используйте полный срез:\n"
                    "     abc(bd[:, \"Продажи\"])\n"
                    "\n"
                    "Если нужен диапазон — отфильтруйте сначала:\n"
                    "     bd2 = filterif(bd[:, \"Год\"] == 2025)\n"
                    "     r = abc(bd2[:, \"Продажи\"])"
                ),
                'variants': [
                    'r = abc(bd[:, "Продажи"])',
                    'bd2 = filterif(bd[:, "Год"] == 2025)\nr = abc(bd2[:, "Продажи"])',
                ],
            },
            'ABC_REQUIRES_ASSIGNMENT': {
                'message': (
                    "abc() возвращает значение — "
                    "результат нужно сохранить."
                ),
                'wrong': 'abc(m[:, "Продажи"])',
                'right': 'r = abc(m[:, "Продажи"])',
                'explanation': (
                    "abc НЕ изменяет исходную матрицу.\n"
                    "Он ВОЗВРАЩАЕТ НОВУЮ с добавленным столбцом __abc.\n"
                    "\n"
                    "Правильно:\n"
                    "  r = abc(...)           — в новую переменную\n"
                    "  m = abc(...)           — мутация\n"
                    "  print(abc(...))        — вывод"
                ),
                'variants': [
                    'r = abc(m[:, "Продажи"])',
                    'm = abc(m[:, "Продажи"])',
                    'print(abc(m[:, "Продажи"]))',
                ],
            },
        },
    },
}


EN = {
    'abc': {
        'name': 'abc',
        'category': 'analytics',
        'signature': 'abc(slice [, threshold1, threshold2] [, %|coef] [, m[:, N]])',
        'description': (
            'ABC analysis (Pareto 80/20).\n'
            '  • Cumulative share sorted descending.\n'
            '  • Assigns "A" / "B" / "C".\n'
            '  • Row order is preserved.\n'
            '  • __abc inserted right of the slice.\n'
            '  • % or coef — share into a separate column.\n'
            '  • Default thresholds: 80 / 95.\n'
            '  • Argument order — ANY.\n'
            '  • Thresholds are auto-sorted: 90, 70 → 70, 90.\n'
            '  • Works with Matrix (RAM) and DuckDB (BigData).'
        ),
        'examples': [
            'r = abc(m[:, "Sales"])',
            'r = abc(m[:, "Sales"], %)',
            'r = abc(m[:, "Sales"], coef)',
            'r = abc(m[:, "Sales"], 70, 90, %)',
            'r = abc(m[:, "Sales"], %, m[:, end+1])',
            'r = abc(m[:, "Sales"], 70, 90, %, m[:, 3])',
        ],
        'errors': {
            'ABC_BAD_SYNTAX': {
                'message': (
                    "abc: unexpected argument.\n"
                    "  Expected: threshold (number), % or coef, slice m[:, N]."
                ),
                'wrong': 'r = abc(m[:, "Sales"], "extra")',
                'right': 'r = abc(m[:, "Sales"], %)',
                'explanation': (
                    "After the slice, the following is allowed:\n"
                    "     • numbers — thresholds (max 2)\n"
                    "     • % or coef — share option\n"
                    "     • m[:, N] — target column\n"
                    "\n"
                    "Argument order — ANY."
                ),
                'variants': [
                    'r = abc(m[:, "Sales"])',
                    'r = abc(m[:, "Sales"], %)',
                    'r = abc(m[:, "Sales"], 70, 90, %)',
                    'r = abc(m[:, "Sales"], %, m[:, end+1])',
                ],
            },
            'ABC_NEED_SLICE': {
                'message': (
                    "abc: first argument must be a slice m[:, \"X\"].\n"
                    "  Cannot pass the whole matrix or a vector."
                ),
                'wrong': 'r = abc(m)',
                'right': 'r = abc(m[:, "Sales"])',
                'explanation': (
                    "abc works with ONE NUMERIC column.\n"
                    "Specify a slice:\n"
                    "     m[:, \"Sales\"]      — by name\n"
                    "     m[:, 3]             — by number\n"
                    "     m[:, end]           — last\n"
                    "\n"
                    "Incorrect:\n"
                    "     abc(m)              — whole matrix\n"
                    "     abc(v)              — vector (no name)\n"
                    "\n"
                    "Correct:\n"
                    "     abc(m[:, \"Sales\"])"
                ),
                'variants': [
                    'r = abc(m[:, "Sales"])',
                    'r = abc(m[:, 3])',
                    'r = abc(m[:, end])',
                ],
            },
            'ABC_TOO_MANY_THRESHOLDS': {
                'message': (
                    "abc: no more than TWO thresholds (boundaries A and AB)."
                ),
                'wrong': 'r = abc(m[:, "Sales"], 60, 80, 95)',
                'right': 'r = abc(m[:, "Sales"], 80, 95)',
                'explanation': (
                    "ABC analysis uses EXACTLY TWO thresholds:\n"
                    "     threshold1 — boundary of A\n"
                    "     threshold2 — boundary of AB\n"
                    "\n"
                    "A third threshold makes no sense.\n"
                    "\n"
                    "Incorrect:\n"
                    "     abc(m[:, \"X\"], 60, 80, 95)\n"
                    "\n"
                    "Correct:\n"
                    "     abc(m[:, \"X\"])              — 80 / 95\n"
                    "     abc(m[:, \"X\"], 80, 95)\n"
                    "     abc(m[:, \"X\"], 70, 90)"
                ),
                'variants': [
                    'r = abc(m[:, "Sales"])',
                    'r = abc(m[:, "Sales"], 70, 90)',
                ],
            },
            'ABC_TOO_MANY_OPTIONS': {
                'message': (
                    "abc: only ONE share-output option — % or coef."
                ),
                'wrong': 'r = abc(m[:, "Sales"], %, coef)',
                'right': 'r = abc(m[:, "Sales"], %)',
                'explanation': (
                    "Share-output option — only one:\n"
                    "     %     — percent (0–100), 2 decimals\n"
                    "     coef  — ratio (0.0–1.0), 4 decimals\n"
                    "\n"
                    "Both at once are not allowed.\n"
                    "\n"
                    "Incorrect:\n"
                    "     abc(m[:, \"X\"], %, coef)\n"
                    "\n"
                    "Correct:\n"
                    "     abc(m[:, \"X\"], %)\n"
                    "     abc(m[:, \"X\"], coef)"
                ),
                'variants': [
                    'r = abc(m[:, "Sales"], %)',
                    'r = abc(m[:, "Sales"], coef)',
                ],
            },
            'ABC_TOO_MANY_TARGETS': {
                'message': "abc: only ONE target column.",
                'wrong': 'r = abc(m[:, "Sales"], %, m[:, 3], m[:, 4])',
                'right': 'r = abc(m[:, "Sales"], %, m[:, 3])',
                'explanation': (
                    "Target column — where to put share values.\n"
                    "Only ONE:\n"
                    "     m[:, 3]             — by number\n"
                    "     m[:, \"Share_%\"]      — by name\n"
                    "     m[:, end+1]         — new column on the right\n"
                    "\n"
                    "Incorrect:\n"
                    "     abc(m[:, \"X\"], %, m[:, 3], m[:, 4])\n"
                    "\n"
                    "Correct:\n"
                    "     abc(m[:, \"X\"], %, m[:, end+1])"
                ),
                'variants': [
                    'r = abc(m[:, "Sales"], %, m[:, end+1])',
                    'r = abc(m[:, "Sales"], coef, m[:, 3])',
                ],
            },
            'ABC_TARGET_WITHOUT_OPTION': {
                'message': (
                    "abc: if target column is given — "
                    "% or coef is required."
                ),
                'wrong': 'r = abc(m[:, "Sales"], m[:, 3])',
                'right': 'r = abc(m[:, "Sales"], %, m[:, 3])',
                'explanation': (
                    "The target column accepts share values.\n"
                    "But the share itself is not computed without an option.\n"
                    "\n"
                    "Specify WHAT to compute:\n"
                    "     %     — percent (0–100)\n"
                    "     coef  — ratio (0.0–1.0)\n"
                    "\n"
                    "Incorrect:\n"
                    "     abc(m[:, \"X\"], m[:, 3])\n"
                    "\n"
                    "Correct:\n"
                    "     abc(m[:, \"X\"], %, m[:, 3])\n"
                    "     abc(m[:, \"X\"], coef, m[:, end+1])"
                ),
                'variants': [
                    'r = abc(m[:, "Sales"], %, m[:, 3])',
                    'r = abc(m[:, "Sales"], coef, m[:, end+1])',
                ],
            },
            'ABC_BAD_TARGET': {
                'message': (
                    "abc: target column must be a slice m[:, N]."
                ),
                'wrong': 'r = abc(m[:, "Sales"], %, 3)',
                'right': 'r = abc(m[:, "Sales"], %, m[:, 3])',
                'explanation': (
                    "Target column is a SLICE:\n"
                    "     m[:, 3]             — by number\n"
                    "     m[:, \"Share\"]       — by name\n"
                    "     m[:, end+1]         — new on the right\n"
                    "\n"
                    "Incorrect:\n"
                    "     abc(m[:, \"X\"], %, 3)        — plain number\n"
                    "     abc(m[:, \"X\"], %, \"Share\")  — plain string\n"
                    "\n"
                    "Correct:\n"
                    "     abc(m[:, \"X\"], %, m[:, 3])\n"
                    "     abc(m[:, \"X\"], %, m[:, end+1])"
                ),
                'variants': [
                    'r = abc(m[:, "Sales"], %, m[:, 3])',
                    'r = abc(m[:, "Sales"], %, m[:, end+1])',
                ],
            },
            'ABC_NOT_NUMERIC': {
                'message': (
                    "abc: column must contain NUMBERS."
                ),
                'wrong': 'r = abc(m[:, "Name"])',
                'right': 'r = abc(m[:, "Sales"])',
                'explanation': (
                    "ABC analysis works only with NUMERIC values.\n"
                    "Text columns do not fit.\n"
                    "\n"
                    "Check the column:\n"
                    "     print(m[1:5, \"Name\"])\n"
                    "\n"
                    "To group text — use:\n"
                    "     groupby, pivot, ValueCounts"
                ),
                'variants': [
                    'r = abc(m[:, "Sales"])',
                    'r = abc(m[:, "Revenue"])',
                ],
            },
            'ABC_ZERO_SUM': {
                'message': (
                    "abc: sum of values = 0. ABC analysis is impossible."
                ),
                'wrong': 'r = abc(m[:, "Sales"])   # all zeros',
                'right': 'r = abc(m[:, "Sales"])   # has non-zeros',
                'explanation': (
                    "ABC analysis computes CUMULATIVE SHARE:\n"
                    "     share[i] = sum[i] / total_sum\n"
                    "\n"
                    "If total sum = 0 — division by 0 is impossible.\n"
                    "\n"
                    "Check the column:\n"
                    "     s = sum(m[:, \"Sales\"])\n"
                    "     print(s)"
                ),
                'variants': [
                    'r = abc(m[:, "Sales"])',
                    'r = abc(m[:, "Revenue"])',
                ],
            },
            'ABC_DUCKDB_ROW_RANGE': {
                'message': (
                    "abc: DuckDB does not support row ranges."
                ),
                'wrong': 'r = abc(bd[2:10, "Sales"])',
                'right': 'r = abc(bd[:, "Sales"])',
                'explanation': (
                    "BigData (DuckDB) — read-only view on a file.\n"
                    "Row ranges are not supported.\n"
                    "\n"
                    "Use a full slice:\n"
                    "     abc(bd[:, \"Sales\"])\n"
                    "\n"
                    "If you need a range — filter first:\n"
                    "     bd2 = filterif(bd[:, \"Year\"] == 2025)\n"
                    "     r = abc(bd2[:, \"Sales\"])"
                ),
                'variants': [
                    'r = abc(bd[:, "Sales"])',
                    'bd2 = filterif(bd[:, "Year"] == 2025)\nr = abc(bd2[:, "Sales"])',
                ],
            },
            'ABC_REQUIRES_ASSIGNMENT': {
                'message': (
                    "abc() returns a value — "
                    "the result must be saved."
                ),
                'wrong': 'abc(m[:, "Sales"])',
                'right': 'r = abc(m[:, "Sales"])',
                'explanation': (
                    "abc does NOT modify the source matrix.\n"
                    "It RETURNS a NEW one with added column __abc.\n"
                    "\n"
                    "Correct:\n"
                    "  r = abc(...)           — to a new variable\n"
                    "  m = abc(...)           — mutation\n"
                    "  print(abc(...))        — output"
                ),
                'variants': [
                    'r = abc(m[:, "Sales"])',
                    'm = abc(m[:, "Sales"])',
                    'print(abc(m[:, "Sales"]))',
                ],
            },
        },
    },
}