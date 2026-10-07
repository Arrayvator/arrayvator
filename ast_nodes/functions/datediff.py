# ast_nodes/functions/datediff.py
"""
Функция DateDiff - разница между датами
"""

from ..base import Node
import datetime


class DateDiffNode(Node):
    def __init__(self, date1, date2, format_str, unit):
        self.date1 = date1
        self.date2 = date2
        self.format_str = format_str
        self.unit = unit

    def _parse_date(self, date_str, format_str):
        if date_str is None:
            return None
        if not isinstance(date_str, str):
            return date_str

        date_part = date_str
        time_part = None

        if ' ' in date_str:
            parts = date_str.split(' ')
            date_part = parts[0]
            if len(parts) > 1:
                time_part = parts[1]

        date_sep = None
        for s in ['.', '/', '-']:
            if s in date_part:
                date_sep = s
                break

        if date_sep is None:
            return None

        date_parts = date_part.split(date_sep)
        format_clean = format_str.split(' ')[0]
        format_parts = format_clean.split(date_sep)

        year = None
        month = None
        day = None

        for i, part in enumerate(format_parts):
            if i >= len(date_parts):
                break
            if part == 'YYYY' or part == 'YY':
                year = int(date_parts[i])
                if part == 'YY' and year < 100:
                    year += 2000
            elif part == 'MM':
                month = int(date_parts[i])
            elif part == 'DD':
                day = int(date_parts[i])

        if year is None or month is None or day is None:
            return None

        hour = 0
        minute = 0
        second = 0

        if time_part:
            time_parts = time_part.split(':')
            if len(time_parts) >= 1:
                hour = int(time_parts[0])
            if len(time_parts) >= 2:
                minute = int(time_parts[1])
            if len(time_parts) >= 3:
                second = int(time_parts[2])

        return datetime.datetime(year, month, day, hour, minute, second)

    def _calc_diff(self, d1, d2, unit):
        if d1 is None or d2 is None:
            return None

        diff = d2 - d1

        if unit == "seconds":
            return diff.total_seconds()
        elif unit == "minutes":
            return diff.total_seconds() / 60
        elif unit == "hours":
            return diff.total_seconds() / 3600
        elif unit == "days":
            return diff.days
        elif unit == "weeks":
            return diff.days / 7
        elif unit == "months":
            return (d2.year - d1.year) * 12 + (d2.month - d1.month)
        elif unit == "years":
            return d2.year - d1.year
        else:
            raise ValueError(f"Неизвестная единица измерения: {unit}")

    def evaluate(self, env):
        from runtime.matrix import MatrExMatrix

        format_val = self.format_str.evaluate(env)
        unit_val = self.unit.evaluate(env)

        date1_val = self.date1.evaluate(env)
        date2_val = self.date2.evaluate(env)

        # Строки
        if isinstance(date1_val, str) and isinstance(date2_val, str):
            d1 = self._parse_date(date1_val, format_val)
            d2 = self._parse_date(date2_val, format_val)
            if d1 is not None and d2 is not None:
                return self._calc_diff(d1, d2, unit_val)
            return None

        # Векторы
        if hasattr(date1_val, 'data') and hasattr(date2_val, 'data'):
            results = []
            for i in range(len(date1_val.data)):
                if i < len(date2_val.data):
                    d1 = self._parse_date(date1_val.data[i], format_val)
                    d2 = self._parse_date(date2_val.data[i], format_val)
                    diff = self._calc_diff(d1, d2, unit_val)
                    results.append(diff)
                else:
                    results.append(None)
            return MatrExMatrix(results, False)

        return None

    def __repr__(self):
        return f"DateDiff({self.date1}, {self.date2}, {self.format_str}, {self.unit})"