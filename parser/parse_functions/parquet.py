# parser/parse_functions/parquet.py
"""
Парсинг Parquet-функций:
    OpenParquet("file.parquet")
    SaveParquet(m, "file.parquet")
"""

from ast_nodes import OpenParquetNode, SaveParquetNode


def parse_parquet(self, token_type):
    """Парсинг Parquet-функций"""
    self.expect('LPAREN')

    if token_type == 'OPENPARQUET':
        file_path = self.parse_expression()
        self.expect('RPAREN')
        return OpenParquetNode(file_path)

    elif token_type == 'SAVEPARQUET':
        data = self.parse_expression()
        self.expect('COMMA')
        file_path = self.parse_expression()
        self.expect('RPAREN')
        return SaveParquetNode(data, file_path)