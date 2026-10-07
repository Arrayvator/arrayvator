# syntax/autocomplete/special_words.py
"""
Специальные слова (RU + EN).

Используются для справки и автодополнения.

ВАЖНО:
    Слово 'null' НЕ используется в языке — только None.
    Литерал 'nan' тоже НЕ используется.
    Оба ловятся лексером как ошибка:
        BANNED_NULL_LITERAL
        BANNED_NAN_LITERAL

    Регистр НЕ важен: None, none, NONE — всё одно и то же.
"""

RU = {
    # ============================================================
    # УПРАВЛЯЮЩИЕ КОНСТРУКЦИИ
    # ============================================================
    'if': {
        'signature': 'if условие then { ... } [else { ... }]',
        'description': (
            'Условная конструкция.\n'
            '  • Блок в фигурных скобках.\n'
            '  • else — опционально.\n'
            '  • elif НЕТ — используйте вложенные if.'
        ),
        'example': (
            'if x > 5 then { print("больше") }\n'
            'if x > 5 then { ... } else { ... }'
        ),
    },
    'while': {
        'signature': 'while условие { ... }',
        'description': (
            'Цикл с условием.\n'
            '  • Выполняется, пока условие истинно.\n'
            '  • Внутри должен быть код, меняющий условие.'
        ),
        'example': (
            'i = 1\n'
            'while i <= 5 {\n'
            '    print(i)\n'
            '    i = i + 1\n'
            '}'
        ),
    },
    'for': {
        'signature': 'for переменная = начало to конец [step S] do { ... }',
        'description': (
            'Цикл по диапазону.\n'
            '  • Оба конца включительно.\n'
            '  • Если начало > конца — идём вниз.\n'
            '  • step — опционально (по умолчанию 1).'
        ),
        'example': (
            'for i = 1 to 5 do { print(i) }        # 1 2 3 4 5\n'
            'for i = 5 to 1 do { print(i) }        # 5 4 3 2 1\n'
            'for i = 1 to 10 step 2 do { print(i) }'
        ),
    },

    # ============================================================
    # ИНДЕКСАЦИЯ
    # ============================================================
    'end': {
        'signature': 'm[end, :] / m[:, end]',
        'description': 'Последняя строка/столбец.',
        'example': (
            'm[end, :]         # последняя строка\n'
            'm[:, end]         # последний столбец\n'
            'm[end-1, :]       # предпоследняя строка\n'
            'm[end+1, :] = X   # расширение строки'
        ),
    },
    'last': {
        'signature': 'm[last N, :] / m[:, last N]',
        'description': 'Последние N строк/столбцов.',
        'example': (
            'm[last 3, :]      # последние 3 строки\n'
            'm[:, last 2]      # последние 2 столбца'
        ),
    },
    'all': {
        'signature': 'm[all, :] / m[:, all]',
        'description': 'Все строки/столбцы. Синоним ":"',
        'example': (
            'm[all, 1]         # весь столбец 1\n'
            'm[1, all]         # вся строка 1\n'
            'm[all, all]       # вся матрица'
        ),
    },
    'begin': {
        'signature': 'm[begin, :] / m[:, begin]',
        'description': 'Первая строка/столбец.',
        'example': 'm[begin, :]',
    },

    # ============================================================
    # НАПРАВЛЕНИЯ / МОДИФИКАТОРЫ
    # ============================================================
    'AZ': {
        'signature': 'sort(m[:, "X"], AZ)',
        'description': 'Направление сортировки: по возрастанию.',
        'example': 'r = sort(m[:, "Имя"], AZ)',
    },
    'ZA': {
        'signature': 'sort(m[:, "X"], ZA)',
        'description': 'Направление сортировки: по убыванию.',
        'example': 'r = sort(m[:, "Имя"], ZA)',
    },
    'before': {
        'signature': 'insert(..., before)',
        'description': 'Направление: ПЕРЕД целью.',
        'example': 'r = insert(m[2, :], before)',
    },
    'after': {
        'signature': 'insert(..., after)',
        'description': 'Направление: ПОСЛЕ цели.',
        'example': 'r = insert(m[2, :], after)',
    },
    'inside': {
        'signature': 'find(m[:, "X"] == "Y", inside)',
        'description': 'Поиск подстроки.',
        'example': 'r = find(m[:, "Имя"] == "ов", inside)',
    },
    'ignore': {
        'signature': 'find(..., ignore)',
        'description': 'Без учёта регистра.',
        'example': 'r = find(m[:, "Имя"] == "аня", ignore)',
    },
    'vertical': {
        'signature': 'joinarray(m1, m2, vertical)',
        'description': 'Объединение: строки вниз.',
        'example': 'r = joinarray(a, b, vertical)',
    },
    'horizontal': {
        'signature': 'joinarray(m1, m2, horizontal)',
        'description': 'Объединение: столбцы вправо.',
        'example': 'r = joinarray(a, b, horizontal)',
    },
    'approx': {
        'signature': 'vlookup(..., approx) / anomaly(..., approx)',
        'description': (
            'Приблизительный поиск (vlookup) '
            'или приблизительные процентили (anomaly, DuckDB).'
        ),
        'example': (
            'r = vlookup(82, grades, "Категория", approx)\n'
            'r = anomaly(m[:, "Сумма"], by m[:, "Магазин"], approx)'
        ),
    },
    'skip': {
        'signature': 'split(текст, ",", skip)',
        'description': 'Пропускать пустые элементы.',
        'example': 'r = split("a,,b", ",", skip)',
    },

    # ============================================================
    # АНАЛИТИКА: ОПЦИИ
    # ============================================================
    'coef': {
        'signature': 'abc(..., coef) / percentof(..., coef)',
        'description': 'Коэффициент (0.0–1.0) вместо процентов (0–100).',
        'example': (
            'r = abc(m[:, "Продажи"], coef)\n'
            'r = percentof(m[:, "Продажи"], coef)'
        ),
    },
    '%': {
        'signature': 'abc(..., %)',
        'description': 'Проценты (0–100) в отдельном столбце.',
        'example': (
            'r = abc(m[:, "Продажи"], %)\n'
            'r = abc(m[:, "Продажи"], %, m[:, end+1])'
        ),
    },
    'iqr': {
        'signature': 'anomaly(..., iqr [, k])',
        'description': (
            'Межквартильный размах.\n'
            '  • k = 1.5 — по умолчанию.\n'
            '  • k = 3.0 — только сильные выбросы.'
        ),
        'example': (
            'r = anomaly(m[:, "Сумма"], iqr)\n'
            'r = anomaly(m[:, "Сумма"], iqr, 3.0)'
        ),
    },
    'zscore': {
        'signature': 'anomaly(..., zscore [, N])',
        'description': (
            'Z-отклонение.\n'
            '  • N = 3 — по умолчанию.\n'
            '  • N = 2 — мягче.'
        ),
        'example': (
            'r = anomaly(m[:, "Сумма"], zscore)\n'
            'r = anomaly(m[:, "Сумма"], zscore, 2)'
        ),
    },
    'percentile': {
        'signature': 'anomaly(..., percentile [, lo, hi])',
        'description': (
            'Процентили.\n'
            '  • lo = 1, hi = 99 — по умолчанию.'
        ),
        'example': (
            'r = anomaly(m[:, "Сумма"], percentile)\n'
            'r = anomaly(m[:, "Сумма"], percentile, 5, 95)'
        ),
    },
    'only': {
        'signature': 'anomaly(..., only)',
        'description': 'Только аномальные строки.',
        'example': 'r = anomaly(m[:, "Сумма"], only)',
    },

    # ============================================================
    # CASE
    # ============================================================
    'when': {
        'signature': 'case(..., when УСЛОВИЕ then "X", ...)',
        'description': 'Условие в case.',
        'example': 'r = case(m[:, "X"], when < 18 then "Дитя", else "Взрослый")',
    },
    'then': {
        'signature': 'when ... then "X"',
        'description': 'Результат в case или блок if.',
        'example': 'when < 18 then "Дитя"',
    },
    'else': {
        'signature': 'else "X"',
        'description': 'Иначе в case или if.',
        'example': 'else "Взрослый"',
    },

    # ============================================================
    # ЗНАЧЕНИЯ
    # ============================================================
    'true': {
        'signature': 'true',
        'description': 'Логическое значение ИСТИНА.',
        'example': 'x = true',
    },
    'false': {
        'signature': 'false',
        'description': 'Логическое значение ЛОЖЬ.',
        'example': 'x = false',
    },
    'None': {
        'signature': 'None',
        'description': (
            'Пустое значение (аналог null / NULL в других языках).\n'
            '  • Регистр не важен: None, none, NONE.\n'
            '  • Проверяется функцией isnone().\n'
            '  • Заменяется функцией fillna().\n'
            '  • Удаляется функцией dropna().\n'
            '  • Первое не-None берётся через coalesce().\n'
            '\n'
            '⚠️  Слова null и nan НЕ используются — только None.'
        ),
        'example': (
            'x = None\n'
            'r = isnone(None)         # True\n'
            'm = [1, None, 3]\n'
            'm = fillna(m, 0)         # None → 0\n'
            'r = coalesce(None, 5)    # 5'
        ),
    },

    # ============================================================
    # GROUPBY
    # ============================================================
    'by': {
        'signature': 'groupby(by m[:, "X"], agg sum(m[:, "Y"]))',
        'description': (
            'Ключ группировки в groupby.\n'
            'Также используется в percentof, anomaly, unpivot, '
            'sumif/avgif/countif/minif/maxif.'
        ),
        'example': (
            'r = groupby(by m[:, "Отдел"], agg sum(m[:, "Зарплата"]))\n'
            'r = percentof(m[:, "Продажи"], by m[:, "Категория"])\n'
            'r = sumif(by m[:, "Отдел"], m[:, "Зарплата"])'
        ),
    },
    'agg': {
        'signature': 'groupby(by ..., agg sum(...), avg(...), count())',
        'description': (
            'Агрегаты в groupby.\n'
            'Допустимо: sum, avg, count, min, max, median, first, last, std.'
        ),
        'example': (
            'r = groupby(by m[:, "Отдел"], agg sum(m[:, "Зарплата"]))'
        ),
    },
    'having': {
        'signature': 'groupby(..., having sum(...) > 100)',
        'description': 'Фильтр групп в groupby.',
        'example': (
            'r = groupby(by m[:, "Отдел"],\n'
            '            agg sum(m[:, "Зарплата"]),\n'
            '            having sum(m[:, "Зарплата"]) > 100000)'
        ),
    },

    # ============================================================
    # РЕЖИМЫ
    # ============================================================
    'BigData': {
        'signature': 'OpenCSV("file.csv", BigData)',
        'description': (
            'Режим открытия CSV: DuckDB (BigData).\n'
            'Данные на диске, RAM ~50 МБ.'
        ),
        'example': 'm = OpenCSV("big.csv", BigData)',
    },
    'Table': {
        'signature': 'OpenCSV("file.csv", Table)',
        'description': 'Режим открытия CSV: MatrExMatrix (RAM).',
        'example': 'm = OpenCSV("small.csv", Table)',
    },

    # ============================================================
    # ГРАФИКИ: ТИПЫ
    # ============================================================
    'bar': {'signature': 'chart(bar, x, y)', 'description': 'Столбчатая.',
            'example': 'chart(bar, m[:, "Отдел"], m[:, "Зарплата"])'},
    'line': {'signature': 'chart(line, x, y)', 'description': 'Линейная.',
             'example': 'chart(line, m[:, "Месяц"], m[:, "Продажи"])'},
    'pie': {'signature': 'chart(pie, x, y)', 'description': 'Круговая.',
            'example': 'chart(pie, m[:, "Отдел"], m[:, "Доля"])'},
    'hist': {'signature': 'chart(hist, x, bins N)', 'description': 'Гистограмма.',
             'example': 'chart(hist, m[:, "Возраст"], bins 10)'},
    'scatter': {'signature': 'chart(scatter, x, y)', 'description': 'Точечная.',
                'example': 'chart(scatter, m[:, "X"], m[:, "Y"])'},
    'box': {'signature': 'chart(box, x, y)', 'description': 'Ящик с усами.',
            'example': 'chart(box, m[:, "Отдел"], m[:, "Зарплата"])'},
    'heatmap': {'signature': 'chart(heatmap, matrix)', 'description': 'Тепловая карта.',
                'example': 'chart(heatmap, m[:, 2:end])'},
    'pair': {'signature': 'chart(pair, matrix)', 'description': 'Парные зависимости.',
             'example': 'chart(pair, m[:, 2:end])'},

    # ============================================================
    # ГРАФИКИ: ОПЦИИ
    # ============================================================
    'title': {'signature': 'title "..."', 'description': 'Заголовок.',
              'example': 'chart(bar, x, y, title "Мой график")'},
    'xlabel': {'signature': 'xlabel "..."', 'description': 'Подпись X.',
               'example': 'chart(bar, x, y, xlabel "Отдел")'},
    'ylabel': {'signature': 'ylabel "..."', 'description': 'Подпись Y.',
               'example': 'chart(bar, x, y, ylabel "Зарплата")'},
    'color': {'signature': 'color "red"', 'description': 'Цвет.',
              'example': 'chart(bar, x, y, color "red")'},
    'save': {'signature': 'save "file.png"', 'description': 'Сохранить в файл.',
             'example': 'chart(bar, x, y, save "chart.png")'},
    'bins': {'signature': 'bins N', 'description': 'Корзин (hist).',
             'example': 'chart(hist, x, bins 10)'},
    'plotly': {'signature': 'plotly', 'description': 'Интерактивный Plotly.',
               'example': 'chart(line, x, y, plotly)'},
    'static': {'signature': 'static', 'description': 'Matplotlib.',
               'example': 'chart(bar, x, y, static)'},

    # ============================================================
    # ОШИБКИ
    # ============================================================
    'try': {
        'signature': 'try { ... } catch { ... }',
        'description': 'Защищённый блок.',
        'example': (
            'try {\n'
            '    m = OpenCSV("missing.csv")\n'
            '}\n'
            'catch {\n'
            '    print("Ошибка:", error)\n'
            '    m = ["A"; 0]\n'
            '}'
        ),
    },
    'catch': {
        'signature': 'catch [(var)] { ... }',
        'description': 'Обработчик ошибок.',
        'example': 'catch (e) { print("Поймано:", e) }',
    },
    'error': {
        'signature': 'error',
        'description': 'Текст последней ошибки (только чтение).',
        'example': (
            'm = OpenCSV("missing.csv")\n'
            'if error then { print("Ошибка:", error) }'
        ),
    },

    # ============================================================
    # ОКНА: ORDER
    # ============================================================
    'order': {
        'signature': 'order m[:, "X"]',
        'description': 'Порядок в оконной функции.',
        'example': 'rownumber(m, by m[:, "Отдел"], order m[:, "Зарплата"], ZA)',
    },
}


EN = {
    # ============================================================
    # CONTROL FLOW
    # ============================================================
    'if': {
        'signature': 'if condition then { ... } [else { ... }]',
        'description': (
            'Conditional statement.\n'
            '  • Block in curly braces.\n'
            '  • else — optional.\n'
            '  • elif — NOT supported, use nested if.'
        ),
        'example': (
            'if x > 5 then { print("greater") }\n'
            'if x > 5 then { ... } else { ... }'
        ),
    },
    'while': {
        'signature': 'while condition { ... }',
        'description': (
            'Loop with condition.\n'
            '  • Runs while condition is true.\n'
            '  • There must be code that changes the condition.'
        ),
        'example': (
            'i = 1\n'
            'while i <= 5 {\n'
            '    print(i)\n'
            '    i = i + 1\n'
            '}'
        ),
    },
    'for': {
        'signature': 'for var = start to end [step S] do { ... }',
        'description': (
            'Loop over a range.\n'
            '  • Both ends inclusive.\n'
            '  • If start > end — goes down.\n'
            '  • step — optional (default 1).'
        ),
        'example': (
            'for i = 1 to 5 do { print(i) }        # 1 2 3 4 5\n'
            'for i = 5 to 1 do { print(i) }        # 5 4 3 2 1\n'
            'for i = 1 to 10 step 2 do { print(i) }'
        ),
    },

    # ============================================================
    # INDEXING
    # ============================================================
    'end': {
        'signature': 'm[end, :] / m[:, end]',
        'description': 'Last row/column.',
        'example': (
            'm[end, :]         # last row\n'
            'm[:, end]         # last column\n'
            'm[end-1, :]       # second-to-last\n'
            'm[end+1, :] = X   # extend rows'
        ),
    },
    'last': {
        'signature': 'm[last N, :] / m[:, last N]',
        'description': 'Last N rows/columns.',
        'example': (
            'm[last 3, :]      # last 3 rows\n'
            'm[:, last 2]      # last 2 columns'
        ),
    },
    'all': {
        'signature': 'm[all, :] / m[:, all]',
        'description': 'All rows/columns. Synonym of ":"',
        'example': (
            'm[all, 1]         # column 1\n'
            'm[1, all]         # row 1\n'
            'm[all, all]       # whole matrix'
        ),
    },
    'begin': {
        'signature': 'm[begin, :] / m[:, begin]',
        'description': 'First row/column.',
        'example': 'm[begin, :]',
    },

    # ============================================================
    # DIRECTIONS / MODIFIERS
    # ============================================================
    'AZ': {
        'signature': 'sort(m[:, "X"], AZ)',
        'description': 'Sort: ascending.',
        'example': 'r = sort(m[:, "Name"], AZ)',
    },
    'ZA': {
        'signature': 'sort(m[:, "X"], ZA)',
        'description': 'Sort: descending.',
        'example': 'r = sort(m[:, "Name"], ZA)',
    },
    'before': {
        'signature': 'insert(..., before)',
        'description': 'BEFORE target.',
        'example': 'r = insert(m[2, :], before)',
    },
    'after': {
        'signature': 'insert(..., after)',
        'description': 'AFTER target.',
        'example': 'r = insert(m[2, :], after)',
    },
    'inside': {
        'signature': 'find(m[:, "X"] == "Y", inside)',
        'description': 'Substring search.',
        'example': 'r = find(m[:, "Name"] == "ov", inside)',
    },
    'ignore': {
        'signature': 'find(..., ignore)',
        'description': 'Case-insensitive.',
        'example': 'r = find(m[:, "Name"] == "ann", ignore)',
    },
    'vertical': {
        'signature': 'joinarray(m1, m2, vertical)',
        'description': 'Rows downward.',
        'example': 'r = joinarray(a, b, vertical)',
    },
    'horizontal': {
        'signature': 'joinarray(m1, m2, horizontal)',
        'description': 'Columns rightward.',
        'example': 'r = joinarray(a, b, horizontal)',
    },
    'approx': {
        'signature': 'vlookup(..., approx) / anomaly(..., approx)',
        'description': (
            'Approximate search (vlookup) or approximate percentiles '
            '(anomaly, DuckDB).'
        ),
        'example': (
            'r = vlookup(82, grades, "Category", approx)\n'
            'r = anomaly(m[:, "Amount"], by m[:, "Store"], approx)'
        ),
    },
    'skip': {
        'signature': 'split(text, ",", skip)',
        'description': 'Skip empty elements.',
        'example': 'r = split("a,,b", ",", skip)',
    },

    # ============================================================
    # ANALYTICS: OPTIONS
    # ============================================================
    'coef': {
        'signature': 'abc(..., coef) / percentof(..., coef)',
        'description': 'Ratio (0.0–1.0) instead of percent.',
        'example': (
            'r = abc(m[:, "Sales"], coef)\n'
            'r = percentof(m[:, "Sales"], coef)'
        ),
    },
    '%': {
        'signature': 'abc(..., %)',
        'description': 'Percent (0–100) into a separate column.',
        'example': (
            'r = abc(m[:, "Sales"], %)\n'
            'r = abc(m[:, "Sales"], %, m[:, end+1])'
        ),
    },
    'iqr': {
        'signature': 'anomaly(..., iqr [, k])',
        'description': (
            'Interquartile range.\n'
            '  • k = 1.5 — default.\n'
            '  • k = 3.0 — strong outliers only.'
        ),
        'example': (
            'r = anomaly(m[:, "Amount"], iqr)\n'
            'r = anomaly(m[:, "Amount"], iqr, 3.0)'
        ),
    },
    'zscore': {
        'signature': 'anomaly(..., zscore [, N])',
        'description': (
            'Z-score.\n'
            '  • N = 3 — default.\n'
            '  • N = 2 — softer.'
        ),
        'example': (
            'r = anomaly(m[:, "Amount"], zscore)\n'
            'r = anomaly(m[:, "Amount"], zscore, 2)'
        ),
    },
    'percentile': {
        'signature': 'anomaly(..., percentile [, lo, hi])',
        'description': (
            'Percentiles.\n'
            '  • lo = 1, hi = 99 — default.'
        ),
        'example': (
            'r = anomaly(m[:, "Amount"], percentile)\n'
            'r = anomaly(m[:, "Amount"], percentile, 5, 95)'
        ),
    },
    'only': {
        'signature': 'anomaly(..., only)',
        'description': 'Only anomalous rows.',
        'example': 'r = anomaly(m[:, "Amount"], only)',
    },

    # ============================================================
    # CASE
    # ============================================================
    'when': {
        'signature': 'case(..., when COND then "X", ...)',
        'description': 'Condition in case.',
        'example': 'r = case(m[:, "Age"], when < 18 then "Child", else "Adult")',
    },
    'then': {
        'signature': 'when ... then "X"',
        'description': 'Result in case or if block.',
        'example': 'when < 18 then "Child"',
    },
    'else': {
        'signature': 'else "X"',
        'description': 'Otherwise in case or if.',
        'example': 'else "Adult"',
    },

    # ============================================================
    # VALUES
    # ============================================================
    'true': {'signature': 'true', 'description': 'Boolean TRUE.', 'example': 'x = true'},
    'false': {'signature': 'false', 'description': 'Boolean FALSE.', 'example': 'x = false'},
    'None': {
        'signature': 'None',
        'description': (
            'Empty value (analog of null / NULL in other languages).\n'
            '  • Case-insensitive: None, none, NONE.\n'
            '  • Tested by isnone().\n'
            '  • Replaced by fillna().\n'
            '  • Removed by dropna().\n'
            '  • First non-None is taken by coalesce().\n'
            '\n'
            '⚠️  Literals null and nan are NOT used — only None.'
        ),
        'example': (
            'x = None\n'
            'r = isnone(None)         # True\n'
            'm = [1, None, 3]\n'
            'm = fillna(m, 0)         # None → 0\n'
            'r = coalesce(None, 5)    # 5'
        ),
    },

    # ============================================================
    # GROUPBY
    # ============================================================
    'by': {
        'signature': 'groupby(by m[:, "X"], agg sum(m[:, "Y"]))',
        'description': (
            'Grouping key in groupby.\n'
            'Also used in percentof, anomaly, unpivot, '
            'sumif/avgif/countif/minif/maxif.'
        ),
        'example': (
            'r = groupby(by m[:, "Dept"], agg sum(m[:, "Salary"]))\n'
            'r = percentof(m[:, "Sales"], by m[:, "Category"])\n'
            'r = sumif(by m[:, "Dept"], m[:, "Salary"])'
        ),
    },
    'agg': {
        'signature': 'groupby(by ..., agg sum(...), avg(...), count())',
        'description': 'Aggregates in groupby.',
        'example': 'r = groupby(by m[:, "Dept"], agg sum(m[:, "Salary"]))',
    },
    'having': {
        'signature': 'groupby(..., having sum(...) > 100)',
        'description': 'Filter groups in groupby.',
        'example': (
            'r = groupby(by m[:, "Dept"],\n'
            '            agg sum(m[:, "Salary"]),\n'
            '            having sum(m[:, "Salary"]) > 100000)'
        ),
    },

    # ============================================================
    # MODES
    # ============================================================
    'BigData': {
        'signature': 'OpenCSV("file.csv", BigData)',
        'description': 'CSV open mode: DuckDB (BigData).',
        'example': 'm = OpenCSV("big.csv", BigData)',
    },
    'Table': {
        'signature': 'OpenCSV("file.csv", Table)',
        'description': 'CSV open mode: Matrix (RAM).',
        'example': 'm = OpenCSV("small.csv", Table)',
    },

    # ============================================================
    # CHARTS: KINDS
    # ============================================================
    'bar': {'signature': 'chart(bar, x, y)', 'description': 'Bar chart.',
            'example': 'chart(bar, m[:, "Dept"], m[:, "Salary"])'},
    'line': {'signature': 'chart(line, x, y)', 'description': 'Line chart.',
             'example': 'chart(line, m[:, "Month"], m[:, "Sales"])'},
    'pie': {'signature': 'chart(pie, x, y)', 'description': 'Pie chart.',
            'example': 'chart(pie, m[:, "Dept"], m[:, "Share"])'},
    'hist': {'signature': 'chart(hist, x, bins N)', 'description': 'Histogram.',
             'example': 'chart(hist, m[:, "Age"], bins 10)'},
    'scatter': {'signature': 'chart(scatter, x, y)', 'description': 'Scatter plot.',
                'example': 'chart(scatter, m[:, "X"], m[:, "Y"])'},
    'box': {'signature': 'chart(box, x, y)', 'description': 'Box plot.',
            'example': 'chart(box, m[:, "Dept"], m[:, "Salary"])'},
    'heatmap': {'signature': 'chart(heatmap, matrix)', 'description': 'Heat map.',
                'example': 'chart(heatmap, m[:, 2:end])'},
    'pair': {'signature': 'chart(pair, matrix)', 'description': 'Pair plot.',
             'example': 'chart(pair, m[:, 2:end])'},

    # ============================================================
    # CHARTS: OPTIONS
    # ============================================================
    'title': {'signature': 'title "..."', 'description': 'Title.',
              'example': 'chart(bar, x, y, title "My chart")'},
    'xlabel': {'signature': 'xlabel "..."', 'description': 'X label.',
               'example': 'chart(bar, x, y, xlabel "Dept")'},
    'ylabel': {'signature': 'ylabel "..."', 'description': 'Y label.',
               'example': 'chart(bar, x, y, ylabel "Salary")'},
    'color': {'signature': 'color "red"', 'description': 'Color.',
              'example': 'chart(bar, x, y, color "red")'},
    'save': {'signature': 'save "file.png"', 'description': 'Save to file.',
             'example': 'chart(bar, x, y, save "chart.png")'},
    'bins': {'signature': 'bins N', 'description': 'Bins (hist).',
             'example': 'chart(hist, x, bins 10)'},
    'plotly': {'signature': 'plotly', 'description': 'Interactive Plotly.',
               'example': 'chart(line, x, y, plotly)'},
    'static': {'signature': 'static', 'description': 'Matplotlib.',
               'example': 'chart(bar, x, y, static)'},

    # ============================================================
    # ERRORS
    # ============================================================
    'try': {
        'signature': 'try { ... } catch { ... }',
        'description': 'Protected block.',
        'example': (
            'try {\n'
            '    m = OpenCSV("missing.csv")\n'
            '}\n'
            'catch {\n'
            '    print("Error:", error)\n'
            '    m = ["A"; 0]\n'
            '}'
        ),
    },
    'catch': {
        'signature': 'catch [(var)] { ... }',
        'description': 'Error handler.',
        'example': 'catch (e) { print("Caught:", e) }',
    },
    'error': {
        'signature': 'error',
        'description': 'Text of the last error (read-only).',
        'example': (
            'm = OpenCSV("missing.csv")\n'
            'if error then { print("Error:", error) }'
        ),
    },

    # ============================================================
    # WINDOW: ORDER
    # ============================================================
    'order': {
        'signature': 'order m[:, "X"]',
        'description': 'Sort order in window function.',
        'example': 'rownumber(m, by m[:, "Dept"], order m[:, "Salary"], ZA)',
    },
}