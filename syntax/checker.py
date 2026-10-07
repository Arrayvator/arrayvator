# syntax/checker.py
"""
Сверка кода пользователя с базой синтаксиса.

Проверяет типичные ошибки:
    - = вместо ==
    - && вместо and, || вместо or, ! вместо not
    - for i(1:10), for i in 10:, for i = 1 to 10 (без do)
    - if без then
    - m[:3], m(2, 3), m[end:end], m[last:3]
    - вложенные скобки [[...]]
    - column / row / col (аналитик убран)
    - unpivot без by
    - OpenCSV с неверным режимом
    - зарезервированные слова как имена переменных
    - insertif без before/after
    - matrixmod без действия
    - find без условия
"""

import re
from errors import ArrayVatorError, ErrorContext


# ============================================================
# ВСПОМОГАТЕЛЬНЫЕ
# ============================================================
def _is_inside_string(line, position):
    """Проверяет, находится ли позиция внутри строки в кавычках."""
    in_string = False
    string_char = None

    for i in range(min(position, len(line))):
        ch = line[i]

        if in_string:
            if ch == string_char:
                in_string = False
                string_char = None
        else:
            if ch in ('"', "'"):
                in_string = True
                string_char = ch

    return in_string


def _is_python_line(stripped):
    """Пропускает Python-строки (def, class, import, return)."""
    s = stripped.strip()
    for kw in ('def ', 'class ', 'import ', 'from ', 'return ', 'try:',
               'except ', 'finally:', 'with ', 'yield '):
        if s.startswith(kw):
            return True
    return False


def _is_case_line(stripped):
    """Пропускает строки с when/then/else — они валидны в case."""
    s = stripped.lower()
    return (
        'when' in s or
        s.startswith('then ') or
        ' then ' in s or
        ' else ' in s
    )


# ============================================================
# СПИСОК ПРОВЕРОК
# ============================================================
COMMON_CHECKS = [

    # ============================================================
    # FOR — старый синтаксис for i(1:10)
    # ============================================================
    {
        'name': 'for_old_syntax',
        'pattern': r'(?i)\bfor\s+\w+\s*\(',
        'reason': (
            'Синтаксис for изменился.\n'
            '  Было: for i(1:10) { ... }\n'
            '  Стало: for i = 1 to 10 do { ... }'
        ),
        'suggestion': (
            '❌  for i(1:10) { print(i) }\n'
            '✅  for i = 1 to 10 do { print(i) }\n'
            '\n'
            'Обратный:\n'
            '✅  for i = 10 to 1 do { print(i) }\n'
            '\n'
            'С шагом:\n'
            '✅  for i = 1 to 10 step 2 do { print(i) }'
        ),
    },

    # ============================================================
    # FOR — нет = после переменной
    # ============================================================
    {
        'name': 'for_no_assign',
        'pattern': r'(?i)\bfor\s+\w+\s+(?!=\s*\d)(?!in\b)(?!to\b)(?!do\b)\d',
        'reason': (
            "for: после переменной нужен '='.\n"
            "  Синтаксис: for i = 1 to 10 do"
        ),
        'suggestion': (
            '❌  for i 1:10\n'
            '✅  for i = 1 to 10 do'
        ),
    },

    # ============================================================
    # FOR — нет to (двоеточие вместо to)
    # ============================================================
    {
        'name': 'for_no_to',
        'pattern': r'(?i)\bfor\s+\w+\s*=\s*\d+\s*:\s*\d+',
        'reason': (
            "for: диапазон указывается через 'to', а не ':'.\n"
            "  Синтаксис: for i = 1 to 10 do"
        ),
        'suggestion': (
            '❌  for i = 1:10 do\n'
            '✅  for i = 1 to 10 do'
        ),
    },

    # ============================================================
    # FOR — нет do
    # ============================================================
    {
        'name': 'for_no_do',
        'pattern': r'(?i)\bfor\s+\w+\s*=\s*\d+\s+to\s+\d+\s*\{',
        'reason': (
            "for: после диапазона нужно 'do'.\n"
            "  Синтаксис: for i = 1 to 10 do { ... }"
        ),
        'suggestion': (
            '❌  for i = 1 to 10 { print(i) }\n'
            '✅  for i = 1 to 10 do { print(i) }'
        ),
    },

    # ============================================================
    # FOR — нет in
    # ============================================================
    {
        'name': 'for_in_syntax',
        'pattern': r'(?i)\bfor\s+\w+\s+in\s+',
        'reason': (
            "В for не используется 'in'.\n"
            "  Синтаксис: for i = 1 to 10 do"
        ),
        'suggestion': (
            '❌  for i in 1:10\n'
            '✅  for i = 1 to 10 do { print(i) }'
        ),
    },

    # ============================================================
    # IF без then
    # ============================================================
    {
        'name': 'if_no_then',
        'pattern': r'(?i)\bif\s+(?:(?!\bthen\b)[^{])+\{',
        'reason': 'После условия if нужно ключевое слово "then"',
        'suggestion': (
            '❌  if x > 5 { print("X") }\n'
            '✅  if x > 5 then { print("X") }'
        ),
    },

    # ============================================================
    # = вместо == в условии
    # ============================================================
    {
        'name': 'assign_in_condition',
        'pattern': r'(?i)\b(if|while)\s+[A-Za-z_][A-Za-z0-9_]*\s*=\s*[^=]',
        'reason': 'В условии нужно СРАВНЕНИЕ (==), а не присваивание (=)',
        'suggestion': (
            '❌  if a = 0 then\n'
            '✅  if a == 0 then\n'
            '❌  while i = 5\n'
            '✅  while i == 5'
        ),
    },

    # ============================================================
    # Голое сравнение
    # ============================================================
    {
        'name': 'expression_not_used',
        'pattern': r'^\s*[A-Za-z_][A-Za-z0-9_]*\s*==\s*[^=]',
        'reason': 'Выражение сравнения не используется',
        'suggestion': (
            '❌  x == 5\n'
            '✅  x = 5'
        ),
    },

    # ============================================================
    # && вместо and
    # ============================================================
    {
        'name': 'and_operator',
        'pattern': r'&&',
        'reason': 'Логическое И — "and", а не "&&"',
        'suggestion': (
            '❌  x > 5 && y < 10\n'
            '✅  x > 5 and y < 10'
        ),
    },

    # ============================================================
    # || вместо or
    # ============================================================
    {
        'name': 'or_operator',
        'pattern': r'\|\|',
        'reason': 'Логическое ИЛИ — "or", а не "||"',
        'suggestion': (
            '❌  x > 5 || y < 10\n'
            '✅  x > 5 or y < 10'
        ),
    },

    # ============================================================
    # ! вместо not
    # ============================================================
    {
        'name': 'not_operator',
        'pattern': r'!(?!=)',
        'reason': 'Логическое НЕ — "not", а не "!"',
        'suggestion': (
            '❌  result = !true\n'
            '✅  result = not true'
        ),
    },

    # ============================================================
    # Вложенные скобки [[...]]
    # ============================================================
    {
        'name': 'nested_brackets',
        'pattern': r'\[\s*\[',
        'reason': 'Матрица записывается через ";"',
        'suggestion': (
            '❌  m = [["A", "B"], [1, 2]]\n'
            '✅  m = ["A", "B"; 1, 2]'
        ),
    },

    # ============================================================
    # m[:3] — пропущена запятая
    # ============================================================
    {
        'name': 'missing_comma_in_index',
        'pattern': r'[A-Za-z_][A-Za-z0-9_]*\[\s*:\s*("[^"]*"|\d+)\s*\]',
        'reason': 'Пропущена запятая между индексами',
        'suggestion': (
            '❌  m[:3]\n'
            '❌  m[:"Имя"]\n'
            '✅  m[:, 3]\n'
            '✅  m[:, "Имя"]\n'
            '\n'
            'Для диапазона — с числом перед ":"\n'
            '✅  m[2:4]'
        ),
    },

    # ============================================================
    # m[:, Имя] — без кавычек
    # ============================================================
    {
        'name': 'column_needs_quotes',
        'pattern': r'[A-Za-z_][A-Za-z0-9_]*\[\s*:\s*[A-Za-zА-Яа-я][A-Za-zА-Яа-я0-9_]*\s*\]',
        'reason': 'Имя столбца в индексе пишется В КАВЫЧКАХ',
        'suggestion': (
            '❌  m[:, Пол]\n'
            '✅  m[:, "Пол"]'
        ),
    },

    # ============================================================
    # m(2, 3) — круглые скобки
    # ============================================================
    {
        'name': 'round_brackets',
        'pattern': r'\b[A-Za-z_][A-Za-z0-9_]*\(:',
        'reason': 'Для индексов используются КВАДРАТНЫЕ скобки',
        'suggestion': (
            '❌  m(:, 2)\n'
            '✅  m[:, 2]'
        ),
    },

    # ============================================================
    # m[end:end, :] — лишнее
    # ============================================================
    {
        'name': 'end_colon_end',
        'pattern': r'(?i)\[\s*end\s*:\s*end\s*,',
        'reason': 'Для последней — просто "end", без ":end"',
        'suggestion': (
            '❌  m[end:end, :]\n'
            '✅  m[end, :]\n'
            '❌  m[:, end:end]\n'
            '✅  m[:, end]'
        ),
    },

    # ============================================================
    # m[last:3, :] — двоеточие
    # ============================================================
    {
        'name': 'last_colon',
        'pattern': r'(?i)\blast\s*:\s*\d+',
        'reason': 'Между "last" и числом — ПРОБЕЛ, не двоеточие',
        'suggestion': (
            '❌  m[last:3, :]\n'
            '✅  m[last 3, :]'
        ),
    },

    # ============================================================
    # column / row / col — аналитик убран
    # ============================================================
    {
        'name': 'analyst_removed',
        'pattern': r'(?i)\b(column|row|col)\s+["\d]',
        'reason': 'Аналитик УБРАН. Используйте срез m[:, "X"]',
        'suggestion': (
            '❌  filterif(m, column "Пол" == "Ж")\n'
            '✅  filterif(m[:, "Пол"] == "Ж")\n'
            '\n'
            '❌  delete(m, row 2)\n'
            '✅  delete(m[2, :])\n'
            '\n'
            '❌  sort(m, column "Имя", AZ)\n'
            '✅  sort(m[:, "Имя"], AZ)'
        ),
    },

    # ============================================================
    # sort без направления
    # ============================================================
    {
        'name': 'sort_missing_direction',
        'pattern': r'(?i)\bsort\s*\((?:(?!\baz\b|\bza\b)[^)])*\)',
        'reason': 'Для сортировки нужно указать направление: AZ или ZA',
        'suggestion': (
            '❌  sort(m[:, "Имя"])\n'
            '✅  sort(m[:, "Имя"], AZ)   ← по возрастанию\n'
            '✅  sort(m[:, "Имя"], ZA)   — по убыванию'
        ),
    },

    # ============================================================
    # vlookup с row
    # ============================================================
    {
        'name': 'vlookup_row',
        'pattern': r'(?i)\bvlookup\s*\([^)]*\brow\b',
        'reason': 'vlookup работает только по СТОЛБЦАМ, не по строкам',
        'suggestion': (
            '❌  vlookup("Иванов", e, 4, row 2)\n'
            '✅  vlookup("Иванов", e, 4, e[:, "Отдел"])'
        ),
    },

    # ============================================================
    # insert без направления
    # ============================================================
    {
        'name': 'insert_missing_direction',
        'pattern': r'(?i)\binsert\s*\([^,)]+\)',
        'reason': 'insert требует направление (before / after)',
        'suggestion': (
            '❌  insert(m[2, :])\n'
            '✅  insert(m[2, :], before)\n'
            '✅  insert(m[2, :], after)'
        ),
    },

    # ============================================================
    # insertif без направления
    # ============================================================
    {
        'name': 'insertif_missing_direction',
        'pattern': r'(?i)\binsertif\s*\([^,)]+\)',
        'reason': 'insertif требует before или after',
        'suggestion': (
            '❌  insertif(m[:, "Отдел"] == "IT")\n'
            '✅  insertif(m[:, "Отдел"] == "IT", after)\n'
            '✅  insertif(m[:, "Отдел"] == "IT", before)'
        ),
    },

    # ============================================================
    # matrixmod без действия
    # ============================================================
    {
        'name': 'matrixmod_missing_action',
        'pattern': r'(?i)\bmatrixmod\s*\([^,)]+,[^,)]+\)',
        'reason': 'matrixmod требует действие (delete, insert, duplicate, clear, keep, swap)',
        'suggestion': (
            '❌  matrixmod(m, [2, 4])\n'
            '✅  matrixmod(m, delete, 2)\n'
            '✅  matrixmod(m, delete, [2, 4])\n'
            '✅  matrixmod(m, insert, 2, before)\n'
            '✅  matrixmod(m, duplicate, 2, after)\n'
            '✅  matrixmod(m, clear, 3)\n'
            '✅  matrixmod(m, keep, [2, 4])\n'
            '✅  matrixmod(m, swap, [2, 5])'
        ),
    },

    # ============================================================
    # copy/move без направления
    # ============================================================
    {
        'name': 'copy_missing_direction',
        'pattern': r'(?i)\bcopy\s*\([^,)]+,[^,)]+\)',
        'reason': 'copy требует направление (before / after)',
        'suggestion': (
            '❌  copy(m[:, 1], m[:, 3])\n'
            '✅  copy(m[:, 1], m[:, 3], after)'
        ),
    },
    {
        'name': 'move_missing_direction',
        'pattern': r'(?i)\bmove\s*\([^,)]+,[^,)]+\)',
        'reason': 'move требует направление (before / after)',
        'suggestion': (
            '❌  move(m[:, 1], m[:, 3])\n'
            '✅  move(m[:, 1], m[:, 3], after)'
        ),
    },

    # ============================================================
    # pivot без agg
    # ============================================================
    {
        'name': 'pivot_missing_agg',
        'pattern': r'(?i)\bpivot\s*\([^,)]+,[^,)]+\)',
        'reason': 'pivot требует функцию агрегации (sum, avg, count, ...)',
        'suggestion': (
            '❌  pivot(m[:, "Отдел"], m[:, "Зарплата"])\n'
            '✅  pivot(m[:, "Отдел"], m[:, "Зарплата"], sum)\n'
            '\n'
            'Доступные: sum, avg, count, min, max,\n'
            '           median, first, last, std'
        ),
    },

    # ============================================================
    # date без выходного формата
    # ============================================================
    {
        'name': 'date_missing_format',
        'pattern': r'(?i)\bdate\s*\([^,)]+,[^,)]+\)',
        'reason': 'date требует ОБА формата: входной и выходной',
        'suggestion': (
            '❌  date("20.06.2025", "DD.MM.YYYY")\n'
            '✅  date("20.06.2025", "DD.MM.YYYY", "DD MMMM YYYY")\n'
            '\n'
            'date(данные, "входной", "выходной")'
        ),
    },

    # ============================================================
    # random вне присваивания
    # ============================================================
    {
        'name': 'random_misuse',
        'pattern': r'(?i)\bprint\s*\(\s*random\s*\(',
        'reason': 'random() нельзя использовать в print',
        'suggestion': (
            '❌  print(random(0:10, 0))\n'
            '✅  x = random(0:10, 0)\n'
            '    print(x)\n'
            '\n'
            'random работает ТОЛЬКО в присваивании:\n'
            '    x = random(0:10, 0)\n'
            '    m[all, all] = random(0:10, 0)'
        ),
    },

    # ============================================================
    # joinarray со срезом
    # ============================================================
    {
        'name': 'joinarray_with_slice',
        'pattern': r'(?i)\bjoinarray\s*\(\s*\w+\s*\[',
        'reason': 'joinarray работает только с ЦЕЛЫМИ матрицами',
        'suggestion': (
            '❌  joinarray(m[:, 1:3], b, vertical)\n'
            '✅  joinarray(m, b, vertical)\n'
            '\n'
            'Сначала извлеките данные в переменные:\n'
            '     col1 = m1[:, 2]\n'
            '     result = joinarray(col1, col2, horizontal)'
        ),
    },

    # ============================================================
    # unpivot без by
    # ============================================================
    {
        'name': 'unpivot_no_by',
        'pattern': r'(?i)\bunpivot\s*\([^,)]+\)',
        'reason': 'unpivot требует параметр "by"',
        'suggestion': (
            '❌  unpivot(m[:, 2:end])\n'
            '✅  unpivot(m[:, 2:end], by m[:, "Страна"])'
        ),
    },

    # ============================================================
    # OpenCSV с неверным режимом
    # ============================================================
    {
        'name': 'opencsv_bad_mode',
        'pattern': r'(?i)\bOpenCSV\s*\([^,)]+,\s*(?!BigData\b|Table\b)[A-Za-z]',
        'reason': 'Режим OpenCSV должен быть BigData или Table',
        'suggestion': (
            '❌  OpenCSV("f.csv", Auto)\n'
            '❌  OpenCSV("f.csv", Big)\n'
            '✅  OpenCSV("f.csv")               — авто\n'
            '✅  OpenCSV("f.csv", BigData)      — DuckDB\n'
            '✅  OpenCSV("f.csv", Table)        — RAM'
        ),
    },

    # ============================================================
    # find без условия
    # ============================================================
    {
        'name': 'find_missing_condition',
        'pattern': r'(?i)\bfind\s*\(\s*\)',
        'reason': 'find требует условие',
        'suggestion': (
            '❌  find()\n'
            '✅  find(m[:, "Отдел"] == "IT")\n'
            '✅  find(m[:, "Отдел"] == "IT", rows)\n'
            '✅  find(m[:, "Отдел"] == "IT", cols)'
        ),
    },

    # ============================================================
    # Зарезервированные слова как имена переменных
    # ============================================================
    {
        'name': 'reserved_word',
        'pattern': (
            r'^\s*('
            r'if|then|else|for|while|break|'
            r'and|or|not|true|false|null|'
            r'all|end|begin|last|'
            r'before|after|AZ|ZA|inside|ignore|approx|skip|'
            r'vertical|horizontal|when|'
            r'rows|cols|'
            r'delete|insert|duplicate|clear|keep|swap|'
            r'by|agg|having|'
            r'BigData|Table|'
            r'count|sum|min|max|avg|'
            r'trim|trimleft|trimright|'
            r'year|month|day|quarter|'
            r'weekday|weekdayname|monthname|'
            r'adddays|addmonths|addyears|datetrunc|'
            r'date|datediff|datenow|timenow'
            r')\s*=[^=]'
        ),
        'reason': 'ЗАРЕЗЕРВИРОВАННОЕ слово — нельзя использовать как имя переменной',
        'suggestion': (
            '❌  count = 0\n'
            '❌  sum = 10\n'
            '❌  rows = [2, 4]\n'
            '❌  cols = [1, 3]\n'
            '❌  delete = "x"\n'
            '❌  insert = 5\n'
            '❌  keep = [1, 2]\n'
            '❌  swap = 0\n'
            '❌  clear = null\n'
            '❌  duplicate = 1\n'
            '❌  by = "x"\n'
            '❌  when = true\n'
            '❌  year = 2025\n'
            '❌  month = 6\n'
            '❌  day = 20\n'
            '❌  adddays = 5\n'
            '❌  trim = ""\n'
            '\n'
            '✅  Используйте другие имена:\n'
            '     cnt   = 0\n'
            '     total = 10\n'
            '     r     = [2, 4]        ← rows → r\n'
            '     c     = [1, 3]        ← cols → c\n'
            '     r1    = [2, 4]        ← rows1 → r1\n'
            '     c1    = [1, 3]        ← cols1 → c1\n'
            '     del_  = "x"\n'
            '     ins_  = 5\n'
            '     keep_ = [1, 2]\n'
            '     swap_ = 0\n'
            '     clr   = null\n'
            '     dup   = 1\n'
            '     grp   = "x"\n'
            '     cond  = true\n'
            '     yr    = 2025          ← year → yr\n'
            '     mo    = 6             ← month → mo\n'
            '     dy    = 20            ← day → dy\n'
            '     add_d = 5             ← adddays → add_d\n'
            '     trim_ = ""            ← trim → trim_\n'
            '\n'
            'Зарезервированные слова:\n'
            '     if, then, else, for, while, break,\n'
            '     and, or, not, true, false, null,\n'
            '     all, end, begin, last, before, after,\n'
            '     AZ, ZA, inside, ignore, approx, skip,\n'
            '     vertical, horizontal, when,\n'
            '     rows, cols,\n'
            '     delete, insert, duplicate, clear, keep, swap,\n'
            '     by, agg, having,\n'
            '     BigData, Table,\n'
            '     count, sum, min, max, avg,\n'
            '     trim, trimleft, trimright,\n'
            '     year, month, day, quarter,\n'
            '     weekday, weekdayname, monthname,\n'
            '     adddays, addmonths, addyears, datetrunc,\n'
            '     date, datediff, datenow, timenow'
        ),
    },
]


# ============================================================
# ПРОВЕРКА ОДНОЙ СТРОКИ
# ============================================================
def check_source_line(line, line_number=None, source_code=None):
    """Проверяет одну строку."""
    if not line:
        return None

    stripped = line.strip()
    if not stripped or stripped.startswith('#'):
        return None

    if _is_python_line(stripped):
        return None

    is_case_line = _is_case_line(stripped)
    indent = len(line) - len(line.lstrip())

    for check in COMMON_CHECKS:
        if is_case_line and check['name'] in (
            'expression_not_used',
            'assign_in_condition',
        ):
            continue

        try:
            for match in re.finditer(check['pattern'], stripped):
                if _is_inside_string(stripped, match.start()):
                    continue

                column = indent + match.start()

                ctx = ErrorContext(
                    line=line_number,
                    column=column,
                    source_line=line,
                    source_code=source_code,
                )

                return ArrayVatorError(
                    code=f"SYNTAX_{check['name'].upper()}",
                    context=ctx,
                    message=check['reason'],
                    suggestion=check.get('suggestion', ''),
                )
        except re.error:
            continue

    return None


# ============================================================
# ПРОВЕРКА ВСЕХ СТРОК
# ============================================================
def check_all_lines(source_code):
    """Проверяет все строки."""
    if not source_code:
        return None

    lines = source_code.split('\n')

    for i, line in enumerate(lines, 1):
        error = check_source_line(line, i, source_code)
        if error:
            return error

    return None


# ============================================================
# ПОИСК ПОДСКАЗКИ
# ============================================================
def find_hint(source_line):
    """Ищет подсказку для строки (без выброса ошибки)."""
    if not source_line:
        return None

    stripped = source_line.strip()
    if not stripped:
        return None

    if _is_python_line(stripped):
        return None

    is_case_line = _is_case_line(stripped)

    for check in COMMON_CHECKS:
        if is_case_line and check['name'] in (
            'expression_not_used',
            'assign_in_condition',
        ):
            continue

        try:
            for match in re.finditer(check['pattern'], stripped):
                if _is_inside_string(stripped, match.start()):
                    continue

                return {
                    'reason': check['reason'],
                    'suggestion': check.get('suggestion', ''),
                }
        except re.error:
            continue

    return None