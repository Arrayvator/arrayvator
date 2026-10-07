# parser/parse_functions/calendar.py
"""
Парсинг calendar / calendarpro.

СИНТАКСИС:
    calendar("dd.mm.yyyy", месяц, год [, "ru"|"eu"|"us"])
    calendarpro(год, месяц [, "ru"|"eu"|"us"])
"""

from ast_nodes.functions.calendar import CalendarNode, CalendarProNode
from ast_nodes import StringNode
from errors import ArrayVatorError


def parse_calendar(self):
    """
    calendar("dd.mm.yyyy", месяц, год [, локаль])

    месяц: 1-12 | all | datenow()
    год:   1981 | 2026 | datenow()
    локаль: "ru" | "eu" | "us" (опц.)
    """
    self.expect('LPAREN')

    # 1. Формат
    fmt = self.parse_expression()
    self.expect('COMMA')

    # 2. Месяц
    month = _parse_month(self, 'CALENDAR_BAD_MONTH', 'calendar')
    self.expect('COMMA')

    # 3. Год
    year = self.parse_expression()

    # 4. Локаль (опционально)
    locale = None
    if self.check('COMMA'):
        self.expect('COMMA')
        locale = self.parse_expression()

    self.expect('RPAREN')
    return CalendarNode(fmt, month, year, locale)


def parse_calendarpro(self):
    """
    calendarpro(год, месяц [, локаль])
    """
    self.expect('LPAREN')

    # 1. Год
    year = self.parse_expression()
    self.expect('COMMA')

    # 2. Месяц
    month = _parse_month(self, 'CALENDARPRO_BAD_MONTH', 'calendarpro')

    # 3. Локаль (опционально)
    locale = None
    if self.check('COMMA'):
        self.expect('COMMA')
        locale = self.parse_expression()

    self.expect('RPAREN')
    return CalendarProNode(year, month, locale)


def _parse_month(self, error_code, func_name):
    """
    Парсит месяц: число, all или datenow().
    """
    token = self.peek()
    if not token:
        raise ArrayVatorError(
            code=error_code,
            context=self._get_context(),
            message=(
                f"{func_name}: не указан месяц.\n"
                f"  Пример: {func_name}(..., 1, ...)\n"
                f"  Пример: {func_name}(..., all, ...)"
            ),
        )

    # all
    if token[0] == 'ALL':
        self.pos += 1
        return StringNode('all')

    # Число или datenow()
    return self.parse_expression()