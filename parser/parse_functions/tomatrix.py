# parser/parse_functions/tomatrix.py
"""
Парсинг функций конвертации:

    ToMatrix(m [, limit])
    Convert_BigData_To_Matrix(m [, limit])
    Convert_Matrix_To_BigData(m)
    ToBigData(m)
"""

from ast_nodes import (
    ToMatrixNode,
    ConvertBigDataToMatrixNode,
    ConvertMatrixToBigDataNode,
    ToBigDataNode,
)


def parse_to_matrix(self):
    """Парсинг ToMatrix (DuckDB → Matrix)"""
    self.expect('LPAREN')

    data = self.parse_expression()

    limit = None
    if self.check('COMMA'):
        self.expect('COMMA')
        limit = self.parse_expression()

    self.expect('RPAREN')
    return ToMatrixNode(data, limit)


def parse_convert_bigdata_to_matrix(self):
    """Парсинг Convert_BigData_To_Matrix (синоним ToMatrix)"""
    self.expect('LPAREN')

    data = self.parse_expression()

    limit = None
    if self.check('COMMA'):
        self.expect('COMMA')
        limit = self.parse_expression()

    self.expect('RPAREN')
    return ConvertBigDataToMatrixNode(data, limit)


def parse_convert_matrix_to_bigdata(self):
    """Парсинг Convert_Matrix_To_BigData (Matrix → DuckDB)"""
    self.expect('LPAREN')

    data = self.parse_expression()

    self.expect('RPAREN')
    return ConvertMatrixToBigDataNode(data)


def parse_tobigdata(self):
    """Парсинг ToBigData (синоним Convert_Matrix_To_BigData)"""
    self.expect('LPAREN')

    data = self.parse_expression()

    self.expect('RPAREN')
    return ToBigDataNode(data)