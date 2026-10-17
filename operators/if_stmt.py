# operators/if_stmt.py
from ast_nodes import Node
from errors import ArrayVatorError


class IfNode(Node):
    def __init__(self, condition, then_body, else_body=None):
        self.condition = condition
        self.then_body = then_body
        self.else_body = else_body

    def execute(self, env):
        if self.condition.evaluate(env):
            for stmt in self.then_body:
                stmt.execute(env)
        elif self.else_body:
            for stmt in self.else_body:
                stmt.execute(env)

    def __repr__(self):
        return f"If({self.condition}, then={self.then_body}, else={self.else_body})"


def check_assign_in_range(parser, start_pos, end_pos, func_name="if"):
    """
    Проверяет, что в диапазоне токенов [start_pos, end_pos)
    И в первом токене сразу после условия нет ASSIGN ('=').

    Вызывается ПОСЛЕ parse_expression — когда уже известно,
    где заканчивается условие.

    Бросает:
        IF_ASSIGN_IN_CONDITION    — для if
        WHILE_ASSIGN_IN_CONDITION — для while
    """
    code = ("WHILE_ASSIGN_IN_CONDITION" if func_name == "while"
            else "IF_ASSIGN_IN_CONDITION")

    # ---- 1. Внутри условия ----
    for i in range(start_pos, end_pos):
        if i >= len(parser.tokens):
            break
        token = parser.tokens[i]
        if token[0] == 'ASSIGN':
            ctx = parser._get_context(token)
            raise ArrayVatorError(code=code, context=ctx)

    # ---- 2. Первый токен сразу после условия ----
    if end_pos < len(parser.tokens):
        next_token = parser.tokens[end_pos]
        if next_token[0] == 'ASSIGN':
            ctx = parser._get_context(next_token)
            raise ArrayVatorError(code=code, context=ctx)


def parse_if(parser):
    parser.expect('IF')

    # ============================================================
    # УСЛОВИЕ + проверка '=' в условии
    # ============================================================
    cond_start = parser.pos
    condition = parser.parse_expression()
    cond_end = parser.pos

    check_assign_in_range(parser, cond_start, cond_end, "if")

    # ============================================================
    # ПРОВЕРКА: 'then' после условия
    # ============================================================
    if not parser.check('THEN'):
        raise ArrayVatorError(
            code="IF_NO_THEN",
            context=parser._get_context(),
        )
    parser.expect('THEN')

    # ============================================================
    # ТЕЛО THEN
    # ============================================================
    then_body = []
    if parser.check('LBRACE'):
        parser.expect('LBRACE')
        while not parser.check('RBRACE') and parser.peek():
            stmt = parser.parse_statement()
            if stmt:
                then_body.append(stmt)
        parser.expect('RBRACE')
    else:
        stmt = parser.parse_statement()
        if stmt:
            then_body.append(stmt)

    # ============================================================
    # ТЕЛО ELSE (опционально)
    # ============================================================
    else_body = None
    if parser.check('ELSE'):
        parser.expect('ELSE')
        if parser.check('LBRACE'):
            parser.expect('LBRACE')
            else_body = []
            while not parser.check('RBRACE') and parser.peek():
                stmt = parser.parse_statement()
                if stmt:
                    else_body.append(stmt)
            parser.expect('RBRACE')
        else:
            stmt = parser.parse_statement()
            if stmt:
                else_body = [stmt]

    return IfNode(condition, then_body, else_body)