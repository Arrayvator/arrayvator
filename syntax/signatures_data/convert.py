# syntax/signatures_data/convert.py
"""
Сигнатуры: конвертация Matrix ↔ DuckDB.
"""

SIGNATURES = {
    'tomatrix': {
        'name': 'ToMatrix',
        'category': 'bigdata',
        'args': ['данные (DuckDBTable)', 'limit (опц.)'],
        'examples': [
            'm = ToMatrix(m)',
            'm = ToMatrix(m, 100000)',
        ],
    },

    'convert_bigdata_to_matrix': {
        'name': 'Convert_BigData_To_Matrix',
        'category': 'bigdata',
        'args': ['данные (DuckDBTable)', 'limit (опц.)'],
        'examples': [
            'm = Convert_BigData_To_Matrix(m)',
            'm = Convert_BigData_To_Matrix(m, 100000)',
        ],
    },

    'convert_matrix_to_bigdata': {
        'name': 'Convert_Matrix_To_BigData',
        'category': 'bigdata',
        'args': ['данные (MatrExMatrix, 2D)'],
        'examples': [
            'bd = Convert_Matrix_To_BigData(m)',
        ],
    },

    'tobigdata': {
        'name': 'ToBigData',
        'category': 'bigdata',
        'args': ['данные (MatrExMatrix, 2D)'],
        'examples': [
            'bd = ToBigData(m)',
        ],
    },
}