# ast_nodes/functions/input_show.py
"""
InputShow / InputShowForm — окна ввода с автоопределением типа
"""

from ..base import Node


# ============================================================
# ЦЕНТРИРОВАНИЕ ОКНА
# ============================================================
def _center_window(win, width, height):
    """Размещает окно по центру экрана"""
    try:
        win.update_idletasks()
        screen_w = win.winfo_screenwidth()
        screen_h = win.winfo_screenheight()
        x = (screen_w - width) // 2
        y = (screen_h - height) // 2
        win.geometry(f"{width}x{height}+{x}+{y}")
    except Exception:
        pass


# ============================================================
# АВТООПРЕДЕЛЕНИЕ ТИПА
# ============================================================
def _auto_convert(text):
    """Автоопределение типа: int / float / bool / None / str"""
    if text is None:
        return None
    if not isinstance(text, str):
        return text

    stripped = text.strip()
    if stripped == "":
        return ""

    lower = stripped.lower()
    if lower in ('null', 'none'):
        return None
    if lower == 'true':
        return True
    if lower == 'false':
        return False

    try:
        if '.' not in stripped and 'e' not in lower:
            if stripped.lstrip('-').isdigit():
                return int(stripped)
    except (ValueError, AttributeError):
        pass

    try:
        if '.' in stripped or 'e' in lower:
            return float(stripped)
    except (ValueError, AttributeError):
        pass

    return text


def _parse_matrix_text(text):
    """Парсит многострочный текст в матрицу"""
    from runtime.matrix import MatrExMatrix

    if not text:
        return MatrExMatrix([], True)

    lines = [line.strip() for line in text.strip().split('\n') if line.strip()]
    if not lines:
        return MatrExMatrix([], True)

    first_line = lines[0]
    delimiter = ','
    for d in [';', '\t', '|', ',', ' ']:
        if d in first_line:
            delimiter = d
            break

    rows = []
    for line in lines:
        cells = [cell.strip() for cell in line.split(delimiter)]
        converted = [_auto_convert(cell) for cell in cells]
        rows.append(converted)

    if rows:
        max_cols = max(len(r) for r in rows)
        for r in rows:
            while len(r) < max_cols:
                r.append("")

    return MatrExMatrix(rows, True)


# ============================================================
# УЗЛЫ
# ============================================================
class InputShowNode(Node):
    """InputShow([prompt] [, mode])"""

    def __init__(self, prompt=None, mode=None):
        self.prompt = prompt
        self.mode = mode

    def evaluate(self, env):
        import tkinter as tk

        prompt_text = "Введите значение:"
        if self.prompt is not None:
            p = self.prompt.evaluate(env) if hasattr(self.prompt, 'evaluate') else self.prompt
            if isinstance(p, str):
                prompt_text = p

        mode_val = "текст"
        if self.mode is not None:
            m = self.mode.evaluate(env) if hasattr(self.mode, 'evaluate') else self.mode
            if isinstance(m, str):
                mode_val = m.lower()

        result = {"value": None}

        root = tk._default_root
        if root is None:
            own_root = tk.Tk()
            own_root.withdraw()
            parent = own_root
        else:
            own_root = None
            parent = root

        # ============================================================
        # МНОГОСТРОЧНЫЙ РЕЖИМ (матрица)
        # ============================================================
        if mode_val in ('матрица', 'matrix'):
            win = tk.Toplevel(parent)
            win.title("Ввод матрицы")
            win.resizable(False, False)
            win.transient(parent)

            W, H = 500, 400
            _center_window(win, W, H)

            tk.Label(win, text=prompt_text, font=("Arial", 11, "bold")).pack(pady=10)
            tk.Label(win, text="Каждая строка — с новой строки. Разделитель: ,",
                     font=("Arial", 9), fg="#666").pack()

            text = tk.Text(win, font=("Consolas", 11), wrap=tk.NONE)
            text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
            text.focus_set()

            def on_ok():
                content = text.get("1.0", tk.END)
                result["value"] = _parse_matrix_text(content)
                win.destroy()

            def on_cancel():
                result["value"] = None
                win.destroy()

            btn = tk.Frame(win)
            btn.pack(pady=10)
            tk.Button(btn, text="OK", command=on_ok,
                      bg="#90EE90", width=12).pack(side=tk.LEFT, padx=5)
            tk.Button(btn, text="Отмена", command=on_cancel,
                      bg="#FF6B6B", fg="white", width=12).pack(side=tk.LEFT, padx=5)

            win.bind('<Escape>', lambda e: on_cancel())
            win.protocol("WM_DELETE_WINDOW", on_cancel)
            win.grab_set()

            win.wait_window()
            if own_root:
                own_root.destroy()
            return result["value"]

        # ============================================================
        # ОДНО ПОЛЕ
        # ============================================================
        win = tk.Toplevel(parent)
        win.title("Ввод")
        win.resizable(False, False)
        win.transient(parent)

        W, H = 400, 170
        _center_window(win, W, H)

        tk.Label(win, text=prompt_text, font=("Arial", 11)).pack(pady=15)

        entry = tk.Entry(win, font=("Consolas", 12), width=35)
        entry.pack(pady=5)
        entry.focus_set()

        def on_ok(event=None):
            content = entry.get()
            result["value"] = _auto_convert(content)
            win.destroy()

        def on_cancel(event=None):
            result["value"] = None
            win.destroy()

        entry.bind('<Return>', on_ok)

        btn = tk.Frame(win)
        btn.pack(pady=15)
        tk.Button(btn, text="OK", command=on_ok,
                  bg="#90EE90", width=12).pack(side=tk.LEFT, padx=5)
        tk.Button(btn, text="Отмена", command=on_cancel,
                  bg="#FF6B6B", fg="white", width=12).pack(side=tk.LEFT, padx=5)

        win.bind('<Escape>', lambda e: on_cancel())
        win.protocol("WM_DELETE_WINDOW", on_cancel)
        win.grab_set()

        win.wait_window()
        if own_root:
            own_root.destroy()

        return result["value"]

    def __repr__(self):
        if self.prompt is None:
            return "InputShow()"
        return f"InputShow({self.prompt})"


class InputShowFormNode(Node):
    """InputShowForm("Заголовок", "Поле1", "Поле2", ...)"""

    def __init__(self, title, fields):
        self.title = title
        self.fields = fields

    def evaluate(self, env):
        import tkinter as tk
        from runtime.matrix import MatrExMatrix

        title_text = "Ввод данных"
        if self.title is not None:
            t = self.title.evaluate(env) if hasattr(self.title, 'evaluate') else self.title
            if isinstance(t, str):
                title_text = t

        field_names = []
        for f in self.fields:
            fname = f.evaluate(env) if hasattr(f, 'evaluate') else f
            field_names.append(str(fname))

        if not field_names:
            return None

        result = {"values": None}

        root = tk._default_root
        if root is None:
            own_root = tk.Tk()
            own_root.withdraw()
            parent = own_root
        else:
            own_root = None
            parent = root

        win = tk.Toplevel(parent)
        win.title(title_text)
        win.resizable(False, False)
        win.transient(parent)

        # Размеры
        W = 450
        H = 100 + len(field_names) * 45
        _center_window(win, W, H)

        tk.Label(win, text=title_text, font=("Arial", 12, "bold")).pack(pady=10)

        entries = []
        frame = tk.Frame(win)
        frame.pack(fill=tk.BOTH, expand=True, padx=20)

        for name in field_names:
            row = tk.Frame(frame)
            row.pack(fill=tk.X, pady=4)
            tk.Label(row, text=name + ":", font=("Arial", 10), width=15,
                     anchor="w").pack(side=tk.LEFT)
            entry = tk.Entry(row, font=("Consolas", 11))
            entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
            entries.append(entry)

        if entries:
            entries[0].focus_set()

        def on_ok(event=None):
            values = [_auto_convert(e.get()) for e in entries]
            result["values"] = MatrExMatrix(values, False)
            win.destroy()

        def on_cancel(event=None):
            result["values"] = None
            win.destroy()

        for i, e in enumerate(entries):
            if i == len(entries) - 1:
                e.bind('<Return>', on_ok)
            else:
                e.bind('<Return>', lambda ev, idx=i: entries[idx + 1].focus_set())

        btn = tk.Frame(win)
        btn.pack(pady=15)
        tk.Button(btn, text="OK", command=on_ok,
                  bg="#90EE90", width=12).pack(side=tk.LEFT, padx=5)
        tk.Button(btn, text="Отмена", command=on_cancel,
                  bg="#FF6B6B", fg="white", width=12).pack(side=tk.LEFT, padx=5)

        win.bind('<Escape>', lambda e: on_cancel())
        win.protocol("WM_DELETE_WINDOW", on_cancel)
        win.grab_set()

        win.wait_window()
        if own_root:
            own_root.destroy()

        return result["values"]

    def __repr__(self):
        return f"InputShowForm({self.title}, {len(self.fields)} полей)"