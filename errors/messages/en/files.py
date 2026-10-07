# errors/messages/en/files.py
"""
Errors for file functions: CSV, Excel, TXT, Parquet, SQLite, BigData.
"""

MESSAGES = {
    # ============================================================
    # EXCEL
    # ============================================================
    "EXCEL_NOT_INSTALLED":
        "openpyxl is not installed. Install: pip install openpyxl",
    "EXCEL_FILE_NOT_FOUND": "Excel file not found.",
    "EXCEL_SHEET_NOT_FOUND": "Excel sheet not found.",
    "EXCEL_LOAD_ERROR": "Error loading Excel file.",
    "EXCEL_SAVE_ERROR": "Error saving Excel file.",

    # ============================================================
    # CSV / BIGDATA
    # ============================================================
    "CSV_FILE_NOT_FOUND": "CSV file not found.",
    "CSV_LOAD_ERROR": "Error loading CSV file.",
    "CSV_SAVE_ERROR": "Error saving CSV file.",
    "CSV_ENCODING_ERROR": "Could not detect CSV file encoding.",
    "CSV_BAD_MODE":
        "Invalid CSV open mode.\n"
        "  Allowed:\n"
        "     OpenCSV(\"file.csv\")               — auto (by size)\n"
        "     OpenCSV(\"file.csv\", BigData)      — force DuckDB\n"
        "     OpenCSV(\"file.csv\", Table)        — force RAM\n"
        "\n"
        "  BigData — for large files (>250 MB): data on disk, RAM ~50 MB.\n"
        "  Table   — data in memory (MatrExMatrix).",
    "CSV_BIGDATA_NOT_AVAILABLE":
        "BigData mode requires DuckDB.\n"
        "  Install: pip install duckdb",
    "CSV_MODE_NOT_STRING":
        "OpenCSV mode must be BigData or Table.",

    # ============================================================
    # TO_MATRIX / TO_BIGDATA
    # ============================================================
    "TOBIGDATA_BAD_SYNTAX":
        "Invalid Convert_Matrix_To_BigData() syntax.\n"
        "  Format: Convert_Matrix_To_BigData(matrix)",
    "TOBIGDATA_VECTOR_NOT_SUPPORTED":
        "Convert_Matrix_To_BigData works only with 2D matrices.\n"
        "  Vector cannot be converted to BigData.",
    "TOBIGDATA_NOT_MATRIX":
        "Convert_Matrix_To_BigData: matrix expected.",
    "TOBIGDATA_EMPTY":
        "Convert_Matrix_To_BigData: matrix is empty.\n"
        "  Nothing to convert.",
    "TOBIGDATA_TEMP_ERROR":
        "Convert_Matrix_To_BigData: failed to create temp file.",
    "TOBIGDATA_DUCKDB_NOT_INSTALLED":
        "Convert_Matrix_To_BigData requires DuckDB.\n"
        "  Install: pip install duckdb",
    "TOMATRIX_BAD_SYNTAX":
        "Invalid ToMatrix() syntax.\n"
        "  Format: ToMatrix(data [, limit])",
    "TOMATRIX_MEMORY_ERROR":
        "Not enough RAM to load into Matrix.\n"
        "  Use limit: ToMatrix(m, 100000)",

    # ============================================================
    # TXT
    # ============================================================
    "TXT_FILE_NOT_FOUND": "TXT file not found.",
    "TXT_LOAD_ERROR": "Error loading TXT file.",
    "TXT_SAVE_ERROR": "Error saving TXT file.",
    "TXT_BAD_DELIMITER":
        "Delimiter must be a single character.\n"
        "  Use '\\t' for tab.",
    "TXT_ENCODING_ERROR": "Could not detect TXT file encoding.",

    # ============================================================
    # SQLITE
    # ============================================================
    "SQLITE_FILE_NOT_FOUND": "SQLite database file not found.",
    "SQLITE_TABLE_NOT_FOUND": "Table not found in database.",
    "SQLITE_TABLE_EXISTS":
        "Table already exists.\n"
        "  Use overwrite to replace it.",
    "SQLITE_QUERY_ERROR": "SQL query execution error.",
    "SQLITE_LOAD_ERROR": "Error loading from SQLite.",
    "SQLITE_SAVE_ERROR": "Error saving to SQLite.",
    "SQLITE_NEED_TABLE_NAME": "Table name not specified.",
    "SQLITE_BAD_WHERE":
        "Invalid WHERE condition.\n"
        "  WHERE must be a string in quotes.",
    "SQLITE_BAD_ORDER":
        "Invalid ORDER BY condition.\n"
        "  ORDER BY must be a string in quotes.",
    "SQLITE_BAD_QUERY":
        "SQL query must be a string in quotes.",
}