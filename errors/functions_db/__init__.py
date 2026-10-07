# errors/functions_db/__init__.py
"""
База ошибок для всех операторов и функций.

СТРУКТУРА:
    Один файл — одна функция или группа.
    В каждом файле два словаря: RU и EN.
    Язык выбирается автоматически по настройке редактора.

ПУБЛИЧНЫЙ API:
    FUNCTIONS_DB_RU — все описания на русском
    FUNCTIONS_DB_EN — все описания на английском
    get_function_db() — база для текущего языка
    find_error(code)  — поиск ошибки по коду

ДИАГНОСТИКА:
    При старте выполняется _load_all(). Если в каком-то файле
    ошибка (SyntaxError, ImportError, …) — она печатается
    в stdout, но НЕ останавливает программу. Битый файл
    просто пропускается. Так редактор запускается и можно
    исправить проблему.
"""

import sys
import importlib
from pathlib import Path


# ============================================================
# СПИСОК ПРОБЛЕМНЫХ ФАЙЛОВ (для внешних инструментов)
# ============================================================
LOAD_ERRORS = []          # [(name, kind, msg, line), ...]


def _load_all():
    """
    Импортирует все .py из папки functions_db,
    кроме самого __init__.py.

    Файлы с префиксом _ (например, _operators.py,
    _statements.py) тоже загружаются — это
    групповые файлы для нескольких функций.

    ⚠️  Ошибки НЕ останавливают программу.
    Битый файл пропускается, его имя попадает в LOAD_ERRORS.
    """
    folder = Path(__file__).parent

    for path in sorted(folder.glob("*.py")):
        name = path.stem
        if name == "__init__":
            continue

        try:
            importlib.import_module(f"{__name__}.{name}")
        except Exception as e:
            # Ловим всё, что угодно — SyntaxError, ImportError,
            # любые другие исключения. НЕ останавливаем программу.
            line = getattr(e, 'lineno', None)
            LOAD_ERRORS.append(
                (name, type(e).__name__, str(e), line)
            )

    # Печатаем отчёт, если есть проблемы — но НЕ падаем.
    if LOAD_ERRORS:
        print()
        print("=" * 70)
        print("⚠️  ПРОБЛЕМЫ В ФАЙЛАХ БАЗЫ errors/functions_db/")
        print("=" * 70)
        for name, kind, msg, line in LOAD_ERRORS:
            print(f"  ⚠️  {name}.py: {kind}")
            if line:
                print(f"       строка {line}: {msg}")
            else:
                print(f"       {msg}")
        print("=" * 70)
        print("  Эти файлы пропущены. Ошибки из них НЕ подсказываются.")
        print("  Исправьте файлы и перезапустите редактор.")
        print("=" * 70)
        print()


def _collect(lang):
    """
    Собирает все словари `RU` или `EN` из всех модулей пакета.
    Возвращает большой словарь:
        { 'sort': {...}, 'filterif': {...}, ... }
    """
    result = {}
    for name, module in list(sys.modules.items()):
        if not name.startswith(__name__ + "."):
            continue
        if not hasattr(module, lang):
            continue
        d = getattr(module, lang)
        if isinstance(d, dict):
            result.update(d)
    return result


_load_all()

FUNCTIONS_DB_RU = _collect("RU")
FUNCTIONS_DB_EN = _collect("EN")


def get_function_db(lang=None):
    """
    Возвращает базу для указанного языка.
    Если lang=None — берёт из настроек редактора (errors.i18n).
    """
    if lang is None:
        try:
            from ..i18n import get_language
            lang = get_language()
        except Exception:
            lang = 'en'

    if lang == 'en':
        return FUNCTIONS_DB_EN
    return FUNCTIONS_DB_RU


def find_error(code):
    """
    Ищет ошибку по коду во всех функциях.
    Возвращает (function_name, error_data) или (None, None).
    """
    db = get_function_db()
    for fname, finfo in db.items():
        errors = finfo.get('errors', {})
        if code in errors:
            return (fname, errors[code])
    return (None, None)


def get_load_errors():
    """
    Возвращает список проблемных файлов при последней загрузке.
    Каждый элемент: (имя, тип_ошибки, сообщение, номер_строки).
    """
    return list(LOAD_ERRORS)


__all__ = [
    'FUNCTIONS_DB_RU',
    'FUNCTIONS_DB_EN',
    'get_function_db',
    'find_error',
    'get_load_errors',
    'LOAD_ERRORS',
]