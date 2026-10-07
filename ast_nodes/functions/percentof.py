# ast_nodes/functions/percentof.py
"""
Функция PERCENTOF — доля от итога (общей суммы или суммы группы).

СИНТАКСИС:
    percentof(срез)
    percentof(срез, coef)
    percentof(срез, by m[:, "Категория"])
    percentof(срез, by m[:, "Категория"], coef)

ПРАВИЛА:
    - Возвращает ВЕКТОР чисел той же длины, что данные в срезе.
    - Без coef — проценты (0–100), округление 2 знака.
    - С coef — коэффициент (0.0–1.0), округление 4 знака.
    - `by` — доля внутри группы (PARTITION BY).
    - Запись в столбец — через addcolumn.
    - Порядок аргументов — ЛЮБОЙ.

DUCKDB:
    - SUM(...) OVER () — без группировки.
    - SUM(...) OVER (PARTITION BY ...) — с группировкой.
    - Результат возвращается как вектор в RAM.
"""

from ..base import Node
from errors import ArrayVatorError


def _is_duckdb(val):
    try:
        from duckdb_engine import DuckDBTable
        return isinstance(val, DuckDBTable)
    except ImportError:
        return False


def _is_text_type(col_type):
    """Проверяет, является ли тип текстовым."""
    if not col_type:
        return False
    t = str(col_type).upper()
    for tt in ('VARCHAR', 'TEXT', 'STRING', 'CHAR', 'CLOB'):
        if tt in t:
            return True
    return False


class PercentOfNode(Node):
    def __init__(self, data, by=None, option=None):
        self.data = data       # IndexNode — срез значений
        self.by = by           # IndexNode | None — группировка
        self.option = option   # None | 'coef'

    def evaluate(self, env):
        from ast_nodes.index import IndexNode

        if not isinstance(self.data, IndexNode):
            raise ArrayVatorError(
                code="PERCENTOF_NEED_SLICE",
                context=None,
            )

        matrix_obj = self.data.matrix.evaluate(env)

        # DUCKDB
        if _is_duckdb(matrix_obj):
            return self._evaluate_duckdb(matrix_obj, env)

        # MATRIX
        if hasattr(matrix_obj, 'data') and matrix_obj.is_2d:
            return self._evaluate_matrix(matrix_obj, env)

        raise ArrayVatorError(
            code="PERCENTOF_NEED_SLICE",
            context=None,
        )

    # ============================================================
    # MATRIX
    # ============================================================
    def _evaluate_matrix(self, matrix_obj, env):
        from ast_nodes.index import IndexNode
        from ..utils.index_utils import resolve_column_index
        from runtime.matrix import MatrExMatrix

        # Столбец значений
        col_spec_node = self.data.indices[1]
        col_spec = (col_spec_node.evaluate(env)
                    if hasattr(col_spec_node, 'evaluate')
                    else col_spec_node)
        val_col, _ = resolve_column_index(matrix_obj, col_spec, env)

        # Столбец группировки (если by)
        by_col = None
        if self.by is not None:
            if not isinstance(self.by, IndexNode):
                raise ArrayVatorError(
                    code="PERCENTOF_BAD_BY",
                    context=None,
                )
            by_spec_node = self.by.indices[1]
            by_spec = (by_spec_node.evaluate(env)
                       if hasattr(by_spec_node, 'evaluate')
                       else by_spec_node)
            by_col, _ = resolve_column_index(matrix_obj, by_spec, env)

        rows = matrix_obj.rows

        # Собираем значения (без заголовка)
        values = []
        groups = []
        for i in range(1, rows):
            row = matrix_obj.data[i]
            v = row[val_col] if val_col < len(row) else None
            values.append(v)
            if by_col is not None:
                g = row[by_col] if by_col < len(row) else None
                groups.append(g)
            else:
                groups.append(None)

        # ============================================================
        # Проверка: столбец должен содержать хотя бы одно число
        # ============================================================
        has_number = False
        for v in values:
            if isinstance(v, (int, float)) and not isinstance(v, bool):
                has_number = True
                break
        if not has_number:
            raise ArrayVatorError(
                code="PERCENTOF_NOT_NUMERIC",
                context=None,
            )

        # ============================================================
        # Сумма по группам
        # ============================================================
        if by_col is None:
            total = 0.0
            for v in values:
                if isinstance(v, (int, float)) and not isinstance(v, bool):
                    total += v

            if total == 0:
                raise ArrayVatorError(
                    code="PERCENTOF_ZERO_SUM",
                    context=None,
                )

            totals = [total] * len(values)
        else:
            totals_map = {}
            for v, g in zip(values, groups):
                if isinstance(v, (int, float)) and not isinstance(v, bool):
                    totals_map[g] = totals_map.get(g, 0.0) + v
            totals = [totals_map.get(g, 0.0) for g in groups]

        # ============================================================
        # Результат
        # ============================================================
        result = []
        for v, t in zip(values, totals):
            if not isinstance(v, (int, float)) or isinstance(v, bool):
                result.append(None)
                continue
            if t == 0:
                result.append(None)
                continue
            if self.option == 'coef':
                result.append(round(v / t, 4))
            else:
                result.append(round(v / t * 100.0, 2))

        return MatrExMatrix(result, False)

    # ============================================================
    # DUCKDB
    # ============================================================
    def _evaluate_duckdb(self, duck_table, env):
        from ast_nodes.index import IndexNode
        from duckdb_engine import DuckDBTable
        from runtime.matrix import MatrExMatrix
        from .filterif import _resolve_column_for_duckdb

        # ============================================================
        # Проверка: row_spec — полный срез (без диапазона строк)
        # ============================================================
        row_spec_node = self.data.indices[0]
        row_spec = (row_spec_node.evaluate(env)
                    if hasattr(row_spec_node, 'evaluate')
                    else row_spec_node)
        if not (isinstance(row_spec, str)
                and row_spec.strip().lower() in (':', 'all')):
            raise ArrayVatorError(
                code="PERCENTOF_DUCKDB_ROW_RANGE",
                context=None,
            )

        columns = duck_table.get_columns()

        # Столбец значений
        col_spec_node = self.data.indices[1]
        col_spec = (col_spec_node.evaluate(env)
                    if hasattr(col_spec_node, 'evaluate')
                    else col_spec_node)
        val_idx = _resolve_column_for_duckdb(columns, col_spec)
        if val_idx is None or val_idx < 0 or val_idx >= len(columns):
            raise ArrayVatorError(
                code="PERCENTOF_NEED_SLICE",
                context=None,
            )
        val_col = columns[val_idx]
        safe_val = '"' + str(val_col).replace('"', '""') + '"'

        # ============================================================
        # Проверка: столбец числовой
        # ============================================================
        col_type = duck_table.get_column_type(val_col)
        if _is_text_type(col_type):
            raise ArrayVatorError(
                code="PERCENTOF_NOT_NUMERIC",
                context=None,
            )

        # ============================================================
        # Проверка: сумма != 0
        # ============================================================
        try:
            total_check = duck_table.con.execute(
                f"SELECT SUM(CAST({safe_val} AS DOUBLE)) "
                f"FROM {duck_table.table_name}"
            ).fetchone()
        except Exception:
            total_check = None

        if not total_check or total_check[0] is None or total_check[0] == 0:
            raise ArrayVatorError(
                code="PERCENTOF_ZERO_SUM",
                context=None,
            )

        # Группировка
        partition_sql = ""
        if self.by is not None:
            if not isinstance(self.by, IndexNode):
                raise ArrayVatorError(
                    code="PERCENTOF_BAD_BY",
                    context=None,
                )
            by_spec_node = self.by.indices[1]
            by_spec = (by_spec_node.evaluate(env)
                       if hasattr(by_spec_node, 'evaluate')
                       else by_spec_node)
            by_idx = _resolve_column_for_duckdb(columns, by_spec)
            if by_idx is None or by_idx < 0 or by_idx >= len(columns):
                raise ArrayVatorError(
                    code="PERCENTOF_BAD_BY",
                    context=None,
                )
            by_col = columns[by_idx]
            safe_by = '"' + str(by_col).replace('"', '""') + '"'
            partition_sql = f"PARTITION BY {safe_by}"

        # Выражение
        base = (
            f"CAST({safe_val} AS DOUBLE) "
            f"/ NULLIF(SUM(CAST({safe_val} AS DOUBLE)) OVER ({partition_sql}), 0)"
        )
        if self.option == 'coef':
            expr = f"ROUND({base}, 4)"
        else:
            expr = f"ROUND({base} * 100, 2)"

        sql = f"SELECT {expr} FROM {duck_table.table_name}"

        try:
            rows = duck_table.con.execute(sql).fetchall()
        except Exception as e:
            raise RuntimeError(f"percentof: ошибка DuckDB: {e}\nSQL: {sql}")

        values = [r[0] for r in rows]
        return MatrExMatrix(values, False)

    def __repr__(self):
        return f"percentof({self.data}, by={self.by}, option={self.option})"