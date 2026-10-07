# locales.py
"""
Локализация интерфейса ArrayVator Editor.
По умолчанию — английский.
"""

_LANGUAGE = "en"


def set_language(lang):
    """'ru' или 'en'."""
    global _LANGUAGE
    if lang not in ("ru", "en"):
        lang = "en"
    _LANGUAGE = lang


def get_language():
    return _LANGUAGE


# ============================================================
# СЛОВАРЬ СТРОК ИНТЕРФЕЙСА
# ============================================================
STRINGS = {
    # --- Окно ---
    "app_title": {
        "ru": "ArrayVator Редактор",
        "en": "ArrayVator Editor",
    },
    "app_title_file": {
        "ru": "ArrayVator Редактор — {name}",
        "en": "ArrayVator Editor — {name}",
    },

    # --- Меню Файл ---
    "menu_file":          {"ru": "Файл",           "en": "File"},
    "menu_new":           {"ru": "Новый",          "en": "New"},
    "menu_open":          {"ru": "Открыть...",     "en": "Open..."},
    "menu_open_as":       {"ru": "Открыть как...", "en": "Open as..."},
    "menu_save":          {"ru": "Сохранить",      "en": "Save"},
    "menu_save_as":       {"ru": "Сохранить как...", "en": "Save as..."},
    "menu_exit":          {"ru": "Выход",          "en": "Exit"},

    # --- Меню Правка ---
    "menu_edit":          {"ru": "Правка",         "en": "Edit"},
    "menu_undo":          {"ru": "Отменить",       "en": "Undo"},
    "menu_redo":          {"ru": "Повторить",      "en": "Redo"},
    "menu_select_all":    {"ru": "Выделить всё",   "en": "Select all"},
    "menu_copy_all":      {"ru": "Копировать всё", "en": "Copy all"},
    "menu_find_replace":  {"ru": "Поиск и замена...", "en": "Find and replace..."},

    # --- Меню Запуск ---
    "menu_run":           {"ru": "Запуск",              "en": "Run"},
    "menu_run_code":      {"ru": "Запустить",           "en": "Run"},
    "menu_show_console":  {"ru": "Показать консоль",    "en": "Show console"},
    "menu_clear_console": {"ru": "Очистить консоль",    "en": "Clear console"},
    "menu_open_workdir":  {"ru": "Открыть рабочую папку", "en": "Open working folder"},

    # --- Меню Инструменты ---
    "menu_tools":         {"ru": "Инструменты",        "en": "Tools"},
    "menu_export_exe":    {"ru": "Экспорт в EXE...",   "en": "Export to EXE..."},
    "menu_settings":      {"ru": "Настройки...",       "en": "Settings..."},

    # --- Меню Справка ---
    "menu_help":          {"ru": "Справка",            "en": "Help"},
    "menu_short_help":    {"ru": "📋 Краткая справка", "en": "📋 Quick reference"},
    "menu_open_help":     {"ru": "📖 Открыть справку", "en": "📖 Open help"},
    "menu_help_folder":   {"ru": "📁 Открыть папку справки", "en": "📁 Open help folder"},
    "menu_help_files_info": {
        "ru": "ℹ️  Информация о файлах справки",
        "en": "ℹ️  Help files info",
    },
    "menu_license":       {"ru": "📜 Лицензия",        "en": "📜 License"},
    "menu_about":         {"ru": "ℹ️  О программе",    "en": "ℹ️  About"},

    # --- Toolbar ---
    "tb_new":             {"ru": "📄 Новый",           "en": "📄 New"},
    "tb_open":            {"ru": "📂 Открыть",         "en": "📂 Open"},
    "tb_save":            {"ru": "💾 Сохранить",       "en": "💾 Save"},
    "tb_run":             {"ru": "▶ Запустить",        "en": "▶ Run"},
    "tb_find":            {"ru": "🔍 Поиск",           "en": "🔍 Find"},
    "tb_workdir":         {"ru": "📁 Рабочая папка",   "en": "📁 Working folder"},
    "tb_lang_label":      {"ru": "Язык ошибок:",       "en": "Error language:"},

    # --- Консоль ---
    "console_title":      {"ru": "Консоль ArrayVator", "en": "ArrayVator Console"},
    "console_clear":      {"ru": "Очистить",           "en": "Clear"},
    "console_copy":       {"ru": "Копировать",         "en": "Copy"},
    "console_save":       {"ru": "Сохранить",          "en": "Save"},
    "console_close":      {"ru": "Закрыть консоль",    "en": "Close console"},
    "console_workdir":    {"ru": "Рабочая папка",      "en": "Working folder"},
    "console_copied":     {"ru": "Скопировано в буфер", "en": "Copied to clipboard"},
    "console_saved":      {"ru": "Сохранено:",         "en": "Saved:"},

    # --- Панель справки ---
    "help_panel_title":   {"ru": "📖  Справка",        "en": "📖  Help"},
    "help_not_found":     {"ru": "Не найдено в справке.", "en": "Not found in help."},
    "help_similar":       {"ru": "Возможно, вы имели в виду:", "en": "Did you mean:"},
    "help_syntax":        {"ru": "СИНТАКСИС:",         "en": "SYNTAX:"},
    "help_example":       {"ru": "💻  ПРИМЕР:",         "en": "💻  EXAMPLE:"},
    "help_matrix_example": {
        "ru": "📊  ПРИМЕР С МАТРИЦЕЙ (вход → код → вывод):",
        "en": "📊  MATRIX EXAMPLE (input → code → output):",
    },
    "help_no_example":    {
        "ru": "(Для этой функции примеры пока не добавлены)",
        "en": "(No examples yet for this function)",
    },
    "help_unavailable":   {"ru": "Справка недоступна", "en": "Help unavailable"},
    "help_module_missing": {
        "ru": "Модуль справки не загружен.",
        "en": "Help module not loaded.",
    },

    # --- Welcome ---
    "welcome_title":      {"ru": "ArrayVator Редактор", "en": "ArrayVator Editor"},
    "welcome_how":        {"ru": "Как пользоваться:",  "en": "How to use:"},
    "welcome_step1":      {
        "ru": "1. Начните печатать название функции — появится список.\n   Tab / Enter — вставить, ↑↓ — навигация, Esc — закрыть.",
        "en": "1. Start typing a function name — a list appears.\n   Tab / Enter — insert, ↑↓ — navigate, Esc — close.",
    },
    "welcome_step2":      {
        "ru": "2. Кликните по имени функции — справа появится справка.",
        "en": "2. Click a function name — help appears on the right.",
    },
    "welcome_step3":      {"ru": "3. F5 — запустить программу.", "en": "3. F5 — run the program."},
    "welcome_step4":      {"ru": "4. Ctrl+F — поиск и замена.", "en": "4. Ctrl+F — find and replace."},
    "welcome_step5":      {"ru": "5. Инструменты → Настройки — шрифт и цвета.",
                            "en": "5. Tools → Settings — font and colors."},
    "welcome_workdir":    {"ru": "Рабочая папка:", "en": "Working folder:"},
    "welcome_example":    {"ru": "Пример:", "en": "Example:"},
    "welcome_return":     {
        "ru": "Все функции ВОЗВРАЩАЮТ результат.\nМутация — через присваивание в себя:",
        "en": "All functions RETURN a value.\nMutation — by assigning to itself:",
    },

    # --- Поиск / замена ---
    "find_title":         {"ru": "Поиск и замена",  "en": "Find and replace"},
    "find_label":         {"ru": "Найти:",          "en": "Find:"},
    "replace_label":      {"ru": "Заменить:",       "en": "Replace:"},
    "find_case":          {"ru": "Учитывать регистр", "en": "Match case"},
    "find_next":          {"ru": "Найти далее",     "en": "Find next"},
    "find_replace_one":   {"ru": "Заменить",        "en": "Replace"},
    "find_replace_all":   {"ru": "Заменить все",    "en": "Replace all"},
    "find_close":         {"ru": "Закрыть",         "en": "Close"},
    "find_not_found":     {"ru": "Не найдено:",     "en": "Not found:"},
    "find_replaced":      {"ru": "Заменено:",       "en": "Replaced:"},

    # --- Настройки ---
    "settings_title":          {"ru": "Настройки",           "en": "Settings"},
    "settings_font_group":     {"ru": "Шрифт",               "en": "Font"},
    "settings_family":         {"ru": "Семейство:",          "en": "Family:"},
    "settings_size":           {"ru": "Размер:",             "en": "Size:"},
    "settings_lang_group":     {"ru": "Язык",                "en": "Language"},
    "settings_lang_label":     {"ru": "Язык интерфейса:",    "en": "Interface language:"},
    "settings_colors_group":   {"ru": "Цвета подсветки",     "en": "Syntax highlighting"},
    "settings_col_keyword":    {"ru": "Ключевые слова (if, for, ...)", "en": "Keywords (if, for, ...)"},
    "settings_col_operator":   {"ru": "Операторы (==, !=, and, ...)",  "en": "Operators (==, !=, and, ...)"},
    "settings_col_function":   {"ru": "Функции (sum, filterif, ...)", "en": "Functions (sum, filterif, ...)"},
    "settings_col_string":     {"ru": "Строки (\"текст\")",   "en": "Strings (\"text\")"},
    "settings_col_number":     {"ru": "Числа (42, 3.14)",     "en": "Numbers (42, 3.14)"},
    "settings_col_comment":    {"ru": "Комментарии (# ...)",  "en": "Comments (# ...)"},
    "settings_style_bold":     {"ru": "Ж",                    "en": "B"},
    "settings_style_italic":   {"ru": "К",                    "en": "I"},
    "settings_save":           {"ru": "Сохранить",            "en": "Save"},
    "settings_reset":          {"ru": "Сбросить",             "en": "Reset"},
    "settings_cancel":         {"ru": "Отмена",               "en": "Cancel"},

    # --- Статусы ---
    "status_ready":        {"ru": "Готов",                    "en": "Ready"},
    "status_new":          {"ru": "Новый файл",               "en": "New file"},
    "status_running":      {"ru": "Выполнение...",            "en": "Running..."},
    "status_ok":           {"ru": "Выполнено успешно",        "en": "Completed successfully"},
    "status_error":        {"ru": "Ошибка выполнения",        "en": "Runtime error"},
    "status_copied":       {"ru": "Текст скопирован в буфер", "en": "Text copied to clipboard"},
    "status_opened":       {"ru": "Открыт:",                  "en": "Opened:"},
    "status_saved":        {"ru": "Сохранён:",                "en": "Saved:"},
    "status_workdir":      {"ru": "Открыта папка:",           "en": "Opened folder:"},
    "status_ready_workdir": {"ru": "Готов. Рабочая папка:",   "en": "Ready. Working folder:"},

    # --- О программе / Лицензия / Справка ---
    "about_window_title":   {"ru": "О программе",  "en": "About"},
    "license_window_title": {"ru": "Лицензия",     "en": "License"},
    "short_help_window_title": {
        "ru": "Краткая справка",
        "en": "Quick reference",
    },
    "help_files_window_title": {
        "ru": "Информация о файлах справки",
        "en": "Help files info",
    },

    # --- Экспорт EXE ---
    "export_title":  {"ru": "Экспорт в EXE", "en": "Export to EXE"},

    # --- Диалоги ---
    "dlg_error":         {"ru": "Ошибка",         "en": "Error"},
    "dlg_warning":       {"ru": "Предупреждение", "en": "Warning"},
    "dlg_info":          {"ru": "Информация",     "en": "Information"},
    "dlg_no_code":       {"ru": "Нет кода для выполнения", "en": "Nothing to run"},
    "dlg_save_error":    {"ru": "Не удалось сохранить:", "en": "Failed to save:"},
    "dlg_open_error":    {"ru": "Не удалось открыть:", "en": "Failed to open:"},
    "dlg_file_not_found": {"ru": "Файл не найден", "en": "File not found"},

    "run_start":         {"ru": "ЗАПУСК ПРОГРАММЫ", "en": "PROGRAM START"},
    "run_done":          {"ru": "ПРОГРАММА ВЫПОЛНЕНА УСПЕШНО", "en": "PROGRAM COMPLETED SUCCESSFULLY"},
    "run_unexpected":    {"ru": "НЕОЖИДАННАЯ ОШИБКА:", "en": "UNEXPECTED ERROR:"},

    # --- Сообщение о перезапуске ---
    "restart_msg": {
        "ru": "Изменения вступят в силу после перезапуска.",
        "en": "Changes will apply after restart.",
    },

    # --- Работа с папкой справки ---
    "status_help_folder_opened": {
        "ru": "Открыта папка справки:",
        "en": "Opened help folder:",
    },
    "dlg_help_folder_error": {
        "ru": "Не удалось открыть папку справки:",
        "en": "Failed to open help folder:",
    },
}


def t(key, **kwargs):
    """Возвращает перевод строки для текущего языка."""
    entry = STRINGS.get(key)
    if not entry:
        return key
    text = entry.get(_LANGUAGE) or entry.get("en") or key
    if kwargs:
        try:
            return text.format(**kwargs)
        except Exception:
            return text
    return text


def get_content_file(base_name):
    """
    Возвращает имя файла контента для текущего языка.

    Поддерживает:
        Help         → Help.txt / Help_EN.txt
        about        → about.txt / about_EN.txt
        license      → license.txt / license_EN.txt
        short_help   → short_help_rus.txt / short_help_en.txt

    ВАЖНО:
        - Для английского языка — суффикс _EN.
        - Для короткой справки — свои имена (short_help_rus / short_help_en).
    """
    # Спец-случай: короткая справка
    if base_name == "short_help":
        return "short_help_rus.txt" if _LANGUAGE == "ru" else "short_help_en.txt"

    if _LANGUAGE == "en":
        return f"{base_name}_EN.txt"
    return f"{base_name}.txt"


def get_help_file_variants(base_name):
    """
    Возвращает список ВСЕХ возможных имён файла для текущего языка.

    Полезно, если пользователь назвал файл с дефисом, а не подчёркиванием:
        Help_EN.txt
        Help-EN.txt
        help_en.txt
        ...

    Возвращает список имён в порядке приоритета.
    """
    # Спец-случай: короткая справка
    if base_name == "short_help":
        if _LANGUAGE == "ru":
            return ["short_help_rus.txt", "short_help_ru.txt", "short_help.txt"]
        return ["short_help_en.txt", "short_help_eng.txt"]

    variants = []

    if _LANGUAGE == "en":
        # Основной вариант
        variants.append(f"{base_name}_EN.txt")
        # С дефисом
        variants.append(f"{base_name}-EN.txt")
        # С маленькой _en
        variants.append(f"{base_name}_en.txt")
        # С маленькой -en
        variants.append(f"{base_name}-en.txt")
        # Fallback на русский
        variants.append(f"{base_name}.txt")
    else:
        # Русский — основной
        variants.append(f"{base_name}.txt")
        # На случай, если пользователь назвал _RU
        variants.append(f"{base_name}_RU.txt")
        variants.append(f"{base_name}-RU.txt")

    # Убираем дубликаты, сохраняя порядок
    seen = set()
    result = []
    for v in variants:
        if v not in seen:
            seen.add(v)
            result.append(v)

    return result