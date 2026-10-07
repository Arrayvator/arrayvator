# main_app/help_windows.py
"""
Окна справки, лицензии, about.
Плюс — работа с папкой help/:
    - открыть папку в проводнике
    - показать информацию о файлах
"""

import os
import sys
import subprocess
import tkinter as tk
from tkinter import scrolledtext
from pathlib import Path

from locales import t, get_language
from theme import make_button

from .loader import load_text_file


# ============================================================
# ПРОСТЫЕ ОКНА СПРАВКИ
# ============================================================
def open_help(app):
    """Полная справка (Help.txt / Help_EN.txt)."""
    content = load_text_file(app.current_dir, "Help")
    _show_text_window(app, t("menu_open_help"), content)


def open_short_help(app):
    """Краткая справка (short_help_rus.txt / short_help_en.txt)."""
    content = load_text_file(app.current_dir, "short_help")
    _show_text_window(app, t("short_help_window_title"), content)


def show_license(app):
    content = load_text_file(app.current_dir, "license")
    _show_text_window(app, t("license_window_title"), content)


def show_about(app):
    content = load_text_file(app.current_dir, "about")
    _show_text_window(app, t("about_window_title"), content)


# ============================================================
# ПОИСК ПАПКИ help/
# ============================================================
def _find_help_dir(current_dir):
    """
    Ищет папку help/ в возможных местах.

    Возвращает Path или None.
    """
    candidates = [
        Path(current_dir) / "help",
        Path(current_dir) / "_internal" / "help",
    ]

    meipass = getattr(sys, '_MEIPASS', None)
    if meipass:
        candidates.append(Path(meipass) / "help")

    for candidate in candidates:
        try:
            if candidate.exists() and candidate.is_dir():
                return candidate
        except Exception:
            continue

    return None


# ============================================================
# ОТКРЫТЬ ПАПКУ help/ В ПРОВОДНИКЕ
# ============================================================
def open_help_folder(app):
    """
    Открывает папку help/ в проводнике.

    Если папки нет — создаёт её.
    """
    help_dir = _find_help_dir(app.current_dir)

    # Если нет — создаём рядом с current_dir
    if help_dir is None:
        help_dir = Path(app.current_dir) / "help"
        try:
            help_dir.mkdir(parents=True, exist_ok=True)
        except Exception as e:
            from tkinter import messagebox
            messagebox.showerror(
                t("dlg_error"),
                f"{t('dlg_help_folder_error')}\n{e}"
            )
            return

    # Открываем
    try:
        path_str = str(help_dir.resolve())

        if sys.platform == 'win32':
            os.startfile(path_str)
        elif sys.platform == 'darwin':
            subprocess.Popen(['open', path_str])
        else:
            subprocess.Popen(['xdg-open', path_str])

        app.status_label.config(
            text=f"{t('status_help_folder_opened')} {path_str}"
        )
    except Exception as e:
        from tkinter import messagebox
        messagebox.showerror(
            t("dlg_error"),
            f"{t('dlg_help_folder_error')}\n{e}"
        )


# ============================================================
# ИНФОРМАЦИЯ О ФАЙЛАХ СПРАВКИ
# ============================================================
def show_help_files_info(app):
    """
    Открывает окно со списком файлов справки:
    какие есть, на каком языке, где лежат.
    """
    T = app.theme
    is_ru = get_language() == "ru"

    win = tk.Toplevel(app.root)
    win.title(t("help_files_window_title"))
    win.geometry("720x560")
    win.configure(bg=T['bg'])

    # ------------------------------------------------------------
    # Заголовок
    # ------------------------------------------------------------
    tk.Label(
        win,
        text="📖  " + t("help_files_window_title"),
        bg=T['bg'], fg=T['text'],
        font=("Segoe UI", 12, "bold"),
    ).pack(pady=(14, 4))

    # Текущий язык
    lang_display = "🇷🇺 Русский" if is_ru else "🇬🇧 English"
    tk.Label(
        win,
        text=f"Текущий язык: {lang_display}" if is_ru
             else f"Current language: {lang_display}",
        bg=T['bg'], fg=T['text_dim'],
        font=("Segoe UI", 10),
    ).pack(pady=(0, 10))

    # ------------------------------------------------------------
    # Текстовая область
    # ------------------------------------------------------------
    text = scrolledtext.ScrolledText(
        win, wrap=tk.WORD, font=("Consolas", 10),
        bg=T['bg_code'], fg=T['text'],
        relief="flat", bd=0, padx=14, pady=14,
        highlightthickness=0,
    )
    text.pack(fill=tk.BOTH, expand=True, padx=14, pady=10)

    # ------------------------------------------------------------
    # Собираем содержимое
    # ------------------------------------------------------------
    lines = []

    lines.append("=" * 60)
    lines.append("ПАПКА СПРАВКИ" if is_ru else "HELP FOLDER")
    lines.append("=" * 60)

    help_dir = _find_help_dir(app.current_dir)

    if help_dir:
        lines.append(f"  {help_dir.resolve()}")
        lines.append("")

        # Файлы по категориям
        base_names = [
            ("Help", "📖 Основная справка" if is_ru else "📖 Main help"),
            ("short_help", "📋 Краткая справка" if is_ru else "📋 Quick reference"),
            ("about", "ℹ️  О программе" if is_ru else "ℹ️  About"),
            ("license", "📜 Лицензия" if is_ru else "📜 License"),
        ]

        # Возможные суффиксы
        suffixes = [
            ("", "🇷🇺 Russian"),
            ("_EN", "🇬🇧 English"),
            ("-EN", "🇬🇧 English"),
            ("_RU", "🇷🇺 Russian"),
            ("_rus", "🇷🇺 Russian"),
            ("_en", "🇬🇧 English"),
        ]

        for base, label in base_names:
            lines.append("-" * 60)
            lines.append(label)
            lines.append("-" * 60)

            found_any = False
            checked = set()

            for suffix, lang_label in suffixes:
                filename = f"{base}{suffix}.txt"
                if filename in checked:
                    continue
                checked.add(filename)

                filepath = help_dir / filename
                if filepath.exists():
                    size_kb = filepath.stat().st_size / 1024
                    lines.append(
                        f"  ✅ {filename:30s} {size_kb:7.1f} KB  {lang_label}"
                    )
                    found_any = True

            if not found_any:
                lines.append("  ❌ Файлы не найдены" if is_ru
                             else "  ❌ No files found")
            lines.append("")
    else:
        lines.append("  ❌ Папка help/ не найдена" if is_ru
                     else "  ❌ help/ folder not found")
        lines.append("")

    lines.append("=" * 60)
    lines.append("ПРАВИЛА ИМЕНОВАНИЯ:" if is_ru else "NAMING RULES:")
    lines.append("=" * 60)
    lines.append("")
    lines.append("  Help.txt          → 🇷🇺 Russian" if is_ru
                 else "  Help.txt          → 🇷🇺 Russian")
    lines.append("  Help_EN.txt       → 🇬🇧 English")
    lines.append("  short_help_rus.txt → 🇷🇺 Russian" if is_ru
                 else "  short_help_rus.txt → 🇷🇺 Russian")
    lines.append("  short_help_en.txt  → 🇬🇧 English")
    lines.append("  about.txt         → 🇷🇺 Russian" if is_ru
                 else "  about.txt         → 🇷🇺 Russian")
    lines.append("  about_EN.txt      → 🇬🇧 English")
    lines.append("  license.txt       → 🇷🇺 Russian" if is_ru
                 else "  license.txt       → 🇷🇺 Russian")
    lines.append("  license_EN.txt    → 🇬🇧 English")
    lines.append("")
    lines.append("Чтобы сменить язык:" if is_ru else "To change language:")
    lines.append("  • Инструменты → Настройки → Language" if is_ru
                 else "  • Tools → Settings → Language")

    text.insert("1.0", "\n".join(lines))
    text.config(state="disabled")

    # ------------------------------------------------------------
    # Кнопки
    # ------------------------------------------------------------
    btn_frame = tk.Frame(win, bg=T['bg'])
    btn_frame.pack(pady=(0, 14))

    def _open_folder():
        """Открывает папку справки в проводнике."""
        if help_dir:
            try:
                path_str = str(help_dir.resolve())
                if sys.platform == 'win32':
                    os.startfile(path_str)
                elif sys.platform == 'darwin':
                    subprocess.Popen(['open', path_str])
                else:
                    subprocess.Popen(['xdg-open', path_str])
            except Exception:
                pass

    make_button(
        btn_frame,
        "📁 Открыть папку" if is_ru else "📁 Open folder",
        _open_folder,
        T, variant='primary'
    ).pack(side=tk.LEFT, padx=6)

    make_button(
        btn_frame,
        "✕ Закрыть" if is_ru else "✕ Close",
        win.destroy,
        T, variant='ghost'
    ).pack(side=tk.LEFT, padx=6)


# ============================================================
# ОБЩЕЕ ОКНО ДЛЯ ТЕКСТА
# ============================================================
def _show_text_window(app, title, content):
    """Окно с текстом (для справки, лицензии, about)."""
    T = app.theme

    win = tk.Toplevel(app.root)
    win.title(title)
    win.geometry("900x700")
    win.configure(bg=T['bg'])

    text = scrolledtext.ScrolledText(
        win, wrap=tk.WORD, font=("Consolas", 11),
        bg=T['bg_code'], fg=T['text'],
        relief="flat", bd=0,
        highlightthickness=0,
        padx=14, pady=14,
    )
    text.pack(expand=True, fill=tk.BOTH, padx=8, pady=8)
    text.insert(1.0, content)
    text.config(state="disabled")

    make_button(win, "✕  " + t("find_close"),
                win.destroy, T, variant='danger').pack(pady=10)