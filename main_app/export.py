# main_app/export.py
"""
Экспорт в EXE — запуск компилятора.
"""

import os
import sys
import subprocess
from tkinter import messagebox

from locales import t
from .paths import find_compiler


def show_export_help(app):
    kind, path = find_compiler(app.current_dir)

    if kind is None:
        messagebox.showerror(
            t("dlg_error"),
            "Compiler not found.\n\n"
            "Expected one of:\n"
            "  • <dir>/compiler/Compiler.exe\n"
            "  • <dir>/Compiler.exe\n"
            "  • <dir>/compiler_gui.py\n\n"
            "Put compiler/ folder next to ArrayVator.exe."
        )
        return

    if not app.current_file:
        code = app.editor.get(1.0, "end-1c").strip()
        if code:
            ans = messagebox.askyesnocancel(
                "Build EXE",
                "Current code is not saved to a file.\n\n"
                "Save as .arrv before opening the compiler?"
            )
            if ans is None:
                return
            if ans:
                app.save_file_as()
                if not app.current_file:
                    return

    try:
        if kind == "exe":
            # Прямой запуск файла — как двойной клик в проводнике.
            # os.startfile() использует Windows API и НЕ наследует
            # консоль/рабочую папку от ArrayVator.exe.
            # Это решает проблему, когда subprocess.Popen() падает
            # в frozen-сборке с --noconsole.
            os.startfile(path)
        else:
            # Python-скрипт — запускаем через интерпретатор.
            subprocess.Popen(
                [sys.executable, path],
                cwd=os.path.dirname(path),
            )
        app.status_label.config(text="Compiler started")
    except Exception as e:
        messagebox.showerror(
            t("dlg_error"),
            f"Failed to start compiler:\n{e}"
        )