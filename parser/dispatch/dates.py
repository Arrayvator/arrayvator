# parser/dispatch/dates.py
"""
Даты и время: DATE, DATEDIFF, DATENOW, TIMENOW, TIMESTAMP,
      YEAR, MONTH, DAY, QUARTER,
      WEEKDAY, WEEKDAYNAME, MONTHNAME,
      ADDDAYS, ADDMONTHS, ADDYEARS, DATETRUNC,
      CALENDAR, CALENDARPRO,
      HOUR, MINUTE, SECOND, AMPM, IS_PM,
      ADDHOURS, ADDMINUTES, ADDSECONDS,
      TIMETRUNC, TIME.
"""

from ._helpers import call_parse


def dispatch(self, token_type, token, value):
    # ============================================================
    # КАЛЕНДАРЬ
    # ============================================================
    if token_type == 'CALENDAR':
        self.pos += 1
        return call_parse(self, 'parse_calendar')

    if token_type == 'CALENDARPRO':
        self.pos += 1
        return call_parse(self, 'parse_calendarpro')

    # ============================================================
    # СТАРЫЕ ДАТЫ
    # ============================================================
    if token_type == 'DATE':
        self.pos += 1
        return call_parse(self, 'parse_date')

    if token_type == 'DATEDIFF':
        self.pos += 1
        return call_parse(self, 'parse_datediff')

    if token_type == 'DATENOW':
        self.pos += 1
        return call_parse(self, 'parse_datenow')

    if token_type == 'TIMENOW':
        self.pos += 1
        return call_parse(self, 'parse_timenow')

    # ============================================================
    # ИЗВЛЕЧЕНИЕ КОМПОНЕНТОВ ДАТЫ
    # ============================================================
    if token_type == 'YEAR':
        self.pos += 1
        return call_parse(self, 'parse_year')

    if token_type == 'MONTH':
        self.pos += 1
        return call_parse(self, 'parse_month')

    if token_type == 'DAY':
        self.pos += 1
        return call_parse(self, 'parse_day')

    if token_type == 'QUARTER':
        self.pos += 1
        return call_parse(self, 'parse_quarter')

    if token_type == 'WEEKDAY':
        self.pos += 1
        return call_parse(self, 'parse_weekday')

    if token_type == 'WEEKDAYNAME':
        self.pos += 1
        return call_parse(self, 'parse_weekdayname')

    if token_type == 'MONTHNAME':
        self.pos += 1
        return call_parse(self, 'parse_monthname')

    # ============================================================
    # АРИФМЕТИКА ДАТ
    # ============================================================
    if token_type == 'ADDDAYS':
        self.pos += 1
        return call_parse(self, 'parse_adddays')

    if token_type == 'ADDMONTHS':
        self.pos += 1
        return call_parse(self, 'parse_addmonths')

    if token_type == 'ADDYEARS':
        self.pos += 1
        return call_parse(self, 'parse_addyears')

    # ============================================================
    # ОБРЕЗКА ДАТ
    # ============================================================
    if token_type == 'DATETRUNC':
        self.pos += 1
        return call_parse(self, 'parse_datetrunc')

    # ============================================================
    # ВРЕМЯ — извлечение компонентов
    # ============================================================
    if token_type == 'HOUR':
        self.pos += 1
        return call_parse(self, 'parse_hour')

    if token_type == 'MINUTE':
        self.pos += 1
        return call_parse(self, 'parse_minute')

    if token_type == 'SECOND':
        self.pos += 1
        return call_parse(self, 'parse_second')

    if token_type == 'AMPM':
        self.pos += 1
        return call_parse(self, 'parse_ampm')

    if token_type == 'IS_PM':
        self.pos += 1
        return call_parse(self, 'parse_is_pm')

    # ============================================================
    # ВРЕМЯ — арифметика
    # ============================================================
    if token_type == 'ADDHOURS':
        self.pos += 1
        return call_parse(self, 'parse_addhours')

    if token_type == 'ADDMINUTES':
        self.pos += 1
        return call_parse(self, 'parse_addminutes')

    if token_type == 'ADDSECONDS':
        self.pos += 1
        return call_parse(self, 'parse_addseconds')

    # ============================================================
    # ВРЕМЯ — обрезка и конвертация
    # ============================================================
    if token_type == 'TIMETRUNC':
        self.pos += 1
        return call_parse(self, 'parse_timetrunc')

    if token_type == 'TIME':
        self.pos += 1
        return call_parse(self, 'parse_time')

    if token_type == 'TIMESTAMP':
        self.pos += 1
        return call_parse(self, 'parse_timestamp')

    return None