# ast_nodes/functions/parquet.py
"""
Parquet-функции ArrayVator:
    OpenParquet     — загрузка из Parquet (DuckDB, потоково)
    SaveParquet     — сохранение в Parquet

Parquet — колоночный сжатый формат. В 10-20 раз быстрее CSV,
в 5-10 раз меньше размер.

СИНТАКСИС:
    m = OpenParquet("data.parquet")
    SaveParquet(m, "out.parquet")
"""

import os
from ..base import Node


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
# ОТКРЫТИЕ PARQUET
# ============================================================
class OpenParquetNode(Node):
    """
    OpenParquet("file.parquet")

    Чтение через DuckDB (потоково, без загрузки в RAM).
    Возвращает DuckDBTable.
    """

    def __init__(self, file_path):
        self.file_path = file_path

    def evaluate(self, env):
        from runtime.matrix import MatrExMatrix

        path = self.file_path.evaluate(env) if hasattr(self.file_path, 'evaluate') else self.file_path
        if not isinstance(path, str):
            raise TypeError(f"Путь к файлу должен быть строкой, получен {type(path)}")

        if not os.path.exists(path):
            raise FileNotFoundError(f"Файл не найден: {path}")

        # ============================================================
        # Через DuckDB (потоково) — используем ГЛОБАЛЬНОЕ соединение
        # ============================================================
        try:
            import duckdb
            from duckdb_engine import DuckDBTable, get_global_connection

            con = get_global_connection()
            safe_path = path.replace("'", "''").replace("\\", "\\\\")

            # Генерируем имя view
            import uuid
            table_name = f"t_parquet_{uuid.uuid4().hex[:8]}"

            # Регистрируем view на Parquet
            con.execute(f"""
                CREATE OR REPLACE VIEW {table_name} AS
                SELECT * FROM read_parquet('{safe_path}')
            """)

            # Создаём DuckDBTable без _register (вручную)
            table = DuckDBTable.__new__(DuckDBTable)
            table.path = path
            table.table_name = table_name
            table.con = con
            table.utf8_path = path
            table.is_temp = False
            table._tmp_path = None

            return table

        except ImportError:
            raise ImportError(
                "DuckDB не установлен.\n"
                "Установите: pip install duckdb"
            )

    def __repr__(self):
        return f"OpenParquet({self.file_path})"


# ============================================================
# СОХРАНЕНИЕ PARQUET
# ============================================================
class SaveParquetNode(Node):
    """
    SaveParquet(data, "file.parquet")

    Сохраняет MatrExMatrix или DuckDBTable в Parquet.
    """

    def __init__(self, data, file_path):
        self.data = data
        self.file_path = file_path

    def evaluate(self, env):
        data_obj = self.data.evaluate(env)
        path = self.file_path.evaluate(env) if hasattr(self.file_path, 'evaluate') else self.file_path

        if not isinstance(path, str):
            raise TypeError(f"Путь к файлу должен быть строкой, получен {type(path)}")

        # ============================================================
        # DuckDBTable → потоковая запись
        # ============================================================
        if _is_duckdb(data_obj):
            try:
                safe_path = path.replace("'", "''").replace("\\", "\\\\")
                data_obj.con.execute(f"""
                    COPY (SELECT * FROM {data_obj.table_name})
                    TO '{safe_path}' (FORMAT PARQUET)
                """)
                rows = data_obj.get_row_count()
                cols = len(data_obj.get_columns())
                size_mb = os.path.getsize(path) / 1024 / 1024
                return (
                    f"Сохранено: {rows} строк, {cols} столбцов "
                    f"в Parquet '{os.path.basename(path)}' ({size_mb:.1f} МБ)"
                )
            except Exception as e:
                raise RuntimeError(f"Ошибка сохранения Parquet: {e}")

        # ============================================================
        # MatrExMatrix или list → через DuckDB
        # ============================================================
        if hasattr(data_obj, 'data'):
            raw = data_obj.data
        elif isinstance(data_obj, list):
            raw = data_obj
        else:
            raise TypeError(
                f"Данные должны быть матрицей или списком, получен {type(data_obj)}"
            )

        if raw and not isinstance(raw[0], list):
            data = [[item] for item in raw]
        else:
            data = raw

        if not data:
            raise ValueError("Нельзя сохранить пустую матрицу")

        try:
            import duckdb
            from duckdb_engine import get_global_connection

            con = get_global_connection()

            headers = data[0]
            rows = data[1:]

            import uuid
            table_name = f"tmp_{uuid.uuid4().hex[:8]}"

            # Собираем CREATE TABLE
            col_defs = []
            for h in headers:
                safe_h = '"' + str(h).replace('"', '""') + '"'
                col_defs.append(f"{safe_h} VARCHAR")

            con.execute(
                f"CREATE OR REPLACE TABLE {table_name} "
                f"({', '.join(col_defs)})"
            )

            # INSERT
            placeholders = ", ".join(["?"] * len(headers))
            con.executemany(
                f"INSERT INTO {table_name} VALUES ({placeholders})",
                rows,
            )

            # COPY в Parquet
            safe_path = path.replace("'", "''").replace("\\", "\\\\")
            con.execute(f"""
                COPY (SELECT * FROM {table_name})
                TO '{safe_path}' (FORMAT PARQUET)
            """)

            # Удаляем временную таблицу
            con.execute(f"DROP TABLE IF EXISTS {table_name}")

            size_mb = os.path.getsize(path) / 1024 / 1024
            return (
                f"Сохранено: {len(rows)} строк, {len(headers)} столбцов "
                f"в Parquet '{os.path.basename(path)}' ({size_mb:.1f} МБ)"
            )

        except ImportError:
            raise ImportError("DuckDB не установлен")

    def __repr__(self):
        return f"SaveParquet({self.data}, {self.file_path})"