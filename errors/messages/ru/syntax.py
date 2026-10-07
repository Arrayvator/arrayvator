# errors/messages/ru/syntax.py
"""
Ошибки синтаксиса из checker.py (SYNTAX_*).
"""

MESSAGES = {
    "SYNTAX_MISSING_COMMA_IN_INDEX":
        "Пропущена запятая между индексами.\n"
        "  После первого индекса ожидается ',' или ']'.",
    "SYNTAX_COLUMN_NEEDS_QUOTES":
        "Имя столбца в индексе пишется В КАВЫЧКАХ.",
    "SYNTAX_ROUND_BRACKETS":
        "Для индексов используются КВАДРАТНЫЕ скобки.",
    "SYNTAX_ASSIGN_IN_CONDITION":
        "В условии нужно СРАВНЕНИЕ (==), а не присваивание (=).",
    "SYNTAX_EXPRESSION_NOT_USED":
        "Выражение сравнения не используется.",
    "SYNTAX_AND_OPERATOR":
        "Логическое И — 'and', а не '&&'.",
    "SYNTAX_OR_OPERATOR":
        "Логическое ИЛИ — 'or', а не '||'.",
    "SYNTAX_NOT_OPERATOR":
        "Логическое НЕ — 'not', а не '!'.",
    "SYNTAX_NESTED_BRACKETS":
        "Матрица записывается через ';' (точку с запятой).",
    "SYNTAX_SORT_MISSING_DIRECTION":
        "Для сортировки нужно указать направление: AZ или ZA.",
    "SYNTAX_VLOOKUP_ROW_INSTEAD_OF_COLUMN":
        "vlookup работает только по СТОЛБЦАМ, не по строкам.",
    "SYNTAX_FUNCTION_NEEDS_ASSIGNMENT":
        "Функция возвращает результат — нужно присвоить переменной.",
    "SYNTAX_MISSING_THEN":
        "После условия if нужно ключевое слово then.",
    "SYNTAX_RESERVED_WORD":
        "Зарезервированное слово — нельзя использовать как имя переменной.",
    "SYNTAX_UNPIVOT_NO_BY":
        "unpivot требует параметр 'by'.\n"
        "  Пример: unpivot(m[:, 2:end], by m[:, \"Страна\"])",
    "SYNTAX_OPENCSV_BAD_MODE":
        "Режим OpenCSV должен быть BigData или Table.\n"
        "  Допустимо:\n"
        "     OpenCSV(\"file.csv\")               — авто\n"
        "     OpenCSV(\"file.csv\", BigData)      — DuckDB\n"
        "     OpenCSV(\"file.csv\", Table)        — RAM",

    # ============================================================
    # FOR — новый синтаксис
    # ============================================================
    "SYNTAX_FOR_OLD_SYNTAX":
        "Синтаксис for изменился.\n"
        "  Было: for i(1:10) { ... }\n"
        "  Стало: for i = 1 to 10 do { ... }",

    "SYNTAX_FOR_BAD_VAR":
        "for: после 'for' ожидается имя переменной.\n"
        "  Пример: for i = 1 to 10 do { ... }",

    "SYNTAX_FOR_NO_ASSIGN":
        "for: после переменной ожидается '='.\n"
        "  Пример: for i = 1 to 10 do { ... }",

    "SYNTAX_FOR_NO_TO":
        "for: ожидается ключевое слово 'to'.\n"
        "  Пример: for i = 1 to 10 do { ... }",

    "SYNTAX_FOR_NO_DO":
        "for: ожидается ключевое слово 'do'.\n"
        "  Пример: for i = 1 to 10 do { ... }",

    "SYNTAX_FOR_NO_STEP":
        "for: после 'step' ожидается число.\n"
        "  Пример: for i = 1 to 10 step 2 do { ... }",

    "SYNTAX_FOR_ZERO_STEP":
        "for: step не может быть 0.",

    "SYNTAX_FOR_IN_SYNTAX":
        "В for не используется 'in'.\n"
        "  Синтаксис: for i = 1 to 10 do { ... }",

    "SYNTAX_FOR_NO_PARENS":
        "Скобки в for больше не нужны.\n"
        "  Было: for i(1:10) { ... }\n"
        "  Стало: for i = 1 to 10 do { ... }",

    "SYNTAX_FOR_TO_SYNTAX":
        "В for не используется ':'.\n"
        "  Синтаксис: for i = 1 to 10 do { ... }",

    "SYNTAX_IF_NO_THEN":
        "После условия if нужно ключевое слово 'then'.",
    "SYNTAX_ANALYST_REMOVED":
        "Аналитик УБРАН. Используйте срез m[:, \"X\"].",
    "SYNTAX_INSERT_MISSING_DIRECTION":
        "insert требует направление (before / after).",
    "SYNTAX_COPY_MISSING_DIRECTION":
        "copy требует направление (before / after).",
    "SYNTAX_MOVE_MISSING_DIRECTION":
        "move требует направление (before / after).",
    "SYNTAX_PIVOT_MISSING_AGG":
        "pivot требует функцию агрегации (sum, avg, count, ...).",
    "SYNTAX_DATE_MISSING_FORMAT":
        "date требует ОБА формата: входной и выходной.",
    "SYNTAX_RANDOM_MISUSE":
        "random() нельзя использовать в print.",
    "SYNTAX_JOINARRAY_WITH_SLICE":
        "joinarray работает только с ЦЕЛЫМИ матрицами.",
    "SYNTAX_INSERTIF_MISSING_DIRECTION":
        "insertif требует before или after.\n"
        "  Формат: insertif(условие, before|after)",
    "SYNTAX_MATRIXMOD_MISSING_ACTION":
        "matrixmod требует действие.\n"
        "  Действия: delete, insert, duplicate, clear, keep, swap",
    "SYNTAX_FIND_MISSING_CONDITION":
        "find требует условие.\n"
        "  Формат: find(m[:, \"X\"] == \"Y\")",
    "SYNTAX_CHART_BAD_KIND":
        "chart: неверный тип графика.\n"
        "  Допустимо: bar, line, pie, hist, scatter, box, heatmap, pair.",
    "SYNTAX_REPORT_NOT_STARTED":
        "report: отчёт не начат.\n"
        "  Сначала вызовите report(\"Название\", \"file.html\")",
    "SYNTAX_ADDROWS_BAD_COUNT":
        "addrows: количество должно быть числом.\n"
        "  Пример: addrows(m, 5)",
    "SYNTAX_ADDROWS_NEGATIVE":
        "addrows: количество не может быть отрицательным.",
}