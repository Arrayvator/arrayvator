# ast_nodes/functions/sqlite.py
"""
SQLite-функции ArrayVator:
    OpenSQLite      — открыть таблицу из базы (простой режим)
    QuerySQLite     — выполнить SQL-запрос (полный режим)
    SaveSQLite      — сохранить матрицу как таблицу
    OpenSQLiteShow  — диалог выбора .db + таблицы
    SaveSQLiteShow  — диалог сохранения

СИНТАКСИС:
    m = OpenSQLite("mydb.db", "employees")
    m = OpenSQLite("mydb.db", "employees", "age > 25")
    m = OpenSQLite("mydb.db", "employees", "age > 25", "name ASC")

    m = QuerySQLite("mydb.db", "SELECT * FROM employees WHERE age > 25")

    SaveSQLite(m, "mydb.db", "employees")              # если есть — спросит
    SaveSQLite(m, "mydb.db", "employees", overwrite)   # перезаписать без вопросов

    m = OpenSQLiteShow()
    SaveSQLiteShow(m)
"""

import os
import sqlite3
from ..base import Node


# ============================================================
# ВНУТРЕННИЕ ФУНКЦИИ
# ============================================================
def _check_file(path):
    if not os.path.exists(path):
        raise FileNotFoundError(f"Файл БД не найден: {path}")


def _get_table_names(conn):
    """Возвращает список таблиц в БД"""
    cursor = conn.cursor()
    cursor.execute(
        "SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%' ORDER BY name"
    )
    return [row[0] for row in cursor.fetchall()]


def _build_query(table, where=None, order_by=None):
    """Собирает SELECT-запрос из частей"""
    query = f"SELECT * FROM {_quote_ident(table)}"

    if where:
        query += f" WHERE {where}"

    if order_by:
        query += f" ORDER BY {order_by}"

    return query


def _quote_ident(name):
    """Экранирует имя таблицы/столбца"""
    return '"' + str(name).replace('"', '""') + '"'


def _execute_query(path, query):
    """Выполняет SQL-запрос, возвращает (columns, rows)"""
    _check_file(path)

    conn = sqlite3.connect(path)
    try:
        cursor = conn.cursor()
        cursor.execute(query)

        columns = [desc[0] for desc in cursor.description] if cursor.description else []
        rows = cursor.fetchall()

        return columns, rows
    except sqlite3.Error as e:
        raise RuntimeError(f"Ошибка SQL: {e}")
    finally:
        conn.close()


def _query_to_matrix(path, query):
    """Выполняет запрос, возвращает матрицу с заголовками"""
    from runtime.matrix import MatrExMatrix

    columns, rows = _execute_query(path, query)

    if not columns:
        return MatrExMatrix([], True)

    data = [list(columns)]
    for row in rows:
        data.append(list(row))

    return MatrExMatrix(data, True)


def _check_table_exists(conn, table_name):
    """Проверяет, есть ли таблица"""
    cursor = conn.cursor()
    cursor.execute(
        "SELECT name FROM sqlite_master WHERE type='table' AND name = ?",
        (table_name,)
    )
    return cursor.fetchone() is not None


def _infer_sqlite_type(values):
    """Определяет тип SQLite по значениям столбца"""
    types = set()
    for v in values:
        if v is None:
            continue
        if isinstance(v, bool):
            types.add('INTEGER')
        elif isinstance(v, int):
            types.add('INTEGER')
        elif isinstance(v, float):
            types.add('REAL')
        elif isinstance(v, str):
            types.add('TEXT')
        else:
            types.add('TEXT')

    if not types:
        return 'TEXT'
    if types == {'INTEGER'}:
        return 'INTEGER'
    if types == {'REAL'}:
        return 'REAL'
    if types == {'INTEGER', 'REAL'}:
        return 'REAL'
    return 'TEXT'


# ============================================================
# ДИАЛОГ «ПЕРЕЗАПИСАТЬ?»
# ============================================================
def _ask_overwrite_dialog(table_name, path):
    """
    Спрашивает пользователя о перезаписи таблицы.

    Возвращает:
        True  — перезаписать
        False — отменить
        None  — GUI недоступен
    """
    try:
        import tkinter as tk
        from tkinter import messagebox

        message = (
            f"Таблица '{table_name}' уже существует в базе\n"
            f"'{os.path.basename(path)}'.\n\n"
            f"Перезаписать?"
        )

        root = tk._default_root

        if root is None:
            # Нет активного окна — создаём своё
            temp_root = tk.Tk()
            temp_root.withdraw()
            try:
                answer = messagebox.askyesno(
                    "Таблица существует",
                    message,
                    parent=temp_root,
                )
                return bool(answer)
            finally:
                temp_root.destroy()
        else:
            # Используем активное окно
            answer = messagebox.askyesno(
                "Таблица существует",
                message,
                parent=root,
            )
            return bool(answer)

    except Exception:
        # GUI недоступен
        return None


# ============================================================
# СОХРАНЕНИЕ МАТРИЦЫ В ТАБЛИЦУ
# ============================================================
def _save_matrix_to_table(path, table_name, data, overwrite=False):
    """
    Сохраняет матрицу в таблицу SQLite.

    Возвращает:
        > 0  — количество добавленных строк
        -1   — пользователь отменил перезапись
    """
    if not path:
        raise ValueError("Не указан путь к БД")
    if not table_name:
        raise ValueError("Не указано имя таблицы")

    # Данные
    if hasattr(data, 'data'):
        raw = data.data
    elif isinstance(data, list):
        raw = data
    else:
        raise TypeError(f"Данные должны быть матрицей или списком, получен {type(data)}")

    if not raw:
        raise ValueError("Пустая матрица")

    # Вектор → матрица
    if raw and not isinstance(raw[0], list):
        raw = [[item] for item in raw]

    headers = raw[0]
    rows = raw[1:]

    if not headers:
        raise ValueError("Матрица не содержит заголовков")

    # Создаём подключение
    conn = sqlite3.connect(path)
    try:
        cursor = conn.cursor()

        # Проверка существования таблицы
        if _check_table_exists(conn, table_name):
            if not overwrite:
                # Спрашиваем через диалог
                confirmed = _ask_overwrite_dialog(table_name, path)

                if confirmed is None:
                    # GUI недоступен — ошибка
                    raise RuntimeError(
                        f"Таблица '{table_name}' уже существует в '{os.path.basename(path)}'.\n"
                        f"Используйте overwrite для перезаписи."
                    )

                if not confirmed:
                    # Пользователь отказался — не сохраняем
                    return -1

            # Перезаписываем
            cursor.execute(f"DROP TABLE {_quote_ident(table_name)}")

        # Собираем схему
        columns_sql = []
        for idx, col_name in enumerate(headers):
            col_values = []
            for row in rows:
                if idx < len(row):
                    col_values.append(row[idx])

            col_type = _infer_sqlite_type(col_values)
            columns_sql.append(f'{_quote_ident(col_name)} {col_type}')

        # CREATE TABLE
        create_sql = (
            f"CREATE TABLE {_quote_ident(table_name)} ("
            + ", ".join(columns_sql)
            + ")"
        )
        cursor.execute(create_sql)

        # INSERT
        placeholders = ", ".join(["?"] * len(headers))
        insert_sql = (
            f"INSERT INTO {_quote_ident(table_name)} "
            f"VALUES ({placeholders})"
        )
        cursor.executemany(insert_sql, rows)

        conn.commit()

        return len(rows)

    except sqlite3.Error as e:
        conn.rollback()
        raise RuntimeError(f"Ошибка SQLite: {e}")
    finally:
        conn.close()


# ============================================================
# УЗЛЫ
# ============================================================
class OpenSQLiteNode(Node):
    """OpenSQLite("path.db", "table" [, where] [, order_by])"""

    def __init__(self, file_path, table_name, where=None, order_by=None):
        self.file_path = file_path
        self.table_name = table_name
        self.where = where
        self.order_by = order_by

    def evaluate(self, env):
        path = self.file_path.evaluate(env) if hasattr(self.file_path, 'evaluate') else self.file_path
        table = self.table_name.evaluate(env) if hasattr(self.table_name, 'evaluate') else self.table_name
        where = None
        if self.where is not None:
            where = self.where.evaluate(env) if hasattr(self.where, 'evaluate') else self.where
        order_by = None
        if self.order_by is not None:
            order_by = self.order_by.evaluate(env) if hasattr(self.order_by, 'evaluate') else self.order_by

        if not isinstance(path, str):
            raise TypeError(f"Путь к БД должен быть строкой, получен {type(path)}")
        if not isinstance(table, str):
            raise TypeError(f"Имя таблицы должно быть строкой, получен {type(table)}")
        if where is not None and not isinstance(where, str):
            raise TypeError(f"WHERE должно быть строкой, получен {type(where)}")
        if order_by is not None and not isinstance(order_by, str):
            raise TypeError(f"ORDER BY должно быть строкой, получен {type(order_by)}")

        query = _build_query(table, where, order_by)
        return _query_to_matrix(path, query)

    def __repr__(self):
        parts = [f"OpenSQLite({self.file_path}, {self.table_name}"]
        if self.where is not None:
            parts.append(f", {self.where}")
        if self.order_by is not None:
            parts.append(f", {self.order_by}")
        parts.append(")")
        return "".join(parts)


class QuerySQLiteNode(Node):
    """QuerySQLite("path.db", "SELECT ...")"""

    def __init__(self, file_path, query):
        self.file_path = file_path
        self.query = query

    def evaluate(self, env):
        path = self.file_path.evaluate(env) if hasattr(self.file_path, 'evaluate') else self.file_path
        query = self.query.evaluate(env) if hasattr(self.query, 'evaluate') else self.query

        if not isinstance(path, str):
            raise TypeError(f"Путь к БД должен быть строкой, получен {type(path)}")
        if not isinstance(query, str):
            raise TypeError(f"Запрос должен быть строкой, получен {type(query)}")

        return _query_to_matrix(path, query)

    def __repr__(self):
        return f"QuerySQLite({self.file_path}, {self.query})"


class SaveSQLiteNode(Node):
    """SaveSQLite(data, "path.db", "table" [, overwrite])"""

    def __init__(self, data, file_path, table_name, overwrite=None):
        self.data = data
        self.file_path = file_path
        self.table_name = table_name
        self.overwrite = overwrite

    def evaluate(self, env):
        data_obj = self.data.evaluate(env)
        path = self.file_path.evaluate(env) if hasattr(self.file_path, 'evaluate') else self.file_path
        table = self.table_name.evaluate(env) if hasattr(self.table_name, 'evaluate') else self.table_name
        ow = False
        if self.overwrite is not None:
            ow_val = self.overwrite.evaluate(env) if hasattr(self.overwrite, 'evaluate') else self.overwrite
            ow = bool(ow_val)

        if not isinstance(path, str):
            raise TypeError(f"Путь к БД должен быть строкой, получен {type(path)}")
        if not isinstance(table, str):
            raise TypeError(f"Имя таблицы должно быть строкой, получен {type(table)}")

        rows_count = _save_matrix_to_table(path, table, data_obj, ow)

        # -1 → пользователь отменил
        if rows_count == -1:
            return f"Сохранение отменено: таблица '{table}' не перезаписана"

        return f"Сохранено: {rows_count} строк в таблицу '{table}' в '{os.path.basename(path)}'"

    def __repr__(self):
        if self.overwrite is not None:
            return f"SaveSQLite({self.data}, {self.file_path}, {self.table_name}, {self.overwrite})"
        return f"SaveSQLite({self.data}, {self.file_path}, {self.table_name})"


class OpenSQLiteShowNode(Node):
    """OpenSQLiteShow() — диалог выбора .db и таблицы"""

    def __init__(self):
        pass

    def evaluate(self, env):
        import tkinter as tk
        from tkinter import filedialog, messagebox

        root = tk.Tk()
        root.withdraw()

        path = filedialog.askopenfilename(
            title="Выберите SQLite базу данных",
            filetypes=[
                ("SQLite databases", "*.db *.sqlite *.sqlite3"),
                ("All files", "*.*"),
            ],
        )

        if not path:
            root.destroy()
            return None

        # Список таблиц
        try:
            conn = sqlite3.connect(path)
            tables = _get_table_names(conn)
            conn.close()
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось открыть БД:\n{e}")
            root.destroy()
            return None

        if not tables:
            messagebox.showinfo("Информация", "В базе нет таблиц")
            root.destroy()
            return None

        # Диалог выбора таблицы
        root.deiconify()
        root.title("Выбор таблицы")
        root.geometry("400x300")

        tk.Label(root, text="Выберите таблицу:", font=("Arial", 12, "bold")).pack(pady=10)

        listbox = tk.Listbox(root, font=("Consolas", 11), height=10)
        listbox.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        for t in tables:
            listbox.insert(tk.END, t)

        if tables:
            listbox.selection_set(0)

        result = {"table": None}

        def on_ok():
            sel = listbox.curselection()
            if sel:
                result["table"] = tables[sel[0]]
            root.quit()
            root.destroy()

        def on_cancel():
            root.quit()
            root.destroy()

        btn_frame = tk.Frame(root)
        btn_frame.pack(pady=10)

        tk.Button(btn_frame, text="OK", command=on_ok,
                  width=12, bg="#90EE90").pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Отмена", command=on_cancel,
                  width=12, bg="#FF6B6B", fg="white").pack(side=tk.LEFT, padx=5)

        root.mainloop()

        if not result["table"]:
            return None

        query = _build_query(result["table"])
        return _query_to_matrix(path, query)

    def __repr__(self):
        return "OpenSQLiteShow()"


class SaveSQLiteShowNode(Node):
    """SaveSQLiteShow(data) — диалог сохранения"""

    def __init__(self, data):
        self.data = data

    def evaluate(self, env):
        import tkinter as tk
        from tkinter import filedialog, simpledialog, messagebox

        data_obj = self.data.evaluate(env)

        root = tk.Tk()
        root.withdraw()

        path = filedialog.asksaveasfilename(
            title="Сохранить в SQLite БД",
            defaultextension=".db",
            filetypes=[
                ("SQLite databases", "*.db"),
                ("All files", "*.*"),
            ],
        )

        if not path:
            root.destroy()
            return "Сохранение отменено"

        table_name = simpledialog.askstring(
            "Имя таблицы",
            "Введите имя таблицы:",
            initialvalue="table1",
            parent=root,
        )

        if not table_name:
            root.destroy()
            return "Сохранение отменено"

        root.destroy()

        # _save_matrix_to_table сам покажет диалог при необходимости
        rows_count = _save_matrix_to_table(path, table_name, data_obj, False)

        if rows_count == -1:
            return f"Сохранение отменено: таблица '{table_name}' не перезаписана"

        return f"Сохранено: {rows_count} строк в таблицу '{table_name}'"

    def __repr__(self):
        return f"SaveSQLiteShow({self.data})"