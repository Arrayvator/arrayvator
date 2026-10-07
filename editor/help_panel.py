# editor/help_panel.py
"""
Панель справки справа в редакторе.
Регулируется мышью — тянем за разделитель.
Стиль компактный — как в редакторе.

ВОЗМОЖНОСТИ:
    - Кнопка "📋 Копировать" — копирует всю справку.
    - Выделение мышью + Ctrl+C — копирует выделенное.
    - Правый клик → "Копировать" / "Выделить всё".
    - Ctrl+A — выделить всю справку.
    - Текст НЕ редактируется (заблокировано).
"""

import os
import tkinter as tk
from tkinter import scrolledtext

from locales import t


class HelpPanel(tk.Frame):
    def __init__(self, parent, theme, syntax_palette=None, width=380):
        super().__init__(parent, bg=theme['bg_alt'], width=width)
        self.pack_propagate(False)
        self.theme = theme
        self.syntax_palette = syntax_palette or {}
        T = theme

        # ============================================================
        # ЗАГОЛОВОК + КНОПКА КОПИРОВАНИЯ
        # ============================================================
        header = tk.Frame(self, bg=T['bg_card'], height=42)
        header.pack(fill=tk.X)
        header.pack_propagate(False)

        tk.Label(
            header, text="📖  " + t("help_panel_title"),
            bg=T['bg_card'], fg=T['text'],
            font=("Segoe UI", 11, "bold"),
        ).pack(side=tk.LEFT, padx=14, pady=10)

        # Кнопка "📋 Копировать" — копирует всю справку
        self._copy_btn = tk.Button(
            header,
            text="📋 " + ("Копировать" if t("app_title").startswith("ArrayVator Р") else "Copy"),
            command=self._copy_all,
            bg=T['bg_card'], fg=T['text_dim'],
            activebackground=T['bg_card'], activeforeground=T['accent'],
            font=("Segoe UI", 9),
            relief="flat", bd=0,
            cursor="hand2",
            padx=8, pady=2,
        )
        self._copy_btn.pack(side=tk.RIGHT, padx=8)

        # ============================================================
        # ТЕКСТ СПРАВКИ
        # ============================================================
        self.text = scrolledtext.ScrolledText(
            self, wrap=tk.WORD, font=("Consolas", 10),
            bg=T['bg_alt'], fg=T['text'],
            padx=10, pady=10, relief="flat", borderwidth=0,
            highlightthickness=0,
            # ------------------------------------------------------
            # ВАЖНО: "normal" — чтобы можно было выделять текст!
            # Редактирование блокируем через bind-обработчики.
            # ------------------------------------------------------
            state="normal",
            cursor="arrow",       # обычная стрелка, не I-beam
            insertwidth=0,        # невидимый курсор ввода
        )
        self.text.pack(fill=tk.BOTH, expand=True)

        self._init_tags()
        self._make_readonly_but_selectable()
        self._add_context_menu()
        self._bind_shortcuts()
        self._show_welcome()

    # ============================================================
    # ЗАПРЕТ РЕДАКТИРОВАНИЯ (но выделение разрешено!)
    # ============================================================
    def _make_readonly_but_selectable(self):
        """
        Трюк: state="normal" разрешает выделение мышью и Ctrl+C,
        но мы блокируем ВСЕ клавиши кроме навигации и копирования.
        """
        NAV_KEYS = {
            'Left', 'Right', 'Up', 'Down',
            'Home', 'End', 'Prior', 'Next',
            'Shift_L', 'Shift_R',
            'Control_L', 'Control_R',
        }

        def on_key(event):
            # Навигация — разрешена
            if event.keysym in NAV_KEYS:
                return None

            # Ctrl+C, Ctrl+A — разрешены
            if event.state & 0x4:  # Ctrl нажат
                if event.keysym.lower() in ('c', 'a'):
                    return None
                return "break"

            # Всё остальное — блокируем (буквы, цифры, вставка и т.д.)
            return "break"

        self.text.bind("<Key>", on_key)

        # Явно блокируем вставку и вырезание
        self.text.bind("<<Paste>>", lambda e: "break")
        self.text.bind("<<Cut>>", lambda e: "break")

    # ============================================================
    # КОНТЕКСТНОЕ МЕНЮ (правый клик)
    # ============================================================
    def _add_context_menu(self):
        T = self.theme
        menu = tk.Menu(
            self.text, tearoff=0,
            bg=T['bg_card'], fg=T['text'],
            activebackground=T['accent_2'],
            activeforeground=T['text_inverse'],
            bd=0,
        )

        # Русский или английский — по локали
        is_ru = t("app_title").startswith("ArrayVator Р")
        copy_label = "📋 Копировать" if is_ru else "📋 Copy"
        sel_all_label = "✅ Выделить всё" if is_ru else "✅ Select all"

        menu.add_command(
            label=copy_label,
            command=lambda: self.text.event_generate("<<Copy>>"),
        )
        menu.add_command(
            label=sel_all_label,
            command=self._select_all,
        )

        def show_menu(event):
            try:
                menu.tk_popup(event.x_root, event.y_root)
            finally:
                menu.grab_release()

        self.text.bind("<Button-3>", show_menu)   # Windows / Linux
        self.text.bind("<Button-2>", show_menu)   # macOS

    # ============================================================
    # ГОРЯЧИЕ КЛАВИШИ
    # ============================================================
    def _bind_shortcuts(self):
        # Ctrl+A — выделить всё в справке
        self.text.bind("<Control-a>", self._select_all)
        self.text.bind("<Control-A>", self._select_all)
        # Ctrl+C — стандартное копирование, уже работает
        # Ctrl+Shift+C — копировать всю справку
        self.text.bind("<Control-Shift-C>", lambda e: (self._copy_all(), "break")[-1])

    # ============================================================
    # КОПИРОВАНИЕ
    # ============================================================
    def _copy_all(self):
        """Копирует всю справку в буфер обмена."""
        try:
            content = self.text.get("1.0", "end-1c")
            self.clipboard_clear()
            self.clipboard_append(content)

            # Показать обратную связь: временно меняем текст кнопки
            is_ru = t("app_title").startswith("ArrayVator Р")
            original = "📋 " + ("Копировать" if is_ru else "Copy")
            done = "✅ " + ("Скопировано" if is_ru else "Copied")

            self._copy_btn.config(text=done, fg=self.theme['green'])
            self.after(
                1500,
                lambda: self._copy_btn.config(
                    text=original, fg=self.theme['text_dim']
                ),
            )
        except Exception:
            pass

    def _select_all(self, event=None):
        """Выделяет весь текст справки."""
        self.text.tag_add("sel", "1.0", "end-1c")
        self.text.mark_set("insert", "1.0")
        self.text.see("insert")
        return "break"

    # ============================================================
    # ТЕГИ ОФОРМЛЕНИЯ — КОМПАКТНЫЕ
    # ============================================================
    def _init_tags(self):
        T = self.theme
        sp = self.syntax_palette

        # Заголовок (имя функции)
        kw = sp.get('keyword', {})
        self.text.tag_config(
            "title",
            font=("Consolas", 12, "bold"),
            foreground=kw.get('color', T['accent']),
            spacing1=0, spacing3=4,
        )

        # Синтаксис
        fn = sp.get('function', {})
        self.text.tag_config(
            "signature",
            font=("Consolas", 10, "bold"),
            foreground=fn.get('color', T['accent']),
            background=T['bg_code'],
            spacing1=2, spacing3=4,
            lmargin1=6, lmargin2=6,
        )

        # Описание
        self.text.tag_config(
            "description",
            font=("Consolas", 10),
            foreground=T['text_dim'],
            spacing1=0, spacing3=2,
            lmargin1=2, lmargin2=2,
        )

        # Заголовки блоков примеров
        self.text.tag_config(
            "example_label",
            font=("Consolas", 10, "bold"),
            foreground=T['green'],
            spacing1=6, spacing3=2,
        )
        self.text.tag_config(
            "matrix_label",
            font=("Consolas", 10, "bold"),
            foreground=T['purple'],
            spacing1=6, spacing3=2,
        )

        # Примеры
        str_color = sp.get('string', {}).get('color', T['text'])
        self.text.tag_config(
            "example",
            font=("Consolas", 10),
            foreground=str_color,
            background=T['bg_code'],
            spacing1=2, spacing3=4,
            lmargin1=6, lmargin2=6,
        )
        self.text.tag_config(
            "matrix",
            font=("Consolas", 10),
            foreground=str_color,
            background=T['bg_code'],
            spacing1=2, spacing3=4,
            lmargin1=6, lmargin2=6,
        )

        # Подсказки
        cm = sp.get('comment', {})
        self.text.tag_config(
            "hint",
            font=("Consolas", 9, "italic"),
            foreground=cm.get('color', T['text_muted']),
            spacing1=4, spacing3=2,
            lmargin1=6, lmargin2=6,
        )

    def set_syntax_palette(self, palette):
        self.syntax_palette = palette
        self._init_tags()
        self._show_welcome()

    # ============================================================
    # ВНУТРЕННИЙ ХЕЛПЕР: очистить + заполнить
    # ============================================================
    def _clear_and_insert(self, insert_func):
        """
        Очищает текст и вызывает insert_func.
        Используем state="normal" постоянно — не переключаем.
        """
        self.text.delete("1.0", tk.END)
        insert_func()
        self.text.see("1.0")

    # ============================================================
    # WELCOME
    # ============================================================
    def _show_welcome(self):
        def fill():
            self.text.insert(tk.END, t("welcome_title") + "\n\n", "title")
            self.text.insert(tk.END, t("welcome_how") + "\n\n", "description")
            self.text.insert(tk.END, t("welcome_step1") + "\n\n", "description")
            self.text.insert(tk.END, t("welcome_step2") + "\n\n", "description")
            self.text.insert(tk.END, t("welcome_step3") + "\n\n", "description")
            self.text.insert(tk.END, t("welcome_step4") + "\n\n", "description")
            self.text.insert(tk.END, t("welcome_step5") + "\n\n", "description")
            self.text.insert(tk.END, t("welcome_workdir") + "\n", "description")
            self.text.insert(tk.END, os.getcwd() + "\n", "example")
            self.text.insert(tk.END, "\n" + t("welcome_return") + "\n", "hint")
            self.text.insert(tk.END, "     m = filterif(m[:, \"Отдел\"] == \"IT\")\n", "hint")
            self.text.insert(tk.END, "     m = sort(m[:, \"Возраст\"], AZ)\n", "hint")

        self._clear_and_insert(fill)

    # ============================================================
    # СПРАВКА ПО ИМЕНИ ФУНКЦИИ
    # ============================================================
    def show_help(self, name):
        try:
            from syntax.autocomplete_data import get_help, get_autocomplete_list
            available = True
        except ImportError:
            available = False

        def fill():
            if not available:
                self.text.insert(tk.END, t("help_unavailable") + "\n", "title")
                self.text.insert(tk.END, t("help_module_missing"), "description")
                return

            info = get_help(name)

            if not info:
                self.text.insert(tk.END, f"'{name}'\n\n", "title")
                self.text.insert(tk.END, t("help_not_found") + "\n\n", "description")
                self.text.insert(tk.END, t("help_similar") + "\n", "description")
                similar = get_autocomplete_list(name.lower()[:2])[:5]
                if similar:
                    for s in similar:
                        self.text.insert(tk.END, f"    • {s}\n", "example")
                return

            # Заголовок
            self.text.insert(tk.END, f"{name}\n\n", "title")

            # Синтаксис
            signature = info.get('signature', '')
            if signature:
                self.text.insert(tk.END, f"{t('help_syntax')}\n", "example_label")
                self.text.insert(tk.END, f"  {signature}\n\n", "signature")

            # Описание
            description = info.get('description', '')
            if description:
                self.text.insert(tk.END, description + "\n", "description")

            # Пример
            example = info.get('example')
            if example:
                self.text.insert(tk.END, "\n" + t("help_example") + "\n", "example_label")
                self.text.insert(tk.END, example + "\n\n", "example")

            # Пример с матрицей
            matrix_example = info.get('matrix_example')
            if matrix_example:
                self.text.insert(
                    tk.END,
                    "\n" + t("help_matrix_example") + "\n",
                    "matrix_label"
                )
                self.text.insert(tk.END, matrix_example + "\n", "matrix")

            if not (example or matrix_example):
                self.text.insert(tk.END, "\n" + t("help_no_example"), "hint")

        self._clear_and_insert(fill)