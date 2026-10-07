# syntax/autocomplete/__init__.py
"""
Пакет данных для автодополнения и справки ArrayVator.

Разбит по темам. Каждый файл items_*.py содержит:

    RU = { имя: {'signature', 'description', 'example'} }
    EN = { имя: {'signature', 'description', 'example'} }

Публичный API — в syntax/autocomplete_data.py и autocomplete_data_en.py.
"""

from . import keywords
from . import special_words
from . import i18n