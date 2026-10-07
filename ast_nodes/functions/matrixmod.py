# ast_nodes/functions/matrixmod.py
"""
Функция MATRIXMOD — модификация строк матрицы.

⚠️  РАБОТАЕТ ТОЛЬКО С MATRIX (RAM).
    НЕ работает с BigData (DuckDB).

СИНТАКСИС:
    matrixmod(m, delete, N)              # удалить строки N
    matrixmod(m, insert, N, before)      # пустые строки перед N
    matrixmod(m, insert, N, after)       # пустые строки после N
    matrixmod(m, duplicate, N, before)   # копии строк перед N
    matrixmod(m, duplicate, N, after)    # копии строк после N
    matrixmod(m, clear, N)               # обнулить строки N
    matrixmod(m, keep, N)                # оставить только строки N
    matrixmod(m, swap, [a, b])           # поменять строки a и b

N — число, вектор, переменная, last K, end.

ПРАВИЛА:
    - Только строки, не столбцы.
    - Порядок обработки — снизу вверх (по убыванию).
    - Дубликаты в N обрабатываются каждый раз.
    - Заголовок сохраняется при keep.
    - При delete/clear заголовок может быть удалён (ответственность аналитика).
"""

from ..base import Node
from runtime.matrix import MatrExMatrix
from ..utils.index_utils import parse_range_spec


def _is_duckdb(val):
    try:
        from duckdb_engine import DuckDBTable
        return isinstance(val, DuckDBTable)
    except ImportError:
        return False


class MatrixModNode(Node):
    def __init__(self, data, action, positions, direction=None):
        self.data = data
        self.action = action
        self.positions = positions
        self.direction = direction

    def evaluate(self, env):
        from errors import ArrayVatorError

        # 1. Получаем матрицу
        matrix_obj = self.data.evaluate(env) if hasattr(self.data, 'evaluate') else self.data

        # ============================================================
        # ВАЖНО: сначала проверяем BigData (DuckDB)
        # ============================================================
        if _is_duckdb(matrix_obj):
            raise ArrayVatorError(
                code="MATRIXMOD_DUCKDB",
                context=None,
                message=(
                    "matrixmod работает только с Matrix (RAM), "
                    "не с BigData (DuckDB).\n"
                    "  BigData — read-only view на файл."
                ),
                suggestion=(
                    "BigData (DuckDB) — read-only view на файл.\n"
                    "Он НЕ поддерживает модификацию строк.\n"
                    "\n"
                    "Решение:\n"
                    "  1. Конвертировать BigData в Matrix:\n"
                    "        m = ToMatrix(bd)\n"
                    "        r = matrixmod(m, delete, 2)\n"
                    "\n"
                    "  2. Использовать SQL-аналог:\n"
                    "        filterif, deleteif, addrows"
                ),
            )

        if not hasattr(matrix_obj, 'data') or not matrix_obj.is_2d:
            raise ArrayVatorError(
                code="MATRIXMOD_BAD_SYNTAX",
                context=None,
                message=(
                    "matrixmod: ожидается матрица.\n"
                    "  Пример: matrixmod(m, delete, 2)"
                ),
            )

        # 2. Получаем номера строк
        positions = self._resolve_positions(self.positions, matrix_obj.rows, env)

        # 3. Выполняем действие
        if self.action == 'delete':
            return self._do_delete(matrix_obj, positions)
        elif self.action == 'insert':
            return self._do_insert(matrix_obj, positions)
        elif self.action == 'duplicate':
            return self._do_duplicate(matrix_obj, positions)
        elif self.action == 'clear':
            return self._do_clear(matrix_obj, positions)
        elif self.action == 'keep':
            return self._do_keep(matrix_obj, positions)
        elif self.action == 'swap':
            return self._do_swap(matrix_obj, positions)
        else:
            raise ArrayVatorError(
                code="MATRIXMOD_BAD_ACTION",
                context=None,
                message=(
                    f"matrixmod: неизвестное действие '{self.action}'.\n"
                    f"  Допустимо: delete, insert, duplicate, clear, keep, swap."
                ),
            )

    # ============================================================
    # ПОЛУЧЕНИЕ СПИСКА НОМЕРОВ
    # ============================================================
    def _resolve_positions(self, positions_node, total_rows, env):
        result = []

        def _add(val):
            if val is None:
                return
            if isinstance(val, str):
                s = val.strip().lower()
                if s == 'end':
                    result.append(total_rows)
                    return
                if s.startswith('end-'):
                    try:
                        n = int(s[4:].strip())
                        result.append(total_rows - n)
                        return
                    except ValueError:
                        pass
                if s.startswith('last'):
                    rest = s[4:].strip()
                    try:
                        n = int(rest)
                        start = total_rows - n + 1
                        if start < 1:
                            start = 1
                        for i in range(start, total_rows + 1):
                            result.append(i)
                        return
                    except ValueError:
                        pass
                try:
                    result.append(int(s))
                except ValueError:
                    pass
                return

            if isinstance(val, (int, float)):
                result.append(int(val))
                return

        # Основной узел
        val = positions_node.evaluate(env) if hasattr(positions_node, 'evaluate') else positions_node

        # Если это MatrExMatrix (вектор)
        if hasattr(val, 'data') and hasattr(val, 'is_2d'):
            if val.is_2d:
                for row in val.data:
                    if row:
                        _add(row[0])
            else:
                for item in val.data:
                    _add(item)
            return result

        if isinstance(val, list):
            for item in val:
                _add(item)
            return result

        _add(val)
        return result

    # ============================================================
    # ДЕЙСТВИЯ
    # ============================================================
    def _do_delete(self, matrix_obj, positions):
        unique_positions = sorted(set(positions), reverse=True)

        result = [list(row) if isinstance(row, list) else [row]
                  for row in matrix_obj.data]

        for pos in unique_positions:
            if 1 <= pos <= len(result):
                del result[pos - 1]

        return MatrExMatrix(result, True)

    def _do_insert(self, matrix_obj, positions):
        direction = self.direction or 'after'
        n_cols = matrix_obj.cols

        sorted_positions = sorted(positions, reverse=True)

        result = [list(row) if isinstance(row, list) else [row]
                  for row in matrix_obj.data]

        empty_row = [None] * n_cols

        for pos in sorted_positions:
            if direction == 'after':
                insert_idx = pos
            else:
                insert_idx = pos - 1

            if 0 <= insert_idx <= len(result):
                result.insert(insert_idx, list(empty_row))

        return MatrExMatrix(result, True)

    def _do_duplicate(self, matrix_obj, positions):
        direction = self.direction or 'after'

        sorted_positions = sorted(positions, reverse=True)

        result = [list(row) if isinstance(row, list) else [row]
                  for row in matrix_obj.data]

        for pos in sorted_positions:
            if not (1 <= pos <= len(result)):
                continue

            row_copy = list(result[pos - 1])

            if direction == 'after':
                insert_idx = pos
            else:
                insert_idx = pos - 1

            if 0 <= insert_idx <= len(result):
                result.insert(insert_idx, row_copy)

        return MatrExMatrix(result, True)

    def _do_clear(self, matrix_obj, positions):
        unique_positions = sorted(set(positions), reverse=True)

        result = [list(row) if isinstance(row, list) else [row]
                  for row in matrix_obj.data]

        n_cols = matrix_obj.cols

        for pos in unique_positions:
            if 1 <= pos <= len(result):
                result[pos - 1] = [None] * n_cols

        return MatrExMatrix(result, True)

    def _do_keep(self, matrix_obj, positions):
        keep_set = set(positions)
        keep_set.add(1)  # заголовок всегда остаётся

        result = []
        for i, row in enumerate(matrix_obj.data, 1):
            if i in keep_set:
                result.append(list(row) if isinstance(row, list) else [row])

        return MatrExMatrix(result, True)

    def _do_swap(self, matrix_obj, positions):
        from errors import ArrayVatorError

        if len(positions) != 2:
            raise ArrayVatorError(
                code="MATRIXMOD_SWAP_NEEDS_TWO",
                context=None,
                message=(
                    "matrixmod swap: нужно ровно ДВА номера строк.\n"
                    "  Пример: matrixmod(m, swap, [2, 5])"
                ),
                suggestion=(
                    "swap меняет две строки местами.\n"
                    "Нужно указать ровно ДВА номера.\n"
                    "\n"
                    "Правильно:\n"
                    "     matrixmod(m, swap, [2, 5])\n"
                    "     matrixmod(m, swap, [1, 3])"
                ),
            )

        a, b = positions[0], positions[1]

        if not (1 <= a <= len(matrix_obj.data)):
            raise ArrayVatorError(
                code="MATRIXMOD_SWAP_NEEDS_TWO",
                context=None,
                message=f"matrixmod swap: строка {a} вне диапазона",
            )

        if not (1 <= b <= len(matrix_obj.data)):
            raise ArrayVatorError(
                code="MATRIXMOD_SWAP_NEEDS_TWO",
                context=None,
                message=f"matrixmod swap: строка {b} вне диапазона",
            )

        result = [list(row) if isinstance(row, list) else [row]
                  for row in matrix_obj.data]

        result[a - 1], result[b - 1] = result[b - 1], result[a - 1]

        return MatrExMatrix(result, True)

    def __repr__(self):
        if self.direction:
            return f"matrixmod({self.data}, {self.action}, {self.positions}, {self.direction})"
        return f"matrixmod({self.data}, {self.action}, {self.positions})"