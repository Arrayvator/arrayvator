# syntax/db.py
"""
Полная база синтаксиса ArrayVator.
Содержит ВСЕ конструкции языка с примерами и частыми ошибками.
"""

SYNTAX_DB = {

    # ============================================================
    # ИНДЕКСАЦИЯ
    # ============================================================
    "matrix_index": {
        "name": "Индексация матрицы",
        "category": "index",
        "patterns": [
            'm[:, "Имя"]           — столбец по имени',
            'm[:, 3]                — столбец по номеру',
            'm[2, :]                — строка',
            'm[2:5, :]              — диапазон строк',
            'm[:, 2:5]              — диапазон столбцов',
            'm[end, :]              — последняя строка',
            'm[:, end]              — последний столбец',
            'm[end-1, :]            — предпоследняя строка',
            'm[last 3, :]           — последние 3 строки',
            'm[:, last 2]           — последние 2 столбца',
            'm[all, :]              — все строки',
            'm[:, all]              — все столбцы',
            'm["Иванов", :]         — строка по значению в 1-м столбце',
        ],
        "examples": [
            'm[2, 3]',
            'm[:, "Имя"]',
            'm[10:end, :]',
            'm[last 2, "Отдел"]',
        ],
        "common_errors": [
            {
                "wrong": 'm[:, Зарплата]',
                "right": 'm[:, "Зарплата"]',
                "reason": "Имя столбца пишется В КАВЫЧКАХ",
            },
            {
                "wrong": 'm(2, 3)',
                "right": 'm[2, 3]',
                "reason": "Индексы — в КВАДРАТНЫХ скобках",
            },
            {
                "wrong": 'm[:3]',
                "right": 'm[:, 3]',
                "reason": "Между индексами — ЗАПЯТАЯ",
            },
            {
                "wrong": 'm[end:end, :]',
                "right": 'm[end, :]',
                "reason": "Для последней — просто 'end'",
            },
            {
                "wrong": 'm[last:3, :]',
                "right": 'm[last 3, :]',
                "reason": "Для последних N — 'last N' (через пробел)",
            },
        ],
    },

    # ============================================================
    # РАСШИРЕНИЕ МАТРИЦЫ
    # ============================================================
    "matrix_extend": {
        "name": "Расширение матрицы",
        "category": "index",
        "patterns": [
            'm[:, end+1] = [...]     — новый столбец',
            'm[end+1, :] = [...]     — новая строка',
            'm[:, 6] = [...]         — расширить до 6 столбцов',
            'm[5, :] = [...]         — расширить до 5 строк',
        ],
        "examples": [
            'm[:, end+1] = [10, 20, 30]',
            'm[end+1, :] = ["new", 99]',
            'm[1:3, 6] = [100, 200, 300]',
        ],
        "common_errors": [
            {
                "wrong": 'm[:, end+1] = None',
                "right": 'm[:, end+1] = [None, None, None]',
                "reason": "При расширении нужно указать значения",
            },
        ],
    },

    # ============================================================
    # ПРИСВАИВАНИЕ
    # ============================================================
    "assign": {
        "name": "Присваивание",
        "category": "assign",
        "patterns": [
            'x = 5',
            'm[1, 1] = "ID"',
            'm[:, 2] = [1, 2, 3]',
            'm[2:3, 2:3] = [1, 2; 3, 4]',
        ],
        "examples": [
            'x = 5',
            'm[2, 3] = 99',
            'm[1, end] = "Итого"',
        ],
        "common_errors": [
            {
                "wrong": 'x == 5',
                "right": 'x = 5',
                "reason": "Присваивание — '=', сравнение — '=='",
            },
        ],
    },

    # ============================================================
    # ФИЛЬТРАЦИЯ
    # ============================================================
    "filterif": {
        "name": "filterif",
        "category": "function",
        "patterns": [
            'filterif(m[:, "X"] == "Y")',
            'filterif(m[:, "X"] > 10 and m[:, "Z"] == "W")',
            'filterif(m[:, "X"] == "Y" or m[:, "X"] == "Z")',
            'filterif(v > 20)',
            'filterif(m[10:end, "X"] == "Y")',
        ],
        "examples": [
            'filterif(m[:, "Пол"] == "Ж")',
            'filterif(m[:, "Возраст"] > 18 and m[:, "Пол"] == "Ж")',
            'filterif(m[:, "Отдел"] == "IT" or m[:, "Отдел"] == "HR")',
        ],
        "common_errors": [
            {
                "wrong": 'filterif(m, "Пол" == "Ж")',
                "right": 'filterif(m[:, "Пол"] == "Ж")',
                "reason": "Нужен срез m[:, \"X\"]",
            },
            {
                "wrong": 'filterif(m[:, "Пол"] = "Ж")',
                "right": 'filterif(m[:, "Пол"] == "Ж")',
                "reason": "Сравнение — '==', не '='",
            },
            {
                "wrong": 'filterif(m[:, "Пол"] == "Ж" && m[:, "Возраст"] > 18)',
                "right": 'filterif(m[:, "Пол"] == "Ж" and m[:, "Возраст"] > 18)',
                "reason": "Логическое И — 'and', не '&&'",
            },
        ],
    },

    # ============================================================
    # СОРТИРОВКА
    # ============================================================
    "sort": {
        "name": "sort",
        "category": "function",
        "patterns": [
            'sort(m[:, "X"], AZ)',
            'sort(m[:, "X"], ZA)',
            'sort(m[:, 3], AZ)',
            'sort(v, AZ)',
        ],
        "examples": [
            'sort(m[:, "Имя"], AZ)',
            'sort(m[:, "Возраст"], ZA)',
            'sort(v, AZ)',
        ],
        "common_errors": [
            {
                "wrong": 'sort(m[:, "Имя"])',
                "right": 'sort(m[:, "Имя"], AZ)',
                "reason": "Нужно указать направление (AZ или ZA)",
            },
            {
                "wrong": 'sort(m, column "Имя", AZ)',
                "right": 'sort(m[:, "Имя"], AZ)',
                "reason": "Аналитик убран — только срез",
            },
        ],
    },

    # ============================================================
    # ВСТАВКА / COPY / MOVE
    # ============================================================
    "insert": {
        "name": "insert",
        "category": "function",
        "patterns": [
            'insert(m[2, :], before)',
            'insert(m[2, :], after)',
            'insert(m[:, 3], before)',
            'insert(v, 3, after)',
        ],
        "examples": [
            'insert(m[2, :], before)',
            'insert(m[:, "Имя"], after)',
        ],
        "common_errors": [
            {
                "wrong": 'insert(m[2, :])',
                "right": 'insert(m[2, :], before)',
                "reason": "Нужно направление (before / after)",
            },
            {
                "wrong": 'insert(m[2:10, end])',
                "right": 'insert(m[2, :], before)',
                "reason": "Диапазон нельзя",
            },
        ],
    },

    "copy": {
        "name": "copy",
        "category": "function",
        "patterns": [
            'copy(m[:, 1], m[:, 3], after)',
            'copy(m[:, 1:3], m[:, 5], after)',
            'copy(m[2, :], m[4, :], before)',
        ],
        "examples": [
            'copy(m[:, 1], m[:, 3], after)',
            'copy(m[:, 1:3], m[:, 5], after)',
        ],
        "common_errors": [
            {
                "wrong": 'copy(m[:, 1], m[:, 3:5], after)',
                "right": 'copy(m[:, 1], m[:, 5], after)',
                "reason": "Цель не может быть диапазоном",
            },
        ],
    },

    "move": {
        "name": "move",
        "category": "function",
        "patterns": [
            'move(m[:, 1], m[:, 4], after)',
            'move(m[1:10, :], m[end, :], after)',
        ],
        "examples": [
            'move(m[:, 1], m[:, 4], after)',
            'move(m[1:10, :], m[end, :], after)',
        ],
        "common_errors": [
            {
                "wrong": 'move(m[:, 1:3], m[:, 2], after)',
                "right": 'move(m[:, 1:3], m[:, 5], after)',
                "reason": "Цель не может быть внутри источника",
            },
        ],
    },

    "joinarray": {
        "name": "joinarray",
        "category": "function",
        "patterns": [
            'joinarray(m1, m2, vertical)',
            'joinarray(m1, m2, horizontal)',
            'joinarray(m1, m2, m3, vertical)',
        ],
        "examples": [
            'joinarray(a, b, vertical)',
            'joinarray(a, b, horizontal)',
        ],
        "common_errors": [
            {
                "wrong": 'joinarray(a[:, 1:3], b, vertical)',
                "right": 'joinarray(a, b, vertical)',
                "reason": "Только ЦЕЛЫЕ матрицы, срезы нельзя",
            },
        ],
    },

    # ============================================================
    # ПОИСК
    # ============================================================
    "find": {
        "name": "find",
        "category": "function",
        "patterns": [
            'find(m[:, "X"] == "Y")',
            'find(m[:, "X"] == "Y", inside)',
            'find(m[:, "X"] == "Y", ignore)',
            'find(v == 5)',
        ],
        "examples": [
            'r = find(m[:, "Имя"] == "Аня")',
            'r = find(m[:, "Имя"] == "ов", inside)',
            'r = find(v == 5)',
        ],
        "common_errors": [],
    },

    # ============================================================
    # INDEX — алиас find
    # ============================================================
    "index_alias": {
        "name": "index (аналог find)",
        "category": "function",
        "patterns": [
            'index(m[:, "X"] == "Y")',
            'index(m[:, "X"] == "Y", inside)',
            'index(v == 5)',
        ],
        "examples": [
            'r = index(m[:, "Имя"] == "Аня")',
            'r = index(v == 5)',
        ],
        "common_errors": [],
    },

    # ============================================================
    # VLOOKUP
    # ============================================================
    "vlookup": {
        "name": "vlookup",
        "category": "function",
        "patterns": [
            'vlookup("X", table, "Y")',
            'vlookup("X", table, "Y", table[:, "Z"])',
            'vlookup(5, table, "Y", approx)',
        ],
        "examples": [
            'vlookup("Аня", e, "Зарплата")',
            'vlookup("IT", e, "Имя", e[:, "Отдел"])',
        ],
        "common_errors": [
            {
                "wrong": 'vlookup("X", e, "Y", row 3)',
                "right": 'vlookup("X", e, "Y", e[:, "Отдел"])',
                "reason": "vlookup работает только по СТОЛБЦАМ",
            },
        ],
    },

    # ============================================================
    # ДУБЛИКАТЫ
    # ============================================================
    "deduplicate": {
        "name": "Уникализация",
        "category": "function",
        "patterns": [
            'Unique(m[:, "X"])',
            'Unique(v)',
            'Unique(m)',
            'CountDistinct(m[:, "X"])',
            'ValueCounts(m[:, "X"])',
            'DeleteDuplicate(m[:, "X"])',
        ],
        "examples": [
            'Unique(m[:, "Отдел"])',
            'Unique(v)',
        ],
        "common_errors": [],
    },

    # ============================================================
    # PIVOT
    # ============================================================
    "pivot": {
        "name": "pivot",
        "category": "function",
        "patterns": [
            'pivot(m[:, "X"], m[:, "Y"], sum)',
            'pivot(m[:, "X"], m[:, "Y"], avg)',
            'pivot(m[:, "X"], m[:, "Y"], count)',
            'pivot(m[:, "X"], m[:, "Y"], median)',
            'pivot(m[:, "X"], m[:, "Y"], first)',
        ],
        "examples": [
            'pivot(m[:, "Отдел"], m[:, "Зарплата"], sum)',
            'pivot(m[:, "Отдел"], m[:, "Сотрудник"], count)',
        ],
        "common_errors": [
            {
                "wrong": 'pivot(m[:, "Отдел"], m[:, "Зарплата"])',
                "right": 'pivot(m[:, "Отдел"], m[:, "Зарплата"], sum)',
                "reason": "Нужна функция агрегации",
            },
        ],
    },

    # ============================================================
    # CASE
    # ============================================================
    "case": {
        "name": "case",
        "category": "function",
        "patterns": [
            'case(m[:, "X"], when < 18 then "Y", else "Z")',
            'case(m[:, "X"], when == "IT" then "Y", else "Z")',
            'case(v, when < 18 then "Y", else "Z")',
        ],
        "examples": [
            'case(m[:, "Возраст"], when < 18 then "Дитя", else "Взрослый")',
            'v = case(m[:, "Возраст"], when < 18 then "Дитя", else "Взрослый")',
        ],
        "common_errors": [
            {
                "wrong": 'case(m[:, "X"], when < 18, else "Y")',
                "right": 'case(m[:, "X"], when < 18 then "Y", else "Z")',
                "reason": "После условия — 'then'",
            },
        ],
    },

    # ============================================================
    # ДАТЫ
    # ============================================================
    "date": {
        "name": "date",
        "category": "function",
        "patterns": [
            'date(данные, "входной", "выходной")',
            'date("20.06.2025", "DD.MM.YYYY", "DD MMMM YYYY")',
            'date("06/20/2025", "MM/DD/YYYY", "DD.MM.YYYY")',
        ],
        "examples": [
            'date(m[:, "Дата"], "MM/DD/YYYY", "DD.MM.YYYY")',
            'date("20.06.2025", "DD.MM.YYYY", "DD MMMM YYYY")',
        ],
        "common_errors": [
            {
                "wrong": 'date("20.06.2025", "DD.MM.YYYY")',
                "right": 'date("20.06.2025", "DD.MM.YYYY", "DD MMMM YYYY")',
                "reason": "Нужны ОБА формата: входной и выходной",
            },
        ],
    },

    # ============================================================
    # ЦИКЛЫ / УСЛОВИЯ
    # ============================================================
    "for": {
        "name": "for",
        "category": "control",
        "patterns": [
            'for i(1:10) { ... }',
            'for i(10:1) { ... }   — обратный',
        ],
        "examples": [
            'for i(1:5) { print(i) }',
            'for n(1:lenrow(m)) { print(m[n, 1]) }',
        ],
        "common_errors": [
            {
                "wrong": 'for i in 10:',
                "right": 'for i(1:10) { ... }',
                "reason": "Нет 'in'. Синтаксис: for i(начало:конец)",
            },
            {
                "wrong": 'for i = 1 to 10',
                "right": 'for i(1:10) { ... }',
                "reason": "Нет 'to'. Диапазон через ':'",
            },
        ],
    },

    "while": {
        "name": "while",
        "category": "control",
        "patterns": [
            'while условие { ... }',
        ],
        "examples": [
            'i = 1\nwhile i <= 5 { print(i); i = i + 1 }',
        ],
        "common_errors": [
            {
                "wrong": 'while i = 5 { ... }',
                "right": 'while i == 5 { ... }',
                "reason": "Сравнение — '==', не '='",
            },
        ],
    },

    "if": {
        "name": "if-then-else",
        "category": "control",
        "patterns": [
            'if условие then { ... }',
            'if условие then { ... } else { ... }',
        ],
        "examples": [
            'if x > 5 then { print("больше") }',
            'if x > 5 then { ... } else { ... }',
        ],
        "common_errors": [
            {
                "wrong": 'if x > 5 { ... }',
                "right": 'if x > 5 then { ... }',
                "reason": "Нужно 'then' после условия",
            },
            {
                "wrong": 'if x = 5 then',
                "right": 'if x == 5 then',
                "reason": "Сравнение — '==', не '='",
            },
        ],
    },

    # ============================================================
    # СПЕЦИАЛЬНЫЕ СЛОВА
    # ============================================================
    "special_words": {
        "name": "Специальные слова",
        "category": "keyword",
        "patterns": [
            'end      — последняя строка/столбец',
            'end-N    — N-я с конца',
            'end+N    — на N дальше (расширение)',
            'last N   — последние N строк/столбцов',
            'all      — все строки/столбцы',
            'begin    — первая строка/столбец',
            'before   — перед целью',
            'after    — после цели',
            'AZ       — сортировка по возрастанию',
            'ZA       — сортировка по убыванию',
            'inside   — поиск подстроки',
            'ignore   — без учёта регистра',
            'approx   — приблизительный поиск',
            'skip     — пропускать пустые',
            'vertical — строки вниз',
            'horizontal — столбцы вправо',
        ],
        "examples": [
            'm[end, :]',
            'm[last 3, :]',
            'sort(m[:, "X"], AZ)',
        ],
        "common_errors": [
            {
                "wrong": 'm[end:end, :]',
                "right": 'm[end, :]',
                "reason": "Для последней — просто 'end'",
            },
            {
                "wrong": 'm[last:3, :]',
                "right": 'm[last 3, :]',
                "reason": "Между 'last' и числом — пробел",
            },
            {
                "wrong": 'm[last 100, :]   # если 50 строк',
                "right": 'm[last 50, :]',
                "reason": "N должно быть МЕНЬШЕ общего количества",
            },
        ],
    },

    # ============================================================
    # ОПЕРАТОРЫ
    # ============================================================
    "operators": {
        "name": "Операторы",
        "category": "operator",
        "patterns": [
            '+   Сложение / Конкатенация',
            '-   Вычитание',
            '*   Умножение',
            '/   Деление',
            '%   Остаток от деления',
            '^   Возведение в степень',
            '//  Целая часть от деления',
            '==  Равно',
            '!=  Не равно',
            '<   Меньше',
            '>   Больше',
            '<=  Меньше или равно',
            '>=  Больше или равно',
            'and Логическое И',
            'or  Логическое ИЛИ',
            'not Логическое НЕ',
        ],
        "examples": [
            'x = 5 + 3',
            'name = "Hello" + "World"',
            'result = (x > 5) and (y < 10)',
        ],
        "common_errors": [
            {
                "wrong": 'if x = 5 then',
                "right": 'if x == 5 then',
                "reason": "Сравнение — '=='. Присваивание — '='",
            },
            {
                "wrong": 'if x > 5 && y < 10',
                "right": 'if x > 5 and y < 10',
                "reason": "Логическое И — 'and', не '&&'",
            },
            {
                "wrong": 'if x > 5 || y < 10',
                "right": 'if x > 5 or y < 10',
                "reason": "Логическое ИЛИ — 'or', не '||'",
            },
            {
                "wrong": 'result = !true',
                "right": 'result = not true',
                "reason": "Логическое НЕ — 'not', не '!'",
            },
        ],
    },
}


# ============================================================
# ИНДЕКС ПО КАТЕГОРИЯМ
# ============================================================
def get_by_category(category):
    """Возвращает все конструкции указанной категории"""
    return {
        name: entry
        for name, entry in SYNTAX_DB.items()
        if entry.get('category') == category
    }


def get_all_categories():
    """Все категории"""
    return sorted(set(
        entry.get('category')
        for entry in SYNTAX_DB.values()
    ))


def find_by_wrong(wrong_code):
    """
    Ищет подсказку по неправильному коду.
    Возвращает (wrong, right, reason) или None.
    """
    wrong_code = wrong_code.strip()

    for entry in SYNTAX_DB.values():
        for err in entry.get('common_errors', []):
            if err['wrong'].strip() == wrong_code:
                return err

    return None


def find_hint_for_line(line):
    """
    Ищет подсказку для строки кода (по ключевым словам).
    Возвращает dict или None.
    """
    if not line:
        return None

    stripped = line.strip().lower()

    for name, entry in SYNTAX_DB.items():
        for pattern in entry.get('patterns', []):
            keyword = pattern.split()[0].lower() if pattern else ''
            if keyword and keyword in stripped:
                return {
                    'name': entry['name'],
                    'patterns': entry.get('patterns', []),
                    'examples': entry.get('examples', []),
                }

    return None