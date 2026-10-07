# main_app/loader.py
"""
Загрузка help-файлов (справка, лицензия, about).

Поддерживает оба варианта имён:
    Help.txt, Help_EN.txt, Help-EN.txt
    about.txt, about_EN.txt, about-EN.txt
    license.txt, license_EN.txt, license-EN.txt
    short_help_rus.txt, short_help_en.txt
"""

import os
from pathlib import Path

from locales import get_content_file
from .paths import get_help_search_paths


def _get_all_variants(filename):
    """
    Возвращает список вариантов имён для поиска.

    Пример: Help_EN.txt → [Help_EN.txt, Help-EN.txt, Help.txt]
    """
    variants = [filename]

    # Help_EN.txt → Help-EN.txt
    if "_EN" in filename:
        alt = filename.replace("_EN", "-EN")
        if alt not in variants:
            variants.append(alt)

        # Также пробуем lowercase вариант: help_en.txt
        lower = filename.replace("_EN", "_en")
        if lower not in variants:
            variants.append(lower)

        # И с маленькой буквы: Help_en.txt
        alt_lower = filename.replace("_EN", "-en")
        if alt_lower not in variants:
            variants.append(alt_lower)

    # Fallback на русский вариант
    if "_EN" in filename or "-EN" in filename:
        base = filename.replace("_EN", "").replace("-EN", "")
        if base not in variants:
            variants.append(base)

    return variants


def load_text_file(current_dir, base_name):
    """
    Загружает текстовый файл справки / лицензии / about.

    Ищет в help/ с учётом языка и разных форматов имён:
        Help.txt
        Help_EN.txt
        Help-EN.txt
        short_help_rus.txt
        short_help_en.txt
        ...
    """
    filename = get_content_file(base_name)

    # Все варианты имён для этого языка
    variants = _get_all_variants(filename)

    for variant in variants:
        candidates = get_help_search_paths(current_dir, variant)

        for path in candidates:
            if os.path.exists(path):
                try:
                    return Path(path).read_text(encoding='utf-8')
                except UnicodeDecodeError:
                    # Пробуем другие кодировки
                    for enc in ('cp1251', 'latin-1'):
                        try:
                            return Path(path).read_text(encoding=enc)
                        except Exception:
                            continue
                    return f"[{filename}: ошибка кодировки]"
                except Exception as e:
                    return f"[{filename}: {e}]"

    return f"[{filename} not found]"