# errors/functions_db/files_txt_parquet.py
"""
База ошибок для TXT и Parquet.

    TXT:
        OpenTXT, SaveTXT, OpenTXTShow, SaveTXTShow

    Parquet:
        OpenParquet, SaveParquet

ВАЖНО:
    Этот файл — только данные. Никаких классов, импортов, функций.
    Регистр кодов ошибок — UPPER_SNAKE_CASE.
"""


RU = {
    # ============================================================
    # TXT — OpenTXT
    # ============================================================
    'OpenTXT': {
        'name': 'OpenTXT',
        'category': 'txt',
        'signature': 'OpenTXT("file.txt" [, "разделитель"])',
        'description': (
            'Загрузка из TXT.\n'
            '  • Без разделителя — автоопределение (, ; \\t |).\n'
            '  • С разделителем — по указанному.\n'
            '  • Для табуляции: "\\t".\n'
            '  • Кодировки: utf-8-sig, utf-8, cp1251, latin-1.'
        ),
        'examples': [
            'm = OpenTXT("data.txt")',
            'm = OpenTXT("data.txt", ";")',
            'm = OpenTXT("data.txt", "\\t")',
        ],
        'errors': {
            'OPENTXT_BAD_SYNTAX': {
                'message': (
                    "OpenTXT: неверный синтаксис.\n"
                    "  Нужен путь к файлу и, опционально, разделитель."
                ),
                'wrong': 'OpenTXT()',
                'right': 'OpenTXT("data.txt")',
                'explanation': (
                    "OpenTXT принимает 1 или 2 аргумента:\n"
                    "     OpenTXT(\"file.txt\")\n"
                    "     OpenTXT(\"file.txt\", \";\")\n"
                    "     OpenTXT(\"file.txt\", \"\\\\t\")   # табуляция"
                ),
                'variants': [
                    'OpenTXT("data.txt")',
                    'OpenTXT("data.txt", ";")',
                    'OpenTXT("data.txt", "\\t")',
                ],
            },
            'OPENTXT_PATH_NOT_STRING': {
                'message': (
                    "OpenTXT: путь к файлу должен быть строкой в кавычках."
                ),
                'wrong': 'OpenTXT(data.txt)',
                'right': 'OpenTXT("data.txt")',
                'explanation': (
                    "Путь — СТРОКА В КАВЫЧКАХ:\n"
                    "     OpenTXT(\"data.txt\")\n"
                    "     OpenTXT(\"C:\\\\data\\\\file.txt\")"
                ),
                'variants': [
                    'OpenTXT("data.txt")',
                    'OpenTXT("C:\\data\\file.txt")',
                ],
            },
            'TXT_FILE_NOT_FOUND': {
                'message': (
                    "OpenTXT: файл не найден.\n"
                    "  Проверьте путь и имя файла."
                ),
                'wrong': 'OpenTXT("no_such_file.txt")',
                'right': 'OpenTXT("data.txt")',
                'explanation': (
                    "Файл должен существовать на диске.\n"
                    "\n"
                    "Относительный путь ищется от рабочей папки\n"
                    "(где запущен ArrayVator)."
                ),
                'variants': [
                    'OpenTXT("data.txt")',
                    'OpenTXT("C:\\data\\file.txt")',
                ],
            },
            'TXT_BAD_DELIMITER': {
                'message': (
                    "OpenTXT: неверный разделитель.\n"
                    "  Разделитель — один символ."
                ),
                'wrong': 'OpenTXT("data.txt", ";;")',
                'right': 'OpenTXT("data.txt", ";")',
                'explanation': (
                    "Разделитель — ОДИН СИМВОЛ в кавычках:\n"
                    "     OpenTXT(\"file.txt\", \",\")\n"
                    "     OpenTXT(\"file.txt\", \";\")\n"
                    "     OpenTXT(\"file.txt\", \"|\")\n"
                    "     OpenTXT(\"file.txt\", \" \")    # пробел\n"
                    "     OpenTXT(\"file.txt\", \"\\\\t\")   # табуляция"
                ),
                'variants': [
                    'OpenTXT("data.txt", ";")',
                    'OpenTXT("data.txt", ",")',
                    'OpenTXT("data.txt", "\\t")',
                ],
            },
            'TXT_LOAD_ERROR': {
                'message': (
                    "OpenTXT: ошибка чтения файла.\n"
                    "  Файл повреждён или кодировка не поддерживается."
                ),
                'wrong': 'OpenTXT("broken.txt")',
                'right': 'OpenTXT("valid.txt")',
                'explanation': (
                    "Возможные причины:\n"
                    "  • файл повреждён\n"
                    "  • кодировка не utf-8/cp1251/latin-1\n"
                    "  • неверный разделитель в первой строке"
                ),
                'variants': [
                    'OpenTXT("data.txt")',
                ],
            },
            'TXT_ENCODING_ERROR': {
                'message': (
                    "OpenTXT: не удалось определить кодировку файла."
                ),
                'wrong': 'OpenTXT("unknown_encoding.txt")',
                'right': 'OpenTXT("utf8_file.txt")',
                'explanation': (
                    "OpenTXT пробует кодировки по порядку:\n"
                    "     utf-8-sig, utf-8, cp1251, latin-1\n"
                    "\n"
                    "Если ни одна не подошла — пересохраните файл в UTF-8."
                ),
                'variants': [
                    'OpenTXT("data.txt")',
                ],
            },
        },
    },

    # ============================================================
    # TXT — SaveTXT
    # ============================================================
    'SaveTXT': {
        'name': 'SaveTXT',
        'category': 'txt',
        'signature': 'SaveTXT(данные, "file.txt" [, "разделитель"])',
        'description': (
            'Сохранение в TXT.\n'
            '  • По умолчанию разделитель — ";".\n'
            '  • Кодировка utf-8-sig (с BOM для Excel).'
        ),
        'examples': [
            'SaveTXT(m, "out.txt")',
            'SaveTXT(m, "out.txt", "\\t")',
        ],
        'errors': {
            'SAVETXT_BAD_SYNTAX': {
                'message': (
                    "SaveTXT: неверный синтаксис.\n"
                    "  Нужны данные и путь к файлу."
                ),
                'wrong': 'SaveTXT(m)',
                'right': 'SaveTXT(m, "out.txt")',
                'explanation': (
                    "SaveTXT принимает 2 или 3 аргумента:\n"
                    "     SaveTXT(данные, \"file.txt\")\n"
                    "     SaveTXT(данные, \"file.txt\", \"разделитель\")\n"
                    "\n"
                    "Примеры:\n"
                    "     SaveTXT(m, \"out.txt\")             # по умолчанию ;\n"
                    "     SaveTXT(m, \"out.txt\", \"\\\\t\")     # табуляция"
                ),
                'variants': [
                    'SaveTXT(m, "out.txt")',
                    'SaveTXT(m, "out.txt", ";")',
                    'SaveTXT(m, "out.txt", "\\t")',
                ],
            },
            'TXT_SAVE_ERROR': {
                'message': (
                    "SaveTXT: не удалось сохранить файл.\n"
                    "  Проверьте путь и права на запись."
                ),
                'wrong': 'SaveTXT(m, "C:\\no_folder\\out.txt")',
                'right': 'SaveTXT(m, "out.txt")',
                'explanation': (
                    "Возможные причины:\n"
                    "  • папка не существует\n"
                    "  • нет прав на запись\n"
                    "  • файл занят другим приложением"
                ),
                'variants': [
                    'SaveTXT(m, "out.txt")',
                ],
            },
            'TXT_BAD_DELIMITER': {
                'message': (
                    "SaveTXT: неверный разделитель.\n"
                    "  Разделитель — один символ."
                ),
                'wrong': 'SaveTXT(m, "out.txt", ";;;")',
                'right': 'SaveTXT(m, "out.txt", ";")',
                'explanation': (
                    "Разделитель — ОДИН СИМВОЛ:\n"
                    "     SaveTXT(m, \"out.txt\", \";\")\n"
                    "     SaveTXT(m, \"out.txt\", \",\")\n"
                    "     SaveTXT(m, \"out.txt\", \"\\\\t\")"
                ),
                'variants': [
                    'SaveTXT(m, "out.txt", ";")',
                    'SaveTXT(m, "out.txt", "\\t")',
                ],
            },
        },
    },

    # ============================================================
    # TXT — OpenTXTShow
    # ============================================================
    'OpenTXTShow': {
        'name': 'OpenTXTShow',
        'category': 'txt',
        'signature': 'OpenTXTShow([разделитель])',
        'description': (
            'Диалог выбора TXT-файла.\n'
            '  • Опционально — разделитель для парсинга.'
        ),
        'examples': [
            'm = OpenTXTShow()',
            'm = OpenTXTShow(";")',
        ],
        'errors': {
            'OPENTXTSHOW_BAD_SYNTAX': {
                'message': (
                    "OpenTXTShow: неверный синтаксис.\n"
                    "  Либо без аргументов, либо один разделитель."
                ),
                'wrong': 'OpenTXTShow("file.txt", ";")',
                'right': 'OpenTXTShow()',
                'explanation': (
                    "OpenTXTShow сам открывает диалог выбора файла.\n"
                    "Путь передавать НЕ нужно.\n"
                    "\n"
                    "Правильно:\n"
                    "     OpenTXTShow()        # автоопределение\n"
                    "     OpenTXTShow(\";\")      # разделитель ;"
                ),
                'variants': [
                    'OpenTXTShow()',
                    'OpenTXTShow(";")',
                    'OpenTXTShow("\\t")',
                ],
            },
            'TXT_BAD_DELIMITER': {
                'message': (
                    "OpenTXTShow: неверный разделитель.\n"
                    "  Разделитель — один символ."
                ),
                'wrong': 'OpenTXTShow(";;")',
                'right': 'OpenTXTShow(";")',
                'explanation': (
                    "Разделитель — ОДИН СИМВОЛ в кавычках:\n"
                    "     OpenTXTShow()\n"
                    "     OpenTXTShow(\";\")\n"
                    "     OpenTXTShow(\"\\\\t\")"
                ),
                'variants': [
                    'OpenTXTShow()',
                    'OpenTXTShow(";")',
                ],
            },
        },
    },

    # ============================================================
    # TXT — SaveTXTShow
    # ============================================================
    'SaveTXTShow': {
        'name': 'SaveTXTShow',
        'category': 'txt',
        'signature': 'SaveTXTShow(данные [, разделитель])',
        'description': 'Диалог сохранения в TXT.',
        'examples': [
            'SaveTXTShow(m)',
            'SaveTXTShow(m, ";")',
        ],
        'errors': {
            'SAVETXTSHOW_BAD_SYNTAX': {
                'message': (
                    "SaveTXTShow: неверный синтаксис.\n"
                    "  Нужны данные и, опционально, разделитель."
                ),
                'wrong': 'SaveTXTShow()',
                'right': 'SaveTXTShow(m)',
                'explanation': (
                    "SaveTXTShow принимает 1 или 2 аргумента:\n"
                    "     SaveTXTShow(данные)\n"
                    "     SaveTXTShow(данные, \";\")"
                ),
                'variants': [
                    'SaveTXTShow(m)',
                    'SaveTXTShow(m, ";")',
                ],
            },
            'TXT_SAVE_ERROR': {
                'message': (
                    "SaveTXTShow: не удалось сохранить файл.\n"
                    "  Проверьте путь и права на запись."
                ),
                'wrong': 'SaveTXTShow(m)   # папка недоступна',
                'right': 'SaveTXTShow(m)   # папка доступна',
                'explanation': (
                    "Возможные причины:\n"
                    "  • папка не существует\n"
                    "  • нет прав на запись\n"
                    "  • файл занят другим приложением"
                ),
                'variants': [
                    'SaveTXTShow(m)',
                ],
            },
        },
    },

    # ============================================================
    # PARQUET — OpenParquet
    # ============================================================
    'OpenParquet': {
        'name': 'OpenParquet',
        'category': 'parquet',
        'signature': 'OpenParquet("file.parquet")',
        'description': (
            'Загрузка из Parquet.\n'
            '  • Через DuckDB (потоково).\n'
            '  • Parquet в 10–20 раз быстрее CSV и в 5–10 раз меньше по размеру.\n'
            '  • Возвращает DuckDBTable.'
        ),
        'examples': [
            'm = OpenParquet("data.parquet")',
        ],
        'errors': {
            'OPENPARQUET_BAD_SYNTAX': {
                'message': (
                    "OpenParquet: неверный синтаксис.\n"
                    "  Нужен путь к файлу."
                ),
                'wrong': 'OpenParquet()',
                'right': 'OpenParquet("data.parquet")',
                'explanation': (
                    "OpenParquet принимает ОДИН аргумент:\n"
                    "     OpenParquet(\"file.parquet\")"
                ),
                'variants': [
                    'OpenParquet("data.parquet")',
                ],
            },
            'OPENPARQUET_PATH_NOT_STRING': {
                'message': (
                    "OpenParquet: путь к файлу должен быть строкой в кавычках."
                ),
                'wrong': 'OpenParquet(data.parquet)',
                'right': 'OpenParquet("data.parquet")',
                'explanation': (
                    "Путь — СТРОКА В КАВЫЧКАХ:\n"
                    "     OpenParquet(\"data.parquet\")\n"
                    "     OpenParquet(\"C:\\\\data\\\\file.parquet\")"
                ),
                'variants': [
                    'OpenParquet("data.parquet")',
                    'OpenParquet("C:\\data\\file.parquet")',
                ],
            },
            'PARQUET_FILE_NOT_FOUND': {
                'message': (
                    "OpenParquet: файл не найден.\n"
                    "  Проверьте путь и имя файла."
                ),
                'wrong': 'OpenParquet("no_such_file.parquet")',
                'right': 'OpenParquet("data.parquet")',
                'explanation': (
                    "Файл должен существовать на диске.\n"
                    "\n"
                    "Относительный путь ищется от рабочей папки."
                ),
                'variants': [
                    'OpenParquet("data.parquet")',
                ],
            },
            'PARQUET_LOAD_ERROR': {
                'message': (
                    "OpenParquet: ошибка чтения файла.\n"
                    "  Файл повреждён или не является Parquet."
                ),
                'wrong': 'OpenParquet("broken.parquet")',
                'right': 'OpenParquet("valid.parquet")',
                'explanation': (
                    "Проверьте:\n"
                    "  • файл действительно в формате Parquet\n"
                    "  • файл не повреждён\n"
                    "  • нет лишних расширений (например, .parquet.txt)"
                ),
                'variants': [
                    'OpenParquet("data.parquet")',
                ],
            },
            'PARQUET_DUCKDB_MISSING': {
                'message': (
                    "OpenParquet: DuckDB не установлен.\n"
                    "  Установите: pip install duckdb"
                ),
                'wrong': 'OpenParquet("data.parquet")',
                'right': (
                    'pip install duckdb\n'
                    'OpenParquet("data.parquet")'
                ),
                'explanation': (
                    "OpenParquet читает Parquet через DuckDB.\n"
                    "\n"
                    "Установка:\n"
                    "     pip install duckdb"
                ),
                'variants': [
                    'pip install duckdb\nOpenParquet("data.parquet")',
                ],
            },
        },
    },

    # ============================================================
    # PARQUET — SaveParquet
    # ============================================================
    'SaveParquet': {
        'name': 'SaveParquet',
        'category': 'parquet',
        'signature': 'SaveParquet(данные, "file.parquet")',
        'description': (
            'Сохранение в Parquet.\n'
            '  • Через DuckDB.\n'
            '  • Работает с Matrix и DuckDBTable.'
        ),
        'examples': [
            'SaveParquet(m, "out.parquet")',
        ],
        'errors': {
            'SAVEPARQUET_BAD_SYNTAX': {
                'message': (
                    "SaveParquet: неверный синтаксис.\n"
                    "  Нужны данные и путь к файлу."
                ),
                'wrong': 'SaveParquet(m)',
                'right': 'SaveParquet(m, "out.parquet")',
                'explanation': (
                    "SaveParquet принимает ДВА аргумента:\n"
                    "     SaveParquet(данные, \"file.parquet\")"
                ),
                'variants': [
                    'SaveParquet(m, "out.parquet")',
                ],
            },
            'PARQUET_SAVE_ERROR': {
                'message': (
                    "SaveParquet: не удалось сохранить файл.\n"
                    "  Проверьте путь и права на запись."
                ),
                'wrong': 'SaveParquet(m, "C:\\no_folder\\out.parquet")',
                'right': 'SaveParquet(m, "out.parquet")',
                'explanation': (
                    "Возможные причины:\n"
                    "  • папка не существует\n"
                    "  • нет прав на запись\n"
                    "  • файл занят другим приложением"
                ),
                'variants': [
                    'SaveParquet(m, "out.parquet")',
                ],
            },
            'PARQUET_DUCKDB_MISSING': {
                'message': (
                    "SaveParquet: DuckDB не установлен.\n"
                    "  Установите: pip install duckdb"
                ),
                'wrong': 'SaveParquet(m, "out.parquet")',
                'right': (
                    'pip install duckdb\n'
                    'SaveParquet(m, "out.parquet")'
                ),
                'explanation': (
                    "SaveParquet пишет Parquet через DuckDB.\n"
                    "\n"
                    "Установка:\n"
                    "     pip install duckdb"
                ),
                'variants': [
                    'pip install duckdb\nSaveParquet(m, "out.parquet")',
                ],
            },
        },
    },
}


EN = {
    # ============================================================
    # TXT — OpenTXT
    # ============================================================
    'OpenTXT': {
        'name': 'OpenTXT',
        'category': 'txt',
        'signature': 'OpenTXT("file.txt" [, "delimiter"])',
        'description': (
            'Load from TXT.\n'
            '  • No delimiter — auto-detect (, ; \\t |).\n'
            '  • With delimiter — as specified.\n'
            '  • For tab: "\\t".\n'
            '  • Encodings: utf-8-sig, utf-8, cp1251, latin-1.'
        ),
        'examples': [
            'm = OpenTXT("data.txt")',
            'm = OpenTXT("data.txt", ";")',
            'm = OpenTXT("data.txt", "\\t")',
        ],
        'errors': {
            'OPENTXT_BAD_SYNTAX': {
                'message': (
                    "OpenTXT: invalid syntax.\n"
                    "  Need a file path and optionally a delimiter."
                ),
                'wrong': 'OpenTXT()',
                'right': 'OpenTXT("data.txt")',
                'explanation': (
                    "OpenTXT takes 1 or 2 arguments:\n"
                    "     OpenTXT(\"file.txt\")\n"
                    "     OpenTXT(\"file.txt\", \";\")\n"
                    "     OpenTXT(\"file.txt\", \"\\\\t\")   # tab"
                ),
                'variants': [
                    'OpenTXT("data.txt")',
                    'OpenTXT("data.txt", ";")',
                    'OpenTXT("data.txt", "\\t")',
                ],
            },
            'OPENTXT_PATH_NOT_STRING': {
                'message': (
                    "OpenTXT: file path must be a quoted string."
                ),
                'wrong': 'OpenTXT(data.txt)',
                'right': 'OpenTXT("data.txt")',
                'explanation': (
                    "Path is a STRING IN QUOTES:\n"
                    "     OpenTXT(\"data.txt\")\n"
                    "     OpenTXT(\"C:\\\\data\\\\file.txt\")"
                ),
                'variants': [
                    'OpenTXT("data.txt")',
                    'OpenTXT("C:\\data\\file.txt")',
                ],
            },
            'TXT_FILE_NOT_FOUND': {
                'message': (
                    "OpenTXT: file not found.\n"
                    "  Check the path and file name."
                ),
                'wrong': 'OpenTXT("no_such_file.txt")',
                'right': 'OpenTXT("data.txt")',
                'explanation': (
                    "The file must exist on disk.\n"
                    "\n"
                    "Relative path is resolved from the working folder\n"
                    "(where ArrayVator is running)."
                ),
                'variants': [
                    'OpenTXT("data.txt")',
                    'OpenTXT("C:\\data\\file.txt")',
                ],
            },
            'TXT_BAD_DELIMITER': {
                'message': (
                    "OpenTXT: invalid delimiter.\n"
                    "  Delimiter must be a single character."
                ),
                'wrong': 'OpenTXT("data.txt", ";;")',
                'right': 'OpenTXT("data.txt", ";")',
                'explanation': (
                    "Delimiter is ONE character in quotes:\n"
                    "     OpenTXT(\"file.txt\", \",\")\n"
                    "     OpenTXT(\"file.txt\", \";\")\n"
                    "     OpenTXT(\"file.txt\", \"|\")\n"
                    "     OpenTXT(\"file.txt\", \"\\\\t\")   # tab"
                ),
                'variants': [
                    'OpenTXT("data.txt", ";")',
                    'OpenTXT("data.txt", ",")',
                    'OpenTXT("data.txt", "\\t")',
                ],
            },
            'TXT_LOAD_ERROR': {
                'message': (
                    "OpenTXT: failed to read the file.\n"
                    "  File is corrupted or encoding is unsupported."
                ),
                'wrong': 'OpenTXT("broken.txt")',
                'right': 'OpenTXT("valid.txt")',
                'explanation': (
                    "Possible reasons:\n"
                    "  • file is corrupted\n"
                    "  • encoding is not utf-8/cp1251/latin-1\n"
                    "  • wrong delimiter in the first line"
                ),
                'variants': [
                    'OpenTXT("data.txt")',
                ],
            },
            'TXT_ENCODING_ERROR': {
                'message': (
                    "OpenTXT: failed to detect file encoding."
                ),
                'wrong': 'OpenTXT("unknown_encoding.txt")',
                'right': 'OpenTXT("utf8_file.txt")',
                'explanation': (
                    "OpenTXT tries encodings in order:\n"
                    "     utf-8-sig, utf-8, cp1251, latin-1\n"
                    "\n"
                    "If none works — re-save the file as UTF-8."
                ),
                'variants': [
                    'OpenTXT("data.txt")',
                ],
            },
        },
    },

    # ============================================================
    # TXT — SaveTXT
    # ============================================================
    'SaveTXT': {
        'name': 'SaveTXT',
        'category': 'txt',
        'signature': 'SaveTXT(data, "file.txt" [, "delimiter"])',
        'description': (
            'Save to TXT.\n'
            '  • Default delimiter — ";".\n'
            '  • Encoding: utf-8-sig (with BOM for Excel).'
        ),
        'examples': [
            'SaveTXT(m, "out.txt")',
            'SaveTXT(m, "out.txt", "\\t")',
        ],
        'errors': {
            'SAVETXT_BAD_SYNTAX': {
                'message': (
                    "SaveTXT: invalid syntax.\n"
                    "  Need data and a file path."
                ),
                'wrong': 'SaveTXT(m)',
                'right': 'SaveTXT(m, "out.txt")',
                'explanation': (
                    "SaveTXT takes 2 or 3 arguments:\n"
                    "     SaveTXT(data, \"file.txt\")\n"
                    "     SaveTXT(data, \"file.txt\", \"delimiter\")"
                ),
                'variants': [
                    'SaveTXT(m, "out.txt")',
                    'SaveTXT(m, "out.txt", "\\t")',
                ],
            },
            'TXT_SAVE_ERROR': {
                'message': (
                    "SaveTXT: failed to save the file.\n"
                    "  Check the path and write permissions."
                ),
                'wrong': 'SaveTXT(m, "C:\\no_folder\\out.txt")',
                'right': 'SaveTXT(m, "out.txt")',
                'explanation': (
                    "Possible reasons:\n"
                    "  • folder does not exist\n"
                    "  • no write permission\n"
                    "  • file is locked"
                ),
                'variants': [
                    'SaveTXT(m, "out.txt")',
                ],
            },
            'TXT_BAD_DELIMITER': {
                'message': (
                    "SaveTXT: invalid delimiter.\n"
                    "  Delimiter must be a single character."
                ),
                'wrong': 'SaveTXT(m, "out.txt", ";;;")',
                'right': 'SaveTXT(m, "out.txt", ";")',
                'explanation': (
                    "Delimiter is ONE character:\n"
                    "     SaveTXT(m, \"out.txt\", \";\")\n"
                    "     SaveTXT(m, \"out.txt\", \",\")\n"
                    "     SaveTXT(m, \"out.txt\", \"\\\\t\")"
                ),
                'variants': [
                    'SaveTXT(m, "out.txt", ";")',
                    'SaveTXT(m, "out.txt", "\\t")',
                ],
            },
        },
    },

    # ============================================================
    # TXT — OpenTXTShow
    # ============================================================
    'OpenTXTShow': {
        'name': 'OpenTXTShow',
        'category': 'txt',
        'signature': 'OpenTXTShow([delimiter])',
        'description': (
            'Dialog for selecting a TXT file.\n'
            '  • Optionally — delimiter for parsing.'
        ),
        'examples': [
            'm = OpenTXTShow()',
            'm = OpenTXTShow(";")',
        ],
        'errors': {
            'OPENTXTSHOW_BAD_SYNTAX': {
                'message': (
                    "OpenTXTShow: invalid syntax.\n"
                    "  Either no arguments or one delimiter."
                ),
                'wrong': 'OpenTXTShow("file.txt", ";")',
                'right': 'OpenTXTShow()',
                'explanation': (
                    "OpenTXTShow itself opens the file dialog.\n"
                    "No path is needed.\n"
                    "\n"
                    "Correct:\n"
                    "     OpenTXTShow()        # auto-detect\n"
                    "     OpenTXTShow(\";\")      # delimiter ;"
                ),
                'variants': [
                    'OpenTXTShow()',
                    'OpenTXTShow(";")',
                ],
            },
            'TXT_BAD_DELIMITER': {
                'message': (
                    "OpenTXTShow: invalid delimiter.\n"
                    "  Delimiter must be a single character."
                ),
                'wrong': 'OpenTXTShow(";;")',
                'right': 'OpenTXTShow(";")',
                'explanation': (
                    "Delimiter is ONE character in quotes."
                ),
                'variants': [
                    'OpenTXTShow()',
                    'OpenTXTShow(";")',
                ],
            },
        },
    },

    # ============================================================
    # TXT — SaveTXTShow
    # ============================================================
    'SaveTXTShow': {
        'name': 'SaveTXTShow',
        'category': 'txt',
        'signature': 'SaveTXTShow(data [, delimiter])',
        'description': 'Dialog for saving to TXT.',
        'examples': [
            'SaveTXTShow(m)',
            'SaveTXTShow(m, ";")',
        ],
        'errors': {
            'SAVETXTSHOW_BAD_SYNTAX': {
                'message': (
                    "SaveTXTShow: invalid syntax.\n"
                    "  Need data and optionally a delimiter."
                ),
                'wrong': 'SaveTXTShow()',
                'right': 'SaveTXTShow(m)',
                'explanation': (
                    "SaveTXTShow takes 1 or 2 arguments:\n"
                    "     SaveTXTShow(data)\n"
                    "     SaveTXTShow(data, \";\")"
                ),
                'variants': [
                    'SaveTXTShow(m)',
                    'SaveTXTShow(m, ";")',
                ],
            },
            'TXT_SAVE_ERROR': {
                'message': (
                    "SaveTXTShow: failed to save the file.\n"
                    "  Check the path and write permissions."
                ),
                'wrong': 'SaveTXTShow(m)   # folder is locked',
                'right': 'SaveTXTShow(m)   # folder is writable',
                'explanation': (
                    "Possible reasons:\n"
                    "  • folder does not exist\n"
                    "  • no write permission\n"
                    "  • file is locked"
                ),
                'variants': [
                    'SaveTXTShow(m)',
                ],
            },
        },
    },

    # ============================================================
    # PARQUET — OpenParquet
    # ============================================================
    'OpenParquet': {
        'name': 'OpenParquet',
        'category': 'parquet',
        'signature': 'OpenParquet("file.parquet")',
        'description': (
            'Load from Parquet.\n'
            '  • Through DuckDB (streamed).\n'
            '  • Parquet is 10–20x faster than CSV and 5–10x smaller.\n'
            '  • Returns a DuckDBTable.'
        ),
        'examples': [
            'm = OpenParquet("data.parquet")',
        ],
        'errors': {
            'OPENPARQUET_BAD_SYNTAX': {
                'message': (
                    "OpenParquet: invalid syntax.\n"
                    "  Need a file path."
                ),
                'wrong': 'OpenParquet()',
                'right': 'OpenParquet("data.parquet")',
                'explanation': (
                    "OpenParquet takes ONE argument:\n"
                    "     OpenParquet(\"file.parquet\")"
                ),
                'variants': [
                    'OpenParquet("data.parquet")',
                ],
            },
            'OPENPARQUET_PATH_NOT_STRING': {
                'message': (
                    "OpenParquet: file path must be a quoted string."
                ),
                'wrong': 'OpenParquet(data.parquet)',
                'right': 'OpenParquet("data.parquet")',
                'explanation': (
                    "Path is a STRING IN QUOTES."
                ),
                'variants': [
                    'OpenParquet("data.parquet")',
                    'OpenParquet("C:\\data\\file.parquet")',
                ],
            },
            'PARQUET_FILE_NOT_FOUND': {
                'message': (
                    "OpenParquet: file not found.\n"
                    "  Check the path and file name."
                ),
                'wrong': 'OpenParquet("no_such_file.parquet")',
                'right': 'OpenParquet("data.parquet")',
                'explanation': (
                    "The file must exist on disk."
                ),
                'variants': [
                    'OpenParquet("data.parquet")',
                ],
            },
            'PARQUET_LOAD_ERROR': {
                'message': (
                    "OpenParquet: failed to read the file.\n"
                    "  File is corrupted or not Parquet."
                ),
                'wrong': 'OpenParquet("broken.parquet")',
                'right': 'OpenParquet("valid.parquet")',
                'explanation': (
                    "Check:\n"
                    "  • file is really in Parquet format\n"
                    "  • file is not corrupted\n"
                    "  • no extra extensions"
                ),
                'variants': [
                    'OpenParquet("data.parquet")',
                ],
            },
            'PARQUET_DUCKDB_MISSING': {
                'message': (
                    "OpenParquet: DuckDB is not installed.\n"
                    "  Install: pip install duckdb"
                ),
                'wrong': 'OpenParquet("data.parquet")',
                'right': (
                    'pip install duckdb\n'
                    'OpenParquet("data.parquet")'
                ),
                'explanation': (
                    "OpenParquet reads Parquet via DuckDB.\n"
                    "\n"
                    "Install:\n"
                    "     pip install duckdb"
                ),
                'variants': [
                    'pip install duckdb\nOpenParquet("data.parquet")',
                ],
            },
        },
    },

    # ============================================================
    # PARQUET — SaveParquet
    # ============================================================
    'SaveParquet': {
        'name': 'SaveParquet',
        'category': 'parquet',
        'signature': 'SaveParquet(data, "file.parquet")',
        'description': (
            'Save to Parquet.\n'
            '  • Through DuckDB.\n'
            '  • Works with Matrix and DuckDBTable.'
        ),
        'examples': [
            'SaveParquet(m, "out.parquet")',
        ],
        'errors': {
            'SAVEPARQUET_BAD_SYNTAX': {
                'message': (
                    "SaveParquet: invalid syntax.\n"
                    "  Need data and a file path."
                ),
                'wrong': 'SaveParquet(m)',
                'right': 'SaveParquet(m, "out.parquet")',
                'explanation': (
                    "SaveParquet takes TWO arguments:\n"
                    "     SaveParquet(data, \"file.parquet\")"
                ),
                'variants': [
                    'SaveParquet(m, "out.parquet")',
                ],
            },
            'PARQUET_SAVE_ERROR': {
                'message': (
                    "SaveParquet: failed to save the file.\n"
                    "  Check the path and write permissions."
                ),
                'wrong': 'SaveParquet(m, "C:\\no_folder\\out.parquet")',
                'right': 'SaveParquet(m, "out.parquet")',
                'explanation': (
                    "Possible reasons:\n"
                    "  • folder does not exist\n"
                    "  • no write permission\n"
                    "  • file is locked"
                ),
                'variants': [
                    'SaveParquet(m, "out.parquet")',
                ],
            },
            'PARQUET_DUCKDB_MISSING': {
                'message': (
                    "SaveParquet: DuckDB is not installed.\n"
                    "  Install: pip install duckdb"
                ),
                'wrong': 'SaveParquet(m, "out.parquet")',
                'right': (
                    'pip install duckdb\n'
                    'SaveParquet(m, "out.parquet")'
                ),
                'explanation': (
                    "SaveParquet writes Parquet via DuckDB.\n"
                    "\n"
                    "Install:\n"
                    "     pip install duckdb"
                ),
                'variants': [
                    'pip install duckdb\nSaveParquet(m, "out.parquet")',
                ],
            },
        },
    },
}