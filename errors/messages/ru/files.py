# errors/messages/ru/files.py
"""
Ошибки файловых функций: CSV, Excel, TXT, Parquet, SQLite, BigData.
"""

MESSAGES = {
    # ============================================================
    # EXCEL
    # ============================================================
    "EXCEL_NOT_INSTALLED":
        "Библиотека openpyxl не установлена. Установите: pip install openpyxl",
    "EXCEL_FILE_NOT_FOUND": "Excel-файл не найден.",
    "EXCEL_SHEET_NOT_FOUND": "Лист Excel не найден.",
    "EXCEL_LOAD_ERROR": "Ошибка загрузки Excel-файла.",
    "EXCEL_SAVE_ERROR": "Ошибка сохранения Excel-файла.",

    # ============================================================
    # CSV / BIGDATA
    # ============================================================
    "CSV_FILE_NOT_FOUND": "CSV-файл не найден.",
    "CSV_LOAD_ERROR": "Ошибка загрузки CSV-файла.",
    "CSV_SAVE_ERROR": "Ошибка сохранения CSV-файла.",
    "CSV_ENCODING_ERROR": "Не удалось определить кодировку CSV-файла.",
    "CSV_BAD_MODE":
        "Неверный режим открытия CSV.\n"
        "  Допустимо:\n"
        "     OpenCSV(\"file.csv\")               — авто (по размеру)\n"
        "     OpenCSV(\"file.csv\", BigData)      — принудительно DuckDB\n"
        "     OpenCSV(\"file.csv\", Table)        — принудительно RAM\n"
        "\n"
        "  BigData — для больших файлов (>250 МБ): данные на диске, RAM ~50 МБ.\n"
        "  Table   — данные в оперативной памяти (MatrExMatrix).",
    "CSV_BIGDATA_NOT_AVAILABLE":
        "Режим BigData требует DuckDB.\n"
        "  Установите: pip install duckdb",
    "CSV_MODE_NOT_STRING":
        "Режим OpenCSV должен быть BigData или Table.",

    # ============================================================
    # TO_MATRIX / TO_BIGDATA
    # ============================================================
    "TOBIGDATA_BAD_SYNTAX":
        "Неверный синтаксис Convert_Matrix_To_BigData().\n"
        "  Формат: Convert_Matrix_To_BigData(матрица)",
    "TOBIGDATA_VECTOR_NOT_SUPPORTED":
        "Convert_Matrix_To_BigData работает только с 2D-матрицами.\n"
        "  Вектор нельзя конвертировать в BigData.",
    "TOBIGDATA_NOT_MATRIX":
        "Convert_Matrix_To_BigData: нужна матрица.",
    "TOBIGDATA_EMPTY":
        "Convert_Matrix_To_BigData: матрица пуста.\n"
        "  Нечего конвертировать.",
    "TOBIGDATA_TEMP_ERROR":
        "Convert_Matrix_To_BigData: не удалось создать временный файл.",
    "TOBIGDATA_DUCKDB_NOT_INSTALLED":
        "Convert_Matrix_To_BigData требует DuckDB.\n"
        "  Установите: pip install duckdb",
    "TOMATRIX_BAD_SYNTAX":
        "Неверный синтаксис ToMatrix().\n"
        "  Формат: ToMatrix(данные [, limit])",
    "TOMATRIX_MEMORY_ERROR":
        "Недостаточно RAM для загрузки в Matrix.\n"
        "  Используйте limit: ToMatrix(m, 100000)",

    # ============================================================
    # TXT
    # ============================================================
    "TXT_FILE_NOT_FOUND": "TXT-файл не найден.",
    "TXT_LOAD_ERROR": "Ошибка загрузки TXT-файла.",
    "TXT_SAVE_ERROR": "Ошибка сохранения TXT-файла.",
    "TXT_BAD_DELIMITER":
        "Разделитель должен быть 1 символ.\n"
        "  Для табуляции используйте '\\t'.",
    "TXT_ENCODING_ERROR": "Не удалось определить кодировку TXT-файла.",

    # ============================================================
    # SQLITE
    # ============================================================
    "SQLITE_FILE_NOT_FOUND": "Файл базы данных SQLite не найден.",
    "SQLITE_TABLE_NOT_FOUND": "Таблица не найдена в базе данных.",
    "SQLITE_TABLE_EXISTS":
        "Таблица уже существует.\n"
        "  Используйте overwrite для перезаписи.",
    "SQLITE_QUERY_ERROR": "Ошибка выполнения SQL-запроса.",
    "SQLITE_LOAD_ERROR": "Ошибка загрузки из SQLite.",
    "SQLITE_SAVE_ERROR": "Ошибка сохранения в SQLite.",
    "SQLITE_NEED_TABLE_NAME": "Не указано имя таблицы.",
    "SQLITE_BAD_WHERE":
        "Неверное условие WHERE.\n"
        "  WHERE должен быть строкой в кавычках.",
    "SQLITE_BAD_ORDER":
        "Неверное условие ORDER BY.\n"
        "  ORDER BY должен быть строкой в кавычках.",
    "SQLITE_BAD_QUERY":
        "SQL-запрос должен быть строкой в кавычках.",
}