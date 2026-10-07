# ============================================================
# ФАЙЛ: ast_nodes/functions/datetime.py
# ФУНКЦИИ ДЛЯ РАБОТЫ С ДАТАМИ И ВРЕМЕНЕМ
# ============================================================

from ..base_nodes import Node
import datetime
import re


# ============================================================
# БАЗОВЫЕ ФУНКЦИИ
# ============================================================

class NowNode(Node):
    """Текущая дата и время"""
    def __init__(self):
        pass
    
    def evaluate(self, env):
        now = datetime.datetime.now()
        return now.strftime("%Y-%m-%d %H:%M:%S")
    
    def execute(self, env):
        return self.evaluate(env)
    
    def __repr__(self):
        return "Now()"


class TodayNode(Node):
    """Текущая дата"""
    def __init__(self):
        pass
    
    def evaluate(self, env):
        now = datetime.datetime.now()
        return now.strftime("%Y-%m-%d")
    
    def execute(self, env):
        return self.evaluate(env)
    
    def __repr__(self):
        return "Today()"


class TimeNode(Node):
    """Текущее время"""
    def __init__(self):
        pass
    
    def evaluate(self, env):
        now = datetime.datetime.now()
        return now.strftime("%H:%M:%S")
    
    def execute(self, env):
        return self.evaluate(env)
    
    def __repr__(self):
        return "Time()"


# ============================================================
# ПАРСИНГ ДАТЫ
# ============================================================

class ParseDateNode(Node):
    """Преобразование строки в дату по формату"""
    def __init__(self, date_str, format_str=None):
        self.date_str = date_str
        self.format_str = format_str
    
    def _convert_format(self, format_str):
        fmt = format_str
        fmt = fmt.replace("DD", "%d")
        fmt = fmt.replace("MM", "%m")
        fmt = fmt.replace("YYYY", "%Y")
        fmt = fmt.replace("HH", "%H")
        fmt = fmt.replace("MI", "%M")
        fmt = fmt.replace("SS", "%S")
        return fmt
    
    def evaluate(self, env):
        date_str = self.date_str.evaluate(env)
        
        if self.format_str:
            format_str = self.format_str.evaluate(env)
            fmt = self._convert_format(format_str)
            try:
                dt = datetime.datetime.strptime(date_str, fmt)
                return dt.strftime("%Y-%m-%d %H:%M:%S")
            except:
                return date_str
        else:
            if re.match(r'^\d{4}-\d{2}-\d{2}$', date_str):
                return date_str
            if re.match(r'^\d{2}\.\d{2}\.\d{4}$', date_str):
                parts = date_str.split('.')
                return f"{parts[2]}-{parts[1]}-{parts[0]}"
            return date_str
    
    def execute(self, env):
        return self.evaluate(env)
    
    def __repr__(self):
        return f"ParseDate({self.date_str}, {self.format_str})"


# ============================================================
# ИЗВЛЕЧЕНИЕ КОМПОНЕНТОВ
# ============================================================

class YearNode(Node):
    def __init__(self, date_val):
        self.date_val = date_val
    
    def evaluate(self, env):
        date_str = self.date_val.evaluate(env)
        match = re.search(r'(\d{4})', date_str)
        if match:
            return int(match.group(1))
        return 0
    
    def execute(self, env):
        return self.evaluate(env)
    
    def __repr__(self):
        return f"Year({self.date_val})"


class MonthNode(Node):
    def __init__(self, date_val):
        self.date_val = date_val
    
    def evaluate(self, env):
        date_str = self.date_val.evaluate(env)
        match = re.search(r'-(\d{2})-', date_str)
        if match:
            return int(match.group(1))
        match = re.search(r'\.(\d{2})\.', date_str)
        if match:
            return int(match.group(1))
        return 0
    
    def execute(self, env):
        return self.evaluate(env)
    
    def __repr__(self):
        return f"Month({self.date_val})"


class DayNode(Node):
    def __init__(self, date_val):
        self.date_val = date_val
    
    def evaluate(self, env):
        date_str = self.date_val.evaluate(env)
        match = re.search(r'-(\d{2})$', date_str)
        if match:
            return int(match.group(1))
        match = re.search(r'^(\d{2})\.', date_str)
        if match:
            return int(match.group(1))
        return 0
    
    def execute(self, env):
        return self.evaluate(env)
    
    def __repr__(self):
        return f"Day({self.date_val})"


class HourNode(Node):
    def __init__(self, datetime_val):
        self.datetime_val = datetime_val
    
    def evaluate(self, env):
        date_str = self.datetime_val.evaluate(env)
        match = re.search(r'(\d{2}):', date_str)
        if match:
            return int(match.group(1))
        return 0
    
    def execute(self, env):
        return self.evaluate(env)
    
    def __repr__(self):
        return f"Hour({self.datetime_val})"


class MinuteNode(Node):
    def __init__(self, datetime_val):
        self.datetime_val = datetime_val
    
    def evaluate(self, env):
        date_str = self.datetime_val.evaluate(env)
        match = re.search(r':(\d{2}):', date_str)
        if match:
            return int(match.group(1))
        return 0
    
    def execute(self, env):
        return self.evaluate(env)
    
    def __repr__(self):
        return f"Minute({self.datetime_val})"


class SecondNode(Node):
    def __init__(self, datetime_val):
        self.datetime_val = datetime_val
    
    def evaluate(self, env):
        date_str = self.datetime_val.evaluate(env)
        match = re.search(r':(\d{2})$', date_str)
        if match:
            return int(match.group(1))
        return 0
    
    def execute(self, env):
        return self.evaluate(env)
    
    def __repr__(self):
        return f"Second({self.datetime_val})"


class WeekdayNode(Node):
    def __init__(self, date_val):
        self.date_val = date_val
    
    def evaluate(self, env):
        date_str = self.date_val.evaluate(env)
        try:
            if re.match(r'^\d{4}-\d{2}-\d{2}$', date_str):
                dt = datetime.datetime.strptime(date_str, "%Y-%m-%d")
                return dt.weekday() + 1
        except:
            pass
        return 0
    
    def execute(self, env):
        return self.evaluate(env)
    
    def __repr__(self):
        return f"Weekday({self.date_val})"


class WeekdayNameNode(Node):
    def __init__(self, date_val):
        self.date_val = date_val
    
    def evaluate(self, env):
        date_str = self.date_val.evaluate(env)
        days_ru = ["Понедельник", "Вторник", "Среда", "Четверг", "Пятница", "Суббота", "Воскресенье"]
        try:
            if re.match(r'^\d{4}-\d{2}-\d{2}$', date_str):
                dt = datetime.datetime.strptime(date_str, "%Y-%m-%d")
                return days_ru[dt.weekday()]
        except:
            pass
        return ""
    
    def execute(self, env):
        return self.evaluate(env)
    
    def __repr__(self):
        return f"WeekdayName({self.date_val})"


class MonthNameNode(Node):
    def __init__(self, date_val):
        self.date_val = date_val
    
    def evaluate(self, env):
        date_str = self.date_val.evaluate(env)
        months_ru = ["Январь", "Февраль", "Март", "Апрель", "Май", "Июнь", 
                     "Июль", "Август", "Сентябрь", "Октябрь", "Ноябрь", "Декабрь"]
        try:
            if re.match(r'^\d{4}-\d{2}-\d{2}$', date_str):
                dt = datetime.datetime.strptime(date_str, "%Y-%m-%d")
                return months_ru[dt.month - 1]
        except:
            pass
        return ""
    
    def execute(self, env):
        return self.evaluate(env)
    
    def __repr__(self):
        return f"MonthName({self.date_val})"


# ============================================================
# ОПЕРАЦИИ С ДАТАМИ
# ============================================================

class AddDaysNode(Node):
    def __init__(self, date_val, days):
        self.date_val = date_val
        self.days = days
    
    def evaluate(self, env):
        date_str = self.date_val.evaluate(env)
        days = self.days.evaluate(env)
        
        try:
            if re.match(r'^\d{4}-\d{2}-\d{2}$', date_str):
                dt = datetime.datetime.strptime(date_str, "%Y-%m-%d")
                new_dt = dt + datetime.timedelta(days=int(days))
                return new_dt.strftime("%Y-%m-%d")
        except:
            pass
        return date_str
    
    def execute(self, env):
        return self.evaluate(env)
    
    def __repr__(self):
        return f"AddDays({self.date_val}, {self.days})"


class AddMonthsNode(Node):
    def __init__(self, date_val, months):
        self.date_val = date_val
        self.months = months
    
    def evaluate(self, env):
        date_str = self.date_val.evaluate(env)
        months = self.months.evaluate(env)
        
        try:
            if re.match(r'^\d{4}-\d{2}-\d{2}$', date_str):
                dt = datetime.datetime.strptime(date_str, "%Y-%m-%d")
                new_year = dt.year + (dt.month + int(months) - 1) // 12
                new_month = (dt.month + int(months) - 1) % 12 + 1
                new_day = min(dt.day, [31, 29 if new_year % 4 == 0 else 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31][new_month - 1])
                new_dt = datetime.datetime(new_year, new_month, new_day)
                return new_dt.strftime("%Y-%m-%d")
        except:
            pass
        return date_str
    
    def execute(self, env):
        return self.evaluate(env)
    
    def __repr__(self):
        return f"AddMonths({self.date_val}, {self.months})"


class AddYearsNode(Node):
    def __init__(self, date_val, years):
        self.date_val = date_val
        self.years = years
    
    def evaluate(self, env):
        date_str = self.date_val.evaluate(env)
        years = self.years.evaluate(env)
        
        try:
            if re.match(r'^\d{4}-\d{2}-\d{2}$', date_str):
                dt = datetime.datetime.strptime(date_str, "%Y-%m-%d")
                new_dt = dt.replace(year=dt.year + int(years))
                return new_dt.strftime("%Y-%m-%d")
        except:
            pass
        return date_str
    
    def execute(self, env):
        return self.evaluate(env)
    
    def __repr__(self):
        return f"AddYears({self.date_val}, {self.years})"


class DateDiffNode(Node):
    def __init__(self, date1, date2):
        self.date1 = date1
        self.date2 = date2
    
    def evaluate(self, env):
        date1_str = self.date1.evaluate(env)
        date2_str = self.date2.evaluate(env)
        
        try:
            if re.match(r'^\d{4}-\d{2}-\d{2}$', date1_str) and re.match(r'^\d{4}-\d{2}-\d{2}$', date2_str):
                dt1 = datetime.datetime.strptime(date1_str, "%Y-%m-%d")
                dt2 = datetime.datetime.strptime(date2_str, "%Y-%m-%d")
                return abs((dt2 - dt1).days)
        except:
            pass
        return 0
    
    def execute(self, env):
        return self.evaluate(env)
    
    def __repr__(self):
        return f"DateDiff({self.date1}, {self.date2})"


class DateDiffMonthsNode(Node):
    def __init__(self, date1, date2):
        self.date1 = date1
        self.date2 = date2
    
    def evaluate(self, env):
        date1_str = self.date1.evaluate(env)
        date2_str = self.date2.evaluate(env)
        
        try:
            if re.match(r'^\d{4}-\d{2}-\d{2}$', date1_str) and re.match(r'^\d{4}-\d{2}-\d{2}$', date2_str):
                dt1 = datetime.datetime.strptime(date1_str, "%Y-%m-%d")
                dt2 = datetime.datetime.strptime(date2_str, "%Y-%m-%d")
                months = abs((dt2.year - dt1.year) * 12 + (dt2.month - dt1.month))
                return months
        except:
            pass
        return 0
    
    def execute(self, env):
        return self.evaluate(env)
    
    def __repr__(self):
        return f"DateDiffMonths({self.date1}, {self.date2})"


# ============================================================
# НОВАЯ ФУНКЦИЯ: DateDiffEx
# ============================================================

class DateDiffExNode(Node):
    """
    Универсальная функция для расчёта разницы между датами
    
    Синтаксис:
        DateDiffEx(дата1, дата2, формат, результат)
    
    Параметры:
        дата1     - первая дата (строка)
        дата2     - вторая дата (строка)
        формат    - "DD.MM.YYYY", "MM/DD/YYYY", "YYYY-MM-DD" и т.д.
        результат - "D" (дни), "M" (месяцы), "Y" (годы)
    """
    
    def __init__(self, date1, date2, format_str, result_type):
        self.date1 = date1
        self.date2 = date2
        self.format_str = format_str
        self.result_type = result_type
    
    def _parse_date(self, date_str, format_str):
        """Парсит дату по указанному формату"""
        fmt = format_str
        fmt = fmt.replace("DD", "%d")
        fmt = fmt.replace("MM", "%m")
        fmt = fmt.replace("YYYY", "%Y")
        fmt = fmt.replace("HH", "%H")
        fmt = fmt.replace("MI", "%M")
        fmt = fmt.replace("SS", "%S")
        
        fmt = fmt.strip()
        date_str = date_str.strip()
        
        try:
            dt = datetime.datetime.strptime(date_str, fmt)
            return dt
        except:
            return self._parse_auto(date_str)
    
    def _parse_auto(self, date_str):
        """Автоматическое определение формата"""
        if re.match(r'^\d{4}-\d{2}-\d{2}$', date_str):
            return datetime.datetime.strptime(date_str, "%Y-%m-%d")
        if re.match(r'^\d{2}\.\d{2}\.\d{4}$', date_str):
            return datetime.datetime.strptime(date_str, "%d.%m.%Y")
        if re.match(r'^\d{2}-\d{2}-\d{4}$', date_str):
            return datetime.datetime.strptime(date_str, "%d-%m-%Y")
        if re.match(r'^\d{2}/\d{2}/\d{4}$', date_str):
            return datetime.datetime.strptime(date_str, "%d/%m/%Y")
        if re.match(r'^\d{2}/\d{2}/\d{4}$', date_str):
            return datetime.datetime.strptime(date_str, "%m/%d/%Y")
        if re.match(r'^\d{4}\.\d{2}\.\d{2}$', date_str):
            return datetime.datetime.strptime(date_str, "%Y.%m.%d")
        if re.match(r'^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}$', date_str):
            return datetime.datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
        return None
    
    def evaluate(self, env):
        date1_str = self.date1.evaluate(env)
        date2_str = self.date2.evaluate(env)
        format_str = self.format_str.evaluate(env)
        result_type = self.result_type.evaluate(env)
        
        dt1 = self._parse_date(date1_str, format_str)
        dt2 = self._parse_date(date2_str, format_str)
        
        if dt1 is None or dt2 is None:
            return 0
        
        if result_type == "D":
            return abs((dt2 - dt1).days)
        
        if result_type == "M":
            months = abs((dt2.year - dt1.year) * 12 + (dt2.month - dt1.month))
            return months
        
        if result_type == "Y":
            months = abs((dt2.year - dt1.year) * 12 + (dt2.month - dt1.month))
            return months / 12
        
        return 0
    
    def execute(self, env):
        return self.evaluate(env)
    
    def __repr__(self):
        return f"DateDiffEx({self.date1}, {self.date2}, {self.format_str}, {self.result_type})"