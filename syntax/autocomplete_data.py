# syntax/autocomplete_data.py
"""
Единая точка доступа к базе автодополнения ArrayVator.

Собирает все данные из syntax/autocomplete/*.py:
    - AUTOCOMPLETE_ITEMS  — описания функций (RU)
    - AUTOCOMPLETE_ITEMS_EN — описания функций (EN)
    - SPECIAL_WORDS       — специальные слова (RU)
    - SPECIAL_WORDS_EN    — специальные слова (EN)
    - KEYWORDS            — ключевые слова (не переводятся)

И предоставляет публичный API:
    get_autocomplete_list(prefix) — список имён для попапа
    get_help(name)                — справка по имени
    get_items()                   — активный словарь функций (RU/EN)
    get_special_words()           — активный словарь спецслов (RU/EN)

ВАЖНО:
    При поиске учитываются АЛИАСЫ (русские и английские синонимы).
    Например:
        "сводная" → pivot
        "впр"     → vlookup
        "фильтр"  → filterif

ЯЗЫК:
    Все публичные функции (get_help, get_autocomplete_list,
    get_items, get_special_words) определяют язык ДИНАМИЧЕСКИ
    через locales.get_language() при каждом вызове.
    Это позволяет переключать язык без перезапуска редактора.
"""

import importlib


# ============================================================
# ОПРЕДЕЛЕНИЕ ЯЗЫКА
# ============================================================
def _get_language():
    """
    Возвращает 'ru' или 'en' (из locales, если доступно).

    Вызывается КАЖДЫЙ РАЗ при обращении к справке / автодополнению,
    поэтому смена языка в настройках сразу видна.
    """
    try:
        from locales import get_language
        lang = get_language()
        if lang in ('ru', 'en'):
            return lang
    except Exception:
        pass
    return 'en'


# ============================================================
# СБОРКА AUTOCOMPLETE_ITEMS
# ============================================================
def _import_items(module_path, ru_name='RU', en_name='EN'):
    """Импортирует модуль и возвращает (RU, EN) словари."""
    try:
        module = importlib.import_module(module_path)
        ru = getattr(module, ru_name, {}) or {}
        en = getattr(module, en_name, {}) or {}
        return ru, en
    except ImportError:
        return {}, {}


def _collect_items():
    """Собирает все items_* в один словарь (RU и EN)."""
    items_ru = {}
    items_en = {}

    modules = [
        'syntax.autocomplete.items_abc',
        'syntax.autocomplete.items_addcolumn',
        'syntax.autocomplete.items_anomaly',
        'syntax.autocomplete.items_bigdata',
        'syntax.autocomplete.items_calendar',
        'syntax.autocomplete.items_case',
        'syntax.autocomplete.items_charts',
        'syntax.autocomplete.items_conditional',
        'syntax.autocomplete.items_create',
        'syntax.autocomplete.items_csv',
        'syntax.autocomplete.items_dates',
        'syntax.autocomplete.items_dedup',
        'syntax.autocomplete.items_excel',
        'syntax.autocomplete.items_filter',
        'syntax.autocomplete.items_groupby',
        'syntax.autocomplete.items_input',
        'syntax.autocomplete.items_insert',
        'syntax.autocomplete.items_join',
        'syntax.autocomplete.items_logging',
        'syntax.autocomplete.items_math',
        'syntax.autocomplete.items_null',
        'syntax.autocomplete.items_numseq',
        'syntax.autocomplete.items_output',
        'syntax.autocomplete.items_parquet',
        'syntax.autocomplete.items_percentof',
        'syntax.autocomplete.items_pivot',
        'syntax.autocomplete.items_reports',
        'syntax.autocomplete.items_sample',
        'syntax.autocomplete.items_search',
        'syntax.autocomplete.items_sort',
        'syntax.autocomplete.items_sqlite',
        'syntax.autocomplete.items_statistics',
        'syntax.autocomplete.items_strings',
        'syntax.autocomplete.items_txt',
        'syntax.autocomplete.items_types',
        'syntax.autocomplete.items_window',
    ]

    for mod in modules:
        ru, en = _import_items(mod)
        items_ru.update(ru)
        items_en.update(en)

    return items_ru, items_en


def _collect_special_words():
    """Собирает SPECIAL_WORDS из special_words.py."""
    try:
        from syntax.autocomplete.special_words import RU, EN
        return (RU or {}), (EN or {})
    except ImportError:
        return {}, {}


def _collect_keywords():
    """Собирает KEYWORDS."""
    try:
        from syntax.autocomplete.keywords import KEYWORDS
        return list(KEYWORDS)
    except ImportError:
        return []


# ============================================================
# ГЛОБАЛЬНЫЕ СЛОВАРИ (замораживаются при первом импорте)
# ============================================================
# ВАЖНО:
#   Эти словари содержат оба языка ОДНОВРЕМЕННО.
#   Выбор активного языка делается в get_items() / get_special_words()
#   и в get_help() / get_autocomplete_list() — при каждом вызове.
#   Никакого кэша активного языка тут нет.
# ============================================================
_ITEMS_RU, _ITEMS_EN = _collect_items()
_SPECIAL_RU, _SPECIAL_EN = _collect_special_words()
KEYWORDS = _collect_keywords()


# ============================================================
# ПУБЛИЧНЫЕ СЛОВАРИ (для обратной совместимости)
# ============================================================
# Эти константы оставлены для тех мест, где код импортирует
# AUTOCOMPLETE_ITEMS / SPECIAL_WORDS напрямую (например, подсветка
# в editor/widgets.py). Они ВСЕГДА указывают на RU-версию.
#
# Для языко-зависимого доступа используйте:
#     get_items()         — активный словарь функций
#     get_special_words() — активный словарь спецслов
# ============================================================
AUTOCOMPLETE_ITEMS = _ITEMS_RU
AUTOCOMPLETE_ITEMS_EN = _ITEMS_EN
SPECIAL_WORDS = _SPECIAL_RU
SPECIAL_WORDS_EN = _SPECIAL_EN


def get_items():
    """
    Возвращает АКТИВНЫЙ словарь функций (RU или EN)
    в зависимости от текущего языка интерфейса.
    """
    return _ITEMS_EN if _get_language() == 'en' else _ITEMS_RU


def get_special_words():
    """
    Возвращает АКТИВНЫЙ словарь спецслов (RU или EN)
    в зависимости от текущего языка интерфейса.
    """
    return _SPECIAL_EN if _get_language() == 'en' else _SPECIAL_RU


# ============================================================
# АЛИАСЫ
# ============================================================
def _load_aliases():
    """Загружает алиасы (RU + EN)."""
    try:
        from syntax.autocomplete.aliases import (
            get_all_aliases,
            find_by_alias,
        )
        return get_all_aliases(), find_by_alias
    except ImportError:
        return {}, (lambda word: [])


_ALL_ALIASES, _find_by_alias = _load_aliases()


# ============================================================
# ПОИСК ДЛЯ АВТОДОПОЛНЕНИЯ
# ============================================================
def get_autocomplete_list(prefix):
    """
    Возвращает список имён для автодополнения.

    Логика:
        1. Прямое совпадение по началу имени (активный язык).
        2. Если ничего не найдено — поиск по АЛИАСАМ
           (русским и английским синонимам).

    Примеры:
        'sum'      → ['sum']
        'сводная'  → ['pivot']
        'впр'      → ['vlookup']
        'фильтр'   → ['filterif']
    """
    if not prefix:
        return []

    prefix_lower = prefix.lower().strip()

    # ============================================================
    # 1. Активный словарь по языку
    # ============================================================
    items = get_items()

    # ============================================================
    # 2. Прямой поиск по началу имени
    # ============================================================
    matches = [
        name for name in items.keys()
        if name.lower().startswith(prefix_lower)
    ]

    # ============================================================
    # 3. Если пусто — ищем по алиасам
    # ============================================================
    if not matches:
        matches = _find_by_alias(prefix_lower)

    # ============================================================
    # 4. Сортируем: точное совпадение → начало → всё остальное
    # ============================================================
    matches.sort(key=lambda x: (
        0 if x.lower() == prefix_lower else
        1 if x.lower().startswith(prefix_lower) else
        2,
        x.lower(),
    ))

    # ============================================================
    # 5. Убираем дубликаты, сохраняя порядок
    # ============================================================
    seen = set()
    result = []
    for m in matches:
        if m not in seen:
            seen.add(m)
            result.append(m)
    return result


# ============================================================
# СПРАВКА
# ============================================================
def _find_in_dict(name_lower, dictionary):
    """Ищет ключ (без учёта регистра) в словаре."""
    for key, value in dictionary.items():
        if key.lower() == name_lower:
            return value
    return None


def get_help(name):
    """
    Возвращает справку по имени функции/слова.

    Логика:
        1. Активный язык (RU или EN) — точное совпадение.
        2. Если не найдено — fallback на другой язык.
        3. Иначе — None.

    Возвращает словарь:
        { 'signature': ..., 'description': ..., 'example': ..., ... }
    Или None, если не найдено.
    """
    if not name:
        return None

    name_lower = name.lower()
    lang = _get_language()

    # ============================================================
    # 1. Активный язык
    # ============================================================
    if lang == 'en':
        primary_items = _ITEMS_EN
        primary_special = _SPECIAL_EN
        fallback_items = _ITEMS_RU
        fallback_special = _SPECIAL_RU
    else:
        primary_items = _ITEMS_RU
        primary_special = _SPECIAL_RU
        fallback_items = _ITEMS_EN
        fallback_special = _SPECIAL_EN

    # 1.1. AUTOCOMPLETE_ITEMS — активный язык
    result = _find_in_dict(name_lower, primary_items)
    if result is not None:
        return result

    # 1.2. SPECIAL_WORDS — активный язык
    result = _find_in_dict(name_lower, primary_special)
    if result is not None:
        return result

    # ============================================================
    # 2. Fallback на другой язык
    # ============================================================
    result = _find_in_dict(name_lower, fallback_items)
    if result is not None:
        return result

    result = _find_in_dict(name_lower, fallback_special)
    if result is not None:
        return result

    # ============================================================
    # 3. Не найдено
    # ============================================================
    return None


# ============================================================
# ДОПОЛНИТЕЛЬНЫЕ УТИЛИТЫ
# ============================================================
def get_all_names():
    """Все доступные имена (функции + спецслова) в нижнем регистре."""
    names = set()
    names.update(k.lower() for k in _ITEMS_RU.keys())
    names.update(k.lower() for k in _ITEMS_EN.keys())
    names.update(k.lower() for k in _SPECIAL_RU.keys())
    names.update(k.lower() for k in _SPECIAL_EN.keys())
    return sorted(names)


def get_alias_targets(word):
    """
    Возвращает список функций, на которые указывает алиас.
    Пустой список, если это не алиас.
    """
    return _find_by_alias(word.lower().strip()) if word else []


def is_alias(word):
    """Является ли слово алиасом (не именем функции)."""
    if not word:
        return False
    word_lower = word.lower().strip()
    # Если это уже имя функции (в любом языке) — не алиас
    if word_lower in (k.lower() for k in _ITEMS_RU.keys()):
        return False
    if word_lower in (k.lower() for k in _ITEMS_EN.keys()):
        return False
    return bool(_find_by_alias(word_lower))


def get_aliases_dict():
    """Возвращает словарь всех алиасов (для отладки)."""
    return dict(_ALL_ALIASES)


def reload_for_language(lang=None):
    """
    Принудительно пересобрать кэш (на случай hot-reload).

    Обычно НЕ нужен: словари содержат оба языка сразу,
    а выбор активного делается динамически.
    Оставлен для отладки и для случаев, когда пользователь
    редактирует items_*.py и хочет увидеть изменения
    без перезапуска редактора.
    """
    global _ITEMS_RU, _ITEMS_EN, _SPECIAL_RU, _SPECIAL_EN, KEYWORDS
    _ITEMS_RU, _ITEMS_EN = _collect_items()
    _SPECIAL_RU, _SPECIAL_EN = _collect_special_words()
    KEYWORDS = _collect_keywords()


__all__ = [
    # Константы (RU — по умолчанию, для подсветки и обратной совместимости)
    'AUTOCOMPLETE_ITEMS',
    'AUTOCOMPLETE_ITEMS_EN',
    'SPECIAL_WORDS',
    'SPECIAL_WORDS_EN',
    'KEYWORDS',

    # Активный язык
    'get_items',
    'get_special_words',

    # Публичный API
    'get_autocomplete_list',
    'get_help',

    # Утилиты
    'get_all_names',
    'get_alias_targets',
    'get_aliases_dict',
    'is_alias',
    'reload_for_language',
]