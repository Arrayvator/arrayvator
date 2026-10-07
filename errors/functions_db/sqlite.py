# errors/functions_db/sqlite.py
"""
База ошибок для функций SQLite:
    OpenSQLite, SaveSQLite, QuerySQLite,
    OpenSQLiteShow, SaveSQLiteShow.

СИНТАКСИС:
    OpenSQLite("file.db", "table" [, "WHERE"] [, "ORDER BY"])
    QuerySQLite("file.db", "SELECT ...")
    SaveSQLite(данные, "file.db", "table" [, overwrite])
    OpenSQLiteShow()
    SaveSQLiteShow(данные)

ПРАВИЛА:
    - WHERE и ORDER BY — строки в кавычках.
    - SaveSQLite спрашивает про перезапись (диалог).
    - overwrite — ключевое слово, чтобы перезаписать без вопроса.
"""


RU = {
    # ============================================================
    # OPEN SQLITE
    # ============================================================
    'OpenSQLite': {
        'name': 'OpenSQLite',
        'category': 'sqlite',
        'signature': 'OpenSQLite("file.db", "table" [, "WHERE"] [, "ORDER BY"])',
        'description': (
            'Открывает таблицу из SQLite-базы.\n'
            '  • path  — путь к .db\n'
            '  • table — имя таблицы\n'
            '  • WHERE — условие (опц., строка в кавычках)\n'
            '  • ORDER BY — сортировка (опц., строка в кавычках)\n'
            '  • Возвращает матрицу с заголовком.'
        ),
        'examples': [
            'm = OpenSQLite("mydb.db", "users")',
            'm = OpenSQLite("mydb.db", "users", "age > 25")',
            'm = OpenSQLite("mydb.db", "users", "age > 25", "name ASC")',
        ],
        'errors': {
            'OPENSQLITE_BAD_SYNTAX': {
                'message': (
                    "OpenSQLite: неверный синтаксис.\n"
                    "  Нужны путь и имя таблицы."
                ),
                'wrong': 'OpenSQLite("mydb.db")',
                'right': 'OpenSQLite("mydb.db", "users")',
                'explanation': (
                    "OpenSQLite принимает 2–4 аргумента:\n"
                    "  1. \"file.db\" — путь к базе\n"
                    "  2. \"table\"   — имя таблицы\n"
                    "  3. \"WHERE\"   — условие (опц.)\n"
                    "  4. \"ORDER BY\" — сортировка (опц.)\n"
                    "\n"
                    "Неправильно:\n"
                    "     OpenSQLite(\"mydb.db\")\n"
                    "\n"
                    "Правильно:\n"
                    "     OpenSQLite(\"mydb.db\", \"users\")"
                ),
                'variants': [
                    'm = OpenSQLite("mydb.db", "users")',
                    'm = OpenSQLite("mydb.db", "users", "age > 25")',
                ],
            },
            'SQLITE_FILE_NOT_FOUND': {
                'message': (
                    "OpenSQLite: файл базы данных не найден."
                ),
                'wrong': 'm = OpenSQLite("no_such.db", "users")',
                'right': 'm = OpenSQLite("mydb.db", "users")',
                'explanation': (
                    "Файл базы должен существовать.\n"
                    "\n"
                    "Проверьте:\n"
                    "  • путь к файлу\n"
                    "  • имя файла (.db, .sqlite, .sqlite3)\n"
                    "  • права доступа\n"
                    "\n"
                    "Правильно:\n"
                    "     OpenSQLite(\"C:\\\\data\\\\mydb.db\", \"users\")"
                ),
                'variants': [
                    'm = OpenSQLite("mydb.db", "users")',
                    'm = OpenSQLite("C:\\data\\mydb.db", "users")',
                ],
            },
            'SQLITE_TABLE_NOT_FOUND': {
                'message': (
                    "OpenSQLite: таблица не найдена в базе."
                ),
                'wrong': 'm = OpenSQLite("mydb.db", "no_such_table")',
                'right': 'm = OpenSQLite("mydb.db", "users")',
                'explanation': (
                    "Проверьте имя таблицы.\n"
                    "\n"
                    "Список таблиц:\n"
                    "     m = OpenSQLiteShow()   # диалог выбора таблицы"
                ),
                'variants': [
                    'm = OpenSQLite("mydb.db", "users")',
                    'm = OpenSQLiteShow()',
                ],
            },
            'SQLITE_BAD_WHERE': {
                'message': (
                    "OpenSQLite: WHERE должен быть строкой в кавычках."
                ),
                'wrong': 'OpenSQLite("mydb.db", "users", age > 25)',
                'right': 'OpenSQLite("mydb.db", "users", "age > 25")',
                'explanation': (
                    "WHERE — СТРОКА В КАВЫЧКАХ:\n"
                    "     OpenSQLite(\"mydb.db\", \"users\", \"age > 25\")\n"
                    "     OpenSQLite(\"mydb.db\", \"users\", \"dept = 'IT'\")\n"
                    "\n"
                    "Неправильно:\n"
                    "     OpenSQLite(\"mydb.db\", \"users\", age > 25)\n"
                    "\n"
                    "Правильно:\n"
                    "     OpenSQLite(\"mydb.db\", \"users\", \"age > 25\")"
                ),
                'variants': [
                    'm = OpenSQLite("mydb.db", "users", "age > 25")',
                    'm = OpenSQLite("mydb.db", "users", "dept = \'IT\'")',
                ],
            },
            'SQLITE_BAD_ORDER': {
                'message': (
                    "OpenSQLite: ORDER BY должен быть строкой в кавычках."
                ),
                'wrong': 'OpenSQLite("mydb.db", "users", "age > 25", name ASC)',
                'right': 'OpenSQLite("mydb.db", "users", "age > 25", "name ASC")',
                'explanation': (
                    "ORDER BY — СТРОКА В КАВЫЧКАХ:\n"
                    "     OpenSQLite(..., \"age > 25\", \"name ASC\")\n"
                    "     OpenSQLite(..., \"age > 25\", \"name DESC\")\n"
                    "\n"
                    "Правильно:\n"
                    "     OpenSQLite(\"mydb.db\", \"users\", \"age > 25\", \"name ASC\")"
                ),
                'variants': [
                    'm = OpenSQLite("mydb.db", "users", "age > 25", "name ASC")',
                    'm = OpenSQLite("mydb.db", "users", "age > 25", "name DESC")',
                ],
            },
        },
    },

    # ============================================================
    # QUERY SQLITE
    # ============================================================
    'QuerySQLite': {
        'name': 'QuerySQLite',
        'category': 'sqlite',
        'signature': 'QuerySQLite("file.db", "SELECT ...")',
        'description': (
            'Выполняет произвольный SQL-запрос.\n'
            '  • Возвращает матрицу с заголовком.\n'
            '  • Любой SELECT-запрос.\n'
            '  • Для сложных запросов: JOIN, GROUP BY, WHERE, ...'
        ),
        'examples': [
            'm = QuerySQLite("mydb.db", "SELECT * FROM users")',
            'm = QuerySQLite("mydb.db", "SELECT dept, COUNT(*) FROM users GROUP BY dept")',
        ],
        'errors': {
            'QUERYSQLITE_BAD_SYNTAX': {
                'message': (
                    "QuerySQLite: неверный синтаксис.\n"
                    "  Нужны путь к базе и SQL-запрос."
                ),
                'wrong': 'QuerySQLite("mydb.db")',
                'right': 'QuerySQLite("mydb.db", "SELECT * FROM users")',
                'explanation': (
                    "QuerySQLite принимает ДВА аргумента:\n"
                    "  1. \"file.db\" — путь к базе\n"
                    "  2. \"SELECT ...\" — SQL-запрос (строка)\n"
                    "\n"
                    "Правильно:\n"
                    "     QuerySQLite(\"mydb.db\", \"SELECT * FROM users\")"
                ),
                'variants': [
                    'm = QuerySQLite("mydb.db", "SELECT * FROM users")',
                    'm = QuerySQLite("mydb.db", "SELECT dept, COUNT(*) FROM users GROUP BY dept")',
                ],
            },
            'SQLITE_FILE_NOT_FOUND': {
                'message': (
                    "QuerySQLite: файл базы данных не найден."
                ),
                'wrong': 'QuerySQLite("no_such.db", "SELECT * FROM users")',
                'right': 'QuerySQLite("mydb.db", "SELECT * FROM users")',
                'explanation': (
                    "Файл базы должен существовать.\n"
                    "\n"
                    "Правильно:\n"
                    "     QuerySQLite(\"mydb.db\", \"SELECT * FROM users\")"
                ),
                'variants': [
                    'm = QuerySQLite("mydb.db", "SELECT * FROM users")',
                ],
            },
            'SQLITE_BAD_QUERY': {
                'message': (
                    "QuerySQLite: SQL-запрос должен быть строкой в кавычках."
                ),
                'wrong': 'QuerySQLite("mydb.db", SELECT * FROM users)',
                'right': 'QuerySQLite("mydb.db", "SELECT * FROM users")',
                'explanation': (
                    "Запрос — СТРОКА В КАВЫЧКАХ:\n"
                    "     QuerySQLite(\"mydb.db\", \"SELECT * FROM users\")\n"
                    "\n"
                    "Неправильно:\n"
                    "     QuerySQLite(\"mydb.db\", SELECT * FROM users)\n"
                    "\n"
                    "Правильно:\n"
                    "     QuerySQLite(\"mydb.db\", \"SELECT * FROM users\")"
                ),
                'variants': [
                    'm = QuerySQLite("mydb.db", "SELECT * FROM users")',
                    'm = QuerySQLite("mydb.db", "SELECT id, name FROM users WHERE age > 25")',
                ],
            },
            'SQLITE_QUERY_ERROR': {
                'message': (
                    "QuerySQLite: ошибка выполнения SQL-запроса."
                ),
                'wrong': 'QuerySQLite("mydb.db", "SELECT * FROM no_such_table")',
                'right': 'QuerySQLite("mydb.db", "SELECT * FROM users")',
                'explanation': (
                    "Проверьте SQL-запрос:\n"
                    "  • имя таблицы\n"
                    "  • имена столбцов\n"
                    "  • синтаксис SELECT\n"
                    "\n"
                    "Проверить таблицы:\n"
                    "     m = OpenSQLiteShow()"
                ),
                'variants': [
                    'm = QuerySQLite("mydb.db", "SELECT * FROM users")',
                ],
            },
        },
    },

    # ============================================================
    # SAVE SQLITE
    # ============================================================
    'SaveSQLite': {
        'name': 'SaveSQLite',
        'category': 'sqlite',
        'signature': 'SaveSQLite(данные, "file.db", "table" [, overwrite])',
        'description': (
            'Сохраняет матрицу как таблицу SQLite.\n'
            '  • Если таблица уже есть — спрашивает про перезапись.\n'
            '  • overwrite — перезаписать без вопроса.\n'
            '  • Типы столбцов определяются автоматически\n'
            '    (INTEGER, REAL, TEXT).'
        ),
        'examples': [
            'SaveSQLite(m, "mydb.db", "users")',
            'SaveSQLite(m, "mydb.db", "users", overwrite)',
        ],
        'errors': {
            'SAVESQLITE_BAD_SYNTAX': {
                'message': (
                    "SaveSQLite: неверный синтаксис.\n"
                    "  Нужны данные, путь и имя таблицы."
                ),
                'wrong': 'SaveSQLite(m, "mydb.db")',
                'right': 'SaveSQLite(m, "mydb.db", "users")',
                'explanation': (
                    "SaveSQLite принимает 3 или 4 аргумента:\n"
                    "  1. данные — матрица\n"
                    "  2. \"file.db\" — путь к базе\n"
                    "  3. \"table\" — имя таблицы\n"
                    "  4. overwrite — перезаписать без вопроса (опц.)\n"
                    "\n"
                    "Неправильно:\n"
                    "     SaveSQLite(m, \"mydb.db\")\n"
                    "\n"
                    "Правильно:\n"
                    "     SaveSQLite(m, \"mydb.db\", \"users\")\n"
                    "     SaveSQLite(m, \"mydb.db\", \"users\", overwrite)"
                ),
                'variants': [
                    'SaveSQLite(m, "mydb.db", "users")',
                    'SaveSQLite(m, "mydb.db", "users", overwrite)',
                ],
            },
            'SQLITE_NEED_TABLE_NAME': {
                'message': (
                    "SaveSQLite: не указано имя таблицы."
                ),
                'wrong': 'SaveSQLite(m, "mydb.db", "")',
                'right': 'SaveSQLite(m, "mydb.db", "users")',
                'explanation': (
                    "Имя таблицы — строка в кавычках:\n"
                    "     SaveSQLite(m, \"mydb.db\", \"users\")\n"
                    "     SaveSQLite(m, \"mydb.db\", \"employees_2026\")\n"
                    "\n"
                    "Правильно:\n"
                    "     SaveSQLite(m, \"mydb.db\", \"users\")"
                ),
                'variants': [
                    'SaveSQLite(m, "mydb.db", "users")',
                    'SaveSQLite(m, "mydb.db", "employees_2026")',
                ],
            },
            'SQLITE_TABLE_EXISTS': {
                'message': (
                    "SaveSQLite: таблица уже существует.\n"
                    "  Используйте overwrite для перезаписи."
                ),
                'wrong': 'SaveSQLite(m, "mydb.db", "users")',
                'right': 'SaveSQLite(m, "mydb.db", "users", overwrite)',
                'explanation': (
                    "Если таблица уже есть — нужно явно разрешить перезапись.\n"
                    "\n"
                    "Вариант 1 — с overwrite:\n"
                    "     SaveSQLite(m, \"mydb.db\", \"users\", overwrite)\n"
                    "\n"
                    "Вариант 2 — другое имя таблицы:\n"
                    "     SaveSQLite(m, \"mydb.db\", \"users_new\")"
                ),
                'variants': [
                    'SaveSQLite(m, "mydb.db", "users", overwrite)',
                    'SaveSQLite(m, "mydb.db", "users_new")',
                ],
            },
            'SQLITE_SAVE_ERROR': {
                'message': (
                    "SaveSQLite: не удалось сохранить.\n"
                    "  Проверьте путь и права на запись."
                ),
                'wrong': 'SaveSQLite(m, "C:\\\\no_folder\\\\out.db", "users")',
                'right': 'SaveSQLite(m, "out.db", "users")',
                'explanation': (
                    "Возможные причины:\n"
                    "  • папка не существует\n"
                    "  • нет прав на запись\n"
                    "  • файл занят другим приложением\n"
                    "\n"
                    "Правильно:\n"
                    "     SaveSQLite(m, \"mydb.db\", \"users\")"
                ),
                'variants': [
                    'SaveSQLite(m, "mydb.db", "users")',
                    'SaveSQLite(m, "C:\\data\\mydb.db", "users")',
                ],
            },
        },
    },

    # ============================================================
    # OPEN SQLITE SHOW
    # ============================================================
    'OpenSQLiteShow': {
        'name': 'OpenSQLiteShow',
        'category': 'sqlite',
        'signature': 'OpenSQLiteShow()',
        'description': (
            'Диалог выбора SQLite-базы и таблицы.\n'
            '  • Аргументов НЕТ.\n'
            '  • Открывает проводник + список таблиц.'
        ),
        'examples': [
            'm = OpenSQLiteShow()',
        ],
        'errors': {
            'OPENSQLITESHOW_BAD_SYNTAX': {
                'message': (
                    "OpenSQLiteShow: аргументы не нужны.\n"
                    "  Он сам открывает диалог."
                ),
                'wrong': 'OpenSQLiteShow("mydb.db")',
                'right': 'OpenSQLiteShow()',
                'explanation': (
                    "OpenSQLiteShow сам открывает диалог выбора файла\n"
                    "и таблицы. Ничего передавать не нужно.\n"
                    "\n"
                    "Неправильно:\n"
                    "     OpenSQLiteShow(\"mydb.db\")\n"
                    "\n"
                    "Правильно:\n"
                    "     m = OpenSQLiteShow()"
                ),
                'variants': [
                    'm = OpenSQLiteShow()',
                ],
            },
        },
    },

    # ============================================================
    # SAVE SQLITE SHOW
    # ============================================================
    'SaveSQLiteShow': {
        'name': 'SaveSQLiteShow',
        'category': 'sqlite',
        'signature': 'SaveSQLiteShow(данные)',
        'description': (
            'Диалог сохранения в SQLite.\n'
            '  • Спрашивает путь к .db и имя таблицы.'
        ),
        'examples': [
            'SaveSQLiteShow(m)',
        ],
        'errors': {
            'SAVESQLITESHOW_BAD_SYNTAX': {
                'message': (
                    "SaveSQLiteShow: неверный синтаксис.\n"
                    "  Нужны данные."
                ),
                'wrong': 'SaveSQLiteShow()',
                'right': 'SaveSQLiteShow(m)',
                'explanation': (
                    "SaveSQLiteShow принимает ОДИН аргумент — данные:\n"
                    "     SaveSQLiteShow(m)\n"
                    "\n"
                    "Путь и имя таблицы спрашивает сам."
                ),
                'variants': [
                    'SaveSQLiteShow(m)',
                ],
            },
            'SQLITE_SAVE_ERROR': {
                'message': (
                    "SaveSQLiteShow: не удалось сохранить.\n"
                    "  Проверьте путь и права на запись."
                ),
                'wrong': 'SaveSQLiteShow(m)   # папка недоступна',
                'right': 'SaveSQLiteShow(m)   # папка доступна',
                'explanation': (
                    "Возможные причины:\n"
                    "  • папка не существует\n"
                    "  • нет прав на запись\n"
                    "  • файл занят другим приложением"
                ),
                'variants': [
                    'SaveSQLiteShow(m)',
                ],
            },
        },
    },
}


EN = {
    # ============================================================
    # OPEN SQLITE
    # ============================================================
    'OpenSQLite': {
        'name': 'OpenSQLite',
        'category': 'sqlite',
        'signature': 'OpenSQLite("file.db", "table" [, "WHERE"] [, "ORDER BY"])',
        'description': (
            'Opens a table from a SQLite database.\n'
            '  • path  — path to .db\n'
            '  • table — table name\n'
            '  • WHERE — condition (optional, quoted string)\n'
            '  • ORDER BY — sorting (optional, quoted string)\n'
            '  • Returns a matrix with a header.'
        ),
        'examples': [
            'm = OpenSQLite("mydb.db", "users")',
            'm = OpenSQLite("mydb.db", "users", "age > 25")',
            'm = OpenSQLite("mydb.db", "users", "age > 25", "name ASC")',
        ],
        'errors': {
            'OPENSQLITE_BAD_SYNTAX': {
                'message': (
                    "OpenSQLite: invalid syntax.\n"
                    "  Need a path and a table name."
                ),
                'wrong': 'OpenSQLite("mydb.db")',
                'right': 'OpenSQLite("mydb.db", "users")',
                'explanation': (
                    "OpenSQLite takes 2–4 arguments:\n"
                    "  1. \"file.db\" — path to DB\n"
                    "  2. \"table\"   — table name\n"
                    "  3. \"WHERE\"   — condition (optional)\n"
                    "  4. \"ORDER BY\" — sorting (optional)\n"
                    "\n"
                    "Incorrect:\n"
                    "     OpenSQLite(\"mydb.db\")\n"
                    "\n"
                    "Correct:\n"
                    "     OpenSQLite(\"mydb.db\", \"users\")"
                ),
                'variants': [
                    'm = OpenSQLite("mydb.db", "users")',
                    'm = OpenSQLite("mydb.db", "users", "age > 25")',
                ],
            },
            'SQLITE_FILE_NOT_FOUND': {
                'message': (
                    "OpenSQLite: database file not found."
                ),
                'wrong': 'm = OpenSQLite("no_such.db", "users")',
                'right': 'm = OpenSQLite("mydb.db", "users")',
                'explanation': (
                    "The database file must exist.\n"
                    "\n"
                    "Check:\n"
                    "  • path to the file\n"
                    "  • file name (.db, .sqlite, .sqlite3)\n"
                    "  • permissions\n"
                    "\n"
                    "Correct:\n"
                    "     OpenSQLite(\"C:\\\\data\\\\mydb.db\", \"users\")"
                ),
                'variants': [
                    'm = OpenSQLite("mydb.db", "users")',
                    'm = OpenSQLite("C:\\data\\mydb.db", "users")',
                ],
            },
            'SQLITE_TABLE_NOT_FOUND': {
                'message': (
                    "OpenSQLite: table not found in the database."
                ),
                'wrong': 'm = OpenSQLite("mydb.db", "no_such_table")',
                'right': 'm = OpenSQLite("mydb.db", "users")',
                'explanation': (
                    "Check the table name.\n"
                    "\n"
                    "List tables:\n"
                    "     m = OpenSQLiteShow()   # table selection dialog"
                ),
                'variants': [
                    'm = OpenSQLite("mydb.db", "users")',
                    'm = OpenSQLiteShow()',
                ],
            },
            'SQLITE_BAD_WHERE': {
                'message': (
                    "OpenSQLite: WHERE must be a quoted string."
                ),
                'wrong': 'OpenSQLite("mydb.db", "users", age > 25)',
                'right': 'OpenSQLite("mydb.db", "users", "age > 25")',
                'explanation': (
                    "WHERE — a QUOTED STRING:\n"
                    "     OpenSQLite(\"mydb.db\", \"users\", \"age > 25\")\n"
                    "     OpenSQLite(\"mydb.db\", \"users\", \"dept = 'IT'\")\n"
                    "\n"
                    "Correct:\n"
                    "     OpenSQLite(\"mydb.db\", \"users\", \"age > 25\")"
                ),
                'variants': [
                    'm = OpenSQLite("mydb.db", "users", "age > 25")',
                    'm = OpenSQLite("mydb.db", "users", "dept = \'IT\'")',
                ],
            },
            'SQLITE_BAD_ORDER': {
                'message': (
                    "OpenSQLite: ORDER BY must be a quoted string."
                ),
                'wrong': 'OpenSQLite("mydb.db", "users", "age > 25", name ASC)',
                'right': 'OpenSQLite("mydb.db", "users", "age > 25", "name ASC")',
                'explanation': (
                    "ORDER BY — a QUOTED STRING:\n"
                    "     OpenSQLite(..., \"age > 25\", \"name ASC\")\n"
                    "     OpenSQLite(..., \"age > 25\", \"name DESC\")\n"
                    "\n"
                    "Correct:\n"
                    "     OpenSQLite(\"mydb.db\", \"users\", \"age > 25\", \"name ASC\")"
                ),
                'variants': [
                    'm = OpenSQLite("mydb.db", "users", "age > 25", "name ASC")',
                    'm = OpenSQLite("mydb.db", "users", "age > 25", "name DESC")',
                ],
            },
        },
    },

    # ============================================================
    # QUERY SQLITE
    # ============================================================
    'QuerySQLite': {
        'name': 'QuerySQLite',
        'category': 'sqlite',
        'signature': 'QuerySQLite("file.db", "SELECT ...")',
        'description': (
            'Executes an arbitrary SQL query.\n'
            '  • Returns a matrix with a header.\n'
            '  • Any SELECT query.\n'
            '  • For complex queries: JOIN, GROUP BY, WHERE, ...'
        ),
        'examples': [
            'm = QuerySQLite("mydb.db", "SELECT * FROM users")',
            'm = QuerySQLite("mydb.db", "SELECT dept, COUNT(*) FROM users GROUP BY dept")',
        ],
        'errors': {
            'QUERYSQLITE_BAD_SYNTAX': {
                'message': (
                    "QuerySQLite: invalid syntax.\n"
                    "  Need a DB path and a SQL query."
                ),
                'wrong': 'QuerySQLite("mydb.db")',
                'right': 'QuerySQLite("mydb.db", "SELECT * FROM users")',
                'explanation': (
                    "QuerySQLite takes TWO arguments:\n"
                    "  1. \"file.db\" — DB path\n"
                    "  2. \"SELECT ...\" — SQL query (string)\n"
                    "\n"
                    "Correct:\n"
                    "     QuerySQLite(\"mydb.db\", \"SELECT * FROM users\")"
                ),
                'variants': [
                    'm = QuerySQLite("mydb.db", "SELECT * FROM users")',
                    'm = QuerySQLite("mydb.db", "SELECT dept, COUNT(*) FROM users GROUP BY dept")',
                ],
            },
            'SQLITE_FILE_NOT_FOUND': {
                'message': (
                    "QuerySQLite: database file not found."
                ),
                'wrong': 'QuerySQLite("no_such.db", "SELECT * FROM users")',
                'right': 'QuerySQLite("mydb.db", "SELECT * FROM users")',
                'explanation': (
                    "The database file must exist.\n"
                    "\n"
                    "Correct:\n"
                    "     QuerySQLite(\"mydb.db\", \"SELECT * FROM users\")"
                ),
                'variants': [
                    'm = QuerySQLite("mydb.db", "SELECT * FROM users")',
                ],
            },
            'SQLITE_BAD_QUERY': {
                'message': (
                    "QuerySQLite: SQL query must be a quoted string."
                ),
                'wrong': 'QuerySQLite("mydb.db", SELECT * FROM users)',
                'right': 'QuerySQLite("mydb.db", "SELECT * FROM users")',
                'explanation': (
                    "Query — a QUOTED STRING:\n"
                    "     QuerySQLite(\"mydb.db\", \"SELECT * FROM users\")\n"
                    "\n"
                    "Correct:\n"
                    "     QuerySQLite(\"mydb.db\", \"SELECT * FROM users\")"
                ),
                'variants': [
                    'm = QuerySQLite("mydb.db", "SELECT * FROM users")',
                    'm = QuerySQLite("mydb.db", "SELECT id, name FROM users WHERE age > 25")',
                ],
            },
            'SQLITE_QUERY_ERROR': {
                'message': (
                    "QuerySQLite: SQL query execution error."
                ),
                'wrong': 'QuerySQLite("mydb.db", "SELECT * FROM no_such_table")',
                'right': 'QuerySQLite("mydb.db", "SELECT * FROM users")',
                'explanation': (
                    "Check the SQL query:\n"
                    "  • table name\n"
                    "  • column names\n"
                    "  • SELECT syntax\n"
                    "\n"
                    "Check tables:\n"
                    "     m = OpenSQLiteShow()"
                ),
                'variants': [
                    'm = QuerySQLite("mydb.db", "SELECT * FROM users")',
                ],
            },
        },
    },

    # ============================================================
    # SAVE SQLITE
    # ============================================================
    'SaveSQLite': {
        'name': 'SaveSQLite',
        'category': 'sqlite',
        'signature': 'SaveSQLite(data, "file.db", "table" [, overwrite])',
        'description': (
            'Saves a matrix as a SQLite table.\n'
            '  • If the table exists — asks about overwrite.\n'
            '  • overwrite — overwrite without asking.\n'
            '  • Column types are auto-detected\n'
            '    (INTEGER, REAL, TEXT).'
        ),
        'examples': [
            'SaveSQLite(m, "mydb.db", "users")',
            'SaveSQLite(m, "mydb.db", "users", overwrite)',
        ],
        'errors': {
            'SAVESQLITE_BAD_SYNTAX': {
                'message': (
                    "SaveSQLite: invalid syntax.\n"
                    "  Need data, path, and table name."
                ),
                'wrong': 'SaveSQLite(m, "mydb.db")',
                'right': 'SaveSQLite(m, "mydb.db", "users")',
                'explanation': (
                    "SaveSQLite takes 3 or 4 arguments:\n"
                    "  1. data — matrix\n"
                    "  2. \"file.db\" — DB path\n"
                    "  3. \"table\" — table name\n"
                    "  4. overwrite — overwrite without asking (optional)\n"
                    "\n"
                    "Correct:\n"
                    "     SaveSQLite(m, \"mydb.db\", \"users\")\n"
                    "     SaveSQLite(m, \"mydb.db\", \"users\", overwrite)"
                ),
                'variants': [
                    'SaveSQLite(m, "mydb.db", "users")',
                    'SaveSQLite(m, "mydb.db", "users", overwrite)',
                ],
            },
            'SQLITE_NEED_TABLE_NAME': {
                'message': (
                    "SaveSQLite: table name is missing."
                ),
                'wrong': 'SaveSQLite(m, "mydb.db", "")',
                'right': 'SaveSQLite(m, "mydb.db", "users")',
                'explanation': (
                    "Table name — a quoted string:\n"
                    "     SaveSQLite(m, \"mydb.db\", \"users\")\n"
                    "     SaveSQLite(m, \"mydb.db\", \"employees_2026\")\n"
                    "\n"
                    "Correct:\n"
                    "     SaveSQLite(m, \"mydb.db\", \"users\")"
                ),
                'variants': [
                    'SaveSQLite(m, "mydb.db", "users")',
                    'SaveSQLite(m, "mydb.db", "employees_2026")',
                ],
            },
            'SQLITE_TABLE_EXISTS': {
                'message': (
                    "SaveSQLite: table already exists.\n"
                    "  Use overwrite to replace it."
                ),
                'wrong': 'SaveSQLite(m, "mydb.db", "users")',
                'right': 'SaveSQLite(m, "mydb.db", "users", overwrite)',
                'explanation': (
                    "If the table already exists — overwrite must be explicit.\n"
                    "\n"
                    "Option 1 — with overwrite:\n"
                    "     SaveSQLite(m, \"mydb.db\", \"users\", overwrite)\n"
                    "\n"
                    "Option 2 — different table name:\n"
                    "     SaveSQLite(m, \"mydb.db\", \"users_new\")"
                ),
                'variants': [
                    'SaveSQLite(m, "mydb.db", "users", overwrite)',
                    'SaveSQLite(m, "mydb.db", "users_new")',
                ],
            },
            'SQLITE_SAVE_ERROR': {
                'message': (
                    "SaveSQLite: failed to save.\n"
                    "  Check the path and write permissions."
                ),
                'wrong': 'SaveSQLite(m, "C:\\\\no_folder\\\\out.db", "users")',
                'right': 'SaveSQLite(m, "out.db", "users")',
                'explanation': (
                    "Possible reasons:\n"
                    "  • folder does not exist\n"
                    "  • no write permission\n"
                    "  • file is locked\n"
                    "\n"
                    "Correct:\n"
                    "     SaveSQLite(m, \"mydb.db\", \"users\")"
                ),
                'variants': [
                    'SaveSQLite(m, "mydb.db", "users")',
                    'SaveSQLite(m, "C:\\data\\mydb.db", "users")',
                ],
            },
        },
    },

    # ============================================================
    # OPEN SQLITE SHOW
    # ============================================================
    'OpenSQLiteShow': {
        'name': 'OpenSQLiteShow',
        'category': 'sqlite',
        'signature': 'OpenSQLiteShow()',
        'description': (
            'Dialog for selecting SQLite DB and table.\n'
            '  • NO arguments.\n'
            '  • Opens file dialog + table list.'
        ),
        'examples': [
            'm = OpenSQLiteShow()',
        ],
        'errors': {
            'OPENSQLITESHOW_BAD_SYNTAX': {
                'message': (
                    "OpenSQLiteShow: no arguments needed.\n"
                    "  It opens the dialog itself."
                ),
                'wrong': 'OpenSQLiteShow("mydb.db")',
                'right': 'OpenSQLiteShow()',
                'explanation': (
                    "OpenSQLiteShow itself opens a file dialog\n"
                    "and a table list. Nothing to pass.\n"
                    "\n"
                    "Incorrect:\n"
                    "     OpenSQLiteShow(\"mydb.db\")\n"
                    "\n"
                    "Correct:\n"
                    "     m = OpenSQLiteShow()"
                ),
                'variants': [
                    'm = OpenSQLiteShow()',
                ],
            },
        },
    },

    # ============================================================
    # SAVE SQLITE SHOW
    # ============================================================
    'SaveSQLiteShow': {
        'name': 'SaveSQLiteShow',
        'category': 'sqlite',
        'signature': 'SaveSQLiteShow(data)',
        'description': (
            'Dialog for saving to SQLite.\n'
            '  • Asks for .db path and table name.'
        ),
        'examples': [
            'SaveSQLiteShow(m)',
        ],
        'errors': {
            'SAVESQLITESHOW_BAD_SYNTAX': {
                'message': (
                    "SaveSQLiteShow: invalid syntax.\n"
                    "  Need data."
                ),
                'wrong': 'SaveSQLiteShow()',
                'right': 'SaveSQLiteShow(m)',
                'explanation': (
                    "SaveSQLiteShow takes ONE argument — data:\n"
                    "     SaveSQLiteShow(m)\n"
                    "\n"
                    "Path and table name are asked by the dialog."
                ),
                'variants': [
                    'SaveSQLiteShow(m)',
                ],
            },
            'SQLITE_SAVE_ERROR': {
                'message': (
                    "SaveSQLiteShow: failed to save.\n"
                    "  Check the path and write permissions."
                ),
                'wrong': 'SaveSQLiteShow(m)   # folder is locked',
                'right': 'SaveSQLiteShow(m)   # folder is writable',
                'explanation': (
                    "Possible reasons:\n"
                    "  • folder does not exist\n"
                    "  • no write permission\n"
                    "  • file is locked"
                ),
                'variants': [
                    'SaveSQLiteShow(m)',
                ],
            },
        },
    },
}