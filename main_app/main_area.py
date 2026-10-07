# main_app/main_area.py
"""
Создание основной области: редактор + разделитель + панель справки.

Используется grid для честного распределения ширины.
Панель справки регулируется мышью — тянем за вертикальный разделитель.
"""

import tkinter as tk

from editor.widgets import NumberedTextEditor
from editor.help_panel import HelpPanel


# ============================================================
# КОНСТАНТЫ
# ============================================================
HELP_MIN_WIDTH = 200        # минимум для панели справки
HELP_MAX_WIDTH = 2400       # фактически «без лимита»
HELP_DEFAULT_WIDTH = 420    # ширина по умолчанию
EDITOR_MIN_WIDTH = 250      # минимум для редактора


def create_main_area(app):
    T = app.theme

    # ============================================================
    # ВНЕШНИЙ КОНТЕЙНЕР — GRID
    # ============================================================
    container = tk.Frame(app.root, bg=T['bg'])
    container.pack(expand=True, fill=tk.BOTH)

    # 3 колонки:
    #   0 — редактор (растягивается)
    #   1 — разделитель (фиксированный 5px)
    #   2 — справка (фиксированная, но её можно тянуть)
    container.grid_columnconfigure(0, weight=1)   # редактор — тянется
    container.grid_columnconfigure(1, weight=0)   # разделитель — фикс
    container.grid_columnconfigure(2, weight=0)   # справка — фикс
    container.grid_rowconfigure(0, weight=1)

    # ============================================================
    # ЛЕВАЯ ЧАСТЬ — РЕДАКТОР
    # ============================================================
    left = tk.Frame(container, bg=T['bg'])
    left.grid(row=0, column=0, sticky="nsew")

    app.editor = NumberedTextEditor(
        left,
        settings=app.settings,
        theme=T,
        syntax_palette=app.syntax_palette,
    )
    app.editor.pack(expand=True, fill=tk.BOTH)
    app.editor.focus_set()
    app.editor.on_word_clicked = app._on_word_clicked

    # ============================================================
    # РАЗДЕЛИТЕЛЬ — ТЯНЕТСЯ МЫШЬЮ
    # ============================================================
    separator = tk.Frame(
        container,
        bg=T['border'],
        width=5,
        cursor="sb_h_double_arrow",
    )
    separator.grid(row=0, column=1, sticky="ns")
    separator.grid_propagate(False)

    # ============================================================
    # ПРАВАЯ ЧАСТЬ — СПРАВКА
    # ============================================================
    app.help_panel = HelpPanel(
        container,
        T,
        syntax_palette=app.syntax_palette,
        width=HELP_DEFAULT_WIDTH,
    )
    app.help_panel.grid(row=0, column=2, sticky="ns")
    app.help_panel.grid_propagate(False)

    # ============================================================
    # ЛОГИКА РЕСАЙЗА
    # ============================================================
    state = {
        'dragging': False,
        'start_x': 0,
        'start_width': HELP_DEFAULT_WIDTH,
    }

    def on_press(event):
        state['dragging'] = True
        state['start_x'] = event.x_root
        state['start_width'] = app.help_panel.winfo_width()

    def on_drag(event):
        if not state['dragging']:
            return

        delta = event.x_root - state['start_x']
        new_width = state['start_width'] - delta

        # Ограничения
        total_width = app.root.winfo_width()
        max_allowed = total_width - EDITOR_MIN_WIDTH - 10

        if new_width < HELP_MIN_WIDTH:
            new_width = HELP_MIN_WIDTH
        if new_width > HELP_MAX_WIDTH:
            new_width = HELP_MAX_WIDTH
        if new_width > max_allowed:
            new_width = max_allowed

        # Меняем ширину фрейма и колонки
        app.help_panel.config(width=new_width)
        container.grid_columnconfigure(2, minsize=new_width)

    def on_release(event):
        state['dragging'] = False

    def on_enter(event):
        separator.config(bg=T['accent'])

    def on_leave(event):
        if not state['dragging']:
            separator.config(bg=T['border'])

    # Привязка событий
    separator.bind("<ButtonPress-1>", on_press)
    separator.bind("<B1-Motion>", on_drag)
    separator.bind("<ButtonRelease-1>", on_release)
    separator.bind("<Enter>", on_enter)
    separator.bind("<Leave>", on_leave)

    container.bind("<ButtonRelease-1>", on_release)

    # Сохраняем в app для доступа
    app.help_separator = separator
    app.help_state = state