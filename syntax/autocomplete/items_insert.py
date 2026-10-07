# syntax/autocomplete/items_insert.py
"""
Описания функций вставки / копирования / перемещения:
insert, insertif, copy, move, matrixmod, joinarray, unpivot.
"""

RU = {
    # ============================================================
    # INSERT
    # ============================================================
    'insert': {
        'signature': 'insert(m[индекс], before | after)',
        'description': (
            '➕ ВСТАВИТЬ ПУСТУЮ СТРОКУ ИЛИ СТОЛБЕЦ\n'
            '\n'
            'ЗАЧЕМ НУЖНА:\n'
            '  • Добавить пустое место в матрицу.\n'
            '  • Классика: "вставить разделитель между блоками".\n'
            '  • Подготовить место для данных.\n'
            '\n'
            'ФОРМАТЫ:\n'
            '  • insert(m[2, :], before)   — пустая строка ПЕРЕД 2-й\n'
            '  • insert(m[2, :], after)    — пустая строка ПОСЛЕ 2-й\n'
            '  • insert(m[:, 3], before)   — пустой столбец ПЕРЕД 3-м\n'
            '  • insert(m[:, 3], after)    — пустой столбец ПОСЛЕ 3-го\n'
            '  • insert(v, 3, after)       — пустое место в вектор\n'
            '\n'
            'НАПРАВЛЕНИЕ ОБЯЗАТЕЛЬНО:\n'
            '  • before — ПЕРЕД указанной позицией.\n'
            '  • after  — ПОСЛЕ указанной позиции.\n'
            '\n'
            'КАКИЕ ЗАДАЧИ РЕШАЕТ:\n'
            '  • Разделить блоки пустой строкой.\n'
            '  • Добавить пустой столбец для будущих данных.\n'
            '  • Подготовить шаблон для заполнения.\n'
            '\n'
            'ПРАВИЛА:\n'
            '  • Все ячейки новой строки/столбца = None.\n'
            '  • Возвращает НОВУЮ матрицу.\n'
            '  • Для мутации: m = insert(...)\n'
            '  ⚠️ Только Matrix (RAM). DuckDB не поддерживается.'
        ),
        'example': (
            'r = insert(m[2, :], before)\n'
            'r = insert(m[2, :], after)\n'
            'm = insert(m[:, 3], after)'
        ),
        'matrix_example': (
            '# ДАНО:\n'
            '#\n'
            '#   m = ["A", "B", "C";\n'
            '#        1,   2,   3;\n'
            '#        4,   5,   6]\n'
            '\n'
            '# ЗАДАЧА 1: вставить пустую строку ПЕРЕД строкой 2\n'
            'r = insert(m[2, :], before)\n'
            'print(r)\n'
            '\n'
            '# ВЫВОД:\n'
            '#\n'
            '#   A     B    C\n'
            '#   None  None None   ← новая строка\n'
            '#   1     2    3\n'
            '#   4     5    6\n'
            '\n'
            '# ЗАДАЧА 2: вставить пустой столбец ПОСЛЕ столбца 2\n'
            'r2 = insert(m[:, 2], after)\n'
            'print(r2)\n'
            '\n'
            '# ВЫВОД:\n'
            '#\n'
            '#   A  B     C\n'
            '#   1  2     None  3\n'
            '#   4  5     None  6'
        ),
    },

    # ============================================================
    # INSERTIF
    # ============================================================
    'insertif': {
        'signature': 'insertif(условие, before | after)',
        'description': (
            '➕ УСЛОВНАЯ ВСТАВКА ПУСТЫХ СТРОК\n'
            '\n'
            'ЗАЧЕМ НУЖНА:\n'
            '  • Вставить пустую строку ПОСЛЕ/ПЕРЕД каждым совпадением.\n'
            '  • Классика: "разделить блоки пустой строкой".\n'
            '  • Разделители между группами.\n'
            '\n'
            'КАК РАБОТАЕТ:\n'
            '  • Идёт по строкам СНИЗУ ВВЕРХ.\n'
            '  • Для каждой подходящей строки вставляет пустую.\n'
            '  • Обработка снизу — чтобы не сбить индексы.\n'
            '\n'
            'КАКИЕ ЗАДАЧИ РЕШАЕТ:\n'
            '  • "Разделить каждый отдел пустой строкой".\n'
            '  • Разделить блоки по маркеру.\n'
            '  • Визуальное разделение отчёта.\n'
            '\n'
            'ПРАВИЛА:\n'
            '  • Пустая строка = None во всех столбцах.\n'
            '  • Возвращает НОВУЮ матрицу.\n'
            '  • Для мутации: m = insertif(...)\n'
            '  ⚠️ Только Matrix (RAM). DuckDB не поддерживается.'
        ),
        'example': (
            'r = insertif(m[:, "Отдел"] == "IT", after)\n'
            'r = insertif(m[:, "Возраст"] > 25, before)'
        ),
        'matrix_example': (
            '# ДАНО:\n'
            '#\n'
            '#   m = ["Отдел", "Сотрудник";\n'
            '#        "IT", "Аня";\n'
            '#        "HR", "Боб";\n'
            '#        "IT", "Света"]\n'
            '\n'
            '# ЗАДАЧА: после каждого IT вставить пустую строку\n'
            'r = insertif(m[:, "Отдел"] == "IT", after)\n'
            'print(r)\n'
            '\n'
            '# ВЫВОД:\n'
            '#\n'
            '#   Отдел  Сотрудник\n'
            '#   IT     Аня\n'
            '#   None   None      ← вставлено после Ани\n'
            '#   HR     Боб\n'
            '#   IT     Света\n'
            '#   None   None      ← вставлено после Светы'
        ),
    },

    # ============================================================
    # COPY
    # ============================================================
    'copy': {
        'signature': 'copy(m[источник], m[цель], before | after)',
        'description': (
            '📋 КОПИРОВАТЬ СТРОКУ ИЛИ СТОЛБЕЦ\n'
            '\n'
            'ЗАЧЕМ НУЖНА:\n'
            '  • Скопировать столбец/строку в другую позицию.\n'
            '  • Оригинал остаётся на месте.\n'
            '  • Классика: "продублировать столбец с формулой".\n'
            '\n'
            'ФОРМАТЫ:\n'
            '  • copy(m[:, 1], m[:, 10], after)  — столбец 1 после 10\n'
            '  • copy(m[2, :], m[4, :], before)  — строка 2 перед 4\n'
            '\n'
            'ОТЛИЧИЕ ОТ move:\n'
            '  copy — копирует (оригинал остаётся).\n'
            '  move — перемещает (оригинал удаляется).\n'
            '\n'
            'КАКИЕ ЗАДАЧИ РЕШАЕТ:\n'
            '  • Дублировать столбец с формулой.\n'
            '  • Сделать копию строки-шаблона.\n'
            '  • Скопировать блок данных.\n'
            '\n'
            'ПРАВИЛА:\n'
            '  • Источник и цель — из ОДНОЙ матрицы.\n'
            '  • Цель не может быть диапазоном.\n'
            '  • Возвращает НОВУЮ матрицу.\n'
            '  ⚠️ Только Matrix (RAM). DuckDB не поддерживается.'
        ),
        'example': (
            'r = copy(m[:, 1], m[:, 3], after)\n'
            'm = copy(m[:, 1], m[:, 3], after)'
        ),
        'matrix_example': (
            '# ДАНО:\n'
            '#\n'
            '#   m = ["A", "B", "C";\n'
            '#        1,   2,   3;\n'
            '#        4,   5,   6]\n'
            '\n'
            '# ЗАДАЧА: скопировать столбец A ПОСЛЕ столбца C\n'
            'r = copy(m[:, "A"], m[:, "C"], after)\n'
            'print(r)\n'
            '\n'
            '# ВЫВОД (A появился в конце):\n'
            '#\n'
            '#   A  B  C  A\n'
            '#   1  2  3  1\n'
            '#   4  5  6  4'
        ),
    },

    # ============================================================
    # MOVE
    # ============================================================
    'move': {
        'signature': 'move(m[источник], m[цель], before | after)',
        'description': (
            '↔️ ПЕРЕМЕСТИТЬ СТРОКУ ИЛИ СТОЛБЕЦ\n'
            '\n'
            'ЗАЧЕМ НУЖНА:\n'
            '  • Переместить столбец/строку в другую позицию.\n'
            '  • Оригинал УДАЛЯЕТСЯ с прежнего места.\n'
            '  • Классика: "переставить столбцы местами".\n'
            '\n'
            'ФОРМАТЫ:\n'
            '  • move(m[:, 1], m[:, 10], after)  — столбец 1 после 10\n'
            '  • move(m[2, :], m[4, :], before)  — строка 2 перед 4\n'
            '\n'
            'ОТЛИЧИЕ ОТ copy:\n'
            '  copy — копирует (оригинал остаётся).\n'
            '  move — перемещает (оригинал удаляется).\n'
            '\n'
            'КАКИЕ ЗАДАЧИ РЕШАЕТ:\n'
            '  • Поменять порядок столбцов.\n'
            '  • Передвинуть строку итогов.\n'
            '  • Переставить блоки местами.\n'
            '\n'
            'ПРАВИЛА:\n'
            '  • Цель не может быть ВНУТРИ источника.\n'
            '  • Цель не может быть диапазоном.\n'
            '  • Возвращает НОВУЮ матрицу.\n'
            '  ⚠️ Только Matrix (RAM). DuckDB не поддерживается.'
        ),
        'example': (
            'r = move(m[:, 1], m[:, 3], after)\n'
            'm = move(m[:, 1], m[:, 3], after)'
        ),
        'matrix_example': (
            '# ДАНО:\n'
            '#\n'
            '#   m = ["A", "B", "C";\n'
            '#        1,   2,   3;\n'
            '#        4,   5,   6]\n'
            '\n'
            '# ЗАДАЧА: переместить столбец A ПОСЛЕ столбца C\n'
            'r = move(m[:, "A"], m[:, "C"], after)\n'
            'print(r)\n'
            '\n'
            '# ВЫВОД (A на новом месте, исходное удалено):\n'
            '#\n'
            '#   B  C  A\n'
            '#   2  3  1\n'
            '#   5  6  4'
        ),
    },

    # ============================================================
    # MATRIXMOD
    # ============================================================
    'matrixmod': {
        'signature': 'matrixmod(m, действие, N [, before|after])',
        'description': (
            '🛠️ МОДИФИКАЦИЯ СТРОК МАТРИЦЫ\n'
            '\n'
            'ЗАЧЕМ НУЖНА:\n'
            '  • Одна функция для разных действий со строками.\n'
            '  • Много операций — один вызов.\n'
            '  • Работает со СПИСКОМ номеров строк.\n'
            '\n'
            'ДОСТУПНЫЕ ДЕЙСТВИЯ:\n'
            '\n'
            '  ▸ delete    — удалить строки\n'
            '      matrixmod(m, delete, 2)\n'
            '      matrixmod(m, delete, [2, 4])\n'
            '\n'
            '  ▸ insert    — вставить пустые строки\n'
            '      matrixmod(m, insert, 2, before)\n'
            '      matrixmod(m, insert, [2, 4], after)\n'
            '\n'
            '  ▸ duplicate — продублировать строки\n'
            '      matrixmod(m, duplicate, 2, after)\n'
            '\n'
            '  ▸ clear     — обнулить строки (None)\n'
            '      matrixmod(m, clear, 3)\n'
            '\n'
            '  ▸ keep      — оставить ТОЛЬКО эти строки\n'
            '      matrixmod(m, keep, [1, 3])\n'
            '\n'
            '  ▸ swap      — поменять две строки местами\n'
            '      matrixmod(m, swap, [2, 5])\n'
            '\n'
            'КАКИЕ ЗАДАЧИ РЕШАЕТ:\n'
            '  • Массовое удаление / добавление строк.\n'
            '  • Оставить только выбранные строки.\n'
            '  • Поменять строки местами.\n'
            '  • Очистить / обнулить строки.\n'
            '\n'
            'ПРАВИЛА:\n'
            '  • insert / duplicate требуют before или after.\n'
            '  • N может быть: число, [список], last K, end.\n'
            '  • Возвращает НОВУЮ матрицу.\n'
            '  ⚠️ Только Matrix (RAM). DuckDB не поддерживается.'
        ),
        'example': (
            'r = matrixmod(m, delete, 2)\n'
            'r = matrixmod(m, insert, 2, before)\n'
            'r = matrixmod(m, duplicate, [2, 4], after)\n'
            'r = matrixmod(m, keep, [1, 3])\n'
            'r = matrixmod(m, swap, [2, 5])\n'
            'r = matrixmod(m, clear, 3)'
        ),
        'matrix_example': (
            '# ДАНО:\n'
            '#\n'
            '#   m = ["A", "B";\n'
            '#        1,   2;\n'
            '#        3,   4;\n'
            '#        5,   6]\n'
            '\n'
            '# ЗАДАЧА 1: удалить строку 2\n'
            'r1 = matrixmod(m, delete, 2)\n'
            'print(r1)\n'
            '# ВЫВОД:\n'
            '#   A  B\n'
            '#   1  2\n'
            '#   5  6\n'
            '\n'
            '# ЗАДАЧА 2: оставить только строки 1 и 3 (с заголовком)\n'
            'r2 = matrixmod(m, keep, [1, 3])\n'
            'print(r2)\n'
            '# ВЫВОД:\n'
            '#   A  B\n'
            '#   1  2\n'
            '#   5  6\n'
            '\n'
            '# ЗАДАЧА 3: поменять строки 2 и 3\n'
            'r3 = matrixmod(m, swap, [2, 3])\n'
            'print(r3)\n'
            '# ВЫВОД:\n'
            '#   A  B\n'
            '#   3  4\n'
            '#   1  2\n'
            '#   5  6'
        ),
    },

    # ============================================================
    # JOINARRAY
    # ============================================================
    'joinarray': {
        'signature': 'joinarray(m1, m2, vertical | horizontal)',
        'description': (
            '🔗 СКЛЕИТЬ МАТРИЦЫ\n'
            '\n'
            'ЗАЧЕМ НУЖНА:\n'
            '  • Объединить несколько матриц в одну.\n'
            '  • vertical — строки ВНИЗ (как UNION ALL в SQL).\n'
            '  • horizontal — столбцы ВПРАВО (как JOIN по позиции).\n'
            '\n'
            'ФОРМАТЫ:\n'
            '  • joinarray(a, b, vertical)        — a и b друг под другом\n'
            '  • joinarray(a, b, horizontal)      — a и b рядом\n'
            '  • joinarray(a, b, c, vertical)     — 3+ матриц\n'
            '\n'
            'ПРАВИЛА VERTICAL:\n'
            '  • Все матрицы должны иметь ОДИНАКОВОЕ число столбцов.\n'
            '  • Строки просто присоединяются снизу.\n'
            '  • Идеально для: "данные за январь + за февраль".\n'
            '\n'
            'ПРАВИЛА HORIZONTAL:\n'
            '  • Все матрицы должны иметь ОДИНАКОВОЕ число строк.\n'
            '  • Столбцы присоединяются вправо.\n'
            '  • Идеально для: "столбец A + столбец B рядом".\n'
            '\n'
            'КАКИЕ ЗАДАЧИ РЕШАЕТ:\n'
            '  • Склеить данные из разных источников.\n'
            '  • Объединить несколько Excel-файлов.\n'
            '  • Соединить справочники по позиции.\n'
            '\n'
            'ПРАВИЛА:\n'
            '  • Работает с Matrix, DuckDB и смешанно.\n'
            '  • НЕ принимает срезы (только целые матрицы).\n'
            '  • Возвращает НОВУЮ матрицу.'
        ),
        'example': (
            'r = joinarray(a, b, vertical)\n'
            'r = joinarray(a, b, horizontal)\n'
            'r = joinarray(a, b, c, vertical)'
        ),
        'matrix_example': (
            '# ДАНО:\n'
            '#\n'
            '#   a = ["ID", "Имя"; 101, "Аня"; 102, "Боб"]\n'
            '#   b = ["ID", "Имя"; 103, "Света"; 104, "Гена"]\n'
            '\n'
            '# ЗАДАЧА 1: склеить ВНИЗ (vertical)\n'
            'r1 = joinarray(a, b, vertical)\n'
            'print(r1)\n'
            '# ВЫВОД:\n'
            '#   ID   Имя\n'
            '#   101  Аня\n'
            '#   102  Боб\n'
            '#   103  Света\n'
            '#   104  Гена\n'
            '\n'
            '# ЗАДАЧА 2: склеить ВПРАВО (horizontal)\n'
            '#   a = ["Имя"; "Аня"; "Боб"]      — вектор 1 столбец\n'
            '#   b = ["Возраст"; 25; 30]\n'
            'r2 = joinarray(a, b, horizontal)\n'
            'print(r2)\n'
            '# ВЫВОД:\n'
            '#   Имя  Возраст\n'
            '#   Аня  25\n'
            '#   Боб  30'
        ),
    },

    # ============================================================
    # UNPIVOT
    # ============================================================
    'unpivot': {
        'signature': (
            'unpivot(m[:, срез], by m[:, "столбец"] '
            '[, names "A", "B"])'
        ),
        'description': (
            '🔄 РАЗВЕРНУТЬ ШИРОКУЮ ТАБЛИЦУ В ДЛИННУЮ (unpivot)\n'
            '\n'
            'ЗАЧЕМ НУЖНА:\n'
            '  • "Сложить" несколько столбцов в два:\n'
            '    один — название исходного столбца, другой — значение.\n'
            '  • Классика: "годы 2021, 2022, 2023 → столбец Год".\n'
            '\n'
            'СИНТАКСИС:\n'
            '  unpivot( ЧТО_СКЛАДЫВАЕМ , by КЛЮЧИ [, names ИМЯ1, ИМЯ2] )\n'
            '\n'
            '  1-й аргумент — срез столбцов, которые "складываем".\n'
            '  by           — идентификаторы (остаются как есть).\n'
            '  names        — имена двух новых колонок.\n'
            '\n'
            'ПО УМОЛЧАНИЮ имена новых колонок:\n'
            '  • "Переменная" — название исходного столбца.\n'
            '  • "Значение"   — само значение.\n'
            '\n'
            'КАКИЕ ЗАДАЧИ РЕШАЕТ:\n'
            '  • Широкая → длинная: годы как столбцы → годы как строки.\n'
            '  • Excel-формат → база данных (long format).\n'
            '  • Развернуть таблицу для графиков.\n'
            '  • Разные категории → один столбец.\n'
            '\n'
            'ЧТО МОЖНО В 1-м АРГУМЕНТЕ:\n'
            '  • диапазон — m[:, 2:end]\n'
            '  • отдельный столбец — m[:, 2]\n'
            '  • last N — m[:, last 2]\n'
            '  • end — m[:, end]\n'
            '\n'
            'ПРАВИЛА:\n'
            '  • by и data НЕ должны пересекаться.\n'
            '  • Работает с Matrix и DuckDB.\n'
            '  • Возвращает НОВУЮ матрицу.'
        ),
        'example': (
            'r = unpivot(m[:, 2:end], by m[:, "Страна"])\n'
            'r = unpivot(m[:, 2:end], by m[:, "Страна"],\n'
            '            names "Год", "Население")'
        ),
        'matrix_example': (
            '# ДАНО:\n'
            '#\n'
            '#   m = ["Страна", "2021", "2022";\n'
            '#        "РФ",     146,    144;\n'
            '#        "США",    331,    333]\n'
            '\n'
            '# ЗАДАЧА: превратить годы-столбцы в строки\n'
            'r = unpivot(m[:, 2:end], by m[:, "Страна"],\n'
            '            names "Год", "Население")\n'
            'print(r)\n'
            '\n'
            '# ВЫВОД:\n'
            '#\n'
            '#   Страна  Год   Население\n'
            '#   РФ      2021  146\n'
            '#   РФ      2022  144\n'
            '#   США     2021  331\n'
            '#   США     2022  333'
        ),
    },
}


EN = {
    'insert': {
        'signature': 'insert(m[index], before | after)',
        'description': (
            '➕ INSERT EMPTY ROW OR COLUMN\n'
            '\n'
            'WHY NEEDED:\n'
            '  • Add empty space into the matrix.\n'
            '  • Classic: "insert separator between blocks".\n'
            '\n'
            'FORMATS:\n'
            '  • insert(m[2, :], before)   — empty row BEFORE row 2\n'
            '  • insert(m[2, :], after)    — empty row AFTER row 2\n'
            '  • insert(m[:, 3], before)   — empty column BEFORE col 3\n'
            '  • insert(m[:, 3], after)    — empty column AFTER col 3\n'
            '\n'
            'DIRECTION IS REQUIRED:\n'
            '  • before — BEFORE the position.\n'
            '  • after  — AFTER the position.\n'
            '\n'
            'RULES:\n'
            '  • All cells of new row/column = None.\n'
            '  • Returns a NEW matrix.\n'
            '  ⚠️ Matrix only (RAM). DuckDB not supported.'
        ),
        'example': (
            'r = insert(m[2, :], before)\n'
            'r = insert(m[2, :], after)\n'
            'm = insert(m[:, 3], after)'
        ),
    },
    'insertif': {
        'signature': 'insertif(condition, before | after)',
        'description': (
            '➕ CONDITIONAL INSERT OF EMPTY ROWS\n'
            '\n'
            'WHY NEEDED:\n'
            '  • Insert empty row AFTER/BEFORE each match.\n'
            '  • Classic: "separate blocks with empty row".\n'
            '\n'
            'HOW IT WORKS:\n'
            '  • Goes through rows BOTTOM-UP.\n'
            '  • Inserts empty row for each match.\n'
            '  • Bottom-up processing — to not shift indices.\n'
            '\n'
            'RULES:\n'
            '  • Empty row = None in all columns.\n'
            '  • Returns a NEW matrix.\n'
            '  ⚠️ Matrix only (RAM). DuckDB not supported.'
        ),
        'example': (
            'r = insertif(m[:, "Dept"] == "IT", after)\n'
            'r = insertif(m[:, "Age"] > 25, before)'
        ),
    },
    'copy': {
        'signature': 'copy(m[source], m[target], before | after)',
        'description': (
            '📋 COPY ROW OR COLUMN\n'
            '\n'
            'WHY NEEDED:\n'
            '  • Copy column/row to another position.\n'
            '  • Original stays in place.\n'
            '\n'
            'HOW IT DIFFERS FROM move:\n'
            '  copy — copies (original remains).\n'
            '  move — moves (original is removed).\n'
            '\n'
            'RULES:\n'
            '  • Source and target — from the SAME matrix.\n'
            '  • Target cannot be a range.\n'
            '  • Returns a NEW matrix.\n'
            '  ⚠️ Matrix only (RAM). DuckDB not supported.'
        ),
        'example': (
            'r = copy(m[:, 1], m[:, 3], after)\n'
            'm = copy(m[:, 1], m[:, 3], after)'
        ),
    },
    'move': {
        'signature': 'move(m[source], m[target], before | after)',
        'description': (
            '↔️ MOVE ROW OR COLUMN\n'
            '\n'
            'WHY NEEDED:\n'
            '  • Move column/row to another position.\n'
            '  • Original is REMOVED from its old place.\n'
            '\n'
            'HOW IT DIFFERS FROM copy:\n'
            '  copy — copies (original remains).\n'
            '  move — moves (original is removed).\n'
            '\n'
            'RULES:\n'
            '  • Target cannot be INSIDE source.\n'
            '  • Target cannot be a range.\n'
            '  • Returns a NEW matrix.\n'
            '  ⚠️ Matrix only (RAM). DuckDB not supported.'
        ),
        'example': (
            'r = move(m[:, 1], m[:, 3], after)\n'
            'm = move(m[:, 1], m[:, 3], after)'
        ),
    },
    'matrixmod': {
        'signature': 'matrixmod(m, action, N [, before|after])',
        'description': (
            '🛠️ MATRIX ROW MODIFICATION\n'
            '\n'
            'WHY NEEDED:\n'
            '  • One function for different row operations.\n'
            '  • Works with a LIST of row numbers.\n'
            '\n'
            'AVAILABLE ACTIONS:\n'
            '\n'
            '  ▸ delete    — delete rows\n'
            '  ▸ insert    — insert empty rows (needs before/after)\n'
            '  ▸ duplicate — duplicate rows (needs before/after)\n'
            '  ▸ clear     — clear rows (set to None)\n'
            '  ▸ keep      — keep ONLY these rows\n'
            '  ▸ swap      — swap two rows\n'
            '\n'
            'RULES:\n'
            '  • insert / duplicate require before or after.\n'
            '  • N can be: number, [list], last K, end.\n'
            '  • Returns a NEW matrix.\n'
            '  ⚠️ Matrix only (RAM). DuckDB not supported.'
        ),
        'example': (
            'r = matrixmod(m, delete, 2)\n'
            'r = matrixmod(m, insert, 2, before)\n'
            'r = matrixmod(m, duplicate, [2, 4], after)\n'
            'r = matrixmod(m, keep, [1, 3])\n'
            'r = matrixmod(m, swap, [2, 5])'
        ),
    },
    'joinarray': {
        'signature': 'joinarray(m1, m2, vertical | horizontal)',
        'description': (
            '🔗 JOIN MATRICES\n'
            '\n'
            'WHY NEEDED:\n'
            '  • Combine several matrices into one.\n'
            '  • vertical — rows DOWN (like UNION ALL in SQL).\n'
            '  • horizontal — columns RIGHT (like positional JOIN).\n'
            '\n'
            'RULES VERTICAL:\n'
            '  • All matrices must have the SAME column count.\n'
            '  • Rows are attached from bottom.\n'
            '\n'
            'RULES HORIZONTAL:\n'
            '  • All matrices must have the SAME row count.\n'
            '  • Columns are attached to the right.\n'
            '\n'
            'RULES:\n'
            '  • Works with Matrix, DuckDB and mixed.\n'
            '  • Does NOT accept slices (only whole matrices).\n'
            '  • Returns a NEW matrix.'
        ),
        'example': (
            'r = joinarray(a, b, vertical)\n'
            'r = joinarray(a, b, horizontal)\n'
            'r = joinarray(a, b, c, vertical)'
        ),
    },
    'unpivot': {
        'signature': (
            'unpivot(m[:, slice], by m[:, "column"] '
            '[, names "A", "B"])'
        ),
        'description': (
            '🔄 UNPIVOT WIDE TABLE INTO LONG\n'
            '\n'
            'WHY NEEDED:\n'
            '  • "Fold" several columns into two:\n'
            '    one — name of source column, another — value.\n'
            '  • Classic: "years 2021, 2022, 2023 → column Year".\n'
            '\n'
            'SYNTAX:\n'
            '  unpivot( WHAT_TO_FOLD , by KEYS [, names NAME1, NAME2] )\n'
            '\n'
            'DEFAULT new column names:\n'
            '  • "Переменная" — name of source column.\n'
            '  • "Значение"   — the value itself.\n'
            '\n'
            'RULES:\n'
            '  • by and data must NOT overlap.\n'
            '  • Works with Matrix and DuckDB.\n'
            '  • Returns a NEW matrix.'
        ),
        'example': (
            'r = unpivot(m[:, 2:end], by m[:, "Country"])\n'
            'r = unpivot(m[:, 2:end], by m[:, "Country"],\n'
            '            names "Year", "Population")'
        ),
    },
}