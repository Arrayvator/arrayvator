# ast_nodes/functions/delete.py
"""
Функция DELETE - удаление строк и столбцов из матрицы.

ВАЖНО: delete() НЕ изменяет исходную матрицу.
Она ВОЗВРАЩАЕТ НОВУЮ матрицу.

    ❌  delete(s[2, :])              # результат теряется
    ✅  s = delete(s[2, :])          # изменяет s

СИНТАКСИС (ТОЛЬКО РЕЖИМ ПРОГРАММИСТА):

    # Строки:
    delete(s[2, :])                  # удалить строку 2
    delete(s[10:end, :])             # удалить строки 10..end
    delete(s[last 3, :])             # удалить последние 3 строки

    # Столбцы:
    delete(s[:, 3])                  # удалить столбец 3
    delete(s[:, "Имя"])              # удалить столбец "Имя"
    delete(s[:, 2:5])                # удалить столбцы 2..5
    delete(s[:, last 2])             # удалить последние 2 столбца

    # Вектор:
    delete(v[3:6])                   # удалить элементы 3..6
    delete(v[last 2])                # удалить последние 2

ПРАВИЛА:
    - Строки удаляются целиком (s[N, :] или s[range, :])
    - Столбцы удаляются целиком (s[:, N] или s[:, range] или s[:, "Имя"])
    - Нельзя удалить часть ячеек (s[10:end, 2:10] — ОШИБКА)

DUCKDB:
    - Удаление столбцов → SQL: SELECT * EXCLUDE (...)
    - Удаление строк → SQL: ROW_NUMBER() OVER ()
"""

from ..base import Node
from runtime.matrix import MatrExMatrix
from ..utils.index_utils import (
    parse_range_spec,
    resolve_column_index,
)


# ============================================================
# ХЕЛПЕР: определение DuckDBTable
# ============================================================
def _is_duckdb(val):
    """Проверяет, является ли значение DuckDBTable."""
    try:
        from duckdb_engine import DuckDBTable
        return isinstance(val, DuckDBTable)
    except ImportError:
        return False


# ============================================================
# УДАЛЕНИЕ СТРОК (Matrix)
# ============================================================

def _delete_rows(matrix_obj, row_start, row_end):
    """Удаляет строки row_start..row_end (1-based)."""
    result_data = (
        list(matrix_obj.data[:row_start - 1])
        + list(matrix_obj.data[row_end:])
    )
    return MatrExMatrix(result_data, True)


# ============================================================
# УДАЛЕНИЕ СТОЛБЦОВ (Matrix)
# ============================================================

def _delete_columns(matrix_obj, col_start, col_end):
    """Удаляет столбцы col_start..col_end (1-based)."""
    result_data = []
    for row in matrix_obj.data:
        new_row = []
        for j, val in enumerate(row):
            if j < col_start - 1 or j >= col_end:
                new_row.append(val)
        result_data.append(new_row)
    return MatrExMatrix(result_data, True)


# ============================================================
# УДАЛЕНИЕ ЭЛЕМЕНТОВ ВЕКТОРА (Matrix)
# ============================================================

def _delete_vector_items(vector_obj, start, end):
    """Удаляет элементы start..end (1-based)."""
    result_data = (
        list(vector_obj.data[:start - 1])
        + list(vector_obj.data[end:])
    )
    return MatrExMatrix(result_data, False)


# ============================================================
# ОПРЕДЕЛЕНИЕ ДИАПАЗОНА СТОЛБЦОВ (с поддержкой имени)
# ============================================================

def _resolve_column_range(matrix_obj, col_spec, env):
    """
    Возвращает (start, end) — 1-based.
    Поддерживает имя, end, last N, диапазон, число.
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
# DELETE NODE
# ============================================================

class DeleteNode(Node):
    def __init__(self, data, arg1=None, arg2=None):
        self.data = data
        self.arg1 = arg1
        self.arg2 = arg2

    def evaluate(self, env):
        from ast_nodes.index import IndexNode

        index_node = self.data
        if not isinstance(index_node, IndexNode):
            raise ValueError(
                "delete: ожидается индекс матрицы или вектора.\n"
                "  Примеры:\n"
                "    delete(s[2, :])\n"
                "    delete(s[10:end, :])\n"
                "    delete(s[:, \"Имя\"])\n"
                "    delete(v[3:6])"
            )

        indices = index_node.indices

        # --- ВЕКТОР ---
        if len(indices) == 1:
            return self._delete_vector(index_node, env)

        # --- МАТРИЦА ---
        if len(indices) == 2:
            return self._delete_matrix(index_node, env)

        raise ValueError(
            f"delete: индекс должен содержать 1 или 2 значения, "
            f"получено {len(indices)}"
        )

    # ------------------------------------------------------------
    # ВЕКТОР
    # ------------------------------------------------------------
    def _delete_vector(self, index_node, env):
        vector_obj = index_node.matrix.evaluate(env)

        if _is_duckdb(vector_obj):
            raise TypeError(
                "delete: вектор не поддерживается для DuckDB.\n"
                "  DuckDB работает только с 2D-таблицами."
            )

        if not hasattr(vector_obj, 'data'):
            raise TypeError("delete: объект не является вектором")

        if vector_obj.is_2d:
            raise TypeError("delete(v[индекс]): объект — матрица, а не вектор")

        idx_node = index_node.indices[0]
        idx_spec = (idx_node.evaluate(env)
                    if hasattr(idx_node, 'evaluate')
                    else idx_node)

        start, end = parse_range_spec(
            idx_spec, len(vector_obj.data), is_column=False
        )

        if start > end:
            return vector_obj

        return _delete_vector_items(vector_obj, start, end)

    # ------------------------------------------------------------
    # МАТРИЦА
    # ------------------------------------------------------------
    def _delete_matrix(self, index_node, env):
        matrix_obj = index_node.matrix.evaluate(env)

        # --- DUCKDB ---
        if _is_duckdb(matrix_obj):
            return self._delete_duckdb(index_node, matrix_obj, env)

        # --- MATRIX ---
        if not hasattr(matrix_obj, 'data') or not matrix_obj.is_2d:
            raise TypeError("delete: объект не является матрицей")

        row_node, col_node = index_node.indices
        row_spec = (row_node.evaluate(env)
                    if hasattr(row_node, 'evaluate')
                    else row_node)
        col_spec = (col_node.evaluate(env)
                    if hasattr(col_node, 'evaluate')
                    else col_node)

        row_is_all = _is_all(row_spec)
        col_is_all = _is_all(col_spec)

        # --- s[N, :] или s[range, :] → удаляем СТРОКИ ---
        if col_is_all and not row_is_all:
            row_start, row_end = parse_range_spec(
                row_spec, matrix_obj.rows, is_column=False
            )
            if row_start > row_end:
                return matrix_obj
            return _delete_rows(matrix_obj, row_start, row_end)

        # --- s[:, N] или s[:, range] или s[:, "Имя"] → удаляем СТОЛБЦЫ ---
        if row_is_all and not col_is_all:
            col_start, col_end = _resolve_column_range(
                matrix_obj, col_spec, env
            )
            if col_start > col_end:
                return matrix_obj
            return _delete_columns(matrix_obj, col_start, col_end)

        # --- Оба all → невалидно ---
        if row_is_all and col_is_all:
            raise ValueError(
                "delete: укажите, что удалять — строки или столбцы.\n"
                "  ✅  delete(s[2, :])      — строки\n"
                "  ✅  delete(s[:, 3])      — столбцы"
            )

        # --- Оба конкретные → ОШИБКА ---
        raise ValueError(
            "delete: нельзя удалить ЧАСТЬ ячеек.\n"
            "  Удалите СТРОКУ целиком или СТОЛБЕЦ целиком:\n"
            "      ✅  delete(s[2:5, :])     — строки 2..5\n"
            "      ✅  delete(s[:, 2:5])     — столбцы 2..5"
        )

    # ------------------------------------------------------------
    # DUCKDB
    # ------------------------------------------------------------
    def _delete_duckdb(self, index_node, duck_table, env):
        from duckdb_engine import DuckDBTable
        from .filterif import _resolve_column_for_duckdb
        import uuid

        row_node, col_node = index_node.indices
        row_spec = (row_node.evaluate(env)
                    if hasattr(row_node, 'evaluate')
                    else row_node)
        col_spec = (col_node.evaluate(env)
                    if hasattr(col_node, 'evaluate')
                    else col_node)

        row_is_all = _is_all(row_spec)
        col_is_all = _is_all(col_spec)

        columns = duck_table.get_columns()
        row_count = duck_table.get_row_count()

        # ============================================================
        # УДАЛЕНИЕ СТОЛБЦОВ
        # ============================================================
        if row_is_all and not col_is_all:
            col_indices = self._resolve_duckdb_col_indices(
                col_spec, columns, env
            )
            if not col_indices:
                return duck_table

            # Имена столбцов для EXCLUDE
            exclude_names = [columns[i] for i in col_indices]
            exclude_sql = ", ".join(
                '"' + str(c).replace('"', '""') + '"'
                for c in exclude_names
            )

            new_name = f"deleted_{uuid.uuid4().hex[:8]}"
            sql = f"""
                CREATE OR REPLACE VIEW {new_name} AS
                SELECT * EXCLUDE ({exclude_sql})
                FROM {duck_table.table_name}
            """

            try:
                duck_table.con.execute(sql)
            except Exception as e:
                raise RuntimeError(f"Ошибка delete (столбцы): {e}\nSQL: {sql}")

            new_table = DuckDBTable.__new__(DuckDBTable)
            new_table.path = duck_table.path
            new_table.table_name = new_name
            new_table.con = duck_table.con
            new_table.utf8_path = duck_table.utf8_path
            new_table.is_temp = False
            new_table._tmp_path = None

            return new_table

        # ============================================================
        # УДАЛЕНИЕ СТРОК
        # ============================================================
        if col_is_all and not row_is_all:
            row_start, row_end = parse_range_spec(
                row_spec, row_count, is_column=False
            )
            if row_start > row_end:
                return duck_table

            # Через ROW_NUMBER
            new_name = f"deleted_{uuid.uuid4().hex[:8]}"
            sql = f"""
                CREATE OR REPLACE VIEW {new_name} AS
                SELECT * EXCLUDE (__rn)
                FROM (
                    SELECT *,
                           ROW_NUMBER() OVER () AS __rn
                    FROM {duck_table.table_name}
                )
                WHERE __rn < {row_start} OR __rn > {row_end}
            """

            try:
                duck_table.con.execute(sql)
            except Exception as e:
                raise RuntimeError(f"Ошибка delete (строки): {e}\nSQL: {sql}")

            new_table = DuckDBTable.__new__(DuckDBTable)
            new_table.path = duck_table.path
            new_table.table_name = new_name
            new_table.con = duck_table.con
            new_table.utf8_path = duck_table.utf8_path
            new_table.is_temp = False
            new_table._tmp_path = None

            return new_table

        # ============================================================
        # ОБА ALL — ошибка
        # ============================================================
        if row_is_all and col_is_all:
            raise ValueError(
                "delete: укажите, что удалять — строки или столбцы.\n"
                "  ✅  delete(m[2, :])      — строки\n"
                "  ✅  delete(m[:, 3])      — столбцы"
            )

        raise ValueError(
            "delete: нельзя удалить ЧАСТЬ ячеек в DuckDB.\n"
            "  Удалите СТРОКУ целиком или СТОЛБЕЦ целиком."
        )

    def _resolve_duckdb_col_indices(self, col_spec, columns, env):
        """Возвращает список 0-based индексов столбцов."""
        from .filterif import _resolve_column_for_duckdb

        s = str(col_spec).strip().lower()

        # : / all — нельзя
        if s in (':', 'all'):
            return []

        # Диапазон
        if ':' in s:
            try:
                start, end = parse_range_spec(str(col_spec), len(columns), is_column=True)
                return list(range(start - 1, end))
            except Exception:
                return []

        # end / end-N / last N
        if s == 'end':
            return [len(columns) - 1]
        if s.startswith('end-'):
            try:
                n = int(s[4:].strip())
                return [len(columns) - n - 1]
            except ValueError:
                pass
        if s.startswith('last'):
            try:
                n = int(s[4:].strip())
                return list(range(len(columns) - n, len(columns)))
            except ValueError:
                pass

        # По имени
        idx = _resolve_column_for_duckdb(columns, col_spec)
        return [idx]

    def __repr__(self):
        if self.arg2 is not None:
            return f"delete({self.data}, {self.arg1}, {self.arg2})"
        if self.arg1 is not None:
            return f"delete({self.data}, {self.arg1})"
        return f"delete({self.data})"


# ============================================================
# ХЕЛПЕРЫ
# ============================================================

def _is_all(spec):
    """Проверяет, является ли спецификация ':' / 'all'."""
    if isinstance(spec, str):
        return spec.strip().lower() in (':', 'all')
    return False