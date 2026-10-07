# errors/messages/__init__.py
"""
Пакет сообщений об ошибках.

Разбит по темам и языкам.
Публичный API:
    from errors.messages import MESSAGES_RU, MESSAGES_EN
    или
    from errors.messages.ru import MESSAGES_RU
    from errors.messages.en import MESSAGES_EN
"""

from .ru import MESSAGES_RU
from .en import MESSAGES_EN

__all__ = ['MESSAGES_RU', 'MESSAGES_EN']