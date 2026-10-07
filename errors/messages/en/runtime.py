# errors/messages/en/runtime.py
"""
Runtime errors (RUNTIME_*).
"""

MESSAGES = {
    "RUNTIME_NOT_MATRIX":
        "Matrix expected.\n"
        "  Example: matrixmod(m, delete, 2)",
    "RUNTIME_NOT_VECTOR":
        "Vector expected.\n"
        "  Vector is one row or column of values.",
    "RUNTIME_MATRIX_ONLY":
        "Function works only with Matrix (RAM).\n"
        "  For BigData use SQL functions:\n"
        "     filterif, groupby, join.",
    "RUNTIME_DUCKDB_ONLY":
        "Function works only with DuckDB (BigData).\n"
        "  Example: OpenCSV(\"file.csv\", BigData)",
    "RUNTIME_DUCKDB_NOT_INSTALLED":
        "DuckDB is not installed.\n"
        "  Install: pip install duckdb",
    "RUNTIME_FILE_NOT_FOUND":
        "File not found.\n"
        "  Check the path and file name.",
    "RUNTIME_NAME_ERROR":
        "Variable is not defined.\n"
        "  Check the variable name.",
    "RUNTIME_TYPE_ERROR":
        "Type error in operation.",
    "RUNTIME_VALUE_ERROR":
        "Invalid value.",
    "RUNTIME_INDEX_ERROR":
        "Index out of range.\n"
        "  Check row/column count.",
    "RUNTIME_DIVISION_BY_ZERO":
        "Division by zero.\n"
        "  Result: inf (infinity).",
    "RUNTIME_EMPTY_MATRIX":
        "Matrix is empty.\n"
        "  Nothing to process.",
    "RUNTIME_NOT_2D":
        "2D matrix expected.\n"
        "  Vector is not supported by this function.",
    "RUNTIME_NOT_1D":
        "Vector (1D) expected.\n"
        "  Matrix is not supported by this function.",
    "RUNTIME_OUT_OF_RANGE":
        "Index out of range.\n"
        "  Allowed values: 1..N.",
}