# errors/functions_db/groupby.py
"""
База ошибок для функции GROUPBY — аналог SQL GROUP BY.

СИНТАКСИС:
    groupby(by m[:, "Отдел"], agg sum(m[:, "Зарплата"]))
    groupby(by m[:, "Отдел"], m[:, "Год"],
            agg sum(m[:, "Продажи"]))
    groupby(by m[:, "Отдел"],
            agg sum(m[:, "Зарплата"]),
                avg(m[:, "Зарплата"]),
                count())
    groupby(by m[:, "Отдел"],
            agg sum(m[:, "Зарплата"]),
            having sum(m[:, "Зарплата"]) > 100000)

АГРЕГАТЫ:
    sum, avg, count, min, max, median, first, last, std

⚠️  Работает с Matrix (RAM) и DuckDB (BigData).
"""


RU = {
    'groupby': {
        'name': 'groupby',
        'category': 'groupby',
        'signature': (
            'groupby(by m[:, "X"], agg <агрегаты> '
            '[having <условие>])'
        ),
        'description': (
            'Группировка строк по ключам с вычислением агрегатов.\n'
            '  • Аналог SQL GROUP BY.\n'
            '  • Ключей может быть несколько (через запятую).\n'
            '  • Агрегатов может быть несколько.\n'
            '  • HAVING — фильтр групп по агрегату.\n'
            '  • Порядок групп — по первому появлению.\n'
            '  • Работает с Matrix и DuckDB.\n'
            '  • Возвращает НОВУЮ матрицу — результат нужно сохранить.'
        ),
        'examples': [
            'r = groupby(by m[:, "Отдел"], agg sum(m[:, "Зарплата"]))',
            'r = groupby(by m[:, "Отдел"], m[:, "Год"], agg sum(m[:, "Продажи"]))',
            'r = groupby(by m[:, "Отдел"], agg sum(m[:, "Зарплата"]), avg(m[:, "Зарплата"]), count())',
            'r = groupby(by m[:, "Отдел"], agg sum(m[:, "Зарплата"]), having sum(m[:, "Зарплата"]) > 100000)',
        ],
        'errors': {
            'GROUPBY_BAD_SYNTAX': {
                'message': (
                    "groupby: неверный синтаксис.\n"
                    "  Нужны ключи (by) и агрегаты (agg)."
                ),
                'wrong': 'groupby(m[:, "Отдел"], agg sum(m[:, "Зарплата"]))',
                'right': 'groupby(by m[:, "Отдел"], agg sum(m[:, "Зарплата"]))',
                'explanation': (
                    "groupby принимает обязательные ключевые слова:\n"
                    "  1. by  <ключи>       — по каким столбцам группировать\n"
                    "  2. agg <агрегаты>    — что считать\n"
                    "\n"
                    "Порядок ВАЖЕН: сначала by, потом agg.\n"
                    "\n"
                    "Структура:\n"
                    "  groupby(by m[:, \"X\"], agg sum(m[:, \"Y\"]))"
                ),
                'variants': [
                    'r = groupby(by m[:, "Отдел"], agg sum(m[:, "Зарплата"]))',
                    'r = groupby(by m[:, "Отдел"], m[:, "Год"], agg sum(m[:, "Продажи"]))',
                ],
            },
            'GROUPBY_NEED_BY': {
                'message': (
                    "groupby: пропущено ключевое слово 'by'.\n"
                    "  Без него непонятно, по каким столбцам группировать."
                ),
                'wrong': 'groupby(m[:, "Отдел"], agg sum(m[:, "Зарплата"]))',
                'right': 'groupby(by m[:, "Отдел"], agg sum(m[:, "Зарплата"]))',
                'explanation': (
                    "'by' — обязательный маркер начала блока ключей.\n"
                    "\n"
                    "Структура:\n"
                    "  groupby(by <ключи>, agg <агрегаты>)\n"
                    "          ^^^\n"
                    "          тут 'by'"
                ),
                'variants': [
                    'r = groupby(by m[:, "Отдел"], agg sum(m[:, "Зарплата"]))',
                    'r = groupby(by m[:, "Отдел"], m[:, "Год"], agg sum(m[:, "Продажи"]))',
                ],
            },
            'GROUPBY_NEED_AGG': {
                'message': (
                    "groupby: пропущено ключевое слово 'agg'.\n"
                    "  Без него непонятно, какие агрегаты считать."
                ),
                'wrong': 'groupby(by m[:, "Отдел"], sum(m[:, "Зарплата"]))',
                'right': 'groupby(by m[:, "Отдел"], agg sum(m[:, "Зарплата"]))',
                'explanation': (
                    "'agg' — обязательный маркер начала блока агрегатов.\n"
                    "\n"
                    "Структура:\n"
                    "  groupby(by <ключи>, agg <агрегаты>)\n"
                    "                    ^^^\n"
                    "                    тут 'agg'"
                ),
                'variants': [
                    'r = groupby(by m[:, "Отдел"], agg sum(m[:, "Зарплата"]))',
                    'r = groupby(by m[:, "Отдел"], agg sum(m[:, "Зарплата"]), avg(m[:, "Зарплата"]))',
                ],
            },
            'GROUPBY_BAD_AGG_NAME': {
                'message': (
                    "groupby: неверная агрегатная функция.\n"
                    "  Допустимо: sum, avg, count, min, max,\n"
                    "             median, first, last, std."
                ),
                'wrong': 'groupby(by m[:, "Отдел"], agg average(m[:, "Зарплата"]))',
                'right': 'groupby(by m[:, "Отдел"], agg avg(m[:, "Зарплата"]))',
                'explanation': (
                    "В groupby используются ТОЛЬКО эти агрегаты:\n"
                    "     sum(m[:, \"X\"])     — сумма\n"
                    "     avg(m[:, \"X\"])     — среднее\n"
                    "     count()             — количество строк\n"
                    "     count(m[:, \"X\"])   — количество непустых\n"
                    "     min(m[:, \"X\"])     — минимум\n"
                    "     max(m[:, \"X\"])     — максимум\n"
                    "     median(m[:, \"X\"])  — медиана\n"
                    "     first(m[:, \"X\"])   — первое значение\n"
                    "     last(m[:, \"X\"])    — последнее значение\n"
                    "     std(m[:, \"X\"])     — стандартное отклонение\n"
                    "\n"
                    "НЕ путать:\n"
                    "     'average'  ❌ → 'avg'  ✅\n"
                    "     'mean'     ❌ → 'avg'  ✅\n"
                    "     'cnt'      ❌ → 'count' ✅"
                ),
                'variants': [
                    'r = groupby(by m[:, "Отдел"], agg sum(m[:, "Зарплата"]))',
                    'r = groupby(by m[:, "Отдел"], agg avg(m[:, "Зарплата"]))',
                    'r = groupby(by m[:, "Отдел"], agg count())',
                    'r = groupby(by m[:, "Отдел"], agg median(m[:, "Зарплата"]))',
                ],
            },
            'GROUPBY_BAD_KEY_SLICE': {
                'message': (
                    "groupby: ключ должен быть срезом m[:, \"X\"].\n"
                    "  Нельзя передать имя строкой или число."
                ),
                'wrong': 'groupby(by "Отдел", agg sum(m[:, "Зарплата"]))',
                'right': 'groupby(by m[:, "Отдел"], agg sum(m[:, "Зарплата"]))',
                'explanation': (
                    "Ключ — это СРЕЗ столбца, а не его имя.\n"
                    "\n"
                    "Неправильно:\n"
                    "     by \"Отдел\"\n"
                    "     by 3\n"
                    "     by column \"Отдел\"\n"
                    "\n"
                    "Правильно:\n"
                    "     by m[:, \"Отдел\"]\n"
                    "     by m[:, 3]\n"
                    "     by m[:, end]"
                ),
                'variants': [
                    'r = groupby(by m[:, "Отдел"], agg sum(m[:, "Зарплата"]))',
                    'r = groupby(by m[:, 3], agg sum(m[:, 5]))',
                ],
            },
            'GROUPBY_BAD_VALUE_SLICE': {
                'message': (
                    "groupby: агрегат должен работать со срезом m[:, \"X\"].\n"
                    "  Пример: sum(m[:, \"Зарплата\"])."
                ),
                'wrong': 'groupby(by m[:, "Отдел"], agg sum("Зарплата"))',
                'right': 'groupby(by m[:, "Отдел"], agg sum(m[:, "Зарплата"]))',
                'explanation': (
                    "Агрегат принимает СРЕЗ, а не имя строкой.\n"
                    "\n"
                    "Неправильно:\n"
                    "     sum(\"Зарплата\")\n"
                    "     sum(3)\n"
                    "\n"
                    "Правильно:\n"
                    "     sum(m[:, \"Зарплата\"])\n"
                    "     sum(m[:, 5])"
                ),
                'variants': [
                    'r = groupby(by m[:, "Отдел"], agg sum(m[:, "Зарплата"]))',
                    'r = groupby(by m[:, "Отдел"], agg avg(m[:, 5]))',
                ],
            },
            'GROUPBY_DIFFERENT_TABLES': {
                'message': (
                    "groupby: все срезы должны быть из ОДНОЙ таблицы.\n"
                    "  Проверьте by, agg, having."
                ),
                'wrong': (
                    'groupby(by m1[:, "Отдел"], '
                    'agg sum(m2[:, "Зарплата"]))'
                ),
                'right': (
                    'groupby(by m1[:, "Отдел"], '
                    'agg sum(m1[:, "Зарплата"]))'
                ),
                'explanation': (
                    "Срезы из разных таблиц бессмысленны — они не связаны\n"
                    "между собой по строкам.\n"
                    "\n"
                    "Неправильно:\n"
                    "     by m1[:, \"Отдел\"], agg sum(m2[:, \"X\"])\n"
                    "\n"
                    "Правильно:\n"
                    "     by m[:, \"Отдел\"], agg sum(m[:, \"X\"])"
                ),
                'variants': [
                    'r = groupby(by m[:, "Отдел"], agg sum(m[:, "Зарплата"]))',
                ],
            },
            'GROUPBY_HAVING_BAD': {
                'message': (
                    "groupby: в having нужно условие с агрегатом.\n"
                    "  Пример: having sum(m[:, \"X\"]) > 100."
                ),
                'wrong': 'groupby(by m[:, "Отдел"], agg sum(m[:, "Зарплата"]), having m[:, "Отдел"] == "IT")',
                'right': 'groupby(by m[:, "Отдел"], agg sum(m[:, "Зарплата"]), having sum(m[:, "Зарплата"]) > 100000)',
                'explanation': (
                    "HAVING фильтрует ГРУППЫ по агрегату.\n"
                    "Внутри having должен быть агрегат + оператор сравнения.\n"
                    "\n"
                    "Неправильно:\n"
                    "     having m[:, \"Отдел\"] == \"IT\"      — это WHERE\n"
                    "\n"
                    "Правильно:\n"
                    "     having sum(m[:, \"X\"]) > 100\n"
                    "     having avg(m[:, \"X\"]) <= 50\n"
                    "     having count() >= 5"
                ),
                'variants': [
                    'r = groupby(by m[:, "Отдел"], agg sum(m[:, "Зарплата"]), having sum(m[:, "Зарплата"]) > 100000)',
                    'r = groupby(by m[:, "Отдел"], agg count(), having count() >= 5)',
                ],
            },
            'GROUPBY_HAVING_NO_AGG': {
                'message': (
                    "groupby: внутри having ожидается агрегатная функция.\n"
                    "  Пример: having sum(m[:, \"X\"]) > 100."
                ),
                'wrong': 'groupby(by m[:, "Отдел"], agg sum(m[:, "Зарплата"]), having m[:, "Зарплата"] > 50000)',
                'right': 'groupby(by m[:, "Отдел"], agg sum(m[:, "Зарплата"]), having sum(m[:, "Зарплата"]) > 100000)',
                'explanation': (
                    "HAVING работает с УЖЕ ПОСЧИТАННЫМИ агрегатами.\n"
                    "Внутри having должен быть один из:\n"
                    "     sum(...), avg(...), count(), min(...), max(...),\n"
                    "     median(...), first(...), last(...), std(...)\n"
                    "\n"
                    "Сначала пересчитайте агрегат:\n"
                    "     having sum(m[:, \"Зарплата\"]) > 100000"
                ),
                'variants': [
                    'r = groupby(by m[:, "Отдел"], agg sum(m[:, "Зарплата"]), having sum(m[:, "Зарплата"]) > 100000)',
                    'r = groupby(by m[:, "Отдел"], agg avg(m[:, "Зарплата"]), having avg(m[:, "Зарплата"]) > 50000)',
                ],
            },
            'GROUPBY_REQUIRES_ASSIGNMENT': {
                'message': (
                    "groupby() возвращает значение — "
                    "результат нужно сохранить."
                ),
                'wrong': 'groupby(by m[:, "Отдел"], agg sum(m[:, "Зарплата"]))',
                'right': 'r = groupby(by m[:, "Отдел"], agg sum(m[:, "Зарплата"]))',
                'explanation': (
                    "groupby НЕ изменяет исходную матрицу.\n"
                    "Он ВОЗВРАЩАЕТ НОВУЮ.\n"
                    "\n"
                    "Правильно:\n"
                    "  r = groupby(...)      — в новую переменную\n"
                    "  m = groupby(...)      — мутация\n"
                    "  print(groupby(...))   — вывод"
                ),
                'variants': [
                    'r = groupby(by m[:, "Отдел"], agg sum(m[:, "Зарплата"]))',
                    'm = groupby(by m[:, "Отдел"], agg sum(m[:, "Зарплата"]))',
                    'print(groupby(by m[:, "Отдел"], agg sum(m[:, "Зарплата"])))',
                ],
            },
        },
    },
}


EN = {
    'groupby': {
        'name': 'groupby',
        'category': 'groupby',
        'signature': (
            'groupby(by m[:, "X"], agg <aggregates> '
            '[having <condition>])'
        ),
        'description': (
            'Group rows by keys and compute aggregates.\n'
            '  • Analog of SQL GROUP BY.\n'
            '  • Multiple keys allowed (comma-separated).\n'
            '  • Multiple aggregates allowed.\n'
            '  • HAVING — filter groups by aggregate.\n'
            '  • Group order — by first appearance.\n'
            '  • Works with Matrix and DuckDB.\n'
            '  • Returns a NEW matrix — save the result.'
        ),
        'examples': [
            'r = groupby(by m[:, "Department"], agg sum(m[:, "Salary"]))',
            'r = groupby(by m[:, "Department"], m[:, "Year"], agg sum(m[:, "Sales"]))',
            'r = groupby(by m[:, "Department"], agg sum(m[:, "Salary"]), avg(m[:, "Salary"]), count())',
            'r = groupby(by m[:, "Department"], agg sum(m[:, "Salary"]), having sum(m[:, "Salary"]) > 100000)',
        ],
        'errors': {
            'GROUPBY_BAD_SYNTAX': {
                'message': (
                    "groupby: invalid syntax.\n"
                    "  Need keys (by) and aggregates (agg)."
                ),
                'wrong': 'groupby(m[:, "Department"], agg sum(m[:, "Salary"]))',
                'right': 'groupby(by m[:, "Department"], agg sum(m[:, "Salary"]))',
                'explanation': (
                    "groupby takes required keywords:\n"
                    "  1. by  <keys>         — which columns to group by\n"
                    "  2. agg <aggregates>   — what to compute\n"
                    "\n"
                    "Order MATTERS: by first, then agg.\n"
                    "\n"
                    "Structure:\n"
                    "  groupby(by m[:, \"X\"], agg sum(m[:, \"Y\"]))"
                ),
                'variants': [
                    'r = groupby(by m[:, "Department"], agg sum(m[:, "Salary"]))',
                    'r = groupby(by m[:, "Department"], m[:, "Year"], agg sum(m[:, "Sales"]))',
                ],
            },
            'GROUPBY_NEED_BY': {
                'message': (
                    "groupby: keyword 'by' is missing.\n"
                    "  Without it, it's unclear which columns to group by."
                ),
                'wrong': 'groupby(m[:, "Department"], agg sum(m[:, "Salary"]))',
                'right': 'groupby(by m[:, "Department"], agg sum(m[:, "Salary"]))',
                'explanation': (
                    "'by' is a required marker for the keys block.\n"
                    "\n"
                    "Structure:\n"
                    "  groupby(by <keys>, agg <aggregates>)\n"
                    "          ^^^\n"
                    "          here 'by'"
                ),
                'variants': [
                    'r = groupby(by m[:, "Department"], agg sum(m[:, "Salary"]))',
                    'r = groupby(by m[:, "Department"], m[:, "Year"], agg sum(m[:, "Sales"]))',
                ],
            },
            'GROUPBY_NEED_AGG': {
                'message': (
                    "groupby: keyword 'agg' is missing.\n"
                    "  Without it, it's unclear which aggregates to compute."
                ),
                'wrong': 'groupby(by m[:, "Department"], sum(m[:, "Salary"]))',
                'right': 'groupby(by m[:, "Department"], agg sum(m[:, "Salary"]))',
                'explanation': (
                    "'agg' is a required marker for the aggregates block.\n"
                    "\n"
                    "Structure:\n"
                    "  groupby(by <keys>, agg <aggregates>)\n"
                    "                    ^^^\n"
                    "                    here 'agg'"
                ),
                'variants': [
                    'r = groupby(by m[:, "Department"], agg sum(m[:, "Salary"]))',
                    'r = groupby(by m[:, "Department"], agg sum(m[:, "Salary"]), avg(m[:, "Salary"]))',
                ],
            },
            'GROUPBY_BAD_AGG_NAME': {
                'message': (
                    "groupby: invalid aggregate function.\n"
                    "  Allowed: sum, avg, count, min, max,\n"
                    "          median, first, last, std."
                ),
                'wrong': 'groupby(by m[:, "Department"], agg average(m[:, "Salary"]))',
                'right': 'groupby(by m[:, "Department"], agg avg(m[:, "Salary"]))',
                'explanation': (
                    "Only these aggregates work in groupby:\n"
                    "     sum(m[:, \"X\"])     — sum\n"
                    "     avg(m[:, \"X\"])     — average\n"
                    "     count()             — row count\n"
                    "     count(m[:, \"X\"])   — non-empty count\n"
                    "     min(m[:, \"X\"])     — minimum\n"
                    "     max(m[:, \"X\"])     — maximum\n"
                    "     median(m[:, \"X\"])  — median\n"
                    "     first(m[:, \"X\"])   — first value\n"
                    "     last(m[:, \"X\"])    — last value\n"
                    "     std(m[:, \"X\"])     — standard deviation\n"
                    "\n"
                    "Don't confuse:\n"
                    "     'average'  ❌ → 'avg'  ✅\n"
                    "     'mean'     ❌ → 'avg'  ✅\n"
                    "     'cnt'      ❌ → 'count' ✅"
                ),
                'variants': [
                    'r = groupby(by m[:, "Department"], agg sum(m[:, "Salary"]))',
                    'r = groupby(by m[:, "Department"], agg avg(m[:, "Salary"]))',
                    'r = groupby(by m[:, "Department"], agg count())',
                    'r = groupby(by m[:, "Department"], agg median(m[:, "Salary"]))',
                ],
            },
            'GROUPBY_BAD_KEY_SLICE': {
                'message': (
                    "groupby: key must be a slice m[:, \"X\"].\n"
                    "  Cannot pass a string name or a number."
                ),
                'wrong': 'groupby(by "Department", agg sum(m[:, "Salary"]))',
                'right': 'groupby(by m[:, "Department"], agg sum(m[:, "Salary"]))',
                'explanation': (
                    "A key is a SLICE of a column, not its name.\n"
                    "\n"
                    "Incorrect:\n"
                    "     by \"Department\"\n"
                    "     by 3\n"
                    "     by column \"Department\"\n"
                    "\n"
                    "Correct:\n"
                    "     by m[:, \"Department\"]\n"
                    "     by m[:, 3]\n"
                    "     by m[:, end]"
                ),
                'variants': [
                    'r = groupby(by m[:, "Department"], agg sum(m[:, "Salary"]))',
                    'r = groupby(by m[:, 3], agg sum(m[:, 5]))',
                ],
            },
            'GROUPBY_BAD_VALUE_SLICE': {
                'message': (
                    "groupby: aggregate must work with a slice m[:, \"X\"].\n"
                    "  Example: sum(m[:, \"Salary\"])."
                ),
                'wrong': 'groupby(by m[:, "Department"], agg sum("Salary"))',
                'right': 'groupby(by m[:, "Department"], agg sum(m[:, "Salary"]))',
                'explanation': (
                    "The aggregate takes a SLICE, not a string name.\n"
                    "\n"
                    "Incorrect:\n"
                    "     sum(\"Salary\")\n"
                    "     sum(3)\n"
                    "\n"
                    "Correct:\n"
                    "     sum(m[:, \"Salary\"])\n"
                    "     sum(m[:, 5])"
                ),
                'variants': [
                    'r = groupby(by m[:, "Department"], agg sum(m[:, "Salary"]))',
                    'r = groupby(by m[:, "Department"], agg avg(m[:, 5]))',
                ],
            },
            'GROUPBY_DIFFERENT_TABLES': {
                'message': (
                    "groupby: all slices must come from the SAME table.\n"
                    "  Check by, agg, having."
                ),
                'wrong': (
                    'groupby(by m1[:, "Department"], '
                    'agg sum(m2[:, "Salary"]))'
                ),
                'right': (
                    'groupby(by m1[:, "Department"], '
                    'agg sum(m1[:, "Salary"]))'
                ),
                'explanation': (
                    "Slices from different tables are meaningless —\n"
                    "they aren't linked by rows.\n"
                    "\n"
                    "Incorrect:\n"
                    "     by m1[:, \"Department\"], agg sum(m2[:, \"X\"])\n"
                    "\n"
                    "Correct:\n"
                    "     by m[:, \"Department\"], agg sum(m[:, \"X\"])"
                ),
                'variants': [
                    'r = groupby(by m[:, "Department"], agg sum(m[:, "Salary"]))',
                ],
            },
            'GROUPBY_HAVING_BAD': {
                'message': (
                    "groupby: having needs an aggregate condition.\n"
                    "  Example: having sum(m[:, \"X\"]) > 100."
                ),
                'wrong': 'groupby(by m[:, "Department"], agg sum(m[:, "Salary"]), having m[:, "Department"] == "IT")',
                'right': 'groupby(by m[:, "Department"], agg sum(m[:, "Salary"]), having sum(m[:, "Salary"]) > 100000)',
                'explanation': (
                    "HAVING filters GROUPS by aggregate.\n"
                    "Inside having there must be an aggregate + comparison operator.\n"
                    "\n"
                    "Incorrect:\n"
                    "     having m[:, \"Department\"] == \"IT\"      — this is WHERE\n"
                    "\n"
                    "Correct:\n"
                    "     having sum(m[:, \"X\"]) > 100\n"
                    "     having avg(m[:, \"X\"]) <= 50\n"
                    "     having count() >= 5"
                ),
                'variants': [
                    'r = groupby(by m[:, "Department"], agg sum(m[:, "Salary"]), having sum(m[:, "Salary"]) > 100000)',
                    'r = groupby(by m[:, "Department"], agg count(), having count() >= 5)',
                ],
            },
            'GROUPBY_HAVING_NO_AGG': {
                'message': (
                    "groupby: inside having an aggregate is expected.\n"
                    "  Example: having sum(m[:, \"X\"]) > 100."
                ),
                'wrong': 'groupby(by m[:, "Department"], agg sum(m[:, "Salary"]), having m[:, "Salary"] > 50000)',
                'right': 'groupby(by m[:, "Department"], agg sum(m[:, "Salary"]), having sum(m[:, "Salary"]) > 100000)',
                'explanation': (
                    "HAVING works with ALREADY COMPUTED aggregates.\n"
                    "Inside having one of these must be used:\n"
                    "     sum(...), avg(...), count(), min(...), max(...),\n"
                    "     median(...), first(...), last(...), std(...)\n"
                    "\n"
                    "Recompute the aggregate first:\n"
                    "     having sum(m[:, \"Salary\"]) > 100000"
                ),
                'variants': [
                    'r = groupby(by m[:, "Department"], agg sum(m[:, "Salary"]), having sum(m[:, "Salary"]) > 100000)',
                    'r = groupby(by m[:, "Department"], agg avg(m[:, "Salary"]), having avg(m[:, "Salary"]) > 50000)',
                ],
            },
            'GROUPBY_REQUIRES_ASSIGNMENT': {
                'message': (
                    "groupby() returns a value — "
                    "the result must be saved."
                ),
                'wrong': 'groupby(by m[:, "Department"], agg sum(m[:, "Salary"]))',
                'right': 'r = groupby(by m[:, "Department"], agg sum(m[:, "Salary"]))',
                'explanation': (
                    "groupby does NOT modify the source matrix.\n"
                    "It RETURNS a NEW one.\n"
                    "\n"
                    "Correct:\n"
                    "  r = groupby(...)      — to a new variable\n"
                    "  m = groupby(...)      — mutation\n"
                    "  print(groupby(...))   — output"
                ),
                'variants': [
                    'r = groupby(by m[:, "Department"], agg sum(m[:, "Salary"]))',
                    'm = groupby(by m[:, "Department"], agg sum(m[:, "Salary"]))',
                    'print(groupby(by m[:, "Department"], agg sum(m[:, "Salary"])))',
                ],
            },
        },
    },
}