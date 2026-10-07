# ast_nodes/functions/csv.py
"""
CSV-функции ArrayVator:
    OpenCSV         — загрузка из CSV
    SaveCSV         — сохранение в CSV
    OpenCSVShow     — загрузка через диалог (GUI)
    SaveCSVShow     — сохранение через диалог (GUI)

РЕЖИМЫ ОТКРЫТИЯ:
    OpenCSV("file.csv")               — авто (по размеру файла)
    OpenCSV("file.csv", BigData)      — принудительно DuckDB
    OpenCSV("file.csv", Table)        — принудительно MatrExMatrix (RAM)
"""

import csv
import os
from ..base import Node


# ============================================================
# ОПРЕДЕЛЕНИЕ РАЗДЕЛИТЕЛЯ
# ============================================================
def _detect_delimiter(sample):
    """Определяет разделитель по первой строке"""
    candidates = [',', ';', '\t', '|']
    best = ','
    best_count = 0
    for d in candidates:
        count = sample.count(d)
        if count > best_count:
            best_count = count
            best = d
    return best


# ============================================================
# ЧТЕНИЕ ФАЙЛА
# ============================================================
def _read_csv_file(path):
    """Читает CSV с автоопределением кодировки"""
    encodings = ['utf-8-sig', 'utf-8', 'cp1251', 'latin-1']
    last_error = None
    for enc in encodings:
        try:
            with open(path, 'r', encoding=enc, newline='') as f:
                content = f.read()
            return content, enc
        except (UnicodeDecodeError, LookupError) as e:
            last_error = e
            continue
    raise RuntimeError(f"Не удалось прочитать файл: {last_error}")


def _auto_convert(cell):
    """Пытается преобразовать строку в число"""
    if cell == "":
        return ""
    try:
        if '.' not in cell and ',' not in cell:
            return int(cell)
    except ValueError:
        pass
    try:
        if '.' in cell and ',' not in cell:
            return float(cell)
    except ValueError:
        pass
    try:
        if ',' in cell and '.' not in cell:
            return float(cell.replace(',', '.'))
    except ValueError:
        pass
    return cell


# ============================================================
# ЗАГРУЗКА CSV (для RAM)
# ============================================================
def load_csv(path):
    """Загружает CSV в список списков"""
    if not os.path.exists(path):
        raise FileNotFoundError(f"Файл не найден: {path}")

    content, encoding = _read_csv_file(path)
    if not content:
        return [[""]]

    first_line = content.split('\n', 1)[0]
    delimiter = _detect_delimiter(first_line)

    rows = []
    reader = csv.reader(content.splitlines(), delimiter=delimiter)
    for row in reader:
        if not row or all(cell == '' for cell in row):
            continue
        cleaned = [cell.strip() for cell in row]
        converted = [_auto_convert(cell) for cell in cleaned]
        rows.append(converted)

    if not rows:
        return [[""]]

    max_cols = max(len(r) for r in rows)
    for r in rows:
        while len(r) < max_cols:
            r.append("")

    return rows


# ============================================================
# СОХРАНЕНИЕ CSV
# ============================================================
def save_csv(data, path, delimiter=','):
    """
    Сохраняет матрицу в CSV.

    ВАЖНО:
        После последней строки гарантированно пишется '\\n'.
        Без этого DuckDB read_csv_auto с ignore_errors=true
        МОЛЧА теряет последнюю строку.
    """
    if not path:
        raise ValueError("Не указан путь к файлу")

    with open(path, 'w', encoding='utf-8-sig', newline='') as f:
        writer = csv.writer(
            f,
            delimiter=delimiter,
            quoting=csv.QUOTE_MINIMAL,
            lineterminator='\n',
        )
        for row in data:
            if not isinstance(row, list):
                row = [row]
            writer.writerow(row)

        # ============================================================
        # ФИНАЛЬНЫЙ ПЕРЕВОД СТРОКИ — критично для DuckDB
        # ============================================================
        f.write('\n')


# ============================================================
# ДИСПЕТЧЕР ОТКРЫТИЯ
# ============================================================
def _open_csv_dispatch(path, mode=None):
    """
    Открывает CSV с выбором движка:

    mode=None      → авто (по размеру файла)
    mode='duckdb'  → принудительно DuckDB (BigData)
    mode='matrix'  → принудительно MatrExMatrix (Table)
    """
    from runtime.matrix import MatrExMatrix

    # ============================================================
    # ВАЛИДАЦИЯ РЕЖИМА
    # ============================================================
    if mode is not None:
        if not isinstance(mode, str):
            raise TypeError(
                f"Режим OpenCSV должен быть строкой, "
                f"получен {type(mode).__name__}.\n"
                f"  Допустимо: BigData, Table."
            )
        mode = mode.strip().lower()
        if mode not in ('matrix', 'duckdb'):
            raise ValueError(
                f"Неверный режим OpenCSV: '{mode}'.\n"
                f"  Допустимо:\n"
                f"     OpenCSV(\"file.csv\")               — авто\n"
                f"     OpenCSV(\"file.csv\", BigData)      — DuckDB\n"
                f"     OpenCSV(\"file.csv\", Table)        — RAM"
            )

    # ============================================================
    # TABLE — принудительно RAM
    # ============================================================
    if mode == 'matrix':
        data = load_csv(path)
        return MatrExMatrix(data, True)

    # ============================================================
    # BIGDATA — принудительно DuckDB
    # ============================================================
    if mode == 'duckdb':
        try:
            from duckdb_engine import DuckDBTable
            return DuckDBTable(path)
        except ImportError:
            raise ImportError(
                "DuckDB не установлен.\n"
                "Режим BigData требует DuckDB.\n"
                "Установите: pip install duckdb"
            )

    # ============================================================
    # АВТО — по размеру файла
    # ============================================================
    try:
        from duckdb_engine import should_use_duckdb, DuckDBTable

        if should_use_duckdb(path):
            return DuckDBTable(path)
    except ImportError:
        pass

    data = load_csv(path)
    return MatrExMatrix(data, True)


# ============================================================
# OPEN CSV
# ============================================================
class OpenCSVNode(Node):
    """
    OpenCSV("file.csv")
    OpenCSV("file.csv", BigData)     — принудительно DuckDB
    OpenCSV("file.csv", Table)        — принудительно RAM
    """

    def __init__(self, file_path, mode=None):
        self.file_path = file_path
        self.mode = mode

    def evaluate(self, env):
        path = self.file_path.evaluate(env) if hasattr(self.file_path, 'evaluate') else self.file_path
        if not isinstance(path, str):
            raise TypeError(f"Путь к файлу должен быть строкой, получен {type(path)}")

        if not os.path.exists(path):
            raise FileNotFoundError(f"Файл не найден: {path}")

        mode_val = None
        if self.mode is not None:
            mode_val = (self.mode.evaluate(env)
                        if hasattr(self.mode, 'evaluate')
                        else self.mode)
            if isinstance(mode_val, str):
                mode_val = mode_val.strip().lower()

        return _open_csv_dispatch(path, mode_val)

    def __repr__(self):
        if self.mode is None:
            return f"OpenCSV({self.file_path})"
        return f"OpenCSV({self.file_path}, {self.mode})"


# ============================================================
# SAVE CSV
# ============================================================
class SaveCSVNode(Node):
    def __init__(self, data, file_path):
        self.data = data
        self.file_path = file_path

    def evaluate(self, env):
        data_obj = self.data.evaluate(env)
        path = self.file_path.evaluate(env) if hasattr(self.file_path, 'evaluate') else self.file_path

        if not isinstance(path, str):
            raise TypeError(f"Путь к файлу должен быть строкой, получен {type(path)}")

        # DuckDBTable → потоковая запись
        try:
            from duckdb_engine import DuckDBTable

            if isinstance(data_obj, DuckDBTable):
                safe_path = path.replace("'", "''")
                data_obj.con.execute(f"""
                    COPY (SELECT * FROM {data_obj.table_name})
                    TO '{safe_path}' (FORMAT CSV, HEADER, DELIMITER ',')
                """)
                rows = data_obj.get_row_count()
                cols = len(data_obj.get_columns())
                return f"Сохранено: {rows} строк, {cols} столбцов в CSV '{os.path.basename(path)}'"
        except ImportError:
            pass

        # MatrExMatrix или list
        if hasattr(data_obj, 'data'):
            raw = data_obj.data
        elif isinstance(data_obj, list):
            raw = data_obj
        else:
            raise TypeError(f"Данные должны быть матрицей или списком, получен {type(data_obj)}")

        if raw and not isinstance(raw[0], list):
            data = [[item] for item in raw]
        else:
            data = raw

        save_csv(data, path)
        rows = len(data)
        cols = max((len(r) for r in data), default=0)
        return f"Сохранено: {rows} строк, {cols} столбцов в CSV '{os.path.basename(path)}'"

    def __repr__(self):
        return f"SaveCSV({self.data}, {self.file_path})"


# ============================================================
# OPEN CSV SHOW
# ============================================================
class OpenCSVShowNode(Node):
    """
    OpenCSVShow()
    OpenCSVShow(BigData)     — принудительно DuckDB
    OpenCSVShow(Table)        — принудительно RAM
    """

    def __init__(self, mode=None):
        self.mode = mode

    def evaluate(self, env):
        import tkinter as tk
        from tkinter import filedialog

        root = tk.Tk()
        root.withdraw()
        path = filedialog.askopenfilename(
            title="Выберите CSV-файл",
            filetypes=[
                ("CSV files", "*.csv"),
                ("Text files", "*.txt"),
                ("All files", "*.*"),
            ],
        )
        root.destroy()

        if not path:
            return None

        mode_val = None
        if self.mode is not None:
            mode_val = (self.mode.evaluate(env)
                        if hasattr(self.mode, 'evaluate')
                        else self.mode)
            if isinstance(mode_val, str):
                mode_val = mode_val.strip().lower()

        return _open_csv_dispatch(path, mode_val)

    def __repr__(self):
        if self.mode is None:
            return "OpenCSVShow()"
        return f"OpenCSVShow({self.mode})"


# ============================================================
# SAVE CSV SHOW
# ============================================================
class SaveCSVShowNode(Node):
    def __init__(self, data):
        self.data = data

    def evaluate(self, env):
        import tkinter as tk
        from tkinter import filedialog

        data_obj = self.data.evaluate(env)

        root = tk.Tk()
        root.withdraw()
        path = filedialog.asksaveasfilename(
            title="Сохранить как CSV",
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
        )
        root.destroy()

        if not path:
            return "Сохранение отменено"

        # DuckDBTable → потоковая запись
        try:
            from duckdb_engine import DuckDBTable

            if isinstance(data_obj, DuckDBTable):
                safe_path = path.replace("'", "''")
                data_obj.con.execute(f"""
                    COPY (SELECT * FROM {data_obj.table_name})
                    TO '{safe_path}' (FORMAT CSV, HEADER, DELIMITER ',')
                """)
                rows = data_obj.get_row_count()
                cols = len(data_obj.get_columns())
                return f"Сохранено: {rows} строк, {cols} столбцов в '{os.path.basename(path)}'"
        except ImportError:
            pass

        # MatrExMatrix или list
        if hasattr(data_obj, 'data'):
            raw = data_obj.data
        elif isinstance(data_obj, list):
            raw = data_obj
        else:
            raise TypeError(f"Данные должны быть матрицей или списком, получен {type(data_obj)}")

        if raw and not isinstance(raw[0], list):
            data = [[item] for item in raw]
        else:
            data = raw

        save_csv(data, path)
        rows = len(data)
        cols = max((len(r) for r in data), default=0)
        return f"Сохранено: {rows} строк, {cols} столбцов в '{os.path.basename(path)}'"

    def __repr__(self):
        return f"SaveCSVShow({self.data})"