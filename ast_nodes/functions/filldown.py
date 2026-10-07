# ast_nodes/functions/filldown.py
"""
Функция FILLDOWN — заполнение пустых значений вниз.

⚠️  РАБОТАЕТ ТОЛЬКО С MATRIX (RAM).
    НЕ работает с BigData (DuckDB).

СИНТАКСИС:
    r = filldown(m[:, "Клиент"])
    r = filldown(m[:, "Клиент"], "")

ЛОГИКА:
    - Идёт по столбцу.
    - Если значение пустое (None, "") — берёт предыдущее непустое.
    - Если непустое — обновляет "текущее".
    - Первая строка, если пустая — остаётся пустой.

ПАРАМЕТРЫ:
    1. m[:, "X"] — срез столбца.
    2. Что считать пустотой (опц.): None (по умолчанию), "" (пустая строка),
       или список/вектор значений.
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


def _is_empty(val, empty_markers):
    """Пустое значение? По умолчанию: None и пустая строка."""
    if empty_markers is None:
        return val is None or (isinstance(val, str) and val.strip() == "")

    for marker in empty_markers:
        if val == marker:
            return True
    return False


# ============================================================
# FILLDOWN NODE
# ============================================================
class FillDownNode(Node):
    def __init__(self, data, empty_marker=None):
        self.data = data
        self.empty_marker = empty_marker

    def evaluate(self, env):
        from ast_nodes.index import IndexNode
        from errors import ArrayVatorError

        if not isinstance(self.data, IndexNode):
            raise ArrayVatorError(
                code="FILLDOWN_BAD_SYNTAX",
                context=None,
                message=(
                    "filldown: 1-й аргумент — срез m[:, \"X\"].\n"
                    "  Пример: filldown(m[:, \"Клиент\"])"
                ),
                suggestion=(
                    "filldown принимает срез одного столбца:\n"
                    "     filldown(m[:, \"Клиент\"])\n"
                    "     filldown(m[:, \"Клиент\"], \"-\")"
                ),
            )

        matrix_obj = self.data.matrix.evaluate(env)

        # ============================================================
        # ВАЖНО: сначала проверяем BigData (DuckDB)
        # ============================================================
        if _is_duckdb(matrix_obj):
            raise ArrayVatorError(
                code="FILLDOWN_DUCKDB",
                context=None,
                message=(
                    "filldown работает только с Matrix (RAM), "
                    "не с BigData (DuckDB).\n"
                    "  BigData — read-only view на файл."
                ),
                suggestion=(
                    "BigData (DuckDB) — read-only view на файл.\n"
                    "Он НЕ поддерживает заполнение вниз.\n"
                    "\n"
                    "Решение:\n"
                    "  1. Конвертировать BigData в Matrix:\n"
                    "        m = ToMatrix(bd)\n"
                    "        r = filldown(m[:, \"Клиент\"])\n"
                    "\n"
                    "  2. Использовать SQL-аналог (оконные функции):\n"
                    "        winsum, winmax"
                ),
            )

        if not hasattr(matrix_obj, 'data') or not matrix_obj.is_2d:
            raise ArrayVatorError(
                code="FILLDOWN_NOT_SLICE",
                context=None,
                message=(
                    "filldown: ожидается матрица.\n"
                    "  Пример: filldown(m[:, \"Клиент\"])"
                ),
                suggestion=(
                    "filldown принимает срез одного столбца:\n"
                    "     filldown(m[:, \"Клиент\"])\n"
                    "     filldown(m[:, 3])"
                ),
            )

        # Разрешаем столбец
        col_idx = self._resolve_col(self.data, matrix_obj, env)

        # Что считать пустотой
        empty_markers = None
        if self.empty_marker is not None:
            marker_val = (self.empty_marker.evaluate(env)
                          if hasattr(self.empty_marker, 'evaluate')
                          else self.empty_marker)
            if isinstance(marker_val, (list, tuple)):
                empty_markers = list(marker_val)
            elif hasattr(marker_val, 'data'):
                empty_markers = list(marker_val.data)
            else:
                empty_markers = [marker_val]

        # Копируем данные
        result_data = [
            list(row) if isinstance(row, list) else [row]
            for row in matrix_obj.data
        ]

        # Заполняем вниз
        last_non_empty = None
        for i in range(1, matrix_obj.rows):
            if i >= len(result_data):
                break
            row = result_data[i]
            while len(row) <= col_idx:
                row.append(None)

            val = row[col_idx]

            if _is_empty(val, empty_markers):
                if last_non_empty is not None:
                    row[col_idx] = last_non_empty
            else:
                last_non_empty = val

        # Выравнивание
        if result_data:
            max_cols = max(len(r) for r in result_data)
            for r in result_data:
                while len(r) < max_cols:
                    r.append(None)

        return MatrExMatrix(result_data, True)

    def _resolve_col(self, index_node, matrix_obj, env):
        """Возвращает 0-based индекс столбца."""
        if len(index_node.indices) != 2:
            raise TypeError("filldown: ожидается срез m[:, \"X\"]")

        col_spec_node = index_node.indices[1]
        col_spec = (col_spec_node.evaluate(env)
                    if hasattr(col_spec_node, 'evaluate')
                    else col_spec_node)

        idx, _ = resolve_column_index(matrix_obj, col_spec, env)
        return idx

    def __repr__(self):
        return f"filldown({self.data})"