# syntax/signatures_data/files.py
"""
Сигнатуры: Excel, CSV, TXT, Parquet, SQLite.
"""

SIGNATURES = {
    # ============================================================
    # EXCEL
    # ============================================================
    'openexcel': {
        'name': 'OpenExcel',
        'category': 'excel',
        'args': ['"путь.xlsx"', 'лист (опц.): "Лист1" | N | all'],
        'examples': [
            'm = OpenExcel("file.xlsx")',
            'm = OpenExcel("file.xlsx", "Лист1")',
            'm = OpenExcel("file.xlsx", all)',
            'm = OpenExcel("file.xlsx", 1)',
        ],
    },

    'saveexcel': {
        'name': 'SaveExcel',
        'category': 'excel',
        'args': ['данные', '"путь.xlsx"', 'лист (опц.)'],
        'examples': [
            'SaveExcel(m, "file.xlsx")',
            'SaveExcel(m, "file.xlsx", "Лист1")',
        ],
    },

    'openexcelshow': {
        'name': 'OpenExcelShow',
        'category': 'excel',
        'args': [],
        'examples': ['m = OpenExcelShow()'],
    },

    'saveexcelshow': {
        'name': 'SaveExcelShow',
        'category': 'excel',
        'args': ['данные', 'имя листа (опц.)'],
        'examples': ['SaveExcelShow(m)', 'SaveExcelShow(m, "Лист1")'],
    },

    # ============================================================
    # CSV
    # ============================================================
    'opencsv': {
        'name': 'OpenCSV',
        'category': 'csv',
        'args': ['"путь.csv"', 'режим (опц.): BigData | Table'],
        'examples': [
            'm = OpenCSV("file.csv")',
            'm = OpenCSV("big.csv", BigData)',
            'm = OpenCSV("small.csv", Table)',
        ],
    },

    'savecsv': {
        'name': 'SaveCSV',
        'category': 'csv',
        'args': ['данные', '"путь.csv"'],
        'examples': [
            'SaveCSV(m, "file.csv")',
            'SaveCSV(m, "out.csv")',
        ],
    },

    'opencsvshow': {
        'name': 'OpenCSVShow',
        'category': 'csv',
        'args': ['режим (опц.): BigData | Table'],
        'examples': [
            'm = OpenCSVShow()',
            'm = OpenCSVShow(BigData)',
            'm = OpenCSVShow(Table)',
        ],
    },

    'savecsvshow': {
        'name': 'SaveCSVShow',
        'category': 'csv',
        'args': ['данные'],
        'examples': ['SaveCSVShow(m)'],
    },

    # ============================================================
    # TXT
    # ============================================================
    'opentxt': {
        'name': 'OpenTXT',
        'category': 'txt',
        'args': ['"путь.txt"', 'разделитель (опц.)'],
        'examples': [
            'm = OpenTXT("file.txt")',
            'm = OpenTXT("file.txt", ";")',
            'm = OpenTXT("file.txt", "\\t")',
        ],
    },

    'savetxt': {
        'name': 'SaveTXT',
        'category': 'txt',
        'args': ['данные', '"путь.txt"', 'разделитель (опц.)'],
        'examples': [
            'SaveTXT(m, "file.txt")',
            'SaveTXT(m, "out.txt", "\\t")',
        ],
    },

    'opentxtshow': {
        'name': 'OpenTXTShow',
        'category': 'txt',
        'args': ['разделитель (опц.)'],
        'examples': ['m = OpenTXTShow()', 'm = OpenTXTShow(";")'],
    },

    'savetxtshow': {
        'name': 'SaveTXTShow',
        'category': 'txt',
        'args': ['данные', 'разделитель (опц.)'],
        'examples': ['SaveTXTShow(m)', 'SaveTXTShow(m, ";")'],
    },

    # ============================================================
    # PARQUET
    # ============================================================
    'openparquet': {
        'name': 'OpenParquet',
        'category': 'parquet',
        'args': ['"путь.parquet"'],
        'examples': [
            'm = OpenParquet("data.parquet")',
            'm = OpenParquet("big.parquet")',
        ],
    },

    'saveparquet': {
        'name': 'SaveParquet',
        'category': 'parquet',
        'args': ['данные', '"путь.parquet"'],
        'examples': [
            'SaveParquet(m, "out.parquet")',
        ],
    },

    # ============================================================
    # SQLITE
    # ============================================================
    'opensqlite': {
        'name': 'OpenSQLite',
        'category': 'sqlite',
        'args': ['"путь.db"', '"таблица"', 'WHERE (опц.)', 'ORDER BY (опц.)'],
        'examples': [
            'm = OpenSQLite("mydb.db", "employees")',
            'm = OpenSQLite("mydb.db", "employees", "age > 25")',
            'm = OpenSQLite("mydb.db", "employees", "age > 25", "name ASC")',
        ],
    },

    'querysqlite': {
        'name': 'QuerySQLite',
        'category': 'sqlite',
        'args': ['"путь.db"', '"SELECT ..."'],
        'examples': [
            'm = QuerySQLite("mydb.db", "SELECT * FROM employees WHERE age > 25")',
            'm = QuerySQLite("mydb.db", "SELECT dept, COUNT(*) FROM employees GROUP BY dept")',
        ],
    },

    'savesqlite': {
        'name': 'SaveSQLite',
        'category': 'sqlite',
        'args': ['данные', '"путь.db"', '"таблица"', 'overwrite (опц.)'],
        'examples': [
            'SaveSQLite(m, "mydb.db", "employees")',
            'SaveSQLite(m, "mydb.db", "employees", overwrite)',
        ],
    },

    'opensqliteshow': {
        'name': 'OpenSQLiteShow',
        'category': 'sqlite',
        'args': [],
        'examples': ['m = OpenSQLiteShow()'],
    },

    'savesqliteshow': {
        'name': 'SaveSQLiteShow',
        'category': 'sqlite',
        'args': ['данные'],
        'examples': ['SaveSQLiteShow(m)'],
    },
}