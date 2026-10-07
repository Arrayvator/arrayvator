# errors/messages/ru/runtime.py
"""
Ошибки времени выполнения (RUNTIME_*).
"""

MESSAGES = {
    "RUNTIME_NOT_MATRIX":
        "Ожидается матрица.\n"
        "  Пример: matrixmod(m, delete, 2)",
    "RUNTIME_NOT_VECTOR":
        "Ожидается вектор.\n"
        "  Вектор — это одна строка или столбец значений.",
    "RUNTIME_MATRIX_ONLY":
        "Функция работает только с Matrix (RAM).\n"
        "  Для BigData используйте SQL-функции:\n"
        "     filterif, groupby, join.",
    "RUNTIME_DUCKDB_ONLY":
        "Функция работает только с DuckDB (BigData).\n"
        "  Пример: OpenCSV(\"file.csv\", BigData)",
    "RUNTIME_DUCKDB_NOT_INSTALLED":
        "DuckDB не установлен.\n"
        "  Установите: pip install duckdb",
    "RUNTIME_FILE_NOT_FOUND":
        "Файл не найден.\n"
        "  Проверьте путь и имя файла.",
    "RUNTIME_NAME_ERROR":
        "Переменная не определена.\n"
        "  Проверьте имя переменной.",
    "RUNTIME_TYPE_ERROR":
        "Неверный тип данных в операции.",
    "RUNTIME_VALUE_ERROR":
        "Неверное значение.",
    "RUNTIME_INDEX_ERROR":
        "Индекс вне диапазона.\n"
        "  Проверьте количество строк/столбцов.",
    "RUNTIME_DIVISION_BY_ZERO":
        "Деление на ноль.\n"
        "  Результат: inf (бесконечность).",
    "RUNTIME_EMPTY_MATRIX":
        "Матрица пуста.\n"
        "  Нечего обрабатывать.",
    "RUNTIME_NOT_2D":
        "Ожидается двумерная матрица (2D).\n"
        "  Вектор не подходит для этой функции.",
    "RUNTIME_NOT_1D":
        "Ожидается вектор (1D).\n"
        "  Матрица не подходит для этой функции.",
    "RUNTIME_OUT_OF_RANGE":
        "Индекс вне диапазона.\n"
        "  Проверьте допустимые значения: 1..N.",
}