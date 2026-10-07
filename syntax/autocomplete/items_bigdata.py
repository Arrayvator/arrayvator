# syntax/autocomplete/items_bigdata.py
"""
Описания функций конвертации Matrix ↔ DuckDB.
"""

RU = {
    'ToMatrix': {
        'signature': 'ToMatrix(данные [, limit])',
        'description': (
            'Конвертирует DuckDBTable в MatrExMatrix (в RAM).\n'
            '  • без limit — все строки\n'
            '  • с limit — только первые N строк'
        ),
        'example': (
            'm = OpenCSV("big.csv", BigData)\n'
            'm = ToMatrix(m)                    # → Matrix\n'
            'm = ToMatrix(m, 100000)            # только 100 тыс. строк'
        ),
    },
    'Convert_BigData_To_Matrix': {
        'signature': 'Convert_BigData_To_Matrix(данные [, limit])',
        'description': 'Синоним ToMatrix. DuckDB → Matrix.',
        'example': 'm = Convert_BigData_To_Matrix(m)',
    },
    'Convert_Matrix_To_BigData': {
        'signature': 'Convert_Matrix_To_BigData(данные)',
        'description': (
            'Конвертирует MatrExMatrix в DuckDBTable (BigData).\n'
            'Работает только с 2D-матрицами.'
        ),
        'example': (
            'm = ["A", "B"; 1, 2]\n'
            'bd = Convert_Matrix_To_BigData(m)\n'
            'print(type(bd))   # duckdb'
        ),
    },
    'ToBigData': {
        'signature': 'ToBigData(данные)',
        'description': 'Синоним Convert_Matrix_To_BigData. Matrix → DuckDB.',
        'example': (
            'm = OpenCSV("small.csv")\n'
            'bd = ToBigData(m)\n'
            'print(type(bd))   # duckdb'
        ),
    },
}


EN = {
    'ToMatrix': {
        'signature': 'ToMatrix(data [, limit])',
        'description': (
            'Convert DuckDBTable to MatrExMatrix (into RAM).\n'
            '  • no limit — all rows\n'
            '  • with limit — only first N rows'
        ),
        'example': (
            'm = OpenCSV("big.csv", BigData)\n'
            'm = ToMatrix(m)                    # → Matrix\n'
            'm = ToMatrix(m, 100000)            # only 100k rows'
        ),
    },
    'Convert_BigData_To_Matrix': {
        'signature': 'Convert_BigData_To_Matrix(data [, limit])',
        'description': 'Synonym for ToMatrix. DuckDB → Matrix.',
        'example': 'm = Convert_BigData_To_Matrix(m)',
    },
    'Convert_Matrix_To_BigData': {
        'signature': 'Convert_Matrix_To_BigData(data)',
        'description': (
            'Convert MatrExMatrix to DuckDBTable (BigData).\n'
            'Works only with 2D matrices.'
        ),
        'example': (
            'm = ["A", "B"; 1, 2]\n'
            'bd = Convert_Matrix_To_BigData(m)\n'
            'print(type(bd))   # duckdb'
        ),
    },
    'ToBigData': {
        'signature': 'ToBigData(data)',
        'description': 'Synonym for Convert_Matrix_To_BigData. Matrix → DuckDB.',
        'example': (
            'm = OpenCSV("small.csv")\n'
            'bd = ToBigData(m)\n'
            'print(type(bd))   # duckdb'
        ),
    },
}