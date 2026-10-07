# syntax/autocomplete/i18n.py
"""
Определение языка для автодополнения и справки.
"""


def get_language():
    """Возвращает текущий язык интерфейса: 'ru' или 'en'."""
    try:
        from locales import get_language as _get
        return _get()
    except Exception:
        return 'ru'