# errors/messages/ru/dates.py
"""
Ошибки функций работы с датами и временем.
"""

MESSAGES = {
    # ============================================================
    # СТАРЫЕ ДАТЫ
    # ============================================================
    "DATENOW_BAD_SYNTAX": "Неверный синтаксис datenow().",
    "TIMENOW_BAD_SYNTAX": "Неверный синтаксис timenow().",
    "DATETIME_BAD_FORMAT":
        "Неверный формат даты/времени.\n"
        "  Используйте: YYYY, YY, MM, DD, HH, SS.",

    "DATE_BAD_SYNTAX":
        "Неверный синтаксис date().\n"
        "  Формат: date(данные, \"входной_формат\", \"выходной_формат\")",

    "DATEDIFF_BAD_SYNTAX":
        "Неверный синтаксис DateDiff().\n"
        "  Формат: DateDiff(дата1, дата2, \"формат\", \"единица\")",

    "DATETRUNC_BAD_UNIT":
        "Неверная единица datetrunc().\n"
        "  Допустимо: 'day', 'month', 'quarter', 'year', "
        "'hour', 'minute', 'second'.\n"
        "\n"
        "  Неправильно: datetrunc(\"20.06.2025\", \"m\")\n"
        "  Правильно: datetrunc(\"20.06.2025\", \"day\")\n"
        "  Правильно: datetrunc(\"20.06.2025\", \"month\")\n"
        "  Правильно: datetrunc(\"20.06.2025\", \"quarter\")\n"
        "  Правильно: datetrunc(\"20.06.2025\", \"year\")\n"
        "  Правильно: datetrunc(\"14:30:15\", \"hour\")",

    # ============================================================
    # КАЛЕНДАРЬ
    # ============================================================
    "CALENDAR_BAD_FORMAT":
        "calendar: формат должен быть строкой.\n"
        "  Примеры:\n"
        "     Правильно: calendar(\"dd.mm.yyyy\", 1, 2026)\n"
        "     Правильно: calendar(\"yyyy-mm-dd\", all, 2026)\n"
        "     Правильно: calendar(\"dd MMMM yyyy\", 5, 2026)",

    "CALENDAR_BAD_YEAR":
        "calendar: год должен быть числом (1900–2200).\n"
        "  Примеры:\n"
        "     Правильно: calendar(\"dd.mm.yyyy\", 1, 2026)\n"
        "     Правильно: calendar(\"dd.mm.yyyy\", 1, 1981)\n"
        "     Правильно: calendar(\"dd.mm.yyyy\", 1, datenow())",

    "CALENDAR_BAD_MONTH":
        "calendar: месяц должен быть 1–12 или all.\n"
        "  Примеры:\n"
        "     Правильно: calendar(\"dd.mm.yyyy\", 1, 2026)\n"
        "     Правильно: calendar(\"dd.mm.yyyy\", all, 2026)\n"
        "     Неправильно: calendar(\"dd.mm.yyyy\", 13, 2026)\n"
        "     Неправильно: calendar(\"dd.mm.yyyy\", 0, 2026)",

    "CALENDAR_BAD_LOCALE":
        "calendar: локаль должна быть 'ru', 'eu' или 'us'.\n"
        "  Примеры:\n"
        "     Правильно: calendar(\"dd.mm.yyyy\", 1, 2026, \"ru\")\n"
        "     Правильно: calendar(\"dd.mm.yyyy\", 1, 2026, \"eu\")\n"
        "     Правильно: calendar(\"dd.mm.yyyy\", 1, 2026, \"us\")",

    "CALENDARPRO_BAD_YEAR":
        "calendarpro: год должен быть числом (1900–2200).\n"
        "  Примеры:\n"
        "     Правильно: calendarpro(2026, 1)\n"
        "     Правильно: calendarpro(datenow(), datenow())",

    "CALENDARPRO_BAD_MONTH":
        "calendarpro: месяц должен быть 1–12 или all.\n"
        "  Примеры:\n"
        "     Правильно: calendarpro(2026, 1)\n"
        "     Правильно: calendarpro(2026, all)",

    "CALENDARPRO_BAD_LOCALE":
        "calendarpro: локаль должна быть 'ru', 'eu' или 'us'.\n"
        "  Примеры:\n"
        "     Правильно: calendarpro(2026, 1, \"ru\")\n"
        "     Правильно: calendarpro(2026, 1, \"us\")",

    # ============================================================
    # ВРЕМЯ
    # ============================================================
    "TIMETRUNC_BAD_UNIT":
        "Неверная единица timetrunc().\n"
        "  Допустимо: 'hour', 'minute', 'second'.\n"
        "\n"
        "  Неправильно: timetrunc(\"14:30:15\", \"h\")\n"
        "  Неправильно: timetrunc(\"14:30:15\", \"day\")\n"
        "  Правильно: timetrunc(\"14:30:15\", \"hour\")     # \"14:00:00\"\n"
        "  Правильно: timetrunc(\"14:30:15\", \"minute\")   # \"14:30:00\"\n"
        "  Правильно: timetrunc(\"14:30:15\", \"second\")   # \"14:30:15\"",

    "TIMETRUNC_BAD_SYNTAX":
        "Неверный синтаксис timetrunc().\n"
        "  Формат: timetrunc(данные, \"единица\" [, \"формат\"])\n"
        "  Пример: timetrunc(\"14:30:15\", \"hour\")",

    "TIME_BAD_SYNTAX":
        "Неверный синтаксис time().\n"
        "  Формат: time(данные, \"входной_формат\", \"выходной_формат\")\n"
        "  Пример: time(\"02:30 PM\", \"hh:MM AM\", \"HH:MM\")\n"
        "  Пример: time(\"14:30\", \"HH:MM\", \"hh:MM AM\")",

    "DATE_EXTRACT_BAD_SYNTAX":
        "Неверный синтаксис функции извлечения.\n"
        "  Формат: hour / minute / second / ampm / is_pm / year / month / day\n"
        "          (данные [, \"формат\"])\n"
        "  Пример: hour(\"14:30:15\")\n"
        "  Пример: hour(m[:, \"Время\"], \"HH:MM:SS\")",

    "DATE_ADD_BAD_SYNTAX":
        "Неверный синтаксис функции арифметики.\n"
        "  Формат: addhours / addminutes / addseconds / adddays / addmonths / addyears\n"
        "          (данные, N [, \"формат\"])\n"
        "  Пример: addhours(\"14:30:15\", 2)\n"
        "  Пример: adddays(m[:, \"Дата\"], 10)",

    "VALID_TIME_BAD_SYNTAX":
        "Неверный синтаксис is_valid_time().\n"
        "  Формат: is_valid_time(данные [, \"формат\"])\n"
        "  Пример: is_valid_time(\"14:30:15\")\n"
        "  Пример: is_valid_time(m[:, \"Время\"], \"HH:MM:SS\")",
}