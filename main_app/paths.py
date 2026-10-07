# main_app/paths.py
"""
Пути и поиск файлов / компилятора.
"""

import os
import sys
from pathlib import Path


def get_help_search_paths(current_dir, filename):
    """
    Возвращает список путей, где искать help-файл.

    Порядок поиска:
        1. <current_dir>/help/<filename>              — dev-режим
        2. <current_dir>/_internal/help/<filename>    — PyInstaller onedir
        3. <sys._MEIPASS>/help/<filename>             — PyInstaller _MEIPASS
        4. <current_dir>/<filename>                   — корень (fallback)
    """
    candidates = [
        os.path.join(current_dir, "help", filename),
        os.path.join(current_dir, "_internal", "help", filename),
    ]

    meipass = getattr(sys, '_MEIPASS', None)
    if meipass:
        candidates.append(os.path.join(meipass, "help", filename))

    candidates.append(os.path.join(current_dir, filename))

    return candidates


def find_compiler(current_dir):
    """
    Ищет компилятор рядом с редактором.

    Возвращает (kind, path) где kind — 'exe' | 'py' | None.
    """
    if getattr(sys, 'frozen', False):
        base = Path(sys.executable).parent.resolve()
    else:
        base = Path(current_dir).resolve()

    candidates_exe = [
        base / "compiler" / "Compiler.exe",
        base / "compiler" / "compiler.exe",
        base / "compiler_gui.exe",
        base / "Compiler.exe",
    ]
    for exe in candidates_exe:
        if exe.exists():
            return ("exe", str(exe))

    py_candidates = [
        base / "compiler_gui.py",
        Path(current_dir) / "compiler_gui.py",
    ]
    for py in py_candidates:
        if py.exists():
            return ("py", str(py))

    return (None, None)