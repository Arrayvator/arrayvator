# syntax/autocomplete/items_sqlite.py
"""
Описания функций SQLite: OpenSQLite, QuerySQLite, SaveSQLite,
OpenSQLiteShow, SaveSQLiteShow.
"""

RU = {
    'OpenSQLite': {
        'signature': 'OpenSQLite("file.db", "table" [, "WHERE"] [, "ORDER BY"])',
        'description': 'Открыть таблицу из SQLite.',
        'example': 'm = OpenSQLite("mydb.db", "users", "age > 25")',
    },
    'QuerySQLite': {
        'signature': 'QuerySQLite("file.db", "SELECT ...")',
        'description': 'Произвольный SQL-запрос.',
        'example': 'm = QuerySQLite("mydb.db", "SELECT * FROM users")',
    },
    'SaveSQLite': {
        'signature': 'SaveSQLite(данные, "file.db", "table" [, overwrite])',
        'description': 'Сохранить как таблицу SQLite.',
        'example': 'SaveSQLite(m, "mydb.db", "users")',
    },
    'OpenSQLiteShow': {
        'signature': 'OpenSQLiteShow()',
        'description': 'Диалог выбора SQLite БД.',
        'example': 'm = OpenSQLiteShow()',
    },
    'SaveSQLiteShow': {
        'signature': 'SaveSQLiteShow(данные)',
        'description': 'Диалог сохранения в SQLite.',
        'example': 'SaveSQLiteShow(m)',
    },
}


EN = {
    'OpenSQLite': {
        'signature': 'OpenSQLite("file.db", "table" [, "WHERE"] [, "ORDER BY"])',
        'description': 'Open a table from SQLite.',
        'example': 'm = OpenSQLite("mydb.db", "users", "age > 25")',
    },
    'QuerySQLite': {
        'signature': 'QuerySQLite("file.db", "SELECT ...")',
        'description': 'Execute arbitrary SQL query.',
        'example': 'm = QuerySQLite("mydb.db", "SELECT * FROM users")',
    },
    'SaveSQLite': {
        'signature': 'SaveSQLite(data, "file.db", "table" [, overwrite])',
        'description': 'Save as SQLite table.',
        'example': 'SaveSQLite(m, "mydb.db", "users")',
    },
    'OpenSQLiteShow': {
        'signature': 'OpenSQLiteShow()',
        'description': 'Dialog for selecting SQLite DB.',
        'example': 'm = OpenSQLiteShow()',
    },
    'SaveSQLiteShow': {
        'signature': 'SaveSQLiteShow(data)',
        'description': 'Dialog for saving to SQLite.',
        'example': 'SaveSQLiteShow(m)',
    },
}