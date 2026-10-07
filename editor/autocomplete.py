# editor/autocomplete.py
"""
Всплывающее окно автодополнения.
"""

import tkinter as tk


class AutocompletePopup:
    def __init__(self, editor_widget, theme):
        self.editor = editor_widget
        self.theme = theme
        self.popup = None
        self.listbox = None
        self.items = []

    def show(self, items, position_x, position_y):
        T = self.theme
        if not items:
            self.hide()
            return
        self.items = items

        if self.popup is None or not self.popup.winfo_exists():
            self.popup = tk.Toplevel(self.editor)
            self.popup.wm_overrideredirect(True)
            self.popup.attributes('-topmost', True)

            frame = tk.Frame(self.popup, bg=T['border'], bd=1)
            frame.pack(fill=tk.BOTH, expand=True)

            self.listbox = tk.Listbox(
                frame, bg=T['bg_card'], fg=T['text'],
                selectbackground=T['accent_2'],
                selectforeground=T['text_inverse'],
                font=("Consolas", 10),
                borderwidth=0, highlightthickness=0,
                activestyle="none",
                height=min(10, len(items)), width=35,
            )
            self.listbox.pack(fill=tk.BOTH, expand=True, padx=1, pady=1)

        self.listbox.delete(0, tk.END)
        for item in items:
            self.listbox.insert(tk.END, item)

        self.listbox.selection_clear(0, tk.END)
        self.listbox.selection_set(0)
        self.listbox.see(0)
        self.listbox.config(height=min(10, len(items)))

        self.popup.wm_geometry(f"+{position_x}+{position_y}")
        self.popup.deiconify()
        self.popup.lift()

    def hide(self):
        if self.popup is not None and self.popup.winfo_exists():
            self.popup.destroy()
        self.popup = None
        self.listbox = None
        self.items = []

    def is_visible(self):
        return self.popup is not None and self.popup.winfo_exists()

    def move_selection(self, delta):
        if not self.listbox:
            return
        current = self.listbox.curselection()
        new_index = (current[0] + delta) if current else 0
        if 0 <= new_index < len(self.items):
            self.listbox.selection_clear(0, tk.END)
            self.listbox.selection_set(new_index)
            self.listbox.see(new_index)

    def get_selected(self):
        if not self.listbox:
            return None
        current = self.listbox.curselection()
        if not current:
            return None
        return self.items[current[0]]