# main_app/settings_glue.py
"""
Настройки и шрифты.
"""

from editor.settings_dialog import open_settings_dialog


def apply_font(app):
    """Применяет шрифт и палитру из настроек."""
    font_family = app.settings.get("font_family", "Consolas")
    font_size = app.settings.get("font_size", 12)

    app.editor.set_font(font_family, font_size)
    app.editor.set_syntax_palette(app.syntax_palette)
    app.help_panel.set_syntax_palette(app.syntax_palette)


def open_settings(app):
    """Открывает диалог настроек."""
    open_settings_dialog(app.root, app)