"""
Функция COPY - копирование столбца/строки внутри матрицы.

⚠️  Работает ТОЛЬКО с Matrix (RAM).
    НЕ работает с BigData (DuckDB).

СИНТАКСИС (ТОЛЬКО РЕЖИМ ПРОГРАММИСТА):

    copy(s[:, 1], s[:, 10], after)
    copy(s[:, 1:3], s[:, 10], after)
    copy(s[:, end], s[:, 10], after)
    copy(s[:, "B"], s[:, "D"], after)
    copy(s[2, :], s[10, :], before)
    copy(s[2:5, :], s[10, :], after)
    copy(s["Боб", :], s["Гоша", :], after)
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


class CopyNode(Node):
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
                code="COPY_BAD_SYNTAX",
                context=None,
                message="copy: ожидается индекс матрицы.",
                suggestion=(
                    "Примеры:\n"
                    "     copy(s[:, 1], s[:, 10], after)\n"
                    "     copy(s[2, :], s[10, :], before)"
                ),
            )

        matrix_obj = self.data.matrix.evaluate(env)

        # ============================================================
        # ВАЖНО: сначала проверяем BigData (DuckDB)
        # ============================================================
        if _is_duckdb(matrix_obj):
            raise ArrayVatorError(
                code="COPY_DUCKDB",
                context=None,
                message=(
                    "copy работает только с Matrix (RAM), "
                    "не с BigData (DuckDB).\n"
                    "  BigData — read-only view на файл."
                ),
                suggestion=(
                    "BigData (DuckDB) — read-only view на файл.\n"
                    "Он НЕ поддерживает копирование столбцов/строк.\n"
                    "\n"
                    "Решение:\n"
                    "  1. Конвертировать BigData в Matrix:\n"
                    "        m = ToMatrix(bd)\n"
                    "        r = copy(m[:, 1], m[:, 3], after)\n"
                    "\n"
                    "  2. Работать напрямую с Matrix."
                ),
            )

        # ============================================================
        # Проверка: не матрица
        # ============================================================
        if not hasattr(matrix_obj, 'data') or not matrix_obj.is_2d:
            raise ArrayVatorError(
                code="COPY_BAD_SOURCE",
                context=None,
                message="copy: объект не является матрицей.",
                suggestion=(
                    "copy работает только с 2D-матрицами.\n"
                    "\n"
                    "✅  copy(m[:, 1], m[:, 3], after)\n"
                    "✅  copy(m[2, :], m[4, :], before)"
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
                code="COPY_BAD_SYNTAX",
                context=None,
                message=(
                    "copy: направление должно быть before или after.\n"
                    f"  Получено: {direction}"
                ),
                suggestion=(
                    "Примеры:\n"
                    "     copy(m[:, 1], m[:, 3], before)\n"
                    "     copy(m[:, 1], m[:, 3], after)"
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
                code="COPY_BAD_TARGET",
                context=None,
                message="copy: цель должна быть индексом.",
                suggestion=(
                    "Примеры:\n"
                    "     copy(m[:, 1], m[:, 3], after)\n"
                    "     copy(m[2, :], m[4, :], before)"
                ),
            )

        source_type, src_range = self._analyze(source_node, matrix_obj, env)
        target_type, tgt_range = self._analyze(target_node, matrix_obj, env)

        if source_type != target_type:
            raise ArrayVatorError(
                code="COPY_TYPE_MISMATCH",
                context=None,
                message=(
                    "copy: источник и цель должны быть одного типа.\n"
                    "  Нельзя смешивать строки и столбцы."
                ),
                suggestion=(
                    "Если источник — столбец, цель тоже столбец.\n"
                    "Если источник — строка, цель тоже строка.\n"
                    "\n"
                    "✅  copy(m[:, 1], m[:, 3], after)\n"
                    "✅  copy(m[2, :], m[4, :], before)"
                ),
            )

        src_start, src_end = src_range
        tgt_start, tgt_end = tgt_range

        if tgt_start != tgt_end:
            raise ArrayVatorError(
                code="COPY_TARGET_IS_RANGE",
                context=None,
                message=(
                    "copy: цель не может быть диапазоном.\n"
                    "  Цель — конкретный столбец или строка."
                ),
                suggestion=(
                    "❌  copy(m[:, 1], m[:, 3:5], after)\n"
                    "✅  copy(m[:, 1], m[:, 5], after)"
                ),
            )

        target_pos = tgt_start

        if source_type == 'column':
            return self._copy_columns(
                matrix_obj, src_start, src_end, target_pos, direction
            )
        else:
            return self._copy_rows(
                matrix_obj, src_start, src_end, target_pos, direction
            )

    def _analyze(self, index_node, matrix_obj, env):
        """
        Возвращает (type, (start, end)) — 1-based.
        type: 'column' | 'row'
        """
        indices = index_node.indices
        if len(indices) != 2:
            raise ValueError("copy: индекс должен содержать 2 значения.")

        row_spec = (indices[0].evaluate(env)
                    if hasattr(indices[0], 'evaluate')
                    else indices[0])
        col_spec = (indices[1].evaluate(env)
                    if hasattr(indices[1], 'evaluate')
                    else indices[1])

        row_is_all = isinstance(row_spec, str) and row_spec.strip().lower() in (':', 'all')
        col_is_all = isinstance(col_spec, str) and col_spec.strip().lower() in (':', 'all')

        # s[:, X] — столбец
        if row_is_all and not col_is_all:
            start, end = _resolve_col_range(matrix_obj, col_spec, env)
            return ('column', (start, end))

        # s[N, :] — строка
        if col_is_all and not row_is_all:
            start, end = _resolve_row_range(matrix_obj, row_spec, env)
            return ('row', (start, end))

        raise ValueError("copy: укажите столбец или строку.")

    # ------------------------------------------------------------
    # Копирование столбцов
    # ------------------------------------------------------------
    def _copy_columns(self, matrix_obj, src_start, src_end, tgt_pos, direction):
        src_data = []
        for row in matrix_obj.data:
            src_cols = []
            for j in range(src_start - 1, src_end):
                if j < len(row):
                    src_cols.append(row[j])
                else:
                    src_cols.append(None)
            src_data.append(src_cols)

        if direction == 'after':
            insert_pos = tgt_pos
        else:
            insert_pos = tgt_pos - 1

        result_data = []
        for i, row in enumerate(matrix_obj.data):
            new_row = list(row)
            while len(new_row) < insert_pos:
                new_row.append(None)
            for k, val in enumerate(src_data[i]):
                new_row.insert(insert_pos + k, val)
            result_data.append(new_row)

        return MatrExMatrix(result_data, True)

    # ------------------------------------------------------------
    # Копирование строк
    # ------------------------------------------------------------
    def _copy_rows(self, matrix_obj, src_start, src_end, tgt_pos, direction):
        src_rows = []
        for i in range(src_start - 1, src_end):
            if i < len(matrix_obj.data):
                src_rows.append(list(matrix_obj.data[i]))
            else:
                src_rows.append([None] * matrix_obj.cols)

        if direction == 'after':
            insert_pos = tgt_pos
        else:
            insert_pos = tgt_pos - 1

        result_data = [list(row) for row in matrix_obj.data]
        while len(result_data) < insert_pos:
            result_data.append([None] * matrix_obj.cols)

        for k, row in enumerate(src_rows):
            result_data.insert(insert_pos + k, row)

        return MatrExMatrix(result_data, True)

    def __repr__(self):
        return f"copy({self.data}, ..., {self.direction})"


# ============================================================
# РАЗРЕШЕНИЕ ДИАПАЗОНА СТОЛБЦА (с именем)
# ============================================================

def _resolve_col_range(matrix_obj, col_spec, env):
    """
    Возвращает (start, end) — 1-based.
    Поддерживает имя "B", end, last N, диапазон, число.
    """
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
    """
    Возвращает (start, end) — 1-based.
    Поддерживает имя "Боб", end, last N, диапазон, число.
    """
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
            try:
                idx, _ = resolve_row_index(matrix_obj, row_spec, env)
                return (idx + 1, idx + 1)
            except Exception:
                raise

    return parse_range_spec(row_spec, matrix_obj.rows, is_column=False)