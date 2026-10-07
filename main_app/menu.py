# main_app/menu.py
"""
Создание главного меню.
"""

import tkinter as tk

from locales import t


def create_menu(app):
    menubar = tk.Menu(app.root)

    # ============================================================
    # ФАЙЛ
    # ============================================================
    file_menu = tk.Menu(menubar, tearoff=0)
    file_menu.add_command(label=t("menu_new"), accelerator="Ctrl+N",
                          command=app.new_file)
    file_menu.add_command(label=t("menu_open"), accelerator="Ctrl+O",
                          command=app.open_file)
    file_menu.add_separator()
    file_menu.add_command(label=t("menu_save"), accelerator="Ctrl+S",
                          command=app.save_file)
    file_menu.add_command(label=t("menu_save_as"),
                          accelerator="Ctrl+Shift+S",
                          command=app.save_file_as)
    file_menu.add_separator()
    file_menu.add_command(label=t("menu_exit"), accelerator="Alt+F4",
                          command=app.close_app)
    menubar.add_cascade(label=t("menu_file"), menu=file_menu)

    # ============================================================
    # ПРАВКА
    # ============================================================
    edit_menu = tk.Menu(menubar, tearoff=0)
    edit_menu.add_command(label=t("menu_undo"), accelerator="Ctrl+Z",
                          command=lambda: app.editor.edit_undo())
    edit_menu.add_command(label=t("menu_redo"), accelerator="Ctrl+Y",
                          command=lambda: app.editor.edit_redo())
    edit_menu.add_separator()
    edit_menu.add_command(label=t("menu_select_all"), accelerator="Ctrl+A",
                          command=app.select_all)
    edit_menu.add_command(label=t("menu_copy_all"),
                          accelerator="Ctrl+Shift+C",
                          command=app.copy_all)
    edit_menu.add_separator()
    edit_menu.add_command(label=t("menu_find_replace"),
                          accelerator="Ctrl+F",
                          command=app.open_find_replace)
    menubar.add_cascade(label=t("menu_edit"), menu=edit_menu)

    # ============================================================
    # ЗАПУСК
    # ============================================================
    run_menu = tk.Menu(menubar, tearoff=0)
    run_menu.add_command(label=t("menu_run_code"), accelerator="F5",
                         command=app.run_code)
    run_menu.add_command(label=t("menu_show_console"), accelerator="Ctrl+K",
                         command=app.console.show)
    run_menu.add_command(label=t("menu_clear_console"),
                         command=app.console.clear)
    run_menu.add_separator()
    run_menu.add_command(label=t("menu_open_workdir"),
                         command=app.open_work_dir)
    menubar.add_cascade(label=t("menu_run"), menu=run_menu)

    # ============================================================
    # ИНСТРУМЕНТЫ
    # ============================================================
    tools_menu = tk.Menu(menubar, tearoff=0)
    tools_menu.add_command(label=t("menu_export_exe"),
                           accelerator="Ctrl+E",
                           command=app.show_export_help)
    tools_menu.add_separator()
    tools_menu.add_command(label=t("menu_settings"),
                           command=app.open_settings)
    menubar.add_cascade(label=t("menu_tools"), menu=tools_menu)

    # ============================================================
    # СПРАВКА
    # ============================================================
    help_menu = tk.Menu(menubar, tearoff=0)

    # --- Основное ---
    help_menu.add_command(label=t("menu_short_help"),
                          command=app.open_short_help)
    help_menu.add_command(label=t("menu_open_help"),
                          command=app.open_help)
    help_menu.add_separator()

    # --- Работа с файлами справки ---
    help_menu.add_command(label=t("menu_help_folder"),
                          command=app.open_help_folder)
    help_menu.add_command(label=t("menu_help_files_info"),
                          command=app.show_help_files_info)
    help_menu.add_separator()

    # --- О программе ---
    help_menu.add_command(label=t("menu_license"),
                          command=app.show_license)
    help_menu.add_command(label=t("menu_about"),
                          command=app.show_about)

    menubar.add_cascade(label=t("menu_help"), menu=help_menu)

    app.root.config(menu=menubar)