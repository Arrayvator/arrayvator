# parser/matrix.py
"""
Парсинг матриц и индексов.
Токены — тройки (type, value, line).
"""

from ast_nodes import IndexNode, MatrixNode, VariableNode, NumberNode, StringNode
from errors import ArrayVatorError
from .base import Parser
from .expressions import parse_expression


# ============================================================
# ХЕЛПЕР: проверка на запрещённые токены внутри [...]
# ============================================================
def _check_forbidden_in_index(self, token):
    """Проверяет, что внутри [...] нет column, row, ;."""
    if not token:
        return

    token_type = token[0]

    if token_type == 'COLUMN':
        ctx = self._get_context(token)
        raise ArrayVatorError(
            code="COLUMN_IN_PROGRAMMER_INDEX",
            context=ctx,
            message=(
                "В режиме программиста 'column' внутри [...] НЕ НУЖЕН.\n"
                "  Имя столбца указывается КАК СТРОКА."
            ),
            suggestion=(
                "✅  s[:, \"Успеваемость\"]\n"
                "✅  s[:, 7]\n"
                "\n"
                "Или используй режим аналитика (column СНАРУЖИ):\n"
                "✅  filterif(s, column \"Успеваемость\" == \"Отлично\")"
            ),
        )

    if token_type == 'ROW':
        ctx = self._get_context(token)
        raise ArrayVatorError(
            code="ROW_IN_PROGRAMMER_INDEX",
            context=ctx,
            message=(
                "В режиме программиста 'row' внутри [...] НЕ НУЖЕН.\n"
                "  Номер строки указывается ЧИСЛОМ."
            ),
            suggestion=(
                "✅  s[2, :]\n"
                "✅  s[2:5, 3]\n"
                "\n"
                "Или используй режим аналитика (row СНАРУЖИ):\n"
                "✅  delete(s, row 2)"
            ),
        )

    if token_type == 'SEMICOLON':
        ctx = self._get_context(token)
        raise ArrayVatorError(
            code="SEMICOLON_IN_INDEX",
            context=ctx,
            message=(
                "Внутри [...] используется ';' — это НЕВЕРНО.\n"
                "  ';' — разделитель СТРОК в матрице, а не индексов."
            ),
            suggestion=(
                "Для индекса используй ЗАПЯТУЮ:\n"
                "     ❌  s[2; 3]\n"
                "     ✅  s[2, 3]"
            ),
        )


def parse_index(self, matrix_name):
    """
    Парсит индекс вида A[...] или A[..., ...] [, inside | ignore].
    """
    indices = []
    open_token = self.peek()

    if open_token and open_token[0] == 'LPAREN':
        ctx = self._get_context(open_token)
        raise ArrayVatorError(
            code="EXPECTED_LBRACKET",
            context=ctx,
            message=(
                "Для индексов используются квадратные скобки '[ ]', "
                "а не круглые '( )'."
            ),
            suggestion=(
                "Замените круглые скобки на квадратные:\n"
                "     ❌  s(:,\"Пол\"]\n"
                "     ✅  s[:,\"Пол\"]"
            ),
        )

    self.expect('LBRACKET')
    next_token = self.peek()

    if next_token and next_token[0] == 'RBRACKET':
        ctx = self._get_context(open_token)
        raise ArrayVatorError(
            code="EMPTY_INDEX",
            context=ctx,
            message=(
                "Индекс не может быть пустым.\n"
                "  В квадратных скобках должно быть ЗНАЧЕНИЕ или "
                "ДВА ЗНАЧЕНИЯ через запятую."
            ),
            suggestion=(
                "Формат индекса:\n"
                "     A[строка, столбец]      — элемент\n"
                "     A[2, :]                 — вся строка 2\n"
                "     A[:, \"Имя\"]             — весь столбец \"Имя\""
            ),
        )

    if next_token and next_token[0] == 'COMMA':
        ctx = self._get_context(open_token)
        raise ArrayVatorError(
            code="EMPTY_INDEX_FIRST",
            context=ctx,
            message=(
                "Первое значение индекса не указано.\n"
                "  Перед запятой должно быть ЗНАЧЕНИЕ."
            ),
            suggestion=(
                "❌  s[, \"Пол\"]\n"
                "✅  s[:, \"Пол\"]       ← двоеточие = все строки"
            ),
        )

    if next_token and next_token[0] == 'SEMICOLON':
        ctx = self._get_context(next_token)
        raise ArrayVatorError(
            code="SEMICOLON_IN_INDEX",
            context=ctx,
            message=(
                "Внутри [...] используется ';' — это НЕВЕРНО.\n"
                "  ';' — разделитель СТРОК в матрице."
            ),
            suggestion=(
                "❌  s[;]\n"
                "✅  s[:, :]\n"
                "✅  s[2, 3]"
            ),
        )

    idx1 = parse_index_expression(self)
    indices.append(idx1)

    if self.check('COMMA'):
        self.expect('COMMA')
        after_comma = self.peek()
        if after_comma and after_comma[0] == 'RBRACKET':
            ctx = self._get_context(after_comma)
            raise ArrayVatorError(
                code="EMPTY_INDEX_SECOND",
                context=ctx,
                message=(
                    "Второе значение индекса не указано.\n"
                    "  После запятой должно быть ЗНАЧЕНИЕ."
                ),
                suggestion=(
                    "❌  s[2, ]\n"
                    "✅  s[2, :]         ← все столбцы\n"
                    "✅  s[2, 3]"
                ),
            )
        _check_forbidden_in_index(self, after_comma)
        idx2 = parse_index_expression(self)
        indices.append(idx2)

    elif self.check('SEMICOLON'):
        ctx = self._get_context(self.peek())
        raise ArrayVatorError(
            code="SEMICOLON_IN_INDEX",
            context=ctx,
            message=(
                "Внутри [...] используется ';' — это НЕВЕРНО.\n"
                "  ';' — разделитель СТРОК в матрице, а не индексов."
            ),
            suggestion=(
                "❌  s[2; 3]\n"
                "✅  s[2, 3]"
            ),
        )

    # ============================================================
    # НОВОЕ: модификаторы inside / ignore (после второго индекса)
    # ============================================================
    inside = False
    ignore = False

    while self.check('COMMA'):
        save_pos = self.pos
        self.expect('COMMA')
        mod_token = self.peek()

        if mod_token and mod_token[0] == 'INSIDE':
            self.expect('INSIDE')
            inside = True
        elif mod_token and mod_token[0] == 'IGNORE':
            self.expect('IGNORE')
            ignore = True
        else:
            self.pos = save_pos
            break

    close_token = self.peek()
    if close_token and close_token[0] == 'RPAREN':
        ctx = self._get_context(close_token)
        raise ArrayVatorError(
            code="MISSING_RBRACKET",
            context=ctx,
            message=(
                "Не хватает закрывающей квадратной скобки ']'.\n"
                "  Похоже, вы закрываете индекс круглой скобкой ')'."
            ),
            suggestion=(
                "❌  s[last 2, 1)\n"
                "✅  s[last 2, 1]"
            ),
        )

    self.expect('RBRACKET')
    return IndexNode(VariableNode(matrix_name), indices,
                     inside=inside, ignore=ignore)


def parse_index_expression(self):
    """Парсит выражение индекса (число, диапазон, ключевое слово)"""
    token = self.peek()
    if not token:
        raise SyntaxError("Неожиданный конец индекса")

    token_type = token[0]
    value = token[1]

    _check_forbidden_in_index(self, token)

    if token_type == 'COLON':
        self.pos += 1
        return StringNode('all')

    if token_type == 'END_PLUS':
        self.pos += 1
        return StringNode(value)

    if token_type == 'END_MINUS':
        self.pos += 1
        return StringNode(value)

    if token_type == 'IDENTIFIER' and value.lower() == 'last':
        self.pos += 1
        next_token = self.peek()
        if next_token and next_token[0] == 'NUMBER':
            self.pos += 1
            return StringNode(f"last {next_token[1]}")
        return StringNode('last')

    if token_type == 'IDENTIFIER' and value.lower() == 'end':
        self.pos += 1
        return StringNode('end')

    if token_type in ['ALL', 'BEGIN_KEYWORD', 'END_KEYWORD']:
        self.pos += 1
        return StringNode(value.lower())

    if token_type == 'LAST_KEYWORD':
        self.pos += 1
        next_token = self.peek()
        if next_token and next_token[0] == 'NUMBER':
            self.pos += 1
            return StringNode(f"last {next_token[1]}")
        return StringNode('last')

    if token_type == 'IDENTIFIER':
        self.pos += 1
        if value.lower() in ['end', 'begin', 'all', 'last']:
            return StringNode(value.lower())
        return VariableNode(value)

    if token_type == 'NUMBER':
        self.pos += 1
        start_value = value

        if self.check('COLON'):
            self.expect('COLON')
            end_token = self.peek()
            if not end_token:
                raise SyntaxError("Ожидалось значение после двоеточия")
            _check_forbidden_in_index(self, end_token)
            end_token_type = end_token[0]
            end_value = end_token[1]

            if end_token_type == 'NUMBER':
                self.pos += 1
                return StringNode(f"{start_value}:{end_value}")
            elif end_token_type == 'END_KEYWORD':
                self.pos += 1
                return StringNode(f"{start_value}:end")
            elif end_token_type == 'ALL':
                self.pos += 1
                return StringNode(f"{start_value}:all")
            elif end_token_type == 'IDENTIFIER' and end_value.lower() == 'end':
                self.pos += 1
                return StringNode(f"{start_value}:end")
            elif end_token_type == 'IDENTIFIER' and end_value.lower() == 'begin':
                self.pos += 1
                return StringNode(f"{start_value}:begin")
            elif end_token_type == 'IDENTIFIER' and end_value.lower() == 'all':
                self.pos += 1
                return StringNode(f"{start_value}:all")
            elif end_token_type == 'IDENTIFIER' and end_value.lower() == 'last':
                self.pos += 1
                next_tok = self.peek()
                if next_tok and next_tok[0] == 'NUMBER':
                    self.pos += 1
                    return StringNode(f"{start_value}:last {next_tok[1]}")
                return StringNode(f"{start_value}:last")
            elif end_token_type == 'LAST_KEYWORD':
                self.pos += 1
                next_tok = self.peek()
                if next_tok and next_tok[0] == 'NUMBER':
                    self.pos += 1
                    return StringNode(f"{start_value}:last {next_tok[1]}")
                return StringNode(f"{start_value}:last")
            elif end_token_type == 'END_PLUS':
                self.pos += 1
                return StringNode(f"{start_value}:{end_value}")
            elif end_token_type == 'END_MINUS':
                self.pos += 1
                return StringNode(f"{start_value}:{end_value}")
            elif end_token_type == 'COLON':
                self.pos += 1
                return StringNode(f"{start_value}:all")
            else:
                raise SyntaxError(f"Неверный диапазон: {start_value}:{end_value}")

        return NumberNode(start_value)

    if token_type == 'LPAREN':
        expr = self.parse_expression()
        return expr

    result = self.parse_expression()
    return result


def parse_matrix(self):
    """Парсит матрицу вида [1,2,3; 4,5,6]"""
    self.expect('LBRACKET')

    if self.check('RBRACKET'):
        self.expect('RBRACKET')
        return MatrixNode([], False)

    if self.check('SEMICOLON'):
        self.expect('SEMICOLON')
        self.expect('RBRACKET')
        return MatrixNode([], True)

    if self.check('LBRACKET'):
        nested_token = self.peek()
        ctx = self._get_context(nested_token)
        raise ArrayVatorError(
            code="NESTED_BRACKETS",
            context=ctx,
            message=(
                "Вложенные квадратные скобки '[' внутри матрицы — недопустимы.\n"
                "  ArrayVator не использует Python-синтаксис [[...], [...]].\n"
                "  Для матрицы используйте точку с запятой ';' как разделитель строк."
            ),
            suggestion=(
                "❌  [[11, 12], [13, 14]]\n"
                "✅  [11, 12; 13, 14]"
            ),
        )

    data = []
    first_row = []
    expr = self.parse_expression()
    first_row.append(expr)

    while self.check('COMMA'):
        self.expect('COMMA')
        if self.check('SEMICOLON'):
            break

        if self.check('LBRACKET'):
            nested_token = self.peek()
            ctx = self._get_context(nested_token)
            raise ArrayVatorError(
                code="NESTED_BRACKETS",
                context=ctx,
                message=(
                    "Вложенные квадратные скобки '[' внутри матрицы — недопустимы.\n"
                    "  Для матрицы используйте точку с запятой ';' как разделитель строк."
                ),
                suggestion=(
                    "❌  [[11, 12], [13, 14]]\n"
                    "✅  [11, 12; 13, 14]"
                ),
            )

        expr = self.parse_expression()
        first_row.append(expr)

    if self.check('SEMICOLON'):
        data.append(first_row)
        while self.check('SEMICOLON'):
            self.expect('SEMICOLON')
            if self.check('RBRACKET'):
                break
            new_row = []
            if not self.check('RBRACKET') and not self.check('SEMICOLON'):
                if self.check('LBRACKET'):
                    nested_token = self.peek()
                    ctx = self._get_context(nested_token)
                    raise ArrayVatorError(
                        code="NESTED_BRACKETS",
                        context=ctx,
                        message=(
                            "Вложенные квадратные скобки '[' внутри матрицы — недопустимы.\n"
                            "  Для матрицы используйте точку с запятой ';' как разделитель строк."
                        ),
                        suggestion=(
                            "❌  [[11, 12], [13, 14]]\n"
                            "✅  [11, 12; 13, 14]"
                        ),
                    )

                expr = self.parse_expression()
                new_row.append(expr)
                while self.check('COMMA'):
                    self.expect('COMMA')
                    if self.check('SEMICOLON') or self.check('RBRACKET'):
                        break
                    expr = self.parse_expression()
                    new_row.append(expr)
            data.append(new_row)
        self.expect('RBRACKET')
        return MatrixNode(data, True)
    else:
        self.expect('RBRACKET')
        return MatrixNode(first_row, False)


Parser.parse_index = parse_index
Parser._parse_index_expression = parse_index_expression
Parser.parse_matrix = parse_matrix