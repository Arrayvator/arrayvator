# ast_nodes/functions/datediff.py
"""
Функция DateDiff — разница между датами.

ЕДИНИЦЫ ИЗМЕРЕНИЯ:
    seconds  — секунды
    minutes  — минуты
    hours    — часы
    days     — дни
    weeks    — недели
    months   — месяцы
    years    — годы
    all      — всё сразу строкой: "5 лет 10 месяцев 2 дня"

ПРАВИЛА:
    - Считаются ПОЛНЫЕ прошедшие периоды (elapsed complete periods).
    - Если хотя бы одного дня не хватает — период НЕ считается полным.
    - Если d2 < d1 — результат отрицательный.
    - Если хотя бы одно значение не распознано как дата — None.
    - Если единица неизвестна — None.
    - Никаких падений: любые ошибки → None.
    - Работает со скалярами, векторами, матрицами.

ПРИМЕРЫ (все считают полные периоды):
    01.07.2019 → 30.06.2024, "years"  → 4   (не 5 — не хватает 1 дня)
    10.06.2020 → 31.12.2023, "years"  → 3   (не 4 — не хватает ~5.5 мес)
    05.12.2015 → 16.10.2026, "years"  → 10  (не 11)
    05.12.2015 → 16.10.2026, "all"    → "10 лет 10 месяцев 11 дней"
"""

import datetime

from ..base import Node


# ============================================================
# ХЕЛПЕРЫ: ПРИВЕДЕНИЕ К СПИСКУ
# ============================================================

def _to_list(val):
    """
    Приводит значение к списку Python.
    - MatrExMatrix (1D) → list
    - MatrExMatrix (2D) → list первой колонки
    - list → list
    - скаляр → [скаляр]
    """
    if hasattr(val, 'data'):
        if val.is_2d:
            return [row[0] if row else None for row in val.data]
        return list(val.data)
    if isinstance(val, list):
        if val and isinstance(val[0], list):
            return [row[0] if row else None for row in val]
        return list(val)
    return [val]


# ============================================================
# ХЕЛПЕРЫ: ПАРСИНГ ДАТЫ
# ============================================================

def _parse_date(value, fmt):
    """
    Парсит дату из строки. Возвращает datetime или None.
    Никогда не падает.
    """
    if value is None:
        return None
    if isinstance(value, (int, float)):
        # Числа (например 0) — это НЕ даты.
        return None
    if not isinstance(value, str):
        return None
    if value.strip() == "":
        return None
    if not isinstance(fmt, str):
        return None

    try:
        # Определяем разделитель даты
        date_sep = None
        for s in ['.', '/', '-']:
            if s in fmt:
                date_sep = s
                break

        if date_sep is None:
            return None

        # Отделяем дату от времени
        date_parts = value.strip().split(' ')
        date_part = date_parts[0]
        time_part = date_parts[1] if len(date_parts) > 1 else None

        parts = date_part.split(date_sep)
        fmt_clean = fmt.split(' ')[0]
        fmt_parts = fmt_clean.split(date_sep)

        if len(parts) != len(fmt_parts):
            return None

        year = month = day = None
        for i, fp in enumerate(fmt_parts):
            if i >= len(parts):
                break
            try:
                if fp in ('YYYY', 'YY'):
                    y = int(parts[i])
                    if fp == 'YY' and y < 100:
                        y += 2000
                    year = y
                elif fp == 'MM':
                    month = int(parts[i])
                elif fp == 'DD':
                    day = int(parts[i])
            except (ValueError, TypeError):
                return None

        if year is None or month is None or day is None:
            return None

        # Время (опционально)
        hour = minute = second = 0
        if time_part:
            try:
                time_parts = time_part.split(':')
                if len(time_parts) >= 1:
                    hour = int(time_parts[0])
                if len(time_parts) >= 2:
                    minute = int(time_parts[1])
                if len(time_parts) >= 3:
                    second = int(time_parts[2])
            except (ValueError, TypeError):
                hour = minute = second = 0

        try:
            return datetime.datetime(year, month, day, hour, minute, second)
        except (ValueError, TypeError):
            return None

    except Exception:
        return None


# ============================================================
# ХЕЛПЕРЫ: КАЛЕНДАРЬ
# ============================================================

def _days_in_month(year, month):
    """Количество дней в месяце с учётом високосного года."""
    if month == 2:
        if year % 4 == 0 and (year % 100 != 0 or year % 400 == 0):
            return 29
        return 28
    return [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31][month - 1]


def _add_years(dt, n):
    """Прибавляет n лет, корректно обрабатывая 29 февраля."""
    y = dt.year + n
    d = min(dt.day, _days_in_month(y, dt.month))
    return dt.replace(year=y, day=d)


def _add_months(dt, n):
    """Прибавляет n месяцев."""
    m = dt.month - 1 + n
    y = dt.year + m // 12
    m = m % 12 + 1
    d = min(dt.day, _days_in_month(y, m))
    return dt.replace(year=y, month=m, day=d)


# ============================================================
# ХЕЛПЕРЫ: ПОЛНЫЕ ПЕРИОДЫ
# ============================================================

def _full_days(d1, d2):
    """Полные прошедшие дни."""
    return (d2 - d1).days


def _full_hours(d1, d2):
    """Полные прошедшие часы."""
    return int((d2 - d1).total_seconds() // 3600)


def _full_minutes(d1, d2):
    """Полные прошедшие минуты."""
    return int((d2 - d1).total_seconds() // 60)


def _full_months(d1, d2):
    """
    Полные прошедшие месяцы.
    Если день d2 < день d1 — последний месяц не считается полным.
    """
    months = (d2.year - d1.year) * 12 + (d2.month - d1.month)
    if d2.day < d1.day:
        months -= 1
    return months


def _full_years(d1, d2):
    """
    Полные прошедшие годы.
    Если (месяц, день) в d2 ещё не наступил в этом году —
    последний год не полный.
    """
    years = d2.year - d1.year
    if (d2.month, d2.day) < (d1.month, d1.day):
        years -= 1
    return years


# ============================================================
# ХЕЛПЕРЫ: СКЛОНЕНИЕ
# ============================================================

def _plural(n, one, few, many):
    """Русская форма множественного числа: 1 год, 2 года, 5 лет."""
    n = abs(n) % 100
    if 11 <= n <= 19:
        return f"{n} {many}"
    n1 = n % 10
    if n1 == 1:
        return f"{n} {one}"
    if 2 <= n1 <= 4:
        return f"{n} {few}"
    return f"{n} {many}"


# ============================================================
# ALL — полная разбивка
# ============================================================

def _all_periods(d1, d2, sign=1):
    """
    Возвращает строку вида:
        "5 лет 10 месяцев 2 дня 3 часа 15 минут"
    Только ненулевые компоненты.
    """
    if d2 < d1:
        d1, d2 = d2, d1
        sign = -1

    years = _full_years(d1, d2)
    cursor = _add_years(d1, years)

    months = _full_months(cursor, d2)
    cursor = _add_months(cursor, months)

    days = _full_days(cursor, d2)
    cursor = cursor + datetime.timedelta(days=days)

    hours = _full_hours(cursor, d2)
    cursor = cursor + datetime.timedelta(hours=hours)

    minutes = _full_minutes(cursor, d2)

    parts = []
    if years:
        parts.append(_plural(years, "год", "года", "лет"))
    if months:
        parts.append(_plural(months, "месяц", "месяца", "месяцев"))
    if days:
        parts.append(_plural(days, "день", "дня", "дней"))
    if hours:
        parts.append(_plural(hours, "час", "часа", "часов"))
    if minutes:
        parts.append(_plural(minutes, "минута", "минуты", "минут"))

    if not parts:
        return "0 минут"

    result = " ".join(parts)
    if sign < 0:
        result = "-" + result
    return result


# ============================================================
# ОСНОВНОЙ РАСЧЁТ
# ============================================================

def _calc_diff(d1, d2, unit):
    """
    Считает разницу между датами.
    Возвращает ПОЛНЫЕ прошедшие периоды (elapsed complete periods).
    Если что-то не так — возвращает None.
    """
    if d1 is None or d2 is None:
        return None
    if not isinstance(d1, datetime.datetime):
        return None
    if not isinstance(d2, datetime.datetime):
        return None
    if not isinstance(unit, str):
        return None

    unit = unit.strip().lower()

    # Знак: если d2 < d1 — периоды отрицательные
    sign = 1
    if d2 < d1:
        d1, d2 = d2, d1
        sign = -1

    try:
        if unit == "seconds":
            return sign * int((d2 - d1).total_seconds())

        if unit == "minutes":
            return sign * _full_minutes(d1, d2)

        if unit == "hours":
            return sign * _full_hours(d1, d2)

        if unit == "days":
            return sign * _full_days(d1, d2)

        if unit == "weeks":
            return sign * (_full_days(d1, d2) // 7)

        if unit == "months":
            return sign * _full_months(d1, d2)

        if unit == "years":
            return sign * _full_years(d1, d2)

        if unit == "all":
            return _all_periods(d1, d2, sign)

        return None

    except (TypeError, ValueError):
        return None


# ============================================================
# УЗЕЛ
# ============================================================

class DateDiffNode(Node):
    def __init__(self, date1, date2, format_str, unit):
        self.date1 = date1
        self.date2 = date2
        self.format_str = format_str
        self.unit = unit

    def evaluate(self, env):
        from runtime.matrix import MatrExMatrix

        # ============================================================
        # 1. Единица измерения
        # ============================================================
        try:
            unit_val = (self.unit.evaluate(env)
                        if hasattr(self.unit, 'evaluate')
                        else self.unit)
        except Exception:
            unit_val = None

        if not isinstance(unit_val, str):
            return None

        # ============================================================
        # 2. Формат
        # ============================================================
        try:
            format_val = (self.format_str.evaluate(env)
                          if hasattr(self.format_str, 'evaluate')
                          else self.format_str)
        except Exception:
            format_val = None

        if not isinstance(format_val, str):
            return None

        # ============================================================
        # 3. Значения
        # ============================================================
        try:
            date1_val = (self.date1.evaluate(env)
                         if hasattr(self.date1, 'evaluate')
                         else self.date1)
        except Exception:
            date1_val = None

        try:
            date2_val = (self.date2.evaluate(env)
                         if hasattr(self.date2, 'evaluate')
                         else self.date2)
        except Exception:
            date2_val = None

        # ============================================================
        # 4. Оба скаляры
        # ============================================================
        if (not isinstance(date1_val, list)
                and not hasattr(date1_val, 'data')
                and not isinstance(date2_val, list)
                and not hasattr(date2_val, 'data')):
            d1 = _parse_date(date1_val, format_val)
            d2 = _parse_date(date2_val, format_val)
            return _calc_diff(d1, d2, unit_val)

        # ============================================================
        # 5. Приводим оба к списку
        # ============================================================
        list1 = _to_list(date1_val)
        list2 = _to_list(date2_val)

        # ============================================================
        # 6. Поэлементно
        # ============================================================
        n = max(len(list1), len(list2))
        results = []
        for i in range(n):
            v1 = list1[i] if i < len(list1) else None
            v2 = list2[i] if i < len(list2) else None

            d1 = _parse_date(v1, format_val)
            d2 = _parse_date(v2, format_val)
            results.append(_calc_diff(d1, d2, unit_val))

        # ============================================================
        # 7. Один элемент → скаляр
        # ============================================================
        if len(results) == 1:
            return results[0]

        # ============================================================
        # 8. Вектор
        # ============================================================
        return MatrExMatrix(results, False)

    def __repr__(self):
        return (f"DateDiff({self.date1}, {self.date2}, "
                f"{self.format_str}, {self.unit})")