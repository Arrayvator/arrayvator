# ast_nodes/functions/sample.py
"""
Функция SAMPLE — случайные N строк из таблицы.

СИНТАКСИС:
    sample(m, N)              # N случайных строк
    sample(m, N, seed)        # N случайных строк с seed

ПРИМЕРЫ:
    m = OpenCSV("big.csv", BigData)
    r = sample(m, 1000)              # 1000 случайных строк
    r = sample(m, 100)               # 100 строк
    r = sample(m, 500, 42)           # 500 строк, seed=42 (воспроизводимо)

DUCKDB:
    - SELECT * FROM t USING SAMPLE N
    - Или с seed: USING SAMPLE N (reservoir, 42)
    - Мгновенно на 10 млн строк.

MATRIX:
    - Случайные N строк из RAM (для небольших данных).
"""

import random as py_random

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


class SampleNode(Node):
    def __init__(self, data, n, seed=None):
        self.data = data
        self.n = n
        self.seed = seed

    def evaluate(self, env):
        # 1. Определяем данные
        data_obj = self.data.evaluate(env) if hasattr(self.data, 'evaluate') else self.data

        # 2. Количество
        n_val = self.n.evaluate(env) if hasattr(self.n, 'evaluate') else self.n
        if not isinstance(n_val, (int, float)):
            raise TypeError(
                f"sample: количество должно быть числом, "
                f"получено {type(n_val).__name__}"
            )
        n_int = int(n_val)
        if n_int < 1:
            raise ValueError(
                f"sample: количество должно быть >= 1, получено {n_int}"
            )

        # 3. Seed (опционально)
        seed_val = None
        if self.seed is not None:
            seed_val = (self.seed.evaluate(env)
                        if hasattr(self.seed, 'evaluate')
                        else self.seed)
            if seed_val is not None:
                try:
                    seed_val = int(seed_val)
                except (ValueError, TypeError):
                    seed_val = None

        # 4. DuckDB → SQL
        if _is_duckdb(data_obj):
            return self._sample_duckdb(data_obj, n_int, seed_val)

        # 5. Matrix → RAM
        if hasattr(data_obj, 'data') and data_obj.is_2d:
            return self._sample_matrix(data_obj, n_int, seed_val)

        raise TypeError(
            "sample: ожидается матрица или DuckDB.\n"
            "  Пример: r = sample(m, 1000)"
        )

    # ============================================================
    # DUCKDB
    # ============================================================
    def _sample_duckdb(self, duck_table, n, seed):
        from duckdb_engine import DuckDBTable
        import uuid

        new_name = f"sample_{uuid.uuid4().hex[:8]}"

        if seed is not None:
            sql = f"""
                CREATE OR REPLACE VIEW {new_name} AS
                SELECT * FROM {duck_table.table_name}
                USING SAMPLE {n} (reservoir, {seed})
            """
        else:
            sql = f"""
                CREATE OR REPLACE VIEW {new_name} AS
                SELECT * FROM {duck_table.table_name}
                USING SAMPLE {n}
            """

        try:
            duck_table.con.execute(sql)
        except Exception as e:
            raise RuntimeError(f"Ошибка sample: {e}\nSQL: {sql}")

        new_table = DuckDBTable.__new__(DuckDBTable)
        new_table.path = duck_table.path
        new_table.table_name = new_name
        new_table.con = duck_table.con
        new_table.utf8_path = duck_table.utf8_path
        new_table.is_temp = False
        new_table._tmp_path = None

        return new_table

    # ============================================================
    # MATRIX
    # ============================================================
    def _sample_matrix(self, matrix_obj, n, seed):
        # Заголовок
        header = matrix_obj.data[0] if matrix_obj.rows > 0 else []

        # Данные (без заголовка)
        data_rows = []
        for i in range(1, matrix_obj.rows):
            data_rows.append(list(matrix_obj.data[i]))

        if not data_rows:
            return MatrExMatrix([list(header)], True)

        # Seed
        if seed is not None:
            py_random.seed(seed)

        # Выборка
        actual_n = min(n, len(data_rows))
        sampled = py_random.sample(data_rows, actual_n)

        # Результат
        result = [list(header)] + sampled
        return MatrExMatrix(result, True)

    def __repr__(self):
        if self.seed is not None:
            return f"sample({self.data}, {self.n}, {self.seed})"
        return f"sample({self.data}, {self.n})"