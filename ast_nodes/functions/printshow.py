# ast_nodes/functions/printshow.py
"""
Функция PrintShow: PrintShowNode

Визуальный вывод матрицы в отдельном окне в стиле Excel.
С виртуализацией: для 1 млн строк окно открывается мгновенно.

Синтаксис:
    printshow(данные)
    printshow(данные, "Заголовок")

Поддерживает:
    - MatrExMatrix (обычные данные)
    - DuckDBTable (большие данные — через SQL)
"""

import tkinter as tk
from tkinter import messagebox, filedialog
import os


# ============================================================
# ОПРЕДЕЛЕНИЕ DUCKDBTABLE
# ============================================================
def _is_duckdb(val):
    """Проверяет, является ли значение DuckDBTable."""
    try:
        from duckdb_engine import DuckDBTable
        return isinstance(val, DuckDBTable)
    except ImportError:
        return False


# ============================================================
# РАЗМЕРЫ (уменьшены для компактности)
# ============================================================
CELL_WIDTH = 80
CELL_HEIGHT = 20
ROW_HEADER_WIDTH = 50
COL_HEADER_HEIGHT = 22
FONT_EDITOR = ("Segoe UI", 9)
FONT_HEADER = ("Segoe UI", 9, "bold")
MAX_DUCKDB_SHOW = 1000000   # 1 млн для DuckDB


# ============================================================
# PRINT SHOW NODE
# ============================================================
class PrintShowNode:
    def __init__(self, data, title=None):
        self.data = data
        self.title = title
        self.var_name = None

    def evaluate(self, env):
        data_obj = self.data.evaluate(env)

        # Заголовок окна
        title = "Данные"
        if self.title is not None:
            title = self.title.evaluate(env)
            if not isinstance(title, str):
                title = "Данные"

        # Имя переменной
        if hasattr(self.data, "name"):
            self.var_name = self.data.name
        else:
            try:
                for name, value in env.vars.items():
                    if value is data_obj:
                        self.var_name = name
                        break
            except Exception:
                pass

        if self.var_name is None:
            self.var_name = "data"

        # ============================================================
        # DUCKDB: получаем данные через SQL
        # ============================================================
        if _is_duckdb(data_obj):
            try:
                data = data_obj.get_data_for_show(limit=MAX_DUCKDB_SHOW)
                headers = data_obj.get_columns()
                data = [headers] + data
                data = self._normalize_data(data)
                self._show_window(data, title)
                return data_obj
            except Exception as e:
                messagebox.showerror(
                    "Ошибка printshow",
                    f"Не удалось загрузить данные из DuckDB:\n{e}"
                )
                return data_obj

        # ============================================================
        # ОБЫЧНЫЙ РЕЖИМ (MatrExMatrix или list)
        # ============================================================
        if hasattr(data_obj, "data"):
            data = data_obj.data
        elif isinstance(data_obj, list):
            data = data_obj
        else:
            data = [[data_obj]]

        data = self._normalize_data(data)
        self._show_window(data, title)
        return data

    # ============================================================
    # ПОДГОТОВКА ДАННЫХ
    # ============================================================
    def _normalize_data(self, data):
        if data is None:
            return [[""]]
        if not isinstance(data, list):
            return [[data]]
        if not data:
            return [[""]]

        if not all(isinstance(row, (list, tuple)) for row in data):
            data = [data]

        max_columns = max((len(row) for row in data), default=1)

        normalized_data = []
        for row in data:
            row = list(row)
            while len(row) < max_columns:
                row.append("")
            normalized_data.append(row)

        return normalized_data

    # ============================================================
    # СОЗДАНИЕ ОКНА
    # ============================================================
    def _show_window(self, data, title):
        root = tk.Tk()
        root.title(f"📊 {title}")
        root.minsize(600, 400)
        root.resizable(True, True)
        root.configure(bg="#f0f2f5")

        try:
            root.update_idletasks()
            W, H = 1100, 720
            sw = root.winfo_screenwidth()
            sh = root.winfo_screenheight()
            x = (sw - W) // 2
            y = (sh - H) // 2
            if x < 0:
                x = 0
            if y < 0:
                y = 0
            root.geometry(f"{W}x{H}+{x}+{y}")
        except Exception:
            root.geometry("1100x720")

        colors = {
            "bg": "#f0f2f5",
            "header_bg": "#217346",
            "header_fg": "#ffffff",
            "row_even": "#ffffff",
            "row_odd": "#f4f8f5",
            "border": "#c5cec8",
            "selected_bg": "#fff2cc",
            "selected_border": "#217346",
            "row_header_bg": "#e2f0e7",
            "text": "#263238",
            "muted": "#718096",
            "coord_bg": "#1f2937",
            "coord_fg": "#ffffff",
            "coord_accent": "#7dd3fc",
            "button_success": "#27ae60",
            "button_copy": "#3485c5",
            "button_danger": "#e74c3c",
        }

        # ============================================================
        # МЕНЮ
        # ============================================================
        menubar = tk.Menu(root)

        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(
            label="Сохранить как Excel...",
            accelerator="Ctrl+S",
            command=lambda: self._save_as_excel(data, root)
        )
        file_menu.add_command(
            label="Сохранить как CSV...",
            accelerator="Ctrl+Shift+C",
            command=lambda: self._save_as_csv(data, root)
        )
        file_menu.add_command(
            label="Сохранить как TXT...",
            accelerator="Ctrl+Shift+T",
            command=lambda: self._save_as_txt(data, root)
        )
        file_menu.add_separator()
        file_menu.add_command(
            label="Копировать всё",
            accelerator="Ctrl+Shift+A",
            command=lambda: self._copy_all(data, root)
        )
        file_menu.add_separator()
        file_menu.add_command(
            label="Закрыть",
            accelerator="Esc",
            command=root.destroy
        )
        menubar.add_cascade(label="Файл", menu=file_menu)

        edit_menu = tk.Menu(menubar, tearoff=0)
        edit_menu.add_command(
            label="Копировать ячейку",
            accelerator="Ctrl+C",
            command=lambda: self._copy_selected_cell(data, selected_cell, root)
        )
        edit_menu.add_command(
            label="Выделить всё",
            accelerator="Ctrl+A",
            command=lambda: self._copy_all(data, root)
        )
        edit_menu.add_separator()
        edit_menu.add_command(
            label="Перейти к ячейке...",
            accelerator="Ctrl+G",
            command=lambda: self._goto_cell(data, root, selected_cell)
        )
        menubar.add_cascade(label="Правка", menu=edit_menu)

        help_menu = tk.Menu(menubar, tearoff=0)
        help_menu.add_command(
            label="О программе",
            command=lambda: self._show_about(root)
        )
        menubar.add_cascade(label="Справка", menu=help_menu)

        root.config(menu=menubar)

        # ============================================================
        # РАЗМЕРЫ ДАННЫХ
        # ============================================================
        row_count = len(data)
        column_count = max((len(row) for row in data), default=1)

        selected_cell = [0, 0]

        # ============================================================
        # ВЕРХНЯЯ ПАНЕЛЬ
        # ============================================================
        top_frame = tk.Frame(root, bg=colors["bg"], height=50)
        top_frame.pack(fill=tk.X, padx=15, pady=(10, 6))
        top_frame.pack_propagate(False)

        var_name = self.var_name or "data"

        name_label = tk.Label(
            top_frame,
            text=f"📊 {var_name}",
            font=("Segoe UI", 14, "bold"),
            bg=colors["bg"],
            fg=colors["text"]
        )
        name_label.pack(side=tk.LEFT, padx=5)

        coord_frame = tk.Frame(top_frame, bg=colors["coord_bg"])
        coord_frame.pack(side=tk.RIGHT, padx=5)

        coord_label = tk.Label(
            coord_frame,
            text=f"{var_name}[1, 1]",
            font=("Consolas", 12, "bold"),
            bg=colors["coord_bg"],
            fg=colors["coord_fg"],
            padx=14,
            pady=4
        )
        coord_label.pack(side=tk.LEFT)

        separator = tk.Frame(coord_frame, bg="#4b5563", width=1)
        separator.pack(side=tk.LEFT, fill=tk.Y, padx=3, pady=4)

        value_label = tk.Label(
            coord_frame,
            text="",
            font=("Consolas", 11),
            bg=colors["coord_bg"],
            fg=colors["coord_accent"],
            padx=12,
            pady=4
        )
        value_label.pack(side=tk.LEFT)

        # ============================================================
        # ТАБЛИЦА
        # ============================================================
        main_frame = tk.Frame(root, bg=colors["bg"])
        main_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=5)

        table_frame = tk.Frame(main_frame, bg=colors["border"],
                                relief="solid", borderwidth=1)
        table_frame.pack(fill=tk.BOTH, expand=True)

        table_frame.grid_rowconfigure(0, weight=1)
        table_frame.grid_columnconfigure(0, weight=1)

        canvas = tk.Canvas(table_frame, bg="white", highlightthickness=0)

        vertical_scrollbar = tk.Scrollbar(
            table_frame, orient="vertical", command=canvas.yview
        )
        horizontal_scrollbar = tk.Scrollbar(
            table_frame, orient="horizontal", command=canvas.xview
        )

        canvas.configure(
            yscrollcommand=vertical_scrollbar.set,
            xscrollcommand=horizontal_scrollbar.set
        )

        canvas.grid(row=0, column=0, sticky="nsew")
        vertical_scrollbar.grid(row=0, column=1, sticky="ns")
        horizontal_scrollbar.grid(row=1, column=0, sticky="ew")

        # ============================================================
        # ОБЩИЕ РАЗМЕРЫ
        # ============================================================
        total_width = ROW_HEADER_WIDTH + column_count * CELL_WIDTH
        total_height = COL_HEADER_HEIGHT + row_count * CELL_HEIGHT

        canvas.configure(scrollregion=(0, 0, total_width, total_height))

        # ============================================================
        # ВИРТУАЛИЗАЦИЯ: РИСУЕМ ТОЛЬКО ВИДИМОЕ
        # ============================================================
        def draw_visible():
            canvas.delete("all")

            # Размер видимой области
            view_w = canvas.winfo_width()
            view_h = canvas.winfo_height()

            # Текущая позиция скролла
            x_start = canvas.canvasx(0)
            y_start = canvas.canvasy(0)
            x_end = x_start + view_w
            y_end = y_start + view_h

            # Диапазон видимых строк
            row_start = max(0, int((y_start - COL_HEADER_HEIGHT) / CELL_HEIGHT) - 1)
            row_end = min(row_count, int((y_end - COL_HEADER_HEIGHT) / CELL_HEIGHT) + 2)

            # Диапазон видимых столбцов
            col_start = max(0, int((x_start - ROW_HEADER_WIDTH) / CELL_WIDTH) - 1)
            col_end = min(column_count, int((x_end - ROW_HEADER_WIDTH) / CELL_WIDTH) + 2)

            # Угол
            canvas.create_rectangle(
                0, 0, ROW_HEADER_WIDTH, COL_HEADER_HEIGHT,
                fill="#185c37", outline="#b7c9bd"
            )
            canvas.create_text(
                ROW_HEADER_WIDTH // 2, COL_HEADER_HEIGHT // 2,
                text="№", fill="white",
                font=("Segoe UI", 8, "bold")
            )

            # Заголовки столбцов (только видимые)
            for col_index in range(col_start, col_end):
                x1 = ROW_HEADER_WIDTH + col_index * CELL_WIDTH
                x2 = x1 + CELL_WIDTH
                canvas.create_rectangle(
                    x1, 0, x2, COL_HEADER_HEIGHT,
                    fill=colors["header_bg"], outline="#b7c9bd"
                )
                canvas.create_text(
                    (x1 + x2) // 2, COL_HEADER_HEIGHT // 2,
                    text=str(col_index + 1),
                    fill=colors["header_fg"],
                    font=("Segoe UI", 8, "bold")
                )

            # Строки (только видимые)
            for row_index in range(row_start, row_end):
                row = data[row_index]
                y1 = COL_HEADER_HEIGHT + row_index * CELL_HEIGHT
                y2 = y1 + CELL_HEIGHT

                row_color = (colors["row_even"] if row_index % 2 == 0
                             else colors["row_odd"])

                # Номер строки (фиксирован слева)
                canvas.create_rectangle(
                    0, y1, ROW_HEADER_WIDTH, y2,
                    fill=colors["row_header_bg"],
                    outline=colors["border"]
                )
                canvas.create_text(
                    ROW_HEADER_WIDTH // 2, (y1 + y2) // 2,
                    text=str(row_index + 1),
                    fill=colors["header_bg"],
                    font=("Segoe UI", 8, "bold")
                )

                # Ячейки (только видимые)
                for col_index in range(col_start, col_end):
                    x1 = ROW_HEADER_WIDTH + col_index * CELL_WIDTH
                    x2 = x1 + CELL_WIDTH

                    if col_index < len(row):
                        value = row[col_index]
                    else:
                        value = ""

                    if value is None:
                        value = ""

                    value = str(value)

                    is_selected = (row_index == selected_cell[0]
                                   and col_index == selected_cell[1])

                    if is_selected:
                        fill_color = colors["selected_bg"]
                        border_color = colors["selected_border"]
                        border_width = 2
                    else:
                        fill_color = row_color
                        border_color = colors["border"]
                        border_width = 1

                    canvas.create_rectangle(
                        x1, y1, x2, y2,
                        fill=fill_color,
                        outline=border_color,
                        width=border_width
                    )

                    # Обрезка длинных значений
                    display_value = value
                    max_chars = max(1, CELL_WIDTH // 7 - 1)
                    if len(display_value) > max_chars:
                        display_value = display_value[:max_chars - 1] + "…"

                    canvas.create_text(
                        x1 + 4, (y1 + y2) // 2,
                        text=display_value, anchor="w",
                        fill=colors["text"],
                        font=FONT_EDITOR
                    )

        # ============================================================
        # ОБНОВЛЕНИЕ КООРДИНАТ
        # ============================================================
        def update_coords():
            if not data:
                return

            selected_row = selected_cell[0]
            selected_col = selected_cell[1]

            row_number = selected_row + 1
            column_number = selected_col + 1

            value = ""
            if selected_row < len(data):
                row = data[selected_row]
                if selected_col < len(row):
                    value = row[selected_col]

            if value is None:
                value = ""

            display_value = str(value)
            if len(display_value) > 50:
                display_value = display_value[:47] + "..."

            coord_label.config(text=f"{var_name}[{row_number}, {column_number}]")
            value_label.config(text=f"= {display_value}")

            draw_visible()

        # ============================================================
        # КЛИК ПО ЯЧЕЙКЕ
        # ============================================================
        def on_click(event):
            x = canvas.canvasx(event.x)
            y = canvas.canvasy(event.y)

            if x < ROW_HEADER_WIDTH or y < COL_HEADER_HEIGHT:
                return

            col_index = int((x - ROW_HEADER_WIDTH) / CELL_WIDTH)
            row_index = int((y - COL_HEADER_HEIGHT) / CELL_HEIGHT)

            if not (0 <= row_index < row_count and 0 <= col_index < column_count):
                return

            selected_cell[0] = row_index
            selected_cell[1] = col_index
            update_coords()

        # ============================================================
        # КЛАВИШИ
        # ============================================================
        def on_key(event):
            row_index = selected_cell[0]
            col_index = selected_cell[1]

            if event.keysym == "Left":
                col_index = max(0, col_index - 1)
            elif event.keysym == "Right":
                col_index = min(column_count - 1, col_index + 1)
            elif event.keysym == "Up":
                row_index = max(0, row_index - 1)
            elif event.keysym == "Down":
                row_index = min(row_count - 1, row_index + 1)
            elif event.keysym == "Home":
                col_index = 0
            elif event.keysym == "End":
                col_index = column_count - 1
            elif event.keysym == "Prior":  # PageUp
                row_index = max(0, row_index - 30)
            elif event.keysym == "Next":   # PageDown
                row_index = min(row_count - 1, row_index + 30)
            else:
                return

            selected_cell[0] = row_index
            selected_cell[1] = col_index
            update_coords()

            # Прокрутка к выделенной ячейке
            target_y = COL_HEADER_HEIGHT + row_index * CELL_HEIGHT
            target_x = ROW_HEADER_WIDTH + col_index * CELL_WIDTH

            view_h = canvas.winfo_height()
            view_w = canvas.winfo_width()

            cur_y = canvas.canvasy(0)
            if target_y < cur_y + COL_HEADER_HEIGHT:
                canvas.yview_moveto(
                    max(0, (target_y - COL_HEADER_HEIGHT) / total_height)
                )
            elif target_y > cur_y + view_h - CELL_HEIGHT:
                canvas.yview_moveto(
                    max(0, (target_y - view_h + CELL_HEIGHT) / total_height)
                )

            cur_x = canvas.canvasx(0)
            if target_x < cur_x + ROW_HEADER_WIDTH:
                canvas.xview_moveto(
                    max(0, (target_x - ROW_HEADER_WIDTH) / total_width)
                )
            elif target_x > cur_x + view_w - CELL_WIDTH:
                canvas.xview_moveto(
                    max(0, (target_x - view_w + CELL_WIDTH) / total_width)
                )

            draw_visible()

        # ============================================================
        # ПРИВЯЗКА СОБЫТИЙ
        # ============================================================
        canvas.bind("<Button-1>", on_click)
        canvas.bind("<Key>", on_key)
        canvas.bind("<Configure>", lambda e: draw_visible())
        canvas.focus_set()

        # Скролл мышью
        def on_mousewheel(event):
            if event.delta:
                canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
            draw_visible()

        def on_mousewheel_linux(event):
            if event.num == 4:
                canvas.yview_scroll(-1, "units")
            elif event.num == 5:
                canvas.yview_scroll(1, "units")
            draw_visible()

        canvas.bind("<MouseWheel>", on_mousewheel)
        canvas.bind("<Button-4>", on_mousewheel_linux)
        canvas.bind("<Button-5>", on_mousewheel_linux)

        def on_yscroll(first, last):
            vertical_scrollbar.set(first, last)
            draw_visible()

        def on_xscroll(first, last):
            horizontal_scrollbar.set(first, last)
            draw_visible()

        canvas.configure(
            yscrollcommand=on_yscroll,
            xscrollcommand=on_xscroll,
        )

        # ============================================================
        # НИЖНЯЯ ПАНЕЛЬ
        # ============================================================
        bottom_frame = tk.Frame(root, bg=colors["bg"])
        bottom_frame.pack(fill=tk.X, padx=15, pady=8)

        info_label = tk.Label(
            bottom_frame,
            text=f"📊 Строк: {row_count}  |  Столбцов: {column_count}",
            font=("Segoe UI", 9),
            bg=colors["bg"],
            fg=colors["muted"]
        )
        info_label.pack(side=tk.LEFT, padx=5)

        close_button = tk.Button(
            bottom_frame,
            text="✕ Закрыть",
            command=root.destroy,
            bg=colors["button_danger"],
            fg="white",
            font=("Segoe UI", 9, "bold"),
            padx=20,
            pady=6,
            relief="flat",
            borderwidth=0,
            cursor="hand2"
        )
        close_button.pack(side=tk.RIGHT, padx=5)

        copy_button = tk.Button(
            bottom_frame,
            text="📋 Копировать",
            command=lambda: self._copy_selected_cell(data, selected_cell, root),
            bg=colors["button_copy"],
            fg="white",
            font=("Segoe UI", 9, "bold"),
            padx=20,
            pady=6,
            relief="flat",
            borderwidth=0,
            cursor="hand2"
        )
        copy_button.pack(side=tk.RIGHT, padx=5)

        save_button = tk.Button(
            bottom_frame,
            text="💾 Сохранить как Excel",
            command=lambda: self._save_as_excel(data, root),
            bg=colors["button_success"],
            fg="white",
            font=("Segoe UI", 9, "bold"),
            padx=20,
            pady=6,
            relief="flat",
            borderwidth=0,
            cursor="hand2"
        )
        save_button.pack(side=tk.RIGHT, padx=5)

        # Горячие клавиши
        root.bind("<Escape>", lambda e: root.destroy())
        root.bind("<Control-s>", lambda e: self._save_as_excel(data, root))
        root.bind("<Control-Shift-C>", lambda e: self._save_as_csv(data, root))
        root.bind("<Control-Shift-T>", lambda e: self._save_as_txt(data, root))
        root.bind("<Control-c>", lambda e: self._copy_selected_cell(data, selected_cell, root))
        root.bind("<Control-a>", lambda e: self._copy_all(data, root))
        root.bind("<Control-g>", lambda e: self._goto_cell(data, root, selected_cell))

        # Первая отрисовка
        root.update_idletasks()
        draw_visible()
        update_coords()

        root.mainloop()

    # ============================================================
    # СОХРАНЕНИЕ
    # ============================================================
    def _save_as_excel(self, data, root):
        try:
            from openpyxl import Workbook
        except ImportError:
            messagebox.showerror("Ошибка",
                                 "openpyxl не установлен.",
                                 parent=root)
            return

        file_path = filedialog.asksaveasfilename(
            parent=root,
            defaultextension=".xlsx",
            filetypes=[("Excel files", "*.xlsx"), ("All files", "*.*")]
        )
        if not file_path:
            return

        try:
            wb = Workbook()
            ws = wb.active
            ws.title = "Данные"

            for r_idx, row in enumerate(data, 1):
                for c_idx, value in enumerate(row, 1):
                    ws.cell(row=r_idx, column=c_idx, value=value)

            wb.save(file_path)
            messagebox.showinfo("Успех",
                                f"Сохранено:\n{file_path}",
                                parent=root)
        except Exception as e:
            messagebox.showerror("Ошибка",
                                 f"Не удалось сохранить:\n{e}",
                                 parent=root)

    def _save_as_csv(self, data, root):
        import csv

        file_path = filedialog.asksaveasfilename(
            parent=root,
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
        )
        if not file_path:
            return

        try:
            with open(file_path, 'w', encoding='utf-8-sig', newline='') as f:
                writer = csv.writer(f)
                for row in data:
                    if not isinstance(row, list):
                        row = [row]
                    writer.writerow(row)

            messagebox.showinfo("Успех",
                                f"Сохранено:\n{file_path}",
                                parent=root)
        except Exception as e:
            messagebox.showerror("Ошибка",
                                 f"Не удалось сохранить:\n{e}",
                                 parent=root)

    def _save_as_txt(self, data, root):
        import csv

        file_path = filedialog.asksaveasfilename(
            parent=root,
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        if not file_path:
            return

        try:
            with open(file_path, 'w', encoding='utf-8-sig', newline='') as f:
                writer = csv.writer(f, delimiter=';')
                for row in data:
                    if not isinstance(row, list):
                        row = [row]
                    writer.writerow(row)

            messagebox.showinfo("Успех",
                                f"Сохранено:\n{file_path}",
                                parent=root)
        except Exception as e:
            messagebox.showerror("Ошибка",
                                 f"Не удалось сохранить:\n{e}",
                                 parent=root)

    # ============================================================
    # КОПИРОВАНИЕ
    # ============================================================
    def _copy_selected_cell(self, data, selected_cell, root):
        row_index = selected_cell[0]
        col_index = selected_cell[1]

        try:
            value = data[row_index][col_index]
        except IndexError:
            value = ""

        if value is None:
            value = ""

        root.clipboard_clear()
        root.clipboard_append(str(value))
        root.update()

        messagebox.showinfo("Успех",
                            f"Скопирована ячейка [{row_index + 1}, {col_index + 1}]",
                            parent=root)

    def _copy_all(self, data, root):
        lines = []
        for row in data:
            lines.append("\t".join(
                str(v) if v is not None else "" for v in row
            ))

        text = "\n".join(lines)

        root.clipboard_clear()
        root.clipboard_append(text)
        root.update()

        messagebox.showinfo("Успех",
                            "Все данные скопированы в буфер",
                            parent=root)

    # ============================================================
    # ПЕРЕХОД К ЯЧЕЙКЕ
    # ============================================================
    def _goto_cell(self, data, root, selected_cell):
        from tkinter import simpledialog

        answer = simpledialog.askstring(
            "Перейти к ячейке",
            "Введите координаты (строка, столбец):\n"
            "Например: 2, 3",
            parent=root,
        )
        if not answer:
            return

        try:
            parts = answer.replace(" ", "").split(",")
            row = int(parts[0]) - 1
            col = int(parts[1]) - 1

            row_count = len(data)
            column_count = max((len(r) for r in data), default=1)

            if 0 <= row < row_count and 0 <= col < column_count:
                selected_cell[0] = row
                selected_cell[1] = col
                root.event_generate("<Configure>")
            else:
                messagebox.showwarning("Внимание",
                                       f"Неверные координаты.\n"
                                       f"Допустимо: 1..{row_count}, 1..{column_count}",
                                       parent=root)
        except Exception:
            messagebox.showerror("Ошибка",
                                 "Введите координаты в формате: 2, 3",
                                 parent=root)

    # ============================================================
    # О ПРОГРАММЕ
    # ============================================================
    def _show_about(self, root):
        messagebox.showinfo(
            "О программе",
            "PrintShow — просмотр данных\n\n"
            "Возможности:\n"
            "• Виртуализация (1 млн строк)\n"
            "• Навигация стрелками\n"
            "• PageUp/PageDown\n"
            "• Копирование ячейки (Ctrl+C)\n"
            "• Сохранить как Excel (Ctrl+S)\n"
            "• Сохранить как CSV (Ctrl+Shift+C)\n"
            "• Сохранить как TXT (Ctrl+Shift+T)\n",
            parent=root
        )

    # ============================================================
    # СТРОКОВОЕ ПРЕДСТАВЛЕНИЕ
    # ============================================================
    def __repr__(self):
        if self.title is None:
            return f"printshow({self.data})"
        return f"printshow({self.data}, {self.title})"