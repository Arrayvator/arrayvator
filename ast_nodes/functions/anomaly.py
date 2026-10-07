# ast_nodes/functions/anomaly.py
"""
Функция ANOMALY — поиск аномалий (выбросов) в числовом столбце.

СИНТАКСИС:
    anomaly(срез)
    anomaly(срез, zscore)
    anomaly(срез, zscore, 2)
    anomaly(срез, percentile)
    anomaly(срез, percentile, 5, 95)
    anomaly(срез, iqr, 3.0)
    anomaly(срез, by m[:, "Магазин"])
    anomaly(срез, by m[:, "Магазин"], iqr, 3.0)
    anomaly(срез, only)
    anomaly(срез, only, approx)
    anomaly(срез, by m[:, "Магазин"], iqr, approx, only)

МЕТОДЫ:
    iqr        — межквартильный размах (по умолчанию, k=1.5)
    zscore     — z-отклонение (N=3)
    percentile — процентили (1, 99)

РЕЗУЛЬТАТ:
    Матрица в исходном порядке строк.
    Новый столбец __anomaly справа от исходного среза:
        0  — норма
        -1 — ниже нижней границы
        1  — выше верхней границы
        None — значение None / не число / мало данных в группе (< 4)

ОПЦИИ:
    by срез   — считать аномалию внутри группы
    only      — вернуть только аномальные строки
    approx    — приблизительные процентили (DuckDB: APPROX_QUANTILE)

DUCKDB:
    - IQR, percentile → quantile_cont(...) в CTE + JOIN (без OVER в подзапросе).
    - zscore → AVG, STDDEV_POP в CTE + JOIN.
    - Порядок строк сохраняется.
    - Маленькие группы (< 4 значений) → __anomaly = NULL.
"""

import math

from ..base import Node


def _is_duckdb(val):
    try:
        from duckdb_engine import DuckDBTable
        return isinstance(val, DuckDBTable)
    except ImportError:
        return False


class AnomalyNode(Node):
    def __init__(self, data, method=None, params=None, by=None,
                 only=False, approx=False):
        self.data = data            # IndexNode — срез
        self.method = method        # None | 'iqr' | 'zscore' | 'percentile'
        self.params = params or []  # список чисел
        self.by = by                # IndexNode | None
        self.only = only
        self.approx = approx

    def evaluate(self, env):
        from ast_nodes.index import IndexNode

        if not isinstance(self.data, IndexNode):
            raise TypeError(
                "anomaly: первый аргумент — срез m[:, \"X\"].\n"
                "  Пример: anomaly(m[:, \"Сумма\"])"
            )

        matrix_obj = self.data.matrix.evaluate(env)

        # Разбор параметров
        method = self.method or 'iqr'
        params = []
        for p in self.params:
            val = p.evaluate(env) if hasattr(p, 'evaluate') else p
            if not isinstance(val, (int, float)):
                raise TypeError(f"anomaly: параметр должен быть числом, получен {type(val)}")
            params.append(float(val))

        if method == 'iqr':
            k = params[0] if params else 1.5
            method_params = {'k': k}
        elif method == 'zscore':
            n = params[0] if params else 3.0
            method_params = {'n': n}
        elif method == 'percentile':
            lo = params[0] if len(params) > 0 else 1.0
            hi = params[1] if len(params) > 1 else 99.0
            method_params = {'lo': lo, 'hi': hi}
        else:
            raise ValueError(f"anomaly: неизвестный метод '{method}'")

        # DUCKDB
        if _is_duckdb(matrix_obj):
            return self._evaluate_duckdb(matrix_obj, env, method, method_params)

        # MATRIX
        if hasattr(matrix_obj, 'data') and matrix_obj.is_2d:
            return self._evaluate_matrix(matrix_obj, env, method, method_params)

        raise TypeError("anomaly: ожидается матрица или DuckDB.")

    # ============================================================
    # MATRIX
    # ============================================================
    def _evaluate_matrix(self, matrix_obj, env, method, params):
        from ast_nodes.index import IndexNode
        from ..utils.index_utils import resolve_column_index
        from runtime.matrix import MatrExMatrix

        # Столбец значений
        col_spec_node = self.data.indices[1]
        col_spec = (col_spec_node.evaluate(env)
                    if hasattr(col_spec_node, 'evaluate')
                    else col_spec_node)
        val_col, _ = resolve_column_index(matrix_obj, col_spec, env)

        # Столбец группировки
        by_col = None
        if self.by is not None:
            if not isinstance(self.by, IndexNode):
                raise TypeError("anomaly: by — срез m[:, \"X\"].")
            by_spec_node = self.by.indices[1]
            by_spec = (by_spec_node.evaluate(env)
                       if hasattr(by_spec_node, 'evaluate')
                       else by_spec_node)
            by_col, _ = resolve_column_index(matrix_obj, by_spec, env)

        rows = matrix_obj.rows
        header = list(matrix_obj.data[0]) if rows > 0 else []

        # Собираем значения
        values = []
        groups = []
        for i in range(1, rows):
            row = matrix_obj.data[i]
            v = row[val_col] if val_col < len(row) else None
            values.append(v)
            if by_col is not None:
                g = row[by_col] if by_col < len(row) else None
            else:
                g = None
            groups.append(g)

        # Считаем __anomaly для каждой строки
        anomaly_by_row = [None] * len(values)

        # Группируем
        if by_col is None:
            group_indices = {None: list(range(len(values)))}
        else:
            group_indices = {}
            for i, g in enumerate(groups):
                group_indices.setdefault(g, []).append(i)

        for g_key, idxs in group_indices.items():
            nums = []
            for i in idxs:
                v = values[i]
                if isinstance(v, (int, float)) and not isinstance(v, bool):
                    nums.append(v)

            if len(nums) < 4:
                # Мало данных — аномалии не считаем (None)
                continue

            nums_sorted = sorted(nums)

            lo = hi = None
            if method == 'iqr':
                q1 = _percentile_linear(nums_sorted, 25)
                q3 = _percentile_linear(nums_sorted, 75)
                iqr = q3 - q1
                if iqr == 0:
                    lo = hi = None
                else:
                    k = params['k']
                    lo = q1 - k * iqr
                    hi = q3 + k * iqr
            elif method == 'zscore':
                mean = sum(nums) / len(nums)
                var = sum((x - mean) ** 2 for x in nums) / len(nums)
                sd = math.sqrt(var)
                if sd == 0:
                    lo = hi = None
                else:
                    n = params['n']
                    lo = mean - n * sd
                    hi = mean + n * sd
            elif method == 'percentile':
                lo = _percentile_linear(nums_sorted, params['lo'])
                hi = _percentile_linear(nums_sorted, params['hi'])

            for i in idxs:
                v = values[i]
                if not isinstance(v, (int, float)) or isinstance(v, bool):
                    anomaly_by_row[i] = None
                    continue
                if lo is None or hi is None:
                    anomaly_by_row[i] = 0
                elif v < lo:
                    anomaly_by_row[i] = -1
                elif v > hi:
                    anomaly_by_row[i] = 1
                else:
                    anomaly_by_row[i] = 0

        # Строим результат
        result_header = list(header)
        abc_pos = val_col + 1
        result_header.insert(abc_pos, "__anomaly")

        result_data = [result_header]
        for i in range(1, rows):
            row = list(matrix_obj.data[i])
            while len(row) < len(header):
                row.append(None)

            a = anomaly_by_row[i - 1]

            if self.only and a == 0:
                continue
            if self.only and a is None:
                continue

            row.insert(abc_pos, a)
            result_data.append(row)

        if result_data:
            max_cols = max(len(r) for r in result_data)
            for r in result_data:
                while len(r) < max_cols:
                    r.append(None)

        return MatrExMatrix(result_data, True)

    # ============================================================
    # DUCKDB
    # ============================================================
    def _evaluate_duckdb(self, duck_table, env, method, params):
        from ast_nodes.index import IndexNode
        from duckdb_engine import DuckDBTable
        from .filterif import _resolve_column_for_duckdb
        import uuid

        columns = duck_table.get_columns()

        col_spec_node = self.data.indices[1]
        col_spec = (col_spec_node.evaluate(env)
                    if hasattr(col_spec_node, 'evaluate')
                    else col_spec_node)
        val_idx = _resolve_column_for_duckdb(columns, col_spec)
        if val_idx is None or val_idx < 0 or val_idx >= len(columns):
            raise ValueError("anomaly: столбец не найден в DuckDB.")
        val_col = columns[val_idx]
        safe_val = '"' + str(val_col).replace('"', '""') + '"'

        # Группировка
        partition_cols = []
        if self.by is not None:
            if not isinstance(self.by, IndexNode):
                raise TypeError("anomaly: by — срез m[:, \"X\"].")
            by_spec_node = self.by.indices[1]
            by_spec = (by_spec_node.evaluate(env)
                       if hasattr(by_spec_node, 'evaluate')
                       else by_spec_node)
            by_idx = _resolve_column_for_duckdb(columns, by_spec)
            if by_idx is None or by_idx < 0 or by_idx >= len(columns):
                raise ValueError("anomaly: столбец группировки не найден.")
            by_col = columns[by_idx]
            safe_by = '"' + str(by_col).replace('"', '""') + '"'
            partition_cols = [safe_by]

        # ============================================================
        # Проверка «мало данных» — как в Matrix
        # ============================================================
        # Если без группировки: считаем общее число непустых числовых.
        # Если с группировкой: проверяем МИНИМУМ по группам.
        # Если в какой-то группе < 4 — для этой группы __anomaly = NULL.
        # ============================================================
        min_count = 4

        if not partition_cols:
            # Одна группа
            check_sql = (
                f"SELECT COUNT(*) FROM {duck_table.table_name} "
                f"WHERE {safe_val} IS NOT NULL "
                f"AND TRY_CAST({safe_val} AS DOUBLE) IS NOT NULL"
            )
            try:
                cnt = duck_table.con.execute(check_sql).fetchone()[0]
            except Exception:
                cnt = 0

            if cnt < min_count:
                # Мало данных — вернуть таблицу с __anomaly = NULL
                return self._empty_result(duck_table, columns, val_idx)
        else:
            # Проверяем каждую группу отдельно через HAVING
            group_by = ", ".join(partition_cols)
            check_sql = (
                f"SELECT {group_by}, COUNT(*) AS __cnt "
                f"FROM {duck_table.table_name} "
                f"WHERE {safe_val} IS NOT NULL "
                f"AND TRY_CAST({safe_val} AS DOUBLE) IS NOT NULL "
                f"GROUP BY {group_by} "
                f"HAVING COUNT(*) < {min_count}"
            )
            try:
                small_groups = duck_table.con.execute(check_sql).fetchall()
            except Exception:
                small_groups = []

            if small_groups:
                # Есть маленькие группы → строим результат
                # со специальной обработкой
                return self._evaluate_duckdb_with_small_groups(
                    duck_table, env, method, params,
                    columns, val_idx, safe_val,
                    partition_cols, small_groups
                )

        # ============================================================
        # ОСНОВНОЙ ПУТЬ: все группы >= 4
        # ============================================================
        agg_exprs = []
        join_cond = ""

        if method == 'iqr':
            k = params['k']
            if self.approx:
                agg_exprs.append(f"APPROX_QUANTILE(CAST({safe_val} AS DOUBLE), 0.25) AS __q1")
                agg_exprs.append(f"APPROX_QUANTILE(CAST({safe_val} AS DOUBLE), 0.75) AS __q3")
            else:
                agg_exprs.append(f"QUANTILE_CONT(CAST({safe_val} AS DOUBLE), 0.25) AS __q1")
                agg_exprs.append(f"QUANTILE_CONT(CAST({safe_val} AS DOUBLE), 0.75) AS __q3")
        elif method == 'zscore':
            agg_exprs.append(f"AVG(CAST({safe_val} AS DOUBLE)) AS __mean")
            agg_exprs.append(f"STDDEV_POP(CAST({safe_val} AS DOUBLE)) AS __sd")
        elif method == 'percentile':
            lo_p = params['lo'] / 100.0
            hi_p = params['hi'] / 100.0
            if self.approx:
                agg_exprs.append(f"APPROX_QUANTILE(CAST({safe_val} AS DOUBLE), {lo_p}) AS __lo")
                agg_exprs.append(f"APPROX_QUANTILE(CAST({safe_val} AS DOUBLE), {hi_p}) AS __hi")
            else:
                agg_exprs.append(f"QUANTILE_CONT(CAST({safe_val} AS DOUBLE), {lo_p}) AS __lo")
                agg_exprs.append(f"QUANTILE_CONT(CAST({safe_val} AS DOUBLE), {hi_p}) AS __hi")

        if partition_cols:
            group_by = ", ".join(partition_cols)
            select_cols = ", ".join(partition_cols + agg_exprs)
            cte_sql = (
                f"WITH __stats AS ("
                f"SELECT {select_cols} "
                f"FROM {duck_table.table_name} "
                f"GROUP BY {group_by})"
            )
            join_cond = " AND ".join(
                f"t.{c} = s.{c}" for c in partition_cols
            )
        else:
            cte_sql = (
                f"WITH __stats AS ("
                f"SELECT {', '.join(agg_exprs)} "
                f"FROM {duck_table.table_name})"
            )
            join_cond = "1=1"

        if method == 'iqr':
            k = params['k']
            anomaly_cond = (
                f"CASE "
                f"WHEN CAST(t.{safe_val} AS DOUBLE) < s.__q1 - {k} * (s.__q3 - s.__q1) THEN -1 "
                f"WHEN CAST(t.{safe_val} AS DOUBLE) > s.__q3 + {k} * (s.__q3 - s.__q1) THEN 1 "
                f"ELSE 0 END"
            )
        elif method == 'zscore':
            n = params['n']
            anomaly_cond = (
                f"CASE "
                f"WHEN CAST(t.{safe_val} AS DOUBLE) < s.__mean - {n} * s.__sd THEN -1 "
                f"WHEN CAST(t.{safe_val} AS DOUBLE) > s.__mean + {n} * s.__sd THEN 1 "
                f"ELSE 0 END"
            )
        elif method == 'percentile':
            anomaly_cond = (
                f"CASE "
                f"WHEN CAST(t.{safe_val} AS DOUBLE) < s.__lo THEN -1 "
                f"WHEN CAST(t.{safe_val} AS DOUBLE) > s.__hi THEN 1 "
                f"ELSE 0 END"
            )
        else:
            raise ValueError(f"anomaly: неизвестный метод '{method}'")

        select_parts = []
        for i, c in enumerate(columns):
            esc = '"' + str(c).replace('"', '""') + '"'
            select_parts.append(f"t.{esc}")
            if i == val_idx:
                select_parts.append(f'{anomaly_cond} AS "__anomaly"')

        if partition_cols:
            inner_sql = (
                f"{cte_sql} "
                f"SELECT {', '.join(select_parts)} "
                f"FROM {duck_table.table_name} AS t "
                f"JOIN __stats AS s ON {join_cond}"
            )
        else:
            inner_sql = (
                f"{cte_sql} "
                f"SELECT {', '.join(select_parts)} "
                f"FROM {duck_table.table_name} AS t "
                f"CROSS JOIN __stats AS s"
            )

        if self.only:
            inner_sql = (
                f"SELECT * FROM ({inner_sql}) WHERE __anomaly <> 0"
            )

        new_name = f"anomaly_{uuid.uuid4().hex[:8]}"
        try:
            duck_table.con.execute(
                f'CREATE OR REPLACE VIEW {new_name} AS {inner_sql}'
            )
        except Exception as e:
            raise RuntimeError(f"anomaly: ошибка DuckDB: {e}\nSQL: {inner_sql}")

        return self._make_new_table(duck_table, new_name)

    # ============================================================
    # DUCKDB: обработка маленьких групп
    # ============================================================
    def _evaluate_duckdb_with_small_groups(self, duck_table, env,
                                            method, params,
                                            columns, val_idx, safe_val,
                                            partition_cols, small_groups):
        """
        Если есть группы < 4 значений — считаем аномалии
        для больших групп, а для маленьких __anomaly = NULL.
        """
        from duckdb_engine import DuckDBTable
        import uuid

        # Строим ключ маленьких групп
        small_keys = []
        for row in small_groups:
            # row = (group_value1, ..., __cnt)
            small_keys.append(tuple(row[:-1]))

        # Условие: если ключ группы в списке маленьких → NULL
        # Формируем через OR для простоты
        part_cols_str = ", ".join(partition_cols)

        # Список маленьких групп как VALUES
        if small_keys:
            values_parts = []
            for k in small_keys:
                vals = ", ".join(_sql_quote(v) for v in k)
                values_parts.append(f"({vals})")
            values_sql = ", ".join(values_parts)
        else:
            values_sql = ""

        agg_exprs = []
        if method == 'iqr':
            k = params['k']
            if self.approx:
                agg_exprs.append(f"APPROX_QUANTILE(CAST({safe_val} AS DOUBLE), 0.25) AS __q1")
                agg_exprs.append(f"APPROX_QUANTILE(CAST({safe_val} AS DOUBLE), 0.75) AS __q3")
            else:
                agg_exprs.append(f"QUANTILE_CONT(CAST({safe_val} AS DOUBLE), 0.25) AS __q1")
                agg_exprs.append(f"QUANTILE_CONT(CAST({safe_val} AS DOUBLE), 0.75) AS __q3")
        elif method == 'zscore':
            agg_exprs.append(f"AVG(CAST({safe_val} AS DOUBLE)) AS __mean")
            agg_exprs.append(f"STDDEV_POP(CAST({safe_val} AS DOUBLE)) AS __sd")
        elif method == 'percentile':
            lo_p = params['lo'] / 100.0
            hi_p = params['hi'] / 100.0
            if self.approx:
                agg_exprs.append(f"APPROX_QUANTILE(CAST({safe_val} AS DOUBLE), {lo_p}) AS __lo")
                agg_exprs.append(f"APPROX_QUANTILE(CAST({safe_val} AS DOUBLE), {hi_p}) AS __hi")
            else:
                agg_exprs.append(f"QUANTILE_CONT(CAST({safe_val} AS DOUBLE), {lo_p}) AS __lo")
                agg_exprs.append(f"QUANTILE_CONT(CAST({safe_val} AS DOUBLE), {hi_p}) AS __hi")

        group_by = ", ".join(partition_cols)
        select_cols = ", ".join(partition_cols + agg_exprs)
        cte_sql = (
            f"WITH __stats AS ("
            f"SELECT {select_cols} "
            f"FROM {duck_table.table_name} "
            f"GROUP BY {group_by})"
        )

        join_cond = " AND ".join(
            f"t.{c} = s.{c}" for c in partition_cols
        )

        if method == 'iqr':
            k = params['k']
            anomaly_cond = (
                f"CASE "
                f"WHEN CAST(t.{safe_val} AS DOUBLE) < s.__q1 - {k} * (s.__q3 - s.__q1) THEN -1 "
                f"WHEN CAST(t.{safe_val} AS DOUBLE) > s.__q3 + {k} * (s.__q3 - s.__q1) THEN 1 "
                f"ELSE 0 END"
            )
        elif method == 'zscore':
            n = params['n']
            anomaly_cond = (
                f"CASE "
                f"WHEN CAST(t.{safe_val} AS DOUBLE) < s.__mean - {n} * s.__sd THEN -1 "
                f"WHEN CAST(t.{safe_val} AS DOUBLE) > s.__mean + {n} * s.__sd THEN 1 "
                f"ELSE 0 END"
            )
        elif method == 'percentile':
            anomaly_cond = (
                f"CASE "
                f"WHEN CAST(t.{safe_val} AS DOUBLE) < s.__lo THEN -1 "
                f"WHEN CAST(t.{safe_val} AS DOUBLE) > s.__hi THEN 1 "
                f"ELSE 0 END"
            )
        else:
            raise ValueError(f"anomaly: неизвестный метод '{method}'")

        # Условие: если группа маленькая — NULL
        small_check_parts = []
        for c in partition_cols:
            small_check_parts.append(f"t.{c}")

        # Условие «в списке маленьких» через IN
        if values_sql:
            small_in_cond = (
                f"({', '.join(small_check_parts)}) IN ({values_sql})"
            )
            anomaly_expr = f"CASE WHEN {small_in_cond} THEN NULL ELSE {anomaly_cond} END"
        else:
            anomaly_expr = anomaly_cond

        select_parts = []
        for i, c in enumerate(columns):
            esc = '"' + str(c).replace('"', '""') + '"'
            select_parts.append(f"t.{esc}")
            if i == val_idx:
                select_parts.append(f'{anomaly_expr} AS "__anomaly"')

        inner_sql = (
            f"{cte_sql} "
            f"SELECT {', '.join(select_parts)} "
            f"FROM {duck_table.table_name} AS t "
            f"JOIN __stats AS s ON {join_cond}"
        )

        if self.only:
            inner_sql = (
                f"SELECT * FROM ({inner_sql}) "
                f"WHERE __anomaly IS NOT NULL AND __anomaly <> 0"
            )

        new_name = f"anomaly_{uuid.uuid4().hex[:8]}"
        try:
            duck_table.con.execute(
                f'CREATE OR REPLACE VIEW {new_name} AS {inner_sql}'
            )
        except Exception as e:
            raise RuntimeError(f"anomaly: ошибка DuckDB: {e}\nSQL: {inner_sql}")

        return self._make_new_table(duck_table, new_name)

    # ============================================================
    # DUCKDB: результат с __anomaly = NULL (мало данных)
    # ============================================================
    def _empty_result(self, duck_table, columns, val_idx):
        """Возвращает таблицу с __anomaly = NULL (мало данных)."""
        from duckdb_engine import DuckDBTable
        import uuid

        select_parts = []
        for i, c in enumerate(columns):
            esc = '"' + str(c).replace('"', '""') + '"'
            select_parts.append(esc)
            if i == val_idx:
                select_parts.append('NULL AS "__anomaly"')

        sql = f"SELECT {', '.join(select_parts)} FROM {duck_table.table_name}"

        if self.only:
            sql = f"SELECT * FROM ({sql}) WHERE 1=0"

        new_name = f"anomaly_{uuid.uuid4().hex[:8]}"
        try:
            duck_table.con.execute(
                f'CREATE OR REPLACE VIEW {new_name} AS {sql}'
            )
        except Exception as e:
            raise RuntimeError(f"anomaly: ошибка DuckDB: {e}\nSQL: {sql}")

        return self._make_new_table(duck_table, new_name)

    def _make_new_table(self, duck_table, new_name):
        from duckdb_engine import DuckDBTable
        new_table = DuckDBTable.__new__(DuckDBTable)
        new_table.path = duck_table.path
        new_table.table_name = new_name
        new_table.con = duck_table.con
        new_table.utf8_path = duck_table.utf8_path
        new_table.is_temp = False
        new_table._tmp_path = None
        return new_table

    def __repr__(self):
        return f"anomaly({self.data}, method={self.method})"


# ============================================================
# ПРОЦЕНТИЛИ (linear interpolation)
# ============================================================
def _percentile_linear(sorted_values, p):
    """
    Процентиль по линейной интерполяции (как в NumPy).
    p — от 0 до 100.
    """
    if not sorted_values:
        return None
    n = len(sorted_values)
    if n == 1:
        return sorted_values[0]
    k = (n - 1) * (p / 100.0)
    f = int(k)
    c = f + 1
    if c >= n:
        return sorted_values[-1]
    return sorted_values[f] + (k - f) * (sorted_values[c] - sorted_values[f])


# ============================================================
# SQL-экранирование
# ============================================================
def _sql_quote(val):
    """Экранирует значение для SQL."""
    if val is None:
        return "NULL"
    if isinstance(val, bool):
        return "TRUE" if val else "FALSE"
    if isinstance(val, (int, float)):
        return str(val)
    return "'" + str(val).replace("'", "''") + "'"