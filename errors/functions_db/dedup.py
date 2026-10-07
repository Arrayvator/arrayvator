# errors/functions_db/dedup.py
"""
База ошибок для функций работы с дубликатами:
    Unique            — уникальные значения / строки
    CountDistinct     — количество уникальных
    ValueCounts       — частотная таблица
    DeleteDuplicate   — удаление дубликатов (синоним Unique)

СИНТАКСИС:
    Unique(вектор)
    Unique(матрица)
    Unique(матрица[:, "Отдел"])
    Unique(матрица[:, 3])
    Unique(матрица[:, end])

    CountDistinct(вектор)
    CountDistinct(матрица[:, "Отдел"])

    ValueCounts(вектор)
    ValueCounts(матрица[:, "Отдел"])

    DeleteDuplicate(вектор)
    DeleteDuplicate(матрица)
    DeleteDuplicate(матрица[:, "Отдел"])

DUCKDB:
    - Unique(m[:, "X"])   → SELECT * с ROW_NUMBER() OVER PARTITION BY
    - Unique(m)           → SELECT DISTINCT *
    - CountDistinct       → SELECT COUNT(DISTINCT)
    - ValueCounts         → SELECT col, COUNT(*) GROUP BY
    - Диапазоны строк (m[10:end, "X"]) НЕ поддерживаются.
"""


RU = {
    # ============================================================
    # UNIQUE
    # ============================================================
    'Unique': {
        'name': 'Unique',
        'category': 'deduplicate',
        'signature': 'Unique(срез)',
        'description': (
            'Уникальные значения.\n'
            '  • Вектор → уникальные элементы.\n'
            '  • Матрица → уникальные строки.\n'
            '  • Срез столбца → уникальные значения столбца.\n'
            '  • Работает с Matrix и DuckDB.\n'
            '  • Возвращает НОВУЮ матрицу — результат нужно сохранить.'
        ),
        'examples': [
            'r = Unique(v)',
            'r = Unique(m[:, "Отдел"])',
            'm = Unique(m[:, "Отдел"])',
            'r = Unique(m)',
        ],
        'errors': {
            'UNIQUE_BAD_SYNTAX': {
                'message': (
                    "Unique: неверный синтаксис.\n"
                    "  Нужен ровно один аргумент."
                ),
                'wrong': 'Unique()',
                'right': 'Unique(m[:, "Отдел"])',
                'explanation': (
                    "Unique принимает ОДИН аргумент:\n"
                    "     Unique(вектор)\n"
                    "     Unique(матрица)\n"
                    "     Unique(матрица[:, \"X\"])\n"
                    "\n"
                    "Неправильно:\n"
                    "     Unique()\n"
                    "     Unique(m1, m2)\n"
                    "\n"
                    "Правильно:\n"
                    "     Unique(m[:, \"Отдел\"])"
                ),
                'variants': [
                    'r = Unique(m[:, "Отдел"])',
                    'r = Unique(v)',
                    'r = Unique(m)',
                ],
            },
            'UNIQUE_BAD_ARG': {
                'message': (
                    "Unique: работает с векторами и матрицами.\n"
                    "  Получен неподходящий тип."
                ),
                'wrong': 'Unique(42)',
                'right': 'Unique(v)',
                'explanation': (
                    "Unique работает с:\n"
                    "     вектором — Unique(v)\n"
                    "     матрицей — Unique(m)\n"
                    "     срезом — Unique(m[:, \"X\"])\n"
                    "\n"
                    "Неправильно:\n"
                    "     Unique(42)\n"
                    "     Unique(\"text\")\n"
                    "     Unique(None)\n"
                    "\n"
                    "Правильно:\n"
                    "     Unique(v)\n"
                    "     Unique(m[:, \"Отдел\"])"
                ),
                'variants': [
                    'r = Unique(v)',
                    'r = Unique(m)',
                    'r = Unique(m[:, "Отдел"])',
                ],
            },
            'UNIQUE_COLON_SLICE': {
                'message': (
                    "Unique: укажите ОДИН столбец.\n"
                    "  Срез \":\" (все столбцы) не подходит."
                ),
                'wrong': 'r = Unique(m[:, :])',
                'right': 'r = Unique(m[:, "Отдел"])',
                'explanation': (
                    "Unique уникализирует по ОДНОМУ столбцу.\n"
                    "Для всей матрицы — передайте её целиком:\n"
                    "     Unique(m)\n"
                    "\n"
                    "Неправильно:\n"
                    "     Unique(m[:, :])\n"
                    "\n"
                    "Правильно:\n"
                    "     Unique(m)\n"
                    "     Unique(m[:, \"Отдел\"])"
                ),
                'variants': [
                    'r = Unique(m)',
                    'r = Unique(m[:, "Отдел"])',
                ],
            },
            'UNIQUE_DUCKDB_ROW_RANGE': {
                'message': (
                    "Unique: DuckDB не поддерживает диапазоны строк."
                ),
                'wrong': 'r = Unique(bd[2:10, "Отдел"])',
                'right': 'r = Unique(bd[:, "Отдел"])',
                'explanation': (
                    "BigData (DuckDB) — read-only view на файл.\n"
                    "Диапазоны строк на нём не поддерживаются.\n"
                    "\n"
                    "Используйте полный срез:\n"
                    "     Unique(bd[:, \"Отдел\"])\n"
                    "\n"
                    "Если нужен диапазон — сначала отфильтруйте:\n"
                    "     bd2 = filterif(bd[:, \"Год\"] == 2025)\n"
                    "     r = Unique(bd2[:, \"Отдел\"])"
                ),
                'variants': [
                    'r = Unique(bd[:, "Отдел"])',
                    'bd2 = filterif(bd[:, "Год"] == 2025)\nr = Unique(bd2[:, "Отдел"])',
                ],
            },
            'UNIQUE_COLUMN_NOT_FOUND': {
                'message': (
                    "Unique: столбец не найден."
                ),
                'wrong': 'r = Unique(m[:, "НетТакого"])',
                'right': 'r = Unique(m[:, "Отдел"])',
                'explanation': (
                    "Столбец указывается по имени в кавычках\n"
                    "или по номеру.\n"
                    "\n"
                    "Проверьте заголовки:\n"
                    "     print(m[0, :])\n"
                    "\n"
                    "Правильно:\n"
                    "     Unique(m[:, \"Отдел\"])\n"
                    "     Unique(m[:, 3])\n"
                    "     Unique(m[:, end])"
                ),
                'variants': [
                    'r = Unique(m[:, "Отдел"])',
                    'r = Unique(m[:, 3])',
                    'r = Unique(m[:, end])',
                ],
            },
            'UNIQUE_REQUIRES_ASSIGNMENT': {
                'message': (
                    "Unique() возвращает значение — "
                    "результат нужно сохранить."
                ),
                'wrong': 'Unique(m[:, "Отдел"])',
                'right': 'r = Unique(m[:, "Отдел"])',
                'explanation': (
                    "Unique НЕ изменяет исходную матрицу.\n"
                    "Он ВОЗВРАЩАЕТ НОВУЮ.\n"
                    "\n"
                    "Правильно:\n"
                    "  r = Unique(...)      — в новую переменную\n"
                    "  m = Unique(...)      — мутация\n"
                    "  print(Unique(...))   — вывод"
                ),
                'variants': [
                    'r = Unique(m[:, "Отдел"])',
                    'm = Unique(m[:, "Отдел"])',
                    'print(Unique(m[:, "Отдел"]))',
                ],
            },
        },
    },

    # ============================================================
    # COUNT DISTINCT
    # ============================================================
    'CountDistinct': {
        'name': 'CountDistinct',
        'category': 'deduplicate',
        'signature': 'CountDistinct(срез)',
        'description': (
            'Количество уникальных значений.\n'
            '  • Работает с вектором и срезом столбца.\n'
            '  • Работает с Matrix и DuckDB.\n'
            '  • Возвращает СКАЛЯР (число).'
        ),
        'examples': [
            'r = CountDistinct(v)',
            'r = CountDistinct(m[:, "Отдел"])',
        ],
        'errors': {
            'COUNTDISTINCT_BAD_SYNTAX': {
                'message': (
                    "CountDistinct: неверный синтаксис.\n"
                    "  Нужен ровно один аргумент."
                ),
                'wrong': 'CountDistinct()',
                'right': 'CountDistinct(m[:, "Отдел"])',
                'explanation': (
                    "CountDistinct принимает ОДИН аргумент:\n"
                    "     CountDistinct(вектор)\n"
                    "     CountDistinct(матрица[:, \"X\"])\n"
                    "\n"
                    "Неправильно:\n"
                    "     CountDistinct()\n"
                    "\n"
                    "Правильно:\n"
                    "     CountDistinct(m[:, \"Отдел\"])"
                ),
                'variants': [
                    'r = CountDistinct(v)',
                    'r = CountDistinct(m[:, "Отдел"])',
                ],
            },
            'COUNTDISTINCT_COLON_SLICE': {
                'message': (
                    "CountDistinct: укажите ОДИН столбец.\n"
                    "  Срез \":\" (все столбцы) не подходит."
                ),
                'wrong': 'r = CountDistinct(m[:, :])',
                'right': 'r = CountDistinct(m[:, "Отдел"])',
                'explanation': (
                    "CountDistinct считает уникальные значения\n"
                    "в ОДНОМ столбце.\n"
                    "\n"
                    "Неправильно:\n"
                    "     CountDistinct(m[:, :])\n"
                    "     CountDistinct(m)\n"
                    "\n"
                    "Правильно:\n"
                    "     CountDistinct(m[:, \"Отдел\"])"
                ),
                'variants': [
                    'r = CountDistinct(m[:, "Отдел"])',
                    'r = CountDistinct(m[:, 3])',
                ],
            },
            'COUNTDISTINCT_BAD_ARG': {
                'message': (
                    "CountDistinct: работает с векторами и столбцами.\n"
                    "  Получен неподходящий тип."
                ),
                'wrong': 'CountDistinct(42)',
                'right': 'CountDistinct(v)',
                'explanation': (
                    "CountDistinct работает с:\n"
                    "     вектором — CountDistinct(v)\n"
                    "     срезом — CountDistinct(m[:, \"X\"])\n"
                    "\n"
                    "Неправильно:\n"
                    "     CountDistinct(42)\n"
                    "     CountDistinct(\"text\")\n"
                    "\n"
                    "Правильно:\n"
                    "     CountDistinct(v)\n"
                    "     CountDistinct(m[:, \"Отдел\"])"
                ),
                'variants': [
                    'r = CountDistinct(v)',
                    'r = CountDistinct(m[:, "Отдел"])',
                ],
            },
            'COUNTDISTINCT_DUCKDB_ROW_RANGE': {
                'message': (
                    "CountDistinct: DuckDB не поддерживает диапазоны строк."
                ),
                'wrong': 'r = CountDistinct(bd[2:10, "Отдел"])',
                'right': 'r = CountDistinct(bd[:, "Отдел"])',
                'explanation': (
                    "BigData (DuckDB) — read-only view на файл.\n"
                    "Диапазоны строк на нём не поддерживаются.\n"
                    "\n"
                    "Используйте полный срез:\n"
                    "     CountDistinct(bd[:, \"Отдел\"])"
                ),
                'variants': [
                    'r = CountDistinct(bd[:, "Отдел"])',
                ],
            },
            'COUNTDISTINCT_REQUIRES_ASSIGNMENT': {
                'message': (
                    "CountDistinct() возвращает значение — "
                    "результат нужно сохранить."
                ),
                'wrong': 'CountDistinct(m[:, "Отдел"])',
                'right': 'r = CountDistinct(m[:, "Отдел"])',
                'explanation': (
                    "CountDistinct возвращает СКАЛЯР (число).\n"
                    "Без присваивания результат теряется.\n"
                    "\n"
                    "Правильно:\n"
                    "  r = CountDistinct(...)\n"
                    "  print(CountDistinct(...))"
                ),
                'variants': [
                    'r = CountDistinct(m[:, "Отдел"])',
                    'print(CountDistinct(m[:, "Отдел"]))',
                ],
            },
        },
    },

    # ============================================================
    # VALUE COUNTS
    # ============================================================
    'ValueCounts': {
        'name': 'ValueCounts',
        'category': 'deduplicate',
        'signature': 'ValueCounts(срез)',
        'description': (
            'Частотная таблица.\n'
            '  • Возвращает 2 столбца: значение, частота.\n'
            '  • Отсортировано по частоте (убывание).\n'
            '  • Работает с Matrix и DuckDB.'
        ),
        'examples': [
            'r = ValueCounts(v)',
            'r = ValueCounts(m[:, "Отдел"])',
        ],
        'errors': {
            'VALUECOUNTS_BAD_SYNTAX': {
                'message': (
                    "ValueCounts: неверный синтаксис.\n"
                    "  Нужен ровно один аргумент."
                ),
                'wrong': 'ValueCounts()',
                'right': 'ValueCounts(m[:, "Отдел"])',
                'explanation': (
                    "ValueCounts принимает ОДИН аргумент:\n"
                    "     ValueCounts(вектор)\n"
                    "     ValueCounts(матрица[:, \"X\"])\n"
                    "\n"
                    "Правильно:\n"
                    "     ValueCounts(m[:, \"Отдел\"])"
                ),
                'variants': [
                    'r = ValueCounts(v)',
                    'r = ValueCounts(m[:, "Отдел"])',
                ],
            },
            'VALUECOUNTS_COLON_SLICE': {
                'message': (
                    "ValueCounts: укажите ОДИН столбец.\n"
                    "  Срез \":\" (все столбцы) не подходит."
                ),
                'wrong': 'r = ValueCounts(m[:, :])',
                'right': 'r = ValueCounts(m[:, "Отдел"])',
                'explanation': (
                    "ValueCounts считает частоты по ОДНОМУ столбцу.\n"
                    "\n"
                    "Неправильно:\n"
                    "     ValueCounts(m[:, :])\n"
                    "     ValueCounts(m)\n"
                    "\n"
                    "Правильно:\n"
                    "     ValueCounts(m[:, \"Отдел\"])"
                ),
                'variants': [
                    'r = ValueCounts(m[:, "Отдел"])',
                ],
            },
            'VALUECOUNTS_BAD_ARG': {
                'message': (
                    "ValueCounts: работает с векторами и столбцами."
                ),
                'wrong': 'ValueCounts(42)',
                'right': 'ValueCounts(v)',
                'explanation': (
                    "ValueCounts работает с:\n"
                    "     вектором — ValueCounts(v)\n"
                    "     срезом — ValueCounts(m[:, \"X\"])"
                ),
                'variants': [
                    'r = ValueCounts(v)',
                    'r = ValueCounts(m[:, "Отдел"])',
                ],
            },
            'VALUECOUNTS_DUCKDB_ROW_RANGE': {
                'message': (
                    "ValueCounts: DuckDB не поддерживает диапазоны строк."
                ),
                'wrong': 'r = ValueCounts(bd[2:10, "Отдел"])',
                'right': 'r = ValueCounts(bd[:, "Отдел"])',
                'explanation': (
                    "BigData (DuckDB) — read-only view на файл.\n"
                    "Диапазоны строк на нём не поддерживаются.\n"
                    "\n"
                    "Используйте полный срез:\n"
                    "     ValueCounts(bd[:, \"Отдел\"])"
                ),
                'variants': [
                    'r = ValueCounts(bd[:, "Отдел"])',
                ],
            },
            'VALUECOUNTS_REQUIRES_ASSIGNMENT': {
                'message': (
                    "ValueCounts() возвращает значение — "
                    "результат нужно сохранить."
                ),
                'wrong': 'ValueCounts(m[:, "Отдел"])',
                'right': 'r = ValueCounts(m[:, "Отдел"])',
                'explanation': (
                    "ValueCounts НЕ изменяет исходную матрицу.\n"
                    "Он ВОЗВРАЩАЕТ НОВУЮ.\n"
                    "\n"
                    "Правильно:\n"
                    "  r = ValueCounts(...)\n"
                    "  print(ValueCounts(...))"
                ),
                'variants': [
                    'r = ValueCounts(m[:, "Отдел"])',
                    'print(ValueCounts(m[:, "Отдел"]))',
                ],
            },
        },
    },

    # ============================================================
    # DELETE DUPLICATE
    # ============================================================
    'DeleteDuplicate': {
        'name': 'DeleteDuplicate',
        'category': 'deduplicate',
        'signature': 'DeleteDuplicate(срез)',
        'description': (
            'Удаляет дубликаты (синоним Unique).\n'
            '  • Вектор → уникальные элементы.\n'
            '  • Матрица → уникальные строки.\n'
            '  • Возвращает НОВУЮ матрицу.\n'
            '  • Работает с Matrix и DuckDB.'
        ),
        'examples': [
            'r = DeleteDuplicate(v)',
            'r = DeleteDuplicate(m[:, "Отдел"])',
            'm = DeleteDuplicate(m)',
        ],
        'errors': {
            'DELETEDUPLICATE_BAD_SYNTAX': {
                'message': (
                    "DeleteDuplicate: неверный синтаксис.\n"
                    "  Нужен ровно один аргумент."
                ),
                'wrong': 'DeleteDuplicate()',
                'right': 'DeleteDuplicate(m[:, "Отдел"])',
                'explanation': (
                    "DeleteDuplicate принимает ОДИН аргумент:\n"
                    "     DeleteDuplicate(вектор)\n"
                    "     DeleteDuplicate(матрица)\n"
                    "     DeleteDuplicate(матрица[:, \"X\"])\n"
                    "\n"
                    "Правильно:\n"
                    "     DeleteDuplicate(m[:, \"Отдел\"])"
                ),
                'variants': [
                    'r = DeleteDuplicate(v)',
                    'r = DeleteDuplicate(m)',
                    'r = DeleteDuplicate(m[:, "Отдел"])',
                ],
            },
            'DELETEDUPLICATE_COLON_SLICE': {
                'message': (
                    "DeleteDuplicate: укажите ОДИН столбец\n"
                    "или передайте матрицу целиком."
                ),
                'wrong': 'r = DeleteDuplicate(m[:, :])',
                'right': 'r = DeleteDuplicate(m)',
                'explanation': (
                    "Для всей матрицы — передайте её без среза:\n"
                    "     DeleteDuplicate(m)\n"
                    "\n"
                    "Для одного столбца:\n"
                    "     DeleteDuplicate(m[:, \"Отдел\"])\n"
                    "\n"
                    "Неправильно:\n"
                    "     DeleteDuplicate(m[:, :])"
                ),
                'variants': [
                    'r = DeleteDuplicate(m)',
                    'r = DeleteDuplicate(m[:, "Отдел"])',
                ],
            },
            'DELETEDUPLICATE_DUCKDB_ROW_RANGE': {
                'message': (
                    "DeleteDuplicate: DuckDB не поддерживает диапазоны строк."
                ),
                'wrong': 'r = DeleteDuplicate(bd[2:10, "Отдел"])',
                'right': 'r = DeleteDuplicate(bd[:, "Отдел"])',
                'explanation': (
                    "BigData (DuckDB) — read-only view на файл.\n"
                    "Диапазоны строк на нём не поддерживаются.\n"
                    "\n"
                    "Используйте полный срез:\n"
                    "     DeleteDuplicate(bd[:, \"Отдел\"])"
                ),
                'variants': [
                    'r = DeleteDuplicate(bd[:, "Отдел"])',
                ],
            },
            'DELETEDUPLICATE_REQUIRES_ASSIGNMENT': {
                'message': (
                    "DeleteDuplicate() возвращает значение — "
                    "результат нужно сохранить."
                ),
                'wrong': 'DeleteDuplicate(m[:, "Отдел"])',
                'right': 'm = DeleteDuplicate(m[:, "Отдел"])',
                'explanation': (
                    "DeleteDuplicate НЕ изменяет исходную матрицу.\n"
                    "Он ВОЗВРАЩАЕТ НОВУЮ.\n"
                    "\n"
                    "Правильно:\n"
                    "  r = DeleteDuplicate(...)\n"
                    "  m = DeleteDuplicate(...)      — мутация"
                ),
                'variants': [
                    'r = DeleteDuplicate(m[:, "Отдел"])',
                    'm = DeleteDuplicate(m[:, "Отдел"])',
                ],
            },
        },
    },
}


EN = {
    # ============================================================
    # UNIQUE
    # ============================================================
    'Unique': {
        'name': 'Unique',
        'category': 'deduplicate',
        'signature': 'Unique(slice)',
        'description': (
            'Unique values.\n'
            '  • Vector → unique elements.\n'
            '  • Matrix → unique rows.\n'
            '  • Column slice → unique column values.\n'
            '  • Works with Matrix and DuckDB.\n'
            '  • Returns a NEW matrix — save the result.'
        ),
        'examples': [
            'r = Unique(v)',
            'r = Unique(m[:, "Department"])',
            'm = Unique(m[:, "Department"])',
            'r = Unique(m)',
        ],
        'errors': {
            'UNIQUE_BAD_SYNTAX': {
                'message': (
                    "Unique: invalid syntax.\n"
                    "  Exactly one argument is required."
                ),
                'wrong': 'Unique()',
                'right': 'Unique(m[:, "Department"])',
                'explanation': (
                    "Unique takes ONE argument:\n"
                    "     Unique(vector)\n"
                    "     Unique(matrix)\n"
                    "     Unique(matrix[:, \"X\"])\n"
                    "\n"
                    "Incorrect:\n"
                    "     Unique()\n"
                    "     Unique(m1, m2)\n"
                    "\n"
                    "Correct:\n"
                    "     Unique(m[:, \"Department\"])"
                ),
                'variants': [
                    'r = Unique(m[:, "Department"])',
                    'r = Unique(v)',
                    'r = Unique(m)',
                ],
            },
            'UNIQUE_BAD_ARG': {
                'message': (
                    "Unique: works with vectors and matrices.\n"
                    "  Unsupported type given."
                ),
                'wrong': 'Unique(42)',
                'right': 'Unique(v)',
                'explanation': (
                    "Unique works with:\n"
                    "     vector — Unique(v)\n"
                    "     matrix — Unique(m)\n"
                    "     slice — Unique(m[:, \"X\"])\n"
                    "\n"
                    "Incorrect:\n"
                    "     Unique(42)\n"
                    "     Unique(\"text\")\n"
                    "     Unique(None)\n"
                    "\n"
                    "Correct:\n"
                    "     Unique(v)\n"
                    "     Unique(m[:, \"Department\"])"
                ),
                'variants': [
                    'r = Unique(v)',
                    'r = Unique(m)',
                    'r = Unique(m[:, "Department"])',
                ],
            },
            'UNIQUE_COLON_SLICE': {
                'message': (
                    "Unique: specify ONE column.\n"
                    "  Slice ':' (all columns) is not supported."
                ),
                'wrong': 'r = Unique(m[:, :])',
                'right': 'r = Unique(m[:, "Department"])',
                'explanation': (
                    "Unique deduplicates by ONE column.\n"
                    "For the whole matrix — pass it without slice:\n"
                    "     Unique(m)\n"
                    "\n"
                    "Incorrect:\n"
                    "     Unique(m[:, :])\n"
                    "\n"
                    "Correct:\n"
                    "     Unique(m)\n"
                    "     Unique(m[:, \"Department\"])"
                ),
                'variants': [
                    'r = Unique(m)',
                    'r = Unique(m[:, "Department"])',
                ],
            },
            'UNIQUE_DUCKDB_ROW_RANGE': {
                'message': (
                    "Unique: DuckDB does not support row ranges."
                ),
                'wrong': 'r = Unique(bd[2:10, "Department"])',
                'right': 'r = Unique(bd[:, "Department"])',
                'explanation': (
                    "BigData (DuckDB) is a read-only view on a file.\n"
                    "Row ranges are not supported.\n"
                    "\n"
                    "Use a full slice:\n"
                    "     Unique(bd[:, \"Department\"])\n"
                    "\n"
                    "If you need a range — filter first:\n"
                    "     bd2 = filterif(bd[:, \"Year\"] == 2025)\n"
                    "     r = Unique(bd2[:, \"Department\"])"
                ),
                'variants': [
                    'r = Unique(bd[:, "Department"])',
                    'bd2 = filterif(bd[:, "Year"] == 2025)\nr = Unique(bd2[:, "Department"])',
                ],
            },
            'UNIQUE_COLUMN_NOT_FOUND': {
                'message': (
                    "Unique: column not found."
                ),
                'wrong': 'r = Unique(m[:, "NoSuch"])',
                'right': 'r = Unique(m[:, "Department"])',
                'explanation': (
                    "A column is specified by name in quotes\n"
                    "or by number.\n"
                    "\n"
                    "Check headers:\n"
                    "     print(m[0, :])\n"
                    "\n"
                    "Correct:\n"
                    "     Unique(m[:, \"Department\"])\n"
                    "     Unique(m[:, 3])\n"
                    "     Unique(m[:, end])"
                ),
                'variants': [
                    'r = Unique(m[:, "Department"])',
                    'r = Unique(m[:, 3])',
                    'r = Unique(m[:, end])',
                ],
            },
            'UNIQUE_REQUIRES_ASSIGNMENT': {
                'message': (
                    "Unique() returns a value — "
                    "the result must be saved."
                ),
                'wrong': 'Unique(m[:, "Department"])',
                'right': 'r = Unique(m[:, "Department"])',
                'explanation': (
                    "Unique does NOT modify the source matrix.\n"
                    "It RETURNS a NEW one.\n"
                    "\n"
                    "Correct:\n"
                    "  r = Unique(...)      — to a new variable\n"
                    "  m = Unique(...)      — mutation\n"
                    "  print(Unique(...))   — output"
                ),
                'variants': [
                    'r = Unique(m[:, "Department"])',
                    'm = Unique(m[:, "Department"])',
                    'print(Unique(m[:, "Department"]))',
                ],
            },
        },
    },

    # ============================================================
    # COUNT DISTINCT
    # ============================================================
    'CountDistinct': {
        'name': 'CountDistinct',
        'category': 'deduplicate',
        'signature': 'CountDistinct(slice)',
        'description': (
            'Number of unique values.\n'
            '  • Works with vector and column slice.\n'
            '  • Works with Matrix and DuckDB.\n'
            '  • Returns a SCALAR (number).'
        ),
        'examples': [
            'r = CountDistinct(v)',
            'r = CountDistinct(m[:, "Department"])',
        ],
        'errors': {
            'COUNTDISTINCT_BAD_SYNTAX': {
                'message': (
                    "CountDistinct: invalid syntax.\n"
                    "  Exactly one argument is required."
                ),
                'wrong': 'CountDistinct()',
                'right': 'CountDistinct(m[:, "Department"])',
                'explanation': (
                    "CountDistinct takes ONE argument:\n"
                    "     CountDistinct(vector)\n"
                    "     CountDistinct(matrix[:, \"X\"])\n"
                    "\n"
                    "Correct:\n"
                    "     CountDistinct(m[:, \"Department\"])"
                ),
                'variants': [
                    'r = CountDistinct(v)',
                    'r = CountDistinct(m[:, "Department"])',
                ],
            },
            'COUNTDISTINCT_COLON_SLICE': {
                'message': (
                    "CountDistinct: specify ONE column.\n"
                    "  Slice ':' (all columns) is not supported."
                ),
                'wrong': 'r = CountDistinct(m[:, :])',
                'right': 'r = CountDistinct(m[:, "Department"])',
                'explanation': (
                    "CountDistinct counts unique values in ONE column.\n"
                    "\n"
                    "Incorrect:\n"
                    "     CountDistinct(m[:, :])\n"
                    "     CountDistinct(m)\n"
                    "\n"
                    "Correct:\n"
                    "     CountDistinct(m[:, \"Department\"])"
                ),
                'variants': [
                    'r = CountDistinct(m[:, "Department"])',
                    'r = CountDistinct(m[:, 3])',
                ],
            },
            'COUNTDISTINCT_BAD_ARG': {
                'message': (
                    "CountDistinct: works with vectors and column slices."
                ),
                'wrong': 'CountDistinct(42)',
                'right': 'CountDistinct(v)',
                'explanation': (
                    "CountDistinct works with:\n"
                    "     vector — CountDistinct(v)\n"
                    "     slice — CountDistinct(m[:, \"X\"])\n"
                    "\n"
                    "Correct:\n"
                    "     CountDistinct(v)\n"
                    "     CountDistinct(m[:, \"Department\"])"
                ),
                'variants': [
                    'r = CountDistinct(v)',
                    'r = CountDistinct(m[:, "Department"])',
                ],
            },
            'COUNTDISTINCT_DUCKDB_ROW_RANGE': {
                'message': (
                    "CountDistinct: DuckDB does not support row ranges."
                ),
                'wrong': 'r = CountDistinct(bd[2:10, "Department"])',
                'right': 'r = CountDistinct(bd[:, "Department"])',
                'explanation': (
                    "BigData (DuckDB) is a read-only view on a file.\n"
                    "Row ranges are not supported.\n"
                    "\n"
                    "Use a full slice:\n"
                    "     CountDistinct(bd[:, \"Department\"])"
                ),
                'variants': [
                    'r = CountDistinct(bd[:, "Department"])',
                ],
            },
            'COUNTDISTINCT_REQUIRES_ASSIGNMENT': {
                'message': (
                    "CountDistinct() returns a value — "
                    "the result must be saved."
                ),
                'wrong': 'CountDistinct(m[:, "Department"])',
                'right': 'r = CountDistinct(m[:, "Department"])',
                'explanation': (
                    "CountDistinct returns a SCALAR (number).\n"
                    "Without assignment the result is lost.\n"
                    "\n"
                    "Correct:\n"
                    "  r = CountDistinct(...)\n"
                    "  print(CountDistinct(...))"
                ),
                'variants': [
                    'r = CountDistinct(m[:, "Department"])',
                    'print(CountDistinct(m[:, "Department"]))',
                ],
            },
        },
    },

    # ============================================================
    # VALUE COUNTS
    # ============================================================
    'ValueCounts': {
        'name': 'ValueCounts',
        'category': 'deduplicate',
        'signature': 'ValueCounts(slice)',
        'description': (
            'Frequency table.\n'
            '  • Returns 2 columns: value, count.\n'
            '  • Sorted by count (descending).\n'
            '  • Works with Matrix and DuckDB.'
        ),
        'examples': [
            'r = ValueCounts(v)',
            'r = ValueCounts(m[:, "Department"])',
        ],
        'errors': {
            'VALUECOUNTS_BAD_SYNTAX': {
                'message': (
                    "ValueCounts: invalid syntax.\n"
                    "  Exactly one argument is required."
                ),
                'wrong': 'ValueCounts()',
                'right': 'ValueCounts(m[:, "Department"])',
                'explanation': (
                    "ValueCounts takes ONE argument:\n"
                    "     ValueCounts(vector)\n"
                    "     ValueCounts(matrix[:, \"X\"])\n"
                    "\n"
                    "Correct:\n"
                    "     ValueCounts(m[:, \"Department\"])"
                ),
                'variants': [
                    'r = ValueCounts(v)',
                    'r = ValueCounts(m[:, "Department"])',
                ],
            },
            'VALUECOUNTS_COLON_SLICE': {
                'message': (
                    "ValueCounts: specify ONE column.\n"
                    "  Slice ':' (all columns) is not supported."
                ),
                'wrong': 'r = ValueCounts(m[:, :])',
                'right': 'r = ValueCounts(m[:, "Department"])',
                'explanation': (
                    "ValueCounts counts frequencies for ONE column.\n"
                    "\n"
                    "Incorrect:\n"
                    "     ValueCounts(m[:, :])\n"
                    "     ValueCounts(m)\n"
                    "\n"
                    "Correct:\n"
                    "     ValueCounts(m[:, \"Department\"])"
                ),
                'variants': [
                    'r = ValueCounts(m[:, "Department"])',
                ],
            },
            'VALUECOUNTS_BAD_ARG': {
                'message': (
                    "ValueCounts: works with vectors and column slices."
                ),
                'wrong': 'ValueCounts(42)',
                'right': 'ValueCounts(v)',
                'explanation': (
                    "ValueCounts works with:\n"
                    "     vector — ValueCounts(v)\n"
                    "     slice — ValueCounts(m[:, \"X\"])"
                ),
                'variants': [
                    'r = ValueCounts(v)',
                    'r = ValueCounts(m[:, "Department"])',
                ],
            },
            'VALUECOUNTS_DUCKDB_ROW_RANGE': {
                'message': (
                    "ValueCounts: DuckDB does not support row ranges."
                ),
                'wrong': 'r = ValueCounts(bd[2:10, "Department"])',
                'right': 'r = ValueCounts(bd[:, "Department"])',
                'explanation': (
                    "BigData (DuckDB) is a read-only view on a file.\n"
                    "Row ranges are not supported.\n"
                    "\n"
                    "Use a full slice:\n"
                    "     ValueCounts(bd[:, \"Department\"])"
                ),
                'variants': [
                    'r = ValueCounts(bd[:, "Department"])',
                ],
            },
            'VALUECOUNTS_REQUIRES_ASSIGNMENT': {
                'message': (
                    "ValueCounts() returns a value — "
                    "the result must be saved."
                ),
                'wrong': 'ValueCounts(m[:, "Department"])',
                'right': 'r = ValueCounts(m[:, "Department"])',
                'explanation': (
                    "ValueCounts does NOT modify the source matrix.\n"
                    "It RETURNS a NEW one.\n"
                    "\n"
                    "Correct:\n"
                    "  r = ValueCounts(...)\n"
                    "  print(ValueCounts(...))"
                ),
                'variants': [
                    'r = ValueCounts(m[:, "Department"])',
                    'print(ValueCounts(m[:, "Department"]))',
                ],
            },
        },
    },

    # ============================================================
    # DELETE DUPLICATE
    # ============================================================
    'DeleteDuplicate': {
        'name': 'DeleteDuplicate',
        'category': 'deduplicate',
        'signature': 'DeleteDuplicate(slice)',
        'description': (
            'Remove duplicates (alias of Unique).\n'
            '  • Vector → unique elements.\n'
            '  • Matrix → unique rows.\n'
            '  • Returns a NEW matrix.\n'
            '  • Works with Matrix and DuckDB.'
        ),
        'examples': [
            'r = DeleteDuplicate(v)',
            'r = DeleteDuplicate(m[:, "Department"])',
            'm = DeleteDuplicate(m)',
        ],
        'errors': {
            'DELETEDUPLICATE_BAD_SYNTAX': {
                'message': (
                    "DeleteDuplicate: invalid syntax.\n"
                    "  Exactly one argument is required."
                ),
                'wrong': 'DeleteDuplicate()',
                'right': 'DeleteDuplicate(m[:, "Department"])',
                'explanation': (
                    "DeleteDuplicate takes ONE argument:\n"
                    "     DeleteDuplicate(vector)\n"
                    "     DeleteDuplicate(matrix)\n"
                    "     DeleteDuplicate(matrix[:, \"X\"])\n"
                    "\n"
                    "Correct:\n"
                    "     DeleteDuplicate(m[:, \"Department\"])"
                ),
                'variants': [
                    'r = DeleteDuplicate(v)',
                    'r = DeleteDuplicate(m)',
                    'r = DeleteDuplicate(m[:, "Department"])',
                ],
            },
            'DELETEDUPLICATE_COLON_SLICE': {
                'message': (
                    "DeleteDuplicate: specify ONE column\n"
                    "or pass the whole matrix."
                ),
                'wrong': 'r = DeleteDuplicate(m[:, :])',
                'right': 'r = DeleteDuplicate(m)',
                'explanation': (
                    "For the whole matrix — pass it without slice:\n"
                    "     DeleteDuplicate(m)\n"
                    "\n"
                    "For one column:\n"
                    "     DeleteDuplicate(m[:, \"Department\"])\n"
                    "\n"
                    "Incorrect:\n"
                    "     DeleteDuplicate(m[:, :])"
                ),
                'variants': [
                    'r = DeleteDuplicate(m)',
                    'r = DeleteDuplicate(m[:, "Department"])',
                ],
            },
            'DELETEDUPLICATE_DUCKDB_ROW_RANGE': {
                'message': (
                    "DeleteDuplicate: DuckDB does not support row ranges."
                ),
                'wrong': 'r = DeleteDuplicate(bd[2:10, "Department"])',
                'right': 'r = DeleteDuplicate(bd[:, "Department"])',
                'explanation': (
                    "BigData (DuckDB) is a read-only view on a file.\n"
                    "Row ranges are not supported.\n"
                    "\n"
                    "Use a full slice:\n"
                    "     DeleteDuplicate(bd[:, \"Department\"])"
                ),
                'variants': [
                    'r = DeleteDuplicate(bd[:, "Department"])',
                ],
            },
            'DELETEDUPLICATE_REQUIRES_ASSIGNMENT': {
                'message': (
                    "DeleteDuplicate() returns a value — "
                    "the result must be saved."
                ),
                'wrong': 'DeleteDuplicate(m[:, "Department"])',
                'right': 'm = DeleteDuplicate(m[:, "Department"])',
                'explanation': (
                    "DeleteDuplicate does NOT modify the source matrix.\n"
                    "It RETURNS a NEW one.\n"
                    "\n"
                    "Correct:\n"
                    "  r = DeleteDuplicate(...)\n"
                    "  m = DeleteDuplicate(...)      — mutation"
                ),
                'variants': [
                    'r = DeleteDuplicate(m[:, "Department"])',
                    'm = DeleteDuplicate(m[:, "Department"])',
                ],
            },
        },
    },
}