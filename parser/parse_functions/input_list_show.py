# parser/parse_functions/input_list_show.py
"""
Парсинг InputListShow
"""

from ast_nodes import InputListShowNode


def parse_inputlistshow(self):
    """Парсинг INPUTLISTSHOW"""
    self.expect('LPAREN')

    title = None

    # Необязательный title:
    if self.check('IDENTIFIER'):
        token = self.peek()
        if token[1].lower() == 'title':
            save_pos = self.pos
            self.pos += 1

            if self.check('COLON'):
                self.expect('COLON')
                title = self.parse_expression()
                if self.check('COMMA'):
                    self.expect('COMMA')
                else:
                    self.expect('COMMA')
            else:
                self.pos = save_pos

    pairs = []

    while not self.check('RPAREN'):
        label = self.parse_expression()

        if not self.check('COMMA'):
            if self.check('RPAREN'):
                break
            self.expect('COMMA')

        self.expect('COMMA')

        if self.check('RPAREN'):
            break

        target = self.parse_expression()
        pairs.append((label, target))

        if self.check('COMMA'):
            self.expect('COMMA')
        else:
            break

    self.expect('RPAREN')
    return InputListShowNode(pairs, title)