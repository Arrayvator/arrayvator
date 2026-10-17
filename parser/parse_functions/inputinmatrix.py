# parser/parse_functions/inputinmatrix.py
"""
Парсинг InputInMatrix.

СИНТАКСИС:
    InputInMatrix(m)
    InputInMatrix(m, "Заголовок")
    InputInMatrix(m, "Заголовок", 10)
"""

from ast_nodes.functions.inputinmatrix import InputInMatrixNode


def parse_inputinmatrix(self):
    self.expect('LPAREN')

    # 1. Матрица (обязательно)
    data = self.parse_expression()

    # 2. Заголовок (опционально)
    title = None
    if self.check('COMMA'):
        self.expect('COMMA')
        title = self.parse_expression()

        # 3. Количество строк контекста (опционально)
        if self.check('COMMA'):
            self.expect('COMMA')
            preview = self.parse_expression()
        else:
            preview = None
    else:
        preview = None

    self.expect('RPAREN')

    return InputInMatrixNode(data, title, preview)