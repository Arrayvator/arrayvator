# ast_nodes/functions/filterif.py
"""
Функция FilterIf - фильтрация строк/элементов по условию.

ВАЖНО: filterif() НЕ изменяет исходную матрицу.
Она ВОЗВРАЩАЕТ НОВУЮ матрицу.

СИНТАКСИС:

    # Матрица:
    filterif(s[:, "Пол"] == "Ж")
    filterif(s[:, 3] > 80)
    filterif(s[10:end, "Итого"] > 100)
    filterif(s[10:end, "Итого"] > 100 and s[10:end, "Класс"] == "10Б")
    filterif(s[:, end] == "Спорт")
    filterif(s[:, last 1] == "Спорт")

    # Вектор:
    filterif(v > 20)
    filterif(v < 5 or v > 90)
    filterif(v[3:6] > 20)
    filterif(v[last 3] > 20)

    # Модификаторы (только для строк):
    filterif(m[:, "Имя"] == "ов", inside)          — поиск подстроки
    filterif(m[:, "Имя"] == "аня", ignore)         — без учёта регистра
    filterif(m[:, "Имя"] == "ов", inside, ignore)  — оба

ПРАВИЛА:
    - По имени [:, "Х"]      → заголовок защищён
    - По номеру [:, 3], end  → заголовок участвует
    - Явный диапазон [10:end, X] → строки 1..9 защищены
    - Все условия в and/or   → один диапазон строк, иначе ошибка
    - В условии — ОДИН столбец

DUCKDB:
    - Если данные в DuckDBTable → фильтрация через SQL
    - Результат — новый DuckDBTable (view)
    - Числовые сравнения — как DOUBLE (иначе '85000' > '100000' даёт True)
    - Строковые сравнения — как VARCHAR

НОВОЕ:
    - Если в условии используется ФУНКЦИЯ (year, month, round, len, ...),
      filterif выдаёт ПОНЯТНУЮ ошибку с решением через addcolumn.
"""

from ..base import Node
from runtime.matrix import MatrExMatrix
from errors import ArrayVatorError
from ..utils.index_utils import (
    parse_range_spec,
    resolve_column_index,
)


# ============================================================
# ХЕЛПЕР: определение DuckDBTable
# ============================================================
def _is_duckdb(val):
    """Проверяет, является ли значение DuckDBTable."""
    try:
        from duckdb_engine import DuckDBTable
        return isinstance(val, DuckDBTable)
    except ImportError:
        return False


# ============================================================
# ДЕТЕКТОР: функция внутри условия
# ============================================================
def _find_function_node_in_condition(condition, env):
    """
    Ищет в условии узел-функцию (year, month, round, len, ...).

    Возвращает (function_name, inner_slice_index_node) или None.

    Пример:
        filterif(year(m[:, "Дата"]) == 2025)
        → ("year", <IndexNode m[:, "Дата"]>)
    """
    from ast_nodes.index import IndexNode
    from ast_nodes.operations import BinaryOp, UnaryOp
    from ast_nodes.variables import VariableNode
    from ast_nodes.base import Node

    def _get_func_name(node):
        """Возвращает человеческое имя функции по типу узла."""
        cls_name = type(node).__name__
        mapping = {
            'YearNode': 'year',
            'MonthNode': 'month',
            'DayNode': 'day',
            'QuarterNode': 'quarter',
            'WeekdayNode': 'weekday',
            'WeekdayNameNode': 'weekdayname',
            'MonthNameNode': 'monthname',
            'HourNode': 'hour',
            'MinuteNode': 'minute',
            'SecondNode': 'second',
            'AmPmNode': 'ampm',
            'IsPmNode': 'is_pm',
            'RoundNode': 'round',
            'IntNode': 'int',
            'FracNode': 'frac',
            'FracDigitsNode': 'frac_digits',
            'LenNode': 'len',
            'LenRowNode': 'lenrow',
            'LenColNode': 'lencol',
            'CaseNode': 'case',
            'IsNullNode': 'isnone',
            'FillnaNode': 'fillna',
            'DropnaNode': 'dropna',
            'CoalesceNode': 'coalesce',
            'NullIfNode': 'noneif',
            'TypeNode': 'type',
            'IsNumberNode': 'is_number',
            'IsIntegerNode': 'is_integer',
            'IsFloatNode': 'is_float',
            'IsStringNode': 'is_string',
            'IsBooleanNode': 'is_boolean',
            'ToNumberNode': 'to_number',
            'ToStringNode': 'to_string',
            'CleanNode': 'clean',
            'ReplaceTextNode': 'replacetext',
            'DeleteTextLeftNode': 'deletetextleft',
            'DeleteTextRightNode': 'deletetextright',
            'TrimNode': 'trim',
            'TrimLeftNode': 'trimleft',
            'TrimRightNode': 'trimright',
            'AddDaysNode': 'adddays',
            'AddMonthsNode': 'addmonths',
            'AddYearsNode': 'addyears',
            'AddHoursNode': 'addhours',
            'AddMinutesNode': 'addminutes',
            'AddSecondsNode': 'addseconds',
            'DateTruncNode': 'datetrunc',
            'TimeTruncNode': 'timetrunc',
            'DateNode': 'date',
            'TimeNode': 'time',
            'TimestampNode': 'timestamp',
            'DateNowNode': 'datenow',
            'TimeNowNode': 'timenow',
            'AbcNode': 'abc',
            'PercentOfNode': 'percentof',
            'AnomalyNode': 'anomaly',
            'SplitNode': 'split',
            'JoinVectorNode': 'joinvector',
        }
        return mapping.get(cls_name, cls_name.replace('Node', '').lower())

    def _find_inner_slice(node):
        """Ищет IndexNode внутри узла-функции."""
        if isinstance(node, IndexNode):
            return node
        for attr_name in ('data', 'arg', 'value', 'column'):
            if hasattr(node, attr_name):
                attr = getattr(node, attr_name)
                if isinstance(attr, IndexNode):
                    return attr
                if isinstance(attr, Node):
                    inner = _find_inner_slice(attr)
                    if inner is not None:
                        return inner
        return None

    def _walk(node):
        if node is None:
            return None

        if isinstance(node, (IndexNode, VariableNode)):
            return None

        if isinstance(node, BinaryOp):
            left = _walk(node.left)
            if left is not None:
                return left
            return _walk(node.right)

        if isinstance(node, UnaryOp):
            return _walk(node.right)

        if isinstance(node, Node):
            inner_slice = _find_inner_slice(node)
            if inner_slice is not None:
                func_name = _get_func_name(node)
                return (func_name, inner_slice)

        return None

    return _walk(condition)


# ============================================================
# АНАЛИЗ СРЕЗА МАТРИЦЫ
# ============================================================
def _analyze_index_node(index_node, env):
    """Разбирает IndexNode для матрицы (2D)."""
    if not hasattr(index_node, 'indices'):
        return None
    if len(index_node.indices) != 2:
        return None

    matrix_obj = index_node.matrix.evaluate(env)

    row_spec_node = index_node.indices[0]
    row_spec = (row_spec_node.evaluate(env)
                if hasattr(row_spec_node, 'evaluate')
                else row_spec_node)

    if _is_duckdb(matrix_obj):
        total_rows = matrix_obj.get_row_count()
    else:
        total_rows = matrix_obj.rows

    row_start, row_end = parse_range_spec(
        row_spec, total_rows, is_column=False
    )

    is_explicit_range = False
    if isinstance(row_spec, str):
        if row_spec.strip().lower() not in (':', 'all'):
            is_explicit_range = True
    elif isinstance(row_spec, (int, float)):
        is_explicit_range = True

    col_spec_node = index_node.indices[1]
    col_spec = (col_spec_node.evaluate(env)
                if hasattr(col_spec_node, 'evaluate')
                else col_spec_node)

    if _is_duckdb(matrix_obj):
        columns = matrix_obj.get_columns()
        col_idx = _resolve_column_for_duckdb(columns, col_spec)
        skip_header = False
    else:
        col_idx, skip_header = resolve_column_index(matrix_obj, col_spec, env)

    if not is_explicit_range and skip_header:
        row_start = max(row_start, 2)

    return (matrix_obj, row_start, row_end, col_idx, is_explicit_range)


def _resolve_column_for_duckdb(columns, col_spec):
    """Находит индекс столбца для DuckDB (1-based → 0-based)."""
    # По номеру
    if isinstance(col_spec, (int, float)):
        n = int(col_spec)
        if 1 <= n <= len(columns):
            return n - 1
        return len(columns) - 1

    # По имени
    if isinstance(col_spec, str):
        s = col_spec.strip().lower()

        if s == 'end':
            return len(columns) - 1
        if s.startswith('end-'):
            try:
                n = int(s[4:].strip())
                idx = len(columns) - n - 1
                return max(0, idx)
            except ValueError:
                pass
        if s.startswith('last'):
            rest = s[4:].strip()
            try:
                n = int(rest)
                if n == 1:
                    return len(columns) - 1
                return max(0, len(columns) - n)
            except ValueError:
                pass

        # По имени столбца
        cols_lower = [str(c).lower().strip() for c in columns]
        if s in cols_lower:
            return cols_lower.index(s)

    return 0


# ============================================================
# АНАЛИЗ СРЕЗА ВЕКТОРА
# ============================================================
def _analyze_vector_index_node(index_node, env):
    """Разбирает IndexNode для вектора (1D)."""
    if not hasattr(index_node, 'indices'):
        return None
    if len(index_node.indices) != 1:
        return None

    vector_obj = index_node.matrix.evaluate(env)
    if not hasattr(vector_obj, 'data') or vector_obj.is_2d:
        return None

    idx_node = index_node.indices[0]
    idx_spec = (idx_node.evaluate(env)
                if hasattr(idx_node, 'evaluate')
                else idx_node)

    start, end = parse_range_spec(
        idx_spec, len(vector_obj.data), is_column=False
    )
    return (vector_obj, start, end)


# ============================================================
# СРАВНЕНИЕ ЗНАЧЕНИЙ
# ============================================================
def _compare_scalar_scalar(op, a, b, inside=False, ignore=False):
    """
    Сравнивает два значения.

    Модификаторы:
        inside — только для строк и op == 'EQUALS':
                 проверяет, что b (подстрока) содержится в a.
        ignore — для строк: сравнение без учёта регистра.
    """
    # ============================================================
    # INSIDE: только для строк и op == 'EQUALS'
    # ============================================================
    if inside and op == 'EQUALS':
        if isinstance(a, str) and isinstance(b, str):
            ca = a.lower() if ignore else a
            cb = b.lower() if ignore else b
            return cb in ca
        return False

    # ============================================================
    # IGNORE: для строк, все операторы
    # ============================================================
    if ignore and isinstance(a, str) and isinstance(b, str):
        ca = a.lower()
        cb = b.lower()
        if op == 'EQUALS':        return ca == cb
        if op == 'NOTEQUAL':      return ca != cb
        if op == 'LESS':          return ca < cb
        if op == 'GREATER':       return ca > cb
        if op == 'LESSEQUAL':     return ca <= cb
        if op == 'GREATEREQUAL':  return ca >= cb
        return False

    # ============================================================
    # ОБЫЧНОЕ СРАВНЕНИЕ
    # ============================================================
    try:
        if op == 'EQUALS':        return a == b
        if op == 'NOTEQUAL':      return a != b
        if op == 'LESS':          return a < b
        if op == 'GREATER':       return a > b
        if op == 'LESSEQUAL':     return a <= b
        if op == 'GREATEREQUAL':  return a >= b
        if op == 'AND':           return a and b
        if op == 'OR':            return a or b
    except TypeError:
        return False
    return False


# ============================================================
# ВЫЧИСЛЕНИЕ УСЛОВИЯ (МАТРИЦА)
# ============================================================
def _evaluate_condition_matrix(condition, env, matrix_obj, row_start, row_end,
                                inside=False, ignore=False):
    """Условие для матрицы — список булевых значений."""
    from ast_nodes.index import IndexNode
    from ast_nodes.operations import BinaryOp, UnaryOp

    # --- IndexNode: s[:, "Пол"] ---
    if isinstance(condition, IndexNode):
        analysis = _analyze_index_node(condition, env)
        if analysis is None:
            return [None] * (row_end - row_start + 1)

        cond_matrix, c_start, c_end, col_idx, _ = analysis

        if (c_start, c_end) != (row_start, row_end):
            raise ValueError(
                f"Все условия должны быть в ОДНОМ диапазоне строк.\n"
                f"  Первое: строки {row_start}..{row_end}\n"
                f"  Это:    строки {c_start}..{c_end}"
            )

        values = []
        for i in range(row_start - 1, row_end):
            if i < len(cond_matrix.data):
                row = cond_matrix.data[i]
                values.append(row[col_idx] if col_idx < len(row) else None)
            else:
                values.append(None)
        return values

    # --- BinaryOp ---
    if isinstance(condition, BinaryOp):
        left = condition.left
        right = condition.right

        if condition.op == 'AND':
            left_res = _evaluate_condition_matrix(
                left, env, matrix_obj, row_start, row_end,
                inside=inside, ignore=ignore,
            )
            right_res = _evaluate_condition_matrix(
                right, env, matrix_obj, row_start, row_end,
                inside=inside, ignore=ignore,
            )
            return _logical_lists('AND', left_res, right_res)

        if condition.op == 'OR':
            left_res = _evaluate_condition_matrix(
                left, env, matrix_obj, row_start, row_end,
                inside=inside, ignore=ignore,
            )
            right_res = _evaluate_condition_matrix(
                right, env, matrix_obj, row_start, row_end,
                inside=inside, ignore=ignore,
            )
            return _logical_lists('OR', left_res, right_res)

        left_is_index = isinstance(left, IndexNode)
        right_is_index = isinstance(right, IndexNode)

        if left_is_index and right_is_index:
            lv = _evaluate_condition_matrix(
                left, env, matrix_obj, row_start, row_end,
                inside=inside, ignore=ignore,
            )
            rv = _evaluate_condition_matrix(
                right, env, matrix_obj, row_start, row_end,
                inside=inside, ignore=ignore,
            )
            return _compare_lists(condition.op, lv, rv,
                                   inside=inside, ignore=ignore)

        if left_is_index:
            lv = _evaluate_condition_matrix(
                left, env, matrix_obj, row_start, row_end,
                inside=inside, ignore=ignore,
            )
            rv = right.evaluate(env) if hasattr(right, 'evaluate') else right
            return [_compare_scalar_scalar(condition.op, v, rv,
                                            inside=inside, ignore=ignore)
                    for v in lv]

        if right_is_index:
            rv = _evaluate_condition_matrix(
                right, env, matrix_obj, row_start, row_end,
                inside=inside, ignore=ignore,
            )
            lv = left.evaluate(env) if hasattr(left, 'evaluate') else left
            return [_compare_scalar_scalar(condition.op, lv, v,
                                            inside=inside, ignore=ignore)
                    for v in rv]

        lv = left.evaluate(env) if hasattr(left, 'evaluate') else left
        rv = right.evaluate(env) if hasattr(right, 'evaluate') else right
        return _compare_scalar_scalar(condition.op, lv, rv,
                                       inside=inside, ignore=ignore)

    # --- UnaryOp ---
    if isinstance(condition, UnaryOp):
        right = _evaluate_condition_matrix(
            condition.right, env, matrix_obj, row_start, row_end,
            inside=inside, ignore=ignore,
        )
        if condition.op == 'NOT':
            if isinstance(right, list):
                return [not x for x in right]
            return not right
        return right

    val = condition.evaluate(env) if hasattr(condition, 'evaluate') else condition
    return val


# ============================================================
# ВЫЧИСЛЕНИЕ УСЛОВИЯ (ВЕКТОР)
# ============================================================
def _evaluate_condition_vector(condition, env, vector_obj, start, end,
                                inside=False, ignore=False):
    """Условие для вектора — список булевых значений."""
    from ast_nodes.index import IndexNode
    from ast_nodes.operations import BinaryOp, UnaryOp
    from ast_nodes.variables import VariableNode

    if isinstance(condition, IndexNode):
        analysis = _analyze_vector_index_node(condition, env)
        if analysis is None:
            return [None] * (end - start + 1)
        vec, c_start, c_end = analysis

        if (c_start, c_end) != (start, end):
            raise ValueError(
                f"Все условия должны быть в ОДНОМ диапазоне.\n"
                f"  Первое: {start}..{end}\n"
                f"  Это:    {c_start}..{c_end}"
            )
        return list(vec.data[start - 1:end])

    if isinstance(condition, BinaryOp):
        left = condition.left
        right = condition.right

        if condition.op == 'AND':
            l = _evaluate_condition_vector(
                left, env, vector_obj, start, end,
                inside=inside, ignore=ignore,
            )
            r = _evaluate_condition_vector(
                right, env, vector_obj, start, end,
                inside=inside, ignore=ignore,
            )
            return _logical_lists('AND', l, r)

        if condition.op == 'OR':
            l = _evaluate_condition_vector(
                left, env, vector_obj, start, end,
                inside=inside, ignore=ignore,
            )
            r = _evaluate_condition_vector(
                right, env, vector_obj, start, end,
                inside=inside, ignore=ignore,
            )
            return _logical_lists('OR', l, r)

        left_is_index = isinstance(left, IndexNode)
        right_is_index = isinstance(right, IndexNode)

        if left_is_index and right_is_index:
            lv = _evaluate_condition_vector(
                left, env, vector_obj, start, end,
                inside=inside, ignore=ignore,
            )
            rv = _evaluate_condition_vector(
                right, env, vector_obj, start, end,
                inside=inside, ignore=ignore,
            )
            return _compare_lists(condition.op, lv, rv,
                                   inside=inside, ignore=ignore)

        if left_is_index:
            lv = _evaluate_condition_vector(
                left, env, vector_obj, start, end,
                inside=inside, ignore=ignore,
            )
            rv = right.evaluate(env) if hasattr(right, 'evaluate') else right
            return [_compare_scalar_scalar(condition.op, v, rv,
                                            inside=inside, ignore=ignore)
                    for v in lv]

        if right_is_index:
            rv = _evaluate_condition_vector(
                right, env, vector_obj, start, end,
                inside=inside, ignore=ignore,
            )
            lv = left.evaluate(env) if hasattr(left, 'evaluate') else left
            return [_compare_scalar_scalar(condition.op, lv, v,
                                            inside=inside, ignore=ignore)
                    for v in rv]

        if isinstance(left, VariableNode):
            try:
                target = env.get(left.name)
            except NameError:
                target = None
            if target is not None and hasattr(target, 'data') and not target.is_2d:
                values = list(target.data[start - 1:end])
                rv = right.evaluate(env) if hasattr(right, 'evaluate') else right
                return [_compare_scalar_scalar(condition.op, v, rv,
                                                inside=inside, ignore=ignore)
                        for v in values]

        if isinstance(right, VariableNode):
            try:
                target = env.get(right.name)
            except NameError:
                target = None
            if target is not None and hasattr(target, 'data') and not target.is_2d:
                values = list(target.data[start - 1:end])
                lv = left.evaluate(env) if hasattr(left, 'evaluate') else left
                return [_compare_scalar_scalar(condition.op, lv, v,
                                                inside=inside, ignore=ignore)
                        for v in values]

        lv = left.evaluate(env) if hasattr(left, 'evaluate') else left
        rv = right.evaluate(env) if hasattr(right, 'evaluate') else right
        return _compare_scalar_scalar(condition.op, lv, rv,
                                       inside=inside, ignore=ignore)

    if isinstance(condition, UnaryOp):
        right = _evaluate_condition_vector(
            condition.right, env, vector_obj, start, end,
            inside=inside, ignore=ignore,
        )
        if condition.op == 'NOT':
            if isinstance(right, list):
                return [not x for x in right]
            return not right
        return right

    val = condition.evaluate(env) if hasattr(condition, 'evaluate') else condition
    return val


# ============================================================
# ОПЕРАЦИИ
# ============================================================
def _compare_lists(op, left, right, inside=False, ignore=False):
    result = []
    n = min(len(left), len(right))
    for i in range(n):
        result.append(_compare_scalar_scalar(op, left[i], right[i],
                                               inside=inside, ignore=ignore))
    return result


def _logical_lists(op, left, right):
    result = []
    n = min(len(left), len(right))
    for i in range(n):
        if op == 'AND':
            result.append(bool(left[i]) and bool(right[i]))
        elif op == 'OR':
            result.append(bool(left[i]) or bool(right[i]))
    return result


# ============================================================
# ИЗВЛЕЧЕНИЕ МАТРИЦЫ / ВЕКТОРА ИЗ УСЛОВИЯ
# ============================================================
def _extract_target(node, env):
    """Извлекает (matrix_obj_or_vector, row_start, row_end) из условия."""
    from ast_nodes.index import IndexNode
    from ast_nodes.operations import BinaryOp, UnaryOp
    from ast_nodes.variables import VariableNode

    if isinstance(node, IndexNode):
        if len(node.indices) == 2:
            analysis = _analyze_index_node(node, env)
            if analysis is None:
                return None
            matrix_obj, r_start, r_end, _, _ = analysis
            return (matrix_obj, r_start, r_end)

        if len(node.indices) == 1:
            analysis = _analyze_vector_index_node(node, env)
            if analysis is None:
                return None
            vec, v_start, v_end = analysis
            return (vec, v_start, v_end)

    if isinstance(node, BinaryOp):
        if node.op in ('AND', 'OR'):
            left = _extract_target(node.left, env)
            if left is not None:
                return left
            return _extract_target(node.right, env)

        left = _extract_target(node.left, env)
        if left is not None:
            return left
        right = _extract_target(node.right, env)
        if right is not None:
            return right

        if isinstance(node.left, VariableNode):
            try:
                target = env.get(node.left.name)
            except NameError:
                target = None
            if target is not None and hasattr(target, 'data') and not target.is_2d:
                return (target, 1, len(target.data))

        if isinstance(node.right, VariableNode):
            try:
                target = env.get(node.right.name)
            except NameError:
                target = None
            if target is not None and hasattr(target, 'data') and not target.is_2d:
                return (target, 1, len(target.data))

    if isinstance(node, UnaryOp):
        return _extract_target(node.right, env)

    return None


# ============================================================
# DUCKDB: ТРАНСЛЯЦИЯ УСЛОВИЯ В SQL
#
# ПРАВИЛО:
#   • Если правый операнд — ЧИСЛО (int/float, не bool) →
#     сравниваем как DOUBLE.
#   • Иначе → сравниваем как VARCHAR.
#
# Это нужно, потому что сравнение VARCHAR лексикографическое:
#   '85000' > '100000'  →  True   (символ '8' > '1')
#   но
#   85000 > 100000      →  False  (числа)
# ============================================================
def _translate_to_sql(condition, env, duck_table, inside=False, ignore=False):
    """
    Переводит условие ArrayVator в SQL WHERE.

    Автоматически выбирает тип сравнения:
        • число → CAST(col AS DOUBLE)
        • строка / bool / None → CAST(col AS VARCHAR)

    Модификаторы:
        inside — LIKE '%value%' (подстрока, только для строк)
        ignore — LOWER(...) с обеих сторон
    """
    from ast_nodes.index import IndexNode
    from ast_nodes.operations import BinaryOp, UnaryOp

    def _escape_ident(name):
        return '"' + str(name).replace('"', '""') + '"'

    def _escape_val_as_str(val):
        """Экранирует значение как VARCHAR."""
        if val is None:
            return "NULL"
        if isinstance(val, bool):
            s = "true" if val else "false"
            return "'" + s + "'"
        return "'" + str(val).replace("'", "''") + "'"

    def _escape_val_as_number(val):
        """Экранирует значение как число (DOUBLE)."""
        if val is None:
            return "NULL"
        if isinstance(val, bool):
            return "1" if val else "0"
        try:
            if isinstance(val, (int, float)):
                return str(val)
            return str(float(val))
        except (ValueError, TypeError):
            return "NULL"

    def _get_col_name(index_node):
        if len(index_node.indices) != 2:
            return None

        col_spec_node = index_node.indices[1]
        col_spec = (col_spec_node.evaluate(env)
                    if hasattr(col_spec_node, 'evaluate')
                    else col_spec_node)

        columns = duck_table.get_columns()
        idx = _resolve_column_for_duckdb(columns, col_spec)
        return columns[idx] if 0 <= idx < len(columns) else None

    def _col_as_varchar(index_node):
        col_name = _get_col_name(index_node)
        if not col_name:
            return "NULL"
        return f"CAST({_escape_ident(col_name)} AS VARCHAR)"

    def _col_as_number(index_node):
        col_name = _get_col_name(index_node)
        if not col_name:
            return "NULL"
        return f"CAST({_escape_ident(col_name)} AS DOUBLE)"

    def _is_number(val):
        return isinstance(val, (int, float)) and not isinstance(val, bool)

    # ============================================================
    # IndexNode
    # ============================================================
    if isinstance(condition, IndexNode):
        return _col_as_varchar(condition)

    # ============================================================
    # BinaryOp
    # ============================================================
    if isinstance(condition, BinaryOp):
        op = condition.op
        left = condition.left
        right = condition.right

        if op == 'AND':
            l_sql = _translate_to_sql(left, env, duck_table,
                                       inside=inside, ignore=ignore)
            r_sql = _translate_to_sql(right, env, duck_table,
                                       inside=inside, ignore=ignore)
            return f"({l_sql} AND {r_sql})"

        if op == 'OR':
            l_sql = _translate_to_sql(left, env, duck_table,
                                       inside=inside, ignore=ignore)
            r_sql = _translate_to_sql(right, env, duck_table,
                                       inside=inside, ignore=ignore)
            return f"({l_sql} OR {r_sql})"

        if inside and op == 'EQUALS':
            if isinstance(left, IndexNode):
                l_sql = _col_as_varchar(left)
            else:
                l_val = left.evaluate(env) if hasattr(left, 'evaluate') else left
                l_sql = _escape_val_as_str(l_val)

            if isinstance(right, IndexNode):
                r_sql = _col_as_varchar(right)
            else:
                r_val = right.evaluate(env) if hasattr(right, 'evaluate') else right
                r_sql = _escape_val_as_str(r_val)

            if ignore:
                return f"LOWER({l_sql}) LIKE LOWER('%' || {r_sql} || '%')"
            return f"{l_sql} LIKE '%' || {r_sql} || '%'"

        sql_ops = {
            'EQUALS': '=',
            'NOTEQUAL': '<>',
            'LESS': '<',
            'GREATER': '>',
            'LESSEQUAL': '<=',
            'GREATEREQUAL': '>=',
        }
        sql_op = sql_ops.get(op)

        if not sql_op:
            return "TRUE"

        left_is_col = isinstance(left, IndexNode)
        right_is_col = isinstance(right, IndexNode)

        left_val = None
        right_val = None

        if not left_is_col:
            left_val = left.evaluate(env) if hasattr(left, 'evaluate') else left
        if not right_is_col:
            right_val = right.evaluate(env) if hasattr(right, 'evaluate') else right

        use_numeric = False

        if left_is_col and not right_is_col:
            use_numeric = _is_number(right_val)
        elif right_is_col and not left_is_col:
            use_numeric = _is_number(left_val)
        elif left_is_col and right_is_col:
            use_numeric = False
        else:
            use_numeric = _is_number(right_val)

        if use_numeric:
            if left_is_col:
                l_sql = _col_as_number(left)
            else:
                l_sql = _escape_val_as_number(left_val)

            if right_is_col:
                r_sql = _col_as_number(right)
            else:
                r_sql = _escape_val_as_number(right_val)
        else:
            if left_is_col:
                l_sql = _col_as_varchar(left)
            else:
                l_sql = _escape_val_as_str(left_val)

            if right_is_col:
                r_sql = _col_as_varchar(right)
            else:
                r_sql = _escape_val_as_str(right_val)

        if ignore and not use_numeric:
            return f"LOWER({l_sql}) {sql_op} LOWER({r_sql})"

        return f"{l_sql} {sql_op} {r_sql}"

    # ============================================================
    # UnaryOp
    # ============================================================
    if isinstance(condition, UnaryOp):
        if condition.op == 'NOT':
            inner = _translate_to_sql(condition.right, env, duck_table,
                                       inside=inside, ignore=ignore)
            return f"NOT ({inner})"
        return _translate_to_sql(condition.right, env, duck_table,
                                  inside=inside, ignore=ignore)

    # ============================================================
    # Скаляр
    # ============================================================
    val = condition.evaluate(env) if hasattr(condition, 'evaluate') else condition
    return _escape_val_as_str(val)


def _filter_duckdb(condition, env, duck_table, inside=False, ignore=False):
    """
    Фильтрует DuckDBTable через SQL.
    Возвращает новый DuckDBTable (view).
    """
    from duckdb_engine import DuckDBTable
    import uuid

    where_sql = _translate_to_sql(condition, env, duck_table,
                                   inside=inside, ignore=ignore)

    new_name = f"filtered_{uuid.uuid4().hex[:8]}"
    sql = f"""
        CREATE OR REPLACE VIEW {new_name} AS
        SELECT * FROM {duck_table.table_name}
        WHERE {where_sql}
    """

    try:
        duck_table.con.execute(sql)
    except Exception as e:
        error_msg = str(e)

        if "Conversion Error" in error_msg and "Could not convert" in error_msg:
            raise ValueError(
                f"filterif: несовпадение типов.\n"
                f"  SQL: {where_sql}\n"
                f"  Ошибка: {error_msg}"
            )
        else:
            raise RuntimeError(f"Ошибка фильтрации: {error_msg}")

    new_table = DuckDBTable.__new__(DuckDBTable)
    new_table.path = duck_table.path
    new_table.table_name = new_name
    new_table.con = duck_table.con
    new_table.utf8_path = duck_table.utf8_path
    new_table.is_temp = False
    new_table._tmp_path = None

    return new_table


# ============================================================
# FILTERIF NODE
# ============================================================
class FilterIfNode(Node):
    def __init__(self, matrix=None, condition=None, cells_range=None,
                 inside=False, ignore=False):
        self.matrix = matrix
        self.condition = condition
        self.cells_range = cells_range
        self.inside = inside
        self.ignore = ignore

    def evaluate(self, env):
        if self.condition is None:
            raise ValueError("FilterIf: условие не указано")

        # ============================================================
        # НОВОЕ: проверяем, нет ли функции в условии
        # ============================================================
        func_info = _find_function_node_in_condition(self.condition, env)
        if func_info is not None:
            func_name, inner_slice = func_info
            raise ArrayVatorError(
                code="FILTERIF_FUNCTION_IN_CONDITION",
                context=None,
                message=(
                    f"filterif: в условии используется функция "
                    f"{func_name}() — так нельзя.\n"
                    f"\n"
                    f"  filterif работает только с ГОТОВЫМ столбцом.\n"
                    f"  Он не умеет фильтровать по результату функции."
                ),
                suggestion=(
                    f"РЕШЕНИЕ: сначала добавьте столбец через addcolumn,\n"
                    f"потом фильтруйте по нему.\n"
                    f"\n"
                    f"  ❌  filterif({func_name}(m[:, \"X\"]) == ...)\n"
                    f"\n"
                    f"  ✅  m2 = addcolumn(m, \"НовыйСтолбец\", "
                    f"{func_name}(m[:, \"X\"]))\n"
                    f"      r = filterif(m2[:, \"НовыйСтолбец\"] == ...)\n"
                    f"\n"
                    f"ПОЧЕМУ ТАК:\n"
                    f"  • filterif строит маску \"построчно\" по срезу.\n"
                    f"  • Результат функции — это ВЕКТОР, его нельзя\n"
                    f"    сравнивать со скаляром построчно.\n"
                    f"  • addcolumn материализует вектор в столбец,\n"
                    f"    и filterif работает с ним как обычно.\n"
                    f"\n"
                    f"ПРИМЕР С МАТРИЦЕЙ:\n"
                    f"\n"
                    f"  m = [\"Имя\", \"Дата\", \"Отдел\";\n"
                    f"       \"Аня\", \"20.06.2025\", \"IT\";\n"
                    f"       \"Боб\", \"15.07.2024\", \"HR\";\n"
                    f"       \"Света\", \"10.08.2025\", \"IT\"]\n"
                    f"\n"
                    f"  # ШАГ 1: добавить столбец с годом\n"
                    f"  m2 = addcolumn(m, \"Год\", year(m[:, \"Дата\"]))\n"
                    f"\n"
                    f"  # ШАГ 2: оставить только строки за 2025 год\n"
                    f"  r = filterif(m2[:, \"Год\"] == 2025)\n"
                    f"\n"
                    f"  print(r)\n"
                    f"\n"
                    f"  ВЫВОД:\n"
                    f"    Имя   Дата          Отдел  Год\n"
                    f"    Аня   20.06.2025    IT     2025\n"
                    f"    Света 10.08.2025    IT     2025\n"
                ),
            )

        # ============================================================
        # Дальше — как было
        # ============================================================
        target_info = _extract_target(self.condition, env)
        if target_info is None:
            raise ValueError(
                "FilterIf: не удалось определить матрицу или вектор "
                "из условия.\n"
                "  Примеры:\n"
                "    filterif(s[:, \"Пол\"] == \"Ж\")\n"
                "    filterif(v > 20)"
            )

        target_obj, row_start, row_end = target_info

        # ============================================================
        # DUCKDB
        # ============================================================
        if _is_duckdb(target_obj):
            return _filter_duckdb(self.condition, env, target_obj,
                                   inside=self.inside, ignore=self.ignore)

        # ============================================================
        # МАТРИЦА (2D) — RAM
        # ============================================================
        if hasattr(target_obj, 'is_2d') and target_obj.is_2d:
            result = _evaluate_condition_matrix(
                self.condition, env, target_obj, row_start, row_end,
                inside=self.inside, ignore=self.ignore,
            )

            if not isinstance(result, list):
                if result:
                    result = [True] * (row_end - row_start + 1)
                else:
                    result = [False] * (row_end - row_start + 1)

            protected_before = target_obj.data[:row_start - 1]
            working = target_obj.data[row_start - 1:row_end]
            protected_after = target_obj.data[row_end:]

            filtered_working = []
            for i, row in enumerate(working):
                if i < len(result) and result[i]:
                    filtered_working.append(row)

            result_data = (
                list(protected_before)
                + filtered_working
                + list(protected_after)
            )
            result_matrix = MatrExMatrix(result_data, True)
            self._log_operation(result_matrix, target_obj)
            return result_matrix

        # ============================================================
        # ВЕКТОР (1D)
        # ============================================================
        if hasattr(target_obj, 'data') and not target_obj.is_2d:
            result = _evaluate_condition_vector(
                self.condition, env, target_obj, row_start, row_end,
                inside=self.inside, ignore=self.ignore,
            )

            if not isinstance(result, list):
                if result:
                    result = [True] * (row_end - row_start + 1)
                else:
                    result = [False] * (row_end - row_start + 1)

            protected_before = target_obj.data[:row_start - 1]
            working = target_obj.data[row_start - 1:row_end]
            protected_after = target_obj.data[row_end:]

            filtered_working = []
            for i, val in enumerate(working):
                if i < len(result) and result[i]:
                    filtered_working.append(val)

            result_data = (
                list(protected_before)
                + filtered_working
                + list(protected_after)
            )
            return MatrExMatrix(result_data, False)

        raise ValueError(
            f"FilterIf: не поддерживаемый тип {type(target_obj)}"
        )

    def _log_operation(self, result_matrix, source_matrix):
        try:
            from runtime.logger import logger
            if not logger.enabled:
                return
            logger.log_operation(
                "filterif",
                repr(self),
                before=source_matrix,
                after=result_matrix,
            )
        except Exception:
            pass

    def __repr__(self):
        if self.cells_range is not None:
            return f"FilterIf({self.condition}, cells={self.cells_range})"
        return f"FilterIf({self.condition})"