# editor/find_replace.py
"""
Диалог поиска и замены.
"""

import re
import tkinter as tk
from tkinter import messagebox

from locales import t
from theme import make_button


class FindReplaceDialog:
    def __init__(self, parent, editor, theme):
        self.editor = editor
        self.theme = theme
        T = theme

        self.window = tk.Toplevel(parent)
        self.window.title(t("find_title"))
        self.window.geometry("540x230")
        self.window.resizable(False, False)
        self.window.transient(parent)
        self.window.configure(bg=T['bg'])

        tk.Label(self.window, text=t("find_label"),
                 bg=T['bg'], fg=T['text'],
                 font=("Segoe UI", 10)).grid(
            row=0, column=0, sticky="w", padx=14, pady=10)

        self.find_entry = tk.Entry(
            self.window, width=42, font=("Consolas", 11),
            bg=T['bg_code'], fg=T['text'],
            insertbackground=T['accent'],
            relief="flat", bd=0,
            highlightthickness=1,
            highlightbackground=T['border'],
            highlightcolor=T['accent'],
        )
        self.find_entry.grid(row=0, column=1, padx=14, pady=10, columnspan=2)

        tk.Label(self.window, text=t("replace_label"),
                 bg=T['bg'], fg=T['text'],
                 font=("Segoe UI", 10)).grid(
            row=1, column=0, sticky="w", padx=14, pady=10)

        self.replace_entry = tk.Entry(
            self.window, width=42, font=("Consolas", 11),
            bg=T['bg_code'], fg=T['text'],
            insertbackground=T['accent'],
            relief="flat", bd=0,
            highlightthickness=1,
            highlightbackground=T['border'],
            highlightcolor=T['accent'],
        )
        self.replace_entry.grid(row=1, column=1, padx=14, pady=10, columnspan=2)

        self.case_var = tk.BooleanVar(value=False)
        tk.Checkbutton(
            self.window, text=t("find_case"),
            variable=self.case_var,
            bg=T['bg'], fg=T['text'],
            selectcolor=T['bg_card'],
            activebackground=T['bg'],
            activeforeground=T['text'],
            font=("Segoe UI", 10),
        ).grid(row=2, column=1, sticky="w", padx=14)

        btn_frame = tk.Frame(self.window, bg=T['bg'])
        btn_frame.grid(row=3, column=0, columnspan=3, pady=16)

        make_button(btn_frame, t("find_next"),
                    self.find_next, T, variant='ghost').pack(side=tk.LEFT, padx=4)
        make_button(btn_frame, t("find_replace_one"),
                    self.replace_one, T, variant='ghost').pack(side=tk.LEFT, padx=4)
        make_button(btn_frame, t("find_replace_all"),
                    self.replace_all, T, variant='primary').pack(side=tk.LEFT, padx=4)
        make_button(btn_frame, t("find_close"),
                    self.window.destroy, T, variant='danger').pack(side=tk.LEFT, padx=4)

        self.find_entry.focus_set()
        self.window.bind('<Return>', lambda e: self.find_next())
        self.window.bind('<Escape>', lambda e: self.window.destroy())

    def find_next(self):
        query = self.find_entry.get()
        if not query:
            return
        tw = self.editor.text
        case_sensitive = self.case_var.get()
        start = tw.index(tk.INSERT)
        pos = tw.search(query, start, stopindex=tk.END,
                        nocase=not case_sensitive)
        if not pos:
            pos = tw.search(query, "1.0", stopindex=tk.END,
                            nocase=not case_sensitive)
        if pos:
            end = f"{pos}+{len(query)}c"
            tw.tag_remove("search", "1.0", tk.END)
            tw.tag_add("search", pos, end)
            tw.tag_config("search",
                          background=self.theme['yellow'],
                          foreground=self.theme['text'])
            tw.mark_set(tk.INSERT, pos)
            tw.see(pos)
        else:
            messagebox.showinfo(t("find_title"),
                                f"{t('find_not_found')} {query}",
                                parent=self.window)

    def replace_one(self):
        query = self.find_entry.get()
        replacement = self.replace_entry.get()
        if not query:
            return
        tw = self.editor.text
        case_sensitive = self.case_var.get()
        start = tw.index(tk.INSERT)
        pos = tw.search(query, start, stopindex=tk.END,
                        nocase=not case_sensitive)
        if not pos:
            pos = tw.search(query, "1.0", stopindex=tk.END,
                            nocase=not case_sensitive)
        if pos:
            end = f"{pos}+{len(query)}c"
            tw.delete(pos, end)
            tw.insert(pos, replacement)
            tw.see(pos)
            self.editor._update_line_numbers()

    def replace_all(self):
        query = self.find_entry.get()
        replacement = self.replace_entry.get()
        if not query:
            return
        tw = self.editor.text
        case_sensitive = self.case_var.get()
        content = tw.get("1.0", tk.END)
        if case_sensitive:
            new_content = content.replace(query, replacement)
            count = content.count(query)
        else:
            pattern = re.compile(re.escape(query), re.IGNORECASE)
            new_content, count = pattern.subn(replacement, content)
        if count == 0:
            messagebox.showinfo(t("find_title"),
                                f"{t('find_not_found')} {query}",
                                parent=self.window)
            return
        tw.delete("1.0", tk.END)
        tw.insert("1.0", new_content)
        self.editor._update_line_numbers()
        messagebox.showinfo(t("find_title"),
                            f"{t('find_replaced')} {count}",
                            parent=self.window)