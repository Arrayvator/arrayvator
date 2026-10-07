# main_app/files.py
"""
Операции с файлами: new, open, save, save_as, select_all, copy_all,
find_replace, open_work_dir.
"""

import os
import sys
import tkinter as tk
from pathlib import Path
from tkinter import filedialog, messagebox

from locales import t
from editor.find_replace import FindReplaceDialog


def new_file(app):
    app.editor.delete(1.0, tk.END)
    app.current_file = None
    app.root.title(t("app_title"))
    app.status_label.config(text=t("status_new"))


def open_file(app):
    filename = filedialog.askopenfilename(
        title=t("menu_open"),
        initialdir=os.getcwd(),
        filetypes=[
            ("ArrayVator files", "*.arrv"),
            ("Text files", "*.txt"),
            ("All files", "*.*"),
        ]
    )
    if filename:
        load_file(app, filename)


def load_file(app, filename):
    try:
        content = Path(filename).read_text(encoding='utf-8')
        app.editor.delete(1.0, tk.END)
        app.editor.insert(1.0, content)
        app.current_file = filename
        app.root.title(t("app_title_file",
                         name=os.path.basename(filename)))
        app.status_label.config(
            text=f"{t('status_opened')} {os.path.basename(filename)}"
        )
        app.editor._highlight_syntax()
    except Exception as e:
        messagebox.showerror(t("dlg_error"),
                             f"{t('dlg_open_error')}\n{e}")


def save_file(app):
    if not app.current_file:
        return save_file_as(app)
    try:
        content = app.editor.get(1.0, tk.END)
        Path(app.current_file).write_text(content, encoding='utf-8')
        app.status_label.config(
            text=f"{t('status_saved')} "
                 f"{os.path.basename(app.current_file)}"
        )
    except Exception as e:
        messagebox.showerror(t("dlg_error"),
                             f"{t('dlg_save_error')}\n{e}")


def save_file_as(app):
    filename = filedialog.asksaveasfilename(
        title=t("menu_save_as"),
        initialdir=os.getcwd(),
        defaultextension=".arrv",
        filetypes=[
            ("ArrayVator files", "*.arrv"),
            ("Text files", "*.txt"),
            ("All files", "*.*"),
        ]
    )
    if not filename:
        return
    app.current_file = filename
    app.root.title(t("app_title_file",
                     name=os.path.basename(filename)))
    save_file(app)


def select_all(app):
    app.editor.text.tag_add(tk.SEL, "1.0", tk.END)
    app.editor.text.mark_set(tk.INSERT, "1.0")
    app.editor.text.see(tk.INSERT)
    return "break"


def copy_all(app):
    content = app.editor.get(1.0, tk.END)
    app.root.clipboard_clear()
    app.root.clipboard_append(content)
    app.status_label.config(text=t("status_copied"))


def open_find_replace(app):
    FindReplaceDialog(app.root, app.editor, app.theme)


def open_work_dir(app):
    try:
        work_dir = os.getcwd()
        if sys.platform == 'win32':
            os.startfile(work_dir)
        elif sys.platform == 'darwin':
            os.system(f'open "{work_dir}"')
        else:
            os.system(f'xdg-open "{work_dir}"')
        app.status_label.config(
            text=f"{t('status_workdir')} {work_dir}"
        )
    except Exception as e:
        messagebox.showerror(t("dlg_error"), str(e))