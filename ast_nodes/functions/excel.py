# ast_nodes/functions/excel.py
"""
Excel-функции ArrayVator:

    OpenExcel      — загрузка (python-calamine, ~10x быстрее openpyxl)
    SaveExcel      — сохранение (pyexcelerate для новых, openpyxl для существующих)
    OpenExcelShow  — диалог открытия + выбор листов
    SaveExcelShow  — диалог сохранения

ЧТЕНИЕ: python-calamine (Rust/calamine)
ЗАПИСЬ: pyexcelerate (быстро) + openpyxl (для дописывания)

СИНТАКСИС:
    OpenExcel("file.xlsx")               — первый лист
    OpenExcel("file.xlsx", "Лист1")      — по имени
    OpenExcel("file.xlsx", 1)            — по номеру (1-based)
    OpenExcel("file.xlsx", all)          — все листы, склеенные подряд

    OpenExcelShow()                      — диалог + выбор листов
    OpenExcelShow(all)                   — диалог + все листы

    SaveExcel(data, "file.xlsx" [, "Лист1"])
    SaveExcelShow(data [, "Лист1"])
"""

import os

# ================================================================
# ЧТЕНИЕ: python-calamine
# ================================================================
try:
    from python_calamine import CalamineWorkbook
    CALAMINE_AVAILABLE = True
except ImportError:
    CALAMINE_AVAILABLE = False

# ================================================================
# ЗАПИСЬ: pyexcelerate (быстро, только новый файл)
# ================================================================
try:
    from pyexcelerate import Workbook as PyExcelerateWorkbook
    PYXECELERATE_AVAILABLE = True
except ImportError:
    PYXECELERATE_AVAILABLE = False

# ================================================================
# ЗАПИСЬ: openpyxl (дописывание в существующий)
# ================================================================
try:
    from openpyxl import Workbook as OpenpyxlWorkbook, load_workbook
    OPENPYXL_AVAILABLE = True
except ImportError:
    OPENPYXL_AVAILABLE = False

from ..base import Node


# ================================================================
# ОБЩАЯ ФУНКЦИЯ ЧТЕНИЯ
# ================================================================
def _read_excel_to_matrix(file_path, sheet_param_value=None):
    """
    Читает Excel через python-calamine и возвращает MatrExMatrix.

    sheet_param_value:
        None        — первый лист
        "all"       — все листы, склеенные подряд
        "Лист1"     — по имени
        1, 2, ...   — по номеру (1-based)
    """
    from runtime.matrix import MatrExMatrix

    if not CALAMINE_AVAILABLE:
        raise ImportError(
            "python-calamine не установлен.\n"
            "Установите: pip install python-calamine"
        )

    if not isinstance(file_path, str):
        raise TypeError(
            f"Путь к файлу должен быть строкой, получен {type(file_path)}"
        )

    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Файл не найден: {file_path}")

    try:
        workbook = CalamineWorkbook.from_path(file_path)
        sheet_names = workbook.sheet_names

        if not sheet_names:
            return MatrExMatrix([[""]], True)

        # 1. Первый лист
        if sheet_param_value is None:
            sheet = workbook.get_sheet_by_index(0)
            data = _normalize_sheet(sheet.to_python())
            return MatrExMatrix(data, True)

        # 2. all — все листы подряд
        if sheet_param_value == 'all':
            return _load_all_sheets(workbook, sheet_names)

        # 3. По имени
        if isinstance(sheet_param_value, str):
            if sheet_param_value not in sheet_names:
                raise ValueError(
                    f"Лист '{sheet_param_value}' не найден.\n"
                    f"Доступны: {sheet_names}"
                )
            sheet = workbook.get_sheet_by_name(sheet_param_value)
            data = _normalize_sheet(sheet.to_python())
            return MatrExMatrix(data, True)

        # 4. По номеру (1-based)
        if isinstance(sheet_param_value, (int, float)):
            idx = int(sheet_param_value)
            if idx < 1 or idx > len(sheet_names):
                raise IndexError(
                    f"Лист с номером {idx} не найден. "
                    f"Всего листов: {len(sheet_names)}"
                )
            sheet = workbook.get_sheet_by_index(idx - 1)
            data = _normalize_sheet(sheet.to_python())
            return MatrExMatrix(data, True)

        raise TypeError(
            f"Неверный параметр листа: {type(sheet_param_value)}"
        )

    except (ImportError, TypeError, ValueError, IndexError, FileNotFoundError):
        raise
    except Exception as e:
        raise RuntimeError(f"Ошибка загрузки Excel: {e}")


def _normalize_sheet(rows):
    """Приводит данные от python-calamine к единому виду."""
    if not rows:
        return [[""]]

    cleaned = []
    for row in rows:
        cleaned.append(["" if c is None else c for c in row])

    while cleaned and all(c == "" for c in cleaned[-1]):
        cleaned.pop()

    if not cleaned:
        return [[""]]

    max_cols = max(len(r) for r in cleaned)
    for r in cleaned:
        while len(r) < max_cols:
            r.append("")

    return cleaned


def _load_all_sheets(workbook, sheet_names):
    """Все листы подряд, без разделителей."""
    from runtime.matrix import MatrExMatrix

    all_data = []
    for name in sheet_names:
        sheet = workbook.get_sheet_by_name(name)
        sheet_data = _normalize_sheet(sheet.to_python())
        all_data.extend(sheet_data)

    if not all_data:
        return MatrExMatrix([[""]], True)

    max_cols = max(len(r) for r in all_data)
    for r in all_data:
        while len(r) < max_cols:
            r.append("")

    return MatrExMatrix(all_data, True)


# ================================================================
# ОБЩАЯ ФУНКЦИЯ ЗАПИСИ
# ================================================================
def _extract_data(data_obj):
    """Извлекает список списков из data_obj (MatrExMatrix или list)."""
    if hasattr(data_obj, 'data'):
        raw = data_obj.data
    elif isinstance(data_obj, list):
        raw = data_obj
    else:
        raise TypeError(
            f"Данные должны быть матрицей или списком, получен {type(data_obj)}"
        )

    if raw and not isinstance(raw[0], list):
        return [[item] for item in raw]
    return raw


def _save_excel(file_path, data, sheet_name):
    """
    Сохраняет данные в Excel.

    Логика:
        - Файл НЕ существует → pyexcelerate (быстро)
        - Файл существует → openpyxl (дописать/заменить лист)
    """
    # ----------------------------------------------------------------
    # СЦЕНАРИЙ 1: новый файл → pyexcelerate
    # ----------------------------------------------------------------
    if not os.path.exists(file_path):
        if PYXECELERATE_AVAILABLE:
            try:
                wb = PyExcelerateWorkbook()
                wb.new_sheet(sheet_name, data=data)
                wb.save(file_path)
                return
            except Exception:
                # Если pyexcelerate упал — fallback на openpyxl
                pass

        # Fallback: openpyxl
        if not OPENPYXL_AVAILABLE:
            raise ImportError(
                "Ни pyexcelerate, ни openpyxl не установлены.\n"
                "Установите: pip install pyexcelerate openpyxl"
            )
        wb = OpenpyxlWorkbook()
        if "Sheet" in wb.sheetnames:
            wb.remove(wb["Sheet"])
        ws = wb.create_sheet(sheet_name)
        for row in data:
            ws.append(row)
        wb.save(file_path)
        return

    # ----------------------------------------------------------------
    # СЦЕНАРИЙ 2: файл существует → openpyxl
    # ----------------------------------------------------------------
    if not OPENPYXL_AVAILABLE:
        raise ImportError(
            "openpyxl не установлен, а файл уже существует.\n"
            "Установите: pip install openpyxl"
        )

    wb = load_workbook(file_path)

    if sheet_name in wb.sheetnames:
        wb.remove(wb[sheet_name])

    ws = wb.create_sheet(sheet_name)
    for row in data:
        ws.append(row)

    wb.save(file_path)


# ================================================================
# OPEN EXCEL
# ================================================================
class OpenExcelNode(Node):
    """OpenExcel("file.xlsx" [, sheet_name | sheet_index | all])"""

    def __init__(self, file_path, sheet_param=None):
        self.file_path = file_path
        self.sheet_param = sheet_param

    def evaluate(self, env):
        file_path = self.file_path.evaluate(env)
        sheet_val = None
        if self.sheet_param is not None:
            sheet_val = self.sheet_param.evaluate(env)
        return _read_excel_to_matrix(file_path, sheet_val)

    def __repr__(self):
        if self.sheet_param is None:
            return f"OpenExcel({self.file_path})"
        return f"OpenExcel({self.file_path}, {self.sheet_param})"


# ================================================================
# SAVE EXCEL
# ================================================================
class SaveExcelNode(Node):
    """
    SaveExcel(data, "file.xlsx" [, sheet_name])

    Логика:
        - Файл НЕ существует → pyexcelerate (быстро)
        - Файл существует → openpyxl (дописать/заменить лист)
    """

    def __init__(self, data, file_path, sheet_param=None):
        self.data = data
        self.file_path = file_path
        self.sheet_param = sheet_param

    def evaluate(self, env):
        data_obj = self.data.evaluate(env)
        file_path = self.file_path.evaluate(env)

        if not isinstance(file_path, str):
            raise TypeError(
                f"Путь к файлу должен быть строкой, получен {type(file_path)}"
            )

        # Имя листа
        sheet_name = "Лист1"
        if self.sheet_param is not None:
            sheet_val = self.sheet_param.evaluate(env)
            if isinstance(sheet_val, str):
                sheet_name = sheet_val
            elif isinstance(sheet_val, (int, float)):
                sheet_name = f"Лист{int(sheet_val)}"
            else:
                raise TypeError(f"Имя листа должно быть строкой или числом")

        # Данные
        data = _extract_data(data_obj)

        try:
            _save_excel(file_path, data, sheet_name)

            rows = len(data)
            cols = max((len(r) for r in data), default=0)
            return (
                f"Сохранено: {rows} строк, {cols} столбцов "
                f"в '{os.path.basename(file_path)}', лист '{sheet_name}'"
            )

        except Exception as e:
            raise RuntimeError(f"Ошибка сохранения Excel: {e}")

    def __repr__(self):
        if self.sheet_param is None:
            return f"SaveExcel({self.data}, {self.file_path})"
        return f"SaveExcel({self.data}, {self.file_path}, {self.sheet_param})"


# ================================================================
# OPEN EXCEL SHOW (диалог + выбор листов)
# ================================================================
class OpenExcelShowNode(Node):
    """
    OpenExcelShow([sheet_param])

    Без параметра — диалог выбора файла + окно выбора листов (чекбоксы).
    С параметром — диалог файла + сразу чтение нужных листов.
    """

    def __init__(self, sheet_param=None):
        self.sheet_param = sheet_param

    def evaluate(self, env):
        import tkinter as tk
        from tkinter import filedialog, messagebox
        from runtime.matrix import MatrExMatrix

        if not CALAMINE_AVAILABLE:
            raise ImportError(
                "python-calamine не установлен. "
                "Установите: pip install python-calamine"
            )

        # Параметр листа (если задан)
        sheet_val = None
        if self.sheet_param is not None:
            sheet_val = self.sheet_param.evaluate(env)

        # Диалог выбора файла
        root = tk.Tk()
        root.withdraw()
        file_path = filedialog.askopenfilename(
            title="Выберите Excel файл",
            filetypes=[("Excel files", "*.xlsx *.xls"), ("All files", "*.*")]
        )

        if not file_path:
            root.destroy()
            return None

        # Читаем workbook
        try:
            workbook = CalamineWorkbook.from_path(file_path)
            sheet_names = workbook.sheet_names
        except Exception as e:
            root.destroy()
            raise RuntimeError(f"Ошибка открытия Excel: {e}")

        # Если sheet_param задан — без окна выбора
        if sheet_val is not None:
            root.destroy()
            return _read_excel_to_matrix(file_path, sheet_val)

        # Иначе — окно выбора листов
        root.deiconify()
        root.title("Выбор листов")
        root.geometry("450x450")
        root.resizable(False, False)

        tk.Label(root, text="Выберите листы для загрузки:",
                 font=("Arial", 12, "bold")).pack(pady=10)
        tk.Label(root, text=f"Файл: {os.path.basename(file_path)}",
                 font=("Arial", 10)).pack(pady=5)

        listbox_frame = tk.Frame(root)
        listbox_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        scrollbar = tk.Scrollbar(listbox_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        listbox = tk.Listbox(
            listbox_frame,
            selectmode=tk.MULTIPLE,
            yscrollcommand=scrollbar.set,
            font=("Consolas", 10),
            height=12,
        )
        listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=listbox.yview)

        for name in sheet_names:
            listbox.insert(tk.END, name)

        btn_frame = tk.Frame(root)
        btn_frame.pack(pady=5)

        tk.Button(btn_frame, text="Выбрать все",
                  command=lambda: listbox.select_set(0, tk.END),
                  width=12).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Снять все",
                  command=lambda: listbox.selection_clear(0, tk.END),
                  width=12).pack(side=tk.LEFT, padx=5)

        btn_frame2 = tk.Frame(root)
        btn_frame2.pack(pady=10)

        selected = {"sheets": None}

        def on_ok():
            sel = listbox.curselection()
            if not sel:
                messagebox.showwarning("Предупреждение",
                                       "Выберите хотя бы один лист")
                return
            selected["sheets"] = [sheet_names[i] for i in sel]
            root.quit()
            root.destroy()

        def on_cancel():
            selected["sheets"] = None
            root.quit()
            root.destroy()

        tk.Button(btn_frame2, text="OK", command=on_ok,
                  bg="#90EE90", width=15, padx=10, pady=5).pack(side=tk.LEFT, padx=10)
        tk.Button(btn_frame2, text="Отмена", command=on_cancel,
                  bg="#FF6B6B", fg="white", width=15, padx=10, pady=5).pack(side=tk.LEFT, padx=10)

        root.mainloop()

        if not selected["sheets"]:
            return None

        # Загружаем выбранные листы подряд
        all_data = []
        for name in selected["sheets"]:
            sheet = workbook.get_sheet_by_name(name)
            sheet_data = _normalize_sheet(sheet.to_python())
            all_data.extend(sheet_data)

        if not all_data:
            return MatrExMatrix([[""]], True)

        max_cols = max(len(r) for r in all_data)
        for r in all_data:
            while len(r) < max_cols:
                r.append("")

        return MatrExMatrix(all_data, True)

    def __repr__(self):
        if self.sheet_param is None:
            return "OpenExcelShow()"
        return f"OpenExcelShow({self.sheet_param})"


# ================================================================
# SAVE EXCEL SHOW (диалог сохранения)
# ================================================================
class SaveExcelShowNode(Node):
    """SaveExcelShow(data [, sheet_name]) — диалог сохранения"""

    def __init__(self, data, sheet_name=None):
        self.data = data
        self.sheet_name = sheet_name

    def evaluate(self, env):
        import tkinter as tk
        from tkinter import filedialog

        data_obj = self.data.evaluate(env)
        data = _extract_data(data_obj)

        sheet_name = "Лист1"
        if self.sheet_name is not None:
            sheet_val = self.sheet_name.evaluate(env)
            if isinstance(sheet_val, str):
                sheet_name = sheet_val
            elif isinstance(sheet_val, (int, float)):
                sheet_name = f"Лист{int(sheet_val)}"

        root = tk.Tk()
        root.withdraw()
        file_path = filedialog.asksaveasfilename(
            title="Сохранить Excel файл",
            defaultextension=".xlsx",
            filetypes=[("Excel files", "*.xlsx"), ("All files", "*.*")]
        )
        root.destroy()

        if not file_path:
            return "Сохранение отменено"

        try:
            _save_excel(file_path, data, sheet_name)

            rows = len(data)
            cols = max((len(r) for r in data), default=0)
            return (
                f"Сохранено: {rows} строк, {cols} столбцов "
                f"в '{os.path.basename(file_path)}', лист '{sheet_name}'"
            )

        except Exception as e:
            raise RuntimeError(f"Ошибка сохранения Excel: {e}")

    def __repr__(self):
        if self.sheet_name is None:
            return f"SaveExcelShow({self.data})"
        return f"SaveExcelShow({self.data}, {self.sheet_name})"