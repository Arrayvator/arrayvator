# errors/formatter.py
"""
Красивое форматирование ошибок ArrayVator.

Порядок поиска информации об ошибке:
    1. functions_db (по code) → полное описание с примерами:
         wrong / right / explanation / variants
    2. messages/ru или messages/en → простое сообщение
    3. error.message → как есть

Поддерживает ANSI-цвета. Автоматически отключает их для tkinter.
"""

import os
import sys

from .i18n import t, get_language
from .base import ArrayVatorError
from .detector import detect_suggestion
from .db_ru import MESSAGES_RU
from .db_en import MESSAGES_EN


# ============================================================
# ПОДКЛЮЧЕНИЕ functions_db (с защитой от ImportError)
# ============================================================
try:
    from .functions_db import get_function_db
    _FUNCTIONS_DB_AVAILABLE = True
except ImportError:
    _FUNCTIONS_DB_AVAILABLE = False

    def get_function_db(lang=None):
        return {}


# ============================================================
# ОПРЕДЕЛЕНИЕ ПОДДЕРЖКИ ЦВЕТОВ
# ============================================================
def _supports_color():
    if os.environ.get('ARRAYVATOR_NO_COLOR') == '1':
        return False

    if not hasattr(sys.stdout, 'isatty'):
        return False

    try:
        if not sys.stdout.isatty():
            return False
    except Exception:
        return False

    if sys.platform == 'win32':
        if os.environ.get('WT_SESSION') or os.environ.get('TERM_PROGRAM'):
            return True
        return False

    return True


_COLOR_ENABLED = _supports_color()


# ============================================================
# КЛАСС ЦВЕТОВ
# ============================================================
class C:
    RED = ''
    YELLOW = ''
    GREEN = ''
    CYAN = ''
    MAGENTA = ''
    BOLD = ''
    DIM = ''
    END = ''


def set_color_enabled(enabled):
    global _COLOR_ENABLED
    _COLOR_ENABLED = enabled

    if enabled:
        C.RED = '\033[91m'
        C.YELLOW = '\033[93m'
        C.GREEN = '\033[92m'
        C.CYAN = '\033[96m'
        C.MAGENTA = '\033[95m'
        C.BOLD = '\033[1m'
        C.DIM = '\033[2m'
        C.END = '\033[0m'
    else:
        C.RED = ''
        C.YELLOW = ''
        C.GREEN = ''
        C.CYAN = ''
        C.MAGENTA = ''
        C.BOLD = ''
        C.DIM = ''
        C.END = ''


set_color_enabled(_COLOR_ENABLED)


# ============================================================
# ПОЛУЧЕНИЕ СООБЩЕНИЯ ПО КОДУ (старая база)
# ============================================================
def _get_message(code):
    if get_language() == 'ru':
        return MESSAGES_RU.get(code, f"Ошибка: {code}")
    return MESSAGES_EN.get(code, f"Error: {code}")


# ============================================================
# ПОИСК В functions_db
# ============================================================
def _find_in_functions_db(code):
    if not code:
        return None

    db = get_function_db()

    for fname, finfo in db.items():
        errors = finfo.get('errors', {})
        if code in errors:
            return (fname, finfo, errors[code])

    return None


# ============================================================
# ФОРМАТИРОВАНИЕ ОШИБКИ
# ============================================================
def format_error(error):
    if not isinstance(error, ArrayVatorError):
        return f"\n{C.RED}{t('Ошибка', 'Error')}: {error}{C.END}\n"

    lines = []

    # --- ЗАГОЛОВОК ---
    header = t("❌ Ошибка", "❌ Error")
    if error.context and error.context.line is not None:
        header += t(
            f" (строка {error.context.line})",
            f" (line {error.context.line})",
        )

    lines.append("")
    lines.append(f"{C.RED}{C.BOLD}{header}:{C.END}")

    # --- СТРОКА КОДА С УКАЗАТЕЛЕМ ---
    if error.context and error.context.source_line is not None:
        source_line = error.context.source_line
        lines.append(f"  {source_line}")

        if error.context.column is not None:
            padding = " " * (2 + error.context.column)
            lines.append(f"{C.RED}{padding}^{C.END}")

    # --- ИЩЕМ В functions_db ---
    db_entry = _find_in_functions_db(error.code)

    if db_entry is not None:
        _format_from_functions_db(lines, error, db_entry)
    else:
        _format_fallback(lines, error)

    # --- АВТОПОДСКАЗКА ---
    if db_entry is None and error.context and error.context.source_code:
        _append_detected_suggestion(lines, error)

    lines.append("")
    return "\n".join(lines)


# ============================================================
# ФОРМАТ ИЗ functions_db
# ============================================================
def _format_from_functions_db(lines, error, db_entry):
    fname, finfo, err = db_entry

    # --- Сообщение ---
    message = err.get('message', '')
    if message:
        lines.append("")
        lines.append(f"  {message}")

    # ============================================================
    # Неправильно / Правильно — СЛОВАМИ
    # ============================================================
    wrong = err.get('wrong')
    right = err.get('right')

    if wrong or right:
        lines.append("")

        if wrong:
            for i, wline in enumerate(wrong.split('\n')):
                if i == 0:
                    prefix = f"  {C.RED}{t('Неправильно', 'Incorrect')}:{C.END}  "
                else:
                    prefix = "      "
                lines.append(f"{prefix}{C.RED}{wline}{C.END}")

        if right:
            for i, rline in enumerate(right.split('\n')):
                if i == 0:
                    prefix = f"  {C.GREEN}{t('Правильно', 'Correct')}:{C.END}  "
                else:
                    prefix = "      "
                lines.append(f"{prefix}{C.GREEN}{rline}{C.END}")

    # --- explanation ---
    explanation = err.get('explanation')
    if explanation:
        lines.append("")
        for i, eline in enumerate(explanation.split('\n')):
            if i == 0:
                lines.append(f"  {C.YELLOW}💡 {eline}{C.END}")
            else:
                lines.append(f"     {C.YELLOW}{eline}{C.END}")

    # --- variants ---
    variants = err.get('variants', [])
    if variants:
        lines.append("")
        lines.append(
            f"  {C.CYAN}📋 {t('Другие примеры', 'Other examples')}:{C.END}"
        )
        for v in variants:
            for j, vline in enumerate(v.split('\n')):
                if j == 0:
                    lines.append(f"     {C.CYAN}•{C.END} {vline}")
                else:
                    lines.append(f"       {vline}")

    # --- Синтаксис ---
    signature = finfo.get('signature')
    examples = finfo.get('examples', [])

    if signature:
        lines.append("")
        lines.append(
            f"  {C.DIM}{t('Синтаксис', 'Syntax')}:{C.END}  {signature}"
        )

    if examples and not variants:
        lines.append(f"  {C.DIM}{t('Примеры', 'Examples')}:{C.END}")
        for ex in examples[:3]:
            lines.append(f"     {ex}")


# ============================================================
# FALLBACK
# ============================================================
def _format_fallback(lines, error):
    message = None

    if error.code:
        message = _get_message(error.code)

    if error.message:
        message = error.message

    if message:
        lines.append("")
        for mline in str(message).split('\n'):
            lines.append(f"  {mline}")

    if error.suggestion:
        lines.append("")
        for sline in error.suggestion.split('\n'):
            lines.append(f"  {C.YELLOW}💡 {sline}{C.END}")

    if error.example:
        lines.append("")
        lines.append(
            f"  {C.GREEN}{t('Пример правильного кода', 'Correct code example')}:{C.END}"
        )
        for exline in error.example.split('\n'):
            lines.append(f"     {exline}")


# ============================================================
# АВТОПОДСКАЗКА
# ============================================================
def _append_detected_suggestion(lines, error):
    try:
        pos = 0
        if error.context.source_code and error.context.source_line:
            pos = error.context.source_code.find(error.context.source_line)
            if error.context.column:
                pos += error.context.column

        detected = detect_suggestion(
            error.context.source_code, pos, error.code
        )

        if detected:
            suggestion = detected.get('suggestion')
            issue = detected.get('issue')

            if issue:
                lines.append("")
                for iline in issue.split('\n'):
                    lines.append(f"  {C.YELLOW}{iline}{C.END}")

            if suggestion:
                lines.append("")
                for sline in suggestion.split('\n'):
                    lines.append(f"  {C.YELLOW}💡 {sline}{C.END}")

    except Exception:
        pass


# ============================================================
# ПЕЧАТЬ
# ============================================================
def print_error(error):
    print(format_error(error))