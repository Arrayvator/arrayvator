# syntax/__init__.py
"""
Пакет базы синтаксиса ArrayVator.

Публичный API — в syntax/signatures.py, syntax/checker.py, syntax/helpers.py,
syntax/db.py, syntax/autocomplete_data.py.

Явные импорты ниже нужны для PyInstaller:
    при сборке EXE он видит только то, что импортируется
    на верхнем уровне модулей. Если импорт спрятан внутри функции
    (как в help_panel.show_help), PyInstaller его не находит
    и не кладёт модуль в сборку.
"""

# Явные импорты для PyInstaller
from . import autocomplete_data   # noqa: F401
from . import signatures          # noqa: F401
from . import checker             # noqa: F401
from . import helpers             # noqa: F401
from . import db                  # noqa: F401