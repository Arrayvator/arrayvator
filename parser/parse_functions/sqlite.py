# parser/parse_functions/sqlite.py
"""
Парсинг SQLite-функций:
    OpenSQLite("path.db", "table" [, where] [, order_by])
    QuerySQLite("path.db", "SELECT ...")
    SaveSQLite(data, "path.db", "table" [, overwrite])
    OpenSQLiteShow()
    SaveSQLiteShow(data)
"""

from ast_nodes import (
    OpenSQLiteNode,
    QuerySQLiteNode,
    SaveSQLiteNode,
    OpenSQLiteShowNode,
    SaveSQLiteShowNode,
)


def parse_sqlite(self, token_type):
    """Парсинг SQLite-функций"""
    self.expect('LPAREN')

    if token_type == 'OPENSQLITE':
        file_path = self.parse_expression()
        self.expect('COMMA')
        table_name = self.parse_expression()

        where = None
        order_by = None
        if self.check('COMMA'):
            self.expect('COMMA')
            where = self.parse_expression()
            if self.check('COMMA'):
                self.expect('COMMA')
                order_by = self.parse_expression()

        self.expect('RPAREN')
        return OpenSQLiteNode(file_path, table_name, where, order_by)

    elif token_type == 'QUERYSQLITE':
        file_path = self.parse_expression()
        self.expect('COMMA')
        query = self.parse_expression()
        self.expect('RPAREN')
        return QuerySQLiteNode(file_path, query)

    elif token_type == 'SAVESQLITE':
        data = self.parse_expression()
        self.expect('COMMA')
        file_path = self.parse_expression()
        self.expect('COMMA')
        table_name = self.parse_expression()

        overwrite = None
        if self.check('COMMA'):
            self.expect('COMMA')
            overwrite = self.parse_expression()

        self.expect('RPAREN')
        return SaveSQLiteNode(data, file_path, table_name, overwrite)

    elif token_type == 'OPENSQLITESHOW':
        self.expect('RPAREN')
        return OpenSQLiteShowNode()

    elif token_type == 'SAVESQLITESHOW':
        data = self.parse_expression()
        self.expect('RPAREN')
        return SaveSQLiteShowNode(data)