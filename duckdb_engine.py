# duckdb_engine.py
"""
Движок для больших данных на DuckDB.
"""

import os
import tempfile
import duckdb


DUCKDB_THRESHOLD = 250 * 1024 * 1024  # 250 МБ
MAX_PRINT_ROWS = 20
MAX_SHOW_ROWS = 1000


# ============================================================
# ГЛОБАЛЬНОЕ СОЕДИНЕНИЕ
# ============================================================
# Все DuckDBTable используют ОДНО соединение, чтобы JOIN, UNPIVOT
# и другие операции могли ссылаться на таблицы друг друга по имени.
_GLOBAL_CON = None


def get_global_connection():
    """Возвращает глобальное соединение DuckDB (создаёт при первом вызове)."""
    global _GLOBAL_CON
    if _GLOBAL_CON is None:
        _GLOBAL_CON = duckdb.connect()
    return _GLOBAL_CON


def should_use_duckdb(path):
    if not os.path.exists(path):
        return False
    return os.path.getsize(path) >= DUCKDB_THRESHOLD


def _detect_encoding(path):
    """Определяет кодировку CSV по первой строке."""
    for enc in ['utf-8', 'cp1251', 'utf-16', 'latin-1', 'koi8-r']:
        try:
            with open(path, 'r', encoding=enc) as f:
                f.readline()
            return enc
        except (UnicodeDecodeError, LookupError):
            continue
    return 'utf-8'


def _ensure_utf8(path):
    """Проверяет, что файл в UTF-8. Если нет — создаёт временную копию."""
    encoding = _detect_encoding(path)

    if encoding == 'utf-8':
        return path, False

    try:
        with open(path, 'r', encoding=encoding, errors='replace') as f:
            content = f.read()
    except Exception as e:
        raise RuntimeError(f"Не удалось прочитать файл как {encoding}: {e}")

    tmp = tempfile.NamedTemporaryFile(
        mode='w',
        suffix='.utf8.csv',
        delete=False,
        encoding='utf-8',
        newline='',
    )
    tmp.write(content)
    tmp.close()

    return tmp.name, True


class DuckDBTable:
    def __init__(self, path, table_name=None, connection=None):
        self.path = path
        self.table_name = table_name or self._make_table_name(path)

        # ============================================================
        # ВАЖНО: используем ГЛОБАЛЬНОЕ соединение,
        # чтобы все таблицы были видны друг другу (JOIN, UNPIVOT).
        # ============================================================
        self.con = connection or get_global_connection()

        self.utf8_path, self.is_temp = _ensure_utf8(path)
        self._tmp_path = self.utf8_path if self.is_temp else None

        self._register()

    def _make_table_name(self, path):
        base = os.path.basename(path).replace('.', '_').replace(' ', '_')
        clean = ''.join(c if c.isalnum() or c == '_' else '_' for c in base)
        return f"t_{clean}"

    def _detect_delimiter(self):
        try:
            with open(self.utf8_path, 'r', encoding='utf-8', errors='replace') as f:
                first_line = f.readline()

            candidates = [',', ';', '\t', '|']
            counts = {d: first_line.count(d) for d in candidates}
            best = max(counts, key=counts.get)

            if counts[best] == 0:
                return ','
            return best
        except Exception:
            return ','

    def _register(self):
        """
        Регистрирует view на CSV-файл.

        ВАЖНО:
            sample_size=20000    — читать первые 20000 строк для детекции типов
            ignore_errors=false  — падать при ошибке парсинга, а не молча терять строки
            new_line             — НЕ указываем, DuckDB сам определяет \\n / \\r\\n / \\r
        """
        safe_path = self.utf8_path.replace("'", "''").replace("\\", "\\\\")
        delimiter = self._detect_delimiter()

        if delimiter == '\t':
            delim_sql = '\\t'
        else:
            delim_sql = delimiter

        self.con.execute(f"""
            CREATE OR REPLACE VIEW {self.table_name} AS
            SELECT * FROM read_csv_auto('{safe_path}', 
                                        sample_size=20000,
                                        ignore_errors=false,
                                        header=true,
                                        delim='{delim_sql}')
        """)

    # ============================================================
    # ПОДСЧЁТ СТРОК
    # ============================================================
    def _count_data(self):
        """
        Количество ДАННЫХ (без заголовка).
        Для внутренних нужд движка (LIMIT, превью и т.п.).
        """
        return self.con.execute(
            f"SELECT COUNT(*) FROM {self.table_name}"
        ).fetchone()[0]

    def get_row_count(self):
        """
        Количество строк ВКЛЮЧАЯ ЗАГОЛОВОК.
        Согласовано с Matrix: lenrow(m) = 5 для 4 строк данных.

        В Matrix data[0] — заголовок, поэтому lenrow = 5.
        В DuckDB view содержит только данные, поэтому +1.
        """
        return self._count_data() + 1

    # ============================================================
    # ДОСТУП К ДАННЫМ
    # ============================================================
    def get_columns(self):
        result = self.con.execute(
            f"SELECT * FROM {self.table_name} LIMIT 0"
        ).description
        return [col[0] for col in result]

    def query(self, sql):
        return self.con.execute(sql).fetchall()

    def query_to_matrix(self, sql):
        from runtime.matrix import MatrExMatrix
        rows = self.con.execute(sql).fetchall()
        data = [list(row) for row in rows]
        return MatrExMatrix(data, True)

    def get_data_for_show(self, limit=MAX_SHOW_ROWS):
        try:
            data = self.query(
                f"SELECT * FROM {self.table_name} LIMIT {limit}"
            )
            return [list(row) for row in data]
        except Exception as e:
            print(f"DuckDB get_data_for_show error: {e}")
            return [[""]]

    def get_headers(self):
        return self.get_columns()

    def get_column_type(self, col_name):
        try:
            safe_col = '"' + str(col_name).replace('"', '""') + '"'
            result = self.con.execute(
                f'SELECT typeof({safe_col}) FROM {self.table_name} LIMIT 1'
            ).fetchone()
            return result[0] if result else 'VARCHAR'
        except Exception:
            return 'VARCHAR'

    def close(self):
        # ============================================================
        # Не закрываем глобальное соединение —
        # оно общее для всех таблиц.
        # ============================================================
        try:
            if self.con is not None and self.con is not get_global_connection():
                self.con.close()
        except Exception:
            pass
        self.con = None

        if self._tmp_path and os.path.exists(self._tmp_path):
            try:
                os.remove(self._tmp_path)
            except Exception:
                pass
            self._tmp_path = None

    def __str__(self):
        try:
            # Внутренний подсчёт использует _count_data (без заголовка)
            data_rows = self._count_data()
            cols = len(self.get_columns())
            columns = self.get_columns()

            preview_rows = min(MAX_PRINT_ROWS, data_rows)
            data = self.query(
                f"SELECT * FROM {self.table_name} LIMIT {preview_rows}"
            )

            lines = self._format_table(columns, data)

            if data_rows > MAX_PRINT_ROWS:
                lines.append(f"... (всего {data_rows} строк × {cols} столбцов)")
            else:
                lines.append(f"({data_rows} строк × {cols} столбцов)")

            return "\n".join(lines)

        except Exception as e:
            import traceback
            return f"DuckDBTable({self.table_name}, ошибка: {e})\n{traceback.format_exc()}"

    def _format_table(self, columns, rows):
        if not rows:
            return ["(пусто)"]

        widths = []
        for i, col in enumerate(columns):
            max_width = len(str(col))
            for row in rows:
                if i < len(row):
                    max_width = max(max_width, len(str(row[i])))
            widths.append(max_width)

        lines = []
        header = "  ".join(
            str(col).ljust(widths[i])
            for i, col in enumerate(columns)
        )
        lines.append(header)
        lines.append("-" * len(header))

        for row in rows:
            line = "  ".join(
                str(row[i] if i < len(row) else "").ljust(widths[i])
                for i in range(len(columns))
            )
            lines.append(line)

        return lines

    def __repr__(self):
        return self.__str__()


def escape_identifier(name):
    return '"' + str(name).replace('"', '""') + '"'


def escape_value(value):
    if value is None:
        return "NULL"
    if isinstance(value, bool):
        return "TRUE" if value else "FALSE"
    if isinstance(value, (int, float)):
        return str(value)
    return "'" + str(value).replace("'", "''") + "'"