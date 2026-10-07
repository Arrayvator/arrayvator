# syntax/signatures.py
"""
Публичный API базы сигнатур ArrayVator.

Собирает SIGNATURES из всех модулей syntax/signatures_data/*.py.

Экспортирует:
    FUNCTION_SIGNATURES     — словарь {имя: {name, category, args, examples}}
    get_signature(name)     — сигнатура по имени
    get_all_signatures()    — весь словарь
    get_signature_keywords(name)  — keywords из сигнатуры
    get_signature_errors(name)    — common_errors из сигнатуры
    find_error_by_wrong(code)     — поиск ошибки по неправильному коду

Совместимо с прежним API — остальной код проекта не меняется.
"""

from .signatures_data import io as _io
from .signatures_data import files as _files
from .signatures_data import convert as _convert
from .signatures_data import statistics as _statistics
from .signatures_data import math as _math
from .signatures_data import strings as _strings
from .signatures_data import filter as _filter
from .signatures_data import sort as _sort
from .signatures_data import modify as _modify
from .signatures_data import search as _search
from .signatures_data import dedup as _dedup
from .signatures_data import pivot as _pivot
from .signatures_data import abc as _abc
from .signatures_data import percentof as _percentof
from .signatures_data import anomaly as _anomaly
from .signatures_data import conditional as _conditional
from .signatures_data import groupby as _groupby
from .signatures_data import addcolumn as _addcolumn
from .signatures_data import sample as _sample
from .signatures_data import case as _case
from .signatures_data import dates as _dates
from .signatures_data import null as _null
from .signatures_data import types as _types
from .signatures_data import create as _create
from .signatures_data import window as _window
from .signatures_data import control as _control
from .signatures_data import numseq as _numseq

# Дополнительные модули
from .signatures_data import extras as _extras
from .signatures_data import calendar as _calendar


def _merge(*dicts):
    result = {}
    for d in dicts:
        result.update(d)
    return result


FUNCTION_SIGNATURES = _merge(
    _io.SIGNATURES,
    _files.SIGNATURES,
    _convert.SIGNATURES,
    _statistics.SIGNATURES,
    _math.SIGNATURES,
    _strings.SIGNATURES,
    _filter.SIGNATURES,
    _sort.SIGNATURES,
    _modify.SIGNATURES,
    _search.SIGNATURES,
    _dedup.SIGNATURES,
    _pivot.SIGNATURES,
    _abc.SIGNATURES,
    _percentof.SIGNATURES,
    _anomaly.SIGNATURES,
    _conditional.SIGNATURES,
    _groupby.SIGNATURES,
    _addcolumn.SIGNATURES,
    _sample.SIGNATURES,
    _case.SIGNATURES,
    _dates.SIGNATURES,
    _null.SIGNATURES,
    _types.SIGNATURES,
    _create.SIGNATURES,
    _window.SIGNATURES,
    _control.SIGNATURES,
    _numseq.SIGNATURES,
    _extras.SIGNATURES,
    _calendar.SIGNATURES,
)


# ============================================================
# ИНДЕКС ПО НАЗВАНИЮ
# ============================================================
def get_signature(func_name):
    """Возвращает сигнатуру функции по имени (регистронезависимо)."""
    name_lower = func_name.lower()
    for key, sig in FUNCTION_SIGNATURES.items():
        if key.lower() == name_lower:
            return sig
    return None


def get_all_signatures():
    return FUNCTION_SIGNATURES


def get_signature_keywords(func_name):
    sig = get_signature(func_name)
    if sig:
        return sig.get('keywords', [])
    return []


def get_signature_errors(func_name):
    sig = get_signature(func_name)
    if sig:
        return sig.get('common_errors', [])
    return []


def find_error_by_wrong(wrong_code):
    wrong_stripped = wrong_code.strip()
    for sig in FUNCTION_SIGNATURES.values():
        for err in sig.get('common_errors', []):
            if err['wrong'].strip() == wrong_stripped:
                return err
    return None


__all__ = [
    'FUNCTION_SIGNATURES',
    'get_signature',
    'get_all_signatures',
    'get_signature_keywords',
    'get_signature_errors',
    'find_error_by_wrong',
]