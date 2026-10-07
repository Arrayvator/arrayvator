# ast_nodes/functions/unpivot.py
"""
Функция UNPIVOT — превращает широкую таблицу в длинную.

СИНТАКСИС:
    unpivot(срез, by срез)
    unpivot(срез, by срез1, срез2, ...)
    unpivot(срез, by срез, names "Имя1", "Имя2")
    unpivot(срез, by срез1, срез2, names "Имя1", "Имя2")

ПРАВИЛА:
    - Первый аргумент — срез, который складываем.
    - by — идентификаторы (срез или список срезов).
    - names — имена двух новых колонок (опционально).
    - Всегда возвращает новую таблицу.
    - by и data не должны пересекаться.
"""

from ..base import Node
from runtime.matrix import MatrExMatrix
from errors import ArrayVatorError


def _is_duckdb(val):
    try:
        from duckdb_engine import DuckDBTable
        return isinstance(val, DuckDBTable)
    except ImportError:
        return False


class UnpivotNode(Node):
    def __init__(self, data, by, names=None):
        self.data = data
        self.by = by
        self.names = names

    def evaluate(self, env):
        from ast_nodes.index import IndexNode

        # ============================================================
        # 1. Проверка: data — срез
        # ============================================================
        if not isinstance(self.data, IndexNode):
            raise ArrayVatorError(
                code="UNPIVOT_BAD_DATA_SLICE",
                context=None,
            )

        # ============================================================
        # 2. Проверка: by — срез или список срезов
        # ============================================================
        if isinstance(self.by, IndexNode):
            by_list = [self.by]
        elif isinstance(self.by, list):
            by_list = self.by
            for b in by_list:
                if not isinstance(b, IndexNode):
                    raise ArrayVatorError(
                        code="UNPIVOT_BAD_BY_SLICE",
                        context=None,
                    )
        else:
            raise ArrayVatorError(
                code="UNPIVOT_BAD_BY_SLICE",
                context=None,
            )

        # ============================================================
        # 3. Матрица
        # ============================================================
        matrix_obj = self.data.matrix.evaluate(env)

        if _is_duckdb(matrix_obj):
            return self._unpivot_duckdb(matrix_obj, by_list, env)

        if not hasattr(matrix_obj, 'data') or not matrix_obj.is_2d:
            raise ArrayVatorError(
                code="UNPIVOT_BAD_DATA_SLICE",
                context=None,
            )

        return self._unpivot_matrix(matrix_obj, by_list, env)

    # ============================================================
    # MATRIX
    # ============================================================
    def _unpivot_matrix(self, matrix_obj, by_nodes, env):
        # Столбцы «складываем»
        data_cols = self._resolve_columns(
            self.data, matrix_obj, env, kind="складываем"
        )

        # Столбцы «by» — объединяем все
        by_cols = []
        for node in by_nodes:
            by_cols.extend(
                self._resolve_columns(node, matrix_obj, env, kind="by")
            )

        # Проверка пересечения
        common = set(data_cols) & set(by_cols)
        if common:
            raise ArrayVatorError(
                code="UNPIVOT_COLUMN_OVERLAP",
                context=None,
                message=(
                    f"unpivot: колонки {sorted(common)} "
                    f"попали и в 'складываем', и в 'by'.\n"
                    f"  Они не должны пересекаться."
                ),
            )

        # Имена новых колонок
        name_var = "Переменная"
        name_val = "Значение"
        if self.names:
            name_var = self._eval_str(self.names[0], env)
            name_val = self._eval_str(self.names[1], env)

        header_row = matrix_obj.data[0] if matrix_obj.rows > 0 else []
        by_headers = [header_row[c] for c in by_cols]
        var_names = [header_row[c] for c in data_cols]

        result = [by_headers + [name_var, name_val]]

        for i in range(1, matrix_obj.rows):
            row = matrix_obj.data[i]
            by_values = [
                row[c] if c < len(row) else None
                for c in by_cols
            ]
            for j, c in enumerate(data_cols):
                val = row[c] if c < len(row) else None
                result.append(by_values + [var_names[j], val])

        return MatrExMatrix(result, True)

    # ============================================================
    # DUCKDB
    # ============================================================
    def _unpivot_duckdb(self, duck_table, by_nodes, env):
        from duckdb_engine import DuckDBTable
        import uuid

        columns = duck_table.get_columns()

        data_idx = self._resolve_duckdb_columns(
            self.data, duck_table, columns, env
        )

        by_idx = []
        for node in by_nodes:
            by_idx.extend(
                self._resolve_duckdb_columns(
                    node, duck_table, columns, env
                )
            )

        # Проверка пересечения
        common = set(data_idx) & set(by_idx)
        if common:
            names = [columns[i] for i in sorted(common)]
            raise ArrayVatorError(
                code="UNPIVOT_COLUMN_OVERLAP",
                context=None,
                message=(
                    f"unpivot: колонки {names} "
                    f"попали и в 'складываем', и в 'by'."
                ),
            )

        data_cols = [columns[i] for i in data_idx]
        by_cols = [columns[i] for i in by_idx]

        name_var = "Переменная"
        name_val = "Значение"
        if self.names:
            name_var = self._eval_str(self.names[0], env)
            name_val = self._eval_str(self.names[1], env)

        parts = []
        for col in data_cols:
            safe_by = ", ".join(
                f'"{str(c).replace(chr(34), chr(34)+chr(34))}"'
                for c in by_cols
            )
            if safe_by:
                safe_by += ", "
            safe_col = '"' + str(col).replace('"', '""') + '"'
            safe_var = "'" + str(col).replace("'", "''") + "'"
            parts.append(f"""
                SELECT {safe_by}
                       {safe_var} AS "{name_var}",
                       CAST({safe_col} AS VARCHAR) AS "{name_val}"
                FROM {duck_table.table_name}
            """)

        union_sql = " UNION ALL ".join(parts)

        # ORDER BY по by-колонкам + по имени переменной
        order_parts = []
        for c in by_cols:
            order_parts.append(
                f'"{str(c).replace(chr(34), chr(34)+chr(34))}"'
            )
        order_parts.append(
            f'"{name_var.replace(chr(34), chr(34)+chr(34))}"'
        )
        order_sql = ", ".join(order_parts)
        if order_sql:
            union_sql = f"SELECT * FROM ({union_sql}) ORDER BY {order_sql}"

        new_name = f"unpivot_{uuid.uuid4().hex[:8]}"
        sql = f"CREATE OR REPLACE VIEW {new_name} AS {union_sql}"

        try:
            duck_table.con.execute(sql)
        except Exception as e:
            raise RuntimeError(f"Ошибка unpivot: {e}\nSQL: {sql}")

        new_table = DuckDBTable.__new__(DuckDBTable)
        new_table.path = duck_table.path
        new_table.table_name = new_name
        new_table.con = duck_table.con
        new_table.utf8_path = duck_table.utf8_path
        new_table.is_temp = False
        new_table._tmp_path = None

        return new_table

    # ============================================================
    # ХЕЛПЕРЫ
    # ============================================================
    def _resolve_columns(self, index_node, matrix_obj, env, kind):
        """Возвращает список 0-based индексов колонок из IndexNode."""
        from ..utils.index_utils import parse_range_spec, resolve_column_index

        if len(index_node.indices) != 2:
            raise ArrayVatorError(
                code="UNPIVOT_BAD_DATA_SLICE",
                context=None,
                message=f"unpivot: {kind} должен быть срезом m[:, ...]",
            )

        row_spec = index_node.indices[0]
        col_spec = index_node.indices[1]

        row_val = (row_spec.evaluate(env)
                   if hasattr(row_spec, 'evaluate')
                   else row_spec)
        if not (isinstance(row_val, str)
                and row_val.lower() in (':', 'all')):
            raise ArrayVatorError(
                code="UNPIVOT_BAD_DATA_SLICE",
                context=None,
                message=(
                    f"unpivot: {kind} должен быть полным срезом "
                    f"по строкам (m[:, ...])"
                ),
            )

        col_val = (col_spec.evaluate(env)
                   if hasattr(col_spec, 'evaluate')
                   else col_spec)
        col_val_str = str(col_val)

        s = col_val_str.strip().lower()

        if s in (':', 'all'):
            return list(range(matrix_obj.cols))

        if ':' in s:
            start, end = parse_range_spec(
                col_val_str, matrix_obj.cols, is_column=True
            )
            return list(range(start - 1, end))

        if s == 'end':
            return [matrix_obj.cols - 1]
        if s.startswith('end-'):
            n = int(s[4:].strip())
            return [matrix_obj.cols - n - 1]
        if s.startswith('last'):
            n = int(s[4:].strip())
            return list(range(matrix_obj.cols - n, matrix_obj.cols))

        idx, _ = resolve_column_index(matrix_obj, col_val, env)
        return [idx]

    def _resolve_duckdb_columns(self, index_node, duck_table, columns, env):
        """Возвращает список 0-based индексов колонок для DuckDB."""
        from .filterif import _resolve_column_for_duckdb
        from ..utils.index_utils import parse_range_spec

        if len(index_node.indices) != 2:
            raise ArrayVatorError(
                code="UNPIVOT_BAD_BY_SLICE",
                context=None,
                message="unpivot: ожидается срез m[:, ...]",
            )

        col_spec_node = index_node.indices[1]
        col_spec = (col_spec_node.evaluate(env)
                    if hasattr(col_spec_node, 'evaluate')
                    else col_spec_node)

        s = str(col_spec).strip().lower()

        if s in (':', 'all'):
            return list(range(len(columns)))

        if ':' in s:
            start, end = parse_range_spec(
                str(col_spec), len(columns), is_column=True
            )
            return list(range(start - 1, end))

        if s == 'end':
            return [len(columns) - 1]
        if s.startswith('end-'):
            n = int(s[4:].strip())
            return [len(columns) - n - 1]
        if s.startswith('last'):
            n = int(s[4:].strip())
            return list(range(len(columns) - n, len(columns)))

        idx = _resolve_column_for_duckdb(columns, col_spec)
        return [idx]

    def _eval_str(self, node, env):
        val = node.evaluate(env) if hasattr(node, 'evaluate') else node
        if not isinstance(val, str):
            raise ArrayVatorError(
                code="UNPIVOT_BAD_NAMES",
                context=None,
                message=(
                    f"unpivot: имя колонки должно быть строкой, "
                    f"получено {type(val).__name__}"
                ),
            )
        return val

    def __repr__(self):
        if self.names:
            return f"unpivot({self.data}, by {self.by}, names {self.names})"
        return f"unpivot({self.data}, by {self.by})"