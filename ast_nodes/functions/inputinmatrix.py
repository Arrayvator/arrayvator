# ast_nodes/functions/inputinmatrix.py
"""
InputInMatrix — визуальное добавление строк в матрицу.

СИНТАКСИС:
    m = InputInMatrix(m)
    m = InputInMatrix(m, "Заголовок окна")
    m = InputInMatrix(m, "Заголовок окна", 10)

ПОВЕДЕНИЕ:
    - Открывает окно с контекстом (последние N строк).
    - Под контекстом — поля ввода ПО ЧИСЛУ СТОЛБЦОВ, ГОРИЗОНТАЛЬНО.
    - Кнопка "Добавить" (или Enter) → строка ВИДИМО добавляется в таблицу.
    - Кнопка "Завершить" (или Ctrl+Enter) → возвращает новую матрицу.
    - Крестик или Esc → отмена, возвращает исходную матрицу.
"""

import tkinter as tk

from ..base import Node
from runtime.matrix import MatrExMatrix


class InputInMatrixNode(Node):
    def __init__(self, data, title=None, preview_count=None):
        self.data = data
        self.title = title
        self.preview_count = preview_count

    def evaluate(self, env):
        matrix_obj = (self.data.evaluate(env)
                      if hasattr(self.data, 'evaluate')
                      else self.data)

        if not hasattr(matrix_obj, 'data') or not matrix_obj.is_2d:
            raise TypeError(
                "InputInMatrix: ожидается 2D-матрица.\n"
                "  Пример: m = InputInMatrix(m)"
            )

        title = self._eval_str(self.title, env, default="Добавление строк")
        preview = self._eval_int(self.preview_count, env, default=10)

        return self._show_window(matrix_obj, title, preview)

    # ============================================================
    # УТИЛИТЫ
    # ============================================================
    def _eval_str(self, node, env, default):
        if node is None:
            return default
        val = node.evaluate(env) if hasattr(node, 'evaluate') else node
        return str(val) if val is not None else default

    def _eval_int(self, node, env, default):
        if node is None:
            return default
        val = node.evaluate(env) if hasattr(node, 'evaluate') else node
        try:
            return int(val)
        except (ValueError, TypeError):
            return default

    def _auto_convert(self, text):
        if text is None:
            return None
        s = text.strip()
        if s == "":
            return ""
        lower = s.lower()
        if lower in ('null', 'none'):
            return None
        if lower == 'true':
            return True
        if lower == 'false':
            return False
        try:
            if '.' not in s and 'e' not in lower:
                return int(s)
        except ValueError:
            pass
        try:
            if '.' in s or 'e' in lower:
                return float(s)
        except ValueError:
            pass
        return text

    # ============================================================
    # ОКНО
    # ============================================================
    def _show_window(self, matrix_obj, title, preview):
        # --- Данные ---
        header = list(matrix_obj.data[0]) if matrix_obj.rows > 0 else []
        n_cols = len(header)

        all_data = matrix_obj.data[1:] if matrix_obj.rows > 1 else []

        # Буфер добавленных строк
        new_rows = []

        result = {"matrix": matrix_obj}

        # --- Родительское окно ---
        root = tk._default_root
        if root is None:
            own_root = tk.Tk()
            own_root.withdraw()
            parent = own_root
        else:
            own_root = None
            parent = root

        # --- Главное окно ---
        win = tk.Toplevel(parent)
        win.title(title)
        win.transient(parent)
        win.geometry("1000x750")

        # Цвета
        BG = "#f0f2f5"
        HEADER_BG = "#217346"
        HEADER_FG = "white"
        ROW_ODD = "#f4f8f5"
        ROW_EVEN = "#ffffff"
        NEW_ROW_BG = "#fff9e6"
        ADDED_ROW_BG = "#fff3b0"      # ← подсветка добавленных
        ADDED_ROW_BORDER = "#e0a800"
        BORDER = "#c5cec8"
        MUTED = "#718096"
        TEXT = "#263238"

        win.configure(bg=BG)

        # ------------------------------------------------------------
        # ЗАГОЛОВОК ОКНА
        # ------------------------------------------------------------
        tk.Label(win, text=title,
                 font=("Segoe UI", 14, "bold"),
                 bg=BG, fg=TEXT).pack(pady=(12, 6))

        # ------------------------------------------------------------
        # КОНТЕКСТ — ТАБЛИЦА (СКРОЛЛИРУЕМАЯ)
        # ------------------------------------------------------------
        tk.Label(win, text="Текущие строки:",
                 font=("Segoe UI", 9, "italic"),
                 bg=BG, fg=MUTED).pack(anchor="w", padx=20)

        # Рамка с вертикальным скроллом
        ctx_outer = tk.Frame(win, bg=BORDER, relief="solid", bd=1)
        ctx_outer.pack(fill=tk.BOTH, expand=True, padx=20, pady=6)

        ctx_canvas = tk.Canvas(ctx_outer, bg="white", highlightthickness=0)
        ctx_scroll = tk.Scrollbar(ctx_outer, orient="vertical",
                                  command=ctx_canvas.yview)

        ctx_canvas.configure(yscrollcommand=ctx_scroll.set)

        ctx_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        ctx_scroll.pack(side=tk.RIGHT, fill=tk.Y)

        # Внутренний фрейм для таблицы
        table_frame = tk.Frame(ctx_canvas, bg="white")
        ctx_canvas.create_window((0, 0), window=table_frame, anchor="nw")

        # Функция обновления scrollregion
        def on_table_configure(event):
            ctx_canvas.configure(scrollregion=ctx_canvas.bbox("all"))

        table_frame.bind("<Configure>", on_table_configure)

        # Прокрутка колёсиком мыши
        def on_mousewheel(event):
            ctx_canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

        def on_mousewheel_linux(event):
            if event.num == 4:
                ctx_canvas.yview_scroll(-1, "units")
            elif event.num == 5:
                ctx_canvas.yview_scroll(1, "units")

        ctx_canvas.bind("<MouseWheel>", on_mousewheel)
        ctx_canvas.bind("<Button-4>", on_mousewheel_linux)
        ctx_canvas.bind("<Button-5>", on_mousewheel_linux)

        # ------------------------------------------------------------
        # ФУНКЦИЯ ОТРИСОВКИ ТАБЛИЦЫ
        # ------------------------------------------------------------
        def render_table():
            """Перерисовывает таблицу: контекст + добавленные строки."""
            # Очищаем
            for widget in table_frame.winfo_children():
                widget.destroy()

            # Заголовки
            for j, h in enumerate(header):
                tk.Label(table_frame,
                         text=str(h) if h is not None else "",
                         font=("Consolas", 10, "bold"),
                         bg=HEADER_BG, fg=HEADER_FG,
                         padx=10, pady=5,
                         relief="solid", bd=1,
                         width=14, anchor="w"
                         ).grid(row=0, column=j, sticky="nsew")

            # Контекст (последние preview строк из исходных)
            context_rows = all_data[-preview:] if preview > 0 else []

            row_idx = 1
            for i, row in enumerate(context_rows):
                bg = ROW_ODD if i % 2 == 0 else ROW_EVEN
                for j in range(n_cols):
                    val = row[j] if j < len(row) else None
                    text = "" if val is None else str(val)
                    tk.Label(table_frame,
                             text=text,
                             font=("Consolas", 10),
                             bg=bg, fg=TEXT,
                             padx=10, pady=4,
                             relief="solid", bd=1,
                             width=14, anchor="w"
                             ).grid(row=row_idx, column=j, sticky="nsew")
                row_idx += 1

            # Добавленные строки — с подсветкой
            for i, row in enumerate(new_rows):
                for j in range(n_cols):
                    val = row[j] if j < len(row) else None
                    text = "" if val is None else str(val)
                    tk.Label(table_frame,
                             text=text,
                             font=("Consolas", 10, "bold"),
                             bg=ADDED_ROW_BG, fg=TEXT,
                             padx=10, pady=4,
                             relief="solid", bd=1,
                             highlightbackground=ADDED_ROW_BORDER,
                             highlightthickness=1,
                             width=14, anchor="w"
                             ).grid(row=row_idx, column=j, sticky="nsew")
                row_idx += 1

            # Обновляем scrollregion
            table_frame.update_idletasks()
            ctx_canvas.configure(scrollregion=ctx_canvas.bbox("all"))

            # Прокрутка вниз — к последней добавленной строке
            if new_rows:
                ctx_canvas.yview_moveto(1.0)

        # Первая отрисовка
        render_table()

        # ------------------------------------------------------------
        # РАЗДЕЛИТЕЛЬ
        # ------------------------------------------------------------
        tk.Frame(win, bg=BORDER, height=1).pack(fill=tk.X, padx=20, pady=8)

        # ------------------------------------------------------------
        # ПОЛЯ ВВОДА — ГОРИЗОНТАЛЬНО В ОДНУ СТРОКУ
        # ------------------------------------------------------------
        tk.Label(win, text="Новая строка:",
                 font=("Segoe UI", 11, "bold"),
                 bg=BG, fg=TEXT).pack(anchor="w", padx=20)

        new_frame = tk.Frame(win, bg=NEW_ROW_BG, relief="solid", bd=2,
                             highlightbackground="#f0ad4e",
                             highlightthickness=1)
        new_frame.pack(fill=tk.X, padx=20, pady=6)

        entries = []
        for j, h in enumerate(header):
            tk.Label(new_frame,
                     text=str(h) if h is not None else "",
                     font=("Segoe UI", 8),
                     bg=NEW_ROW_BG, fg=MUTED
                     ).grid(row=0, column=j, padx=4, pady=(6, 0), sticky="w")

            e = tk.Entry(new_frame, font=("Consolas", 11), width=14)
            e.grid(row=1, column=j, padx=4, pady=(0, 6), sticky="ew")
            entries.append(e)

        for j in range(n_cols):
            new_frame.grid_columnconfigure(j, weight=1)

        if entries:
            entries[0].focus_set()

        # ------------------------------------------------------------
        # КНОПКИ И СТАТУС
        # ------------------------------------------------------------
        bottom = tk.Frame(win, bg=BG)
        bottom.pack(fill=tk.X, padx=20, pady=10)

        status_var = tk.StringVar(value="Готово к вводу")
        tk.Label(bottom, textvariable=status_var,
                 font=("Segoe UI", 9),
                 bg=BG, fg=MUTED).pack(side=tk.LEFT)

        def on_add(event=None):
            """Добавить строку в буфер + обновить таблицу."""
            row = [self._auto_convert(e.get()) for e in entries]

            if all(v == "" or v is None for v in row):
                status_var.set("⚠ Все поля пустые")
                return

            new_rows.append(row)

            # Очистить поля
            for e in entries:
                e.delete(0, tk.END)

            if entries:
                entries[0].focus_set()

            # ★ ОБНОВИТЬ ТАБЛИЦУ
            render_table()

            status_var.set(f"✓ Добавлено строк: {len(new_rows)}")

        def on_undo(event=None):
            """Убрать последнюю добавленную строку."""
            if not new_rows:
                status_var.set("⚠ Нет добавленных строк")
                return

            new_rows.pop()
            render_table()
            status_var.set(f"↩ Отменено. Осталось: {len(new_rows)}")

        def on_finish(event=None):
            """Завершить и вернуть новую матрицу."""
            result_data = [list(matrix_obj.data[0])]
            for row in all_data:
                result_data.append(list(row))
            for row in new_rows:
                result_data.append(row)

            max_cols = max(len(r) for r in result_data) if result_data else 0
            for r in result_data:
                while len(r) < max_cols:
                    r.append(None)

            result["matrix"] = MatrExMatrix(result_data, True)
            win.destroy()

        def on_close(event=None):
            """Крестик или Esc → отмена."""
            result["matrix"] = matrix_obj
            win.destroy()

        # Кнопка "Отменить последнюю"
        undo_btn = tk.Button(bottom, text="↩ Убрать последнюю",
                             command=on_undo,
                             bg="#f0ad4e", fg="white",
                             font=("Segoe UI", 9),
                             padx=10, pady=4)
        undo_btn.pack(side=tk.LEFT, padx=(15, 4))

        # Кнопка "Добавить"
        add_btn = tk.Button(bottom, text="✓ Добавить строку",
                            command=on_add,
                            bg="#90EE90", fg="#1a5c1a",
                            font=("Segoe UI", 10, "bold"),
                            padx=15, pady=6)
        add_btn.pack(side=tk.RIGHT, padx=4)

        # Кнопка "Завершить"
        finish_btn = tk.Button(bottom, text="Завершить",
                               command=on_finish,
                               bg="#4a90d9", fg="white",
                               font=("Segoe UI", 10, "bold"),
                               padx=15, pady=6)
        finish_btn.pack(side=tk.RIGHT, padx=4)

        # Горячие клавиши
        for e in entries:
            e.bind('<Return>', on_add)

        win.bind('<Escape>', on_close)
        win.bind('<Control-Return>', on_finish)
        win.bind('<Control-z>', on_undo)
        win.protocol("WM_DELETE_WINDOW", on_close)

        win.grab_set()
        win.wait_window()

        if own_root:
            own_root.destroy()

        return result["matrix"]

    def __repr__(self):
        return f"InputInMatrix({self.data})"