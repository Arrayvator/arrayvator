# main_app/toolbar.py
"""
Создание верхнего тулбара.
"""

import tkinter as tk

from theme import make_separator


def create_toolbar(app):
    T = app.theme

    toolbar = tk.Frame(app.root, bg=T['bg_alt'], height=44)
    toolbar.pack(side=tk.TOP, fill=tk.X)
    toolbar.pack_propagate(False)

    logo_frame = tk.Frame(toolbar, bg=T['bg_alt'])
    logo_frame.pack(side=tk.LEFT, padx=14, pady=8)

    tk.Label(
        logo_frame, text="AV",
        bg=T['accent_2'], fg=T['text_inverse'],
        font=("Segoe UI", 10, "bold"),
        width=3, height=1, bd=0,
    ).pack(side=tk.LEFT)

    tk.Label(
        logo_frame, text="ArrayVator",
        bg=T['bg_alt'], fg=T['text'],
        font=("Segoe UI", 11, "bold"),
    ).pack(side=tk.LEFT, padx=(8, 0))

    make_separator(app.root, T).pack(side=tk.TOP, fill=tk.X)