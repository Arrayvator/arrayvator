# main_app/runner.py
"""
Запуск кода ArrayVator.
"""

import os
import sys
import traceback
import tkinter as tk
from tkinter import messagebox

from locales import t
from lexer import Lexer
from parser import Parser
from errors import ArrayVatorError, format_error


# ============================================================
# ФЛАГ ЗАНЯТОСТИ
# ============================================================
_is_running = False


class _ConsoleRedirector:
    """Перенаправляет stdout/stderr в консоль редактора."""

    def __init__(self, console):
        self.console = console

    def write(self, text):
        if text:
            self.console.write(text)

    def flush(self):
        pass


def run_code(app):
    global _is_running

    # Защита от повторного запуска
    if _is_running:
        messagebox.showwarning(
            t("dlg_warning"),
            "Программа уже выполняется.\n"
            "Закройте все окна (графики, printshow) и попробуйте снова."
            if t("app_title").startswith("ArrayVator Редактор")
            else
            "Program is already running.\n"
            "Close all windows (charts, printshow) and try again."
        )
        return

    code = app.editor.get(1.0, tk.END)
    if not code.strip():
        messagebox.showwarning(t("dlg_warning"), t("dlg_no_code"))
        return

    _is_running = True

    app.console.show()
    app.console.write("\n" + "=" * 60 + "\n")
    app.console.write(t("run_start") + "\n")
    app.console.write("=" * 60 + "\n")
    app.console.write(f"{t('console_workdir')}: {os.getcwd()}\n\n")
    app.status_label.config(text=t("status_running"))

    old_stdout = sys.stdout
    old_stderr = sys.stderr

    sys.stdout = _ConsoleRedirector(app.console)
    sys.stderr = _ConsoleRedirector(app.console)

    try:
        try:
            from syntax import (check_all_lines, find_hint,
                                get_function_hint)
            syntax_available = True
        except ImportError:
            syntax_available = False

        if syntax_available:
            syntax_error = check_all_lines(code)
            if syntax_error:
                raise syntax_error

        lexer = Lexer(code)
        tokens = lexer.tokenize()
        parser = Parser(tokens, source=code)
        parser.parse_program()

        app.console.write("\n" + "=" * 60 + "\n")
        app.console.write(t("run_done") + "\n")
        app.console.write("=" * 60 + "\n\n")
        app.status_label.config(text=t("status_ok"))

    except ArrayVatorError as e:
        app.console.write("\n")
        app.console.write(format_error(e))

        if syntax_available:
            source_line = e.context.source_line if e.context else None
            hint_shown = False

            if source_line:
                line_hint = find_hint(source_line)
                if line_hint:
                    app.console.write("\n")
                    app.console.write_hint(f"💡 {line_hint['reason']}\n")
                    app.console.write_hint(line_hint['suggestion'] + "\n")
                    hint_shown = True

            if not hint_shown and source_line:
                func_hint = get_function_hint(source_line)
                if func_hint:
                    app.console.write("\n")
                    app.console.write_hint(func_hint['text'] + "\n")

        app.status_label.config(text=t("status_error"))

    except Exception as e:
        app.console.write("\n" + "=" * 60 + "\n")
        app.console.write(t("run_unexpected") + "\n")
        app.console.write("=" * 60 + "\n")
        app.console.write(str(e) + "\n\n")
        app.console.write(traceback.format_exc() + "\n")
        app.console.write("=" * 60 + "\n\n")
        app.status_label.config(text=t("status_error"))

    finally:
        sys.stdout = old_stdout
        sys.stderr = old_stderr
        _is_running = False