# ast_nodes/functions/addrows.py
"""
Функция ADDROWS — добавляет N строк в таблицу.

СИНТАКСИС:
    m2 = addrows(m, 5)           # 5 пустых строк (None)
    m2 = addrows(m, 3, 0)        # 3 строки, заполненные 0
    m2 = addrows(m, 2, "-")      # 2 строки, заполненные "-"

ПРАВИЛА:
    - Всегда возвращает НОВУЮ таблицу.
    - Строки добавляются В КОНЕЦ.
    - Работает с Matrix (в RAM) и DuckDB (через SQL).
    - N — число или переменная.
    - Fill — опционально (по умолчанию None).
"""

from ..base import Node
from runtime.matrix import MatrExMatrix


def _is_duckdb(val):
    try:
        from duckdb_engine import DuckDBTable
        return isinstance(val, DuckDBTable)
    except ImportError:
        return False


class AddRowsNode(Node):
    def __init__(self, data, count, fill=None):
        self.data = data
        self.count = count
        self.fill = fill

    def evaluate(self, env):
        # 1. Данные
        data_obj = (self.data.evaluate(env)
                    if hasattr(self.data, 'evaluate')
                    else self.data)

        # 2. Количество
        count_val = (self.count.evaluate(env)
                     if hasattr(self.count, 'evaluate')
                     else self.count)
        if not isinstance(count_val, (int, float)):
            raise TypeError(
                f"addrows: количество должно быть числом, "
                f"получено {type(count_val).__name__}"
            )
        n = int(count_val)
        if n < 0:
            raise ValueError(
                f"addrows: количество не может быть отрицательным: {n}"
            )

        # 3. Значение заполнения
        fill_val = None
        if self.fill is not None:
            fill_val = (self.fill.evaluate(env)
                        if hasattr(self.fill, 'evaluate')
                        else self.fill)

        # 4. DuckDB → SQL
        if _is_duckdb(data_obj):
            return self._addrows_duckdb(data_obj, n, fill_val)

        # 5. Matrix → RAM
        if hasattr(data_obj, 'data') and data_obj.is_2d:
            return self._addrows_matrix(data_obj, n, fill_val)

        raise TypeError(
            "addrows: ожидается матрица или DuckDB.\n"
            "  Пример: m2 = addrows(m, 5)"
        )

    # ============================================================
    # MATRIX
    # ============================================================
    def _addrows_matrix(self, matrix_obj, n, fill_val):
        if n == 0:
            return MatrExMatrix(
                [list(row) if isinstance(row, list) else [row]
                 for row in matrix_obj.data],
                True
            )

        result_data = [list(row) if isinstance(row, list) else [row]
                       for row in matrix_obj.data]

        n_cols = matrix_obj.cols
        new_row = [fill_val] * n_cols

        for _ in range(n):
            result_data.append(list(new_row))

        return MatrExMatrix(result_data, True)

    # ============================================================
    # DUCKDB
    # ============================================================
    def _addrows_duckdb(self, duck_table, n, fill_val):
        from duckdb_engine import DuckDBTable
        import uuid

        if n == 0:
            return duck_table

        columns = duck_table.get_columns()

        def _escape_val(val):
            if val is None:
                return "NULL"
            if isinstance(val, bool):
                return "TRUE" if val else "FALSE"
            if isinstance(val, (int, float)):
                return str(val)
            return "'" + str(val).replace("'", "''") + "'"

        val_sql = _escape_val(fill_val)
        select_row = "SELECT " + ", ".join([val_sql] * len(columns))

        parts = [f"SELECT * FROM {duck_table.table_name}"]
        for _ in range(n):
            parts.append(select_row)

        union_sql = " UNION ALL ".join(parts)

        new_name = f"addrows_{uuid.uuid4().hex[:8]}"
        sql = f"CREATE OR REPLACE VIEW {new_name} AS {union_sql}"

        try:
            duck_table.con.execute(sql)
        except Exception as e:
            raise RuntimeError(
                f"Ошибка addrows: {e}\n"
                f"  SQL: {sql}"
            )

        new_table = DuckDBTable.__new__(DuckDBTable)
        new_table.path = duck_table.path
        new_table.table_name = new_name
        new_table.con = duck_table.con
        new_table.utf8_path = duck_table.utf8_path
        new_table.is_temp = False
        new_table._tmp_path = None

        return new_table

    def __repr__(self):
        if self.fill is not None:
            return f"addrows({self.data}, {self.count}, {self.fill})"
        return f"addrows({self.data}, {self.count})"