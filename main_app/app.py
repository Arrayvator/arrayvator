# main_app/app.py
"""
Главный класс ArrayVatorEditor.

Собирает всё вместе — но каждая часть в своём модуле.
"""

import os
import tkinter as tk

from locales import set_language, t
from theme import get_theme, get_syntax_palette

from editor.settings import Settings
from editor.console import ConsoleWindow

from .menu import create_menu
from .toolbar import create_toolbar
from .main_area import create_main_area
from .statusbar import create_statusbar
from .shortcuts import bind_shortcuts
from .settings_glue import apply_font, open_settings
from .files import (new_file, open_file, load_file,
                    save_file, save_file_as, select_all, copy_all,
                    open_find_replace, open_work_dir)
from .runner import run_code
from .export import show_export_help
from .help_windows import (
    open_help,
    open_short_help,
    open_help_folder,
    show_help_files_info,
    show_license,
    show_about,
)


class ArrayVatorEditor:
    def __init__(self, root, current_dir):
        self.root = root
        self.current_dir = current_dir

        # ============================================================
        # НАСТРОЙКИ
        # ============================================================
        settings_path = os.path.join(current_dir, "settings.json")
        self.settings = Settings(settings_path)

        lang = self.settings.get("language", "en")
        set_language(lang)

        self.theme_name = self.settings.get("theme", "light")
        self.theme = get_theme(self.theme_name)
        self.syntax_palette = get_syntax_palette(
            self.theme_name,
            self.settings.get("syntax", {}),
        )
        T = self.theme

        # ============================================================
        # ГЕОМЕТРИЯ
        # ============================================================
        w = self.settings.get("window_width", 1400)
        h = self.settings.get("window_height", 800)
        self.root.geometry(f"{w}x{h}")
        self.root.configure(bg=T['bg'])
        self.root.title(t("app_title"))

        # ============================================================
        # СОСТОЯНИЕ
        # ============================================================
        self.current_file = None
        self.console = ConsoleWindow(root, T)

        # ============================================================
        # СБОРКА UI
        # ============================================================
        create_menu(self)
        create_toolbar(self)
        create_main_area(self)
        create_statusbar(self)
        bind_shortcuts(self)
        apply_font(self)

        self.status_label.config(
            text=f"{t('status_ready_workdir')} {os.getcwd()}"
        )

    # ============================================================
    # ДЕЛЕГИРУЮЩИЕ МЕТОДЫ
    # ============================================================
    def new_file(self):
        return new_file(self)

    def open_file(self):
        return open_file(self)

    def _load_file(self, filename):
        return load_file(self, filename)

    def save_file(self):
        return save_file(self)

    def save_file_as(self):
        return save_file_as(self)

    def select_all(self):
        return select_all(self)

    def copy_all(self):
        return copy_all(self)

    def open_find_replace(self):
        return open_find_replace(self)

    def open_work_dir(self):
        return open_work_dir(self)

    def run_code(self):
        return run_code(self)

    def show_export_help(self):
        return show_export_help(self)

    # ------------------------------------------------------------
    # СПРАВКА
    # ------------------------------------------------------------
    def open_short_help(self):
        """Открывает краткую справку (short_help_rus.txt / short_help_en.txt)."""
        return open_short_help(self)

    def open_help(self):
        """Открывает полную справку (Help.txt / Help_EN.txt)."""
        return open_help(self)

    def open_help_folder(self):
        """Открывает папку help/ в проводнике."""
        return open_help_folder(self)

    def show_help_files_info(self):
        """Показывает информацию о файлах справки."""
        return show_help_files_info(self)

    def show_license(self):
        return show_license(self)

    def show_about(self):
        return show_about(self)

    def open_settings(self):
        return open_settings(self)

    def _apply_font(self):
        """Обёртка над apply_font для вызова из settings_dialog."""
        apply_font(self)

    # ============================================================
    # ОБРАБОТЧИКИ
    # ============================================================
    def _on_word_clicked(self, word):
        if word and len(word) >= 1:
            self.help_panel.show_help(word)

    def _update_cursor_pos(self, event=None):
        try:
            pos = self.editor.index(tk.INSERT)
            self.cursor_label.config(text=pos)
        except Exception:
            pass

    def close_app(self):
        try:
            if self.console:
                self.console.hide()
        except Exception:
            pass
        self.root.destroy()