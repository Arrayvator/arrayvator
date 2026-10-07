# syntax/autocomplete/items_groupby.py
"""
Описания функций группировки: groupby, groupagg, filldown.
"""

RU = {
    # ============================================================
    # GROUPBY
    # ============================================================
    'groupby': {
        'signature': 'groupby(by m[:, "X"], agg sum(m[:, "Y"]))',
        'description': (
            '📊 ГРУППИРОВКА (аналог SQL GROUP BY)\n'
            '\n'
            'ЗАЧЕМ НУЖНА:\n'
            '  • Свернуть много строк в одну сводку по группам.\n'
            '  • "Одна строка на каждый уникальный ключ".\n'
            '  • Классика: "сумма продаж по каждому товару".\n'
            '\n'
            'СИНТАКСИС:\n'
            '  groupby(by КЛЮЧ, agg АГРЕГАТ1, АГРЕГАТ2, ...)\n'
            '\n'
            'ГЛАВНОЕ ПРАВИЛО:\n'
            '  groupby группирует ПО ЗНАЧЕНИЮ, а не по порядку.\n'
            '  Сортировка исходных данных НЕ НУЖНА.\n'
            '  Работает и с хаотичными данными.\n'
            '\n'
            'КАКИЕ ЗАДАЧИ РЕШАЕТ:\n'
            '  • Сводная таблица: "зарплаты по отделам".\n'
            '  • Количество клиентов по городам.\n'
            '  • Максимальный чек по магазинам.\n'
            '  • Итоги по кварталам, категориям, менеджерам.\n'
            '\n'
            'ДОСТУПНЫЕ АГРЕГАТЫ:\n'
            '  sum, avg, count, min, max, median, first, last, std\n'
            '\n'
            '  • Работает с Matrix и DuckDB.\n'
            '  • Возвращает НОВУЮ сводную матрицу.'
        ),
        'example': (
            'r = groupby(by m[:, "Отдел"], agg sum(m[:, "Зарплата"]))\n'
            'r = groupby(by m[:, "Отдел"],\n'
            '            agg sum(m[:, "Зарплата"]), avg(m[:, "Зарплата"]), count())'
        ),
        'matrix_example': (
            '# ДАНО (хаотичный порядок отделов):\n'
            '#\n'
            '#   m = ["Отдел", "Сотрудник", "Зарплата";\n'
            '#        "HR",    "Егор",      65000;\n'
            '#        "IT",    "Боб",       95000;\n'
            '#        "Sales", "Катя",      80000;\n'
            '#        "HR",    "Жанна",     72000;\n'
            '#        "IT",    "Света",     70000]\n'
            '\n'
            '# ЗАДАЧА: сумма зарплат по каждому отделу\n'
            'r = groupby(by m[:, "Отдел"], agg sum(m[:, "Зарплата"]))\n'
            'print(r)\n'
            '\n'
            '# ВЫВОД:\n'
            '#\n'
            '#   Отдел  Сумма_Зарплата\n'
            '#   HR     137000\n'
            '#   IT     165000\n'
            '#   Sales  80000'
        ),
    },

    # ============================================================
    # GROUPAGG
    # ============================================================
    'groupagg': {
        'signature': 'groupagg(ключ-срез, значение-срез, agg [, имя] [, fill|exact])',
        'description': (
            '📦 БЛОЧНАЯ АГРЕГАЦИЯ ПО МАРКЕРУ\n'
            '\n'
            'ЗАЧЕМ НУЖНА:\n'
            '  • Итог ВСТАВЛЯЕТСЯ ВНУТРЬ таблицы, ПОСЛЕ каждого блока.\n'
            '  • Сохраняет структуру данных (детали + итог рядом).\n'
            '  • Классика: "по каждому клиенту — список заказов и ИТОГО".\n'
            '\n'
            'ГЛАВНОЕ ПРАВИЛО:\n'
            '  groupagg режет ПО ПОРЯДКУ строк, а не по значению!\n'
            '  Требует ПРЕДВАРИТЕЛЬНОЙ СОРТИРОВКИ.\n'
            '  Иначе получатся "рваные" блоки и неправильные итоги.\n'
            '\n'
            'ЧЕМ ОТЛИЧАЕТСЯ ОТ groupby:\n'
            '  groupby  — сжимает всё в одну строку на группу (сводка).\n'
            '  groupagg — оставляет детали и вставляет итог между блоками.\n'
            '\n'
            'РЕЖИМЫ:\n'
            '  fill  — пустые значения присоединяются к блоку (по умолчанию).\n'
            '  exact — каждое значение — отдельный блок.\n'
            '\n'
            'КАКИЕ ЗАДАЧИ РЕШАЕТ:\n'
            '  • Отчёт по клиентам: детали + ИТОГО.\n'
            '  • Печатная форма с подытогами.\n'
            '  • Детализация с блочными итогами.\n'
            '\n'
            '  ⚠️ Только Matrix (RAM). DuckDB не поддерживается.'
        ),
        'example': (
            'm_sorted = sort(m[:, "Отдел"], AZ)\n'
            'r = groupagg(m_sorted[:, "Отдел"], m_sorted[:, "Зарплата"], '
            'sum, "ИТОГО")'
        ),
        'matrix_example': (
            '# ДАНО (хаотично):\n'
            '#\n'
            '#   m = ["Отдел", "Сотрудник", "Зарплата";\n'
            '#        "IT", "Аня", 85000;\n'
            '#        "HR", "Егор", 65000;\n'
            '#        "IT", "Боб", 95000;\n'
            '#        "HR", "Жанна", 72000]\n'
            '\n'
            '# ШАГ 1: ОБЯЗАТЕЛЬНО сортируем по ключу\n'
            'm_sorted = sort(m[:, "Отдел"], AZ)\n'
            'print(m_sorted)\n'
            '#   Отдел  Сотрудник  Зарплата\n'
            '#   HR     Егор       65000\n'
            '#   HR     Жанна      72000\n'
            '#   IT     Аня        85000\n'
            '#   IT     Боб        95000\n'
            '\n'
            '# ШАГ 2: Блочная агрегация\n'
            'r = groupagg(m_sorted[:, "Отдел"], m_sorted[:, "Зарплата"],\n'
            '             sum, "ИТОГО")\n'
            'print(r)\n'
            '\n'
            '# ВЫВОД:\n'
            '#\n'
            '#   Отдел  Сотрудник  Зарплата\n'
            '#   HR     Егор       65000\n'
            '#   HR     Жанна      72000\n'
            '#   ИТОГО  None       137000   ← вставлен итог\n'
            '#   IT     Аня        85000\n'
            '#   IT     Боб        95000\n'
            '#   ИТОГО  None       180000   ← вставлен итог'
        ),
    },

    # ============================================================
    # FILLDOWN
    # ============================================================
    'filldown': {
        'signature': 'filldown(m[:, "X"] [, маркер])',
        'description': (
            '⬇️ ЗАПОЛНЕНИЕ ПУСТЫХ ЗНАЧЕНИЙ ВНИЗ\n'
            '\n'
            'ЗАЧЕМ НУЖНА:\n'
            '  • Заменить None или пустые строки предыдущим непустым.\n'
            '  • Классика: "развернуть" объединённые ячейки Excel.\n'
            '  • Устранить разрывы в группировках.\n'
            '\n'
            'КАК РАБОТАЕТ:\n'
            '  • Идёт по столбцу сверху вниз.\n'
            '  • Если значение пустое — берёт предыдущее непустое.\n'
            '  • Первая строка, если пустая — остаётся пустой.\n'
            '\n'
            'МАРКЕР ПУСТОТЫ:\n'
            '  • По умолчанию: None и пустая строка "" считаются пустыми.\n'
            '  • Можно указать свой маркер: "-", "N/A" и т.д.\n'
            '\n'
            'КАКИЕ ЗАДАЧИ РЕШАЕТ:\n'
            '  • Excel-стиль: объединённые ячейки → развернуть вниз.\n'
            '  • Разрывы в группировках: "восстановить группы".\n'
            '  • Заполнить пропуски в категориальных данных.\n'
            '\n'
            '  ⚠️ Только Matrix (RAM). DuckDB не поддерживается.\n'
            '  • Возвращает МАТРИЦУ с заполненным столбцом.'
        ),
        'example': (
            'r = filldown(m[:, "Клиент"])\n'
            'r = filldown(m[:, "Клиент"], "-")'
        ),
        'matrix_example': (
            '# ДАНО:\n'
            '#\n'
            '#   m = ["Клиент", "Товар";\n'
            '#        "Аня",    "Яблоки";\n'
            '#        "",       "Груши";\n'
            '#        "",       "Сливы";\n'
            '#        "Боб",    "Бананы";\n'
            '#        "",       "Апельсины"]\n'
            '\n'
            '# ЗАДАЧА: развернуть объединённые ячейки клиентов\n'
            'r = filldown(m[:, "Клиент"])\n'
            'print(r)\n'
            '\n'
            '# ВЫВОД:\n'
            '#\n'
            '#   Клиент  Товар\n'
            '#   Аня     Яблоки\n'
            '#   Аня     Груши       ← было ""\n'
            '#   Аня     Сливы       ← было ""\n'
            '#   Боб     Бананы\n'
            '#   Боб     Апельсины   ← было ""'
        ),
    },
}


EN = {
    'groupby': {
        'signature': 'groupby(by m[:, "X"], agg sum(m[:, "Y"]))',
        'description': (
            '📊 GROUPING (analog of SQL GROUP BY)\n'
            '\n'
            'WHY NEEDED:\n'
            '  • Collapse many rows into one summary per group.\n'
            '  • "One row per unique key".\n'
            '  • Classic: "total sales per product".\n'
            '\n'
            'SYNTAX:\n'
            '  groupby(by KEY, agg AGG1, AGG2, ...)\n'
            '\n'
            'MAIN RULE:\n'
            '  groupby groups BY VALUE, not by order.\n'
            '  Sorting of source data is NOT needed.\n'
            '  Works with chaotic data too.\n'
            '\n'
            'TASKS IT SOLVES:\n'
            '  • Pivot: "salaries by department".\n'
            '  • Client count by city.\n'
            '  • Max check per store.\n'
            '  • Totals by quarter, category, manager.\n'
            '\n'
            'AVAILABLE AGGREGATES:\n'
            '  sum, avg, count, min, max, median, first, last, std\n'
            '\n'
            '  • Works with Matrix and DuckDB.\n'
            '  • Returns a NEW summary matrix.'
        ),
        'example': (
            'r = groupby(by m[:, "Department"], agg sum(m[:, "Salary"]))\n'
            'r = groupby(by m[:, "Department"],\n'
            '            agg sum(m[:, "Salary"]), avg(m[:, "Salary"]), count())'
        ),
        'matrix_example': (
            '# INPUT (chaotic department order):\n'
            '#\n'
            '#   m = ["Dept", "Employee", "Salary";\n'
            '#        "HR",    "Greg",      65000;\n'
            '#        "IT",    "Bob",       95000;\n'
            '#        "Sales", "Kate",      80000;\n'
            '#        "HR",    "Jane",      72000;\n'
            '#        "IT",    "Eve",       70000]\n'
            '\n'
            'r = groupby(by m[:, "Dept"], agg sum(m[:, "Salary"]))\n'
            'print(r)\n'
            '\n'
            '# OUTPUT:\n'
            '#\n'
            '#   Dept   Sum_Salary\n'
            '#   HR     137000\n'
            '#   IT     165000\n'
            '#   Sales  80000'
        ),
    },

    'groupagg': {
        'signature': 'groupagg(key_slice, value_slice, agg [, name] [, fill|exact])',
        'description': (
            '📦 BLOCK AGGREGATION BY MARKER\n'
            '\n'
            'WHY NEEDED:\n'
            '  • Total is INSERTED INTO the table, AFTER each block.\n'
            '  • Preserves structure (details + total side by side).\n'
            '  • Classic: "per client — list of orders and TOTAL".\n'
            '\n'
            'MAIN RULE:\n'
            '  groupagg slices BY ROW ORDER, not by value!\n'
            '  Requires PRELIMINARY SORTING.\n'
            '  Otherwise you get "ragged" blocks and wrong totals.\n'
            '\n'
            'HOW IT DIFFERS FROM groupby:\n'
            '  groupby  — collapses all into one row per group.\n'
            '  groupagg — keeps details and inserts total between blocks.\n'
            '\n'
            'MODES:\n'
            '  fill  — empty values join the block (default).\n'
            '  exact — each value is a separate block.\n'
            '\n'
            'TASKS IT SOLVES:\n'
            '  • Client report: details + TOTAL.\n'
            '  • Printed form with subtotals.\n'
            '  • Detail with block totals.\n'
            '\n'
            '  ⚠️ Matrix only (RAM). DuckDB not supported.'
        ),
        'example': (
            'm_sorted = sort(m[:, "Department"], AZ)\n'
            'r = groupagg(m_sorted[:, "Department"], m_sorted[:, "Salary"], '
            'sum, "TOTAL")'
        ),
    },

    'filldown': {
        'signature': 'filldown(m[:, "X"] [, marker])',
        'description': (
            '⬇️ FILL EMPTY VALUES DOWNWARD\n'
            '\n'
            'WHY NEEDED:\n'
            '  • Replace None or empty strings with previous non-empty.\n'
            '  • Classic: "unfold" merged Excel cells.\n'
            '  • Fix gaps in groupings.\n'
            '\n'
            'HOW IT WORKS:\n'
            '  • Goes through the column top-down.\n'
            '  • If value is empty — takes previous non-empty.\n'
            '  • First row, if empty — stays empty.\n'
            '\n'
            'EMPTY MARKER:\n'
            '  • Default: None and empty string "" count as empty.\n'
            '  • You can specify your own: "-", "N/A", etc.\n'
            '\n'
            'TASKS IT SOLVES:\n'
            '  • Excel-style: merged cells → unfold downward.\n'
            '  • Fix groupings: "restore groups".\n'
            '  • Fill gaps in categorical data.\n'
            '\n'
            '  ⚠️ Matrix only (RAM). DuckDB not supported.\n'
            '  • Returns a MATRIX with filled column.'
        ),
        'example': (
            'r = filldown(m[:, "Client"])\n'
            'r = filldown(m[:, "Client"], "-")'
        ),
    },
}