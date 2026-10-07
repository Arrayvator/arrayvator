# ast_nodes/functions/is_valid_time.py
"""
Функция IS_VALID_TIME — проверка, что строка является корректным временем.

СИНТАКСИС:
    is_valid_time("14:30:15")                    # True
    is_valid_time("14:30")                       # True
    is_valid_time("02:30 PM")                    # True
    is_valid_time("25:99:99")                    # False
    is_valid_time("29.09.2026")                  # False (это дата, не время)

    is_valid_time(m[:, "Время"])
    is_valid_time(m[:, "Время"], "HH:MM:SS")

ПРАВИЛА:
    - Если формат не указан — автоопределение.
    - None → False.
    - Не-строка → False.
    - Пустая строка → False.
    - Вектор / матрица → поэлементно.
"""

import datetime
from ..base import Node
from runtime.matrix import MatrExMatrix
from ..utils.index_utils import parse_range_spec, resolve_column_index


# ============================================================
# ФОРМАТЫ ДЛЯ АВТООПРЕДЕЛЕНИЯ
# ============================================================
_TIME_AUTO_FORMATS = [
    "HH:MM:SS",
    "HH:MM",
    "HH",
    "hh:MM:SS AM",
    "hh:MM AM",
    "hh AM",
]


def _to_strptime_format(fmt):
    """Конвертирует формат ArrayVator в strptime."""
    if not isinstance(fmt, str):
        return "%H:%M:%S"

    result = fmt
    result = result.replace("AM", "%p").replace("PM", "%p")
    result = result.replace("HH", "%H")
    result = result.replace("hh", "%I")
    result = result.replace("SS", "%S")
    result = result.replace("YYYY", "%Y")
    result = result.replace("YY", "%y")

    has_hour = ("%H" in result) or ("%I" in result)
    if has_hour:
        result = result.replace("MM", "%M")
    else:
        result = result.replace("MM", "%m")

    result = result.replace("DD", "%d")
    return result


def _is_valid_time_single(value, fmt=None):
    """Проверяет одно значение."""
    if value is None:
        return False
    if not isinstance(value, str):
        return False
    if value.strip() == "":
        return False

    if fmt:
        try:
            datetime.datetime.strptime(value, _to_strptime_format(fmt))
            return True
        except (ValueError, TypeError):
            pass

    # Автоопределение
    for auto_fmt in _TIME_AUTO_FORMATS:
        try:
            datetime.datetime.strptime(value, _to_strptime_format(auto_fmt))
            return True
        except (ValueError, TypeError):
            continue

    return False


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
# IS_VALID_TIME NODE
# ============================================================
class IsValidTimeNode(Node):
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
                f"is_valid_time: формат должен быть строкой, "
                f"получено {type(val).__name__}"
            )
        if val.strip() == "":
            return None
        return val

    def evaluate(self, env):
        from ast_nodes.index import IndexNode

        fmt = self._eval_fmt(env)

        def fn(v):
            return _is_valid_time_single(v, fmt)

        # МАТРИЦА: срез
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

        if isinstance(data_obj, (int, float, bool)):
            return False

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
        if self.fmt is not None:
            return f"is_valid_time({self.data}, {self.fmt})"
        return f"is_valid_time({self.data})"