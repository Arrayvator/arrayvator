# editor/settings_dialog.py
"""
Диалог настроек: язык, тема, шрифт, палитра синтаксиса.
"""

import tkinter as tk
from tkinter import ttk, colorchooser, messagebox

from locales import t, set_language
from theme import get_syntax_palette, make_button, make_card


def open_settings_dialog(parent, app):
    """
    Открывает диалог настроек.
    app — ссылка на ArrayVatorEditor, чтобы менять настройки.
    """
    T = app.theme

    win = tk.Toplevel(parent)
    win.title(t("settings_title"))
    win.geometry("620x820")
    win.resizable(False, False)
    win.transient(parent)
    win.grab_set()
    win.configure(bg=T['bg'])

    btn_frame = tk.Frame(win, bg=T['bg'])
    btn_frame.pack(side=tk.BOTTOM, pady=14)

    common_card = make_card(win, T)
    common_card.pack(fill=tk.X, padx=14, pady=(14, 8))

    tk.Label(
        common_card, text="General",
        bg=T['bg_card'], fg=T['accent'],
        font=("Segoe UI", 11, "bold"),
    ).pack(anchor="w", padx=14, pady=(12, 6))

    lang_row = tk.Frame(common_card, bg=T['bg_card'])
    lang_row.pack(fill=tk.X, padx=14, pady=(0, 6))

    tk.Label(lang_row, text="Language:",
             bg=T['bg_card'], fg=T['text'],
             font=("Segoe UI", 10), width=14, anchor="w").pack(side=tk.LEFT)

    lang_var = tk.StringVar(value=app.settings.get("language", "en"))
    for val, label in [("en", "🇬🇧 English"), ("ru", "🇷🇺 Русский")]:
        tk.Radiobutton(
            lang_row, text=label, variable=lang_var, value=val,
            bg=T['bg_card'], fg=T['text'],
            selectcolor=T['bg_card'],
            activebackground=T['bg_card'],
            activeforeground=T['text'],
            font=("Segoe UI", 10),
        ).pack(side=tk.LEFT, padx=(0, 14))

    theme_row = tk.Frame(common_card, bg=T['bg_card'])
    theme_row.pack(fill=tk.X, padx=14, pady=(0, 6))

    tk.Label(theme_row, text="Theme:",
             bg=T['bg_card'], fg=T['text'],
             font=("Segoe UI", 10), width=14, anchor="w").pack(side=tk.LEFT)

    theme_var = tk.StringVar(value=app.settings.get("theme", "light"))
    for val, label in [("light", "☀ Light"), ("dark", "🌙 Dark")]:
        tk.Radiobutton(
            theme_row, text=label, variable=theme_var, value=val,
            bg=T['bg_card'], fg=T['text'],
            selectcolor=T['bg_card'],
            activebackground=T['bg_card'],
            activeforeground=T['text'],
            font=("Segoe UI", 10),
        ).pack(side=tk.LEFT, padx=(0, 14))

    font_row = tk.Frame(common_card, bg=T['bg_card'])
    font_row.pack(fill=tk.X, padx=14, pady=(0, 14))

    tk.Label(font_row, text="Font:",
             bg=T['bg_card'], fg=T['text'],
             font=("Segoe UI", 10), width=14, anchor="w").pack(side=tk.LEFT)

    font_var = tk.StringVar(value=app.settings.get("font_family", "Consolas"))
    ttk.Combobox(
        font_row, textvariable=font_var,
        values=["Consolas", "Courier New", "Segoe UI",
                "Arial", "Verdana", "Tahoma", "Georgia"],
        state="readonly", width=18,
    ).pack(side=tk.LEFT, padx=(0, 8))

    tk.Label(font_row, text="Size:",
             bg=T['bg_card'], fg=T['text'],
             font=("Segoe UI", 10)).pack(side=tk.LEFT, padx=(8, 4))

    size_var = tk.IntVar(value=app.settings.get("font_size", 12))
    tk.Spinbox(
        font_row, from_=8, to=24,
        textvariable=size_var, width=5,
    ).pack(side=tk.LEFT)

    syntax_card = make_card(win, T)
    syntax_card.pack(fill=tk.BOTH, expand=True, padx=14, pady=8)

    tk.Label(
        syntax_card, text="Syntax highlighting",
        bg=T['bg_card'], fg=T['accent'],
        font=("Segoe UI", 11, "bold"),
    ).pack(anchor="w", padx=14, pady=(12, 4))

    tk.Label(
        syntax_card,
        text="Color, bold, italic for each category",
        bg=T['bg_card'], fg=T['text_dim'],
        font=("Segoe UI", 9),
    ).pack(anchor="w", padx=14, pady=(0, 8))

    header_row = tk.Frame(syntax_card, bg=T['bg_card'])
    header_row.pack(fill=tk.X, padx=14, pady=(0, 4))

    tk.Label(header_row, text="Category",
             bg=T['bg_card'], fg=T['text_muted'],
             font=("Segoe UI", 9, "bold"),
             width=26, anchor="w").pack(side=tk.LEFT)
    tk.Label(header_row, text="Color",
             bg=T['bg_card'], fg=T['text_muted'],
             font=("Segoe UI", 9, "bold"),
             width=6).pack(side=tk.LEFT)
    tk.Label(header_row, text="B",
             bg=T['bg_card'], fg=T['text_muted'],
             font=("Segoe UI", 9, "bold"),
             width=4).pack(side=tk.LEFT)
    tk.Label(header_row, text="I",
             bg=T['bg_card'], fg=T['text_muted'],
             font=("Segoe UI", 9, "bold"),
             width=4).pack(side=tk.LEFT)

    syntax_keys = [
        ('keyword',  'Conditional operators'),
        ('function', 'Functions'),
        ('variable', 'Variables'),
        ('string',   'Text in quotes'),
        ('number',   'Numbers'),
        ('comment',  'Comments'),
        ('operator', 'Operators'),
    ]

    syntax_vars = {}
    color_buttons = {}

    for key, label in syntax_keys:
        entry = app.syntax_palette.get(key, {})
        color = entry.get('color', '#000000')
        bold = entry.get('bold', False)
        italic = entry.get('italic', False)

        row = tk.Frame(syntax_card, bg=T['bg_card'])
        row.pack(fill=tk.X, padx=14, pady=2)

        tk.Label(row, text=label,
                 bg=T['bg_card'], fg=T['text'],
                 font=("Segoe UI", 10),
                 width=26, anchor="w").pack(side=tk.LEFT)

        color_var = tk.StringVar(value=color)
        bold_var = tk.BooleanVar(value=bold)
        italic_var = tk.BooleanVar(value=italic)

        btn = tk.Button(
            row, text="  ", bg=color, width=4, bd=1, relief="solid",
            command=lambda k=key, cv=color_var, cb=color_buttons: _pick_color(k, cv, cb),
        )
        btn.pack(side=tk.LEFT, padx=2)
        color_buttons[key] = btn

        tk.Checkbutton(
            row, variable=bold_var,
            bg=T['bg_card'], fg=T['text'],
            selectcolor=T['bg_card'],
            activebackground=T['bg_card'],
            width=4,
        ).pack(side=tk.LEFT, padx=2)

        tk.Checkbutton(
            row, variable=italic_var,
            bg=T['bg_card'], fg=T['text'],
            selectcolor=T['bg_card'],
            activebackground=T['bg_card'],
            width=4,
        ).pack(side=tk.LEFT, padx=2)

        syntax_vars[key] = {
            'color': color_var,
            'bold': bold_var,
            'italic': italic_var,
        }

    def _pick_color(key, color_var, color_buttons):
        current = color_var.get()
        color = colorchooser.askcolor(color=current, title=f"Color: {key}")
        if color and color[1]:
            color_var.set(color[1])
            color_buttons[key].config(bg=color[1])

    def on_save():
        new_lang = lang_var.get()
        old_lang = app.settings.get("language", "en")
        new_theme = theme_var.get()
        old_theme = app.settings.get("theme", "light")

        app.settings.set("language", new_lang)
        set_language(new_lang)
        app.settings.set("theme", new_theme)
        app.settings.set("font_family", font_var.get())
        app.settings.set("font_size", size_var.get())

        new_syntax = {}
        for key, vars_dict in syntax_vars.items():
            new_syntax[key] = {
                'color': vars_dict['color'].get(),
                'bold': bool(vars_dict['bold'].get()),
                'italic': bool(vars_dict['italic'].get()),
            }
        app.settings.data["syntax"] = new_syntax
        app.settings.save()

        app.syntax_palette = get_syntax_palette(new_theme, new_syntax)
        app.editor.set_syntax_palette(app.syntax_palette)
        app.help_panel.set_syntax_palette(app.syntax_palette)
        app._apply_font()

        win.destroy()

        if new_lang != old_lang or new_theme != old_theme:
            messagebox.showinfo(
                t("settings_title"),
                t("restart_msg"),
                parent=parent,
            )

    def on_reset():
        lang_var.set("en")
        theme_var.set("light")
        font_var.set("Consolas")
        size_var.set(12)

        default = get_syntax_palette("light", None)
        for key, vars_dict in syntax_vars.items():
            entry = default[key]
            vars_dict['color'].set(entry['color'])
            vars_dict['bold'].set(entry['bold'])
            vars_dict['italic'].set(entry['italic'])
            color_buttons[key].config(bg=entry['color'])

    make_button(btn_frame, "💾  Save", on_save, T,
                variant='primary').pack(side=tk.LEFT, padx=6)
    make_button(btn_frame, "↺  Reset", on_reset, T,
                variant='ghost').pack(side=tk.LEFT, padx=6)
    make_button(btn_frame, "✕  Cancel", win.destroy, T,
                variant='ghost').pack(side=tk.LEFT, padx=6)