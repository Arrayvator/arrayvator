# ast_nodes/functions/case.py
"""
Функция CASE: CaseNode
Условное преобразование значений.

СИНТАКСИС:
    case(m[:, "X"], when < 18 then "Дитя", else "Взрослый")

ФОРМАТЫ WHEN:
    when < 18 then "X"
    when > 50 then "X"
    when <= 30 then "X"
    when >= 18 then "X"
    when == "IT" then "X"
    when != "X" then "Y"

ФОРМАТЫ THEN / ELSE:
    then "строка"
    then 5
    then m[:, "X"]      — значение из другого столбца для ТЕКУЩЕЙ строки
    else "строка"
    else m[:, "X"]

DUCKDB:
    - Если данные в DuckDBTable → SQL CASE WHEN через * REPLACE
    - Возвращает новый DuckDBTable (view)
    - Столбец остаётся на своём месте

Matrix:
    - ВСЕГДА возвращает ВЕКТОР (согласовано с fillna, isnone, replacetext).
    - Вектор имеет ту же длину, что исходный срез.
    - Если пользователь хочет заменить столбец в матрице — он пишет:
          m[:, "X"] = case(m[:, "X"], ...)
"""

from ..base import Node
from runtime.matrix import MatrExMatrix
from ..utils.index_utils import parse_range_spec, resolve_column_index


# ============================================================
# ХЕЛПЕР: определение DuckDBTable
# ============================================================
def _is_duckdb(val):
    try:
        from duckdb_engine import DuckDBTable
        return isinstance(val, DuckDBTable)
    except ImportError:
        return False


# ============================================================
# ИЗВЛЕЧЕНИЕ DUCKDBTABLE И СТОЛБЦА
# ============================================================
def _extract_duckdb_column(index_node, env):
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

    is_full = (
        isinstance(row_spec, str)
        and row_spec.strip().lower() in (':', 'all')
    )
    if not is_full:
        raise ValueError(
            "case: DuckDB не поддерживает диапазоны строк.\n"
            f"  Указано: {row_spec}\n"
            "  ✅ Используйте: case(m[:, \"X\"], when ... then ..., else ...)"
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
# ОПРЕДЕЛЕНИЕ ТИПА СТОЛБЦА
# ============================================================
def _is_numeric_type(col_type):
    if not col_type:
        return False
    col_type_upper = str(col_type).upper()
    numeric_types = (
        'INTEGER', 'BIGINT', 'SMALLINT', 'TINYINT',
        'DOUBLE', 'FLOAT', 'REAL', 'DECIMAL', 'NUMERIC',
        'HUGEINT', 'UBIGINT', 'UINTEGER',
    )
    for nt in numeric_types:
        if nt in col_type_upper:
            return True
    return False


def _get_column_type(duck_table, col_name):
    try:
        safe_col = '"' + str(col_name).replace('"', '""') + '"'
        result = duck_table.con.execute(
            f'SELECT typeof({safe_col}) FROM {duck_table.table_name} LIMIT 1'
        ).fetchone()
        return result[0] if result else 'VARCHAR'
    except Exception:
        return 'VARCHAR'


# ============================================================
# DUCKDB: CASE WHEN
# ============================================================
def _translate_when_to_sql(condition, env, duck_table, col_name,
                            is_numeric=False):
    from ast_nodes.operations import BinaryOp
    from ast_nodes.variables import VariableNode

    safe_col = '"' + str(col_name).replace('"', '""') + '"'

    def _escape_val_as_varchar(val):
        if val is None:
            return "NULL"
        if isinstance(val, bool):
            s = "true" if val else "false"
            return "'" + s + "'"
        return "'" + str(val).replace("'", "''") + "'"

    def _escape_val_as_number(val):
        if val is None:
            return "NULL"
        if isinstance(val, bool):
            return "1" if val else "0"
        try:
            if isinstance(val, (int, float)):
                return str(val)
            return str(float(val))
        except (ValueError, TypeError):
            return _escape_val_as_varchar(val)

    if isinstance(condition, BinaryOp):
        op = condition.op
        left = condition.left
        right = condition.right

        sql_ops = {
            'EQUALS': '=',
            'NOTEQUAL': '<>',
            'LESS': '<',
            'GREATER': '>',
            'LESSEQUAL': '<=',
            'GREATEREQUAL': '>=',
            'AND': 'AND',
            'OR': 'OR',
        }
        sql_op = sql_ops.get(op)

        if not sql_op:
            return "TRUE"

        if op in ('AND', 'OR'):
            l_sql = _translate_when_to_sql(
                left, env, duck_table, col_name, is_numeric
            )
            r_sql = _translate_when_to_sql(
                right, env, duck_table, col_name, is_numeric
            )
            return f"({l_sql} {sql_op} {r_sql})"

        if is_numeric:
            if isinstance(left, VariableNode) and left.name == '_value':
                l_sql = f'CAST({safe_col} AS DOUBLE)'
            else:
                l_val = left.evaluate(env) if hasattr(left, 'evaluate') else left
                l_sql = _escape_val_as_number(l_val)

            if isinstance(right, VariableNode) and right.name == '_value':
                r_sql = f'CAST({safe_col} AS DOUBLE)'
            else:
                r_val = right.evaluate(env) if hasattr(right, 'evaluate') else right
                r_sql = _escape_val_as_number(r_val)
        else:
            if isinstance(left, VariableNode) and left.name == '_value':
                l_sql = f'CAST({safe_col} AS VARCHAR)'
            else:
                l_val = left.evaluate(env) if hasattr(left, 'evaluate') else left
                l_sql = _escape_val_as_varchar(l_val)

            if isinstance(right, VariableNode) and right.name == '_value':
                r_sql = f'CAST({safe_col} AS VARCHAR)'
            else:
                r_val = right.evaluate(env) if hasattr(right, 'evaluate') else right
                r_sql = _escape_val_as_varchar(r_val)

        return f"{l_sql} {sql_op} {r_sql}"

    val = condition.evaluate(env) if hasattr(condition, 'evaluate') else condition
    if is_numeric:
        return _escape_val_as_number(val)
    return _escape_val_as_varchar(val)


def _case_duckdb(duck_table, col_name, whens, else_value, env):
    from duckdb_engine import DuckDBTable
    import uuid

    safe_col = '"' + str(col_name).replace('"', '""') + '"'

    def _escape_val(val):
        if val is None:
            return "NULL"
        if isinstance(val, bool):
            return "TRUE" if val else "FALSE"
        if isinstance(val, (int, float)):
            return str(val)
        return "'" + str(val).replace("'", "''") + "'"

    col_type = _get_column_type(duck_table, col_name)
    is_numeric = _is_numeric_type(col_type)

    when_parts = []
    for cond, result in whens:
        cond_sql = _translate_when_to_sql(
            cond, env, duck_table, col_name, is_numeric
        )
        res_val = result.evaluate(env) if hasattr(result, 'evaluate') else result
        res_sql = _escape_val(res_val)
        when_parts.append(f"WHEN {cond_sql} THEN {res_sql}")

    if else_value is not None:
        else_val = else_value.evaluate(env) if hasattr(else_value, 'evaluate') else else_value
        else_sql = _escape_val(else_val)
    else:
        else_sql = "NULL"

    when_sql = "\n                ".join(when_parts)

    new_name = f"case_{uuid.uuid4().hex[:8]}"
    sql = f"""
        CREATE OR REPLACE VIEW {new_name} AS
        SELECT * REPLACE (
            CASE
                {when_sql}
                ELSE {else_sql}
            END AS {safe_col}
        )
        FROM {duck_table.table_name}
    """

    try:
        duck_table.con.execute(sql)
    except Exception as e:
        raise RuntimeError(
            f"Ошибка case: {e}\n"
            f"  Тип столбца: {col_type} (numeric={is_numeric})\n"
            f"SQL: {sql}"
        )

    new_table = DuckDBTable.__new__(DuckDBTable)
    new_table.path = duck_table.path
    new_table.table_name = new_name
    new_table.con = duck_table.con
    new_table.utf8_path = duck_table.utf8_path
    new_table.is_temp = False
    new_table._tmp_path = None

    return new_table


# ============================================================
# АНАЛИЗ СРЕЗА МАТРИЦЫ (для RAM)
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

    col_idx, skip_header = resolve_column_index(matrix_obj, col_spec, env)

    if not is_explicit and skip_header:
        row_start = max(row_start, 2)

    return (matrix_obj, row_start, row_end, col_idx)


# ============================================================
# ВЫЧИСЛЕНИЕ (для Matrix)
# ============================================================
def _check_condition(condition, value, env):
    if condition is None:
        return False

    if isinstance(condition, (str, int, float, bool)):
        return condition == value

    if hasattr(condition, 'evaluate'):
        from environment import Environment
        temp_env = Environment(parent=env)
        temp_env.set("_value", value)
        try:
            result = condition.evaluate(temp_env)
            return bool(result)
        except Exception:
            return False

    return False


def _evaluate_result_expr(expr, env, matrix_obj=None, row_idx=None):
    """
    Вычисляет выражение-результат (then/else).
    Если expr — IndexNode со срезом одного столбца, И передан matrix_obj + row_idx —
    извлекает значение для конкретной строки.
    """
    from ast_nodes.index import IndexNode

    # ============================================================
    # Если expr — IndexNode (срез m[:, "X"])
    # ============================================================
    if isinstance(expr, IndexNode) and matrix_obj is not None and row_idx is not None:
        try:
            if len(expr.indices) == 2:
                matrix_of_expr = expr.matrix.evaluate(env)
                if matrix_of_expr is matrix_obj:
                    col_spec_node = expr.indices[1]
                    col_spec = (col_spec_node.evaluate(env)
                                if hasattr(col_spec_node, 'evaluate')
                                else col_spec_node)
                    col_idx, _ = resolve_column_index(matrix_obj, col_spec, env)

                    if row_idx < len(matrix_obj.data):
                        row = matrix_obj.data[row_idx]
                        if col_idx < len(row):
                            return row[col_idx]
                    return None
        except Exception:
            pass

    # ============================================================
    # Обычный скаляр
    # ============================================================
    if hasattr(expr, 'evaluate'):
        return expr.evaluate(env)
    return expr


def _process_values(values, whens, else_value, env,
                     matrix_obj=None, row_start=1):
    results = []
    for i, val in enumerate(values):
        if matrix_obj is not None:
            row_idx = row_start - 1 + i
        else:
            row_idx = None

        matched = False
        for condition, result_expr in whens:
            if _check_condition(condition, val, env):
                res = _evaluate_result_expr(result_expr, env,
                                              matrix_obj, row_idx)
                results.append(res)
                matched = True
                break

        if not matched:
            if else_value is not None:
                res = _evaluate_result_expr(else_value, env,
                                              matrix_obj, row_idx)
                results.append(res)
            else:
                results.append(None)

    return results


# ============================================================
# CASE NODE
# ============================================================
class CaseNode(Node):
    def __init__(self, data, column=None, whens=None, else_value=None):
        self.data = data
        self.column = column
        self.whens = whens if whens else []
        self.else_value = else_value

    def evaluate(self, env):
        # DUCKDB
        duck_table, col_name = _extract_duckdb_column(self.data, env)
        if duck_table is not None:
            return _case_duckdb(
                duck_table, col_name,
                self.whens, self.else_value, env
            )

        # MATRIX СРЕЗ m[:, "X"] → ВЕКТОР
        analysis = _analyze_matrix_index(self.data, env)
        if analysis is not None:
            matrix_obj, row_start, row_end, col_idx = analysis

            values = []
            for i in range(row_start - 1, row_end):
                if i < len(matrix_obj.data):
                    row = matrix_obj.data[i]
                    if col_idx < len(row):
                        values.append(row[col_idx])
                    else:
                        values.append(None)
                else:
                    values.append(None)

            results = _process_values(
                values, self.whens, self.else_value, env,
                matrix_obj=matrix_obj, row_start=row_start,
            )

            if row_start == row_end:
                return results[0] if results else None

            # ============================================================
            # Возвращаем ВЕКТОР (согласовано с fillna, isnone, replacetext)
            # ============================================================
            return MatrExMatrix(results, False)

        # ВЕКТОР
        data_obj = self.data.evaluate(env)

        if hasattr(data_obj, 'data') and not data_obj.is_2d:
            results = _process_values(
                data_obj.data, self.whens, self.else_value, env
            )
            return MatrExMatrix(results, False)

        if isinstance(data_obj, list) and not (data_obj and isinstance(data_obj[0], list)):
            results = _process_values(
                data_obj, self.whens, self.else_value, env
            )
            return MatrExMatrix(results, False)

        # СКАЛЯР
        if isinstance(data_obj, (int, float, str, bool)) or data_obj is None:
            results = _process_values([data_obj], self.whens, self.else_value, env)
            return results[0] if results else None

        raise TypeError(
            f"case() работает с матрицами и векторами, "
            f"получен {type(data_obj)}"
        )

    def __repr__(self):
        return f"case({self.data}, whens={self.whens}, else={self.else_value})"