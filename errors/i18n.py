# errors/i18n.py
"""
Локализация сообщений об ошибках.

Синхронизирована с locales.py — общий язык
для интерфейса и сообщений об ошибках.
"""

_LANGUAGE = "en"


def set_language(lang):
    """Устанавливает язык: 'ru' или 'en'."""
    global _LANGUAGE
    if lang not in ('ru', 'en'):
        raise ValueError(f"Unsupported language: {lang}")
    _LANGUAGE = lang

    try:
        from locales import set_language as loc_set
        loc_set(lang)
    except Exception:
        pass


def get_language():
    """
    Возвращает текущий язык.

    Приоритет:
        1. Язык из locales (общий для всего приложения)
        2. Локальная переменная _LANGUAGE
    """
    global _LANGUAGE
    try:
        from locales import get_language as loc_get
        loc_lang = loc_get()
        if loc_lang in ('ru', 'en'):
            _LANGUAGE = loc_lang
            return loc_lang
    except Exception:
        pass
    return _LANGUAGE


def t(ru_text, en_text):
    """Возвращает текст на текущем языке."""
    return ru_text if get_language() == "ru" else en_text