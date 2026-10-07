# errors/messages/en/common.py
"""
Common errors: brackets, quotes, operators, indexing.
"""

MESSAGES = {
    # ============================================================
    # SYNTAX: BRACKETS
    # ============================================================
    "MISSING_RPAREN": "Missing closing parenthesis ')'.",
    "MISSING_LPAREN": "Missing opening parenthesis '('.",
    "MISSING_RBRACKET": "Missing closing square bracket ']'.",
    "MISSING_LBRACKET": "Missing opening square bracket '['.",
    "MISSING_RBRACE": "Missing closing curly brace '}'.",
    "MISSING_LBRACE": "Missing opening curly brace '{'.",
    "EXTRA_RPAREN": "Extra closing parenthesis ')'.",
    "EXTRA_RBRACKET": "Extra closing square bracket ']'.",
    "EXTRA_RBRACE": "Extra closing curly brace '}'.",
    "NESTED_BRACKETS":
        "Nested square brackets '[' inside a matrix are not allowed.\n"
        "  ArrayVator does not use Python syntax [[...], [...]].\n"
        "  Use semicolon ';' as a row separator for matrices.",

    # ============================================================
    # INDEXING
    # ============================================================
    "EMPTY_INDEX":
        "Index cannot be empty.\n"
        "  Inside square brackets, there must be a VALUE or TWO VALUES separated by comma.",
    "EMPTY_INDEX_FIRST":
        "First index value is missing.\n"
        "  Before the comma there must be a VALUE.",
    "EMPTY_INDEX_SECOND":
        "Second index value is missing.\n"
        "  After the comma there must be a VALUE.",

    "SEMICOLON_IN_INDEX":
        "Inside [...] a ';' is used — this is WRONG.\n"
        "  ';' is a ROW separator in matrices, not in indices.",

    "SEMICOLON_INSTEAD_OF_COMMA":
        "A ';' (row separator) is used, but a COMMA ',' is needed.\n"
        "  ';' is only used INSIDE [...] for matrices.",

    # ============================================================
    # QUOTES
    # ============================================================
    "UNCLOSED_STRING":
        "String is not closed. Missing closing quote.\n"
        "  Perhaps you accidentally typed an extra quote.",
    "UNCLOSED_STRING_DOUBLE":
        "String is not closed. Missing closing double quote '\"'.",
    "UNCLOSED_STRING_SINGLE":
        "String is not closed. Missing closing single quote \"'.",

    # ============================================================
    # OPERATORS
    # ============================================================
    "ASSIGN_IN_CONDITION":
        "In condition, '=' (assignment) is used instead of '==' (comparison).\n"
        "  '=' — assigns a value.\n"
        "  '==' — compares values.",
    "EQ_IN_STATEMENT":
        "In statement, '==' (comparison) is used instead of '=' (assignment).\n"
        "  '==' — compares values.\n"
        "  '=' — assigns a value.",
    "EXPRESSION_NOT_USED":
        "Comparison expression is not used.\n"
        "  The result of the comparison is not saved anywhere.",
    "UNEXPECTED_ASSIGN": "Unexpected '='.",
    "MISSING_THEN": "After 'if' condition, keyword 'then' is expected.",
    "MISSING_COLON": "Expected colon ':'.",
    "MISSING_COMMA": "Missing comma between function arguments.\n"
                     "  After the first argument, ',' is expected.",
    "MISSING_CATCH": "After try { ... }, catch { ... } is expected.",

    # ============================================================
    # BLOCKS
    # ============================================================
    "MISSING_BLOCK":
        "After condition, a code block in curly braces '{ ... }' is expected.",

    # ============================================================
    # GENERAL
    # ============================================================
    "UNEXPECTED_EOF": "Unexpected end of file.",
    "UNEXPECTED_TOKEN": "Unexpected token.",
    "UNKNOWN_SYMBOL": "Unknown symbol. Perhaps a typo or extra character.",
    "UNDEFINED_VARIABLE": "Variable is not defined.",
    "UNDEFINED_COLUMN": "Column not found.",

    # ============================================================
    # RANDOM
    # ============================================================
    "RANDOM_MISUSE":
        "random() cannot be used here — only in assignment.",

    # ============================================================
    # TYPES
    # ============================================================
    "TYPE_ERROR": "Type error.",
    "INDEX_OUT_OF_RANGE": "Index out of range.",
    "EMPTY_MATRIX_RANDOM":
        "Cannot fill empty matrix/vector with random numbers.",

    # ============================================================
    # ERROR HANDLING
    # ============================================================
    "ERROR_RESERVED":
        "The name 'error' is reserved.\n"
        "  It is used for error handling.",
    "TRY_BAD_SYNTAX":
        "Invalid try/catch syntax.\n"
        "  Format: try { ... } catch { ... }\n"
        "  Or:     try { ... } catch (e) { ... }",

    # ============================================================
    # EXTENDED SYNTAX
    # ============================================================
    "EXPECTED_EXPRESSION":
        "Expected an expression (number, string, variable or function).",
    "EXPECTED_IDENTIFIER": "Expected a variable name.",
    "EXPECTED_OPERATOR": "Expected an operator (+, -, *, / etc.).",
    "EXPECTED_COLUMN_OR_ROW": "Expected 'column' or 'row'.",
    "EXPECTED_AFTER_COLUMN":
        "After 'column', expected a column name or number.",
    "EXPECTED_AFTER_ROW":
        "After 'row', expected a row number or value.",
    "EXPECTED_BEFORE_OR_AFTER": "Expected 'before' or 'after'.",
    "EXPECTED_AZ_OR_ZA":
        "Sort direction: AZ (ascending) or ZA (descending).",
    "EXPECTED_LBRACE": "Expected opening curly brace '{'.",
    "EXPECTED_RBRACE": "Expected closing curly brace '}'.",
    "EXPECTED_THEN": "Expected keyword 'then' after the condition.",
    "EXPECTED_DO": "Expected keyword 'do'.",
    "EXPECTED_ASSIGN": "Expected '=' (assignment).",
    "EXPECTED_LPAREN": "Expected opening parenthesis '('.",
    "EXPECTED_RPAREN": "Expected closing parenthesis ')'.",
    "EXPECTED_LBRACKET": "Expected opening square bracket '['.",
    "EXPECTED_RBRACKET": "Expected closing square bracket ']'.",

    # ============================================================
    # CONTEXT ERRORS
    # ============================================================
    "FOR_MISSING_LPAREN":
        "After 'for' an opening parenthesis '(' is expected.\n"
        "  Syntax: for i(start:end) { ... }",
    "WHILE_BAD_SYNTAX":
        "Syntax: while condition { ... }",
    "FUNCTION_MISSING_LPAREN":
        "After a function name, '(' is expected.",

    "FORGOT_PAREN_OPEN": "Missing opening parenthesis '('.",
    "FORGOT_PAREN_CLOSE": "Missing closing parenthesis ')'.",
    "FORGOT_BRACKET_OPEN": "Missing opening square bracket '['.",
    "FORGOT_BRACKET_CLOSE": "Missing closing square bracket ']'.",
    "FORGOT_BRACE_OPEN": "Missing opening curly brace '{'.",
    "FORGOT_BRACE_CLOSE": "Missing closing curly brace '}'.",

    # ============================================================
    # FUNCTIONS — general
    # ============================================================
    "WRONG_ARG_COUNT": "Wrong number of function arguments.",
    "UNKNOWN_FUNCTION": "Unknown function.",
    "WRONG_ARG_TYPE": "Wrong argument type for function.",
    "FUNCTION_REQUIRES_ASSIGNMENT":
        "Function returns a value — the result must be saved.\n"
        "  It does NOT modify the source matrix automatically.\n"
        "  Direct call without assignment is an error.",

    # ============================================================
    # MATRICES
    # ============================================================
    "NOT_A_MATRIX": "Object is not a matrix.",
    "NOT_2D_MATRIX": "Object is not a 2D matrix.",
    "EMPTY_MATRIX": "Matrix is empty.",
    "INDEX_MISMATCH": "Matrix size mismatch.",

    # ============================================================
    # EXECUTION
    # ============================================================
    "DIVISION_BY_ZERO": "Division by zero.",
    "NAME_ERROR": "Name not found.",
    "VALUE_ERROR": "Invalid value.",
    "RUNTIME_ERROR": "Runtime error.",

    # ============================================================
    # SORT
    # ============================================================
    "SORT_BAD_FIRST_ARG":
        "sort works only with a slice m[:, \"X\"] or a vector.\n"
        "  Examples:\n"
        "     Правильно: sort(m[:, \"Name\"], AZ)\n"
        "     Правильно: sort(m[:, 3], ZA)\n"
        "     Правильно: sort(v, AZ)              ← vector\n"
        "\n"
        "  Неправильно: sort(m, AZ)   ← whole matrix without a column",

    "SORT_BAD_DIRECTION":
        "Sort direction must be AZ or ZA.\n"
        "  Examples:\n"
        "     Правильно: sort(m[:, \"Name\"], AZ)   — ascending\n"
        "     Правильно: sort(m[:, \"Name\"], ZA)   — descending\n"
        "\n"
        "  Неправильно: sort(m[:, \"Name\"], UP)\n"
        "  Неправильно: sort(m[:, \"Name\"], DOWN)\n"
        "  Неправильно: sort(m[:, \"Name\"])       ← no direction",

    "SORT_BAD_SLICE":
        "sort: invalid slice.\n"
        "  Examples:\n"
        "     Правильно: sort(m[:, \"Name\"], AZ)\n"
        "     Правильно: sort(m[:, 3], ZA)\n"
        "     Правильно: sort(m[10:end, \"Name\"], AZ)",
}