# errors/functions_db/convert.py
"""
База ошибок для функций конвертации Matrix ↔ DuckDB:

    ToMatrix(data [, limit])                    — DuckDB → Matrix
    ToBigData(data)                             — Matrix → DuckDB
    Convert_BigData_To_Matrix(data [, limit])   — синоним ToMatrix
    Convert_Matrix_To_BigData(data)             — синоним ToBigData

ПРАВИЛА:
    - ToMatrix загружает данные из DuckDB в RAM.
      Для больших таблиц — используйте limit.
    - ToBigData сохраняет Matrix в DuckDB через временный CSV.
      Работает только с 2D-матрицами (не с векторами).
    - Временный CSV удаляется при выходе из программы.
"""


RU = {
    # ============================================================
    # TO_MATRIX — DuckDB → Matrix
    # ============================================================
    'ToMatrix': {
        'name': 'ToMatrix',
        'category': 'bigdata',
        'signature': 'ToMatrix(данные [, limit])',
        'description': (
            'Конвертирует DuckDBTable в MatrExMatrix (RAM).\n'
            '  • Без limit — загружает ВСЕ строки.\n'
            '  • С limit — только первые N строк.\n'
            '  • Возвращает НОВУЮ матрицу.\n'
            '  • Для больших таблиц используйте limit — иначе RAM переполнится.'
        ),
        'examples': [
            'm = OpenCSV("big.csv", BigData)',
            'm = ToMatrix(m)                    # все строки',
            'm = ToMatrix(m, 100000)            # первые 100 тыс.',
        ],
        'errors': {
            'TOMATRIX_BAD_SYNTAX': {
                'message': (
                    "ToMatrix: неверный синтаксис.\n"
                    "  Нужны данные и, опционально, limit."
                ),
                'wrong': 'ToMatrix()',
                'right': 'ToMatrix(bd)',
                'explanation': (
                    "ToMatrix принимает 1 или 2 аргумента:\n"
                    "  1. данные — DuckDBTable\n"
                    "  2. limit  — число (опц.), максимум строк\n"
                    "\n"
                    "Неправильно:\n"
                    "     ToMatrix()\n"
                    "     ToMatrix(bd, 100000, 200000)\n"
                    "\n"
                    "Правильно:\n"
                    "     ToMatrix(bd)             # все строки\n"
                    "     ToMatrix(bd, 100000)     # первые 100 тыс."
                ),
                'variants': [
                    'm = ToMatrix(bd)',
                    'm = ToMatrix(bd, 100000)',
                ],
            },
            'TOMATRIX_NOT_DUCKDB': {
                'message': (
                    "ToMatrix: ожидается DuckDBTable (BigData).\n"
                    "  Если данные уже в RAM — конвертация не нужна."
                ),
                'wrong': 'm = ToMatrix(42)',
                'right': 'm = ToMatrix(bd)',
                'explanation': (
                    "ToMatrix работает только с DuckDBTable:\n"
                    "     bd = OpenCSV(\"big.csv\", BigData)\n"
                    "     m  = ToMatrix(bd)\n"
                    "\n"
                    "Неправильно:\n"
                    "     ToMatrix(42)\n"
                    "     ToMatrix(m)         — уже Matrix, не нужно\n"
                    "\n"
                    "Правильно:\n"
                    "     ToMatrix(bd)"
                ),
                'variants': [
                    'bd = OpenCSV("big.csv", BigData)\nm = ToMatrix(bd)',
                    'bd = OpenParquet("data.parquet")\nm = ToMatrix(bd)',
                ],
            },
            'TOMATRIX_MEMORY_ERROR': {
                'message': (
                    "ToMatrix: недостаточно RAM для загрузки.\n"
                    "  Используйте limit для загрузки части данных."
                ),
                'wrong': 'm = ToMatrix(bd)         # миллионы строк',
                'right': 'm = ToMatrix(bd, 100000)',
                'explanation': (
                    "DuckDB хранит данные на диске (RAM ~50 МБ).\n"
                    "ToMatrix загружает ВСЁ в RAM.\n"
                    "\n"
                    "Для больших таблиц используйте limit:\n"
                    "     m = ToMatrix(bd, 100000)     # первые 100 тыс.\n"
                    "     m = ToMatrix(bd, 1000000)    # 1 млн\n"
                    "\n"
                    "Ориентир: 1 млн строк × 5 столбцов ≈ 500 МБ RAM.\n"
                    "\n"
                    "Если нужен весь объём — работайте с DuckDB напрямую:\n"
                    "     filterif(bd[:, \"Отдел\"] == \"IT\")\n"
                    "     groupby(by bd[:, \"Отдел\"], agg sum(bd[:, \"Сумма\"]))"
                ),
                'variants': [
                    'm = ToMatrix(bd, 100000)',
                    'm = ToMatrix(bd, 1000000)',
                ],
            },
        },
    },

    # ============================================================
    # TO_BIGDATA — Matrix → DuckDB
    # ============================================================
    'ToBigData': {
        'name': 'ToBigData',
        'category': 'bigdata',
        'signature': 'ToBigData(данные)',
        'description': (
            'Конвертирует MatrExMatrix в DuckDBTable (BigData).\n'
            '  • Работает только с 2D-матрицами (не с векторами).\n'
            '  • Создаёт временный CSV в _av_temp/.\n'
            '  • Временный файл удаляется при выходе.\n'
            '  • Возвращает DuckDBTable.'
        ),
        'examples': [
            'bd = ToBigData(m)',
        ],
        'errors': {
            'TOBIGDATA_BAD_SYNTAX': {
                'message': (
                    "ToBigData: неверный синтаксис.\n"
                    "  Нужна матрица."
                ),
                'wrong': 'ToBigData()',
                'right': 'ToBigData(m)',
                'explanation': (
                    "ToBigData принимает ОДИН аргумент — матрицу:\n"
                    "     bd = ToBigData(m)\n"
                    "\n"
                    "Неправильно:\n"
                    "     ToBigData()\n"
                    "     ToBigData(m, 100)\n"
                    "\n"
                    "Правильно:\n"
                    "     bd = ToBigData(m)"
                ),
                'variants': [
                    'bd = ToBigData(m)',
                ],
            },
            'TOBIGDATA_NOT_MATRIX': {
                'message': (
                    "ToBigData: ожидается MatrExMatrix.\n"
                    "  Число, строка или вектор не подходят."
                ),
                'wrong': 'bd = ToBigData(42)',
                'right': 'bd = ToBigData(m)',
                'explanation': (
                    "ToBigData работает только с 2D-матрицами:\n"
                    "     m  = [\"A\", \"B\"; 1, 2; 3, 4]\n"
                    "     bd = ToBigData(m)\n"
                    "\n"
                    "Неправильно:\n"
                    "     ToBigData(42)\n"
                    "     ToBigData(\"text\")\n"
                    "     ToBigData(v)         — вектор (1D)\n"
                    "\n"
                    "Правильно:\n"
                    "     ToBigData(m)"
                ),
                'variants': [
                    'm = ["A", "B"; 1, 2]\nbd = ToBigData(m)',
                ],
            },
            'TOBIGDATA_VECTOR_NOT_SUPPORTED': {
                'message': (
                    "ToBigData: работает только с 2D-матрицами.\n"
                    "  Вектор нельзя конвертировать в BigData."
                ),
                'wrong': 'bd = ToBigData(v)',
                'right': 'bd = ToBigData(m)',
                'explanation': (
                    "DuckDB — это таблица (2D).\n"
                    "Вектор (1D) не имеет смысла как таблица.\n"
                    "\n"
                    "Неправильно:\n"
                    "     ToBigData([1, 2, 3])         — вектор\n"
                    "\n"
                    "Правильно:\n"
                    "     m  = [\"A\"; 1; 2; 3]         — матрица N×1\n"
                    "     bd = ToBigData(m)\n"
                    "\n"
                    "Или сделайте вектор столбцом матрицы:\n"
                    "     m = [\"A\", \"B\"; 1, 2]\n"
                    "     bd = ToBigData(m)"
                ),
                'variants': [
                    'm = ["A", "B"; 1, 2]\nbd = ToBigData(m)',
                    'm = ["A"; 1; 2; 3]\nbd = ToBigData(m)',
                ],
            },
            'TOBIGDATA_EMPTY': {
                'message': (
                    "ToBigData: матрица пуста.\n"
                    "  Нечего конвертировать."
                ),
                'wrong': 'bd = ToBigData(matrix(0, 0))',
                'right': 'bd = ToBigData(m)',
                'explanation': (
                    "Пустая матрица (0 строк) не конвертируется.\n"
                    "\n"
                    "Неправильно:\n"
                    "     ToBigData(matrix(0, 0))\n"
                    "\n"
                    "Правильно:\n"
                    "     m = [\"A\", \"B\"; 1, 2]\n"
                    "     bd = ToBigData(m)"
                ),
                'variants': [
                    'm = ["A", "B"; 1, 2]\nbd = ToBigData(m)',
                ],
            },
            'TOBIGDATA_DUCKDB_NOT_INSTALLED': {
                'message': (
                    "ToBigData: DuckDB не установлен.\n"
                    "  Установите: pip install duckdb"
                ),
                'wrong': 'bd = ToBigData(m)',
                'right': (
                    'pip install duckdb\n'
                    'bd = ToBigData(m)'
                ),
                'explanation': (
                    "ToBigData использует DuckDB для чтения временного CSV.\n"
                    "\n"
                    "Установка:\n"
                    "     pip install duckdb"
                ),
                'variants': [
                    'pip install duckdb\nbd = ToBigData(m)',
                ],
            },
            'TOBIGDATA_TEMP_ERROR': {
                'message': (
                    "ToBigData: не удалось создать временный файл.\n"
                    "  Проверьте права на запись в рабочую папку."
                ),
                'wrong': 'bd = ToBigData(m)   # нет прав на запись',
                'right': 'bd = ToBigData(m)   # папка доступна',
                'explanation': (
                    "ToBigData создаёт временный CSV в _av_temp/.\n"
                    "\n"
                    "Возможные причины:\n"
                    "  • нет прав на запись в рабочую папку\n"
                    "  • диск переполнен\n"
                    "  • антивирус блокирует\n"
                    "\n"
                    "Временный файл создаётся рядом с программой:\n"
                    "     <рабочая_папка>/_av_temp/matrixtobigdata_XXXX.csv"
                ),
                'variants': [
                    'bd = ToBigData(m)',
                ],
            },
        },
    },

    # ============================================================
    # CONVERT_BIGDATA_TO_MATRIX — синоним ToMatrix
    # ============================================================
    'Convert_BigData_To_Matrix': {
        'name': 'Convert_BigData_To_Matrix',
        'category': 'bigdata',
        'signature': 'Convert_BigData_To_Matrix(данные [, limit])',
        'description': (
            'Синоним ToMatrix. DuckDB → Matrix.\n'
            '  • Без limit — все строки.\n'
            '  • С limit — первые N строк.'
        ),
        'examples': [
            'm = Convert_BigData_To_Matrix(bd)',
            'm = Convert_BigData_To_Matrix(bd, 100000)',
        ],
        'errors': {
            'CONVERT_BDM_BAD_SYNTAX': {
                'message': (
                    "Convert_BigData_To_Matrix: неверный синтаксис.\n"
                    "  Нужны данные и, опционально, limit."
                ),
                'wrong': 'Convert_BigData_To_Matrix()',
                'right': 'Convert_BigData_To_Matrix(bd)',
                'explanation': (
                    "Принимает 1 или 2 аргумента:\n"
                    "     Convert_BigData_To_Matrix(bd)\n"
                    "     Convert_BigData_To_Matrix(bd, 100000)\n"
                    "\n"
                    "Это синоним ToMatrix."
                ),
                'variants': [
                    'm = Convert_BigData_To_Matrix(bd)',
                    'm = Convert_BigData_To_Matrix(bd, 100000)',
                ],
            },
            'CONVERT_BDM_NOT_DUCKDB': {
                'message': (
                    "Convert_BigData_To_Matrix: ожидается DuckDBTable."
                ),
                'wrong': 'm = Convert_BigData_To_Matrix(42)',
                'right': 'm = Convert_BigData_To_Matrix(bd)',
                'explanation': (
                    "Работает только с DuckDBTable:\n"
                    "     bd = OpenCSV(\"big.csv\", BigData)\n"
                    "     m  = Convert_BigData_To_Matrix(bd)\n"
                    "\n"
                    "Неправильно:\n"
                    "     Convert_BigData_To_Matrix(42)"
                ),
                'variants': [
                    'bd = OpenCSV("big.csv", BigData)\nm = Convert_BigData_To_Matrix(bd)',
                ],
            },
            'CONVERT_BDM_MEMORY_ERROR': {
                'message': (
                    "Convert_BigData_To_Matrix: недостаточно RAM.\n"
                    "  Используйте limit."
                ),
                'wrong': 'm = Convert_BigData_To_Matrix(bd)',
                'right': 'm = Convert_BigData_To_Matrix(bd, 100000)',
                'explanation': (
                    "Для больших таблиц используйте limit:\n"
                    "     m = Convert_BigData_To_Matrix(bd, 100000)"
                ),
                'variants': [
                    'm = Convert_BigData_To_Matrix(bd, 100000)',
                ],
            },
        },
    },

    # ============================================================
    # CONVERT_MATRIX_TO_BIGDATA — синоним ToBigData
    # ============================================================
    'Convert_Matrix_To_BigData': {
        'name': 'Convert_Matrix_To_BigData',
        'category': 'bigdata',
        'signature': 'Convert_Matrix_To_BigData(данные)',
        'description': (
            'Синоним ToBigData. Matrix → DuckDB.\n'
            '  • Работает только с 2D-матрицами.'
        ),
        'examples': [
            'bd = Convert_Matrix_To_BigData(m)',
        ],
        'errors': {
            'CONVERT_MB_BAD_SYNTAX': {
                'message': (
                    "Convert_Matrix_To_BigData: неверный синтаксис.\n"
                    "  Нужна матрица."
                ),
                'wrong': 'Convert_Matrix_To_BigData()',
                'right': 'Convert_Matrix_To_BigData(m)',
                'explanation': (
                    "Принимает ОДИН аргумент — матрицу:\n"
                    "     Convert_Matrix_To_BigData(m)\n"
                    "\n"
                    "Это синоним ToBigData."
                ),
                'variants': [
                    'bd = Convert_Matrix_To_BigData(m)',
                ],
            },
            'CONVERT_MB_NOT_MATRIX': {
                'message': (
                    "Convert_Matrix_To_BigData: ожидается MatrExMatrix."
                ),
                'wrong': 'bd = Convert_Matrix_To_BigData(42)',
                'right': 'bd = Convert_Matrix_To_BigData(m)',
                'explanation': (
                    "Работает только с 2D-матрицами:\n"
                    "     bd = Convert_Matrix_To_BigData(m)\n"
                    "\n"
                    "Неправильно:\n"
                    "     Convert_Matrix_To_BigData(42)\n"
                    "     Convert_Matrix_To_BigData(v)     — вектор"
                ),
                'variants': [
                    'bd = Convert_Matrix_To_BigData(m)',
                ],
            },
            'CONVERT_MB_VECTOR_NOT_SUPPORTED': {
                'message': (
                    "Convert_Matrix_To_BigData: только 2D-матрицы.\n"
                    "  Вектор нельзя конвертировать в BigData."
                ),
                'wrong': 'bd = Convert_Matrix_To_BigData(v)',
                'right': 'bd = Convert_Matrix_To_BigData(m)',
                'explanation': (
                    "DuckDB — это таблица (2D).\n"
                    "Вектор (1D) не подходит.\n"
                    "\n"
                    "Правильно:\n"
                    "     m = [\"A\", \"B\"; 1, 2]\n"
                    "     bd = Convert_Matrix_To_BigData(m)"
                ),
                'variants': [
                    'm = ["A", "B"; 1, 2]\nbd = Convert_Matrix_To_BigData(m)',
                ],
            },
            'CONVERT_MB_EMPTY': {
                'message': (
                    "Convert_Matrix_To_BigData: матрица пуста."
                ),
                'wrong': 'bd = Convert_Matrix_To_BigData(matrix(0, 0))',
                'right': 'bd = Convert_Matrix_To_BigData(m)',
                'explanation': (
                    "Пустая матрица не конвертируется.\n"
                    "\n"
                    "Правильно:\n"
                    "     m = [\"A\", \"B\"; 1, 2]\n"
                    "     bd = Convert_Matrix_To_BigData(m)"
                ),
                'variants': [
                    'm = ["A", "B"; 1, 2]\nbd = Convert_Matrix_To_BigData(m)',
                ],
            },
        },
    },
}


EN = {
    # ============================================================
    # TO_MATRIX
    # ============================================================
    'ToMatrix': {
        'name': 'ToMatrix',
        'category': 'bigdata',
        'signature': 'ToMatrix(data [, limit])',
        'description': (
            'Converts DuckDBTable to MatrExMatrix (RAM).\n'
            '  • Without limit — loads ALL rows.\n'
            '  • With limit — only the first N rows.\n'
            '  • Returns a NEW matrix.\n'
            '  • For large tables use limit — otherwise RAM overflows.'
        ),
        'examples': [
            'm = OpenCSV("big.csv", BigData)',
            'm = ToMatrix(m)                    # all rows',
            'm = ToMatrix(m, 100000)            # first 100k',
        ],
        'errors': {
            'TOMATRIX_BAD_SYNTAX': {
                'message': (
                    "ToMatrix: invalid syntax.\n"
                    "  Need data and optionally a limit."
                ),
                'wrong': 'ToMatrix()',
                'right': 'ToMatrix(bd)',
                'explanation': (
                    "ToMatrix takes 1 or 2 arguments:\n"
                    "  1. data — DuckDBTable\n"
                    "  2. limit — number (optional), max rows\n"
                    "\n"
                    "Incorrect:\n"
                    "     ToMatrix()\n"
                    "     ToMatrix(bd, 100000, 200000)\n"
                    "\n"
                    "Correct:\n"
                    "     ToMatrix(bd)             # all rows\n"
                    "     ToMatrix(bd, 100000)     # first 100k"
                ),
                'variants': [
                    'm = ToMatrix(bd)',
                    'm = ToMatrix(bd, 100000)',
                ],
            },
            'TOMATRIX_NOT_DUCKDB': {
                'message': (
                    "ToMatrix: DuckDBTable (BigData) expected.\n"
                    "  If data is already in RAM — no conversion needed."
                ),
                'wrong': 'm = ToMatrix(42)',
                'right': 'm = ToMatrix(bd)',
                'explanation': (
                    "ToMatrix works only with DuckDBTable:\n"
                    "     bd = OpenCSV(\"big.csv\", BigData)\n"
                    "     m  = ToMatrix(bd)\n"
                    "\n"
                    "Incorrect:\n"
                    "     ToMatrix(42)\n"
                    "     ToMatrix(m)         — already Matrix, no need\n"
                    "\n"
                    "Correct:\n"
                    "     ToMatrix(bd)"
                ),
                'variants': [
                    'bd = OpenCSV("big.csv", BigData)\nm = ToMatrix(bd)',
                    'bd = OpenParquet("data.parquet")\nm = ToMatrix(bd)',
                ],
            },
            'TOMATRIX_MEMORY_ERROR': {
                'message': (
                    "ToMatrix: not enough RAM to load.\n"
                    "  Use limit to load a subset."
                ),
                'wrong': 'm = ToMatrix(bd)         # millions of rows',
                'right': 'm = ToMatrix(bd, 100000)',
                'explanation': (
                    "DuckDB keeps data on disk (RAM ~50 MB).\n"
                    "ToMatrix loads EVERYTHING into RAM.\n"
                    "\n"
                    "For large tables use limit:\n"
                    "     m = ToMatrix(bd, 100000)     # first 100k\n"
                    "     m = ToMatrix(bd, 1000000)    # 1M\n"
                    "\n"
                    "Guide: 1M rows × 5 columns ≈ 500 MB RAM.\n"
                    "\n"
                    "If you need the whole volume — work with DuckDB directly:\n"
                    "     filterif(bd[:, \"Dept\"] == \"IT\")\n"
                    "     groupby(by bd[:, \"Dept\"], agg sum(bd[:, \"Amount\"]))"
                ),
                'variants': [
                    'm = ToMatrix(bd, 100000)',
                    'm = ToMatrix(bd, 1000000)',
                ],
            },
        },
    },

    # ============================================================
    # TO_BIGDATA
    # ============================================================
    'ToBigData': {
        'name': 'ToBigData',
        'category': 'bigdata',
        'signature': 'ToBigData(data)',
        'description': (
            'Converts MatrExMatrix to DuckDBTable (BigData).\n'
            '  • Works only with 2D matrices (not vectors).\n'
            '  • Creates a temp CSV in _av_temp/.\n'
            '  • Temp file is deleted on exit.\n'
            '  • Returns a DuckDBTable.'
        ),
        'examples': [
            'bd = ToBigData(m)',
        ],
        'errors': {
            'TOBIGDATA_BAD_SYNTAX': {
                'message': (
                    "ToBigData: invalid syntax.\n"
                    "  A matrix is required."
                ),
                'wrong': 'ToBigData()',
                'right': 'ToBigData(m)',
                'explanation': (
                    "ToBigData takes ONE argument — a matrix:\n"
                    "     bd = ToBigData(m)\n"
                    "\n"
                    "Incorrect:\n"
                    "     ToBigData()\n"
                    "     ToBigData(m, 100)\n"
                    "\n"
                    "Correct:\n"
                    "     bd = ToBigData(m)"
                ),
                'variants': [
                    'bd = ToBigData(m)',
                ],
            },
            'TOBIGDATA_NOT_MATRIX': {
                'message': (
                    "ToBigData: MatrExMatrix expected.\n"
                    "  A number, string, or vector will not work."
                ),
                'wrong': 'bd = ToBigData(42)',
                'right': 'bd = ToBigData(m)',
                'explanation': (
                    "ToBigData works only with 2D matrices:\n"
                    "     m  = [\"A\", \"B\"; 1, 2; 3, 4]\n"
                    "     bd = ToBigData(m)\n"
                    "\n"
                    "Incorrect:\n"
                    "     ToBigData(42)\n"
                    "     ToBigData(\"text\")\n"
                    "     ToBigData(v)         — vector (1D)\n"
                    "\n"
                    "Correct:\n"
                    "     ToBigData(m)"
                ),
                'variants': [
                    'm = ["A", "B"; 1, 2]\nbd = ToBigData(m)',
                ],
            },
            'TOBIGDATA_VECTOR_NOT_SUPPORTED': {
                'message': (
                    "ToBigData: works only with 2D matrices.\n"
                    "  A vector cannot be converted to BigData."
                ),
                'wrong': 'bd = ToBigData(v)',
                'right': 'bd = ToBigData(m)',
                'explanation': (
                    "DuckDB is a table (2D).\n"
                    "A vector (1D) makes no sense as a table.\n"
                    "\n"
                    "Incorrect:\n"
                    "     ToBigData([1, 2, 3])         — vector\n"
                    "\n"
                    "Correct:\n"
                    "     m  = [\"A\"; 1; 2; 3]         — matrix N×1\n"
                    "     bd = ToBigData(m)\n"
                    "\n"
                    "Or make the vector a column of a matrix:\n"
                    "     m = [\"A\", \"B\"; 1, 2]\n"
                    "     bd = ToBigData(m)"
                ),
                'variants': [
                    'm = ["A", "B"; 1, 2]\nbd = ToBigData(m)',
                    'm = ["A"; 1; 2; 3]\nbd = ToBigData(m)',
                ],
            },
            'TOBIGDATA_EMPTY': {
                'message': (
                    "ToBigData: matrix is empty.\n"
                    "  Nothing to convert."
                ),
                'wrong': 'bd = ToBigData(matrix(0, 0))',
                'right': 'bd = ToBigData(m)',
                'explanation': (
                    "An empty matrix (0 rows) cannot be converted.\n"
                    "\n"
                    "Correct:\n"
                    "     m = [\"A\", \"B\"; 1, 2]\n"
                    "     bd = ToBigData(m)"
                ),
                'variants': [
                    'm = ["A", "B"; 1, 2]\nbd = ToBigData(m)',
                ],
            },
            'TOBIGDATA_DUCKDB_NOT_INSTALLED': {
                'message': (
                    "ToBigData: DuckDB is not installed.\n"
                    "  Install: pip install duckdb"
                ),
                'wrong': 'bd = ToBigData(m)',
                'right': (
                    'pip install duckdb\n'
                    'bd = ToBigData(m)'
                ),
                'explanation': (
                    "ToBigData uses DuckDB to read the temp CSV.\n"
                    "\n"
                    "Install:\n"
                    "     pip install duckdb"
                ),
                'variants': [
                    'pip install duckdb\nbd = ToBigData(m)',
                ],
            },
            'TOBIGDATA_TEMP_ERROR': {
                'message': (
                    "ToBigData: failed to create temp file.\n"
                    "  Check write permissions in the working folder."
                ),
                'wrong': 'bd = ToBigData(m)   # no write permission',
                'right': 'bd = ToBigData(m)   # folder is writable',
                'explanation': (
                    "ToBigData creates a temp CSV in _av_temp/.\n"
                    "\n"
                    "Possible reasons:\n"
                    "  • no write permission in the working folder\n"
                    "  • disk is full\n"
                    "  • antivirus blocking\n"
                    "\n"
                    "The temp file is created next to the program:\n"
                    "     <working_folder>/_av_temp/matrixtobigdata_XXXX.csv"
                ),
                'variants': [
                    'bd = ToBigData(m)',
                ],
            },
        },
    },

    # ============================================================
    # CONVERT_BIGDATA_TO_MATRIX
    # ============================================================
    'Convert_BigData_To_Matrix': {
        'name': 'Convert_BigData_To_Matrix',
        'category': 'bigdata',
        'signature': 'Convert_BigData_To_Matrix(data [, limit])',
        'description': (
            'Synonym for ToMatrix. DuckDB → Matrix.\n'
            '  • Without limit — all rows.\n'
            '  • With limit — first N rows.'
        ),
        'examples': [
            'm = Convert_BigData_To_Matrix(bd)',
            'm = Convert_BigData_To_Matrix(bd, 100000)',
        ],
        'errors': {
            'CONVERT_BDM_BAD_SYNTAX': {
                'message': (
                    "Convert_BigData_To_Matrix: invalid syntax.\n"
                    "  Need data and optionally a limit."
                ),
                'wrong': 'Convert_BigData_To_Matrix()',
                'right': 'Convert_BigData_To_Matrix(bd)',
                'explanation': (
                    "Takes 1 or 2 arguments:\n"
                    "     Convert_BigData_To_Matrix(bd)\n"
                    "     Convert_BigData_To_Matrix(bd, 100000)\n"
                    "\n"
                    "This is a synonym for ToMatrix."
                ),
                'variants': [
                    'm = Convert_BigData_To_Matrix(bd)',
                    'm = Convert_BigData_To_Matrix(bd, 100000)',
                ],
            },
            'CONVERT_BDM_NOT_DUCKDB': {
                'message': (
                    "Convert_BigData_To_Matrix: DuckDBTable expected."
                ),
                'wrong': 'm = Convert_BigData_To_Matrix(42)',
                'right': 'm = Convert_BigData_To_Matrix(bd)',
                'explanation': (
                    "Works only with DuckDBTable:\n"
                    "     bd = OpenCSV(\"big.csv\", BigData)\n"
                    "     m  = Convert_BigData_To_Matrix(bd)\n"
                    "\n"
                    "Incorrect:\n"
                    "     Convert_BigData_To_Matrix(42)"
                ),
                'variants': [
                    'bd = OpenCSV("big.csv", BigData)\nm = Convert_BigData_To_Matrix(bd)',
                ],
            },
            'CONVERT_BDM_MEMORY_ERROR': {
                'message': (
                    "Convert_BigData_To_Matrix: not enough RAM.\n"
                    "  Use limit."
                ),
                'wrong': 'm = Convert_BigData_To_Matrix(bd)',
                'right': 'm = Convert_BigData_To_Matrix(bd, 100000)',
                'explanation': (
                    "For large tables use limit:\n"
                    "     m = Convert_BigData_To_Matrix(bd, 100000)"
                ),
                'variants': [
                    'm = Convert_BigData_To_Matrix(bd, 100000)',
                ],
            },
        },
    },

    # ============================================================
    # CONVERT_MATRIX_TO_BIGDATA
    # ============================================================
    'Convert_Matrix_To_BigData': {
        'name': 'Convert_Matrix_To_BigData',
        'category': 'bigdata',
        'signature': 'Convert_Matrix_To_BigData(data)',
        'description': (
            'Synonym for ToBigData. Matrix → DuckDB.\n'
            '  • Works only with 2D matrices.'
        ),
        'examples': [
            'bd = Convert_Matrix_To_BigData(m)',
        ],
        'errors': {
            'CONVERT_MB_BAD_SYNTAX': {
                'message': (
                    "Convert_Matrix_To_BigData: invalid syntax.\n"
                    "  A matrix is required."
                ),
                'wrong': 'Convert_Matrix_To_BigData()',
                'right': 'Convert_Matrix_To_BigData(m)',
                'explanation': (
                    "Takes ONE argument — a matrix:\n"
                    "     Convert_Matrix_To_BigData(m)\n"
                    "\n"
                    "This is a synonym for ToBigData."
                ),
                'variants': [
                    'bd = Convert_Matrix_To_BigData(m)',
                ],
            },
            'CONVERT_MB_NOT_MATRIX': {
                'message': (
                    "Convert_Matrix_To_BigData: MatrExMatrix expected."
                ),
                'wrong': 'bd = Convert_Matrix_To_BigData(42)',
                'right': 'bd = Convert_Matrix_To_BigData(m)',
                'explanation': (
                    "Works only with 2D matrices:\n"
                    "     bd = Convert_Matrix_To_BigData(m)\n"
                    "\n"
                    "Incorrect:\n"
                    "     Convert_Matrix_To_BigData(42)\n"
                    "     Convert_Matrix_To_BigData(v)     — vector"
                ),
                'variants': [
                    'bd = Convert_Matrix_To_BigData(m)',
                ],
            },
            'CONVERT_MB_VECTOR_NOT_SUPPORTED': {
                'message': (
                    "Convert_Matrix_To_BigData: only 2D matrices.\n"
                    "  A vector cannot be converted to BigData."
                ),
                'wrong': 'bd = Convert_Matrix_To_BigData(v)',
                'right': 'bd = Convert_Matrix_To_BigData(m)',
                'explanation': (
                    "DuckDB is a table (2D).\n"
                    "A vector (1D) will not work.\n"
                    "\n"
                    "Correct:\n"
                    "     m = [\"A\", \"B\"; 1, 2]\n"
                    "     bd = Convert_Matrix_To_BigData(m)"
                ),
                'variants': [
                    'm = ["A", "B"; 1, 2]\nbd = Convert_Matrix_To_BigData(m)',
                ],
            },
            'CONVERT_MB_EMPTY': {
                'message': (
                    "Convert_Matrix_To_BigData: matrix is empty."
                ),
                'wrong': 'bd = Convert_Matrix_To_BigData(matrix(0, 0))',
                'right': 'bd = Convert_Matrix_To_BigData(m)',
                'explanation': (
                    "An empty matrix cannot be converted.\n"
                    "\n"
                    "Correct:\n"
                    "     m = [\"A\", \"B\"; 1, 2]\n"
                    "     bd = Convert_Matrix_To_BigData(m)"
                ),
                'variants': [
                    'm = ["A", "B"; 1, 2]\nbd = Convert_Matrix_To_BigData(m)',
                ],
            },
        },
    },
}