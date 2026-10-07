# ast_nodes/functions/joinarray.py
"""
Функция JOINARRAY - объединение матриц.

ВАЖНО: joinarray() НЕ изменяет исходные матрицы.
Она ВОЗВРАЩАЕТ НОВУЮ матрицу.

СИНТАКСИС:
    joinarray(a, b, vertical)              # строки вниз
    joinarray(a, b, horizontal)            # столбцы вправо
    joinarray(a, b, c, vertical)           # несколько матриц
    joinarray(a, b, c, d, horizontal)

ПОДДЕРЖКА DUCKDB:
    - DuckDBTable + DuckDBTable → SQL UNION ALL (потоково)
    - DuckDBTable + MatrExMatrix → конвертация
    - MatrExMatrix + MatrExMatrix → как раньше (RAM)
"""

from ..base import Node
from runtime.matrix import MatrExMatrix


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
# JOINARRAY NODE
# ============================================================
class JoinArrayNode(Node):
    """Объединение матриц с автоматическим дополнением None."""

    def __init__(self, matrices, axis=None):
        self.matrices = matrices
        self.axis = axis

    # ============================================================
    # ПРОВЕРКА: НЕ СРЕЗЫ ЛИ
    # ============================================================
    def _check_no_slices(self, env):
        """Проверяет, что аргументы — не срезы."""
        from ast_nodes.index import IndexNode
        from errors import ArrayVatorError, ErrorContext

        for i, m in enumerate(self.matrices, 1):
            if isinstance(m, IndexNode):
                raise ArrayVatorError(
                    code="JOINARRAY_NO_SLICES",
                    context=ErrorContext(
                        source_code=env.source if hasattr(env, 'source') else None,
                    ),
                    message=(
                        f"Нельзя объединять частичные диапазоны.\n"
                        f"  joinarray() работает только с ЦЕЛЫМИ матрицами.\n"
                        f"  Аргумент №{i} — это срез, а не матрица."
                    ),
                    suggestion=(
                        "Сначала извлеките данные в переменные:\n"
                        "     col1 = m1[:, 2]\n"
                        "     col2 = m2[:, 3]\n"
                        "     result = joinarray(col1, col2, horizontal)\n"
                        "\n"
                        "Или объедините целые матрицы:\n"
                        "     result = joinarray(m1, m2, horizontal)"
                    ),
                )

    # ============================================================
    # EVALUATE
    # ============================================================
    def evaluate(self, env):
        from errors import ArrayVatorError

        # 1. Проверка на срезы
        self._check_no_slices(env)

        # 2. Вычисляем аргументы
        matrix_objs = []
        for m in self.matrices:
            obj = m.evaluate(env) if hasattr(m, 'evaluate') else m

            # Проверяем, что это матрица или DuckDBTable
            is_matrix = hasattr(obj, 'data') and hasattr(obj, 'is_2d')
            is_duckdb = _is_duckdb(obj)

            if not (is_matrix or is_duckdb):
                raise TypeError(
                    f"joinarray(): все аргументы должны быть матрицами, "
                    f"получен {type(obj)}"
                )
            matrix_objs.append(obj)

        if not matrix_objs:
            return MatrExMatrix([], True)

        # 3. Определяем направление
        axis_val = None
        if self.axis is not None:
            axis_val = self.axis.evaluate(env) if hasattr(self.axis, 'evaluate') else self.axis
            if isinstance(axis_val, str):
                axis_val = axis_val.strip().lower()

        # 4. Проверяем: все ли DuckDB
        all_duckdb = all(_is_duckdb(m) for m in matrix_objs)

        if all_duckdb:
            # ВСЕ DuckDB → используем SQL UNION ALL
            return self._join_duckdb(matrix_objs, axis_val)

        # 5. Гибридный режим: конвертируем DuckDB в MatrExMatrix
        converted = []
        for m in matrix_objs:
            if _is_duckdb(m):
                # Загружаем в RAM
                converted.append(self._duckdb_to_matrix(m))
            else:
                converted.append(m)

        # 6. HORIZONTAL
        if axis_val == 'horizontal':
            return self._join_horizontal(converted)

        # 7. VERTICAL (по умолчанию)
        return self._join_vertical(converted)

    # ============================================================
    # DUCKDB → MatrExMatrix
    # ============================================================
    def _duckdb_to_matrix(self, duck_table):
        """Конвертирует DuckDBTable в MatrExMatrix (загружает в RAM)."""
        try:
            data = duck_table.get_data_for_show(limit=10**9)
            return MatrExMatrix(data, True)
        except Exception:
            # Fallback: первые 1000 строк
            data = duck_table.get_data_for_show(limit=1000)
            return MatrExMatrix(data, True)

    # ============================================================
    # ОБЪЕДИНЕНИЕ DUCKDB (SQL UNION ALL)
    # ============================================================
    def _join_duckdb(self, duck_tables, axis_val):
        """
        Объединяет несколько DuckDBTable через SQL.
        Возвращает НОВЫЙ DuckDBTable с view.
        """
        from duckdb_engine import DuckDBTable

        # Используем соединение первой таблицы
        con = duck_tables[0].con

        # Генерируем уникальное имя для новой view
        import uuid
        new_name = f"joined_{uuid.uuid4().hex[:8]}"

        # Получаем SQL для каждой таблицы
        selects = [f"SELECT * FROM {t.table_name}" for t in duck_tables]

        if axis_val == 'horizontal':
            # HORIZONTAL — объединение столбцов
            # Проверяем, что одинаковое количество строк
            row_counts = [t.get_row_count() for t in duck_tables]
            if len(set(row_counts)) > 1:
                raise ValueError(
                    f"joinarray(horizontal): все таблицы должны иметь "
                    f"одинаковое количество строк. Получено: {row_counts}"
                )

            # Собираем все столбцы
            all_columns = []
            for t in duck_tables:
                all_columns.extend(t.get_columns())

            # Формируем SELECT с ROW_NUMBER для соединения
            selects_with_rn = []
            for i, t in enumerate(duck_tables):
                cols = ", ".join(t.get_columns())
                selects_with_rn.append(f"""
                    SELECT ROW_NUMBER() OVER () AS rn_{i}, {cols}
                    FROM {t.table_name}
                """)

            # JOIN по rn
            join_sql = selects_with_rn[0]
            for i in range(1, len(duck_tables)):
                join_sql = f"""
                    SELECT a.*, b.* EXCLUDE (rn_{i})
                    FROM ({join_sql}) a
                    JOIN ({selects_with_rn[i]}) b ON a.rn_0 = b.rn_{i}
                """

            # Упрощённый вариант через UNION ALL — не сработает для horizontal
            # Используем более простой подход: берём столбцы последовательно
            final_sql = self._build_horizontal_sql(duck_tables)

        else:
            # VERTICAL — объединение строк (UNION ALL)
            # Проверяем, что одинаковое количество столбцов
            col_counts = [len(t.get_columns()) for t in duck_tables]
            if len(set(col_counts)) > 1:
                raise ValueError(
                    f"joinarray(vertical): все таблицы должны иметь "
                    f"одинаковое количество столбцов. Получено: {col_counts}"
                )

            final_sql = " UNION ALL ".join(selects)

        # Создаём view
        con.execute(f"CREATE OR REPLACE VIEW {new_name} AS {final_sql}")

        # Создаём новый DuckDBTable с этим view
        new_table = DuckDBTable.__new__(DuckDBTable)
        new_table.path = duck_tables[0].path  # путь первой таблицы
        new_table.table_name = new_name
        new_table.con = con
        new_table.utf8_path = duck_tables[0].utf8_path
        new_table.is_temp = False
        new_table._tmp_path = None

        return new_table

    def _build_horizontal_sql(self, duck_tables):
        """Строит SQL для горизонтального объединения."""
        # Простой вариант: если у всех 1 столбец или совпадает структура
        # Используем UNION ALL с дополнительными колонками

        # Более надёжно: используем ROW_NUMBER и JOIN
        parts = []
        for i, t in enumerate(duck_tables):
            cols = t.get_columns()
            col_list = ", ".join(f'"{c}"' for c in cols)
            parts.append(f"""
                SELECT ROW_NUMBER() OVER () AS __rn, {col_list}
                FROM {t.table_name}
            """)

        # Базовый SELECT
        first_cols = duck_tables[0].get_columns()
        first_col_list = ", ".join(f'a."{c}"' for c in first_cols)

        join_parts = []
        for i in range(1, len(duck_tables)):
            cols = duck_tables[i].get_columns()
            col_list = ", ".join(f'b{i}."{c}"' for c in cols)
            join_parts.append(
                f"JOIN ({parts[i]}) b{i} ON a.__rn = b{i}.__rn"
            )

        all_cols = first_col_list
        for i in range(1, len(duck_tables)):
            cols = duck_tables[i].get_columns()
            all_cols += ", " + ", ".join(f'b{i}."{c}"' for c in cols)

        return f"""
            SELECT {all_cols}
            FROM ({parts[0]}) a
            {' '.join(join_parts)}
        """

    # ============================================================
    # ВЕРТИКАЛЬНОЕ ОБЪЕДИНЕНИЕ (RAM)
    # ============================================================
    def _join_vertical(self, matrix_objs):
        """Объединение по строкам (вниз)."""
        max_cols = 0
        for m in matrix_objs:
            cols = m.cols if m.is_2d else 1
            if cols > max_cols:
                max_cols = cols

        result_data = []
        for m in matrix_objs:
            if m.is_2d:
                for row in m.data:
                    new_row = list(row)
                    while len(new_row) < max_cols:
                        new_row.append(None)
                    result_data.append(new_row)
            else:
                for item in m.data:
                    new_row = [item]
                    while len(new_row) < max_cols:
                        new_row.append(None)
                    result_data.append(new_row)

        return MatrExMatrix(result_data, True)

    # ============================================================
    # ГОРИЗОНТАЛЬНОЕ ОБЪЕДИНЕНИЕ (RAM)
    # ============================================================
    def _join_horizontal(self, matrix_objs):
        """Объединение по столбцам (вправо)."""
        max_rows = max(m.rows for m in matrix_objs)

        result_data = []
        for i in range(max_rows):
            new_row = []
            for m in matrix_objs:
                if i < len(m.data):
                    row = m.data[i]
                    if isinstance(row, list):
                        new_row.extend(row)
                    else:
                        new_row.append(row)
                else:
                    cols_count = m.cols if m.is_2d else 1
                    new_row.extend([None] * cols_count)
            result_data.append(new_row)

        return MatrExMatrix(result_data, True)

    def __repr__(self):
        return f"joinarray({self.matrices}, axis={self.axis})"