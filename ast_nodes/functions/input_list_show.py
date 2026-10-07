# ast_nodes/functions/input_list_show.py
"""
InputListShow — последовательный ввод в несколько целей
"""

from ..base import Node
from .input_show import _auto_convert, _center_window


class InputListShowNode(Node):
    """InputListShow([title: "Заголовок",] "подпись1", цель1, ...)"""

    def __init__(self, pairs, title=None):
        self.pairs = pairs
        self.title = title

    def evaluate(self, env):
        import tkinter as tk

        if not self.pairs:
            return None

        # Заголовок
        window_title = "Ввод данных"
        if self.title is not None:
            try:
                t = self.title.evaluate(env) if hasattr(self.title, 'evaluate') else self.title
                if isinstance(t, str) and t:
                    window_title = t
            except Exception:
                pass

        # Подписи
        labels = []
        for label_node, _ in self.pairs:
            if hasattr(label_node, 'evaluate'):
                try:
                    val = label_node.evaluate(env)
                except Exception:
                    val = label_node
            else:
                val = label_node
            labels.append(str(val) if val is not None else "")

        root = tk._default_root
        if root is None:
            own_root = tk.Tk()
            own_root.withdraw()
            parent = own_root
        else:
            own_root = None
            parent = root

        win = tk.Toplevel(parent)
        win.title(window_title)
        win.resizable(False, False)
        win.transient(parent)

        # Размеры и центрирование
        W = 520
        H = 110 + len(labels) * 45
        _center_window(win, W, H)

        tk.Label(win, text=window_title,
                 font=("Arial", 13, "bold")).pack(pady=12)

        frame = tk.Frame(win)
        frame.pack(fill=tk.BOTH, expand=True, padx=20)

        entries = []
        for label in labels:
            row = tk.Frame(frame)
            row.pack(fill=tk.X, pady=4)
            tk.Label(row, text=label, font=("Arial", 10),
                     width=20, anchor="w").pack(side=tk.LEFT)
            entry = tk.Entry(row, font=("Consolas", 11))
            entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
            entries.append(entry)

        if entries:
            entries[0].focus_set()

        result = {"values": None}

        def on_ok(event=None):
            values = [_auto_convert(e.get()) for e in entries]
            result["values"] = values
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
        btn.pack(pady=12)
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

        if result["values"] is None:
            return None

        for (label_node, target_node), value in zip(self.pairs, result["values"]):
            try:
                self._write_to_target(env, target_node, value)
            except Exception:
                pass

        return None

    def _write_to_target(self, env, target_node, value):
        from ast_nodes.variables import VariableNode
        from ast_nodes.index import IndexNode

        if isinstance(target_node, VariableNode):
            env.set(target_node.name, value)
            return

        if isinstance(target_node, IndexNode):
            matrix_obj = target_node.matrix.evaluate(env)
            if not hasattr(matrix_obj, 'data'):
                raise TypeError("Объект не является матрицей")

            indices = []
            for idx_node in target_node.indices:
                idx_val = idx_node.evaluate(env) if hasattr(idx_node, 'evaluate') else idx_node
                indices.append(idx_val)

            from operators.assign import AssignNode
            from ast_nodes.literals import NullNode

            assigner = AssignNode(
                var_name="__tmp__",
                value=NullNode(),
                is_matrix=False,
                is_index=True,
                index_node=target_node,
            )

            if len(indices) == 1:
                assigner._assign_single(matrix_obj, indices[0], value)
                return

            if len(indices) == 2:
                assigner._assign_double(matrix_obj, indices[0], indices[1], value)
                return

        raise TypeError(f"Неизвестный тип цели: {type(target_node).__name__}")

    def __repr__(self):
        if self.title is not None:
            return f"InputListShow(title: {self.title}, {len(self.pairs)} пар)"
        return f"InputListShow({len(self.pairs)} пар)"