# errors/functions_db/groupagg.py
"""
База ошибок для функции GROUPAGG — блочная агрегация по маркеру.

СИНТАКСИС:
    groupagg(ключ-срез, значение-срез, agg)
    groupagg(ключ-срез, значение-срез, agg, "ИТОГО")
    groupagg(ключ-срез, значение-срез, agg, "ИТОГО", fill)
    groupagg(ключ-срез, значение-срез, agg, "ИТОГО", exact)

РЕЖИМЫ:
    fill  — пустые (None, "") присоединяются к текущему блоку (по умолчанию).
    exact — каждое значение — отдельный блок (даже пустое).

АГРЕГАТЫ: sum, count, avg, min, max, median, std, first, last.

⚠️  Работает ТОЛЬКО с Matrix (RAM).
    НЕ работает с BigData (DuckDB).
"""


RU = {
    'groupagg': {
        'name': 'groupagg',
        'category': 'analytics',
        'signature': 'groupagg(ключ, значение, agg [, имя] [, fill|exact])',
        'description': (
            'Блочная агрегация с группировкой по маркеру.\n'
            '  • Идёт по ключу, определяет блоки.\n'
            '  • Вставляет ИТОГ ПОСЛЕ каждого блока.\n'
            '  • Пустые значения присоединяются к текущему блоку (fill).\n'
            '  • Агрегаты: sum, count, avg, min, max, median, std, first, last.\n'
            '  • Возвращает НОВУЮ матрицу — результат нужно сохранить.\n'
            '  ⚠️  Работает только с Matrix (RAM), не с BigData (DuckDB).'
        ),
        'examples': [
            'r = groupagg(m[:, "Клиент"], m[:, "Сумма"], sum)',
            'r = groupagg(m[:, "Клиент"], m[:, "Сумма"], sum, "ИТОГО")',
            'r = groupagg(m[:, "Клиент"], m[:, "Сумма"], avg, "Среднее", exact)',
        ],
        'errors': {
            'GROUPAGG_BAD_SYNTAX': {
                'message': (
                    "groupagg: неверный синтаксис.\n"
                    "  Нужны ключ, значение и агрегат."
                ),
                'wrong': 'groupagg(m, "Клиент")',
                'right': 'groupagg(m[:, "Клиент"], m[:, "Сумма"], sum)',
                'explanation': (
                    "groupagg принимает минимум ТРИ аргумента:\n"
                    "  1. ключ — срез m[:, \"Клиент\"]\n"
                    "  2. значение — срез m[:, \"Сумма\"]\n"
                    "  3. агрегат — sum, count, avg, min, max, median, std, first, last\n"
                    "\n"
                    "Неправильно:\n"
                    "     groupagg(m, \"Клиент\")\n"
                    "\n"
                    "Правильно:\n"
                    "     groupagg(m[:, \"Клиент\"], m[:, \"Сумма\"], sum)"
                ),
                'variants': [
                    'r = groupagg(m[:, "Клиент"], m[:, "Сумма"], sum)',
                    'r = groupagg(m[:, "Клиент"], m[:, "Сумма"], sum, "ИТОГО")',
                ],
            },
            'GROUPAGG_BAD_KEY_SLICE': {
                'message': (
                    "groupagg: 1-й аргумент — срез m[:, \"X\"]."
                ),
                'wrong': 'groupagg("Клиент", m[:, "Сумма"], sum)',
                'right': 'groupagg(m[:, "Клиент"], m[:, "Сумма"], sum)',
                'explanation': (
                    "Первый аргумент — СРЕЗ столбца-маркера:\n"
                    "     m[:, \"Клиент\"]      — по имени\n"
                    "     m[:, 1]             — по номеру\n"
                    "\n"
                    "Неправильно:\n"
                    "     groupagg(\"Клиент\", m[:, \"Сумма\"], sum)\n"
                    "\n"
                    "Правильно:\n"
                    "     groupagg(m[:, \"Клиент\"], m[:, \"Сумма\"], sum)"
                ),
                'variants': [
                    'r = groupagg(m[:, "Клиент"], m[:, "Сумма"], sum)',
                    'r = groupagg(m[:, 1], m[:, 2], sum)',
                ],
            },
            'GROUPAGG_BAD_VALUE_SLICE': {
                'message': (
                    "groupagg: 2-й аргумент — срез m[:, \"X\"]."
                ),
                'wrong': 'groupagg(m[:, "Клиент"], "Сумма", sum)',
                'right': 'groupagg(m[:, "Клиент"], m[:, "Сумма"], sum)',
                'explanation': (
                    "Второй аргумент — СРЕЗ столбца-значения:\n"
                    "     m[:, \"Сумма\"]       — по имени\n"
                    "     m[:, 2]             — по номеру\n"
                    "\n"
                    "Неправильно:\n"
                    "     groupagg(m[:, \"Клиент\"], \"Сумма\", sum)\n"
                    "\n"
                    "Правильно:\n"
                    "     groupagg(m[:, \"Клиент\"], m[:, \"Сумма\"], sum)"
                ),
                'variants': [
                    'r = groupagg(m[:, "Клиент"], m[:, "Сумма"], sum)',
                    'r = groupagg(m[:, 1], m[:, 2], sum)',
                ],
            },
            'GROUPAGG_BAD_AGG': {
                'message': (
                    "groupagg: неверный агрегат.\n"
                    "  Допустимо: sum, count, avg, min, max, "
                    "median, std, first, last."
                ),
                'wrong': 'groupagg(m[:, "Клиент"], m[:, "Сумма"], average)',
                'right': 'groupagg(m[:, "Клиент"], m[:, "Сумма"], avg)',
                'explanation': (
                    "Только эти агрегаты:\n"
                    "     sum      — сумма\n"
                    "     count    — количество\n"
                    "     avg      — среднее\n"
                    "     min, max — минимум, максимум\n"
                    "     median   — медиана\n"
                    "     std      — стандартное отклонение\n"
                    "     first    — первое значение\n"
                    "     last     — последнее значение\n"
                    "\n"
                    "Неправильно:\n"
                    "     groupagg(m[:, \"Клиент\"], m[:, \"Сумма\"], average)\n"
                    "     groupagg(m[:, \"Клиент\"], m[:, \"Сумма\"], mean)\n"
                    "\n"
                    "Правильно:\n"
                    "     groupagg(m[:, \"Клиент\"], m[:, \"Сумма\"], avg)"
                ),
                'variants': [
                    'r = groupagg(m[:, "Клиент"], m[:, "Сумма"], sum)',
                    'r = groupagg(m[:, "Клиент"], m[:, "Сумма"], avg)',
                    'r = groupagg(m[:, "Клиент"], m[:, "Сумма"], count)',
                ],
            },
            'GROUPAGG_BAD_MODE': {
                'message': (
                    "groupagg: режим должен быть fill или exact."
                ),
                'wrong': 'groupagg(m[:, "Клиент"], m[:, "Сумма"], sum, "ИТОГО", all)',
                'right': 'groupagg(m[:, "Клиент"], m[:, "Сумма"], sum, "ИТОГО", fill)',
                'explanation': (
                    "Допустимо только два режима:\n"
                    "     fill  — пустые значения присоединяются к блоку (по умолчанию)\n"
                    "     exact — каждое значение — отдельный блок\n"
                    "\n"
                    "Неправильно:\n"
                    "     groupagg(..., all)\n"
                    "     groupagg(..., strict)\n"
                    "\n"
                    "Правильно:\n"
                    "     groupagg(..., fill)\n"
                    "     groupagg(..., exact)"
                ),
                'variants': [
                    'r = groupagg(m[:, "Клиент"], m[:, "Сумма"], sum, "ИТОГО", fill)',
                    'r = groupagg(m[:, "Клиент"], m[:, "Сумма"], sum, "ИТОГО", exact)',
                ],
            },
            'GROUPAGG_DUCKDB': {
                'message': (
                    "groupagg работает только с Matrix (RAM), "
                    "не с BigData (DuckDB).\n"
                    "  BigData — read-only view на файл."
                ),
                'wrong': 'r = groupagg(bd[:, "Клиент"], bd[:, "Сумма"], sum)',
                'right': (
                    'm = ToMatrix(bd)\n'
                    'r = groupagg(m[:, "Клиент"], m[:, "Сумма"], sum)'
                ),
                'explanation': (
                    "BigData (DuckDB) — read-only view на файл.\n"
                    "Он НЕ поддерживает блочную агрегацию.\n"
                    "\n"
                    "Решение:\n"
                    "  1. Конвертировать BigData в Matrix:\n"
                    "        m = ToMatrix(bd)\n"
                    "        r = groupagg(m[:, \"Клиент\"], m[:, \"Сумма\"], sum)\n"
                    "\n"
                    "  2. Использовать SQL-аналог:\n"
                    "        groupby, pivot"
                ),
                'variants': [
                    'm = ToMatrix(bd)\nr = groupagg(m[:, "Клиент"], m[:, "Сумма"], sum)',
                    'm = ToMatrix(bd)\nr = groupagg(m[:, "Клиент"], m[:, "Сумма"], sum, "ИТОГО")',
                ],
            },
            'GROUPAGG_REQUIRES_ASSIGNMENT': {
                'message': (
                    "groupagg() возвращает значение — "
                    "результат нужно сохранить."
                ),
                'wrong': 'groupagg(m[:, "Клиент"], m[:, "Сумма"], sum)',
                'right': 'r = groupagg(m[:, "Клиент"], m[:, "Сумма"], sum)',
                'explanation': (
                    "groupagg НЕ изменяет исходную матрицу.\n"
                    "Он ВОЗВРАЩАЕТ НОВУЮ.\n"
                    "\n"
                    "Правильно:\n"
                    "  r = groupagg(...)      — в новую переменную\n"
                    "  m = groupagg(...)      — мутация"
                ),
                'variants': [
                    'r = groupagg(m[:, "Клиент"], m[:, "Сумма"], sum)',
                    'm = groupagg(m[:, "Клиент"], m[:, "Сумма"], sum)',
                ],
            },
        },
    },
}


EN = {
    'groupagg': {
        'name': 'groupagg',
        'category': 'analytics',
        'signature': 'groupagg(key, value, agg [, name] [, fill|exact])',
        'description': (
            'Block aggregation by marker.\n'
            '  • Walks the key column, determines blocks.\n'
            '  • Inserts TOTAL AFTER each block.\n'
            '  • Empty values join the current block (fill).\n'
            '  • Aggregates: sum, count, avg, min, max, median, std, first, last.\n'
            '  • Returns a NEW matrix — save the result.\n'
            '  ⚠️  Works only with Matrix (RAM), not with BigData (DuckDB).'
        ),
        'examples': [
            'r = groupagg(m[:, "Client"], m[:, "Amount"], sum)',
            'r = groupagg(m[:, "Client"], m[:, "Amount"], sum, "TOTAL")',
            'r = groupagg(m[:, "Client"], m[:, "Amount"], avg, "Avg", exact)',
        ],
        'errors': {
            'GROUPAGG_BAD_SYNTAX': {
                'message': (
                    "groupagg: invalid syntax.\n"
                    "  Need key, value, and aggregate."
                ),
                'wrong': 'groupagg(m, "Client")',
                'right': 'groupagg(m[:, "Client"], m[:, "Amount"], sum)',
                'explanation': (
                    "groupagg takes at least THREE arguments:\n"
                    "  1. key — slice m[:, \"Client\"]\n"
                    "  2. value — slice m[:, \"Amount\"]\n"
                    "  3. aggregate — sum, count, avg, min, max, median, std, first, last\n"
                    "\n"
                    "Incorrect:\n"
                    "     groupagg(m, \"Client\")\n"
                    "\n"
                    "Correct:\n"
                    "     groupagg(m[:, \"Client\"], m[:, \"Amount\"], sum)"
                ),
                'variants': [
                    'r = groupagg(m[:, "Client"], m[:, "Amount"], sum)',
                    'r = groupagg(m[:, "Client"], m[:, "Amount"], sum, "TOTAL")',
                ],
            },
            'GROUPAGG_BAD_KEY_SLICE': {
                'message': (
                    "groupagg: 1st argument — slice m[:, \"X\"]."
                ),
                'wrong': 'groupagg("Client", m[:, "Amount"], sum)',
                'right': 'groupagg(m[:, "Client"], m[:, "Amount"], sum)',
                'explanation': (
                    "First argument is a SLICE of the marker column:\n"
                    "     m[:, \"Client\"]      — by name\n"
                    "     m[:, 1]             — by number\n"
                    "\n"
                    "Incorrect:\n"
                    "     groupagg(\"Client\", m[:, \"Amount\"], sum)\n"
                    "\n"
                    "Correct:\n"
                    "     groupagg(m[:, \"Client\"], m[:, \"Amount\"], sum)"
                ),
                'variants': [
                    'r = groupagg(m[:, "Client"], m[:, "Amount"], sum)',
                    'r = groupagg(m[:, 1], m[:, 2], sum)',
                ],
            },
            'GROUPAGG_BAD_VALUE_SLICE': {
                'message': (
                    "groupagg: 2nd argument — slice m[:, \"X\"]."
                ),
                'wrong': 'groupagg(m[:, "Client"], "Amount", sum)',
                'right': 'groupagg(m[:, "Client"], m[:, "Amount"], sum)',
                'explanation': (
                    "Second argument is a SLICE of the value column:\n"
                    "     m[:, \"Amount\"]       — by name\n"
                    "     m[:, 2]             — by number\n"
                    "\n"
                    "Incorrect:\n"
                    "     groupagg(m[:, \"Client\"], \"Amount\", sum)\n"
                    "\n"
                    "Correct:\n"
                    "     groupagg(m[:, \"Client\"], m[:, \"Amount\"], sum)"
                ),
                'variants': [
                    'r = groupagg(m[:, "Client"], m[:, "Amount"], sum)',
                    'r = groupagg(m[:, 1], m[:, 2], sum)',
                ],
            },
            'GROUPAGG_BAD_AGG': {
                'message': (
                    "groupagg: invalid aggregate.\n"
                    "  Allowed: sum, count, avg, min, max, "
                    "median, std, first, last."
                ),
                'wrong': 'groupagg(m[:, "Client"], m[:, "Amount"], average)',
                'right': 'groupagg(m[:, "Client"], m[:, "Amount"], avg)',
                'explanation': (
                    "Only these aggregates:\n"
                    "     sum      — sum\n"
                    "     count    — count\n"
                    "     avg      — average\n"
                    "     min, max — minimum, maximum\n"
                    "     median   — median\n"
                    "     std      — standard deviation\n"
                    "     first    — first value\n"
                    "     last     — last value\n"
                    "\n"
                    "Incorrect:\n"
                    "     groupagg(m[:, \"Client\"], m[:, \"Amount\"], average)\n"
                    "     groupagg(m[:, \"Client\"], m[:, \"Amount\"], mean)\n"
                    "\n"
                    "Correct:\n"
                    "     groupagg(m[:, \"Client\"], m[:, \"Amount\"], avg)"
                ),
                'variants': [
                    'r = groupagg(m[:, "Client"], m[:, "Amount"], sum)',
                    'r = groupagg(m[:, "Client"], m[:, "Amount"], avg)',
                    'r = groupagg(m[:, "Client"], m[:, "Amount"], count)',
                ],
            },
            'GROUPAGG_BAD_MODE': {
                'message': (
                    "groupagg: mode must be fill or exact."
                ),
                'wrong': 'groupagg(m[:, "Client"], m[:, "Amount"], sum, "TOTAL", all)',
                'right': 'groupagg(m[:, "Client"], m[:, "Amount"], sum, "TOTAL", fill)',
                'explanation': (
                    "Only two modes are allowed:\n"
                    "     fill  — empty values join the block (default)\n"
                    "     exact — each value is a separate block\n"
                    "\n"
                    "Incorrect:\n"
                    "     groupagg(..., all)\n"
                    "     groupagg(..., strict)\n"
                    "\n"
                    "Correct:\n"
                    "     groupagg(..., fill)\n"
                    "     groupagg(..., exact)"
                ),
                'variants': [
                    'r = groupagg(m[:, "Client"], m[:, "Amount"], sum, "TOTAL", fill)',
                    'r = groupagg(m[:, "Client"], m[:, "Amount"], sum, "TOTAL", exact)',
                ],
            },
            'GROUPAGG_DUCKDB': {
                'message': (
                    "groupagg works only with Matrix (RAM), "
                    "not with BigData (DuckDB).\n"
                    "  BigData is a read-only view on a file."
                ),
                'wrong': 'r = groupagg(bd[:, "Client"], bd[:, "Amount"], sum)',
                'right': (
                    'm = ToMatrix(bd)\n'
                    'r = groupagg(m[:, "Client"], m[:, "Amount"], sum)'
                ),
                'explanation': (
                    "BigData (DuckDB) is a read-only view on a file.\n"
                    "It does NOT support block aggregation.\n"
                    "\n"
                    "Solution:\n"
                    "  1. Convert BigData to Matrix:\n"
                    "        m = ToMatrix(bd)\n"
                    "        r = groupagg(m[:, \"Client\"], m[:, \"Amount\"], sum)\n"
                    "\n"
                    "  2. Use SQL analog:\n"
                    "        groupby, pivot"
                ),
                'variants': [
                    'm = ToMatrix(bd)\nr = groupagg(m[:, "Client"], m[:, "Amount"], sum)',
                    'm = ToMatrix(bd)\nr = groupagg(m[:, "Client"], m[:, "Amount"], sum, "TOTAL")',
                ],
            },
            'GROUPAGG_REQUIRES_ASSIGNMENT': {
                'message': (
                    "groupagg() returns a value — "
                    "the result must be saved."
                ),
                'wrong': 'groupagg(m[:, "Client"], m[:, "Amount"], sum)',
                'right': 'r = groupagg(m[:, "Client"], m[:, "Amount"], sum)',
                'explanation': (
                    "groupagg does NOT modify the source matrix.\n"
                    "It RETURNS a NEW one.\n"
                    "\n"
                    "Correct:\n"
                    "  r = groupagg(...)      — to a new variable\n"
                    "  m = groupagg(...)      — mutation"
                ),
                'variants': [
                    'r = groupagg(m[:, "Client"], m[:, "Amount"], sum)',
                    'm = groupagg(m[:, "Client"], m[:, "Amount"], sum)',
                ],
            },
        },
    },
}