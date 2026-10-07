# ast_nodes/functions/transpose.py
"""
Функция транспонирования: TransposeNode

⚠️  Работает ТОЛЬКО с Matrix (RAM).
    НЕ работает с BigData (DuckDB).

СИНТАКСИС:
    r = transpose(m)
    m = transpose(m)
"""

from ..base import Node


def _is_duckdb(val):
    try:
        from duckdb_engine import DuckDBTable
        return isinstance(val, DuckDBTable)
    except ImportError:
        return False


class TransposeNode(Node):
    def __init__(self, arg):
        self.arg = arg

    def evaluate(self, env):
        from runtime.matrix import MatrExMatrix
        from errors import ArrayVatorError

        value = self.arg.evaluate(env) if hasattr(self.arg, 'evaluate') else self.arg

        # ============================================================
        # ВАЖНО: сначала проверяем BigData (DuckDB)
        # ============================================================
        if _is_duckdb(value):
            raise ArrayVatorError(
                code="TRANSPOSE_DUCKDB",
                context=None,
                message=(
                    "transpose работает только с Matrix (RAM), "
                    "не с BigData (DuckDB).\n"
                    "  BigData — read-only view на файл."
                ),
                suggestion=(
                    "BigData (DuckDB) — read-only view на файл.\n"
                    "Он НЕ поддерживает транспонирование.\n"
                    "\n"
                    "Решение:\n"
                    "  1. Конвертировать BigData в Matrix:\n"
                    "        m = ToMatrix(bd)\n"
                    "        r = transpose(m)\n"
                    "\n"
                    "  2. Работать напрямую с Matrix."
                ),
            )

        # ============================================================
        # Проверка: не матрица и не вектор
        # ============================================================
        if not hasattr(value, 'data'):
            raise ArrayVatorError(
                code="TRANSPOSE_NOT_MATRIX",
                context=None,
                message=(
                    "transpose: ожидается матрица или вектор."
                ),
                suggestion=(
                    "transpose работает только с 2D-матрицами\n"
                    "и векторами.\n"
                    "\n"
                    "❌  transpose(42)\n"
                    "❌  transpose(\"text\")\n"
                    "✅  transpose(m)\n"
                    "✅  transpose(v)"
                ),
            )

        # ============================================================
        # Вектор → матрица N×1
        # ============================================================
        if not value.is_2d:
            new_data = [[x] for x in value.data]
            return MatrExMatrix(new_data, True)

        # ============================================================
        # Пустая матрица
        # ============================================================
        if value.rows == 0:
            return MatrExMatrix([], True)

        # ============================================================
        # Транспонирование
        # ============================================================
        transposed_data = []
        for j in range(value.cols):
            new_row = []
            for i in range(value.rows):
                new_row.append(value.data[i][j])
            transposed_data.append(new_row)

        return MatrExMatrix(transposed_data, True)

    def __repr__(self):
        return f"Transpose({self.arg})"