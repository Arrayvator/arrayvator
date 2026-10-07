# errors/messages/en/syntax.py
"""
Syntax errors from checker.py (SYNTAX_*).
"""

MESSAGES = {
    "SYNTAX_MISSING_COMMA_IN_INDEX":
        "Missing comma between indices.\n"
        "  After the first index, ',' or ']' is expected.",
    "SYNTAX_COLUMN_NEEDS_QUOTES":
        "Column name in index must be in QUOTES.",
    "SYNTAX_ROUND_BRACKETS":
        "Use SQUARE brackets for indices.",
    "SYNTAX_ASSIGN_IN_CONDITION":
        "In condition, use COMPARISON (==), not assignment (=).",
    "SYNTAX_EXPRESSION_NOT_USED":
        "Comparison expression is not used.",
    "SYNTAX_AND_OPERATOR":
        "Logical AND is 'and', not '&&'.",
    "SYNTAX_OR_OPERATOR":
        "Logical OR is 'or', not '||'.",
    "SYNTAX_NOT_OPERATOR":
        "Logical NOT is 'not', not '!'.",
    "SYNTAX_NESTED_BRACKETS":
        "Matrix is written with ';' (semicolon).",
    "SYNTAX_SORT_MISSING_DIRECTION":
        "Sort needs direction: AZ or ZA.",
    "SYNTAX_VLOOKUP_ROW_INSTEAD_OF_COLUMN":
        "vlookup works only by COLUMNS, not by rows.",
    "SYNTAX_FUNCTION_NEEDS_ASSIGNMENT":
        "Function returns result — must be assigned to a variable.",
    "SYNTAX_MISSING_THEN":
        "After if condition, keyword 'then' is needed.",
    "SYNTAX_RESERVED_WORD":
        "Reserved word — cannot be used as a variable name.",
    "SYNTAX_UNPIVOT_NO_BY":
        "unpivot requires 'by' parameter.\n"
        "  Example: unpivot(m[:, 2:end], by m[:, \"Country\"])",
    "SYNTAX_OPENCSV_BAD_MODE":
        "OpenCSV mode must be BigData or Table.\n"
        "  Allowed:\n"
        "     OpenCSV(\"file.csv\")               — auto\n"
        "     OpenCSV(\"file.csv\", BigData)      — DuckDB\n"
        "     OpenCSV(\"file.csv\", Table)        — RAM",

    # ============================================================
    # FOR — new syntax
    # ============================================================
    "SYNTAX_FOR_OLD_SYNTAX":
        "The 'for' syntax has changed.\n"
        "  Was: for i(1:10) { ... }\n"
        "  Now: for i = 1 to 10 do { ... }",

    "SYNTAX_FOR_BAD_VAR":
        "for: variable name expected after 'for'.\n"
        "  Example: for i = 1 to 10 do { ... }",

    "SYNTAX_FOR_NO_ASSIGN":
        "for: '=' expected after the variable.\n"
        "  Example: for i = 1 to 10 do { ... }",

    "SYNTAX_FOR_NO_TO":
        "for: keyword 'to' expected.\n"
        "  Example: for i = 1 to 10 do { ... }",

    "SYNTAX_FOR_NO_DO":
        "for: keyword 'do' expected.\n"
        "  Example: for i = 1 to 10 do { ... }",

    "SYNTAX_FOR_NO_STEP":
        "for: number expected after 'step'.\n"
        "  Example: for i = 1 to 10 step 2 do { ... }",

    "SYNTAX_FOR_ZERO_STEP":
        "for: step cannot be 0.",

    "SYNTAX_FOR_IN_SYNTAX":
        "'in' is not used in for.\n"
        "  Syntax: for i = 1 to 10 do { ... }",

    "SYNTAX_FOR_NO_PARENS":
        "Parentheses in for are no longer needed.\n"
        "  Was: for i(1:10) { ... }\n"
        "  Now: for i = 1 to 10 do { ... }",

    "SYNTAX_FOR_TO_SYNTAX":
        "':' is not used in for.\n"
        "  Syntax: for i = 1 to 10 do { ... }",

    "SYNTAX_IF_NO_THEN":
        "After if condition, keyword 'then' is needed.",
    "SYNTAX_ANALYST_REMOVED":
        "Analyst mode REMOVED. Use slice m[:, \"X\"].",
    "SYNTAX_INSERT_MISSING_DIRECTION":
        "insert requires direction (before / after).",
    "SYNTAX_COPY_MISSING_DIRECTION":
        "copy requires direction (before / after).",
    "SYNTAX_MOVE_MISSING_DIRECTION":
        "move requires direction (before / after).",
    "SYNTAX_PIVOT_MISSING_AGG":
        "pivot requires aggregation function (sum, avg, count, ...).",
    "SYNTAX_DATE_MISSING_FORMAT":
        "date requires BOTH formats: input and output.",
    "SYNTAX_RANDOM_MISUSE":
        "random() cannot be used in print.",
    "SYNTAX_JOINARRAY_WITH_SLICE":
        "joinarray works only with WHOLE matrices.",
    "SYNTAX_INSERTIF_MISSING_DIRECTION":
        "insertif requires before or after.\n"
        "  Format: insertif(condition, before|after)",
    "SYNTAX_MATRIXMOD_MISSING_ACTION":
        "matrixmod requires action.\n"
        "  Actions: delete, insert, duplicate, clear, keep, swap",
    "SYNTAX_FIND_MISSING_CONDITION":
        "find requires condition.\n"
        "  Format: find(m[:, \"X\"] == \"Y\")",
    "SYNTAX_CHART_BAD_KIND":
        "chart: invalid chart type.\n"
        "  Allowed: bar, line, pie, hist, scatter, box, heatmap, pair.",
    "SYNTAX_REPORT_NOT_STARTED":
        "report: report not started.\n"
        "  First call report(\"Title\", \"file.html\")",
    "SYNTAX_ADDROWS_BAD_COUNT":
        "addrows: count must be a number.\n"
        "  Example: addrows(m, 5)",
    "SYNTAX_ADDROWS_NEGATIVE":
        "addrows: count cannot be negative.",
}