# errors/messages/en/dates.py
"""
Errors for date and time functions.
"""

MESSAGES = {
    # ============================================================
    # OLD DATES
    # ============================================================
    "DATENOW_BAD_SYNTAX": "Invalid datenow() syntax.",
    "TIMENOW_BAD_SYNTAX": "Invalid timenow() syntax.",
    "DATETIME_BAD_FORMAT":
        "Invalid date/time format.\n"
        "  Use: YYYY, YY, MM, DD, HH, SS.",

    "DATE_BAD_SYNTAX":
        "Invalid date() syntax.\n"
        "  Format: date(data, \"input_format\", \"output_format\")",

    "DATEDIFF_BAD_SYNTAX":
        "Invalid DateDiff() syntax.\n"
        "  Format: DateDiff(date1, date2, \"format\", \"unit\")",

    "DATETRUNC_BAD_UNIT":
        "Invalid datetrunc() unit.\n"
        "  Allowed: 'day', 'month', 'quarter', 'year', "
        "'hour', 'minute', 'second'.\n"
        "\n"
        "  Неправильно: datetrunc(\"20.06.2025\", \"m\")\n"
        "  Правильно: datetrunc(\"20.06.2025\", \"day\")\n"
        "  Правильно: datetrunc(\"20.06.2025\", \"month\")\n"
        "  Правильно: datetrunc(\"20.06.2025\", \"quarter\")\n"
        "  Правильно: datetrunc(\"20.06.2025\", \"year\")\n"
        "  Правильно: datetrunc(\"14:30:15\", \"hour\")",

    # ============================================================
    # CALENDAR
    # ============================================================
    "CALENDAR_BAD_FORMAT":
        "calendar: format must be a string.\n"
        "  Examples:\n"
        "     Правильно: calendar(\"dd.mm.yyyy\", 1, 2026)\n"
        "     Правильно: calendar(\"yyyy-mm-dd\", all, 2026)\n"
        "     Правильно: calendar(\"dd MMMM yyyy\", 5, 2026)",

    "CALENDAR_BAD_YEAR":
        "calendar: year must be a number (1900–2200).\n"
        "  Examples:\n"
        "     Правильно: calendar(\"dd.mm.yyyy\", 1, 2026)\n"
        "     Правильно: calendar(\"dd.mm.yyyy\", 1, 1981)\n"
        "     Правильно: calendar(\"dd.mm.yyyy\", 1, datenow())",

    "CALENDAR_BAD_MONTH":
        "calendar: month must be 1–12 or all.\n"
        "  Examples:\n"
        "     Правильно: calendar(\"dd.mm.yyyy\", 1, 2026)\n"
        "     Правильно: calendar(\"dd.mm.yyyy\", all, 2026)\n"
        "     Неправильно: calendar(\"dd.mm.yyyy\", 13, 2026)\n"
        "     Неправильно: calendar(\"dd.mm.yyyy\", 0, 2026)",

    "CALENDAR_BAD_LOCALE":
        "calendar: locale must be 'ru', 'eu' or 'us'.\n"
        "  Examples:\n"
        "     Правильно: calendar(\"dd.mm.yyyy\", 1, 2026, \"ru\")\n"
        "     Правильно: calendar(\"dd.mm.yyyy\", 1, 2026, \"eu\")\n"
        "     Правильно: calendar(\"dd.mm.yyyy\", 1, 2026, \"us\")",

    "CALENDARPRO_BAD_YEAR":
        "calendarpro: year must be a number (1900–2200).\n"
        "  Examples:\n"
        "     Правильно: calendarpro(2026, 1)\n"
        "     Правильно: calendarpro(datenow(), datenow())",

    "CALENDARPRO_BAD_MONTH":
        "calendarpro: month must be 1–12 or all.\n"
        "  Examples:\n"
        "     Правильно: calendarpro(2026, 1)\n"
        "     Правильно: calendarpro(2026, all)",

    "CALENDARPRO_BAD_LOCALE":
        "calendarpro: locale must be 'ru', 'eu' or 'us'.\n"
        "  Examples:\n"
        "     Правильно: calendarpro(2026, 1, \"ru\")\n"
        "     Правильно: calendarpro(2026, 1, \"us\")",

    # ============================================================
    # TIME
    # ============================================================
    "TIMETRUNC_BAD_UNIT":
        "Invalid timetrunc() unit.\n"
        "  Allowed: 'hour', 'minute', 'second'.\n"
        "\n"
        "  Неправильно: timetrunc(\"14:30:15\", \"h\")\n"
        "  Неправильно: timetrunc(\"14:30:15\", \"day\")\n"
        "  Правильно: timetrunc(\"14:30:15\", \"hour\")     # \"14:00:00\"\n"
        "  Правильно: timetrunc(\"14:30:15\", \"minute\")   # \"14:30:00\"\n"
        "  Правильно: timetrunc(\"14:30:15\", \"second\")   # \"14:30:15\"",

    "TIMETRUNC_BAD_SYNTAX":
        "Invalid timetrunc() syntax.\n"
        "  Format: timetrunc(data, \"unit\" [, \"format\"])\n"
        "  Example: timetrunc(\"14:30:15\", \"hour\")",

    "TIME_BAD_SYNTAX":
        "Invalid time() syntax.\n"
        "  Format: time(data, \"input_format\", \"output_format\")\n"
        "  Example: time(\"02:30 PM\", \"hh:MM AM\", \"HH:MM\")\n"
        "  Example: time(\"14:30\", \"HH:MM\", \"hh:MM AM\")",

    "DATE_EXTRACT_BAD_SYNTAX":
        "Invalid extraction function syntax.\n"
        "  Format: hour / minute / second / ampm / is_pm / year / month / day\n"
        "          (data [, \"format\"])\n"
        "  Example: hour(\"14:30:15\")\n"
        "  Example: hour(m[:, \"Time\"], \"HH:MM:SS\")",

    "DATE_ADD_BAD_SYNTAX":
        "Invalid arithmetic function syntax.\n"
        "  Format: addhours / addminutes / addseconds / adddays / addmonths / addyears\n"
        "          (data, N [, \"format\"])\n"
        "  Example: addhours(\"14:30:15\", 2)\n"
        "  Example: adddays(m[:, \"Date\"], 10)",

    "VALID_TIME_BAD_SYNTAX":
        "Invalid is_valid_time() syntax.\n"
        "  Format: is_valid_time(data [, \"format\"])\n"
        "  Example: is_valid_time(\"14:30:15\")\n"
        "  Example: is_valid_time(m[:, \"Time\"], \"HH:MM:SS\")",
}