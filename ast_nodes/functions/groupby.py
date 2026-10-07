# ast_nodes/functions/groupby.py
"""
Функция GROUPBY — аналог SQL GROUP BY.

СИНТАКСИС:
    r = groupby(by m[:, "Отдел"], agg sum(m[:, "Зарплата"]))

    # Несколько ключей
    r = groupby(by m[:, "Отдел"], m[:, "Год"],
                agg sum(m[:, "Продажи"]))

    # Несколько агрегатов
    r = groupby(by m[:, "Отдел"],
                agg sum(m[:, "Зарплата"]),
                    avg(m[:, "Зарплата"]),
                    count())

    # С HAVING
    r = groupby(by m[:, "Отдел"],
                agg sum(m[:, "Зарплата"]),
                having sum(m[:, "Зарплата"]) > 100000)

ПРАВИЛА:
    - Таблица берётся из первого среза в by.
    - Все срезы (by, agg, having) должны быть из ОДНОЙ таблицы.
    - Всегда возвращает новую матрицу / DuckDBTable.
    - Колонки by → как есть.
    - Колонки agg → автоматические имена.
"""

from ..base import Node
from runtime.matrix import MatrExMatrix


# ============================================================
# ОПРЕДЕЛЕНИЕ DUCKDBTABLE
# ============================================================
def _is_duckdb(val):
    try:
        from duckdb_engine import DuckDBTable
        return isinstance(val, DuckDBTable)
    except ImportError:
        return False


# ============================================================
# ИМЕНА АГРЕГАТОВ
# ============================================================
AGG_NAMES = {
    'sum':    'Сумма',
    'avg':    'Среднее',
    'count':  'Количество',
    'min':    'Минимум',
    'max':    'Максимум',
    'median': 'Медиана',
    'first':  'Первое',
    'last':   'Последнее',
    'std':    'Отклонение',
}

SQL_AGG = {
    'sum':    'SUM',
    'avg':    'AVG',
    'count':  'COUNT',
    'min':    'MIN',
    'max':    'MAX',
    'median': 'MEDIAN',
    'first':  'FIRST',
    'last':   'LAST',
    'std':    'STDDEV',
}


class GroupByNode(Node):
    def __init__(self, by_list, agg_list, having=None):
        self.by_list = by_list      # список IndexNode
        self.agg_list = agg_list    # список (agg_name, IndexNode | None)
        self.having = having        # (agg_name, IndexNode, op, scalar) или None

    def evaluate(self, env):
        from ast_nodes.index import IndexNode

        # 1. Таблица — из первого by
        if not self.by_list:
            raise ValueError("groupby: не указаны ключи by")

        first_by = self.by_list[0]
        if not isinstance(first_by, IndexNode):
            raise TypeError(
                "groupby: by требует срез m[:, \"X\"]\n"
                "  Пример: groupby(by m[:, \"Отдел\"], agg sum(m[:, \"Зарплата\"]))"
            )

        data_obj = first_by.matrix.evaluate(env)

        # 2. Проверяем, что все срезы — из одной таблицы
        self._check_same_table(data_obj, env)

        # 3. DuckDB → SQL
        if _is_duckdb(data_obj):
            return self._groupby_duckdb(data_obj, env)

        # 4. Matrix → RAM
        if hasattr(data_obj, 'data') and data_obj.is_2d:
            return self._groupby_matrix(data_obj, env)

        raise TypeError(
            "groupby: ожидается матрица или DuckDB.\n"
            "  Пример: groupby(by m[:, \"Отдел\"], agg sum(m[:, \"Зарплата\"]))"
        )

    def _check_same_table(self, data_obj, env):
        """Проверяет, что все срезы ссылаются на одну таблицу."""
        from ast_nodes.index import IndexNode

        all_nodes = list(self.by_list)
        for agg_name, agg_node in self.agg_list:
            if agg_node is not None:
                all_nodes.append(agg_node)
        if self.having is not None:
            _, having_node, _, _ = self.having
            if having_node is not None:
                all_nodes.append(having_node)

        for node in all_nodes:
            if not isinstance(node, IndexNode):
                continue
            try:
                other = node.matrix.evaluate(env)
            except Exception:
                continue
            if other is not data_obj:
                raise ValueError(
                    "groupby: все срезы должны быть из ОДНОЙ таблицы.\n"
                    "  Проверьте by, agg, having — они должны ссылаться на одну переменную."
                )

    # ============================================================
    # MATRIX
    # ============================================================
    def _groupby_matrix(self, matrix_obj, env):
        # --- Заголовки ---
        header = matrix_obj.data[0] if matrix_obj.rows > 0 else []

        # --- Ключи ---
        by_indices = []
        by_names = []
        for by_node in self.by_list:
            idx = self._resolve_col(by_node, matrix_obj, env)
            by_indices.append(idx)
            by_names.append(header[idx] if idx < len(header) else f"col{idx}")

        # --- Агрегаты ---
        agg_specs = []  # [(agg_name, col_idx | None, result_name)]
        for agg_name, agg_node in self.agg_list:
            if agg_node is None:
                result_name = AGG_NAMES.get(agg_name, agg_name)
                agg_specs.append((agg_name, None, result_name))
            else:
                idx = self._resolve_col(agg_node, matrix_obj, env)
                col_name = header[idx] if idx < len(header) else f"col{idx}"
                result_name = f"{AGG_NAMES.get(agg_name, agg_name)}_{col_name}"
                agg_specs.append((agg_name, idx, result_name))

        # --- Строки данных (без заголовка) ---
        data_rows = []
        for i in range(1, matrix_obj.rows):
            data_rows.append(matrix_obj.data[i])

        # --- Группировка ---
        groups = {}
        order = []
        for row in data_rows:
            key = tuple(
                row[idx] if idx < len(row) else None
                for idx in by_indices
            )
            if key not in groups:
                groups[key] = []
                order.append(key)
            groups[key].append(row)

        # --- HAVING ---
        if self.having is not None:
            order = self._apply_having(order, groups, agg_specs, env)

        # --- Результат ---
        result_header = by_names + [s[2] for s in agg_specs]
        result = [result_header]

        for key in order:
            rows = groups[key]
            row_out = list(key)
            for agg_name, col_idx, _ in agg_specs:
                row_out.append(self._apply_agg(agg_name, col_idx, rows))
            result.append(row_out)

        return MatrExMatrix(result, True)

    def _apply_agg(self, agg_name, col_idx, rows):
        """Применяет агрегат к списку строк."""
        if agg_name == 'count':
            if col_idx is None:
                return len(rows)
            return sum(
                1 for r in rows
                if col_idx < len(r) and r[col_idx] is not None
            )

        values = []
        for r in rows:
            if col_idx is not None and col_idx < len(r):
                values.append(r[col_idx])

        nums = [v for v in values if v is not None]

        if not nums:
            return None

        if agg_name == 'sum':
            try:
                return sum(nums)
            except Exception:
                return None

        if agg_name == 'avg':
            try:
                return sum(nums) / len(nums)
            except Exception:
                return None

        if agg_name == 'min':
            try:
                return min(nums)
            except Exception:
                return None

        if agg_name == 'max':
            try:
                return max(nums)
            except Exception:
                return None

        if agg_name == 'median':
            try:
                s = sorted(nums)
                n = len(s)
                if n % 2 == 1:
                    return s[n // 2]
                return (s[n // 2 - 1] + s[n // 2]) / 2
            except Exception:
                return None

        if agg_name == 'first':
            return nums[0]

        if agg_name == 'last':
            return nums[-1]

        if agg_name == 'std':
            try:
                mean = sum(nums) / len(nums)
                var = sum((x - mean) ** 2 for x in nums) / len(nums)
                return var ** 0.5
            except Exception:
                return None

        return None

    def _apply_having(self, order, groups, agg_specs, env):
        """Фильтрует группы по HAVING."""
        agg_name, agg_node, op, value_node = self.having
        value = (value_node.evaluate(env)
                 if hasattr(value_node, 'evaluate')
                 else value_node)

        col_idx = None
        if agg_node is not None:
            for an, ci, _ in agg_specs:
                if an == agg_name:
                    col_idx = ci
                    break

        new_order = []
        for key in order:
            rows = groups[key]
            agg_result = self._apply_agg(agg_name, col_idx, rows)
            if self._compare(agg_result, op, value):
                new_order.append(key)
        return new_order

    def _compare(self, a, op, b):
        if a is None:
            return False
        try:
            if op == 'EQUALS':       return a == b
            if op == 'NOTEQUAL':     return a != b
            if op == 'LESS':         return a < b
            if op == 'GREATER':      return a > b
            if op == 'LESSEQUAL':    return a <= b
            if op == 'GREATEREQUAL': return a >= b
        except TypeError:
            return False
        return False

    def _resolve_col(self, index_node, matrix_obj, env):
        """Извлекает 0-based индекс столбца из IndexNode."""
        from ast_nodes.index import IndexNode
        from ..utils.index_utils import resolve_column_index

        if not isinstance(index_node, IndexNode):
            raise TypeError("groupby: ожидается срез m[:, \"X\"]")

        if len(index_node.indices) != 2:
            raise TypeError("groupby: ожидается срез m[:, \"X\"]")

        col_spec_node = index_node.indices[1]
        col_spec = (col_spec_node.evaluate(env)
                    if hasattr(col_spec_node, 'evaluate')
                    else col_spec_node)

        idx, _ = resolve_column_index(matrix_obj, col_spec, env)
        return idx

    # ============================================================
    # DUCKDB
    # ============================================================
    def _groupby_duckdb(self, duck_table, env):
        from duckdb_engine import DuckDBTable
        from .filterif import _resolve_column_for_duckdb
        import uuid

        columns = duck_table.get_columns()

        def _get_col_name(index_node):
            if not hasattr(index_node, 'indices'):
                return None
            if len(index_node.indices) != 2:
                return None
            col_spec_node = index_node.indices[1]
            col_spec = (col_spec_node.evaluate(env)
                        if hasattr(col_spec_node, 'evaluate')
                        else col_spec_node)
            idx = _resolve_column_for_duckdb(columns, col_spec)
            return columns[idx] if 0 <= idx < len(columns) else None

        def _esc(name):
            return '"' + str(name).replace('"', '""') + '"'

        # --- Ключи ---
        by_cols = []
        for by_node in self.by_list:
            col_name = _get_col_name(by_node)
            if col_name:
                by_cols.append(col_name)

        if not by_cols:
            raise ValueError("groupby: не удалось определить ключи by")

        # --- Агрегаты ---
        select_parts = [_esc(c) for c in by_cols]
        for agg_name, agg_node in self.agg_list:
            sql_agg = SQL_AGG.get(agg_name, 'SUM')
            if agg_node is None:
                result_name = AGG_NAMES.get(agg_name, agg_name)
                select_parts.append(f'{sql_agg}(*) AS {_esc(result_name)}')
            else:
                col_name = _get_col_name(agg_node)
                if not col_name:
                    continue
                result_name = f"{AGG_NAMES.get(agg_name, agg_name)}_{col_name}"
                select_parts.append(
                    f'{sql_agg}(CAST({_esc(col_name)} AS DOUBLE)) '
                    f'AS {_esc(result_name)}'
                )

        group_by = ', '.join(_esc(c) for c in by_cols)

        # --- HAVING ---
        having_sql = ""
        if self.having is not None:
            agg_name, agg_node, op, value_node = self.having
            sql_agg = SQL_AGG.get(agg_name, 'SUM')
            op_sql = {
                'EQUALS': '=', 'NOTEQUAL': '<>',
                'LESS': '<', 'GREATER': '>',
                'LESSEQUAL': '<=', 'GREATEREQUAL': '>=',
            }.get(op, '=')
            value = (value_node.evaluate(env)
                     if hasattr(value_node, 'evaluate')
                     else value_node)
            value_sql = str(value)
            if agg_node is None:
                agg_expr = f'{sql_agg}(*)'
            else:
                col_name = _get_col_name(agg_node)
                agg_expr = f'{sql_agg}(CAST({_esc(col_name)} AS DOUBLE))'
            having_sql = f" HAVING {agg_expr} {op_sql} {value_sql}"

        # --- SQL ---
        new_name = f"groupby_{uuid.uuid4().hex[:8]}"
        sql = f"""
            CREATE OR REPLACE VIEW {new_name} AS
            SELECT {', '.join(select_parts)}
            FROM {duck_table.table_name}
            GROUP BY {group_by}
            {having_sql}
        """

        try:
            duck_table.con.execute(sql)
        except Exception as e:
            raise RuntimeError(f"Ошибка groupby: {e}\nSQL: {sql}")

        new_table = DuckDBTable.__new__(DuckDBTable)
        new_table.path = duck_table.path
        new_table.table_name = new_name
        new_table.con = duck_table.con
        new_table.utf8_path = duck_table.utf8_path
        new_table.is_temp = False
        new_table._tmp_path = None

        return new_table

    def __repr__(self):
        return f"groupby(by {len(self.by_list)}, agg {len(self.agg_list)})"