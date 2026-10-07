"""
Функция MOVE - перемещение столбца/строки внутри матрицы.

⚠️  Работает ТОЛЬКО с Matrix (RAM).
    НЕ работает с BigData (DuckDB).

СИНТАКСИС:
    move(s[:, 1], s[:, 10], after)
    move(s[:, 1:3], s[:, 10], after)
    move(s[:, end], s[:, 10], after)
    move(s[2, :], s[10, :], before)
    move(s[1:10, :], s[end, :], after)
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


class MoveNode(Node):
    def __init__(self, data, source_type, source_value,
                 target_type, target_value, direction):
        self.data = data
        self.source_type = source_type
        self.source_value = source_value
        self.target_type = target_type
        self.target_value = target_value
        self.direction = direction

    def evaluate(self, env):
        from ast_nodes.index import IndexNode
        from errors import ArrayVatorError

        if not isinstance(self.data, IndexNode):
            raise ArrayVatorError(
                code="MOVE_BAD_SYNTAX",
                context=None,
                message="move: ожидается индекс матрицы.",
                suggestion=(
                    "Примеры:\n"
                    "     move(s[:, 1], s[:, 10], after)\n"
                    "     move(s[2, :], s[10, :], before)"
                ),
            )

        matrix_obj = self.data.matrix.evaluate(env)

        # ============================================================
        # ВАЖНО: сначала проверяем BigData (DuckDB)
        # ============================================================
        if _is_duckdb(matrix_obj):
            raise ArrayVatorError(
                code="MOVE_DUCKDB",
                context=None,
                message=(
                    "move работает только с Matrix (RAM), "
                    "не с BigData (DuckDB).\n"
                    "  BigData — read-only view на файл."
                ),
                suggestion=(
                    "BigData (DuckDB) — read-only view на файл.\n"
                    "Он НЕ поддерживает перемещение столбцов/строк.\n"
                    "\n"
                    "Решение:\n"
                    "  1. Конвертировать BigData в Matrix:\n"
                    "        m = ToMatrix(bd)\n"
                    "        r = move(m[:, 1], m[:, 4], after)\n"
                    "\n"
                    "  2. Работать напрямую с Matrix."
                ),
            )

        # ============================================================
        # Проверка: не матрица
        # ============================================================
        if not hasattr(matrix_obj, 'data') or not matrix_obj.is_2d:
            raise ArrayVatorError(
                code="MOVE_BAD_SOURCE",
                context=None,
                message="move: объект не является матрицей.",
                suggestion=(
                    "move работает только с 2D-матрицами.\n"
                    "\n"
                    "Правильно:\n"
                    "     move(m[:, 1], m[:, 4], after)\n"
                    "     move(m[2, :], m[10, :], before)"
                ),
            )

        # ============================================================
        # Направление
        # ============================================================
        direction = (self.direction.evaluate(env)
                     if hasattr(self.direction, 'evaluate')
                     else self.direction)
        if isinstance(direction, str):
            direction = direction.lower()
        if direction not in ('before', 'after'):
            raise ArrayVatorError(
                code="MOVE_BAD_SYNTAX",
                context=None,
                message=(
                    "move: направление должно быть before или after.\n"
                    f"  Получено: {direction}"
                ),
                suggestion=(
                    "Примеры:\n"
                    "     move(m[:, 1], m[:, 4], before)\n"
                    "     move(m[:, 1], m[:, 4], after)"
                ),
            )

        return self._execute(env, matrix_obj, direction)

    def _execute(self, env, matrix_obj, direction):
        from ast_nodes.index import IndexNode
        from errors import ArrayVatorError

        source_node = self.data
        target_node = self.target_value

        if not isinstance(target_node, IndexNode):
            raise ArrayVatorError(
                code="MOVE_BAD_TARGET",
                context=None,
                message="move: цель должна быть индексом.",
                suggestion=(
                    "Примеры:\n"
                    "     move(m[:, 1], m[:, 4], after)\n"
                    "     move(m[2, :], m[10, :], before)"
                ),
            )

        source_type, src_range = self._analyze(source_node, matrix_obj, env)
        target_type, tgt_range = self._analyze(target_node, matrix_obj, env)

        if source_type != target_type:
            raise ArrayVatorError(
                code="MOVE_TYPE_MISMATCH",
                context=None,
                message=(
                    "move: источник и цель должны быть одного типа.\n"
                    "  Нельзя смешивать строки и столбцы."
                ),
                suggestion=(
                    "Если источник — столбец, цель тоже столбец.\n"
                    "Если источник — строка, цель тоже строка.\n"
                    "\n"
                    "Правильно:\n"
                    "     move(m[:, 1], m[:, 4], after)\n"
                    "     move(m[2, :], m[10, :], before)"
                ),
            )

        src_start, src_end = src_range
        tgt_start, tgt_end = tgt_range

        if tgt_start != tgt_end:
            raise ArrayVatorError(
                code="MOVE_TARGET_IS_RANGE",
                context=None,
                message=(
                    "move: цель не может быть диапазоном.\n"
                    "  Цель — конкретный столбец или строка."
                ),
                suggestion=(
                    "Неправильно:\n"
                    "     move(m[:, 1], m[:, 3:5], after)\n"
                    "\n"
                    "Правильно:\n"
                    "     move(m[:, 1], m[:, 5], after)"
                ),
            )

        target_pos = tgt_start

        # Проверка: цель внутри источника?
        if src_start <= target_pos <= src_end:
            raise ArrayVatorError(
                code="MOVE_TARGET_INSIDE_SOURCE",
                context=None,
                message=(
                    "move: цель находится ВНУТРИ источника.\n"
                    f"  Источник: {src_start}..{src_end}\n"
                    f"  Цель: {target_pos}"
                ),
                suggestion=(
                    "Укажите цель ВНЕ источника.\n"
                    "\n"
                    "Неправильно:\n"
                    "     move(m[:, 1:5], m[:, 3], after)\n"
                    "\n"
                    "Правильно:\n"
                    "     move(m[:, 1:5], m[:, 7], after)\n"
                    "     move(m[:, 1:5], m[:, 10], before)"
                ),
            )

        if source_type == 'column':
            return self._move_columns(
                matrix_obj, src_start, src_end, target_pos, direction
            )
        else:
            return self._move_rows(
                matrix_obj, src_start, src_end, target_pos, direction
            )

    def _analyze(self, index_node, matrix_obj, env):
        indices = index_node.indices
        if len(indices) != 2:
            raise ValueError("move: индекс должен содержать 2 значения.")

        row_spec = (indices[0].evaluate(env)
                    if hasattr(indices[0], 'evaluate')
                    else indices[0])
        col_spec = (indices[1].evaluate(env)
                    if hasattr(indices[1], 'evaluate')
                    else indices[1])

        row_is_all = isinstance(row_spec, str) and row_spec.strip().lower() in (':', 'all')
        col_is_all = isinstance(col_spec, str) and col_spec.strip().lower() in (':', 'all')

        if row_is_all and not col_is_all:
            start, end = _resolve_col_range(matrix_obj, col_spec, env)
            return ('column', (start, end))

        if col_is_all and not row_is_all:
            start, end = _resolve_row_range(matrix_obj, row_spec, env)
            return ('row', (start, end))

        raise ValueError("move: укажите столбец или строку.")

    # ------------------------------------------------------------
    # Перемещение столбцов
    # ------------------------------------------------------------
    def _move_columns(self, matrix_obj, src_start, src_end, tgt_pos, direction):
        src_data = []
        for row in matrix_obj.data:
            cols = []
            for j in range(src_start - 1, src_end):
                cols.append(row[j] if j < len(row) else None)
            src_data.append(cols)

        temp_data = []
        for row in matrix_obj.data:
            new_row = []
            for j, val in enumerate(row):
                if j < src_start - 1 or j >= src_end:
                    new_row.append(val)
            temp_data.append(new_row)

        if tgt_pos > src_end:
            tgt_pos -= (src_end - src_start + 1)

        if direction == 'after':
            insert_pos = tgt_pos
        else:
            insert_pos = tgt_pos - 1

        result_data = []
        for i, row in enumerate(temp_data):
            new_row = list(row)
            while len(new_row) < insert_pos:
                new_row.append(None)
            for k, val in enumerate(src_data[i]):
                new_row.insert(insert_pos + k, val)
            result_data.append(new_row)

        return MatrExMatrix(result_data, True)

    # ------------------------------------------------------------
    # Перемещение строк
    # ------------------------------------------------------------
    def _move_rows(self, matrix_obj, src_start, src_end, tgt_pos, direction):
        src_rows = []
        for i in range(src_start - 1, src_end):
            if i < len(matrix_obj.data):
                src_rows.append(list(matrix_obj.data[i]))
            else:
                src_rows.append([None] * matrix_obj.cols)

        result_data = []
        for i, row in enumerate(matrix_obj.data):
            if i < src_start - 1 or i >= src_end:
                result_data.append(list(row))

        if tgt_pos > src_end:
            tgt_pos -= (src_end - src_start + 1)

        if direction == 'after':
            insert_pos = tgt_pos
        else:
            insert_pos = tgt_pos - 1

        while len(result_data) < insert_pos:
            result_data.append([None] * matrix_obj.cols)

        for k, row in enumerate(src_rows):
            result_data.insert(insert_pos + k, row)

        return MatrExMatrix(result_data, True)

    def __repr__(self):
        return f"move({self.data}, ..., {self.direction})"


# ============================================================
# РАЗРЕШЕНИЕ ДИАПАЗОНА СТОЛБЦА (с именем)
# ============================================================

def _resolve_col_range(matrix_obj, col_spec, env):
    if isinstance(col_spec, str):
        s = col_spec.strip().lower()
        is_special = (
            s in (':', 'all', 'end')
            or s.startswith('end-')
            or s.startswith('end+')
            or s.startswith('last')
            or ':' in s
        )
        if not is_special:
            idx, _ = resolve_column_index(matrix_obj, col_spec, env)
            return (idx + 1, idx + 1)
    return parse_range_spec(col_spec, matrix_obj.cols, is_column=True)


# ============================================================
# РАЗРЕШЕНИЕ ДИАПАЗОНА СТРОКИ (с именем)
# ============================================================

def _resolve_row_range(matrix_obj, row_spec, env):
    if isinstance(row_spec, str):
        s = row_spec.strip().lower()
        is_special = (
            s in (':', 'all', 'end')
            or s.startswith('end-')
            or s.startswith('end+')
            or s.startswith('last')
            or ':' in s
        )
        if not is_special:
            idx, _ = resolve_row_index(matrix_obj, row_spec, env)
            return (idx + 1, idx + 1)
    return parse_range_spec(row_spec, matrix_obj.rows, is_column=False)