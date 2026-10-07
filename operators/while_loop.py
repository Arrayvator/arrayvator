# operators/while_loop.py
"""
Цикл WHILE.

СИНТАКСИС:
    while условие
    {
        команды
    }

    while условие команда
"""

from ast_nodes import Node
from errors import ArrayVatorError
from .break_stmt import BreakException


# ============================================================
# ХЕЛПЕР: рекурсивный поиск 'end' в дереве условия
# ============================================================
def _contains_bare_end(node):
    """
    Рекурсивно ищет чистое 'end' в дереве условия.

    Проверяет:
      • VariableNode / StringNode с 'end'
      • BinaryOp — left и right
      • UnaryOp — right

    Возвращает True, если где-то в дереве найден голый 'end'.
    """
    if node is None:
        return False

    # VariableNode('end')
    if hasattr(node, 'name'):
        name = getattr(node, 'name', '')
        if isinstance(name, str) and name.lower() == 'end':
            return True

    # StringNode('end')
    if hasattr(node, 'value'):
        value = getattr(node, 'value', '')
        if isinstance(value, str) and value.lower() == 'end':
            return True

    # BinaryOp: left и right
    if hasattr(node, 'left'):
        if _contains_bare_end(getattr(node, 'left', None)):
            return True
    if hasattr(node, 'right'):
        if _contains_bare_end(getattr(node, 'right', None)):
            return True

    return False


class WhileNode(Node):
    def __init__(self, condition, body):
        self.condition = condition
        self.body = body

    def execute(self, env):
        try:
            while self.condition.evaluate(env):
                for stmt in self.body:
                    stmt.execute(env)
        except BreakException:
            pass

    def __repr__(self):
        return f"While({self.condition}, {self.body})"


def parse_while(parser):
    parser.expect('WHILE')

    # ============================================================
    # ПРОВЕРКА: '=' вместо '==' в условии
    # ============================================================
    from .if_stmt import _check_assign_in_condition
    _check_assign_in_condition(parser, "while")

    condition = parser.parse_expression()

    # ============================================================
    # ПРОВЕРКА: 'end' в while запрещён
    # ============================================================
    if _contains_bare_end(condition):
        raise ArrayVatorError(
            code="WHILE_END_KEYWORD",
            context=parser._get_context(),
        )

    # ============================================================
    # ТЕЛО
    # ============================================================
    body = []
    if parser.check('LBRACE'):
        parser.expect('LBRACE')
        while not parser.check('RBRACE') and parser.peek():
            stmt = parser.parse_statement()
            if stmt:
                body.append(stmt)
        parser.expect('RBRACE')
    else:
        stmt = parser.parse_statement()
        if stmt:
            body.append(stmt)

    return WhileNode(condition, body)