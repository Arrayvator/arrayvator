# ast_nodes/functions/window.py
"""
Оконные функции ArrayVator.

ПОДДЕРЖКА:
    - Matrix (RAM) — реализация на Python
    - DuckDB (BigData) — трансляция в SQL OVER (...)

ДВА БАЗОВЫХ КЛАССА:
    WindowOverTable  — функции над всей таблицей
        rownumber, rank, denserank, percentrank, cumedist, ntile

    WindowOverColumn — функции над столбцом (срез m[:, "X"])
        lag, lead, firstvalue, lastvalue, nthvalue,
        winsum, winavg, wincount, winmin, winmax, winmedian, winstdev

QUALIFY — фильтр по оконной функции (работает и на Matrix, и на DuckDB).

СИНТАКСИС:
    # Над таблицей
    r = rownumber(m, by m[:, "Отдел"], order m[:, "Зарплата"], ZA)
    r = rank(m, by m[:, "Отдел"], order m[:, "Зарплата"], ZA)
    r = denserank(m, by m[:, "Отдел"], order m[:, "Зарплата"], ZA)
    r = percentrank(m, by m[:, "Отдел"], order m[:, "Зарплата"], ZA)
    r = cumedist(m, by m[:, "Отдел"], order m[:, "Зарплата"], ZA)
    r = ntile(m, 4, by m[:, "Отдел"], order m[:, "Зарплата"], ZA)

    # Над столбцом
    r = lag(m[:, "Зарплата"], 1, 0)
    r = lead(m[:, "Зарплата"], 1, 0)
    r = firstvalue(m[:, "Зарплата"], by m[:, "Отдел"], order m[:, "Дата"], AZ)
    r = lastvalue(m[:, "Зарплата"], by m[:, "Отдел"], order m[:, "Дата"], AZ)
    r = nthvalue(m[:, "Зарплата"], 2, by m[:, "Отдел"], order m[:, "Дата"], AZ)
    r = winsum(m[:, "Зарплата"], by m[:, "Отдел"], order m[:, "Дата"], AZ)
    r = winavg(m[:, "Зарплата"], by m[:, "Отдел"])
    r = wincount(m[:, "Зарплата"], by m[:, "Отдел"])
    r = winmin(m[:, "Зарплата"], by m[:, "Отдел"])
    r = winmax(m[:, "Зарплата"], by m[:, "Отдел"])
    r = winmedian(m[:, "Зарплата"], by m[:, "Отдел"])
    r = winstdev(m[:, "Зарплата"], by m[:, "Отдел"])

    # QUALIFY
    r = qualify(m, rownumber(m, by m[:, "Отдел"], order m[:, "Зарплата"], ZA) <= 3)

ПРАВИЛО ОКРУГЛЕНИЯ:
    Все дробные результаты округляются до 4 знаков после запятой.
"""

from ..base import Node
from runtime.matrix import MatrExMatrix
from errors import ArrayVatorError


# ============================================================
# ХЕЛПЕРЫ
# ============================================================
def _is_duckdb(val):
    try:
        from duckdb_engine import DuckDBTable
        return isinstance(val, DuckDBTable)
    except ImportError:
        return False


def _resolve_column_index(matrix_obj, col_node, env):
    """Возвращает 0-based индекс столбца."""
    from ..utils.index_utils import resolve_column_index

    if hasattr(col_node, 'indices') and len(col_node.indices) == 2:
        col_spec = col_node.indices[1]
    else:
        col_spec = col_node

    if hasattr(col_spec, 'evaluate'):
        col_val = col_spec.evaluate(env)
    else:
        col_val = col_spec

    idx, _ = resolve_column_index(matrix_obj, col_val, env)
    return idx


def _resolve_column_duckdb(columns, col_node, env):
    """Возвращает имя столбца для DuckDB."""
    from .filterif import _resolve_column_for_duckdb

    if hasattr(col_node, 'indices') and len(col_node.indices) == 2:
        col_spec = col_node.indices[1]
    else:
        col_spec = col_node

    if hasattr(col_spec, 'evaluate'):
        col_val = col_spec.evaluate(env)
    else:
        col_val = col_spec

    idx = _resolve_column_for_duckdb(columns, col_val)
    if 0 <= idx < len(columns):
        return columns[idx]
    return None


def _eval_str(node, env):
    return node.evaluate(env) if hasattr(node, 'evaluate') else node


def _eval_int(node, env):
    val = node.evaluate(env) if hasattr(node, 'evaluate') else node
    if not isinstance(val, (int, float)):
        raise ArrayVatorError(
            code="WINDOW_BAD_N",
            context=None,
        )
    return int(val)


def _parse_order(order_node, env):
    """Возвращает 'az' или 'za'."""
    if order_node is None:
        return 'az'
    val = _eval_str(order_node, env)
    if isinstance(val, str):
        v = val.strip().lower()
        if v in ('az', 'za'):
            return v
    return 'az'


def _sort_key(value):
    if value is None:
        return (2, "")
    if isinstance(value, (int, float)):
        return (0, value)
    return (1, str(value))


def _make_new_table(duck_table, new_name):
    """Создаёт новый DuckDBTable с указанным view."""
    from duckdb_engine import DuckDBTable
    new_table = DuckDBTable.__new__(DuckDBTable)
    new_table.path = duck_table.path
    new_table.table_name = new_name
    new_table.con = duck_table.con
    new_table.utf8_path = duck_table.utf8_path
    new_table.is_temp = False
    new_table._tmp_path = None
    return new_table


# ============================================================
# БАЗОВЫЙ КЛАСС 1: ФУНКЦИИ НАД ТАБЛИЦЕЙ
# ============================================================
class WindowOverTable(Node):
    """
    Базовый класс для оконных функций над всей таблицей.
        rownumber, rank, denserank, percentrank, cumedist, ntile
    """

    func_name = "window"
    sql_func = None

    def __init__(self, table, by=None, order=None,
                 direction=None, frame=None, **kwargs):
        self.table = table
        self.by = by
        self.order = order
        self.direction = direction
        self.frame = frame
        self.extra = kwargs

    def evaluate(self, env):
        table_obj = (self.table.evaluate(env)
                     if hasattr(self.table, 'evaluate')
                     else self.table)

        if _is_duckdb(table_obj):
            return self._evaluate_duckdb(table_obj, env)

        if not hasattr(table_obj, 'data') or not table_obj.is_2d:
            raise ArrayVatorError(
                code="WINDOW_NEED_TABLE",
                context=None,
            )

        return self._evaluate_matrix(table_obj, env)

    # ------------------------------------------------------------
    # MATRIX
    # ------------------------------------------------------------
    def _evaluate_matrix(self, matrix_obj, env):
        raise NotImplementedError

    # ------------------------------------------------------------
    # DUCKDB
    # ------------------------------------------------------------
    def _evaluate_duckdb(self, duck_table, env):
        raise NotImplementedError

    # ------------------------------------------------------------
    # ХЕЛПЕРЫ ДЛЯ MATRIX
    # ------------------------------------------------------------
    def _get_partitions(self, matrix_obj, env):
        if self.by is None:
            return [((), list(range(1, matrix_obj.rows)))]

        by_indices = self._resolve_by_columns(matrix_obj, env)

        groups = {}
        order = []
        for i in range(1, matrix_obj.rows):
            row = matrix_obj.data[i]
            key = tuple(
                row[idx] if idx < len(row) else None
                for idx in by_indices
            )
            if key not in groups:
                groups[key] = []
                order.append(key)
            groups[key].append(i)

        return [(k, groups[k]) for k in order]

    def _resolve_by_columns(self, matrix_obj, env):
        if self.by is None:
            return []
        by_nodes = self.by if isinstance(self.by, list) else [self.by]
        return [_resolve_column_index(matrix_obj, n, env) for n in by_nodes]

    def _resolve_order_column(self, matrix_obj, env):
        if self.order is None:
            return None
        return _resolve_column_index(matrix_obj, self.order, env)

    def _sort_partition(self, rows, matrix_obj, order_idx, direction):
        reverse = (direction == 'za')
        if order_idx is None:
            return sorted(rows)
        return sorted(
            rows,
            key=lambda i: _sort_key(
                matrix_obj.data[i][order_idx]
                if order_idx < len(matrix_obj.data[i]) else None
            ),
            reverse=reverse,
        )

    def _build_result(self, matrix_obj, row_values):
        result = [list(matrix_obj.data[0])]

        n_new = 0
        for v in row_values.values():
            if isinstance(v, list):
                n_new = max(n_new, len(v))
            else:
                n_new = max(n_new, 1)

        header = list(matrix_obj.data[0])
        for k in range(n_new):
            header.append(f"__{self.func_name}")
        result[0] = header

        for i in range(1, matrix_obj.rows):
            row = list(matrix_obj.data[i])
            vals = row_values.get(i, None)
            if vals is None:
                vals = [None] * n_new
            elif not isinstance(vals, list):
                vals = [vals]
            while len(vals) < n_new:
                vals.append(None)
            result.append(row + vals)

        return MatrExMatrix(result, True)

    # ------------------------------------------------------------
    # ХЕЛПЕРЫ ДЛЯ DUCKDB
    # ------------------------------------------------------------
    def _build_over_sql(self, duck_table, env, columns):
        parts = []

        if self.by is not None:
            by_nodes = self.by if isinstance(self.by, list) else [self.by]
            by_cols = []
            for node in by_nodes:
                col = _resolve_column_duckdb(columns, node, env)
                if col:
                    safe = '"' + str(col).replace('"', '""') + '"'
                    by_cols.append(safe)
            if by_cols:
                parts.append("PARTITION BY " + ", ".join(by_cols))

        if self.order is not None:
            col = _resolve_column_duckdb(columns, self.order, env)
            if col:
                safe = '"' + str(col).replace('"', '""') + '"'
                direction = _parse_order(self.direction, env)
                sql_dir = "ASC" if direction == 'az' else "DESC"
                parts.append(f"ORDER BY {safe} {sql_dir}")

        if not parts:
            return "OVER ()"

        return "OVER (" + " ".join(parts) + ")"

    def __repr__(self):
        return f"{self.func_name}(...)"


# ============================================================
# ROWNUMBER
# ============================================================
class RowNumberNode(WindowOverTable):
    func_name = "rownumber"
    sql_func = "ROW_NUMBER"

    def _evaluate_matrix(self, matrix_obj, env):
        order_idx = self._resolve_order_column(matrix_obj, env)
        direction = _parse_order(self.direction, env)
        partitions = self._get_partitions(matrix_obj, env)

        row_values = {}
        for _, rows in partitions:
            sorted_rows = self._sort_partition(rows, matrix_obj, order_idx, direction)
            for n, i in enumerate(sorted_rows, 1):
                row_values[i] = n

        return self._build_result(matrix_obj, row_values)

    def _evaluate_duckdb(self, duck_table, env):
        import uuid
        columns = duck_table.get_columns()
        over_sql = self._build_over_sql(duck_table, env, columns)

        new_name = f"wn_{uuid.uuid4().hex[:8]}"
        sql = f"""
            CREATE OR REPLACE VIEW {new_name} AS
            SELECT *,
                   ROW_NUMBER() {over_sql} AS "__rownumber"
            FROM {duck_table.table_name}
        """
        try:
            duck_table.con.execute(sql)
        except Exception as e:
            raise RuntimeError(f"Ошибка rownumber: {e}\nSQL: {sql}")

        return _make_new_table(duck_table, new_name)


# ============================================================
# RANK
# ============================================================
class RankNode(WindowOverTable):
    func_name = "rank"
    sql_func = "RANK"

    def _evaluate_matrix(self, matrix_obj, env):
        order_idx = self._resolve_order_column(matrix_obj, env)
        direction = _parse_order(self.direction, env)
        partitions = self._get_partitions(matrix_obj, env)

        row_values = {}
        for _, rows in partitions:
            sorted_rows = self._sort_partition(rows, matrix_obj, order_idx, direction)

            prev_val = None
            prev_rank = 0
            for n, i in enumerate(sorted_rows, 1):
                val = (matrix_obj.data[i][order_idx]
                       if order_idx is not None and order_idx < len(matrix_obj.data[i])
                       else None)
                if prev_val is None or _sort_key(val) != _sort_key(prev_val):
                    rank = n
                    prev_rank = n
                else:
                    rank = prev_rank
                prev_val = val
                row_values[i] = rank

        return self._build_result(matrix_obj, row_values)

    def _evaluate_duckdb(self, duck_table, env):
        import uuid
        columns = duck_table.get_columns()
        over_sql = self._build_over_sql(duck_table, env, columns)

        new_name = f"wn_{uuid.uuid4().hex[:8]}"
        sql = f"""
            CREATE OR REPLACE VIEW {new_name} AS
            SELECT *,
                   RANK() {over_sql} AS "__rank"
            FROM {duck_table.table_name}
        """
        try:
            duck_table.con.execute(sql)
        except Exception as e:
            raise RuntimeError(f"Ошибка rank: {e}\nSQL: {sql}")

        return _make_new_table(duck_table, new_name)


# ============================================================
# DENSERANK
# ============================================================
class DenseRankNode(WindowOverTable):
    func_name = "denserank"
    sql_func = "DENSE_RANK"

    def _evaluate_matrix(self, matrix_obj, env):
        order_idx = self._resolve_order_column(matrix_obj, env)
        direction = _parse_order(self.direction, env)
        partitions = self._get_partitions(matrix_obj, env)

        row_values = {}
        for _, rows in partitions:
            sorted_rows = self._sort_partition(rows, matrix_obj, order_idx, direction)

            prev_val = None
            rank = 0
            for i in sorted_rows:
                val = (matrix_obj.data[i][order_idx]
                       if order_idx is not None and order_idx < len(matrix_obj.data[i])
                       else None)
                if prev_val is None or _sort_key(val) != _sort_key(prev_val):
                    rank += 1
                    prev_val = val
                row_values[i] = rank

        return self._build_result(matrix_obj, row_values)

    def _evaluate_duckdb(self, duck_table, env):
        import uuid
        columns = duck_table.get_columns()
        over_sql = self._build_over_sql(duck_table, env, columns)

        new_name = f"wn_{uuid.uuid4().hex[:8]}"
        sql = f"""
            CREATE OR REPLACE VIEW {new_name} AS
            SELECT *,
                   DENSE_RANK() {over_sql} AS "__denserank"
            FROM {duck_table.table_name}
        """
        try:
            duck_table.con.execute(sql)
        except Exception as e:
            raise RuntimeError(f"Ошибка denserank: {e}\nSQL: {sql}")

        return _make_new_table(duck_table, new_name)


# ============================================================
# PERCENTRANK
# ============================================================
class PercentRankNode(WindowOverTable):
    func_name = "percentrank"
    sql_func = "PERCENT_RANK"

    def _evaluate_matrix(self, matrix_obj, env):
        order_idx = self._resolve_order_column(matrix_obj, env)
        direction = _parse_order(self.direction, env)
        partitions = self._get_partitions(matrix_obj, env)

        row_values = {}
        for _, rows in partitions:
            sorted_rows = self._sort_partition(rows, matrix_obj, order_idx, direction)
            n = len(sorted_rows)
            if n == 0:
                continue

            prev_val = None
            prev_rank = 0
            for pos, i in enumerate(sorted_rows, 1):
                val = (matrix_obj.data[i][order_idx]
                       if order_idx is not None and order_idx < len(matrix_obj.data[i])
                       else None)
                if prev_val is None or _sort_key(val) != _sort_key(prev_val):
                    rank = pos
                    prev_rank = pos
                else:
                    rank = prev_rank
                prev_val = val

                if n == 1:
                    row_values[i] = 0.0
                else:
                    row_values[i] = round((rank - 1) / (n - 1), 4)

        return self._build_result(matrix_obj, row_values)

    def _evaluate_duckdb(self, duck_table, env):
        import uuid
        columns = duck_table.get_columns()
        over_sql = self._build_over_sql(duck_table, env, columns)

        new_name = f"wn_{uuid.uuid4().hex[:8]}"
        sql = f"""
            CREATE OR REPLACE VIEW {new_name} AS
            SELECT *,
                   ROUND(PERCENT_RANK() {over_sql}, 4) AS "__percentrank"
            FROM {duck_table.table_name}
        """
        try:
            duck_table.con.execute(sql)
        except Exception as e:
            raise RuntimeError(f"Ошибка percentrank: {e}\nSQL: {sql}")

        return _make_new_table(duck_table, new_name)


# ============================================================
# CUMEDIST
# ============================================================
class CumeDistNode(WindowOverTable):
    func_name = "cumedist"
    sql_func = "CUME_DIST"

    def _evaluate_matrix(self, matrix_obj, env):
        order_idx = self._resolve_order_column(matrix_obj, env)
        direction = _parse_order(self.direction, env)
        partitions = self._get_partitions(matrix_obj, env)

        row_values = {}
        for _, rows in partitions:
            sorted_rows = self._sort_partition(rows, matrix_obj, order_idx, direction)
            n = len(sorted_rows)
            if n == 0:
                continue

            for i in sorted_rows:
                val = (matrix_obj.data[i][order_idx]
                       if order_idx is not None and order_idx < len(matrix_obj.data[i])
                       else None)
                count_le = sum(
                    1 for j in sorted_rows
                    if _sort_key(matrix_obj.data[j][order_idx]
                                 if order_idx is not None and order_idx < len(matrix_obj.data[j])
                                 else None) <= _sort_key(val)
                )
                row_values[i] = round(count_le / n, 4)

        return self._build_result(matrix_obj, row_values)

    def _evaluate_duckdb(self, duck_table, env):
        import uuid
        columns = duck_table.get_columns()
        over_sql = self._build_over_sql(duck_table, env, columns)

        new_name = f"wn_{uuid.uuid4().hex[:8]}"
        sql = f"""
            CREATE OR REPLACE VIEW {new_name} AS
            SELECT *,
                   ROUND(CUME_DIST() {over_sql}, 4) AS "__cumedist"
            FROM {duck_table.table_name}
        """
        try:
            duck_table.con.execute(sql)
        except Exception as e:
            raise RuntimeError(f"Ошибка cumedist: {e}\nSQL: {sql}")

        return _make_new_table(duck_table, new_name)


# ============================================================
# NTILE
# ============================================================
class NTileNode(WindowOverTable):
    func_name = "ntile"
    sql_func = "NTILE"

    def __init__(self, table, n, by=None, order=None,
                 direction=None, frame=None, **kwargs):
        super().__init__(table, by=by, order=order,
                         direction=direction, frame=frame, **kwargs)
        self.n = n

    def _evaluate_matrix(self, matrix_obj, env):
        n = _eval_int(self.n, env)
        if n < 1:
            raise ArrayVatorError(
                code="WINDOW_BAD_N",
                context=None,
            )

        order_idx = self._resolve_order_column(matrix_obj, env)
        direction = _parse_order(self.direction, env)
        partitions = self._get_partitions(matrix_obj, env)

        row_values = {}
        for _, rows in partitions:
            sorted_rows = self._sort_partition(rows, matrix_obj, order_idx, direction)
            total = len(sorted_rows)
            if total == 0:
                continue

            base = total // n
            remainder = total % n
            pos = 0
            for bucket in range(1, n + 1):
                size = base + (1 if bucket <= remainder else 0)
                for _ in range(size):
                    if pos < total:
                        row_values[sorted_rows[pos]] = bucket
                        pos += 1

        return self._build_result(matrix_obj, row_values)

    def _evaluate_duckdb(self, duck_table, env):
        import uuid
        columns = duck_table.get_columns()
        n = _eval_int(self.n, env)
        over_sql = self._build_over_sql(duck_table, env, columns)

        new_name = f"wn_{uuid.uuid4().hex[:8]}"
        sql = f"""
            CREATE OR REPLACE VIEW {new_name} AS
            SELECT *,
                   NTILE({n}) {over_sql} AS "__ntile"
            FROM {duck_table.table_name}
        """
        try:
            duck_table.con.execute(sql)
        except Exception as e:
            raise RuntimeError(f"Ошибка ntile: {e}\nSQL: {sql}")

        return _make_new_table(duck_table, new_name)


# ============================================================
# БАЗОВЫЙ КЛАСС 2: ФУНКЦИИ НАД СТОЛБЦОМ
# ============================================================
class WindowOverColumn(Node):
    """
    Базовый класс для оконных функций над столбцом (срез m[:, "X"]).
        lag, lead, firstvalue, lastvalue, nthvalue,
        winsum, winavg, wincount, winmin, winmax, winmedian, winstdev
    """

    func_name = "window"
    sql_func = None

    def __init__(self, value, by=None, order=None,
                 direction=None, frame=None, **kwargs):
        self.value = value
        self.by = by
        self.order = order
        self.direction = direction
        self.frame = frame
        self.extra = kwargs

    def evaluate(self, env):
        from ast_nodes.index import IndexNode

        if not isinstance(self.value, IndexNode):
            raise ArrayVatorError(
                code="WINDOW_NEED_SLICE",
                context=None,
            )

        matrix_obj = self.value.matrix.evaluate(env)

        if _is_duckdb(matrix_obj):
            return self._evaluate_duckdb(matrix_obj, env)

        if not hasattr(matrix_obj, 'data') or not matrix_obj.is_2d:
            raise ArrayVatorError(
                code="WINDOW_NEED_TABLE",
                context=None,
            )

        return self._evaluate_matrix(matrix_obj, env)

    # ------------------------------------------------------------
    # MATRIX
    # ------------------------------------------------------------
    def _evaluate_matrix(self, matrix_obj, env):
        raise NotImplementedError

    # ------------------------------------------------------------
    # DUCKDB
    # ------------------------------------------------------------
    def _evaluate_duckdb(self, duck_table, env):
        raise NotImplementedError

    # ------------------------------------------------------------
    # ХЕЛПЕРЫ
    # ------------------------------------------------------------
    def _get_partitions(self, matrix_obj, env):
        if self.by is None:
            return [((), list(range(1, matrix_obj.rows)))]

        by_indices = self._resolve_by_columns(matrix_obj, env)

        groups = {}
        order = []
        for i in range(1, matrix_obj.rows):
            row = matrix_obj.data[i]
            key = tuple(
                row[idx] if idx < len(row) else None
                for idx in by_indices
            )
            if key not in groups:
                groups[key] = []
                order.append(key)
            groups[key].append(i)

        return [(k, groups[k]) for k in order]

    def _resolve_by_columns(self, matrix_obj, env):
        if self.by is None:
            return []
        by_nodes = self.by if isinstance(self.by, list) else [self.by]
        return [_resolve_column_index(matrix_obj, n, env) for n in by_nodes]

    def _resolve_value_column(self, matrix_obj, env):
        if self.value is None:
            return None
        return _resolve_column_index(matrix_obj, self.value, env)

    def _resolve_order_column(self, matrix_obj, env):
        if self.order is None:
            return None
        return _resolve_column_index(matrix_obj, self.order, env)

    def _sort_partition(self, rows, matrix_obj, order_idx, direction):
        reverse = (direction == 'za')
        if order_idx is None:
            return sorted(rows)
        return sorted(
            rows,
            key=lambda i: _sort_key(
                matrix_obj.data[i][order_idx]
                if order_idx < len(matrix_obj.data[i]) else None
            ),
            reverse=reverse,
        )

    def _build_result(self, matrix_obj, row_values):
        result = [list(matrix_obj.data[0])]

        n_new = 0
        for v in row_values.values():
            if isinstance(v, list):
                n_new = max(n_new, len(v))
            else:
                n_new = max(n_new, 1)

        header = list(matrix_obj.data[0])
        for k in range(n_new):
            header.append(f"__{self.func_name}")
        result[0] = header

        for i in range(1, matrix_obj.rows):
            row = list(matrix_obj.data[i])
            vals = row_values.get(i, None)
            if vals is None:
                vals = [None] * n_new
            elif not isinstance(vals, list):
                vals = [vals]
            while len(vals) < n_new:
                vals.append(None)
            result.append(row + vals)

        return MatrExMatrix(result, True)

    def _build_over_sql(self, duck_table, env, columns):
        parts = []

        if self.by is not None:
            by_nodes = self.by if isinstance(self.by, list) else [self.by]
            by_cols = []
            for node in by_nodes:
                col = _resolve_column_duckdb(columns, node, env)
                if col:
                    safe = '"' + str(col).replace('"', '""') + '"'
                    by_cols.append(safe)
            if by_cols:
                parts.append("PARTITION BY " + ", ".join(by_cols))

        if self.order is not None:
            col = _resolve_column_duckdb(columns, self.order, env)
            if col:
                safe = '"' + str(col).replace('"', '""') + '"'
                direction = _parse_order(self.direction, env)
                sql_dir = "ASC" if direction == 'az' else "DESC"
                parts.append(f"ORDER BY {safe} {sql_dir}")

        if not parts:
            return "OVER ()"

        return "OVER (" + " ".join(parts) + ")"

    def __repr__(self):
        return f"{self.func_name}(...)"


# ============================================================
# LAG / LEAD
# ============================================================
class LagNode(WindowOverColumn):
    func_name = "lag"
    sql_func = "LAG"

    def __init__(self, value, offset=None, default=None,
                 by=None, order=None, direction=None, frame=None, **kwargs):
        super().__init__(value, by=by, order=order,
                         direction=direction, frame=frame, **kwargs)
        self.offset = offset
        self.default = default

    def _evaluate_matrix(self, matrix_obj, env):
        val_idx = self._resolve_value_column(matrix_obj, env)
        order_idx = self._resolve_order_column(matrix_obj, env)
        direction = _parse_order(self.direction, env)
        offset = _eval_int(self.offset, env) if self.offset is not None else 1
        default = (_eval_str(self.default, env)
                   if self.default is not None else None)
        partitions = self._get_partitions(matrix_obj, env)

        shift = -offset if self.sql_func == "LAG" else offset

        row_values = {}
        for _, rows in partitions:
            sorted_rows = self._sort_partition(rows, matrix_obj, order_idx, direction)
            for pos, i in enumerate(sorted_rows):
                src = pos + shift
                if 0 <= src < len(sorted_rows):
                    src_row = sorted_rows[src]
                    val = (matrix_obj.data[src_row][val_idx]
                           if val_idx is not None and val_idx < len(matrix_obj.data[src_row])
                           else None)
                    row_values[i] = val
                else:
                    row_values[i] = default

        return self._build_result(matrix_obj, row_values)

    def _evaluate_duckdb(self, duck_table, env):
        import uuid
        columns = duck_table.get_columns()

        col = _resolve_column_duckdb(columns, self.value, env)
        if col is None:
            raise ArrayVatorError(
                code="WINDOW_NEED_SLICE",
                context=None,
            )
        safe = '"' + str(col).replace('"', '""') + '"'

        args = [safe]
        if self.offset is not None:
            args.append(str(_eval_int(self.offset, env)))
        if self.default is not None:
            default_val = _eval_str(self.default, env)
            if isinstance(default_val, str):
                args.append("'" + default_val.replace("'", "''") + "'")
            elif default_val is None:
                args.append("NULL")
            else:
                args.append(str(default_val))

        over_sql = self._build_over_sql(duck_table, env, columns)

        new_name = f"wn_{uuid.uuid4().hex[:8]}"
        sql = f"""
            CREATE OR REPLACE VIEW {new_name} AS
            SELECT *,
                   {self.sql_func}({', '.join(args)}) {over_sql}
                       AS "__{self.func_name}"
            FROM {duck_table.table_name}
        """
        try:
            duck_table.con.execute(sql)
        except Exception as e:
            raise RuntimeError(f"Ошибка {self.func_name}: {e}\nSQL: {sql}")

        return _make_new_table(duck_table, new_name)


class LeadNode(LagNode):
    func_name = "lead"
    sql_func = "LEAD"


# ============================================================
# FIRSTVALUE / LASTVALUE / NTHVALUE
# ============================================================
class FirstValueNode(WindowOverColumn):
    func_name = "firstvalue"
    sql_func = "FIRST_VALUE"

    def _evaluate_matrix(self, matrix_obj, env):
        val_idx = self._resolve_value_column(matrix_obj, env)
        order_idx = self._resolve_order_column(matrix_obj, env)
        direction = _parse_order(self.direction, env)
        partitions = self._get_partitions(matrix_obj, env)

        row_values = {}
        for _, rows in partitions:
            sorted_rows = self._sort_partition(rows, matrix_obj, order_idx, direction)
            if not sorted_rows:
                continue
            first = sorted_rows[0]
            first_val = (matrix_obj.data[first][val_idx]
                         if val_idx is not None and val_idx < len(matrix_obj.data[first])
                         else None)
            for i in sorted_rows:
                row_values[i] = first_val

        return self._build_result(matrix_obj, row_values)

    def _evaluate_duckdb(self, duck_table, env):
        import uuid
        columns = duck_table.get_columns()
        col = _resolve_column_duckdb(columns, self.value, env)
        safe = '"' + str(col).replace('"', '""') + '"'
        over_sql = self._build_over_sql(duck_table, env, columns)

        if "ROWS" not in over_sql and "RANGE" not in over_sql:
            over_sql = over_sql[:-1] + \
                " ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING)"

        new_name = f"wn_{uuid.uuid4().hex[:8]}"
        sql = f"""
            CREATE OR REPLACE VIEW {new_name} AS
            SELECT *,
                   FIRST_VALUE({safe}) {over_sql} AS "__firstvalue"
            FROM {duck_table.table_name}
        """
        try:
            duck_table.con.execute(sql)
        except Exception as e:
            raise RuntimeError(f"Ошибка firstvalue: {e}\nSQL: {sql}")

        return _make_new_table(duck_table, new_name)


class LastValueNode(FirstValueNode):
    func_name = "lastvalue"
    sql_func = "LAST_VALUE"

    def _evaluate_matrix(self, matrix_obj, env):
        val_idx = self._resolve_value_column(matrix_obj, env)
        order_idx = self._resolve_order_column(matrix_obj, env)
        direction = _parse_order(self.direction, env)
        partitions = self._get_partitions(matrix_obj, env)

        row_values = {}
        for _, rows in partitions:
            sorted_rows = self._sort_partition(rows, matrix_obj, order_idx, direction)
            if not sorted_rows:
                continue
            last = sorted_rows[-1]
            last_val = (matrix_obj.data[last][val_idx]
                        if val_idx is not None and val_idx < len(matrix_obj.data[last])
                        else None)
            for i in sorted_rows:
                row_values[i] = last_val

        return self._build_result(matrix_obj, row_values)

    def _evaluate_duckdb(self, duck_table, env):
        import uuid
        columns = duck_table.get_columns()
        col = _resolve_column_duckdb(columns, self.value, env)
        safe = '"' + str(col).replace('"', '""') + '"'
        over_sql = self._build_over_sql(duck_table, env, columns)

        if "ROWS" not in over_sql and "RANGE" not in over_sql:
            over_sql = over_sql[:-1] + \
                " ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING)"

        new_name = f"wn_{uuid.uuid4().hex[:8]}"
        sql = f"""
            CREATE OR REPLACE VIEW {new_name} AS
            SELECT *,
                   LAST_VALUE({safe}) {over_sql} AS "__lastvalue"
            FROM {duck_table.table_name}
        """
        try:
            duck_table.con.execute(sql)
        except Exception as e:
            raise RuntimeError(f"Ошибка lastvalue: {e}\nSQL: {sql}")

        return _make_new_table(duck_table, new_name)


class NthValueNode(FirstValueNode):
    func_name = "nthvalue"
    sql_func = "NTH_VALUE"

    def __init__(self, value, n, by=None, order=None,
                 direction=None, frame=None, **kwargs):
        super().__init__(value, by=by, order=order,
                         direction=direction, frame=frame, **kwargs)
        self.n = n

    def _evaluate_matrix(self, matrix_obj, env):
        val_idx = self._resolve_value_column(matrix_obj, env)
        order_idx = self._resolve_order_column(matrix_obj, env)
        direction = _parse_order(self.direction, env)
        n = _eval_int(self.n, env)
        partitions = self._get_partitions(matrix_obj, env)

        row_values = {}
        for _, rows in partitions:
            sorted_rows = self._sort_partition(rows, matrix_obj, order_idx, direction)
            nth_val = None
            if 1 <= n <= len(sorted_rows):
                nth_row = sorted_rows[n - 1]
                nth_val = (matrix_obj.data[nth_row][val_idx]
                           if val_idx is not None and val_idx < len(matrix_obj.data[nth_row])
                           else None)
            for i in sorted_rows:
                row_values[i] = nth_val

        return self._build_result(matrix_obj, row_values)

    def _evaluate_duckdb(self, duck_table, env):
        import uuid
        columns = duck_table.get_columns()
        col = _resolve_column_duckdb(columns, self.value, env)
        safe = '"' + str(col).replace('"', '""') + '"'
        n = _eval_int(self.n, env)
        over_sql = self._build_over_sql(duck_table, env, columns)

        if "ROWS" not in over_sql and "RANGE" not in over_sql:
            over_sql = over_sql[:-1] + \
                " ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING)"

        new_name = f"wn_{uuid.uuid4().hex[:8]}"
        sql = f"""
            CREATE OR REPLACE VIEW {new_name} AS
            SELECT *,
                   NTH_VALUE({safe}, {n}) {over_sql} AS "__nthvalue"
            FROM {duck_table.table_name}
        """
        try:
            duck_table.con.execute(sql)
        except Exception as e:
            raise RuntimeError(f"Ошибка nthvalue: {e}\nSQL: {sql}")

        return _make_new_table(duck_table, new_name)


# ============================================================
# ОКОННЫЕ АГРЕГАТЫ
# ============================================================
class WinAggBase(WindowOverColumn):
    sql_func = "SUM"

    def _evaluate_matrix(self, matrix_obj, env):
        val_idx = self._resolve_value_column(matrix_obj, env)
        order_idx = self._resolve_order_column(matrix_obj, env)
        direction = _parse_order(self.direction, env)
        partitions = self._get_partitions(matrix_obj, env)

        row_values = {}
        for _, rows in partitions:
            sorted_rows = self._sort_partition(rows, matrix_obj, order_idx, direction)

            values = []
            for i in sorted_rows:
                v = (matrix_obj.data[i][val_idx]
                     if val_idx is not None and val_idx < len(matrix_obj.data[i])
                     else None)
                values.append(v)

            for pos, i in enumerate(sorted_rows):
                window_vals = values[:pos + 1]
                row_values[i] = self._apply_agg(window_vals)

        return self._build_result(matrix_obj, row_values)

    def _apply_agg(self, values):
        nums = [v for v in values if isinstance(v, (int, float))
                and not isinstance(v, bool)]

        if self.sql_func == 'COUNT':
            return len([v for v in values if v is not None])

        if not nums:
            return None

        if self.sql_func == 'SUM':
            return sum(nums)
        if self.sql_func == 'AVG':
            return round(sum(nums) / len(nums), 4)
        if self.sql_func == 'MIN':
            return min(nums)
        if self.sql_func == 'MAX':
            return max(nums)
        if self.sql_func == 'MEDIAN':
            s = sorted(nums)
            n = len(s)
            if n % 2 == 1:
                return s[n // 2]
            return round((s[n // 2 - 1] + s[n // 2]) / 2, 4)
        if self.sql_func in ('STDDEV', 'STDDEV_POP'):
            mean = sum(nums) / len(nums)
            var = sum((x - mean) ** 2 for x in nums) / len(nums)
            return round(var ** 0.5, 4)
        return None

    def _evaluate_duckdb(self, duck_table, env):
        import uuid
        columns = duck_table.get_columns()

        col = _resolve_column_duckdb(columns, self.value, env)
        if col is None:
            raise ArrayVatorError(
                code="WINDOW_NEED_SLICE",
                context=None,
            )
        safe = '"' + str(col).replace('"', '""') + '"'

        new_name = f"wn_{uuid.uuid4().hex[:8]}"

        if self.order is None:
            over_sql = self._build_agg_over_sql(
                duck_table, env, columns, use_orig_row=True
            )
            agg_expr = self._build_agg_expr(safe, over_sql)
            sql = f"""
                CREATE OR REPLACE VIEW {new_name} AS
                SELECT * EXCLUDE (__orig_row),
                       {agg_expr} AS "__{self.func_name}"
                FROM (
                    SELECT *, ROW_NUMBER() OVER () AS __orig_row
                    FROM {duck_table.table_name}
                )
            """
        else:
            over_sql = self._build_agg_over_sql(
                duck_table, env, columns, use_orig_row=False
            )
            agg_expr = self._build_agg_expr(safe, over_sql)
            sql = f"""
                CREATE OR REPLACE VIEW {new_name} AS
                SELECT *,
                       {agg_expr} AS "__{self.func_name}"
                FROM {duck_table.table_name}
            """

        try:
            duck_table.con.execute(sql)
        except Exception as e:
            raise RuntimeError(f"Ошибка {self.func_name}: {e}\nSQL: {sql}")

        return _make_new_table(duck_table, new_name)

    def _build_agg_expr(self, safe_col, over_sql):
        if self.sql_func == 'COUNT':
            return f"COUNT({safe_col}) OVER ({over_sql})"

        agg = f"{self.sql_func}(CAST({safe_col} AS DOUBLE)) OVER ({over_sql})"
        return f"ROUND({agg}, 4)"

    def _build_agg_over_sql(self, duck_table, env, columns,
                             use_orig_row=False):
        parts = []

        if self.by is not None:
            by_nodes = self.by if isinstance(self.by, list) else [self.by]
            by_cols = []
            for node in by_nodes:
                col = _resolve_column_duckdb(columns, node, env)
                if col:
                    safe = '"' + str(col).replace('"', '""') + '"'
                    by_cols.append(safe)
            if by_cols:
                parts.append("PARTITION BY " + ", ".join(by_cols))

        if self.order is not None:
            col = _resolve_column_duckdb(columns, self.order, env)
            if col:
                safe = '"' + str(col).replace('"', '""') + '"'
                direction = _parse_order(self.direction, env)
                sql_dir = "ASC" if direction == 'az' else "DESC"
                parts.append(f"ORDER BY {safe} {sql_dir}")
        elif use_orig_row:
            parts.append("ORDER BY __orig_row")
        else:
            parts.append("ORDER BY 1")

        parts.append("ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW")

        return " ".join(parts)


class WinSumNode(WinAggBase):
    func_name = "winsum"
    sql_func = "SUM"


class WinAvgNode(WinAggBase):
    func_name = "winavg"
    sql_func = "AVG"


class WinCountNode(WinAggBase):
    func_name = "wincount"
    sql_func = "COUNT"


class WinMinNode(WinAggBase):
    func_name = "winmin"
    sql_func = "MIN"


class WinMaxNode(WinAggBase):
    func_name = "winmax"
    sql_func = "MAX"


class WinMedianNode(WinAggBase):
    func_name = "winmedian"
    sql_func = "MEDIAN"


class WinStdevNode(WinAggBase):
    func_name = "winstdev"
    sql_func = "STDDEV_POP"


# ============================================================
# QUALIFY
# ============================================================
class QualifyNode(Node):
    """
    Фильтр строк по оконной функции.

    СИНТАКСИС:
        qualify(m, rownumber(m, by m[:, "Отдел"], order m[:, "Зарплата"], ZA) <= 3)
        qualify(m, rank(m, by m[:, "Отдел"], order m[:, "Зарплата"], ZA) == 1)

    РАБОТАЕТ:
        - Matrix (RAM) — фильтрация через Python
        - DuckDB (BigData) — фильтрация через SQL
    """

    def __init__(self, table, condition):
        self.table = table
        self.condition = condition

    def evaluate(self, env):
        matrix_obj = (self.table.evaluate(env)
                      if hasattr(self.table, 'evaluate')
                      else self.table)

        # Извлекаем оконную функцию и порог
        window_result, op, threshold = self._extract_window_op(env)

        if window_result is None:
            raise ArrayVatorError(
                code="QUALIFY_NO_WINDOW",
                context=None,
            )

        # ============================================================
        # DUCKDB
        # ============================================================
        if _is_duckdb(window_result):
            return self._qualify_duckdb(window_result, op, threshold)

        # ============================================================
        # MATRIX
        # ============================================================
        if hasattr(window_result, 'data'):
            last_col_idx = window_result.cols - 1

            result = [list(window_result.data[0])]
            for i in range(1, window_result.rows):
                row = window_result.data[i]
                val = row[last_col_idx] if last_col_idx < len(row) else None
                if self._compare(val, op, threshold):
                    result.append(list(row))

            return MatrExMatrix(result, True)

        raise ArrayVatorError(
            code="QUALIFY_BAD_SYNTAX",
            context=None,
        )

    # ------------------------------------------------------------
    # DUCKDB
    # ------------------------------------------------------------
    def _qualify_duckdb(self, duck_view, op, threshold):
        """Применяет фильтр к DuckDB-окну через SQL."""
        import uuid

        columns = duck_view.get_columns()
        if not columns:
            raise ArrayVatorError(
                code="QUALIFY_BAD_SYNTAX",
                context=None,
            )

        last_col = columns[-1]

        op_sql = {
            'LESS': '<',
            'GREATER': '>',
            'LESSEQUAL': '<=',
            'GREATEREQUAL': '>=',
            'EQUALS': '=',
            'NOTEQUAL': '<>',
        }.get(op)

        if not op_sql:
            raise ArrayVatorError(
                code="QUALIFY_BAD_SYNTAX",
                context=None,
            )

        if threshold is None:
            thr_sql = "NULL"
        elif isinstance(threshold, bool):
            thr_sql = "TRUE" if threshold else "FALSE"
        elif isinstance(threshold, (int, float)):
            thr_sql = str(threshold)
        else:
            thr_sql = "'" + str(threshold).replace("'", "''") + "'"

        safe_col = '"' + str(last_col).replace('"', '""') + '"'

        new_name = f"qualify_{uuid.uuid4().hex[:8]}"
        sql = f"""
            CREATE OR REPLACE VIEW {new_name} AS
            SELECT * FROM {duck_view.table_name}
            WHERE {safe_col} {op_sql} {thr_sql}
        """

        try:
            duck_view.con.execute(sql)
        except Exception as e:
            raise RuntimeError(f"Ошибка qualify: {e}\nSQL: {sql}")

        return _make_new_table(duck_view, new_name)

    # ------------------------------------------------------------
    # ИЗВЛЕЧЕНИЕ ОКОННОЙ ФУНКЦИИ
    # ------------------------------------------------------------
    def _extract_window_op(self, env):
        from ast_nodes.operations import BinaryOp

        cond = self.condition

        if isinstance(cond, BinaryOp):
            op = cond.op
            left = cond.left
            right = cond.right

            if isinstance(left, (WindowOverTable, WindowOverColumn)):
                win_res = left.evaluate(env)
                threshold = (right.evaluate(env)
                             if hasattr(right, 'evaluate') else right)
                return win_res, op, threshold

            if isinstance(right, (WindowOverTable, WindowOverColumn)):
                win_res = right.evaluate(env)
                threshold = (left.evaluate(env)
                             if hasattr(left, 'evaluate') else left)
                return win_res, self._reverse_op(op), threshold

        return None, None, None

    def _reverse_op(self, op):
        mapping = {
            'LESS': 'GREATER',
            'GREATER': 'LESS',
            'LESSEQUAL': 'GREATEREQUAL',
            'GREATEREQUAL': 'LESSEQUAL',
            'EQUALS': 'EQUALS',
            'NOTEQUAL': 'NOTEQUAL',
        }
        return mapping.get(op, op)

    def _compare(self, a, op, b):
        try:
            if op == 'LESS':          return a < b
            if op == 'GREATER':       return a > b
            if op == 'LESSEQUAL':     return a <= b
            if op == 'GREATEREQUAL':  return a >= b
            if op == 'EQUALS':        return a == b
            if op == 'NOTEQUAL':      return a != b
        except TypeError:
            return False
        return False

    def __repr__(self):
        return f"qualify({self.table}, {self.condition})"