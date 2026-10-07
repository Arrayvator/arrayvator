# parser/dispatch/_helpers.py
"""
Хелперы для диспетчеров.
"""


def call_parse(self, func_name, *args, **kwargs):
    """Поздний импорт parse-функции и вызов."""
    from .. import parse_functions
    fn = getattr(parse_functions, func_name)
    return fn(self, *args, **kwargs)