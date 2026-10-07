# parser/base.py
"""
Базовый класс парсера.
Все ошибки бросаются через ArrayVatorError с кодами и координатами.
Токены — тройки: (type, value, line).
"""

from errors import ArrayVatorError, ErrorContext


# ============================================================
# ИМПОРТ БАЗЫ ПОДСКАЗОК
# ============================================================
try:
    from errors.syntax_hints import get_hint as get_syntax_hint
    SYNTAX_HINTS_AVAILABLE = True
except ImportError:
    SYNTAX_HINTS_AVAILABLE = False
    def get_syntax_hint(expected_token, context=None, source_line=None):
        return None


class Parser:
    def __init__(self, tokens, source=None):
        self.tokens = tokens
        self.pos = 0
        self.current_line = 1
        self.source = source

    # ============================================================
    # БАЗОВЫЕ МЕТОДЫ
    # ============================================================

    def peek(self, offset=0):
        """
        Возвращает токен на позиции self.pos + offset.
        offset по умолчанию 0 — текущий токен.
        Возвращает None, если вышли за пределы.
        """
        pos = self.pos + offset
        return self.tokens[pos] if pos < len(self.tokens) else None

    def peek_type(self):
        token = self.peek()
        return token[0] if token else None

    def check(self, token_type):
        token = self.peek()
        return token and token[0] == token_type

    # ============================================================
    # ПОЗИЦИЯ И КОНТЕКСТ
    # ============================================================

    def _get_token_line(self, token):
        if token and len(token) >= 3:
            return token[2]
        return self.current_line

    def _get_context(self, token=None):
        if token is None:
            token = self.peek()

        line = self._get_token_line(token)
        column = None
        source_line = None

        if self.source and line is not None:
            lines = self.source.split('\n')
            if 0 < line <= len(lines):
                source_line = lines[line - 1]

        return ErrorContext(
            line=line,
            column=column,
            source_line=source_line,
            source_code=self.source,
            token=token,
        )

    # ============================================================
    # ОПРЕДЕЛЕНИЕ КОНТЕКСТА ПО ИСХОДНОЙ СТРОКЕ
    # ============================================================

    def _detect_context(self, expected_type):
        """
        Определяет контекст ошибки по исходной строке.
        Возвращает 'FOR', 'IF', 'WHILE', 'FUNCTION' или None.
        """
        if not self.source:
            return None

        token = self.peek()
        line = self._get_token_line(token) if token else self.current_line

        lines = self.source.split('\n')
        if not (0 < line <= len(lines)):
            return None

        source_line = lines[line - 1].strip()
        line_lower = source_line.lower()

        # Определяем контекст
        if line_lower.startswith('for '):
            return 'FOR'
        if line_lower.startswith('while '):
            return 'WHILE'
        if line_lower.startswith('if '):
            return 'IF'

        # Функции
        KNOWN_FUNCS = [
            'filterif', 'deleteif', 'sort', 'find', 'vlookup', 'pivot',
            'case', 'unique', 'countdistinct', 'valuecounts', 'deleteduplicate',
            'deletetextleft', 'deletetextright', 'replacetext',
            'sum', 'min', 'max', 'avg', 'len', 'lenrow', 'lencol',
            'round', 'int', 'frac', 'frac_digits', 'clean',
            'split', 'join', 'matrix', 'vector', 'zeros', 'ones',
            'range', 'fill', 'random', 'transpose',
            'copy', 'move', 'joinarray', 'insert',
            'print', 'println', 'printshow', 'input',
            'datenow', 'timenow', 'datediff',
            'abc', 'percentof', 'anomaly',
        ]
        for fn in KNOWN_FUNCS:
            if fn + '(' in line_lower or f' {fn} ' in f' {line_lower} ':
                return 'FUNCTION'

        return None

    # ============================================================
    # ОЖИДАНИЕ ТОКЕНА
    # ============================================================

    def expect(self, token_type):
        token = self.peek()

        if token and token[0] == token_type:
            self.pos += 1
            return token

        # ============================================================
        # Особая проверка: ожидали COMMA, а получили SEMICOLON
        # ============================================================
        if token_type == 'COMMA' and token and token[0] == 'SEMICOLON':
            ctx = self._get_context(token)
            raise ArrayVatorError(
                code="SEMICOLON_INSTEAD_OF_COMMA",
                context=ctx,
                message=(
                    "Используется ';' (разделитель строк), а нужна ЗАПЯТАЯ ','.\n"
                    "  ';' применяется только ВНУТРИ [...] для матриц."
                ),
                suggestion=(
                    "Замените ';' на ',' в аргументах:\n"
                    "     ❌  filterif(s; column \"Пол\" == \"Ж\")\n"
                    "     ✅  filterif(s, column \"Пол\" == \"Ж\")\n"
                    "\n"
                    "     ❌  print(a; b)\n"
                    "     ✅  print(a, b)"
                ),
            )

        # ============================================================
        # ГЛАВНОЕ: собираем контекст и подсказку
        # ============================================================
        code = self._get_missing_code(token_type)
        ctx = self._get_context(token)
        suggestion = self._get_suggestion(token, token_type)
        message = self._get_message(token, token_type)

        # Если ожидали LPAREN в контексте FOR — спец. код
        if token_type == 'LPAREN':
            context = self._detect_context('LPAREN')
            if context == 'FOR':
                code = 'FOR_MISSING_LPAREN'
            elif context == 'WHILE':
                code = 'WHILE_BAD_SYNTAX'
            elif context == 'FUNCTION':
                code = 'FUNCTION_MISSING_LPAREN'

        raise ArrayVatorError(
            code=code,
            context=ctx,
            message=message,
            suggestion=suggestion,
        )

    # ============================================================
    # ПРОВЕРКА: ПРОПУЩЕНА ЗАПЯТАЯ
    # ============================================================

    def _check_missing_comma(self, func_name, first_arg_desc="первым аргументом"):
        if self.check('COMMA'):
            return

        next_token = self.peek()
        if not next_token:
            return

        keywords_list = []
        try:
            from syntax.signatures import get_signature_keywords
            keywords_list = get_signature_keywords(func_name)
        except ImportError:
            pass

        keywords = {kw.upper(): kw for kw in keywords_list}

        COMMON_KEYWORDS = {
            'COLUMN': 'column', 'COL': 'col', 'ROW': 'row',
            'VALUES': 'values', 'COLS': 'cols',
            'BEFORE': 'before', 'AFTER': 'after',
            'AZ': 'AZ', 'ZA': 'ZA', 'APPROX': 'approx', 'SKIP': 'skip',
            'SUM': 'sum', 'AVG': 'avg', 'MIN': 'min', 'MAX': 'max', 'COUNT': 'count',
            'CELLS': 'cells', 'CELL': 'cell', 'RANGE': 'range',
            'WHEN': 'when', 'ELSE': 'else',
            'INSIDE': 'inside', 'IGNORE': 'ignore', 'ALL': 'all',
            'VERTICAL': 'vertical', 'HORIZONTAL': 'horizontal',
        }

        for k, v in COMMON_KEYWORDS.items():
            if k not in keywords:
                keywords[k] = v

        if next_token[0] in keywords:
            kw = keywords[next_token[0]]
            ctx = self._get_context(next_token)

            example_right = None
            try:
                from syntax.signatures import get_signature
                sig = get_signature(func_name)
                if sig and sig.get('examples'):
                    example_right = sig['examples'][0]
            except ImportError:
                pass

            suggestion = (
                f"После первого аргумента нужна ЗАПЯТАЯ:\n"
                f"     ❌  {func_name}(s {kw} ...)\n"
                f"     ✅  {func_name}(s, {kw} ...)"
            )

            if example_right:
                suggestion += f"\n\nПример:\n     {example_right}"

            raise ArrayVatorError(
                code="MISSING_COMMA",
                context=ctx,
                message=(
                    f"Пропущена запятая между {first_arg_desc} и '{kw}' "
                    f"в {func_name}()."
                ),
                suggestion=suggestion,
            )

    # ============================================================
    # ПАРСИНГ column N или row N
    # ============================================================

    def _parse_column_or_row(self, func_name):
        """
        Парсит 'column N' или 'row N'.
        Возвращает кортеж ('column', value_node) или ('row', value_node).
        Используется в copy, move.
        """
        from ast_nodes import StringNode

        token = self.peek()
        if not token:
            raise ArrayVatorError(
                code="EXPECTED_COLUMN_OR_ROW",
                context=self._get_context(),
                message=f"Ожидалось 'column' или 'row' в {func_name}().",
                suggestion=(
                    f"Пример:\n"
                    f"     {func_name}(m, column 1, column 10, after)"
                ),
            )

        # COLUMN
        if token[0] in ('COLUMN', 'COL'):
            self.expect(token[0])

            if self.check('ASSIGN'):
                self.expect('ASSIGN')

            value = self._parse_column_or_row_value(func_name, "column")
            return ('column', value)

        # ROW
        if token[0] == 'ROW':
            self.expect('ROW')

            if self.check('ASSIGN'):
                self.expect('ASSIGN')

            value = self._parse_column_or_row_value(func_name, "row")
            return ('row', value)

        raise ArrayVatorError(
            code="EXPECTED_COLUMN_OR_ROW",
            context=self._get_context(token),
            message=(
                f"Ожидалось 'column' или 'row' в {func_name}(), "
                f"получено '{token[0]}'."
            ),
            suggestion=(
                f"Примеры:\n"
                f"     {func_name}(m, column 1, column 10, after)\n"
                f"     {func_name}(m, row 2, row 5, before)"
            ),
        )

    def _parse_column_or_row_value(self, func_name, kind):
        """
        Парсит значение после 'column' или 'row'.
        Может быть: строка, число, end, end-1, end+1, last N, выражение.
        """
        from ast_nodes import StringNode, NumberNode

        next_token = self.peek()
        if not next_token:
            raise ArrayVatorError(
                code=f"EXPECTED_AFTER_{kind.upper()}",
                context=self._get_context(),
                message=f"После '{kind}' ожидается имя или номер.",
                suggestion=(
                    f"Примеры:\n"
                    f"     {kind} \"Имя\"\n"
                    f"     {kind} 3\n"
                    f"     {kind} end\n"
                    f"     {kind} last 2"
                ),
            )

        # Строка "Имя"
        if next_token[0] == 'STRING':
            val = StringNode(next_token[1])
            self.pos += 1
            return val

        # Число 3
        if next_token[0] == 'NUMBER':
            val = StringNode(str(int(next_token[1])))
            self.pos += 1
            return val

        # end
        if next_token[0] == 'END_KEYWORD':
            val = StringNode('end')
            self.pos += 1
            return val

        # end-1
        if next_token[0] == 'END_MINUS':
            val = StringNode(next_token[1])
            self.pos += 1
            return val

        # end+1
        if next_token[0] == 'END_PLUS':
            val = StringNode(next_token[1])
            self.pos += 1
            return val

        # last N
        if next_token[0] == 'LAST_KEYWORD':
            self.pos += 1
            next_num = self.peek()
            if next_num and next_num[0] == 'NUMBER':
                val = StringNode(f"last {next_num[1]}")
                self.pos += 1
                return val
            return StringNode('last')

        # IDENTIFIER (имя столбца без кавычек)
        if next_token[0] == 'IDENTIFIER':
            name = next_token[1]
            self.pos += 1
            if name.lower() in ('end', 'begin', 'all', 'last'):
                return StringNode(name.lower())
            return StringNode(name)

        # Иначе — выражение
        return self.parse_expression()

    # ============================================================
    # КОДЫ ОШИБОК
    # ============================================================

    def _get_missing_code(self, expected_type):
        mapping = {
            'RPAREN': 'MISSING_RPAREN',
            'LPAREN': 'MISSING_LPAREN',
            'RBRACKET': 'MISSING_RBRACKET',
            'LBRACKET': 'MISSING_LBRACKET',
            'RBRACE': 'MISSING_RBRACE',
            'LBRACE': 'MISSING_LBRACE',
            'THEN': 'MISSING_THEN',
            'COMMA': 'MISSING_COMMA',
            'COLON': 'MISSING_COLON',
            'ASSIGN': 'EXPECTED_ASSIGN',
            'IDENTIFIER': 'EXPECTED_IDENTIFIER',
            'EXPRESSION': 'EXPECTED_EXPRESSION',
        }
        return mapping.get(expected_type, 'UNEXPECTED_TOKEN')

    # ============================================================
    # СООБЩЕНИЯ
    # ============================================================

    def _get_message(self, token, expected_type):
        if token is None:
            return f"Неожиданный конец файла. Ожидался {expected_type}."

        token_names = {
            'RBRACKET': "']'",
            'LBRACKET': "'['",
            'RPAREN': "')'",
            'LPAREN': "'('",
            'RBRACE': "'}'",
            'LBRACE': "'{'",
            'ASSIGN': "'='",
            'EQUALS': "'=='",
            'THEN': "'then'",
            'COMMA': "','",
            'COLON': "':'",
            'SEMICOLON': "';'",
            'IDENTIFIER': "имя переменной",
            'NUMBER': "число",
            'STRING': "строку",
        }

        expected_name = token_names.get(expected_type, expected_type)
        got_name = token_names.get(token[0], token[0])

        if expected_type == 'RBRACKET' and token[0] == 'RPAREN':
            return (
                f"Не хватает закрывающей квадратной скобки ']'.\n"
                f"  Похоже, вы открыли индекс круглой скобкой '(', "
                f"а закрываете круглой ')'."
            )

        if expected_type == 'RBRACKET' and token[0] == 'ASSIGN':
            return (
                f"Не хватает закрывающей квадратной скобки ']' перед '='.\n"
                f"  Возможно, вы забыли закрыть индекс."
            )

        if expected_type == 'RBRACKET' and token[0] == 'COMMA':
            return (
                f"Не хватает закрывающей квадратной скобки ']' перед ','.\n"
                f"  Возможно, вы написали лишнюю запятую в индексе."
            )

        if expected_type == 'RPAREN' and token[0] == 'RBRACKET':
            return (
                f"Не хватает закрывающей круглой скобки ')'.\n"
                f"  Похоже, вы открыли скобку круглой '(', "
                f"а закрываете квадратной ']'."
            )

        if expected_type == 'RPAREN' and token[0] == 'ASSIGN':
            return (
                f"Не хватает закрывающей круглой скобки ')' перед '='.\n"
                f"  Возможно, вы забыли закрыть скобку."
            )

        if expected_type == 'RPAREN' and token[0] == 'LPAREN':
            return (
                f"Не хватает закрывающей круглой скобки ')'.\n"
                f"  Перед этой '(' нет закрывающей ')'."
            )

        if expected_type == 'LBRACKET' and token[0] == 'LPAREN':
            return (
                f"Ожидалась квадратная скобка '['.\n"
                f"  Для индексов используются квадратные скобки '[ ]', "
                f"а не круглые '( )'."
            )

        if expected_type == 'THEN':
            return "После условия 'if' ожидается ключевое слово 'then'."

        if expected_type == 'RBRACE':
            return (
                f"Не хватает закрывающей фигурной скобки '}}'.\n"
                f"  Возможно, вы забыли закрыть блок."
            )

        return f"Ожидался {expected_name}, получен {got_name}."

    # ============================================================
    # ГЛОБАЛЬНЫЙ ОБРАБОТЧИК ПОДСКАЗОК
    # ============================================================

    def _get_suggestion(self, token, expected_type):
        """
        Возвращает подсказку для любой ошибки.
        Приоритет:
            1. База syntax_hints.py (рабочий пример)
            2. Старые эвристики (по токену)
            3. None
        """
        # ============================================================
        # 1. База syntax_hints
        # ============================================================
        if SYNTAX_HINTS_AVAILABLE:
            context = self._detect_context(expected_type)

            source_line = None
            if self.source and token:
                line = self._get_token_line(token)
                lines = self.source.split('\n')
                if 0 < line <= len(lines):
                    source_line = lines[line - 1]

            hint = get_syntax_hint(expected_type, context, source_line)
            if hint:
                return hint

        # ============================================================
        # 2. Старые эвристики
        # ============================================================
        if not self.source:
            return None

        if expected_type == 'RBRACKET':
            if token and token[0] in ('ASSIGN', 'COMMA', 'RPAREN'):
                return (
                    "Для индексов используйте квадратные скобки:\n"
                    "     m[строка, столбец]        — элемент\n"
                    "     m[:,\"Пол\"]                — столбец\n"
                    "     m[last 2, 1]              — последние N строк"
                )
            return "Проверьте, все ли квадратные скобки закрыты."

        if expected_type == 'RPAREN':
            if token and token[0] == 'RBRACKET':
                return (
                    "Для функций используйте круглые скобки:\n"
                    "     deleteif(m, ...)          — функция\n"
                    "     filterif(m, ...)          — функция\n"
                    "     m[:,\"Пол\"]                — индекс"
                )
            return "Проверьте, все ли открытые скобки закрыты."

        if expected_type == 'RBRACE':
            return "Проверьте, все ли фигурные скобки закрыты."

        if expected_type == 'THEN':
            return (
                "После условия 'if' должно идти 'then':\n"
                "     if x > 5 then\n"
                "     {\n"
                "         ...\n"
                "     }"
            )

        if expected_type == 'COMMA':
            return "Проверьте разделители в списке аргументов."

        return None