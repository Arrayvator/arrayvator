# parser/functions.py
"""
Парсинг функций — тонкий диспетчер.
Все маршруты разбиты по модулям parser/dispatch/*.py.
"""

from .base import Parser
from .dispatch import DISPATCHERS


def parse_primary(self):
    token = self.peek()
    if not token:
        raise SyntaxError("Неожиданный конец выражения")

    token_type = token[0]
    value = token[1]

    # Спец-обработка ASSIGN (не диспетчеризуется)
    if token_type == 'ASSIGN':
        self.pos += 1
        raise SyntaxError(f"Неожиданный символ '='")

    for dispatcher in DISPATCHERS:
        result = dispatcher(self, token_type, token, value)
        if result is not None:
            return result

    # Не обработано ни одним диспетчером
    line_num = token[2] if len(token) >= 3 else self.current_line
    raise SyntaxError(f"Неожиданный токен: {token_type} (строка {line_num})")


Parser.parse_primary = parse_primary