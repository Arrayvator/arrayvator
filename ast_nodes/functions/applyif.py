# ast_nodes/functions/applyif.py
"""
Функция APPLYIF — условное присваивание в срез.

СИНТАКСИС:
    applyif(условие, m[:, "X"] = значение)
    applyif(условие, m[:, end+1] = значение)

ПРАВИЛА:
    - Возвращает НОВУЮ матрицу.
    - Где условие ЛОЖНО — не трогать (оставить как было).
    - Работает на Matrix (RAM) и DuckDB (SQL CASE WHEN).
    - Значение может быть скаляром ИЛИ выражением от столбцов.
    - Float-результаты округляются до 4 знаков.
"""

from ..base import Node
from runtime.matrix import MatrExMatrix
from ..utils.index_utils import parse_range_spec, resolve_column_index


def _is_duckdb(val):
    try:
        from duckdb_engine import DuckDBTable
        return isinstance(val, DuckDBTable)
    except ImportError:
        return False


class ApplyIfNode(Node):
    def __init__(self, condition, target, value):
        self.condition = condition
        self.target = target
        self.value = value

    def evaluate(self, env):
        from ast_nodes.index import IndexNode

        if not isinstance(self.target, IndexNode):
            raise TypeError(
                "applyif: цель должна быть срезом m[:, \"X\"] или m[:, end+1]"
            )

        matrix_obj = self.target.matrix.evaluate(env)

        if _is_duckdb(matrix_obj):
            return self._applyif_duckdb(matrix_obj, env)

        if hasattr(matrix_obj, 'data') and matrix_obj.is_2d:
            return self._applyif_matrix(matrix_obj, env)

        raise TypeError(
            "applyif: ожидается матрица или DuckDB.\n"
            "  Пример: applyif(m[:, \"Отдел\"] == \"IT\", m[:, \"Статус\"] = \"VIP\")"
        )

    # ============================================================
    # MATRIX
    # ============================================================
    def _applyif_matrix(self, matrix_obj, env):
        if len(self.target.indices) != 2:
            raise TypeError("applyif: цель должна быть m[:, \"X\"]")

        row_spec_node = self.target.indices[0]
        col_spec_node = self.target.indices[1]

        row_spec = (row_spec_node.evaluate(env)
                    if hasattr(row_spec_node, 'evaluate')
                    else row_spec_node)
        col_spec = (col_spec_node.evaluate(env)
                    if hasattr(col_spec_node, 'evaluate')
                    else col_spec_node)

        is_row_all = (
            isinstance(row_spec, str)
            and row_spec.strip().lower() in (':', 'all')
        )
        if not is_row_all:
            raise ValueError(
                "applyif: по строкам должен быть полный срез (m[:, ...])."
            )

        col_is_new = False
        col_idx = None
        col_name = None

        if isinstance(col_spec, str):
            s = col_spec.strip().lower()
            if s == 'end+1' or (s.startswith('end+') and s != 'end+1'):
                col_is_new = True
                col_idx = matrix_obj.cols
            elif s == 'end':
                col_idx = matrix_obj.cols - 1
            else:
                try:
                    col_idx, _ = resolve_column_index(matrix_obj, col_spec, env)
                except Exception:
                    col_is_new = True
                    col_name = col_spec
                    col_idx = matrix_obj.cols
        elif isinstance(col_spec, (int, float)):
            n = int(col_spec)
            if n < 1 or n > matrix_obj.cols:
                raise ValueError(
                    f"applyif: столбец {n} за пределами (всего: {matrix_obj.cols})"
                )
            col_idx = n - 1
        else:
            col_is_new = True
            col_name = str(col_spec) if col_spec is not None else "new_col"
            col_idx = matrix_obj.cols

        result_data = [list(row) if isinstance(row, list) else [row]
                       for row in matrix_obj.data]

        if col_is_new:
            if matrix_obj.rows > 0:
                header_name = col_name if col_name else "new_col"
                while len(result_data[0]) <= col_idx:
                    result_data[0].append(None)
                result_data[0][col_idx] = header_name

        condition_values = self._evaluate_condition(
            self.condition, matrix_obj, env
        )

        # Применяем ПОСТРОЧНО, округляем float до 4 знаков
        for i in range(1, matrix_obj.rows):
            if i < len(condition_values) and condition_values[i]:
                row_value = self._eval_value_for_row(
                    self.value, matrix_obj, i, env
                )

                if isinstance(row_value, float):
                    row_value = round(row_value, 4)

                row = result_data[i]
                while len(row) <= col_idx:
                    row.append(None)
                row[col_idx] = row_value

        max_cols = max(len(r) for r in result_data) if result_data else 0
        for r in result_data:
            while len(r) < max_cols:
                r.append(None)

        return MatrExMatrix(result_data, True)

    def _eval_value_for_row(self, value_node, matrix_obj, row_idx, env):
        from ast_nodes.index import IndexNode
        from ast_nodes.operations import BinaryOp, UnaryOp

        if not hasattr(value_node, 'evaluate'):
            return value_node

        if isinstance(value_node, IndexNode):
            return self._get_cell_from_slice(value_node, matrix_obj, row_idx, env)

        if isinstance(value_node, BinaryOp):
            left = self._eval_value_for_row(value_node.left, matrix_obj, row_idx, env)
            right = self._eval_value_for_row(value_node.right, matrix_obj, row_idx, env)

            op = value_node.op
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

        if isinstance(value_node, UnaryOp):
            right = self._eval_value_for_row(
                value_node.right, matrix_obj, row_idx, env
            )
            if value_node.op == 'MINUS':
                try:
                    return -right
                except Exception:
                    return None
            if value_node.op == 'NOT':
                return not right
            return right

        try:
            return value_node.evaluate(env)
        except Exception:
            return None

    def _get_cell_from_slice(self, index_node, matrix_obj, row_idx, env):
        if len(index_node.indices) != 2:
            try:
                return index_node.evaluate(env)
            except Exception:
                return None

        col_spec_node = index_node.indices[1]
        col_spec = (col_spec_node.evaluate(env)
                    if hasattr(col_spec_node, 'evaluate')
                    else col_spec_node)

        try:
            col_idx, _ = resolve_column_index(matrix_obj, col_spec, env)
        except Exception:
            return None

        if row_idx < len(matrix_obj.data):
            row = matrix_obj.data[row_idx]
            if col_idx < len(row):
                return row[col_idx]
        return None

    def _evaluate_condition(self, condition, matrix_obj, env):
        from ast_nodes.index import IndexNode
        from ast_nodes.operations import BinaryOp, UnaryOp

        results = [False] * matrix_obj.rows

        if isinstance(condition, IndexNode):
            for i in range(1, matrix_obj.rows):
                results[i] = True
            return results

        if isinstance(condition, BinaryOp):
            op = condition.op
            left = condition.left
            right = condition.right

            if op == 'AND':
                l = self._evaluate_condition(left, matrix_obj, env)
                r = self._evaluate_condition(right, matrix_obj, env)
                return [a and b for a, b in zip(l, r)]

            if op == 'OR':
                l = self._evaluate_condition(left, matrix_obj, env)
                r = self._evaluate_condition(right, matrix_obj, env)
                return [a or b for a, b in zip(l, r)]

            left_values = self._extract_values(left, matrix_obj, env)
            right_values = self._extract_values(right, matrix_obj, env)

            from .filterif import _compare_scalar_scalar

            result = []
            for i in range(matrix_obj.rows):
                lv = left_values[i] if left_values else None
                rv = right_values[i] if right_values else None
                result.append(_compare_scalar_scalar(op, lv, rv))
            return result

        if isinstance(condition, UnaryOp):
            r = self._evaluate_condition(condition.right, matrix_obj, env)
            if condition.op == 'NOT':
                return [not x for x in r]
            return r

        return results

    def _extract_values(self, node, matrix_obj, env):
        from ast_nodes.index import IndexNode

        if isinstance(node, IndexNode):
            col_spec_node = node.indices[1]
            col_spec = (col_spec_node.evaluate(env)
                        if hasattr(col_spec_node, 'evaluate')
                        else col_spec_node)
            col_idx, _ = resolve_column_index(matrix_obj, col_spec, env)

            values = []
            for i in range(matrix_obj.rows):
                if i < len(matrix_obj.data):
                    row = matrix_obj.data[i]
                    values.append(row[col_idx] if col_idx < len(row) else None)
                else:
                    values.append(None)
            return values

        val = node.evaluate(env) if hasattr(node, 'evaluate') else node
        return [val] * matrix_obj.rows

    # ============================================================
    # DUCKDB
    # ============================================================
    def _applyif_duckdb(self, duck_table, env):
        from duckdb_engine import DuckDBTable
        from .filterif import _translate_to_sql
        import uuid

        col_spec_node = self.target.indices[1]
        col_spec = (col_spec_node.evaluate(env)
                    if hasattr(col_spec_node, 'evaluate')
                    else col_spec_node)

        columns = duck_table.get_columns()

        is_new_col = False
        col_name_for_target = "new_col"

        if isinstance(col_spec, str):
            s = col_spec.strip()
            s_lower = s.lower()

            if s_lower.startswith('end+'):
                is_new_col = True
                col_name_for_target = "new_col"
            elif s_lower in (':', 'all'):
                is_new_col = True
                col_name_for_target = "new_col"
            else:
                cols_lower = [str(c).lower().strip() for c in columns]
                if s_lower in cols_lower:
                    idx = cols_lower.index(s_lower)
                    col_name_for_target = columns[idx]
                else:
                    is_new_col = True
                    col_name_for_target = s

        elif isinstance(col_spec, (int, float)):
            n = int(col_spec)
            if 1 <= n <= len(columns):
                col_name_for_target = columns[n - 1]
            else:
                is_new_col = True
                col_name_for_target = f"col_{n}"
        else:
            is_new_col = True
            col_name_for_target = str(col_spec) if col_spec else "new_col"

        cond_sql = _translate_to_sql(self.condition, env, duck_table)
        val_sql = self._translate_value_to_sql(self.value, duck_table, env)

        safe_target = '"' + str(col_name_for_target).replace('"', '""') + '"'
        new_name = f"applyif_{uuid.uuid4().hex[:8]}"

        if is_new_col:
            sql = f"""
                CREATE OR REPLACE VIEW {new_name} AS
                SELECT *,
                       CASE WHEN {cond_sql} THEN {val_sql} ELSE NULL END
                       AS {safe_target}
                FROM {duck_table.table_name}
            """
        else:
            sql = f"""
                CREATE OR REPLACE VIEW {new_name} AS
                SELECT * REPLACE (
                    CASE WHEN {cond_sql} THEN {val_sql}
                         ELSE CAST({safe_target} AS VARCHAR) END
                    AS {safe_target}
                )
                FROM {duck_table.table_name}
            """

        try:
            duck_table.con.execute(sql)
        except Exception as e:
            raise RuntimeError(f"Ошибка applyif: {e}\nSQL: {sql}")

        new_table = DuckDBTable.__new__(DuckDBTable)
        new_table.path = duck_table.path
        new_table.table_name = new_name
        new_table.con = duck_table.con
        new_table.utf8_path = duck_table.utf8_path
        new_table.is_temp = False
        new_table._tmp_path = None

        return new_table

    def _translate_value_to_sql(self, value_node, duck_table, env):
        from ast_nodes.index import IndexNode
        from ast_nodes.operations import BinaryOp, UnaryOp

        if isinstance(value_node, IndexNode):
            col_spec_node = value_node.indices[1]
            col_spec = (col_spec_node.evaluate(env)
                        if hasattr(col_spec_node, 'evaluate')
                        else col_spec_node)

            columns = duck_table.get_columns()
            s = str(col_spec).strip().lower()
            cols_lower = [str(c).lower().strip() for c in columns]

            if s in cols_lower:
                idx = cols_lower.index(s)
                col_name = columns[idx]
                return '"' + str(col_name).replace('"', '""') + '"'

            return "NULL"

        if isinstance(value_node, BinaryOp):
            l = self._translate_value_to_sql(value_node.left, duck_table, env)
            r = self._translate_value_to_sql(value_node.right, duck_table, env)

            op_map = {
                'PLUS': '+', 'MINUS': '-', 'STAR': '*', 'SLASH': '/',
                'MOD': '%', 'POW': '**', 'FLOORDIV': '//',
                'EQUALS': '=', 'NOTEQUAL': '<>',
                'LESS': '<', 'GREATER': '>',
                'LESSEQUAL': '<=', 'GREATEREQUAL': '>=',
                'AND': 'AND', 'OR': 'OR',
            }
            op = op_map.get(value_node.op)
            if not op:
                return "NULL"
            return f"({l} {op} {r})"

        if isinstance(value_node, UnaryOp):
            inner = self._translate_value_to_sql(
                value_node.right, duck_table, env
            )
            if value_node.op == 'MINUS':
                return f"(-{inner})"
            if value_node.op == 'NOT':
                return f"(NOT {inner})"
            return inner

        val = (value_node.evaluate(env)
               if hasattr(value_node, 'evaluate')
               else value_node)

        if val is None:
            return "NULL"
        if isinstance(val, bool):
            return "TRUE" if val else "FALSE"
        if isinstance(val, (int, float)):
            return str(val)
        return "'" + str(val).replace("'", "''") + "'"

    def __repr__(self):
        return f"applyif({self.condition}, {self.target} = {self.value})"