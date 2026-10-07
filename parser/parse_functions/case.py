# parser/parse_functions/case.py
"""
Парсинг CASE (только программист).

СИНТАКСИС:
    case(s[:, "Возраст"], when < 18 then "Дитя", else "Взрослый")
    case(s[2:5, "Возраст"], when < 18 then "Дитя", else "Взрослый")
    v = case(s[:, "Возраст"], when < 18 then "Дитя", else "Взрослый")
    s[:, end+1] = case(s[:, "Возраст"], when < 18 then "Дитя", else "Взрослый")

ФОРМАТЫ WHEN:
    when < 18 then "X"
    when > 50 then "X"
    when <= 30 then "X"
    when >= 18 then "X"
    when == "IT" then "X"
    when != "X" then "Y"
"""

from ast_nodes import CaseNode, StringNode, BinaryOp, VariableNode
from errors import ArrayVatorError


def _parse_when_condition(self):
    """
    Парсит условие в when.
    Форматы:
        < 18
        > 50
        <= 30
        >= 18
        == "IT"
        != "X"
    """
    op_token = self.peek()

    # ============================================================
    # ПРОВЕРКА: '=' (присваивание) вместо '==' (сравнение)
    # ============================================================
    if op_token and op_token[0] == 'ASSIGN':
        raise ArrayVatorError(
            code="CASE_ASSIGN_IN_CONDITION",
            context=self._get_context(op_token),
        )

    if op_token and op_token[0] in ['LESS', 'GREATER', 'LESSEQUAL',
                                    'GREATEREQUAL', 'EQUALS', 'NOTEQUAL']:
        op_type = op_token[0]
        self.expect(op_type)

        right = self.parse_expression()

        # BinaryOp с плейсхолдером _value
        left = VariableNode('_value')
        return BinaryOp(op_type, left, right)

    # Иначе — обычное выражение
    return self.parse_expression()


def parse_case(self):
    """Парсинг CASE (только программист)"""
    self.expect('LPAREN')

    # ============================================================
    # 1. Данные (срез или вектор)
    # ============================================================
    save_pos = self.pos
    try:
        data = self.parse_primary()
    except Exception:
        self.pos = save_pos
        data = self.parse_expression()

    # ============================================================
    # 2. Запятая после среза
    # ============================================================
    if not self.check('COMMA'):
        raise ArrayVatorError(
            code="CASE_BAD_SYNTAX",
            context=self._get_context(),
        )
    self.expect('COMMA')

    # ============================================================
    # 3. WHEN / ELSE
    # ============================================================
    whens = []
    else_value = None
    seen_else = False

    while not self.check('RPAREN'):
        # ============================================================
        # WHEN
        # ============================================================
        if self.check('WHEN'):
            if seen_else:
                raise ArrayVatorError(
                    code="CASE_BAD_ELSE",
                    context=self._get_context(),
                )

            self.expect('WHEN')

            condition = _parse_when_condition(self)

            # Проверка на 'then'
            if not self.check('THEN'):
                raise ArrayVatorError(
                    code="CASE_NO_THEN",
                    context=self._get_context(),
                )
            self.expect('THEN')

            result_expr = self.parse_expression()
            whens.append((condition, result_expr))

        # ============================================================
        # ELSE
        # ============================================================
        elif self.check('ELSE'):
            if seen_else:
                raise ArrayVatorError(
                    code="CASE_BAD_ELSE",
                    context=self._get_context(),
                )

            self.expect('ELSE')
            else_value = self.parse_expression()
            seen_else = True

        # ============================================================
        # Ни WHEN, ни ELSE — ошибка
        # ============================================================
        else:
            raise ArrayVatorError(
                code="CASE_BAD_SYNTAX",
                context=self._get_context(),
            )

        # Запятая между блоками (опционально перед RPAREN)
        if self.check('COMMA'):
            self.expect('COMMA')

    self.expect('RPAREN')

    # ============================================================
    # 4. Проверка: хотя бы один WHEN
    # ============================================================
    if not whens:
        raise ArrayVatorError(
            code="CASE_NO_WHEN",
            context=self._get_context(),
        )

    return CaseNode(data, column=None, whens=whens, else_value=else_value)