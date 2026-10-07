# ast_nodes/functions/insertif.py
"""
Функция INSERTIF — условная вставка пустых строк.

⚠️  РАБОТАЕТ ТОЛЬКО С MATRIX (RAM).
    НЕ работает с BigData (DuckDB).

СИНТАКСИС:
    insertif(условие, before)
    insertif(условие, after)

ПРАВИЛА:
    - Вставляется пустая строка (None для всех столбцов).
    - Обработка снизу вверх (от N к 1).
    - Заголовок не участвует в условии (для матрицы).
    - Поддерживается вектор.
"""

from ..base import Node
from runtime.matrix import MatrExMatrix
from ..utils.index_utils import resolve_column_index


def _is_duckdb(val):
    try:
        from duckdb_engine import DuckDBTable
        return isinstance(val, DuckDBTable)
    except ImportError:
        return False


# ============================================================
# ХЕЛПЕР: извлечение матрицы/вектора из условия
# ============================================================
def _extract_target_from_condition(condition, env):
    """
    Извлекает (target_obj, is_2d) из условия.

    Возвращает:
        (MatrExMatrix, True)   — если матрица
        (MatrExMatrix, False)  — если вектор
        (DuckDBTable, None)    — если BigData (DuckDB)
        (None, None)           — если не нашли
    """
    from ast_nodes.index import IndexNode
    from ast_nodes.operations import BinaryOp, UnaryOp
    from ast_nodes.variables import VariableNode

    def _wrap(obj):
        """Возвращает (obj, is_2d) с учётом BigData (DuckDB)."""
        if obj is None:
            return (None, None)
        if _is_duckdb(obj):
            return (obj, None)
        if hasattr(obj, 'data') and hasattr(obj, 'is_2d'):
            return (obj, obj.is_2d)
        return (None, None)

    if isinstance(condition, IndexNode):
        try:
            obj = condition.matrix.evaluate(env)
            return _wrap(obj)
        except Exception:
            return (None, None)

    if isinstance(condition, BinaryOp):
        if condition.op in ('AND', 'OR'):
            left, left_2d = _extract_target_from_condition(condition.left, env)
            if left is not None:
                return (left, left_2d)
            return _extract_target_from_condition(condition.right, env)

        left, left_2d = _extract_target_from_condition(condition.left, env)
        if left is not None:
            return (left, left_2d)
        right, right_2d = _extract_target_from_condition(condition.right, env)
        if right is not None:
            return (right, right_2d)

        if isinstance(condition.left, VariableNode):
            try:
                obj = env.get(condition.left.name)
                return _wrap(obj)
            except NameError:
                pass

        if isinstance(condition.right, VariableNode):
            try:
                obj = env.get(condition.right.name)
                return _wrap(obj)
            except NameError:
                pass

    if isinstance(condition, UnaryOp):
        return _extract_target_from_condition(condition.right, env)

    return (None, None)


# ============================================================
# ВЫЧИСЛЕНИЕ УСЛОВИЯ
# ============================================================
def _evaluate_condition(condition, target_obj, env, is_2d):
    """Возвращает список булевых значений для каждой строки/элемента."""
    from ast_nodes.index import IndexNode
    from ast_nodes.operations import BinaryOp, UnaryOp
    from .filterif import _compare_scalar_scalar

    n_rows = target_obj.rows if is_2d else len(target_obj.data)
    results = [False] * n_rows

    if isinstance(condition, IndexNode):
        for i in range(1, n_rows):
            results[i] = True
        return results

    if isinstance(condition, BinaryOp):
        op = condition.op
        left = condition.left
        right = condition.right

        if op == 'AND':
            l = _evaluate_condition(left, target_obj, env, is_2d)
            r = _evaluate_condition(right, target_obj, env, is_2d)
            return [a and b for a, b in zip(l, r)]

        if op == 'OR':
            l = _evaluate_condition(left, target_obj, env, is_2d)
            r = _evaluate_condition(right, target_obj, env, is_2d)
            return [a or b for a, b in zip(l, r)]

        left_values = _extract_values(left, target_obj, env, is_2d)
        right_values = _extract_values(right, target_obj, env, is_2d)

        result = []
        for i in range(n_rows):
            lv = left_values[i] if left_values else None
            rv = right_values[i] if right_values else None
            result.append(_compare_scalar_scalar(op, lv, rv))
        return result

    if isinstance(condition, UnaryOp):
        r = _evaluate_condition(condition.right, target_obj, env, is_2d)
        if condition.op == 'NOT':
            return [not x for x in r]
        return r

    return results


def _extract_values(node, target_obj, env, is_2d):
    """Извлекает значения для каждой строки/элемента."""
    from ast_nodes.index import IndexNode

    # Матрица — срез столбца
    if isinstance(node, IndexNode) and is_2d:
        col_spec_node = node.indices[1]
        col_spec = (col_spec_node.evaluate(env)
                    if hasattr(col_spec_node, 'evaluate')
                    else col_spec_node)
        try:
            col_idx, _ = resolve_column_index(target_obj, col_spec, env)
        except Exception:
            return None

        values = []
        for i in range(target_obj.rows):
            if i < len(target_obj.data):
                row = target_obj.data[i]
                values.append(row[col_idx] if col_idx < len(row) else None)
            else:
                values.append(None)
        return values

    # Вектор — IndexNode
    if isinstance(node, IndexNode) and not is_2d:
        return list(target_obj.data)

    # Общий случай
    val = node.evaluate(env) if hasattr(node, 'evaluate') else node

    if hasattr(val, 'data') and hasattr(val, 'is_2d') and not val.is_2d:
        return list(val.data)

    if hasattr(val, 'data') and hasattr(val, 'is_2d') and val.is_2d:
        return [row[0] if row else None for row in val.data]

    n_rows = target_obj.rows if is_2d else len(target_obj.data)
    return [val] * n_rows


# ============================================================
# INSERTIF NODE
# ============================================================
class InsertIfNode(Node):
    def __init__(self, condition, direction):
        self.condition = condition
        self.direction = direction    # 'before' | 'after'

    def evaluate(self, env):
        from errors import ArrayVatorError

        # 1. Извлекаем матрицу или вектор
        target_obj, is_2d = _extract_target_from_condition(self.condition, env)

        # ============================================================
        # ВАЖНО: сначала проверяем BigData (DuckDB), потом None
        # ============================================================
        if _is_duckdb(target_obj):
            raise ArrayVatorError(
                code="INSERTIF_DUCKDB",
                context=None,
                message=(
                    "insertif работает только с Matrix (RAM), "
                    "не с BigData (DuckDB).\n"
                    "  BigData — read-only view на файл."
                ),
                suggestion=(
                    "BigData (DuckDB) — read-only view на файл.\n"
                    "Он НЕ поддерживает вставку строк.\n"
                    "\n"
                    "Решение:\n"
                    "  1. Конвертировать BigData в Matrix:\n"
                    "        m = ToMatrix(bd)\n"
                    "        r = insertif(m[:, \"Отдел\"] == \"IT\", after)\n"
                    "\n"
                    "  2. Использовать SQL-аналог:\n"
                    "        filterif, addrows"
                ),
            )

        if target_obj is None:
            raise ArrayVatorError(
                code="INSERTIF_BAD_SYNTAX",
                context=None,
                message=(
                    "insertif: не удалось определить матрицу/вектор из условия.\n"
                    "  Пример: insertif(m[:, \"Отдел\"] == \"IT\", after)"
                ),
                suggestion=(
                    "Проверьте, что условие использует срез матрицы:\n"
                    "     ✅  insertif(m[:, \"Отдел\"] == \"IT\", after)\n"
                    "     ✅  insertif(m[:, \"Возраст\"] > 25, before)\n"
                    "     ✅  insertif(v > 20, after)         — вектор\n"
                    "     ❌  insertif(\"Отдел\" == \"IT\", after)  — нет среза"
                ),
            )

        # 2. Вычисляем условие
        condition_values = _evaluate_condition(
            self.condition, target_obj, env, is_2d
        )

        # 3. Определяем подходящие строки
        if is_2d:
            n_rows = target_obj.rows
            matching_rows = []
            for i in range(1, n_rows):
                if i < len(condition_values) and condition_values[i]:
                    matching_rows.append(i)
        else:
            n_rows = len(target_obj.data)
            matching_rows = []
            for i in range(0, n_rows):
                if i < len(condition_values) and condition_values[i]:
                    matching_rows.append(i)

        # 4. Нет совпадений — вернуть как есть
        if not matching_rows:
            if is_2d:
                return MatrExMatrix(
                    [list(row) if isinstance(row, list) else [row]
                     for row in target_obj.data],
                    True
                )
            else:
                return MatrExMatrix(list(target_obj.data), False)

        # 5. Обрабатываем СНИЗУ ВВЕРХ
        if is_2d:
            return self._do_matrix(target_obj, matching_rows)
        else:
            return self._do_vector(target_obj, matching_rows)

    # ------------------------------------------------------------
    # Матрица
    # ------------------------------------------------------------
    def _do_matrix(self, matrix_obj, matching_rows):
        result_data = [
            list(row) if isinstance(row, list) else [row]
            for row in matrix_obj.data
        ]

        n_cols = matrix_obj.cols
        empty_row = [None] * n_cols

        for row_num in sorted(matching_rows, reverse=True):
            src_idx = row_num

            if src_idx >= len(result_data):
                continue

            if self.direction == 'after':
                insert_idx = src_idx + 1
            else:
                insert_idx = src_idx

            result_data.insert(insert_idx, list(empty_row))

        max_cols = max(len(r) for r in result_data) if result_data else 0
        for r in result_data:
            while len(r) < max_cols:
                r.append(None)

        return MatrExMatrix(result_data, True)

    # ------------------------------------------------------------
    # Вектор
    # ------------------------------------------------------------
    def _do_vector(self, vector_obj, matching_rows):
        result_data = list(vector_obj.data)

        for idx in sorted(matching_rows, reverse=True):
            if self.direction == 'after':
                insert_idx = idx + 1
            else:
                insert_idx = idx

            result_data.insert(insert_idx, None)

        return MatrExMatrix(result_data, False)

    def __repr__(self):
        return f"insertif({self.condition}, {self.direction})"