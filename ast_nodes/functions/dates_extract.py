# ast_nodes/functions/dates_extract.py
"""
Извлечение компонентов даты и времени, арифметика, обрезка, конвертация.

Поддерживается 12-часовой (американский) формат:
    HH  — часы 24-часовые (00-23)
    hh  — часы 12-часовые (01-12)
    MM  — минуты (после HH/hh) или месяц (до HH/hh)
    SS  — секунды
    AM / PM — маркер дня

АВТООПРЕДЕЛЕНИЕ ФОРМАТА (если формат не указан):
    Даты:     DD.MM.YYYY, YYYY-MM-DD, DD/MM/YYYY, MM/DD/YYYY
    Время:    HH:MM:SS, HH:MM, hh:MM:SS AM, hh:MM AM
    Дата+время: DD.MM.YYYY HH:MM:SS и т.д.

АРИФМЕТИКА (add*):
    Если формат не указан — результат возвращается в формате
    входной строки. То есть:
        adddays("20.06.2025", 10)   → "30.06.2025"
        addhours("14:30:15", 2)     → "16:30:15"
"""

import datetime
import re

from ..base import Node
from runtime.matrix import MatrExMatrix
from ..utils.index_utils import parse_range_spec, resolve_column_index


# ============================================================
# КОНСТАНТЫ
# ============================================================
DEFAULT_FORMAT = "DD.MM.YYYY"
DEFAULT_TIME_FORMAT = "HH:MM:SS"

MONTHS_RU_NOM = [
    "Январь", "Февраль", "Март", "Апрель", "Май", "Июнь",
    "Июль", "Август", "Сентябрь", "Октябрь", "Ноябрь", "Декабрь",
]

WEEKDAYS_RU = [
    "Понедельник", "Вторник", "Среда", "Четверг",
    "Пятница", "Суббота", "Воскресенье",
]

DAYS_IN_MONTH = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]


# ============================================================
# ХЕЛПЕРЫ: DuckDB
# ============================================================
def _is_duckdb(val):
    try:
        from duckdb_engine import DuckDBTable
        return isinstance(val, DuckDBTable)
    except ImportError:
        return False


# ============================================================
# АВТООПРЕДЕЛЕНИЕ ФОРМАТА
# ============================================================
_TIME_AUTO_FORMATS = [
    "HH:MM:SS",
    "HH:MM",
    "HH",
    "hh:MM:SS AM",
    "hh:MM AM",
    "hh AM",
]

_DATE_AUTO_FORMATS = [
    "DD.MM.YYYY",
    "YYYY-MM-DD",
    "DD/MM/YYYY",
    "MM/DD/YYYY",
    "DD.MM.YY",
    "YYYY/MM/DD",
]

_DATETIME_AUTO_FORMATS = [
    "DD.MM.YYYY HH:MM:SS",
    "DD.MM.YYYY HH:MM",
    "DD.MM.YYYY hh:MM:SS AM",
    "DD.MM.YYYY hh:MM AM",
    "YYYY-MM-DD HH:MM:SS",
    "YYYY-MM-DD HH:MM",
    "YYYY-MM-DD hh:MM:SS AM",
    "YYYY-MM-DD hh:MM AM",
]


def _try_parse_auto(value, is_time_only=False):
    """Пробует распарсить значение автоподбором форматов.
    Возвращает (datetime, использованный_формат) или (None, None)."""
    if not isinstance(value, str):
        return (None, None)
    if value.strip() == "":
        return (None, None)

    if is_time_only:
        formats = _TIME_AUTO_FORMATS
    else:
        formats = (
            _DATETIME_AUTO_FORMATS
            + _DATE_AUTO_FORMATS
            + _TIME_AUTO_FORMATS
        )

    for fmt in formats:
        try:
            dt = datetime.datetime.strptime(value, _to_strptime_format(fmt))
            return (dt, fmt)
        except (ValueError, TypeError):
            continue

    return (None, None)


# ============================================================
# ХЕЛПЕРЫ: формат
# ============================================================
def _to_strptime_format(fmt):
    """
    'DD.MM.YYYY'  → '%d.%m.%Y'
    'hh:MM AM'    → '%I:%M %p'
    'DD.MM.YYYY HH:MM' → '%d.%m.%Y %H:%M'
    """
    if not isinstance(fmt, str):
        return "%d.%m.%Y"

    result = fmt

    # 1. AM/PM
    result = result.replace("AM", "%p").replace("PM", "%p")

    # 2. День недели (на будущее)
    result = result.replace("dddd", "%A")
    result = result.replace("ddd", "%a")

    # 3. Названия месяцев (до MM!)
    result = result.replace("MMMM", "%B")
    result = result.replace("MMM", "%b")

    # 4. Год
    result = result.replace("YYYY", "%Y")
    result = result.replace("YY", "%y")

    # 5. Часы
    result = result.replace("HH", "%H")
    result = result.replace("hh", "%I")

    # 6. Секунды
    result = result.replace("SS", "%S")

    # 7. MM — контекстно
    hour_pos = -1
    if "%H" in result:
        hour_pos = result.find("%H")
    elif "%I" in result:
        hour_pos = result.find("%I")

    if hour_pos >= 0:
        before = result[:hour_pos].replace("MM", "%m")
        after = result[hour_pos:].replace("MM", "%M")
        result = before + after
    else:
        result = result.replace("MM", "%m")

    # 8. День
    result = result.replace("DD", "%d")

    return result


# ============================================================
# ХЕЛПЕРЫ: парсинг одного значения
# ============================================================
def _parse_single(value, fmt):
    """Строка → datetime или None."""
    if value is None:
        return None
    if not isinstance(value, str):
        return None
    if value.strip() == "":
        return None

    try:
        return datetime.datetime.strptime(value, _to_strptime_format(fmt))
    except (ValueError, TypeError):
        return None


def _parse_single_with_auto(value, fmt, is_time_only=False):
    """Сначала пробует fmt, потом автоопределение."""
    if fmt is not None:
        dt = _parse_single(value, fmt)
        if dt is not None:
            return dt
    dt, _ = _try_parse_auto(value, is_time_only=is_time_only)
    return dt


# ============================================================
# ХЕЛПЕРЫ: извлечение компонента
# ============================================================
def _extract_from_dt(dt, kind):
    """Извлекает компонент из уже разобранной даты."""
    if dt is None:
        return None

    if kind == 'year':
        return dt.year
    if kind == 'month':
        return dt.month
    if kind == 'day':
        return dt.day
    if kind == 'quarter':
        return (dt.month - 1) // 3 + 1
    if kind == 'weekday':
        return dt.weekday() + 1
    if kind == 'weekdayname':
        return WEEKDAYS_RU[dt.weekday()]
    if kind == 'monthname':
        return MONTHS_RU_NOM[dt.month - 1]
    if kind == 'hour':
        return dt.hour
    if kind == 'minute':
        return dt.minute
    if kind == 'second':
        return dt.second
    if kind == 'ampm':
        return "PM" if dt.hour >= 12 else "AM"
    if kind == 'is_pm':
        return dt.hour >= 12

    return None


def _extract_single(value, fmt, kind):
    """Извлекает компонент из строки."""
    dt = _parse_single_with_auto(value, fmt)
    return _extract_from_dt(dt, kind)


# ============================================================
# ХЕЛПЕРЫ: арифметика
# ============================================================
def _days_in_month(year, month):
    if month == 2:
        if year % 4 == 0 and (year % 100 != 0 or year % 400 == 0):
            return 29
        return 28
    return DAYS_IN_MONTH[month - 1]


def _add_datetime(dt, n, unit):
    """Прибавляет N единиц. Возвращает datetime или None."""
    if dt is None:
        return None

    if unit == 'days':
        return dt + datetime.timedelta(days=n)
    if unit == 'hours':
        return dt + datetime.timedelta(hours=n)
    if unit == 'minutes':
        return dt + datetime.timedelta(minutes=n)
    if unit == 'seconds':
        return dt + datetime.timedelta(seconds=n)
    if unit == 'months':
        m = dt.month - 1 + n
        y = dt.year + m // 12
        m = m % 12 + 1
        d = min(dt.day, _days_in_month(y, m))
        return dt.replace(year=y, month=m, day=d)
    if unit == 'years':
        y = dt.year + n
        d = min(dt.day, _days_in_month(y, dt.month))
        return dt.replace(year=y, day=d)

    return None


def _detect_add_output_format(value, unit):
    """
    Определяет формат вывода для add*.

    Логика: ВСЕГДА используем формат входной строки.
    То есть:
        adddays("20.06.2025", 10)   → "30.06.2025"
        addhours("14:30:15", 2)     → "16:30:15"
        addminutes("14:30", 45)     → "15:15"

    Если входную строку распознать не удалось — fallback на DD.MM.YYYY.
    """
    if not isinstance(value, str):
        return "DD.MM.YYYY"

    v = value.strip()
    v_upper = v.upper()

    has_am_pm = ('AM' in v_upper) or ('PM' in v_upper)
    has_seconds = v.count(':') >= 2
    has_colon = ':' in v
    has_date_sep = ('.' in v) or ('-' in v) or ('/' in v)
    has_digit = any(c.isdigit() for c in v)

    has_date = has_digit and has_date_sep

    # --- Дата + время ---
    if has_date and has_am_pm:
        return "DD.MM.YYYY hh:MM:SS AM" if has_seconds else "DD.MM.YYYY hh:MM AM"
    if has_date and has_colon:
        return "DD.MM.YYYY HH:MM:SS" if has_seconds else "DD.MM.YYYY HH:MM"
    if has_date:
        return "DD.MM.YYYY"

    # --- Только время ---
    if has_am_pm:
        return "hh:MM:SS AM" if has_seconds else "hh:MM AM"
    if has_seconds:
        return "HH:MM:SS"
    if has_colon:
        return "HH:MM"

    # Fallback
    return "DD.MM.YYYY"


def _add_single(value, n, unit, fmt):
    """Прибавляет N единиц к дате/времени. Использует fmt если задан."""
    dt = _parse_single_with_auto(value, fmt)
    if dt is None:
        return None

    try:
        n = int(n)
    except (ValueError, TypeError):
        return None

    dt2 = _add_datetime(dt, n, unit)
    if dt2 is None:
        return None

    return dt2.strftime(_to_strptime_format(fmt))


# ============================================================
# ХЕЛПЕРЫ: обрезка
# ============================================================
def _trunc_datetime(dt, unit):
    """Обрезает дату/время. Возвращает datetime или None."""
    if dt is None:
        return None

    if unit == 'day':
        return dt.replace(hour=0, minute=0, second=0, microsecond=0)
    if unit == 'month':
        return dt.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    if unit == 'quarter':
        m = (dt.month - 1) // 3 * 3 + 1
        return dt.replace(month=m, day=1, hour=0, minute=0, second=0, microsecond=0)
    if unit == 'year':
        return dt.replace(month=1, day=1, hour=0, minute=0, second=0, microsecond=0)
    if unit == 'hour':
        return dt.replace(minute=0, second=0, microsecond=0)
    if unit == 'minute':
        return dt.replace(second=0, microsecond=0)
    if unit == 'second':
        return dt.replace(microsecond=0)
    return None


def _trunc_single(value, unit, fmt):
    """Обрезает дату/время. Использует fmt если задан."""
    dt = _parse_single_with_auto(value, fmt)
    if dt is None:
        return None
    dt2 = _trunc_datetime(dt, unit)
    if dt2 is None:
        return None
    return dt2.strftime(_to_strptime_format(fmt))


def _trunc_time_single(value, unit, fmt):
    """Обрезает время. Алиас для _trunc_single."""
    return _trunc_single(value, unit, fmt)


# ============================================================
# ХЕЛПЕРЫ: конвертация
# ============================================================
def _convert_single(value, in_fmt, out_fmt):
    """Конвертирует формат. Если не распознано — возвращает как есть."""
    if value is None:
        return None

    if not isinstance(value, str):
        return value

    if value.strip() == "":
        return value

    dt = None
    if in_fmt:
        dt = _parse_single(value, in_fmt)
    if dt is None:
        dt, _ = _try_parse_auto(value, is_time_only=False)

    if dt is None:
        return value

    try:
        return dt.strftime(_to_strptime_format(out_fmt))
    except Exception:
        return value


# ============================================================
# DuckDB
# ============================================================
def _extract_duckdb_column(index_node, env, func_name):
    from ast_nodes.index import IndexNode

    if not isinstance(index_node, IndexNode):
        return (None, None)
    if len(index_node.indices) != 2:
        return (None, None)

    try:
        matrix_obj = index_node.matrix.evaluate(env)
    except Exception:
        return (None, None)

    if not _is_duckdb(matrix_obj):
        return (None, None)

    row_spec_node = index_node.indices[0]
    row_spec = (row_spec_node.evaluate(env)
                if hasattr(row_spec_node, 'evaluate')
                else row_spec_node)

    is_full = (isinstance(row_spec, str)
               and row_spec.strip().lower() in (':', 'all'))
    if not is_full:
        raise ValueError(
            f"{func_name}: DuckDB не поддерживает диапазоны строк.\n"
            f"  Указано: {row_spec}\n"
            f"  Используйте: {func_name}(m[:, \"Дата\"])"
        )

    col_spec_node = index_node.indices[1]
    col_spec = (col_spec_node.evaluate(env)
                if hasattr(col_spec_node, 'evaluate')
                else col_spec_node)

    from .filterif import _resolve_column_for_duckdb
    columns = matrix_obj.get_columns()
    col_idx = _resolve_column_for_duckdb(columns, col_spec)
    if 0 <= col_idx < len(columns):
        return (matrix_obj, columns[col_idx])
    return (None, None)


# ============================================================
# АНАЛИЗ СРЕЗА МАТРИЦЫ
# ============================================================
def _analyze_matrix_index(index_node, env):
    if not hasattr(index_node, 'indices'):
        return None
    if len(index_node.indices) != 2:
        return None

    matrix_obj = index_node.matrix.evaluate(env)
    if not hasattr(matrix_obj, 'data') or not matrix_obj.is_2d:
        return None

    row_spec_node = index_node.indices[0]
    row_spec = (row_spec_node.evaluate(env)
                if hasattr(row_spec_node, 'evaluate')
                else row_spec_node)

    row_start, row_end = parse_range_spec(
        row_spec, matrix_obj.rows, is_column=False
    )

    is_explicit = False
    if isinstance(row_spec, str) and row_spec.strip().lower() not in (':', 'all'):
        is_explicit = True
    elif isinstance(row_spec, (int, float)):
        is_explicit = True

    col_spec_node = index_node.indices[1]
    col_spec = (col_spec_node.evaluate(env)
                if hasattr(col_spec_node, 'evaluate')
                else col_spec_node)

    col_info = None
    skip_header = False

    if isinstance(col_spec, str):
        s = col_spec.strip().lower()

        if s in (':', 'all'):
            col_info = (1, matrix_obj.cols)
        elif s == 'end':
            col_info = (matrix_obj.cols, matrix_obj.cols)
        elif s.startswith('end-'):
            try:
                n = int(s[4:].strip())
                idx = matrix_obj.cols - n
                if idx < 1:
                    idx = 1
                col_info = (idx, idx)
            except Exception:
                col_info = (1, matrix_obj.cols)
        elif s.startswith('last'):
            rest = s[4:].strip()
            try:
                n = int(rest)
                if n == 1:
                    col_info = (matrix_obj.cols, matrix_obj.cols)
                else:
                    col_info = (matrix_obj.cols - n + 1, matrix_obj.cols)
            except Exception:
                col_info = (1, matrix_obj.cols)
        elif ':' in s:
            col_start, col_end = parse_range_spec(
                s, matrix_obj.cols, is_column=True
            )
            col_info = (col_start, col_end)
        else:
            idx, skip_header = resolve_column_index(
                matrix_obj, col_spec, env
            )
            col_info = (idx + 1, idx + 1)
    elif isinstance(col_spec, (int, float)):
        n = int(col_spec)
        if n < 1 or n > matrix_obj.cols:
            n = matrix_obj.cols
        col_info = (n, n)
    else:
        col_info = (1, matrix_obj.cols)

    if not is_explicit and skip_header:
        row_start = max(row_start, 2)

    return (matrix_obj, row_start, row_end, col_info)


# ============================================================
# ПРИМЕНЕНИЕ ФУНКЦИИ К СРЕЗУ
# ============================================================
def _apply_to_matrix_slice(matrix_obj, row_start, row_end, col_info, fn):
    col_start, col_end = col_info

    if row_start == row_end and col_start == col_end:
        i = row_start - 1
        j = col_start - 1
        if i < len(matrix_obj.data) and j < len(matrix_obj.data[i]):
            return fn(matrix_obj.data[i][j])
        return None

    result_data = [
        row.copy() if isinstance(row, list) else [row]
        for row in matrix_obj.data
    ]

    for i in range(row_start - 1, row_end):
        if i >= len(result_data):
            continue
        row = result_data[i]
        for j in range(col_start - 1, col_end):
            if j < len(row):
                row[j] = fn(row[j])

    n_cols = col_end - col_start + 1

    if n_cols == 1:
        j = col_start - 1
        vector_data = []
        for i in range(row_start - 1, row_end):
            if i < len(result_data):
                row = result_data[i]
                vector_data.append(row[j] if j < len(row) else None)
        return MatrExMatrix(vector_data, False)
    else:
        return MatrExMatrix(result_data, True)


def _apply_to_vector_slice(vector_obj, start, end, fn):
    if start == end:
        i = start - 1
        if 0 <= i < len(vector_obj.data):
            return fn(vector_obj.data[i])
        return None

    result_data = list(vector_obj.data)
    for i in range(start - 1, end):
        if i < len(result_data):
            result_data[i] = fn(result_data[i])

    return MatrExMatrix(result_data, False)


# ============================================================
# БАЗОВЫЙ КЛАСС: извлечение
# ============================================================
class _DateExtractBase(Node):
    _kind = None
    _name = None
    _is_time_only = False

    def __init__(self, data, fmt=None):
        self.data = data
        self.fmt = fmt

    def _eval_fmt(self, env):
        if self.fmt is None:
            return None
        val = (self.fmt.evaluate(env)
               if hasattr(self.fmt, 'evaluate')
               else self.fmt)
        if not isinstance(val, str):
            raise TypeError(
                f"{self._name}: формат должен быть строкой, "
                f"получено {type(val).__name__}"
            )
        if val.strip() == "":
            return None
        return val

    def evaluate(self, env):
        from ast_nodes.index import IndexNode

        fmt = self._eval_fmt(env)
        kind = self._kind

        def fn(v):
            return _extract_single(v, fmt, kind)

        # DUCKDB
        duck_table, col_name = _extract_duckdb_column(
            self.data, env, self._name
        )
        if duck_table is not None:
            raise NotImplementedError(
                f"{self._name}: DuckDB пока не поддерживается для дат/времени."
            )

        # МАТРИЦА: срез
        analysis = _analyze_matrix_index(self.data, env)
        if analysis is not None:
            matrix_obj, row_start, row_end, col_info = analysis
            return _apply_to_matrix_slice(
                matrix_obj, row_start, row_end, col_info, fn
            )

        # СРЕЗ ВЕКТОРА
        if isinstance(self.data, IndexNode) and len(self.data.indices) == 1:
            vector_obj = self.data.matrix.evaluate(env)
            if hasattr(vector_obj, 'data') and not vector_obj.is_2d:
                idx_spec_node = self.data.indices[0]
                idx_spec = (idx_spec_node.evaluate(env)
                            if hasattr(idx_spec_node, 'evaluate')
                            else idx_spec_node)
                start, end = parse_range_spec(
                    idx_spec, len(vector_obj.data), is_column=False
                )
                return _apply_to_vector_slice(
                    vector_obj, start, end, fn
                )

        # ОБЫЧНЫЙ РЕЖИМ
        data_obj = self.data.evaluate(env)

        if isinstance(data_obj, str) or data_obj is None:
            return fn(data_obj)

        if not hasattr(data_obj, 'data'):
            return None

        if data_obj.is_2d:
            result_data = []
            for row in data_obj.data:
                new_row = [fn(v) for v in row]
                result_data.append(new_row)
            return MatrExMatrix(result_data, True)

        result_data = [fn(v) for v in data_obj.data]
        return MatrExMatrix(result_data, False)

    def __repr__(self):
        if self.fmt is not None:
            return f"{self._name}({self.data}, {self.fmt})"
        return f"{self._name}({self.data})"


# ============================================================
# КОНКРЕТНЫЕ КЛАССЫ: ДАТЫ
# ============================================================
class YearNode(_DateExtractBase):
    _kind = 'year'
    _name = 'year'


class MonthNode(_DateExtractBase):
    _kind = 'month'
    _name = 'month'


class DayNode(_DateExtractBase):
    _kind = 'day'
    _name = 'day'


class QuarterNode(_DateExtractBase):
    _kind = 'quarter'
    _name = 'quarter'


class WeekdayNode(_DateExtractBase):
    _kind = 'weekday'
    _name = 'weekday'


class WeekdayNameNode(_DateExtractBase):
    _kind = 'weekdayname'
    _name = 'weekdayname'


class MonthNameNode(_DateExtractBase):
    _kind = 'monthname'
    _name = 'monthname'


# ============================================================
# КОНКРЕТНЫЕ КЛАССЫ: ВРЕМЯ
# ============================================================
class HourNode(_DateExtractBase):
    _kind = 'hour'
    _name = 'hour'


class MinuteNode(_DateExtractBase):
    _kind = 'minute'
    _name = 'minute'


class SecondNode(_DateExtractBase):
    _kind = 'second'
    _name = 'second'


class AmPmNode(_DateExtractBase):
    _kind = 'ampm'
    _name = 'ampm'


class IsPmNode(_DateExtractBase):
    _kind = 'is_pm'
    _name = 'is_pm'


# ============================================================
# БАЗОВЫЙ КЛАСС: арифметика
# ============================================================
class _DateAddBase(Node):
    _unit = None
    _name = None

    def __init__(self, data, n, fmt=None):
        self.data = data
        self.n = n
        self.fmt = fmt

    def _eval_fmt(self, env):
        if self.fmt is None:
            return None
        val = (self.fmt.evaluate(env)
               if hasattr(self.fmt, 'evaluate')
               else self.fmt)
        if not isinstance(val, str):
            raise TypeError(
                f"{self._name}: формат должен быть строкой, "
                f"получено {type(val).__name__}"
            )
        if val.strip() == "":
            return None
        return val

    def _eval_n(self, env):
        val = (self.n.evaluate(env)
               if hasattr(self.n, 'evaluate')
               else self.n)
        if isinstance(val, bool):
            raise TypeError(f"{self._name}: N не может быть bool")
        try:
            return int(val)
        except (ValueError, TypeError):
            raise TypeError(
                f"{self._name}: N должно быть числом, "
                f"получено {type(val).__name__}"
            )

    def evaluate(self, env):
        from ast_nodes.index import IndexNode

        fmt = self._eval_fmt(env)
        n = self._eval_n(env)
        unit = self._unit

        def fn(v):
            if fmt is None:
                # Авто: определяем формат по входной строке
                dt = _parse_single_with_auto(v, None)
                if dt is None:
                    return None
                out_fmt = _detect_add_output_format(v, unit)
                dt2 = _add_datetime(dt, n, unit)
                if dt2 is None:
                    return None
                try:
                    return dt2.strftime(_to_strptime_format(out_fmt))
                except Exception:
                    return None
            else:
                return _add_single(v, n, unit, fmt)

        # DUCKDB
        duck_table, col_name = _extract_duckdb_column(
            self.data, env, self._name
        )
        if duck_table is not None:
            raise NotImplementedError(
                f"{self._name}: DuckDB пока не поддерживается."
            )

        # МАТРИЦА: срез
        analysis = _analyze_matrix_index(self.data, env)
        if analysis is not None:
            matrix_obj, row_start, row_end, col_info = analysis
            return _apply_to_matrix_slice(
                matrix_obj, row_start, row_end, col_info, fn
            )

        # СРЕЗ ВЕКТОРА
        if isinstance(self.data, IndexNode) and len(self.data.indices) == 1:
            vector_obj = self.data.matrix.evaluate(env)
            if hasattr(vector_obj, 'data') and not vector_obj.is_2d:
                idx_spec_node = self.data.indices[0]
                idx_spec = (idx_spec_node.evaluate(env)
                            if hasattr(idx_spec_node, 'evaluate')
                            else idx_spec_node)
                start, end = parse_range_spec(
                    idx_spec, len(vector_obj.data), is_column=False
                )
                return _apply_to_vector_slice(
                    vector_obj, start, end, fn
                )

        # ОБЫЧНЫЙ РЕЖИМ
        data_obj = self.data.evaluate(env)

        if isinstance(data_obj, str) or data_obj is None:
            return fn(data_obj)

        if not hasattr(data_obj, 'data'):
            return None

        if data_obj.is_2d:
            result_data = []
            for row in data_obj.data:
                new_row = [fn(v) for v in row]
                result_data.append(new_row)
            return MatrExMatrix(result_data, True)

        result_data = [fn(v) for v in data_obj.data]
        return MatrExMatrix(result_data, False)

    def __repr__(self):
        if self.fmt is not None:
            return f"{self._name}({self.data}, {self.n}, {self.fmt})"
        return f"{self._name}({self.data}, {self.n})"


# ============================================================
# КОНКРЕТНЫЕ КЛАССЫ: АРИФМЕТИКА
# ============================================================
class AddDaysNode(_DateAddBase):
    _unit = 'days'
    _name = 'adddays'


class AddMonthsNode(_DateAddBase):
    _unit = 'months'
    _name = 'addmonths'


class AddYearsNode(_DateAddBase):
    _unit = 'years'
    _name = 'addyears'


class AddHoursNode(_DateAddBase):
    _unit = 'hours'
    _name = 'addhours'


class AddMinutesNode(_DateAddBase):
    _unit = 'minutes'
    _name = 'addminutes'


class AddSecondsNode(_DateAddBase):
    _unit = 'seconds'
    _name = 'addseconds'


# ============================================================
# DATE_TRUNC
# ============================================================
class DateTruncNode(Node):
    _name = 'datetrunc'

    def __init__(self, data, unit, fmt=None):
        self.data = data
        self.unit = unit
        self.fmt = fmt

    def _eval_fmt(self, env):
        if self.fmt is None:
            return None
        val = (self.fmt.evaluate(env)
               if hasattr(self.fmt, 'evaluate')
               else self.fmt)
        if not isinstance(val, str):
            raise TypeError(
                f"{self._name}: формат должен быть строкой, "
                f"получено {type(val).__name__}"
            )
        if val.strip() == "":
            return None
        return val

    def _eval_unit(self, env):
        val = (self.unit.evaluate(env)
               if hasattr(self.unit, 'evaluate')
               else self.unit)

        if not isinstance(val, str):
            from errors import ArrayVatorError
            raise ArrayVatorError(code="DATETRUNC_BAD_UNIT")

        val = val.strip().lower()

        if val not in ('day', 'month', 'quarter', 'year',
                       'hour', 'minute', 'second'):
            from errors import ArrayVatorError
            raise ArrayVatorError(code="DATETRUNC_BAD_UNIT")
        return val

    def evaluate(self, env):
        from ast_nodes.index import IndexNode

        fmt = self._eval_fmt(env)
        unit = self._eval_unit(env)

        def fn(v):
            if fmt is None:
                # Авто: определяем формат входной строки
                dt = _parse_single_with_auto(v, None)
                if dt is None:
                    return None
                out_fmt = _detect_trunc_output_format(v, unit)
                dt2 = _trunc_datetime(dt, unit)
                if dt2 is None:
                    return None
                try:
                    return dt2.strftime(_to_strptime_format(out_fmt))
                except Exception:
                    return None
            else:
                return _trunc_single(v, unit, fmt)

        # DUCKDB
        duck_table, col_name = _extract_duckdb_column(
            self.data, env, self._name
        )
        if duck_table is not None:
            raise NotImplementedError(
                f"{self._name}: DuckDB пока не поддерживается."
            )

        analysis = _analyze_matrix_index(self.data, env)
        if analysis is not None:
            matrix_obj, row_start, row_end, col_info = analysis
            return _apply_to_matrix_slice(
                matrix_obj, row_start, row_end, col_info, fn
            )

        if isinstance(self.data, IndexNode) and len(self.data.indices) == 1:
            vector_obj = self.data.matrix.evaluate(env)
            if hasattr(vector_obj, 'data') and not vector_obj.is_2d:
                idx_spec_node = self.data.indices[0]
                idx_spec = (idx_spec_node.evaluate(env)
                            if hasattr(idx_spec_node, 'evaluate')
                            else idx_spec_node)
                start, end = parse_range_spec(
                    idx_spec, len(vector_obj.data), is_column=False
                )
                return _apply_to_vector_slice(
                    vector_obj, start, end, fn
                )

        data_obj = self.data.evaluate(env)

        if isinstance(data_obj, str) or data_obj is None:
            return fn(data_obj)

        if not hasattr(data_obj, 'data'):
            return None

        if data_obj.is_2d:
            result_data = []
            for row in data_obj.data:
                new_row = [fn(v) for v in row]
                result_data.append(new_row)
            return MatrExMatrix(result_data, True)

        result_data = [fn(v) for v in data_obj.data]
        return MatrExMatrix(result_data, False)

    def __repr__(self):
        if self.fmt is not None:
            return f"{self._name}({self.data}, {self.unit}, {self.fmt})"
        return f"{self._name}({self.data}, {self.unit})"


def _detect_trunc_output_format(value, unit):
    """
    Определяет формат вывода для datetrunc.
    Если входная строка — дата, выводим дату.
    Если время — время.
    """
    return _detect_add_output_format(value, unit)


# ============================================================
# TIME_TRUNC
# ============================================================
class TimeTruncNode(Node):
    _name = 'timetrunc'

    def __init__(self, data, unit, fmt=None):
        self.data = data
        self.unit = unit
        self.fmt = fmt

    def _eval_fmt(self, env):
        if self.fmt is None:
            return None
        val = (self.fmt.evaluate(env)
               if hasattr(self.fmt, 'evaluate')
               else self.fmt)
        if not isinstance(val, str):
            raise TypeError(
                f"{self._name}: формат должен быть строкой, "
                f"получено {type(val).__name__}"
            )
        if val.strip() == "":
            return None
        return val

    def _eval_unit(self, env):
        val = (self.unit.evaluate(env)
               if hasattr(self.unit, 'evaluate')
               else self.unit)
        if not isinstance(val, str):
            from errors import ArrayVatorError
            raise ArrayVatorError(code="TIMETRUNC_BAD_UNIT")
        val = val.strip().lower()
        if val not in ('hour', 'minute', 'second'):
            from errors import ArrayVatorError
            raise ArrayVatorError(code="TIMETRUNC_BAD_UNIT")
        return val

    def evaluate(self, env):
        from ast_nodes.index import IndexNode

        fmt = self._eval_fmt(env)
        unit = self._eval_unit(env)

        def fn(v):
            if fmt is None:
                # Авто: определяем формат входной строки (время)
                dt = _parse_single_with_auto(v, None, is_time_only=True)
                if dt is None:
                    dt = _parse_single_with_auto(v, None)
                if dt is None:
                    return None
                out_fmt = _detect_time_output_format(v)
                dt2 = _trunc_datetime(dt, unit)
                if dt2 is None:
                    return None
                try:
                    return dt2.strftime(_to_strptime_format(out_fmt))
                except Exception:
                    return None
            else:
                return _trunc_single(v, unit, fmt)

        analysis = _analyze_matrix_index(self.data, env)
        if analysis is not None:
            matrix_obj, row_start, row_end, col_info = analysis
            return _apply_to_matrix_slice(
                matrix_obj, row_start, row_end, col_info, fn
            )

        if isinstance(self.data, IndexNode) and len(self.data.indices) == 1:
            vector_obj = self.data.matrix.evaluate(env)
            if hasattr(vector_obj, 'data') and not vector_obj.is_2d:
                idx_spec_node = self.data.indices[0]
                idx_spec = (idx_spec_node.evaluate(env)
                            if hasattr(idx_spec_node, 'evaluate')
                            else idx_spec_node)
                start, end = parse_range_spec(
                    idx_spec, len(vector_obj.data), is_column=False
                )
                return _apply_to_vector_slice(
                    vector_obj, start, end, fn
                )

        data_obj = self.data.evaluate(env)

        if isinstance(data_obj, str) or data_obj is None:
            return fn(data_obj)

        if not hasattr(data_obj, 'data'):
            return None

        if data_obj.is_2d:
            result_data = []
            for row in data_obj.data:
                new_row = [fn(v) for v in row]
                result_data.append(new_row)
            return MatrExMatrix(result_data, True)

        result_data = [fn(v) for v in data_obj.data]
        return MatrExMatrix(result_data, False)

    def __repr__(self):
        if self.fmt is not None:
            return f"{self._name}({self.data}, {self.unit}, {self.fmt})"
        return f"{self._name}({self.data}, {self.unit})"


def _detect_time_output_format(value):
    """Определяет формат вывода для timetrunc."""
    if not isinstance(value, str):
        return "HH:MM:SS"

    v_upper = value.upper()
    has_seconds = value.count(':') >= 2
    has_am_pm = ('AM' in v_upper) or ('PM' in v_upper)

    if has_am_pm:
        return "hh:MM:SS AM" if has_seconds else "hh:MM AM"
    return "HH:MM:SS" if has_seconds else "HH:MM"


# ============================================================
# TIME — конвертер форматов
# ============================================================
class TimeNode(Node):
    _name = 'time'

    def __init__(self, data, in_format, out_format):
        self.data = data
        self.in_format = in_format
        self.out_format = out_format

    def _eval_fmt(self, node, env, default="HH:MM:SS"):
        if node is None:
            return default
        val = (node.evaluate(env)
               if hasattr(node, 'evaluate')
               else node)
        if not isinstance(val, str):
            raise TypeError(
                f"time: формат должен быть строкой, "
                f"получено {type(val).__name__}"
            )
        return val

    def evaluate(self, env):
        from ast_nodes.index import IndexNode

        in_fmt = self._eval_fmt(self.in_format, env, default="")
        out_fmt = self._eval_fmt(self.out_format, env, default="HH:MM:SS")

        def fn(v):
            return _convert_single(v, in_fmt, out_fmt)

        analysis = _analyze_matrix_index(self.data, env)
        if analysis is not None:
            matrix_obj, row_start, row_end, col_info = analysis
            return _apply_to_matrix_slice(
                matrix_obj, row_start, row_end, col_info, fn
            )

        if isinstance(self.data, IndexNode) and len(self.data.indices) == 1:
            vector_obj = self.data.matrix.evaluate(env)
            if hasattr(vector_obj, 'data') and not vector_obj.is_2d:
                idx_spec_node = self.data.indices[0]
                idx_spec = (idx_spec_node.evaluate(env)
                            if hasattr(idx_spec_node, 'evaluate')
                            else idx_spec_node)
                start, end = parse_range_spec(
                    idx_spec, len(vector_obj.data), is_column=False
                )
                return _apply_to_vector_slice(
                    vector_obj, start, end, fn
                )

        data_obj = self.data.evaluate(env)

        if isinstance(data_obj, str) or data_obj is None:
            return fn(data_obj)

        if not hasattr(data_obj, 'data'):
            return fn(data_obj)

        if data_obj.is_2d:
            result_data = []
            for row in data_obj.data:
                new_row = [fn(v) for v in row]
                result_data.append(new_row)
            return MatrExMatrix(result_data, True)

        result_data = [fn(v) for v in data_obj.data]
        return MatrExMatrix(result_data, False)

    def __repr__(self):
        return f"time({self.data}, {self.in_format}, {self.out_format})"