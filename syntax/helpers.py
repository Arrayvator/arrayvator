# syntax/helpers.py
"""
Вспомогательные функции для поиска сигнатур по строке кода.
"""

import re
from .signatures import FUNCTION_SIGNATURES


# ============================================================
# ВСЕ ИЗВЕСТНЫЕ ФУНКЦИИ
# ============================================================
KNOWN_FUNCTIONS = list(FUNCTION_SIGNATURES.keys())


def find_function_in_line(line):
    """
    Ищет название функции в строке кода.
    Возвращает название (в нижнем регистре) или None.
    """
    if not line:
        return None

    stripped = line.strip()
    if stripped.startswith('#'):
        return None

    for func_name in KNOWN_FUNCTIONS:
        pattern = r'\b' + re.escape(func_name) + r'\s*\('
        if re.search(pattern, stripped, re.IGNORECASE):
            return func_name.lower()

    return None


def get_function_hint(line):
    """
    Возвращает подсказку с синтаксисом функции из строки.

    Возвращает dict:
        - function: название функции
        - name:     человекочитаемое название
        - examples: примеры правильного синтаксиса
        - args:     описание аргументов
        - text:     готовый текст подсказки
    """
    if not line:
        return None

    func_name = find_function_in_line(line)
    if not func_name:
        return None

    from .signatures import get_signature
    sig = get_signature(func_name)
    if not sig:
        return None

    examples = sig.get('examples', [])
    args = sig.get('args', [])
    name = sig.get('name', func_name)

    lines = [f"Синтаксис {name}():"]

    if args:
        lines.append("")
        for arg in args:
            lines.append(f"  • {arg}")

    if examples:
        lines.append("")
        lines.append("Примеры:")
        for ex in examples[:3]:
            lines.append(f"     {ex}")

    return {
        'function': func_name,
        'name': name,
        'examples': examples,
        'args': args,
        'text': '\n'.join(lines),
    }