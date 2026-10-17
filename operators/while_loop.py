# operators/while_loop.py
"""
Цикл WHILE.

СИНТАКСИС:
    while условие do
    {
        команды
    }

    while условие do команда

    while условие
    {
        команды
    }

    while условие команда

КЛЮЧЕВОЕ СЛОВО 'do' — ОПЦИОНАЛЬНО.
"""

from ast_nodes import Node
from errors import ArrayVatorError
from .break_stmt import BreakException


def _contains_bare_end(node):
    """Рекурсивно ищет чистое 'end' в дереве условия."""
    if node is None:
        return False

    if hasattr(node, 'name'):
        name = getattr(node, 'name', '')
        if isinstance(name, str) and name.lower() == 'end':
            return True

    if hasattr(node, 'value'):
        value = getattr(node, 'value', '')
        if isinstance(value, str) and value.lower() == 'end':
            return True

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
    # УСЛОВИЕ + проверка '=' в условии
    # ============================================================
    from .if_stmt import check_assign_in_range

    cond_start = parser.pos
    condition = parser.parse_expression()
    cond_end = parser.pos

    check_assign_in_range(parser, cond_start, cond_end, "while")

    # ============================================================
    # ПРОВЕРКА: 'end' в while запрещён
    # ============================================================
    if _contains_bare_end(condition):
        raise ArrayVatorError(
            code="WHILE_END_KEYWORD",
            context=parser._get_context(),
        )

    # ============================================================
    # 'do' — ОПЦИОНАЛЬНО
    # ============================================================
    if parser.check('DO'):
        parser.expect('DO')

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