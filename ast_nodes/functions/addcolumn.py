# ast_nodes/functions/addcolumn.py
from ..base import Node
from runtime.matrix import MatrExMatrix


def _is_duckdb(val):
    try:
        from duckdb_engine import DuckDBTable
        return isinstance(val, DuckDBTable)
    except ImportError:
        return False


class AddColumnNode(Node):
    """
    ADDCOLUMN — гибкое добавление столбцов.

    РЕЖИМЫ (определяются по типам аргументов args[1], args[2]):

        1. addcolumn(m, "Имя", expr)
           args[1] — str, args[2] — любое выражение (скаляр / вектор / срез)
           → ОДИН столбец с заголовком "Имя", заполненный expr.

        2. addcolumn(m, "Имя")
           args[1] — str, args[2] нет
           → ОДИН столбец с заголовком "Имя", значения None.

        3. addcolumn(m, N)
           args[1] — int, args[2] нет
           → N ПУСТЫХ столбцов (заголовки None, значения None).

        4. addcolumn(m, N, fill)
           args[1] — int, args[2] — скаляр
           → N столбцов, заполненных fill (заголовки None).

    Работает с Matrix и DuckDB.
    """

    def __init__(self, args):
        self.args = args

    def evaluate(self, env):
        if not self.args:
            raise TypeError("addcolumn: нет аргументов.")

        # ============================================================
        # 1. Матрица
        # ============================================================
        data_obj = (self.args[0].evaluate(env)
                    if hasattr(self.args[0], 'evaluate')
                    else self.args[0])

        # ============================================================
        # 2. Второй аргумент: имя (str) или количество (int)
        # ============================================================
        arg1_val = (self.args[1].evaluate(env)
                    if hasattr(self.args[1], 'evaluate')
                    else self.args[1])

        # ============================================================
        # 3. Режим 4: addcolumn(m, N, fill)
        #    args[1] — int, args[2] — скаляр
        # ============================================================
        if len(self.args) == 3 and isinstance(arg1_val, (int, float)) \
                and not isinstance(arg1_val, bool):
            n = int(arg1_val)
            if n < 0:
                raise ValueError(f"addcolumn: N не может быть отрицательным: {n}")

            fill_val = (self.args[2].evaluate(env)
                        if hasattr(self.args[2], 'evaluate')
                        else self.args[2])

            if not self._is_scalar_value(fill_val):
                raise TypeError(
                    "addcolumn: при добавлении N столбцов значение должно "
                    "быть скаляром.\n"
                    f"  Получено: {type(fill_val).__name__}\n"
                    "  Пример: addcolumn(m, 2, 0)"
                )

            return self._add_n_columns(
                data_obj, n, fill_val,
                name_arg=None, env=env
            )

        # ============================================================
        # 4. Режим 3: addcolumn(m, N) — N ПУСТЫХ столбцов
        # ============================================================
        if len(self.args) == 2 and isinstance(arg1_val, (int, float)) \
                and not isinstance(arg1_val, bool):
            n = int(arg1_val)
            if n < 0:
                raise ValueError(f"addcolumn: N не может быть отрицательным: {n}")

            return self._add_n_columns(
                data_obj, n, None,
                name_arg=None, env=env
            )

        # ============================================================
        # 5. Режим 2: addcolumn(m, "Имя") — один столбец, значения None
        # ============================================================
        if len(self.args) == 2 and isinstance(arg1_val, str):
            return self._add_one_named_column(
                data_obj, arg1_val, None, env
            )

        # ============================================================
        # 6. Режим 1: addcolumn(m, "Имя", expr) — один столбец
        # ============================================================
        if len(self.args) == 3 and isinstance(arg1_val, str):
            return self._add_one_named_column(
                data_obj, arg1_val, self.args[2], env
            )

        # ============================================================
        # 7. Ошибка: непонятная комбинация
        # ============================================================
        raise TypeError(
            "addcolumn: неверные аргументы.\n"
            f"  args[1] = {type(arg1_val).__name__} ({arg1_val!r})\n"
            f"  args[2] = {'—' if len(self.args) < 3 else 'есть'}\n"
            "\n"
            "Допустимо:\n"
            "  addcolumn(m, \"Имя\", expr)\n"
            "  addcolumn(m, \"Имя\")\n"
            "  addcolumn(m, N)\n"
            "  addcolumn(m, N, fill)"
        )

    # ============================================================
    # УТИЛИТЫ
    # ============================================================
    def _is_scalar_value(self, v):
        return isinstance(v, (int, float, str, bool)) or v is None

    # ============================================================
    # РЕЖИМ: N столбцов (пустых или с fill)
    # ============================================================
    def _add_n_columns(self, data_obj, n, fill_val, name_arg, env):
        if n == 0:
            return data_obj

        # ---------------- DuckDB ----------------
        if _is_duckdb(data_obj):
            return self._add_n_columns_duckdb(data_obj, n, fill_val)

        # ---------------- Matrix ----------------
        if hasattr(data_obj, 'data') and data_obj.is_2d:
            return self._add_n_columns_matrix(data_obj, n, fill_val)

        raise TypeError(
            "addcolumn: ожидается матрица или DuckDB.\n"
            "  Пример: m2 = addcolumn(m, 2)"
        )

    def _add_n_columns_matrix(self, matrix_obj, n, fill_val):
        result_data = [
            list(row) if isinstance(row, list) else [row]
            for row in matrix_obj.data
        ]

        if matrix_obj.rows > 0:
            for _ in range(n):
                result_data[0].append(None)   # заголовки None

        for i in range(1, len(result_data)):
            for _ in range(n):
                result_data[i].append(fill_val)

        return MatrExMatrix(result_data, True)

    def _add_n_columns_duckdb(self, duck_table, n, fill_val):
        from duckdb_engine import DuckDBTable
        import uuid

        def _escape_val(val):
            if val is None:
                return "NULL"
            if isinstance(val, bool):
                return "TRUE" if val else "FALSE"
            if isinstance(val, (int, float)):
                return str(val)
            return "'" + str(val).replace("'", "''") + "'"

        columns = duck_table.get_columns()
        val_sql = _escape_val(fill_val)

        # Генерируем имена: __new_1, __new_2, ...
        new_cols_sql = []
        for k in range(1, n + 1):
            new_cols_sql.append(f'{val_sql} AS "__new_{k}"')

        new_name = f"addcol_{uuid.uuid4().hex[:8]}"
        sql = f"""
            CREATE OR REPLACE VIEW {new_name} AS
            SELECT *, {', '.join(new_cols_sql)}
            FROM {duck_table.table_name}
        """

        try:
            duck_table.con.execute(sql)
        except Exception as e:
            raise RuntimeError(
                f"Ошибка addcolumn (N столбцов): {e}\n"
                f"  SQL: {sql}"
            )

        return self._make_new_table(duck_table, new_name)

    # ============================================================
    # РЕЖИМ: один столбец с именем
    # ============================================================
    def _add_one_named_column(self, data_obj, name_val, expr_node, env):
        # ---------------- DuckDB ----------------
        if _is_duckdb(data_obj):
            return self._add_one_named_duckdb(data_obj, name_val, expr_node, env)

        # ---------------- Matrix ----------------
        if hasattr(data_obj, 'data') and data_obj.is_2d:
            return self._add_one_named_matrix(data_obj, name_val, expr_node, env)

        raise TypeError(
            "addcolumn: ожидается матрица или DuckDB.\n"
            "  Пример: m2 = addcolumn(m, \"Сумма\", m[:, \"A\"] + m[:, \"B\"])"
        )

    def _add_one_named_matrix(self, matrix_obj, name_val, expr_node, env):
        result_data = [
            list(row) if isinstance(row, list) else [row]
            for row in matrix_obj.data
        ]

        if matrix_obj.rows > 0:
            result_data[0].append(name_val)

        # ------------------------------------------------
        # expr_node is None → столбец из None
        # ------------------------------------------------
        if expr_node is None:
            for i in range(1, len(result_data)):
                result_data[i].append(None)
            return MatrExMatrix(result_data, True)

        # ------------------------------------------------
        # expr_node задан → вычисляем
        # ------------------------------------------------
        vec_data = None
        scalar_value = None
        is_scalar = False

        try:
            full_val = (expr_node.evaluate(env)
                        if hasattr(expr_node, 'evaluate')
                        else expr_node)

            if self._is_scalar_value(full_val):
                is_scalar = True
                scalar_value = full_val
            elif hasattr(full_val, 'data') and not full_val.is_2d:
                vec_data = list(full_val.data)
            elif hasattr(full_val, 'data') and full_val.is_2d:
                col0 = []
                for row in full_val.data:
                    if isinstance(row, list) and len(row) > 0:
                        col0.append(row[0])
                    elif isinstance(row, list):
                        col0.append(None)
                    else:
                        col0.append(row)
                vec_data = col0
        except Exception:
            vec_data = None
            is_scalar = False

        for i in range(1, len(result_data)):
            if is_scalar:
                value = scalar_value
            elif vec_data is not None:
                idx = i - 1
                if 0 <= idx < len(vec_data):
                    value = vec_data[idx]
                else:
                    value = None
            else:
                value = self._eval_expr(expr_node, matrix_obj, i, env)

            result_data[i].append(value)

        return MatrExMatrix(result_data, True)

    def _add_one_named_duckdb(self, duck_table, name_val, expr_node, env):
        from duckdb_engine import DuckDBTable
        import uuid

        columns = duck_table.get_columns()

        if expr_node is None:
            expr_sql = "NULL"
        else:
            expr_sql = self._translate_to_sql(expr_node, env, duck_table, columns)

        safe_name = '"' + str(name_val).replace('"', '""') + '"'

        new_name = f"addcol_{uuid.uuid4().hex[:8]}"
        sql = f"""
            CREATE OR REPLACE VIEW {new_name} AS
            SELECT *, ({expr_sql}) AS {safe_name}
            FROM {duck_table.table_name}
        """

        try:
            duck_table.con.execute(sql)
        except Exception as e:
            raise RuntimeError(
                f"Ошибка addcolumn: {e}\n"
                f"  SQL: {sql}"
            )

        return self._make_new_table(duck_table, new_name)

    # ============================================================
    # ОБЩИЙ ХЕЛПЕР: новый DuckDBTable
    # ============================================================
    def _make_new_table(self, duck_table, new_name):
        from duckdb_engine import DuckDBTable
        new_table = DuckDBTable.__new__(DuckDBTable)
        new_table.path = duck_table.path
        new_table.table_name = new_name
        new_table.con = duck_table.con
        new_table.utf8_path = duck_table.utf8_path
        new_table.is_temp = False
        new_table._tmp_path = None
        return new_table

    # ============================================================
    # СТАРЫЕ ХЕЛПЕРЫ (переносим без изменений)
    # ============================================================
    def _eval_expr(self, expr, matrix_obj, row_idx, env):
        from ast_nodes.index import IndexNode
        from ast_nodes.operations import BinaryOp, UnaryOp

        if isinstance(expr, IndexNode):
            return self._get_cell(expr, matrix_obj, row_idx, env)

        if isinstance(expr, BinaryOp):
            left = self._eval_expr(expr.left, matrix_obj, row_idx, env)
            right = self._eval_expr(expr.right, matrix_obj, row_idx, env)

            op = expr.op
            try:
                if op == 'PLUS':
                    if isinstance(left, str) or isinstance(right, str):
                        return str(left) + str(right)
                    return left + right
                if op == 'MINUS':
                    return left - right
                if op == 'STAR':
                    return left * right
                if op == 'SLASH':
                    return left / right if right != 0 else None
                if op == 'MOD':
                    return left % right if right != 0 else None
                if op == 'POW':
                    return left ** right
                if op == 'FLOORDIV':
                    return left // right if right != 0 else None
                if op == 'EQUALS':
                    return left == right
                if op == 'NOTEQUAL':
                    return left != right
                if op == 'LESS':
                    return left < right
                if op == 'GREATER':
                    return left > right
                if op == 'LESSEQUAL':
                    return left <= right
                if op == 'GREATEREQUAL':
                    return left >= right
                if op == 'AND':
                    return left and right
                if op == 'OR':
                    return left or right
            except Exception:
                return None

        if isinstance(expr, UnaryOp):
            right = self._eval_expr(expr.right, matrix_obj, row_idx, env)
            if expr.op == 'MINUS':
                try:
                    return -right
                except Exception:
                    return None
            if expr.op == 'NOT':
                return not right
            return right

        from ast_nodes.functions.math import (
            RoundNode, IntNode, FracNode, FracDigitsNode,
        )

        if isinstance(expr, RoundNode):
            inner = self._eval_expr(expr.arg, matrix_obj, row_idx, env)
            digits = None
            if expr.digits is not None:
                digits = self._eval_expr(expr.digits, matrix_obj, row_idx, env)
            if isinstance(inner, (int, float)) and not isinstance(inner, bool):
                try:
                    if digits is not None:
                        return round(inner, int(digits))
                    return round(inner)
                except Exception:
                    return None
            return inner

        if isinstance(expr, IntNode):
            inner = self._eval_expr(expr.arg, matrix_obj, row_idx, env)
            if isinstance(inner, (int, float)) and not isinstance(inner, bool):
                import math
                try:
                    return math.trunc(inner)
                except Exception:
                    return None
            return inner

        if isinstance(expr, FracNode):
            inner = self._eval_expr(expr.arg, matrix_obj, row_idx, env)
            digits = None
            if expr.digits is not None:
                digits = self._eval_expr(expr.digits, matrix_obj, row_idx, env)
            if isinstance(inner, (int, float)) and not isinstance(inner, bool):
                import math
                try:
                    frac = inner - math.trunc(inner)
                    if digits is not None:
                        return round(frac, int(digits))
                    str_val = str(inner)
                    if '.' in str_val and 'e' not in str_val.lower():
                        auto = len(str_val.split('.')[1])
                        if auto > 0:
                            return round(frac, auto)
                    return frac
                except Exception:
                    return None
            return inner

        if isinstance(expr, FracDigitsNode):
            inner = self._eval_expr(expr.arg, matrix_obj, row_idx, env)
            if isinstance(inner, (int, float)) and not isinstance(inner, bool):
                str_val = str(inner)
                if '.' in str_val:
                    frac_part = str_val.split('.')[1].lstrip('0')
                    if frac_part == '':
                        return 0
                    try:
                        return int(frac_part)
                    except Exception:
                        return 0
                return 0
            return inner

        return expr.evaluate(env) if hasattr(expr, 'evaluate') else expr

    def _get_cell(self, index_node, matrix_obj, row_idx, env):
        from ..utils.index_utils import resolve_column_index

        if len(index_node.indices) != 2:
            raise TypeError(
                "addcolumn: в выражении нужен срез m[:, \"X\"]"
            )

        col_spec_node = index_node.indices[1]
        col_spec = (col_spec_node.evaluate(env)
                    if hasattr(col_spec_node, 'evaluate')
                    else col_spec_node)

        col_idx, _ = resolve_column_index(matrix_obj, col_spec, env)

        if row_idx < len(matrix_obj.data):
            row = matrix_obj.data[row_idx]
            if col_idx < len(row):
                return row[col_idx]
        return None

    def _translate_to_sql(self, expr, env, duck_table, columns):
        from ast_nodes.index import IndexNode
        from ast_nodes.operations import BinaryOp, UnaryOp
        from .filterif import _resolve_column_for_duckdb

        def _esc(name):
            return '"' + str(name).replace('"', '""') + '"'

        def _get_col_name(index_node):
            if len(index_node.indices) != 2:
                return None
            col_spec_node = index_node.indices[1]
            col_spec = (col_spec_node.evaluate(env)
                        if hasattr(col_spec_node, 'evaluate')
                        else col_spec_node)
            idx = _resolve_column_for_duckdb(columns, col_spec)
            return columns[idx] if 0 <= idx < len(columns) else None

        def _escape_val(val):
            if val is None:
                return "NULL"
            if isinstance(val, bool):
                return "TRUE" if val else "FALSE"
            if isinstance(val, (int, float)):
                return str(val)
            return "'" + str(val).replace("'", "''") + "'"

        if isinstance(expr, IndexNode):
            col_name = _get_col_name(expr)
            if not col_name:
                return "NULL"
            return _esc(col_name)

        if isinstance(expr, BinaryOp):
            l = self._translate_to_sql(expr.left, env, duck_table, columns)
            r = self._translate_to_sql(expr.right, env, duck_table, columns)

            op_map = {
                'PLUS': '+', 'MINUS': '-', 'STAR': '*', 'SLASH': '/',
                'MOD': '%', 'POW': '**', 'FLOORDIV': '//',
                'EQUALS': '=', 'NOTEQUAL': '<>',
                'LESS': '<', 'GREATER': '>',
                'LESSEQUAL': '<=', 'GREATEREQUAL': '>=',
                'AND': 'AND', 'OR': 'OR',
            }
            sql_op = op_map.get(expr.op, '+')
            return f"({l} {sql_op} {r})"

        if isinstance(expr, UnaryOp):
            inner = self._translate_to_sql(expr.right, env, duck_table, columns)
            if expr.op == 'MINUS':
                return f"(-{inner})"
            if expr.op == 'NOT':
                return f"(NOT {inner})"
            return inner

        from ast_nodes.functions.math import (
            RoundNode, IntNode, FracNode, FracDigitsNode,
        )

        if isinstance(expr, RoundNode):
            inner = self._translate_to_sql(expr.arg, env, duck_table, columns)
            digits = 0
            if expr.digits is not None:
                d_val = (expr.digits.evaluate(env)
                         if hasattr(expr.digits, 'evaluate')
                         else expr.digits)
                try:
                    digits = int(d_val)
                except (ValueError, TypeError):
                    digits = 0
            return f"ROUND({inner}, {digits})"

        if isinstance(expr, IntNode):
            inner = self._translate_to_sql(expr.arg, env, duck_table, columns)
            return f"CAST({inner} AS BIGINT)"

        if isinstance(expr, FracNode):
            inner = self._translate_to_sql(expr.arg, env, duck_table, columns)
            digits = 4
            if expr.digits is not None:
                d_val = (expr.digits.evaluate(env)
                         if hasattr(expr.digits, 'evaluate')
                         else expr.digits)
                try:
                    digits = int(d_val)
                except (ValueError, TypeError):
                    digits = 4
            return f"ROUND(({inner}) - CAST(({inner}) AS BIGINT), {digits})"

        if isinstance(expr, FracDigitsNode):
            inner = self._translate_to_sql(expr.arg, env, duck_table, columns)
            return (
                f"CAST(SUBSTR(CAST(({inner}) - CAST(({inner}) AS BIGINT) "
                f"AS VARCHAR), 3) AS BIGINT)"
            )

        val = expr.evaluate(env) if hasattr(expr, 'evaluate') else expr
        return _escape_val(val)

    def __repr__(self):
        return f"addcolumn({len(self.args)} args)"