# main_app/shortcuts.py
"""
Горячие клавиши.
"""


def bind_shortcuts(app):
    app.root.bind('<Control-n>', lambda e: app.new_file())
    app.root.bind('<Control-o>', lambda e: app.open_file())
    app.root.bind('<Control-s>', lambda e: app.save_file())
    app.root.bind('<Control-Shift-S>', lambda e: app.save_file_as())
    app.root.bind('<Control-f>', lambda e: app.open_find_replace())
    app.root.bind('<Control-a>', lambda e: app.select_all())
    app.root.bind('<Control-Shift-C>', lambda e: app.copy_all())
    app.root.bind('<Control-k>', lambda e: app.console.show())
    app.root.bind('<Control-e>', lambda e: app.show_export_help())
    app.root.bind('<F5>', lambda e: app.run_code())