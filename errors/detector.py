# errors/detector.py
"""
Анализатор для автоподсказок.
"""

from .i18n import t
from .syntax_db import BRACKET_PAIRS, CLOSING_BRACKETS, CONDITION_KEYWORDS


def _count_unbalanced_brackets(source):
    """
    Считает незакрытые скобки в ВСЁМ исходнике.
    Возвращает (stack, in_string, string_char, string_start).
    """
    stack = []
    in_string = False
    string_char = None
    string_start = -1
    i = 0
    
    while i < len(source):
        ch = source[i]
        
        if in_string:
            if ch == string_char:
                in_string = False
                string_char = None
                string_start = -1
            elif ch == '\\':
                i += 1  # пропускаем экранированный
        else:
            if ch in ('"', "'"):
                in_string = True
                string_char = ch
                string_start = i
            elif ch in BRACKET_PAIRS:
                stack.append((ch, i))
            elif ch in CLOSING_BRACKETS:
                if stack and stack[-1][0] == CLOSING_BRACKETS[ch]:
                    stack.pop()
        
        i += 1
    
    return stack, in_string, string_char, string_start


def detect_suggestion(source, pos, code=None):
    """
    Возвращает подсказку-словарь или None.
    
    Порядок проверок:
        1. Незакрытые скобки (приоритет выше)
        2. Незакрытые кавычки
        3. '=' вместо '==' в условии
        4. '==' вместо '=' в присваивании
    """
    
    # ============================================================
    # 1. АНАЛИЗИРУЕМ ВЕСЬ ИСХОДНИК (не только до pos!)
    # ============================================================
    stack, in_string, string_char, string_start = _count_unbalanced_brackets(source)
    
    # ============================================================
    # 2. НЕЗАКРЫТЫЕ СКОБКИ
    # ============================================================
    if stack:
        opener, opener_pos = stack[-1]
        closer = BRACKET_PAIRS[opener]
        
        bracket_names = {
            '(': ('круглой скобки', 'parenthesis'),
            '[': ('квадратной скобки', 'square bracket'),
            '{': ('фигурной скобки', 'curly brace'),
        }
        ru_name, en_name = bracket_names[opener]
        
        return {
            'issue': t(
                f"Не хватает закрывающей {ru_name} '{closer}'.",
                f"Missing closing {en_name} '{closer}'."
            ),
            'suggestion': t(
                f"Открывающая '{opener}' находится в позиции {opener_pos + 1}. Добавьте '{closer}'.",
                f"Opening '{opener}' at position {opener_pos + 1}. Add '{closer}'."
            ),
            'expected': closer,
        }
    
    # ============================================================
    # 3. НЕЗАКРЫТЫЕ КАВЫЧКИ
    # ============================================================
    if in_string:
        quote_name = 'двойной кавычки' if string_char == '"' else 'одинарной кавычки'
        quote_name_en = 'double quote' if string_char == '"' else 'single quote'
        
        return {
            'issue': t(
                f"Строка не закрыта. Не хватает закрывающей {quote_name} '{string_char}'.",
                f"String is not closed. Missing closing {quote_name_en} '{string_char}'."
            ),
            'suggestion': t(
                f"Открывающая кавычка '{string_char}' в позиции {string_start + 1}. Добавьте '{string_char}' в конце.",
                f"Opening quote '{string_char}' at position {string_start + 1}. Add '{string_char}' at the end."
            ),
            'expected': string_char,
        }
    
    # ============================================================
    # 4. '=' ВМЕСТО '==' В УСЛОВИИ
    # ============================================================
    if pos < len(source) and source[pos] == '=':
        # Не '=='
        if pos + 1 >= len(source) or source[pos + 1] != '=':
            before = source[:pos]
            # Есть ли if/while/filterif и т.д. в этой же строке?
            last_newline = before.rfind('\n')
            line_before = before[last_newline + 1:]
            
            for kw in CONDITION_KEYWORDS:
                if kw in line_before.lower():
                    return {
                        'issue': t(
                            "В условии используется '=' (присваивание) вместо '==' (сравнение).",
                            "In condition, '=' (assignment) is used instead of '==' (comparison)."
                        ),
                        'suggestion': t(
                            "Замените '=' на '=='.",
                            "Replace '=' with '=='."
                        ),
                        'expected': '==',
                    }
    
    # ============================================================
    # 5. '==' ВМЕСТО '=' В ПРИСВАИВАНИИ
    # ============================================================
    if pos + 1 < len(source) and source[pos:pos + 2] == '==':
        before = source[:pos]
        last_newline = before.rfind('\n')
        line_before = before[last_newline + 1:]
        
        is_condition = any(kw in line_before.lower() for kw in CONDITION_KEYWORDS)
        
        if not is_condition:
            return {
                'issue': t(
                    "Возможно, вы использовали '==' (сравнение) вместо '=' (присваивание).",
                    "You might have used '==' (comparison) instead of '=' (assignment)."
                ),
                'suggestion': t(
                    "Замените '==' на '='.",
                    "Replace '==' with '='."
                ),
                'expected': '=',
            }
    
    return None