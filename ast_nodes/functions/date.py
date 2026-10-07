"""
Функция DATE - конвертация формата даты.

СИНТАКСИС (ТОЛЬКО РЕЖИМ ПРОГРАММИСТА):

    date(данные, "входной_формат", "выходной_формат")

ПРИМЕРЫ:
    date("20.06.2025", "DD.MM.YYYY", "DD MMMM YYYY")
    # → "20 июня 2025"

    date("06/20/2025", "MM/DD/YYYY", "DD.MM.YYYY")
    # → "20.06.2025"

    date("2025-06-20", "YYYY-MM-DD", "DD MONTH YYYY")
    # → "20 июня 2025"

    date("20.06.2025 15:30", "DD.MM.YYYY HH:MM", "DD.MM.YYYY")
    # → "20.06.2025"

ТОКЕНЫ:
    YYYY / YEAR    — год (4 цифры)
    YY             — год (2 цифры)
    MM / MONTHNUM  — месяц (2 цифры)
    M              — месяц (1-2 цифры)
    MMMM / MONTH   — месяц словом
    MMM / MON       — месяц кратко
    DD / DAY       — день (2 цифры)
    D              — день (1-2 цифры)
    HH / HOUR      — часы
    MM / MIN       — минуты (в time-контексте)
    SS / SEC       — секунды

РАЗДЕЛИТЕЛИ: . / - пробел запятая

ПРАВИЛО:
    Если значение НЕ распознано как дата → оставить как есть.
    Если значение None → оставить None.
    Одна ячейка / один элемент вектора → скаляр.
"""

import re
from ..base import Node
from runtime.matrix import MatrExMatrix
from ..utils.index_utils import parse_range_spec, resolve_column_index


# ============================================================
# МЕСЯЦЫ
# ============================================================
MONTHS_RU = [
    "января", "февраля", "марта", "апреля", "мая", "июня",
    "июля", "августа", "сентября", "октября", "ноября", "декабря"
]

MONTHS_RU_NOM = [
    "январь", "февраль", "март", "апрель", "май", "июнь",
    "июль", "август", "сентябрь", "октябрь", "ноябрь", "декабрь"
]

MONTHS_RU_SHORT = [
    "янв", "фев", "мар", "апр", "май", "июн",
    "июл", "авг", "сен", "окт", "ноя", "дек"
]

MONTHS_EN = [
    "january", "february", "march", "april", "may", "june",
    "july", "august", "september", "october", "november", "december"
]

MONTHS_EN_SHORT = [
    "jan", "feb", "mar", "apr", "may", "jun",
    "jul", "aug", "sep", "oct", "nov", "dec"
]


# ============================================================
# ПАРСИНГ ФОРМАТА
# ============================================================

def _parse_format(fmt):
    """Разбирает строку формата на токены."""
    if not isinstance(fmt, str):
        return None

    fmt_upper = fmt.upper()

    aliases = {
        'YEAR': 'YYYY',
        'MONTHNUM': 'MM',
        'MONTH': 'MMMM',
        'MON': 'MMM',
        'DAY': 'DD',
        'HOUR': 'HH',
        'MIN': 'MM',
        'SEC': 'SS',
    }

    tokens = []
    i = 0
    n = len(fmt_upper)

    while i < n:
        ch = fmt_upper[i]

        if ch in ('.', '/', '-', ' ', ',', ':', 'T'):
            tokens.append(('SEP', fmt[i]))
            i += 1
            continue

        matched = False
        for token_name in ['YYYY', 'MMMM', 'MMM', 'MM', 'DD', 'HH', 'SS', 'YY', 'M', 'D']:
            if fmt_upper[i:i+len(token_name)] == token_name:
                tokens.append(('TOKEN', token_name))
                i += len(token_name)
                matched = True
                break

        if not matched:
            for alias, standard in aliases.items():
                if fmt_upper[i:i+len(alias)] == alias:
                    tokens.append(('TOKEN', standard))
                    i += len(alias)
                    matched = True
                    break

        if not matched:
            i += 1

    return tokens


# ============================================================
# ПАРСИНГ ДАТЫ
# ============================================================

def _parse_date(value, fmt, env=None):
    """Разбирает значение по формату."""
    if value is None:
        return None

    if not isinstance(value, str):
        value = str(value)

    tokens = _parse_format(fmt)
    if not tokens:
        return None

    pattern_parts = []
    token_order = []

    for kind, val in tokens:
        if kind == 'SEP':
            pattern_parts.append(re.escape(val))
        else:
            token_order.append(val)
            if val == 'YYYY':
                pattern_parts.append(r'(\d{4})')
            elif val == 'YY':
                pattern_parts.append(r'(\d{2})')
            elif val == 'MM':
                pattern_parts.append(r'(\d{1,2})')
            elif val == 'M':
                pattern_parts.append(r'(\d{1,2})')
            elif val == 'DD':
                pattern_parts.append(r'(\d{1,2})')
            elif val == 'D':
                pattern_parts.append(r'(\d{1,2})')
            elif val == 'HH':
                pattern_parts.append(r'(\d{1,2})')
            elif val == 'SS':
                pattern_parts.append(r'(\d{1,2})')
            elif val in ('MMMM', 'MMM'):
                pattern_parts.append(r'([A-Za-zА-Яа-яЁё]+)')
            else:
                pattern_parts.append(r'(\S+)')

    pattern = '^' + ''.join(pattern_parts) + '$'
    m = re.match(pattern, value.strip(), re.IGNORECASE)
    if not m:
        return None

    groups = m.groups()

    result = {'year': None, 'month': None, 'day': None,
              'hour': 0, 'minute': 0, 'second': 0}

    for i, token in enumerate(token_order):
        if i >= len(groups):
            break
        g = groups[i]

        if token == 'YYYY':
            result['year'] = int(g)
        elif token == 'YY':
            y = int(g)
            result['year'] = 2000 + y if y < 50 else 1900 + y
        elif token in ('MM', 'M'):
            if result['hour'] is not None and result['hour'] > 0 and result['month'] is not None:
                result['minute'] = int(g)
            else:
                result['month'] = int(g)
        elif token in ('DD', 'D'):
            result['day'] = int(g)
        elif token == 'HH':
            result['hour'] = int(g)
        elif token == 'SS':
            result['second'] = int(g)
        elif token in ('MMMM', 'MMM'):
            month_num = _parse_month_name(g)
            if month_num is not None:
                result['month'] = month_num

    if result['year'] is None or result['month'] is None or result['day'] is None:
        return None

    if not (1 <= result['month'] <= 12):
        return None
    if not (1 <= result['day'] <= 31):
        return None

    return result


def _parse_month_name(name):
    """Распознаёт название месяца."""
    if not name:
        return None
    n = name.lower().strip()

    for i, m in enumerate(MONTHS_RU):
        if n.startswith(m[:3]):
            return i + 1
    for i, m in enumerate(MONTHS_RU_NOM):
        if n.startswith(m[:3]):
            return i + 1
    for i, m in enumerate(MONTHS_RU_SHORT):
        if n.startswith(m[:3]):
            return i + 1
    for i, m in enumerate(MONTHS_EN):
        if n.startswith(m[:3]):
            return i + 1
    for i, m in enumerate(MONTHS_EN_SHORT):
        if n.startswith(m[:3]):
            return i + 1

    return None


# ============================================================
# ФОРМАТИРОВАНИЕ ДАТЫ
# ============================================================

def _format_date(parsed, fmt):
    """Форматирует распарсенную дату."""
    if parsed is None:
        return None

    if not isinstance(fmt, str):
        return None

    tokens = _parse_format(fmt)
    if not tokens:
        return None

    result = []
    hour_seen = False

    for kind, val in tokens:
        if kind == 'SEP':
            result.append(val)
            continue

        if val == 'YYYY':
            result.append(str(parsed['year']).zfill(4) if parsed['year'] else '')
        elif val == 'YY':
            if parsed['year']:
                result.append(str(parsed['year'])[-2:].zfill(2))
            else:
                result.append('')
        elif val == 'MMMM':
            if parsed['month']:
                result.append(MONTHS_RU[parsed['month'] - 1])
            else:
                result.append('')
        elif val == 'MMM':
            if parsed['month']:
                result.append(MONTHS_RU_SHORT[parsed['month'] - 1])
            else:
                result.append('')
        elif val == 'MM':
            if hour_seen:
                result.append(str(parsed['minute']).zfill(2))
            else:
                result.append(str(parsed['month']).zfill(2) if parsed['month'] else '')
        elif val == 'M':
            if hour_seen:
                result.append(str(parsed['minute']))
            else:
                result.append(str(parsed['month']) if parsed['month'] else '')
        elif val == 'DD':
            result.append(str(parsed['day']).zfill(2) if parsed['day'] else '')
        elif val == 'D':
            result.append(str(parsed['day']) if parsed['day'] else '')
        elif val == 'HH':
            result.append(str(parsed['hour']).zfill(2))
            hour_seen = True
        elif val == 'SS':
            result.append(str(parsed['second']).zfill(2))
        else:
            result.append('')

    return ''.join(result)


# ============================================================
# КОНВЕРТАЦИЯ ОДНОГО ЗНАЧЕНИЯ
# ============================================================

def _convert_single(value, in_fmt, out_fmt, env=None):
    """Конвертирует одно значение.
    Если не распознано — оставить как есть.
    """
    if value is None:
        return None

    parsed = _parse_date(value, in_fmt, env)
    if parsed is None:
        return value

    return _format_date(parsed, out_fmt)


# ============================================================
# АНАЛИЗ СРЕЗА МАТРИЦЫ
# ============================================================

def _analyze_matrix_index(index_node, env):
    """Разбирает IndexNode для матрицы."""
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

    row_start, row_end = parse_range_spec(row_spec, matrix_obj.rows, is_column=False)

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
            except:
                col_info = (1, matrix_obj.cols)
        elif s.startswith('last'):
            rest = s[4:].strip()
            try:
                n = int(rest)
                if n == 1:
                    col_info = (matrix_obj.cols, matrix_obj.cols)
                else:
                    col_info = (matrix_obj.cols - n + 1, matrix_obj.cols)
            except:
                col_info = (1, matrix_obj.cols)
        elif ':' in s:
            col_start, col_end = parse_range_spec(s, matrix_obj.cols, is_column=True)
            col_info = (col_start, col_end)
        else:
            idx, skip_header = resolve_column_index(matrix_obj, col_spec, env)
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
# DATE NODE
# ============================================================

class DateNode(Node):
    def __init__(self, data, in_format, out_format):
        self.data = data
        self.in_format = in_format
        self.out_format = out_format

    def evaluate(self, env):
        from ast_nodes.index import IndexNode

        in_fmt = (self.in_format.evaluate(env)
                  if hasattr(self.in_format, 'evaluate')
                  else self.in_format)
        out_fmt = (self.out_format.evaluate(env)
                   if hasattr(self.out_format, 'evaluate')
                   else self.out_format)

        if not isinstance(in_fmt, str):
            raise TypeError(f"Входной формат должен быть строкой, получен {type(in_fmt)}")
        if not isinstance(out_fmt, str):
            raise TypeError(f"Выходной формат должен быть строкой, получен {type(out_fmt)}")

        # ============================================================
        # 1. СРЕЗ МАТРИЦЫ
        # ============================================================
        analysis = _analyze_matrix_index(self.data, env)
        if analysis is not None:
            matrix_obj, row_start, row_end, col_info = analysis
            col_start, col_end = col_info

            # ОДНА ЯЧЕЙКА → скаляр
            if row_start == row_end and col_start == col_end:
                i = row_start - 1
                j = col_start - 1
                if i < len(matrix_obj.data) and j < len(matrix_obj.data[i]):
                    return _convert_single(
                        matrix_obj.data[i][j], in_fmt, out_fmt, env
                    )
                return None

            # ИНАЧЕ → матрица
            result_data = [row.copy() if isinstance(row, list) else [row]
                           for row in matrix_obj.data]

            for i in range(row_start - 1, row_end):
                if i >= len(result_data):
                    continue
                row = result_data[i]
                for j in range(col_start - 1, col_end):
                    if j < len(row):
                        row[j] = _convert_single(row[j], in_fmt, out_fmt, env)

            return MatrExMatrix(result_data, True)

        # ============================================================
        # 2. СРЕЗ ВЕКТОРА
        # ============================================================
        if isinstance(self.data, IndexNode) and len(self.data.indices) == 1:
            vector_obj = self.data.matrix.evaluate(env)
            if hasattr(vector_obj, 'data') and not vector_obj.is_2d:
                idx_spec_node = self.data.indices[0]
                idx_spec = (idx_spec_node.evaluate(env)
                            if hasattr(idx_spec_node, 'evaluate')
                            else idx_spec_node)
                start, end = parse_range_spec(idx_spec, len(vector_obj.data), is_column=False)

                # ОДИН ЭЛЕМЕНТ → скаляр
                if start == end:
                    i = start - 1
                    if 0 <= i < len(vector_obj.data):
                        return _convert_single(
                            vector_obj.data[i], in_fmt, out_fmt, env
                        )
                    return None

                result_data = list(vector_obj.data)
                for i in range(start - 1, end):
                    if i < len(result_data):
                        result_data[i] = _convert_single(result_data[i], in_fmt, out_fmt, env)

                return MatrExMatrix(result_data, False)

        # ============================================================
        # 3. ОБЫЧНЫЙ РЕЖИМ
        # ============================================================
        data_obj = self.data.evaluate(env)

        if hasattr(data_obj, 'data') and data_obj.is_2d:
            result_data = []
            for row in data_obj.data:
                new_row = [_convert_single(v, in_fmt, out_fmt, env) for v in row]
                result_data.append(new_row)
            return MatrExMatrix(result_data, True)

        if hasattr(data_obj, 'data') and not data_obj.is_2d:
            result_data = [_convert_single(v, in_fmt, out_fmt, env)
                           for v in data_obj.data]
            return MatrExMatrix(result_data, False)

        if isinstance(data_obj, (int, float, str)):
            return _convert_single(data_obj, in_fmt, out_fmt, env)

        if isinstance(data_obj, list):
            if data_obj and isinstance(data_obj[0], list):
                result_data = []
                for row in data_obj:
                    new_row = [_convert_single(v, in_fmt, out_fmt, env) for v in row]
                    result_data.append(new_row)
                return MatrExMatrix(result_data, True)
            else:
                result_data = [_convert_single(v, in_fmt, out_fmt, env)
                               for v in data_obj]
                return MatrExMatrix(result_data, False)

        raise TypeError(
            f"date() работает со строками, числами, векторами и матрицами, "
            f"получен {type(data_obj)}"
        )

    def __repr__(self):
        return f"date({self.data}, {self.in_format}, {self.out_format})"