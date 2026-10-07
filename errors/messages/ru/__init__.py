# errors/messages/ru/__init__.py
"""
Сборка всех русских сообщений об ошибках.
"""

from .common import MESSAGES as _common
from .strings import MESSAGES as _strings
from .functions import MESSAGES as _functions
from .syntax import MESSAGES as _syntax
from .runtime import MESSAGES as _runtime
from .reserved import MESSAGES as _reserved
from .files import MESSAGES as _files
from .types import MESSAGES as _types
from .dates import MESSAGES as _dates
from .window import MESSAGES as _window


def _merge(*dicts):
    result = {}
    for d in dicts:
        result.update(d)
    return result


MESSAGES_RU = _merge(
    _common,
    _strings,
    _functions,
    _syntax,
    _runtime,
    _reserved,
    _files,
    _types,
    _dates,
    _window,
)

__all__ = ['MESSAGES_RU']