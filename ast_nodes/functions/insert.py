"""
Функция INSERT - вставка ПУСТОЙ строки или столбца в матрицу.

⚠️  Работает ТОЛЬКО с Matrix (RAM).
    НЕ работает с BigData (DuckDB).

СИНТАКСИС (ТОЛЬКО РЕЖИМ ПРОГРАММИСТА):

    # Матрица:
    insert(s[2, :], before)
    insert(s[2, :], after)
    insert(s[end, :], after)
    insert(s[:, 3], before)
    insert(s[:, "Имя"], before)
    insert(s[:, end], after)

    # Вектор:
    insert(v, 3, after)
    insert(v[3], after)

ПРАВИЛА:
    - Направление (before / after) — ОБЯЗАТЕЛЬНО.
    - Расширение: если цель вне матрицы → пропущенные = None.
"""

from ..base import Node
from runtime.matrix import MatrExMatrix
from ..utils.index_utils import (
    parse_range_spec,
    resolve_column_index,
    resolve_row_index,
)


def _is_duckdb(val):
    try:
        from duckdb_engine import DuckDBTable
        return isinstance(val, DuckDBTable)
    except ImportError:
        return False


class InsertNode(Node):
    def __init__(self, data, arg1, arg2=None, arg3=None):
        self.data = data
        self.arg1 = arg1
        self.arg2 = arg2
        self.arg3 = arg3

    def evaluate(self, env):
        from ast_nodes.index import IndexNode
        from errors import ArrayVatorError

        index_node = self.data
        if not isinstance(index_node, IndexNode):
            raise ArrayVatorError(
                code="INSERT_BAD_INDEX",
                context=None,
                message="insert: ожидается индекс матрицы или вектора.",
                suggestion=(
                    "Примеры:\n"
                    "     insert(m[2, :], before)\n"
                    "     insert(m[:, 3], after)\n"
                    "     insert(v, 3, after)"
                ),
            )

        indices = index_node.indices

        # ============================================================
        # Направление
        # ============================================================
        direction = None
        for arg in [self.arg1, self.arg2, self.arg3]:
            if arg is None:
                continue
            val = arg.evaluate(env) if hasattr(arg, 'evaluate') else arg
            if isinstance(val, str) and val.lower() in ('before', 'after'):
                direction = val.lower()
                break

        if direction is None:
            raise ArrayVatorError(
                code="INSERT_MISSING_DIRECTION",
                context=None,
                message=(
                    "insert: не указано направление — before или after."
                ),
                suggestion=(
                    "insert принимает направление: before или after.\n"
                    "\n"
                    "Правильно:\n"
                    "     insert(m[2, :], before)\n"
                    "     insert(m[2, :], after)"
                ),
            )

        # ============================================================
        # ВЕКТОР (1 индекс)
        # ============================================================
        if len(indices) == 1:
            return self._insert_vector(index_node, direction, env)

        # ============================================================
        # МАТРИЦА (2 индекса)
        # ============================================================
        if len(indices) == 2:
            return self._insert_matrix(index_node, direction, env)

        raise ArrayVatorError(
            code="INSERT_BAD_INDEX",
            context=None,
            message="insert: индекс должен содержать 1 или 2 значения.",
        )

    # ------------------------------------------------------------
    # ВЕКТОР
    # ------------------------------------------------------------
    def _insert_vector(self, index_node, direction, env):
        from errors import ArrayVatorError

        vector_obj = index_node.matrix.evaluate(env)

        # DuckDB
        if _is_duckdb(vector_obj):
            raise ArrayVatorError(
                code="INSERT_DUCKDB",
                context=None,
                message=(
                    "insert работает только с Matrix (RAM), "
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
                    "        r = insert(m[2, :], before)\n"
                    "\n"
                    "  2. Работать напрямую с Matrix."
                ),
            )

        if not hasattr(vector_obj, 'data') or vector_obj.is_2d:
            raise ArrayVatorError(
                code="INSERT_BAD_INDEX",
                context=None,
                message="insert: объект не является вектором.",
                suggestion=(
                    "Для вектора:\n"
                    "     insert(v, 3, after)\n"
                    "     insert(v[3], after)"
                ),
            )

        idx_spec_node = index_node.indices[0]
        idx_spec = (idx_spec_node.evaluate(env)
                    if hasattr(idx_spec_node, 'evaluate')
                    else idx_spec_node)

        start, end = parse_range_spec(
            idx_spec, len(vector_obj.data), is_column=False
        )

        if start != end:
            raise ArrayVatorError(
                code="INSERT_BAD_INDEX",
                context=None,
                message=(
                    "insert: для вектора укажите ОДИН индекс.\n"
                    "  ✅  insert(v, 3, after)"
                ),
            )

        if direction == 'after':
            insert_pos = start
        else:
            insert_pos = start - 1

        result_data = list(vector_obj.data)
        while len(result_data) < insert_pos:
            result_data.append(None)

        result_data.insert(insert_pos, None)
        return MatrExMatrix(result_data, False)

    # ------------------------------------------------------------
    # МАТРИЦА
    # ------------------------------------------------------------
    def _insert_matrix(self, index_node, direction, env):
        from errors import ArrayVatorError

        matrix_obj = index_node.matrix.evaluate(env)

        # DuckDB
        if _is_duckdb(matrix_obj):
            raise ArrayVatorError(
                code="INSERT_DUCKDB",
                context=None,
                message=(
                    "insert работает только с Matrix (RAM), "
                    "не с BigData (DuckDB).\n"
                    "  BigData — read-only view на файл."
                ),
                suggestion=(
                    "BigData (DuckDB) — read-only view на файл.\n"
                    "Он НЕ поддерживает вставку строк/столбцов.\n"
                    "\n"
                    "Решение:\n"
                    "  1. Конвертировать BigData в Matrix:\n"
                    "        m = ToMatrix(bd)\n"
                    "        r = insert(m[2, :], before)\n"
                    "\n"
                    "  2. Работать напрямую с Matrix."
                ),
            )

        if not hasattr(matrix_obj, 'data') or not matrix_obj.is_2d:
            raise ArrayVatorError(
                code="INSERT_BAD_INDEX",
                context=None,
                message="insert: объект не является матрицей.",
                suggestion=(
                    "insert работает только с 2D-матрицами.\n"
                    "\n"
                    "Правильно:\n"
                    "     insert(m[2, :], before)\n"
                    "     insert(m[:, 3], after)"
                ),
            )

        row_node, col_node = index_node.indices

        row_spec = (row_node.evaluate(env)
                    if hasattr(row_node, 'evaluate')
                    else row_node)
        col_spec = (col_node.evaluate(env)
                    if hasattr(col_node, 'evaluate')
                    else col_node)

        row_is_all = isinstance(row_spec, str) and row_spec.strip().lower() in (':', 'all')
        col_is_all = isinstance(col_spec, str) and col_spec.strip().lower() in (':', 'all')

        # --- s[N, :] — вставка СТРОКИ ---
        if col_is_all and not row_is_all:
            return self._insert_row(matrix_obj, row_spec, direction, env)

        # --- s[:, N] — вставка СТОЛБЦА ---
        if row_is_all and not col_is_all:
            return self._insert_col(matrix_obj, col_spec, direction, env)

        raise ArrayVatorError(
            code="INSERT_BAD_INDEX",
            context=None,
            message=(
                "insert: укажите строку или столбец.\n"
                "  ✅  insert(m[2, :], before)\n"
                "  ✅  insert(m[:, 3], before)"
            ),
        )

    # ------------------------------------------------------------
    # Вставка строки
    # ------------------------------------------------------------
    def _insert_row(self, matrix_obj, row_spec, direction, env):
        try:
            pos_0based, _ = resolve_row_index(matrix_obj, row_spec, env)
        except Exception:
            if isinstance(row_spec, (int, float)):
                pos_0based = int(row_spec) - 1
            else:
                raise

        if direction == 'after':
            insert_pos = pos_0based + 1
        else:
            insert_pos = pos_0based

        result_data = [list(row) for row in matrix_obj.data]
        while len(result_data) < insert_pos:
            result_data.append([None] * matrix_obj.cols)

        new_row = [None] * matrix_obj.cols
        result_data.insert(insert_pos, new_row)

        return MatrExMatrix(result_data, True)

    # ------------------------------------------------------------
    # Вставка столбца
    # ------------------------------------------------------------
    def _insert_col(self, matrix_obj, col_spec, direction, env):
        try:
            pos_0based, _ = resolve_column_index(matrix_obj, col_spec, env)
        except Exception:
            if isinstance(col_spec, (int, float)):
                pos_0based = int(col_spec) - 1
            else:
                raise

        if direction == 'after':
            insert_pos = pos_0based + 1
        else:
            insert_pos = pos_0based

        result_data = []
        for row in matrix_obj.data:
            new_row = list(row)
            while len(new_row) < insert_pos:
                new_row.append(None)
            new_row.insert(insert_pos, None)
            result_data.append(new_row)

        return MatrExMatrix(result_data, True)

    def __repr__(self):
        return f"insert({self.data}, {self.arg1}, {self.arg2})"