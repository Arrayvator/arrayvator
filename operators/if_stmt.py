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


def _check_assign_in_condition(parser, func_name="if"):
    """
    Проверяет, что в условии нет '=' (присваивания).
    Должно быть '==' (сравнение).

    Вызывается ДО parse_expression, иначе '=' уже не будет виден.

    Бросает:
        IF_ASSIGN_IN_CONDITION   — для if
        WHILE_ASSIGN_IN_CONDITION — для while
    """
    save_pos = parser.pos
    condition_tokens = []

    depth = 0
    while parser.peek():
        token = parser.peek()

        if token[0] == 'LPAREN':
            depth += 1
        elif token[0] == 'RPAREN':
            if depth == 0:
                break
            depth -= 1
        elif token[0] == 'THEN' and depth == 0:
            break
        elif token[0] == 'LBRACE' and depth == 0:
            break

        condition_tokens.append(token)
        parser.pos += 1

    parser.pos = save_pos

    # Ищем ASSIGN (=)
    for token in condition_tokens:
        if token[0] == 'ASSIGN':
            ctx = parser._get_context(token)

            if func_name == 'while':
                code = "WHILE_ASSIGN_IN_CONDITION"
            else:
                code = "IF_ASSIGN_IN_CONDITION"

            raise ArrayVatorError(
                code=code,
                context=ctx,
            )


def parse_if(parser):
    parser.expect('IF')

    # ============================================================
    # ПРОВЕРКА: '=' вместо '==' в условии
    # ============================================================
    _check_assign_in_condition(parser, "if")

    # ============================================================
    # УСЛОВИЕ
    # ============================================================
    condition = parser.parse_expression()

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