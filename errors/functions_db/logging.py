# errors/functions_db/logging.py
"""
База ошибок для функций логирования:
    LogToFile, LogOff.

СИНТАКСИС:
    LogToFile("file.txt")                — уровень "all"
    LogToFile("file.txt", "matrix")      — без содержимого матриц
    LogToFile("file.txt", "summary")     — только итоги
    LogOff()                             — выключить

ПРАВИЛА:
    - Уровни: "all", "matrix", "summary".
    - Логирование выключается автоматически при закрытии программы.
"""


RU = {
    # ============================================================
    # LOG TO FILE
    # ============================================================
    'LogToFile': {
        'name': 'LogToFile',
        'category': 'logging',
        'signature': 'LogToFile("file.txt" [, "all"|"matrix"|"summary"])',
        'description': (
            'Включает логирование в файл.\n'
            '  • "file.txt" — путь к файлу лога.\n'
            '  • Уровни:\n'
            '      "all"     — всё (по умолчанию)\n'
            '      "matrix"  — без содержимого матриц\n'
            '      "summary" — только итоги операций\n'
            '  • Логирование выключается при выходе.'
        ),
        'examples': [
            'LogToFile("log.txt")',
            'LogToFile("log.txt", "matrix")',
            'LogToFile("log.txt", "summary")',
        ],
        'errors': {
            'LOGTOFILE_BAD_SYNTAX': {
                'message': (
                    "LogToFile: неверный синтаксис.\n"
                    "  Нужен путь и, опционально, уровень."
                ),
                'wrong': 'LogToFile()',
                'right': 'LogToFile("log.txt")',
                'explanation': (
                    "LogToFile принимает 1 или 2 аргумента:\n"
                    "  1. \"file.txt\" — путь к файлу\n"
                    "  2. \"all\" | \"matrix\" | \"summary\" — уровень (опц.)\n"
                    "\n"
                    "Неправильно:\n"
                    "     LogToFile()\n"
                    "     LogToFile(\"log.txt\", \"all\", \"extra\")\n"
                    "\n"
                    "Правильно:\n"
                    "     LogToFile(\"log.txt\")\n"
                    "     LogToFile(\"log.txt\", \"matrix\")"
                ),
                'variants': [
                    'LogToFile("log.txt")',
                    'LogToFile("log.txt", "matrix")',
                    'LogToFile("log.txt", "summary")',
                ],
            },
            'LOGTOFILE_BAD_LEVEL': {
                'message': (
                    "LogToFile: неверный уровень логирования.\n"
                    "  Допустимо: \"all\", \"matrix\", \"summary\"."
                ),
                'wrong': 'LogToFile("log.txt", "full")',
                'right': 'LogToFile("log.txt", "all")',
                'explanation': (
                    "Только три уровня:\n"
                    "     \"all\"     — всё (по умолчанию)\n"
                    "     \"matrix\"  — без содержимого матриц\n"
                    "     \"summary\" — только итоги операций\n"
                    "\n"
                    "Неправильно:\n"
                    "     LogToFile(\"log.txt\", \"full\")\n"
                    "     LogToFile(\"log.txt\", \"debug\")\n"
                    "\n"
                    "Правильно:\n"
                    "     LogToFile(\"log.txt\", \"all\")\n"
                    "     LogToFile(\"log.txt\", \"matrix\")\n"
                    "     LogToFile(\"log.txt\", \"summary\")"
                ),
                'variants': [
                    'LogToFile("log.txt", "all")',
                    'LogToFile("log.txt", "matrix")',
                    'LogToFile("log.txt", "summary")',
                ],
            },
            'LOGTOFILE_CANT_OPEN': {
                'message': (
                    "LogToFile: не удалось открыть файл лога.\n"
                    "  Проверьте путь и права на запись."
                ),
                'wrong': 'LogToFile("C:\\\\no_folder\\\\log.txt")',
                'right': 'LogToFile("log.txt")',
                'explanation': (
                    "Возможные причины:\n"
                    "  • папка не существует\n"
                    "  • нет прав на запись\n"
                    "  • файл занят другим приложением\n"
                    "\n"
                    "Правильно:\n"
                    "     LogToFile(\"log.txt\")"
                ),
                'variants': [
                    'LogToFile("log.txt")',
                    'LogToFile("C:\\data\\log.txt")',
                ],
            },
        },
    },

    # ============================================================
    # LOG OFF
    # ============================================================
    'LogOff': {
        'name': 'LogOff',
        'category': 'logging',
        'signature': 'LogOff()',
        'description': (
            'Отключает логирование.\n'
            '  • Аргументов НЕТ.\n'
            '  • Файл закрывается.'
        ),
        'examples': [
            'LogOff()',
        ],
        'errors': {
            'LOGOFF_BAD_SYNTAX': {
                'message': (
                    "LogOff: аргументы не нужны."
                ),
                'wrong': 'LogOff("log.txt")',
                'right': 'LogOff()',
                'explanation': (
                    "LogOff не принимает аргументов — просто выключает логирование.\n"
                    "\n"
                    "Неправильно:\n"
                    "     LogOff(\"log.txt\")\n"
                    "\n"
                    "Правильно:\n"
                    "     LogOff()"
                ),
                'variants': [
                    'LogOff()',
                ],
            },
        },
    },
}


EN = {
    # ============================================================
    # LOG TO FILE
    # ============================================================
    'LogToFile': {
        'name': 'LogToFile',
        'category': 'logging',
        'signature': 'LogToFile("file.txt" [, "all"|"matrix"|"summary"])',
        'description': (
            'Enables logging to a file.\n'
            '  • "file.txt" — log file path.\n'
            '  • Levels:\n'
            '      "all"     — everything (default)\n'
            '      "matrix"  — without matrix contents\n'
            '      "summary" — only operation summaries\n'
            '  • Logging is disabled on exit.'
        ),
        'examples': [
            'LogToFile("log.txt")',
            'LogToFile("log.txt", "matrix")',
            'LogToFile("log.txt", "summary")',
        ],
        'errors': {
            'LOGTOFILE_BAD_SYNTAX': {
                'message': (
                    "LogToFile: invalid syntax.\n"
                    "  Need a path and optionally a level."
                ),
                'wrong': 'LogToFile()',
                'right': 'LogToFile("log.txt")',
                'explanation': (
                    "LogToFile takes 1 or 2 arguments:\n"
                    "  1. \"file.txt\" — file path\n"
                    "  2. \"all\" | \"matrix\" | \"summary\" — level (optional)\n"
                    "\n"
                    "Incorrect:\n"
                    "     LogToFile()\n"
                    "     LogToFile(\"log.txt\", \"all\", \"extra\")\n"
                    "\n"
                    "Correct:\n"
                    "     LogToFile(\"log.txt\")\n"
                    "     LogToFile(\"log.txt\", \"matrix\")"
                ),
                'variants': [
                    'LogToFile("log.txt")',
                    'LogToFile("log.txt", "matrix")',
                    'LogToFile("log.txt", "summary")',
                ],
            },
            'LOGTOFILE_BAD_LEVEL': {
                'message': (
                    "LogToFile: invalid logging level.\n"
                    "  Allowed: \"all\", \"matrix\", \"summary\"."
                ),
                'wrong': 'LogToFile("log.txt", "full")',
                'right': 'LogToFile("log.txt", "all")',
                'explanation': (
                    "Only three levels:\n"
                    "     \"all\"     — everything (default)\n"
                    "     \"matrix\"  — without matrix contents\n"
                    "     \"summary\" — only operation summaries\n"
                    "\n"
                    "Incorrect:\n"
                    "     LogToFile(\"log.txt\", \"full\")\n"
                    "     LogToFile(\"log.txt\", \"debug\")\n"
                    "\n"
                    "Correct:\n"
                    "     LogToFile(\"log.txt\", \"all\")\n"
                    "     LogToFile(\"log.txt\", \"matrix\")\n"
                    "     LogToFile(\"log.txt\", \"summary\")"
                ),
                'variants': [
                    'LogToFile("log.txt", "all")',
                    'LogToFile("log.txt", "matrix")',
                    'LogToFile("log.txt", "summary")',
                ],
            },
            'LOGTOFILE_CANT_OPEN': {
                'message': (
                    "LogToFile: failed to open log file.\n"
                    "  Check the path and write permissions."
                ),
                'wrong': 'LogToFile("C:\\\\no_folder\\\\log.txt")',
                'right': 'LogToFile("log.txt")',
                'explanation': (
                    "Possible reasons:\n"
                    "  • folder does not exist\n"
                    "  • no write permission\n"
                    "  • file is locked\n"
                    "\n"
                    "Correct:\n"
                    "     LogToFile(\"log.txt\")"
                ),
                'variants': [
                    'LogToFile("log.txt")',
                    'LogToFile("C:\\data\\log.txt")',
                ],
            },
        },
    },

    # ============================================================
    # LOG OFF
    # ============================================================
    'LogOff': {
        'name': 'LogOff',
        'category': 'logging',
        'signature': 'LogOff()',
        'description': (
            'Disables logging.\n'
            '  • NO arguments.\n'
            '  • The file is closed.'
        ),
        'examples': [
            'LogOff()',
        ],
        'errors': {
            'LOGOFF_BAD_SYNTAX': {
                'message': (
                    "LogOff: no arguments needed."
                ),
                'wrong': 'LogOff("log.txt")',
                'right': 'LogOff()',
                'explanation': (
                    "LogOff takes no arguments — it just disables logging.\n"
                    "\n"
                    "Incorrect:\n"
                    "     LogOff(\"log.txt\")\n"
                    "\n"
                    "Correct:\n"
                    "     LogOff()"
                ),
                'variants': [
                    'LogOff()',
                ],
            },
        },
    },
}