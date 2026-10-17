# parser/statements.py
"""
Парсинг операторов.

ВСЕ функции возвращают значение.
Мутация — только через явное присваивание.
"""

from operators import assign, if_stmt, for_loop, while_loop, break_stmt, print_stmt, input_stmt
from ast_nodes import PrintShowNode
from ast_nodes.base import TryNode
from errors import ArrayVatorError
from .expressions import parse_expression
from .base import Parser


# ============================================================
# СПИСКИ ФУНКЦИЙ
# ============================================================

MUTATING_FUNCTIONS = set()


REQUIRE_ASSIGNMENT_FUNCTIONS = {
    'FILTERIF', 'DELETEIF', 'DELETE',
    'SORT',
    'UNIQUE', 'DELETE_DUPLICATE',
    'REPLACETEXT',
    'DELETETEXTLEFT', 'DELETETEXTRIGHT',
    'CLEAN',
    'DATE',
    'CASE',
    'INSERT', 'COPY', 'MOVE', 'JOINARRAY', 'TRANSPOSE',
    'MATRIXMOD',
    'INSERTIF',
    'ROUND', 'INT', 'FRAC', 'FRAC_DIGITS',
    'PIVOT',
    'FILL',

    # НОВЫЕ АНАЛИТИЧЕСКИЕ
    'ABC',
    'PERCENTOF',
    'ANOMALY',

    # УСЛОВНЫЕ АГРЕГАТЫ (НОВОЕ)
    'SUMIF', 'COUNTIF', 'AVGIF', 'MINIF', 'MAXIF',
    'MEDIANIF', 'COUNTUNIQUEIF', 'SUMPRODUCT',

    'FIND', 'VALUE_COUNTS',
    'SPLIT', 'RANGE', 'VECTOR', 'ZEROS', 'ONES', 'MATRIX', 'JOINVECTOR',
    'FILLNA', 'DROPNA', 'COALESCE', 'NULL_IF',
    'DATENOW', 'TIMENOW',
    'TYPE', 'IS_NULL', 'IS_NUMBER', 'IS_INTEGER', 'IS_FLOAT',
    'IS_STRING', 'IS_BOOLEAN', 'TO_STRING', 'TO_NUMBER',
    'OPENEXCEL', 'OPENCSV', 'OPENTXT', 'OPENSQLITE',
    'OPENEXCELSHOW', 'OPENCSVSHOW', 'OPENTXTSHOW', 'OPENSQLITESHOW',
    'INPUTSHOW', 'INPUTSHOWFORM', 'INPUTLISTSHOW',
    'INPUTINMATRIX',

    'TOMATRIX', 'TOBIGDATA',
    'CONVERT_BIGDATA_TO_MATRIX', 'CONVERT_MATRIX_TO_BIGDATA',

    'UNPIVOT',
    'GROUPBY',
    'GROUPAGG',
    'FILLDOWN',
    'ADDCOLUMN',
    'ADDROWS',
    'SAMPLE',
    'APPLYIF',
    'JOIN',

    'ROWNUMBER', 'RANK', 'DENSERANK', 'PERCENTRANK',
    'CUMEDIST', 'NTILE', 'LAG', 'LEAD',
    'FIRSTVALUE', 'LASTVALUE', 'NTHVALUE',
    'WINSUM', 'WINAVG', 'WINCOUNT', 'WINMIN',
    'WINMAX', 'WINMEDIAN', 'WINSTDEV',
    'QUALIFY',
}


# ============================================================
# СПЕЦИФИЧНЫЕ ПОДСКАЗКИ ДЛЯ ФУНКЦИЙ
# ============================================================
# Для некоторых функций общая подсказка «r = func(...)» не подходит.
# Ниже — специфичные тексты, которые заменяют общий шаблон.
# ============================================================
CUSTOM_ASSIGNMENT_HINTS = {
    # ------------------------------------------------------------
    # InputInMatrix
    # ------------------------------------------------------------
    'INPUTINMATRIX': (
        "InputInMatrix: результат нужно сохранить.\n"
        "  Функция возвращает НОВУЮ матрицу с добавленными строками.\n"
        "  Исходная матрица НЕ изменяется.\n"
        "\n"
        "  ❌  Неправильно:\n"
        "     InputInMatrix(m, \"Сотрудники\")     ← результат теряется\n"
        "\n"
        "  ✅  Правильно:\n"
        "     m = InputInMatrix(m, \"Сотрудники\")\n"
        "\n"
        "  Что делает:\n"
        "     Открывает окно с последними N строками таблицы\n"
        "     и полями ввода по числу столбцов.\n"
        "     Кнопка «Добавить» — строка появляется в таблице (жёлтая).\n"
        "     Кнопка «Завершить» — возвращает новую матрицу.\n"
        "\n"
        "  Примеры:\n"
        "     ✅  m = InputInMatrix(m)\n"
        "     ✅  m = InputInMatrix(m, \"Сотрудники\")\n"
        "     ✅  m = InputInMatrix(m, \"Сотрудники\", 5)"
    ),

    # ------------------------------------------------------------
    # InputListShow
    # ------------------------------------------------------------
    'INPUTLISTSHOW': (
        "InputListShow: результат нужно сохранить (даже если он None).\n"
        "  Функция пишет значения в переменные/ячейки, а не возвращает их.\n"
        "  Парсер требует присваивания — используйте dummy.\n"
        "\n"
        "  ❌  Неправильно:\n"
        "     InputListShow(\"Имя\", name, \"Возраст\", age)\n"
        "\n"
        "  ✅  Правильно:\n"
        "     dummy = InputListShow(\"Имя\", name, \"Возраст\", age)\n"
        "\n"
        "  dummy = None — это заглушка для парсера.\n"
        "  Значения name и age уже записаны в переменные."
    ),

    # ------------------------------------------------------------
    # InputShow
    # ------------------------------------------------------------
    'INPUTSHOW': (
        "InputShow: результат нужно сохранить.\n"
        "  Функция возвращает значение (число, строку или матрицу).\n"
        "\n"
        "  ❌  Неправильно:\n"
        "     InputShow(\"Введите имя:\")     ← результат теряется\n"
        "\n"
        "  ✅  Правильно:\n"
        "     name = InputShow(\"Введите имя:\")\n"
        "     x = InputShow(\"Введите число:\", \"число\")\n"
        "     m = InputShow(\"Матрица:\", \"матрица\")"
    ),

    # ------------------------------------------------------------
    # InputShowForm
    # ------------------------------------------------------------
    'INPUTSHOWFORM': (
        "InputShowForm: результат нужно сохранить.\n"
        "  Функция возвращает вектор введённых значений.\n"
        "\n"
        "  ❌  Неправильно:\n"
        "     InputShowForm(\"Анкета\", \"Имя\", \"Возраст\")\n"
        "\n"
        "  ✅  Правильно:\n"
        "     data = InputShowForm(\"Анкета\", \"Имя\", \"Возраст\")\n"
        "     m[end+1, :] = InputShowForm(\"Сотрудник\", \"Имя\", \"Отдел\")"
    ),

    # ------------------------------------------------------------
    # Delete / DeleteIf
    # ------------------------------------------------------------
    'DELETE': (
        "delete: результат нужно сохранить.\n"
        "  Функция возвращает НОВУЮ матрицу без строк/столбцов.\n"
        "\n"
        "  ❌  Неправильно:\n"
        "     delete(m[2, :])           ← результат теряется\n"
        "\n"
        "  ✅  Правильно:\n"
        "     m = delete(m[2, :])       ← удалить строку 2\n"
        "     m = delete(m[:, \"Имя\"])   ← удалить столбец"
    ),

    'DELETEIF': (
        "deleteif: результат нужно сохранить.\n"
        "  Функция возвращает НОВУЮ матрицу без строк по условию.\n"
        "\n"
        "  ❌  Неправильно:\n"
        "     deleteif(m[:, \"Пол\"] == \"Ж\")\n"
        "\n"
        "  ✅  Правильно:\n"
        "     m = deleteif(m[:, \"Пол\"] == \"Ж\")\n"
        "     r = deleteif(m[:, \"Возраст\"] < 18)"
    ),

    # ------------------------------------------------------------
    # FilterIf
    # ------------------------------------------------------------
    'FILTERIF': (
        "filterif: результат нужно сохранить.\n"
        "  Функция возвращает НОВУЮ матрицу с отфильтрованными строками.\n"
        "\n"
        "  ❌  Неправильно:\n"
        "     filterif(m[:, \"Отдел\"] == \"IT\")\n"
        "\n"
        "  ✅  Правильно:\n"
        "     r = filterif(m[:, \"Отдел\"] == \"IT\")\n"
        "     m = filterif(m[:, \"Зарплата\"] > 50000)"
    ),

    # ------------------------------------------------------------
    # Sort
    # ------------------------------------------------------------
    'SORT': (
        "sort: результат нужно сохранить.\n"
        "  Функция возвращает НОВУЮ отсортированную матрицу.\n"
        "\n"
        "  ❌  Неправильно:\n"
        "     sort(m[:, \"Имя\"], AZ)\n"
        "\n"
        "  ✅  Правильно:\n"
        "     m = sort(m[:, \"Имя\"], AZ)\n"
        "     r = sort(m[:, \"Зарплата\"], ZA)"
    ),

    # ------------------------------------------------------------
    # Find
    # ------------------------------------------------------------
    'FIND': (
        "find: результат нужно сохранить.\n"
        "  Функция возвращает координаты, строки или столбцы.\n"
        "\n"
        "  ❌  Неправильно:\n"
        "     find(m[:, \"Имя\"] == \"Аня\")\n"
        "\n"
        "  ✅  Правильно:\n"
        "     r = find(m[:, \"Имя\"] == \"Аня\")\n"
        "     pos = find(m[:, \"Отдел\"] == \"IT\", rows)\n"
        "     cols = find(m[:, \"Отдел\"] == \"IT\", cols)"
    ),

    # ------------------------------------------------------------
    # AddColumn / AddRows
    # ------------------------------------------------------------
    'ADDCOLUMN': (
        "addcolumn: результат нужно сохранить.\n"
        "  Функция возвращает НОВУЮ матрицу с добавленным столбцом.\n"
        "\n"
        "  ❌  Неправильно:\n"
        "     addcolumn(m, \"Сумма\", m[:, \"ID\"] * 2)\n"
        "\n"
        "  ✅  Правильно:\n"
        "     m2 = addcolumn(m, \"Сумма\", m[:, \"ID\"] * 2)\n"
        "     m = addcolumn(m, \"Год\", year(m[:, \"Дата\"]))"
    ),

    'ADDROWS': (
        "addrows: результат нужно сохранить.\n"
        "  Функция возвращает НОВУЮ матрицу с добавленными строками.\n"
        "\n"
        "  ❌  Неправильно:\n"
        "     addrows(m, 5)\n"
        "\n"
        "  ✅  Правильно:\n"
        "     m = addrows(m, 5)            — 5 пустых строк\n"
        "     m = addrows(m, 3, 0)         — 3 строки со значениями 0"
    ),

    # ------------------------------------------------------------
    # MatrixMod
    # ------------------------------------------------------------
    'MATRIXMOD': (
        "matrixmod: результат нужно сохранить.\n"
        "  Функция возвращает НОВУЮ матрицу.\n"
        "\n"
        "  ❌  Неправильно:\n"
        "     matrixmod(m, delete, 2)\n"
        "\n"
        "  ✅  Правильно:\n"
        "     m = matrixmod(m, delete, 2)\n"
        "     m = matrixmod(m, insert, 2, before)\n"
        "     m = matrixmod(m, keep, [1, 3, 5])"
    ),

    # ------------------------------------------------------------
    # Insert / InsertIf
    # ------------------------------------------------------------
    'INSERT': (
        "insert: результат нужно сохранить.\n"
        "  Функция возвращает НОВУЮ матрицу.\n"
        "\n"
        "  ❌  Неправильно:\n"
        "     insert(m[2, :], before)\n"
        "\n"
        "  ✅  Правильно:\n"
        "     m = insert(m[2, :], before)\n"
        "     m = insert(m[:, 3], after)"
    ),

    'INSERTIF': (
        "insertif: результат нужно сохранить.\n"
        "  Функция возвращает НОВУЮ матрицу.\n"
        "\n"
        "  ❌  Неправильно:\n"
        "     insertif(m[:, \"Отдел\"] == \"IT\", after)\n"
        "\n"
        "  ✅  Правильно:\n"
        "     m = insertif(m[:, \"Отдел\"] == \"IT\", after)\n"
        "     r = insertif(m[:, \"Возраст\"] > 25, before)"
    ),
}


# ============================================================
# PARSE_STATEMENT
# ============================================================

def parse_statement(self):
    token = self.peek()
    if not token:
        return None
    token_type = token[0]

    # ============================================================
    # TRY / CATCH
    # ============================================================
    if token_type == 'TRY':
        return parse_try(self)

    # ============================================================
    # ОПЕРАТОРЫ
    # ============================================================
    if token_type == 'PRINT':
        return print_stmt.parse_print(self)
    elif token_type == 'PRINTLN':
        return print_stmt.parse_println(self)
    elif token_type == 'PRINT_SHOW':
        return parse_print_show(self)
    elif token_type == 'CHART':
        return parse_chart_statement(self)
    elif token_type in ('REPORT', 'REPORT_SECTION', 'REPORT_TEXT',
                        'REPORT_TABLE', 'REPORT_CHART', 'REPORT_SAVE',
                        'REPORT_SHOW', 'REPORT_SAVE_PDF'):
        return parse_report_statement(self)
    elif token_type == 'IF':
        return if_stmt.parse_if(self)
    elif token_type == 'WHILE':
        return while_loop.parse_while(self)
    elif token_type == 'FOR':
        return for_loop.parse_for(self)
    elif token_type == 'BREAK':
        self.expect('BREAK')
        return break_stmt.BreakNode()
    elif token_type == 'INPUT':
        return input_stmt.parse_input(self)

    # ============================================================
    # ФУНКЦИИ, ТРЕБУЮЩИЕ ПРИСВАИВАНИЯ
    # ============================================================
    if token_type in REQUIRE_ASSIGNMENT_FUNCTIONS:
        save_pos = self.pos

        result = assign.parse_assign(self)
        if result:
            return result

        self.pos = save_pos
        func_name = token_type.lower()

        # ------------------------------------------------------------
        # Специфичная подсказка?
        # ------------------------------------------------------------
        custom = CUSTOM_ASSIGNMENT_HINTS.get(token_type)
        if custom is not None:
            raise ArrayVatorError(
                code="FUNCTION_REQUIRES_ASSIGNMENT",
                context=self._get_context(token),
                message=(
                    f"{func_name}() возвращает значение — "
                    f"результат нужно сохранить."
                ),
                suggestion=custom,
            )

        # ------------------------------------------------------------
        # Общая подсказка
        # ------------------------------------------------------------
        raise ArrayVatorError(
            code="FUNCTION_REQUIRES_ASSIGNMENT",
            context=self._get_context(token),
            message=(
                f"{func_name}() возвращает значение — "
                f"результат нужно сохранить."
            ),
            suggestion=(
                f"Правильно:\n"
                f"     r = {func_name}(...)         — в новую переменную\n"
                f"     m = {func_name}(m, ...)      — мутация через присваивание в себя\n"
                f"     print({func_name}(...))      — вывод результата"
            ),
        )

    # ============================================================
    # IDENTIFIER / ОСТАЛЬНОЕ
    # ============================================================
    if token_type == 'IDENTIFIER':
        save_pos = self.pos
        result = assign.parse_assign(self)
        if result:
            return result
        self.pos = save_pos

    return parse_expression(self)


# ============================================================
# TRY / CATCH
# ============================================================

def parse_try(self):
    self.expect('TRY')

    try_body = []
    self.expect('LBRACE')
    while not self.check('RBRACE') and self.peek():
        stmt = parse_statement(self)
        if stmt:
            try_body.append(stmt)
    self.expect('RBRACE')

    if not self.check('CATCH'):
        raise ArrayVatorError(
            code="MISSING_CATCH",
            context=self._get_context(),
            message="После try { ... } ожидается catch { ... }.",
        )
    self.expect('CATCH')

    var_name = 'error'
    if self.check('LPAREN'):
        self.expect('LPAREN')
        if self.check('IDENTIFIER'):
            var_name = self.expect('IDENTIFIER')[1]
        self.expect('RPAREN')

    catch_body = []
    self.expect('LBRACE')
    while not self.check('RBRACE') and self.peek():
        stmt = parse_statement(self)
        if stmt:
            catch_body.append(stmt)
    self.expect('RBRACE')

    return TryNode(try_body, catch_body, var_name)


# ============================================================
# PRINT_SHOW
# ============================================================

def parse_print_show(self):
    self.expect('PRINT_SHOW')
    self.expect('LPAREN')
    data = parse_expression(self)

    title = None
    if self.check('COMMA'):
        self.expect('COMMA')
        title = parse_expression(self)

    self.expect('RPAREN')
    return PrintShowNode(data, title)


# ============================================================
# CHART (как оператор, без присваивания)
# ============================================================

def parse_chart_statement(self):
    from .parse_functions.chart import parse_chart

    self.expect('CHART')
    return parse_chart(self)


# ============================================================
# REPORT (как оператор, без присваивания)
# ============================================================

def parse_report_statement(self):
    from .parse_functions.report import (
        parse_report,
        parse_report_section,
        parse_report_text,
        parse_report_table,
        parse_report_chart,
        parse_report_save,
        parse_report_show,
        parse_report_save_pdf,
    )

    token_type = self.peek()[0]
    self.pos += 1

    if token_type == 'REPORT':
        return parse_report(self)
    elif token_type == 'REPORT_SECTION':
        return parse_report_section(self)
    elif token_type == 'REPORT_TEXT':
        return parse_report_text(self)
    elif token_type == 'REPORT_TABLE':
        return parse_report_table(self)
    elif token_type == 'REPORT_CHART':
        return parse_report_chart(self)
    elif token_type == 'REPORT_SAVE':
        return parse_report_save(self)
    elif token_type == 'REPORT_SHOW':
        return parse_report_show(self)
    elif token_type == 'REPORT_SAVE_PDF':
        return parse_report_save_pdf(self)

    raise ArrayVatorError(
        code="UNEXPECTED_TOKEN",
        context=self._get_context(),
        message=f"Неизвестный оператор отчёта: {token_type}",
    )


# ============================================================
# ПРИВЯЗКА К PARSER
# ============================================================

Parser.parse_statement = parse_statement
Parser.parse_try = parse_try
Parser.parse_print_show = parse_print_show
Parser.parse_chart_statement = parse_chart_statement
Parser.parse_report_statement = parse_report_statement