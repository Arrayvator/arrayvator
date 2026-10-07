# ast_nodes/functions/deleteif.py
"""
Функция DeleteIf - удаление строк по условию.

ПРАВИЛА:
    - Header СОХРАНЯЕТСЯ.
    - Возвращает НОВУЮ матрицу.
    - НЕ мутирует исходную:
          m = deleteif(m[:, "X"] == "Y")

НОВОЕ:
    - Если в условии используется ФУНКЦИЯ (year, month, round, len, ...),
      deleteif выдаёт ПОНЯТНУЮ ошибку с решением через addcolumn.
"""

from ..base import Node
from runtime.matrix import MatrExMatrix
from errors import ArrayVatorError


def _is_duckdb(val):
    """Проверяет, является ли значение DuckDBTable."""
    try:
        from duckdb_engine import DuckDBTable
        return isinstance(val, DuckDBTable)
    except ImportError:
        return False


# ============================================================
# ДЕТЕКТОР: функция внутри условия (общий с filterif)
# ============================================================
def _find_function_node_in_condition(condition, env):
    """
    Ищет в условии узел-функцию (year, month, round, len, ...).
    Возвращает (function_name, inner_slice) или None.
    """
    from ast_nodes.index import IndexNode
    from ast_nodes.operations import BinaryOp, UnaryOp
    from ast_nodes.variables import VariableNode
    from ast_nodes.base import Node

    def _get_func_name(node):
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
# ИЗВЛЕЧЕНИЕ ЦЕЛИ
# ============================================================
def _extract_target_deleteif(node, env):
    """Извлекает (target, start, end) из условия."""
    from ast_nodes.index import IndexNode
    from ast_nodes.operations import BinaryOp, UnaryOp
    from ast_nodes.variables import VariableNode
    from ..utils.index_utils import parse_range_spec, resolve_column_index

    if isinstance(node, IndexNode):
        if len(node.indices) == 2:
            try:
                matrix_obj = node.matrix.evaluate(env)
            except Exception:
                return None

            if _is_duckdb(matrix_obj):
                return (matrix_obj, 1, matrix_obj.get_row_count())

            row_spec_node = node.indices[0]
            row_spec = (row_spec_node.evaluate(env)
                        if hasattr(row_spec_node, 'evaluate')
                        else row_spec_node)

            r_start, r_end = parse_range_spec(
                row_spec, matrix_obj.rows, is_column=False
            )

            is_explicit_range = False
            if isinstance(row_spec, str):
                if row_spec.strip().lower() not in (':', 'all'):
                    is_explicit_range = True
            elif isinstance(row_spec, (int, float)):
                is_explicit_range = True

            col_spec_node = node.indices[1]
            col_spec = (col_spec_node.evaluate(env)
                        if hasattr(col_spec_node, 'evaluate')
                        else col_spec_node)

            try:
                _, skip_header = resolve_column_index(matrix_obj, col_spec, env)
            except Exception:
                skip_header = False

            if not is_explicit_range and skip_header:
                r_start = max(r_start, 2)

            return (matrix_obj, r_start, r_end)

        if len(node.indices) == 1:
            try:
                vector_obj = node.matrix.evaluate(env)
            except Exception:
                return None

            if not hasattr(vector_obj, 'data') or vector_obj.is_2d:
                return None

            idx_node = node.indices[0]
            idx_spec = (idx_node.evaluate(env)
                        if hasattr(idx_node, 'evaluate')
                        else idx_node)
            v_start, v_end = parse_range_spec(
                idx_spec, len(vector_obj.data), is_column=False
            )
            return (vector_obj, v_start, v_end)

    if isinstance(node, BinaryOp):
        if node.op in ('AND', 'OR'):
            left = _extract_target_deleteif(node.left, env)
            if left is not None:
                return left
            return _extract_target_deleteif(node.right, env)

        left = _extract_target_deleteif(node.left, env)
        if left is not None:
            return left
        right = _extract_target_deleteif(node.right, env)
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
        return _extract_target_deleteif(node.right, env)

    return None


# ============================================================
# DELETEIF NODE
# ============================================================
class DeleteIfNode(Node):
    def __init__(self, matrix=None, condition=None, cells_range=None):
        self.matrix = matrix
        self.condition = condition
        self.cells_range = cells_range

    def evaluate(self, env):
        if self.condition is None:
            raise ValueError("DeleteIf: условие не указано")

        # ============================================================
        # НОВОЕ: проверяем, нет ли функции в условии
        # ============================================================
        func_info = _find_function_node_in_condition(self.condition, env)
        if func_info is not None:
            func_name, inner_slice = func_info
            raise ArrayVatorError(
                code="DELETEIF_FUNCTION_IN_CONDITION",
                context=None,
                message=(
                    f"deleteif: в условии используется функция "
                    f"{func_name}() — так нельзя.\n"
                    f"\n"
                    f"  deleteif работает только с ГОТОВЫМ столбцом.\n"
                    f"  Он не умеет фильтровать по результату функции."
                ),
                suggestion=(
                    f"РЕШЕНИЕ: сначала добавьте столбец через addcolumn,\n"
                    f"потом удаляйте по нему.\n"
                    f"\n"
                    f"  ❌  deleteif({func_name}(m[:, \"X\"]) == ...)\n"
                    f"\n"
                    f"  ✅  m2 = addcolumn(m, \"НовыйСтолбец\", "
                    f"{func_name}(m[:, \"X\"]))\n"
                    f"      r = deleteif(m2[:, \"НовыйСтолбец\"] == ...)\n"
                    f"\n"
                    f"ПОЧЕМУ ТАК:\n"
                    f"  • deleteif строит маску \"построчно\" по срезу.\n"
                    f"  • Результат функции — это ВЕКТОР, его нельзя\n"
                    f"    сравнивать со скаляром построчно.\n"
                    f"  • addcolumn материализует вектор в столбец,\n"
                    f"    и deleteif работает с ним как обычно.\n"
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
                    f"  # ШАГ 2: удалить строки за 2025 год\n"
                    f"  r = deleteif(m2[:, \"Год\"] == 2025)\n"
                    f"\n"
                    f"  print(r)\n"
                    f"\n"
                    f"  ВЫВОД:\n"
                    f"    Имя   Дата          Отдел  Год\n"
                    f"    Боб   15.07.2024    HR     2024\n"
                ),
            )

        # ============================================================
        # Дальше — как было
        # ============================================================
        target_info = _extract_target_deleteif(self.condition, env)
        if target_info is None:
            raise ValueError(
                "DeleteIf: не удалось определить матрицу или вектор "
                "из условия."
            )

        target_obj, row_start, row_end = target_info

        # DUCKDB
        if _is_duckdb(target_obj):
            return self._delete_duckdb(target_obj, env)

        # МАТРИЦА
        if hasattr(target_obj, 'is_2d') and target_obj.is_2d:
            from .filterif import _evaluate_condition_matrix

            result = _evaluate_condition_matrix(
                self.condition, env, target_obj, row_start, row_end
            )

            if not isinstance(result, list):
                result = [True if result else False] * (row_end - row_start + 1)

            protected_before = target_obj.data[:row_start - 1]
            working = target_obj.data[row_start - 1:row_end]
            protected_after = target_obj.data[row_end:]

            remaining = [row for i, row in enumerate(working)
                         if i < len(result) and not result[i]]

            return MatrExMatrix(
                list(protected_before) + remaining + list(protected_after),
                True
            )

        # ВЕКТОР
        if hasattr(target_obj, 'data') and not target_obj.is_2d:
            from .filterif import _evaluate_condition_vector

            result = _evaluate_condition_vector(
                self.condition, env, target_obj, row_start, row_end
            )

            if not isinstance(result, list):
                result = [True if result else False] * (row_end - row_start + 1)

            protected_before = target_obj.data[:row_start - 1]
            working = target_obj.data[row_start - 1:row_end]
            protected_after = target_obj.data[row_end:]

            remaining = [val for i, val in enumerate(working)
                         if i < len(result) and not result[i]]

            return MatrExMatrix(
                list(protected_before) + remaining + list(protected_after),
                False
            )

        raise ValueError(f"DeleteIf: не поддерживаемый тип {type(target_obj)}")

    def _delete_duckdb(self, duck_table, env):
        from duckdb_engine import DuckDBTable
        from .filterif import _translate_to_sql
        import uuid

        where_sql = _translate_to_sql(self.condition, env, duck_table)

        new_name = f"deleted_{uuid.uuid4().hex[:8]}"
        sql = f"""
            CREATE OR REPLACE VIEW {new_name} AS
            SELECT * FROM {duck_table.table_name}
            WHERE NOT ({where_sql})
        """

        try:
            duck_table.con.execute(sql)
        except Exception as e:
            raise RuntimeError(f"Ошибка DeleteIf: {e}")

        new_table = DuckDBTable.__new__(DuckDBTable)
        new_table.path = duck_table.path
        new_table.table_name = new_name
        new_table.con = duck_table.con
        new_table.utf8_path = duck_table.utf8_path
        new_table.is_temp = False
        new_table._tmp_path = None

        return new_table

    def __repr__(self):
        return f"DeleteIf({self.condition})"