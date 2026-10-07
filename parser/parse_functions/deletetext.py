# parser/parse_functions/deletetext.py
"""
Парсинг deletetextleft и deletetextright (только программист).

СИНТАКСИС:
    deletetextleft("PR-001", 3)
    deletetextleft(s, 4)
    deletetextleft(s[:, "Код"], 4)
    deletetextleft(s[:, 3], 4)
    deletetextleft(s[2, :], 4)
    deletetextleft(s[2:5, :], 4)
    deletetextleft(s[2, 3], 4)
    deletetextleft(v, 4)
    deletetextleft(v[3:6], 4)
    deletetextleft(v[last 2], 4)
    deletetextleft(v[3], 4)
"""

from ast_nodes import (
    DeleteTextLeftNode,
    DeleteTextRightNode,
)


def _parse_deletetext(self, node_class):
    """Общий парсер для deletetextleft / deletetextright."""
    self.expect('LPAREN')

    # 1. Первый аргумент — данные (срез или переменная)
    save_pos = self.pos
    try:
        data = self.parse_primary()
    except Exception:
        self.pos = save_pos
        data = self.parse_expression()

    self.expect('COMMA')

    # 2. Количество символов
    count = self.parse_expression()

    self.expect('RPAREN')

    return node_class(data, count)


def parse_deletetextleft(self):
    """Парсинг DELETETEXTLEFT"""
    return _parse_deletetext(self, DeleteTextLeftNode)


def parse_deletetextright(self):
    """Парсинг DELETETEXTRIGHT"""
    return _parse_deletetext(self, DeleteTextRightNode)