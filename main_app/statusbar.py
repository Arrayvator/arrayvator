# main_app/statusbar.py
"""
Создание статус-бара внизу окна.
"""

import tkinter as tk

from locales import t
from theme import make_separator


def create_statusbar(app):
    T = app.theme

    make_separator(app.root, T).pack(side=tk.BOTTOM, fill=tk.X)

    status_frame = tk.Frame(app.root, bg=T['bg_alt'], height=28)
    status_frame.pack(side=tk.BOTTOM, fill=tk.X)
    status_frame.pack_propagate(False)

    app.status_label = tk.Label(
        status_frame, text=t("status_ready"),
        font=("Consolas", 9),
        bg=T['bg_alt'], fg=T['text_dim'],
        anchor="w",
    )
    app.status_label.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=12)

    app.cursor_label = tk.Label(
        status_frame, text="1:1",
        font=("Consolas", 9),
        bg=T['bg_alt'], fg=T['text_dim'],
        anchor="e",
    )
    app.cursor_label.pack(side=tk.RIGHT, padx=12)

    app.editor.text.bind('<KeyRelease>', app._update_cursor_pos, add='+')
    app.editor.text.bind('<Button-1>', app._update_cursor_pos, add='+')