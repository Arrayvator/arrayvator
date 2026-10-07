# ast_nodes/functions/txt.py
"""
TXT-функции ArrayVator:
    OpenTXT      — загрузка из TXT
    SaveTXT      — сохранение в TXT
    OpenTXTShow  — загрузка через диалог
    SaveTXTShow  — сохранение через диалог

TXT — это файл с разделителем. По умолчанию:
    - Загрузка: автоопределение (, ; \t |)
    - Сохранение: ";"

СИНТАКСИС:
    m = OpenTXT("data.txt")
    m = OpenTXT("data.txt", ";")
    m = OpenTXT("data.txt", "\t")
    SaveTXT(m, "out.txt")
    SaveTXT(m, "out.txt", "\t")
"""

import csv
import os
from ..base import Node


# ============================================================
# РАЗДЕЛИТЕЛИ
# ============================================================
VALID_DELIMITERS = [',', ';', '\t', '|', ' ']

DEFAULT_SAVE_DELIMITER = ';'


def _normalize_delimiter(delim):
    """Приводит разделитель к 1 символу"""
    if delim is None:
        return None

    if not isinstance(delim, str):
        raise TypeError(f"Разделитель должен быть строкой, получен {type(delim)}")

    if len(delim) == 0:
        raise ValueError("Разделитель не может быть пустым")

    # Специальные последовательности
    if delim == '\\t':
        return '\t'
    if delim == '\\n':
        return '\n'

    if len(delim) > 1:
        raise ValueError(
            f"Разделитель должен быть 1 символ, получено '{delim}'. "
            f"Используйте '\\t' для табуляции."
        )

    return delim


def _detect_delimiter(sample):
    """Определяет разделитель по первой строке"""
    best = ','
    best_count = 0
    for d in VALID_DELIMITERS:
        count = sample.count(d)
        if count > best_count:
            best_count = count
            best = d
    return best


def _read_file(path):
    """Читает TXT с автоопределением кодировки"""
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


def load_txt(path, delimiter=None):
    """Загружает TXT в список списков"""
    if not os.path.exists(path):
        raise FileNotFoundError(f"Файл не найден: {path}")

    content, encoding = _read_file(path)
    if not content:
        return [[""]]

    # Разделитель
    if delimiter is not None:
        delim = _normalize_delimiter(delimiter)
    else:
        first_line = content.split('\n', 1)[0]
        delim = _detect_delimiter(first_line)

    # Парсим
    rows = []
    reader = csv.reader(content.splitlines(), delimiter=delim)
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


def save_txt(data, path, delimiter=DEFAULT_SAVE_DELIMITER):
    """Сохраняет матрицу в TXT"""
    if not path:
        raise ValueError("Не указан путь к файлу")

    delim = _normalize_delimiter(delimiter) or DEFAULT_SAVE_DELIMITER

    with open(path, 'w', encoding='utf-8-sig', newline='') as f:
        writer = csv.writer(f, delimiter=delim, quoting=csv.QUOTE_MINIMAL)
        for row in data:
            if not isinstance(row, list):
                row = [row]
            writer.writerow(row)


# ============================================================
# УЗЛЫ
# ============================================================
class OpenTXTNode(Node):
    """OpenTXT('file.txt' [, delimiter])"""

    def __init__(self, file_path, delimiter=None):
        self.file_path = file_path
        self.delimiter = delimiter

    def evaluate(self, env):
        from runtime.matrix import MatrExMatrix

        path = self.file_path.evaluate(env) if hasattr(self.file_path, 'evaluate') else self.file_path
        delim = None
        if self.delimiter is not None:
            delim = self.delimiter.evaluate(env) if hasattr(self.delimiter, 'evaluate') else self.delimiter

        if not isinstance(path, str):
            raise TypeError(f"Путь к файлу должен быть строкой, получен {type(path)}")

        data = load_txt(path, delim)
        return MatrExMatrix(data, True)

    def __repr__(self):
        if self.delimiter is not None:
            return f"OpenTXT({self.file_path}, {self.delimiter})"
        return f"OpenTXT({self.file_path})"


class SaveTXTNode(Node):
    """SaveTXT(data, 'file.txt' [, delimiter])"""

    def __init__(self, data, file_path, delimiter=None):
        self.data = data
        self.file_path = file_path
        self.delimiter = delimiter

    def evaluate(self, env):
        data_obj = self.data.evaluate(env)
        path = self.file_path.evaluate(env) if hasattr(self.file_path, 'evaluate') else self.file_path
        delim = None
        if self.delimiter is not None:
            delim = self.delimiter.evaluate(env) if hasattr(self.delimiter, 'evaluate') else self.delimiter

        if not isinstance(path, str):
            raise TypeError(f"Путь к файлу должен быть строкой, получен {type(path)}")

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

        save_txt(data, path, delim or DEFAULT_SAVE_DELIMITER)

        rows = len(data)
        cols = max((len(r) for r in data), default=0)
        return f"Сохранено: {rows} строк, {cols} столбцов в TXT '{os.path.basename(path)}'"

    def __repr__(self):
        if self.delimiter is not None:
            return f"SaveTXT({self.data}, {self.file_path}, {self.delimiter})"
        return f"SaveTXT({self.data}, {self.file_path})"


class OpenTXTShowNode(Node):
    """OpenTXTShow([delimiter])"""

    def __init__(self, delimiter=None):
        self.delimiter = delimiter

    def evaluate(self, env):
        from runtime.matrix import MatrExMatrix
        import tkinter as tk
        from tkinter import filedialog

        delim = None
        if self.delimiter is not None:
            delim = self.delimiter.evaluate(env) if hasattr(self.delimiter, 'evaluate') else self.delimiter

        root = tk.Tk()
        root.withdraw()
        path = filedialog.askopenfilename(
            title="Выберите TXT-файл",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
        )
        root.destroy()

        if not path:
            return None

        data = load_txt(path, delim)
        return MatrExMatrix(data, True)

    def __repr__(self):
        if self.delimiter is not None:
            return f"OpenTXTShow({self.delimiter})"
        return "OpenTXTShow()"


class SaveTXTShowNode(Node):
    """SaveTXTShow(data [, delimiter])"""

    def __init__(self, data, delimiter=None):
        self.data = data
        self.delimiter = delimiter

    def evaluate(self, env):
        import tkinter as tk
        from tkinter import filedialog

        data_obj = self.data.evaluate(env)
        delim = None
        if self.delimiter is not None:
            delim = self.delimiter.evaluate(env) if hasattr(self.delimiter, 'evaluate') else self.delimiter

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

        root = tk.Tk()
        root.withdraw()
        path = filedialog.asksaveasfilename(
            title="Сохранить как TXT",
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
        )
        root.destroy()

        if not path:
            return "Сохранение отменено"

        save_txt(data, path, delim or DEFAULT_SAVE_DELIMITER)

        rows = len(data)
        cols = max((len(r) for r in data), default=0)
        return f"Сохранено: {rows} строк, {cols} столбцов в '{os.path.basename(path)}'"

    def __repr__(self):
        if self.delimiter is not None:
            return f"SaveTXTShow({self.data}, {self.delimiter})"
        return f"SaveTXTShow({self.data})"