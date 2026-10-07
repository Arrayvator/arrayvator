# syntax/autocomplete_data_en.py
"""
Публичный API базы автодополнения и справки (английская версия).
"""

from .autocomplete import keywords as _keywords
from .autocomplete import special_words as _special

from .autocomplete.items_input import EN as _en_input
from .autocomplete.items_output import EN as _en_output
from .autocomplete.items_logging import EN as _en_logging
from .autocomplete.items_excel import EN as _en_excel
from .autocomplete.items_csv import EN as _en_csv
from .autocomplete.items_txt import EN as _en_txt
from .autocomplete.items_parquet import EN as _en_parquet
from .autocomplete.items_sqlite import EN as _en_sqlite
from .autocomplete.items_bigdata import EN as _en_bigdata
from .autocomplete.items_statistics import EN as _en_statistics
from .autocomplete.items_math import EN as _en_math
from .autocomplete.items_strings import EN as _en_strings
from .autocomplete.items_filter import EN as _en_filter
from .autocomplete.items_sort import EN as _en_sort
from .autocomplete.items_insert import EN as _en_insert
from .autocomplete.items_search import EN as _en_search
from .autocomplete.items_dedup import EN as _en_dedup
from .autocomplete.items_pivot import EN as _en_pivot
from .autocomplete.items_abc import EN as _en_abc
from .autocomplete.items_percentof import EN as _en_percentof
from .autocomplete.items_anomaly import EN as _en_anomaly
from .autocomplete.items_conditional import EN as _en_conditional
from .autocomplete.items_groupby import EN as _en_groupby
from .autocomplete.items_addcolumn import EN as _en_addcolumn
from .autocomplete.items_sample import EN as _en_sample
from .autocomplete.items_case import EN as _en_case
from .autocomplete.items_join import EN as _en_join
from .autocomplete.items_dates import EN as _en_dates
from .autocomplete.items_calendar import EN as _en_calendar
from .autocomplete.items_null import EN as _en_null
from .autocomplete.items_types import EN as _en_types
from .autocomplete.items_create import EN as _en_create
from .autocomplete.items_charts import EN as _en_charts
from .autocomplete.items_reports import EN as _en_reports
from .autocomplete.items_window import EN as _en_window
from .autocomplete.items_numseq import EN as _en_numseq


# ============================================================
# СОБИРАЕМ AUTOCOMPLETE_ITEMS ИЗ ВСЕХ МОДУЛЕЙ
# ============================================================
def _merge(*dicts):
    result = {}
    for d in dicts:
        result.update(d)
    return result


AUTOCOMPLETE_ITEMS = _merge(
    _en_input,
    _en_output,
    _en_logging,
    _en_excel,
    _en_csv,
    _en_txt,
    _en_parquet,
    _en_sqlite,
    _en_bigdata,
    _en_statistics,
    _en_math,
    _en_strings,
    _en_filter,
    _en_sort,
    _en_insert,
    _en_search,
    _en_dedup,
    _en_pivot,
    _en_abc,
    _en_percentof,
    _en_anomaly,
    _en_conditional,
    _en_groupby,
    _en_addcolumn,
    _en_sample,
    _en_case,
    _en_join,
    _en_dates,
    _en_calendar,
    _en_null,
    _en_types,
    _en_create,
    _en_charts,
    _en_reports,
    _en_window,
    _en_numseq,
)


# ============================================================
# СПЕЦИАЛЬНЫЕ СЛОВА
# ============================================================
SPECIAL_WORDS = _special.EN


# ============================================================
# КЛЮЧЕВЫЕ СЛОВА (одни и те же для RU и EN)
# ============================================================
KEYWORDS = _keywords.KEYWORDS


# ============================================================
# ПОЛУЧИТЬ СПИСОК ДЛЯ АВТОДОПОЛНЕНИЯ
# ============================================================
def get_autocomplete_list(prefix):
    """Возвращает список подсказок (EN)."""
    if not prefix:
        return []

    prefix_lower = prefix.lower()

    starts_with = []
    ends_with = []

    def _collect(name):
        n = name.lower()
        if n.startswith(prefix_lower):
            if name not in starts_with:
                starts_with.append(name)
        elif n.endswith(prefix_lower):
            if name not in ends_with:
                ends_with.append(name)

    for name in AUTOCOMPLETE_ITEMS.keys():
        _collect(name)
    for name in SPECIAL_WORDS.keys():
        _collect(name)
    for kw in KEYWORDS:
        _collect(kw)

    starts_with.sort(key=lambda x: x.lower())
    ends_with.sort(key=lambda x: x.lower())

    return starts_with + ends_with


# ============================================================
# ПОЛУЧИТЬ СПРАВКУ ПО ИМЕНИ
# ============================================================
def get_help(name):
    """Возвращает справку (EN)."""
    if name in AUTOCOMPLETE_ITEMS:
        return AUTOCOMPLETE_ITEMS[name]
    for key in AUTOCOMPLETE_ITEMS:
        if key.lower() == name.lower():
            return AUTOCOMPLETE_ITEMS[key]

    if name in SPECIAL_WORDS:
        return SPECIAL_WORDS[name]
    for key in SPECIAL_WORDS:
        if key.lower() == name.lower():
            return SPECIAL_WORDS[key]

    return None