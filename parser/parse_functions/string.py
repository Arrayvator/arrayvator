# parser/parse_functions/string.py
"""
Парсинг строковых функций: SPLIT, JOINVECTOR, REPLACETEXT

СИНТАКСИС REPLACETEXT:

    replacetext(s, "что", "на_что")
    replacetext(s, "что", "на_что", ignore)
    replacetext(s[:, "Отдел"], "что", "на_что")
    replacetext(s[:, 3], "что", "на_что")
    replacetext(s[2:5, :], "что", "на_что")
    replacetext(v, "что", "на_что")
    replacetext("Hello", "l", "L")

СИНТАКСИС JOINVECTOR:

    joinvector(вектор [, разделитель])
"""

from ast_nodes import SplitNode, JoinVectorNode, ReplaceTextNode, StringNode


def parse_string(self, token_type):
    """Парсинг строковых функций"""
    self.expect('LPAREN')

    if token_type == 'SPLIT':
        text = self.parse_expression()
        delimiter = None
        skip_empty = False

        if self.check('COMMA'):
            self.expect('COMMA')
            delimiter = self.parse_expression()
            if self.check('COMMA'):
                self.expect('COMMA')
                if self.check('SKIP'):
                    self.expect('SKIP')
                    skip_empty = True
                else:
                    self.parse_expression()
                    skip_empty = True

        self.expect('RPAREN')
        return SplitNode(text, delimiter, skip_empty)

    elif token_type == 'JOINVECTOR':
        data = self.parse_expression()
        delimiter = None
        if self.check('COMMA'):
            self.expect('COMMA')
            delimiter = self.parse_expression()
        self.expect('RPAREN')
        return JoinVectorNode(data, delimiter)

    elif token_type == 'REPLACETEXT':
        save_pos = self.pos
        try:
            data = self.parse_primary()
        except Exception:
            self.pos = save_pos
            data = self.parse_expression()

        self.expect('COMMA')

        old = self.parse_expression()
        self.expect('COMMA')

        new = self.parse_expression()

        ignore = None
        if self.check('COMMA'):
            self.expect('COMMA')
            if self.check('IGNORE'):
                self.expect('IGNORE')
                ignore = StringNode('ignore')
            else:
                ignore = self.parse_expression()

        self.expect('RPAREN')
        return ReplaceTextNode(data, old, new, ignore=ignore)