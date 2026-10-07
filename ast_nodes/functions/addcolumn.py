# ast_nodes/functions/addcolumn.py
"""
Функция ADDCOLUMN — добавляет новый столбец в таблицу.

СИНТАКСИС:
    m2 = addcolumn(m, "Сумма", m[:, "ID"] + m[:, "ID_10"])
    m2 = addcolumn(m, "Год", 2024)
    m2 = addcolumn(m, "Статус", "новый")
    m2 = addcolumn(m, "Доля_%", percentof(m[:, "Продажи"]))

ПРАВИЛА:
    - Всегда возвращает НОВУЮ таблицу.
    - Работает с Matrix (в RAM) и DuckDB (через SQL).
    - Имя столбца — строка в кавычках.
    - Значение — скаляр, вектор (построчно) или выражение.

ВАЖНО:
    Вектор из функции (например, year(m[:, "Дата"]) или
    hour(m[:, "Время"])) НЕ содержит заголовка — только данные.
    Поэтому при заполнении строки i берём vec_data[i - 1].
"""

from ..base import Node
from runtime.matrix import MatrExMatrix


def _is_duckdb(val):
    try:
        from duckdb_engine import DuckDBTable
        return isinstance(val, DuckDBTable)
    except ImportError:
        return False


class AddColumnNode(Node):
    def __init__(self, data, name, expr):
        self.data = data
        self.name = name
        self.expr = expr

    def evaluate(self, env):
        # 1. Определяем данные
        data_obj = self.data.evaluate(env) if hasattr(self.data, 'evaluate') else self.data

        # 2. Имя нового столбца
        name_val = (self.name.evaluate(env)
                    if hasattr(self.name, 'evaluate')
                    else self.name)
        if not isinstance(name_val, str):
            raise TypeError(
                f"addcolumn: имя столбца должно быть строкой, "
                f"получено {type(name_val).__name__}"
            )

        # 3. DuckDB → SQL
        if _is_duckdb(data_obj):
            return self._addcolumn_duckdb(data_obj, name_val, env)

        # 4. Matrix → RAM
        if hasattr(data_obj, 'data') and data_obj.is_2d:
            return self._addcolumn_matrix(data_obj, name_val, env)

        raise TypeError(
            "addcolumn: ожидается матрица или DuckDB.\n"
            "  Пример: m2 = addcolumn(m, \"Сумма\", m[:, \"ID\"] + m[:, \"ID_10\"])"
        )

    # ============================================================
    # MATRIX
    # ============================================================
    def _addcolumn_matrix(self, matrix_obj, name_val, env):
        result_data = [list(row) for row in matrix_obj.data]

        if matrix_obj.rows > 0:
            header = result_data[0]
            header.append(name_val)

        # ============================================================
        # ПРОБУЕМ ВЫЧИСЛИТЬ ВЫРАЖЕНИЕ ЦЕЛИКОМ
        # ============================================================
        # Возможные типы результата:
        #   • Скаляр (число, строка, bool, None) — заполнить все ячейки
        #   • Вектор (is_2d=False) — построчно
        #     ⚠️ Вектор из функций (year, hour, month, ...) приходит БЕЗ заголовка,
        #        то есть vec_data[0] — данные первой строки.
        #   • 2D-матрица (is_2d=True) — берём ПЕРВУЮ КОЛОНКУ,
        #     первую строку (заголовок) пропускаем
        # ============================================================
        vec_data = None       # список значений для строк данных
        scalar_value = None   # скаляр — заполнить все ячейки
        is_scalar = False

        try:
            full_val = (self.expr.evaluate(env)
                        if hasattr(self.expr, 'evaluate')
                        else self.expr)

            # Скаляр
            if isinstance(full_val, (int, float, str, bool)) or full_val is None:
                is_scalar = True
                scalar_value = full_val

            # Вектор (1D)
            elif hasattr(full_val, 'data') and not full_val.is_2d:
                vec_data = list(full_val.data)

            # Матрица (2D) — берём ПЕРВУЮ КОЛОНКУ
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

        # ============================================================
        # ЗАПОЛНЯЕМ
        # ============================================================
        # ВАЖНО: для строки i (1-based, начиная с 1) берём vec_data[i - 1].
        # Потому что vec_data[0] — это значение для строки 1 (первой строки данных).
        # ============================================================
        for i in range(1, matrix_obj.rows):
            if is_scalar:
                value = scalar_value
            elif vec_data is not None:
                idx = i - 1
                if 0 <= idx < len(vec_data):
                    value = vec_data[idx]
                else:
                    value = None
            else:
                value = self._eval_expr(self.expr, matrix_obj, i, env)

            while len(result_data[i]) < len(result_data[0]):
                result_data[i].append(None)
            result_data[i][-1] = value

        return MatrExMatrix(result_data, True)

    def _eval_expr(self, expr, matrix_obj, row_idx, env):
        from ast_nodes.index import IndexNode
        from ast_nodes.operations import BinaryOp, UnaryOp

        # ============================================================
        # IndexNode: m[:, "X"] → значение для текущей строки
        # ============================================================
        if isinstance(expr, IndexNode):
            return self._get_cell(expr, matrix_obj, row_idx, env)

        # ============================================================
        # BinaryOp: поэлементно (left op right)
        # ============================================================
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

        # ============================================================
        # UnaryOp: -x, not x
        # ============================================================
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

        # ============================================================
        # ФУНКЦИИ-ОБЁРТКИ: round, int, frac, frac_digits
        # ============================================================
        # Идея: у этих функций ОДИН основной аргумент (плюс опциональные
        # параметры-скаляры, например digits у round). Мы вычисляем
        # основной аргумент построчно, а потом применяем функцию.
        # ============================================================
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
                    # Автоопределение по строковому виду (как в FracNode)
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

        # ============================================================
        # Fallback: скаляр, вычисляем как есть
        # ============================================================
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

    # ============================================================
    # DUCKDB
    # ============================================================
    def _addcolumn_duckdb(self, duck_table, name_val, env):
        from duckdb_engine import DuckDBTable
        import uuid

        columns = duck_table.get_columns()

        expr_sql = self._translate_to_sql(self.expr, env, duck_table, columns)

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

        new_table = DuckDBTable.__new__(DuckDBTable)
        new_table.path = duck_table.path
        new_table.table_name = new_name
        new_table.con = duck_table.con
        new_table.utf8_path = duck_table.utf8_path
        new_table.is_temp = False
        new_table._tmp_path = None

        return new_table

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

        # ============================================================
        # ФУНКЦИИ-ОБЁРТКИ: round, int, frac, frac_digits
        # ============================================================
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
            return f"CAST(SUBSTR(CAST(({inner}) - CAST(({inner}) AS BIGINT) AS VARCHAR), 3) AS BIGINT)"

        val = expr.evaluate(env) if hasattr(expr, 'evaluate') else expr
        return _escape_val(val)

    def __repr__(self):
        return f"addcolumn({self.data}, {self.name}, {self.expr})"