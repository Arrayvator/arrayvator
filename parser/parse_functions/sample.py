# parser/parse_functions/sample.py
"""
Парсинг SAMPLE.

СИНТАКСИС:
    r = sample(m, 1000)
    r = sample(m, 100, 42)
"""

from ast_nodes import SampleNode


def parse_sample(self):
    """Парсинг SAMPLE"""
    self.expect('LPAREN')

    # 1. Данные
    data = self.parse_expression()

    self.expect('COMMA')

    # 2. Количество
    n = self.parse_expression()

    # 3. Seed (опционально)
    seed = None
    if self.check('COMMA'):
        self.expect('COMMA')
        seed = self.parse_expression()

    self.expect('RPAREN')
    return SampleNode(data, n, seed)