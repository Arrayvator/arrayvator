# errors/functions_db/files_excel_csv.py
"""
База ошибок для Excel и CSV.

    Excel:
        OpenExcel, SaveExcel, OpenExcelShow, SaveExcelShow

    CSV:
        OpenCSV, SaveCSV, OpenCSVShow, SaveCSVShow

ВАЖНО:
    Этот файл — только данные. Никаких классов, импортов, функций.
    Регистр кодов ошибок — UPPER_SNAKE_CASE.
"""


RU = {
    # ============================================================
    # EXCEL — OpenExcel
    # ============================================================
    'OpenExcel': {
        'name': 'OpenExcel',
        'category': 'excel',
        'signature': 'OpenExcel("file.xlsx" [, лист])',
        'description': (
            'Загрузка из Excel.\n'
            '  • Без листа — первый лист.\n'
            '  • "Лист1" — по имени.\n'
            '  • 1, 2, ... — по номеру (1-based).\n'
            '  • all — все листы подряд.\n'
            '  • Чтение — python-calamine (~10x быстрее openpyxl).'
        ),
        'examples': [
            'm = OpenExcel("data.xlsx")',
            'm = OpenExcel("data.xlsx", "Продажи")',
            'm = OpenExcel("data.xlsx", 1)',
            'm = OpenExcel("data.xlsx", all)',
        ],
        'errors': {
            'OPENEXCEL_BAD_SYNTAX': {
                'message': (
                    "OpenExcel: неверный синтаксис.\n"
                    "  Нужен путь к файлу и, опционально, лист."
                ),
                'wrong': 'OpenExcel()',
                'right': 'OpenExcel("data.xlsx")',
                'explanation': (
                    "OpenExcel принимает 1 или 2 аргумента:\n"
                    "     OpenExcel(\"file.xlsx\")\n"
                    "     OpenExcel(\"file.xlsx\", \"Лист1\")\n"
                    "     OpenExcel(\"file.xlsx\", 1)\n"
                    "     OpenExcel(\"file.xlsx\", all)"
                ),
                'variants': [
                    'OpenExcel("data.xlsx")',
                    'OpenExcel("data.xlsx", "Продажи")',
                    'OpenExcel("data.xlsx", 1)',
                    'OpenExcel("data.xlsx", all)',
                ],
            },
            'OPENEXCEL_PATH_NOT_STRING': {
                'message': (
                    "OpenExcel: путь к файлу должен быть строкой в кавычках."
                ),
                'wrong': 'OpenExcel(data.xlsx)',
                'right': 'OpenExcel("data.xlsx")',
                'explanation': (
                    "Путь — СТРОКА В КАВЫЧКАХ:\n"
                    "     OpenExcel(\"data.xlsx\")\n"
                    "     OpenExcel(\"C:\\\\reports\\\\data.xlsx\")\n"
                    "\n"
                    "Без кавычек парсер ищет переменную с таким именем."
                ),
                'variants': [
                    'OpenExcel("data.xlsx")',
                    'OpenExcel("C:\\reports\\data.xlsx")',
                ],
            },
            'EXCEL_FILE_NOT_FOUND': {
                'message': (
                    "OpenExcel: файл не найден.\n"
                    "  Проверьте путь и имя файла."
                ),
                'wrong': 'OpenExcel("no_such_file.xlsx")',
                'right': 'OpenExcel("data.xlsx")',
                'explanation': (
                    "Файл должен существовать на диске.\n"
                    "\n"
                    "Возможные причины:\n"
                    "  • опечатка в имени файла\n"
                    "  • файл лежит в другой папке\n"
                    "  • используется относительный путь без папки\n"
                    "\n"
                    "Проверьте путь:\n"
                    "     print(OpenExcel(\"data.xlsx\"))   # ошибка, если нет файла\n"
                    "\n"
                    "Правильно:\n"
                    "     OpenExcel(\"C:\\\\data\\\\file.xlsx\")"
                ),
                'variants': [
                    'OpenExcel("data.xlsx")',
                    'OpenExcel("C:\\data\\file.xlsx")',
                ],
            },
            'EXCEL_SHEET_NOT_FOUND': {
                'message': (
                    "OpenExcel: лист не найден в файле.\n"
                    "  Проверьте имя или номер листа."
                ),
                'wrong': 'OpenExcel("data.xlsx", "НетТакого")',
                'right': 'OpenExcel("data.xlsx", "Продажи")',
                'explanation': (
                    "Лист указывается по имени, номеру или all:\n"
                    "     OpenExcel(\"file.xlsx\", \"Продажи\")   # по имени\n"
                    "     OpenExcel(\"file.xlsx\", 1)            # первый лист\n"
                    "     OpenExcel(\"file.xlsx\", all)          # все листы\n"
                    "\n"
                    "Имена листов в файле — через openpyxl:\n"
                    "     m = OpenExcel(\"file.xlsx\", all)\n"
                    "     print(m)"
                ),
                'variants': [
                    'OpenExcel("data.xlsx", "Продажи")',
                    'OpenExcel("data.xlsx", 1)',
                    'OpenExcel("data.xlsx", all)',
                ],
            },
            'EXCEL_LOAD_ERROR': {
                'message': (
                    "OpenExcel: ошибка чтения файла.\n"
                    "  Файл повреждён или не является .xlsx."
                ),
                'wrong': 'OpenExcel("broken.xlsx")',
                'right': 'OpenExcel("valid.xlsx")',
                'explanation': (
                    "Проверьте:\n"
                    "  • файл открывается в Excel\n"
                    "  • формат — .xlsx или .xls\n"
                    "  • нет лишних расширений (например, .xlsx.txt)"
                ),
                'variants': [
                    'OpenExcel("data.xlsx")',
                ],
            },
            'EXCEL_NOT_INSTALLED': {
                'message': (
                    "OpenExcel: python-calamine не установлен.\n"
                    "  Установите: pip install python-calamine"
                ),
                'wrong': 'OpenExcel("data.xlsx")',
                'right': (
                    'pip install python-calamine\n'
                    'OpenExcel("data.xlsx")'
                ),
                'explanation': (
                    "OpenExcel использует python-calamine (Rust/calamine).\n"
                    "\n"
                    "Установка:\n"
                    "     pip install python-calamine"
                ),
                'variants': [
                    'pip install python-calamine\nOpenExcel("data.xlsx")',
                ],
            },
        },
    },

    # ============================================================
    # EXCEL — SaveExcel
    # ============================================================
    'SaveExcel': {
        'name': 'SaveExcel',
        'category': 'excel',
        'signature': 'SaveExcel(данные, "file.xlsx" [, "Лист1"])',
        'description': (
            'Сохранение в Excel.\n'
            '  • Новый файл — pyexcelerate (быстро).\n'
            '  • Существующий — openpyxl (дописать/заменить лист).'
        ),
        'examples': [
            'SaveExcel(m, "out.xlsx")',
            'SaveExcel(m, "out.xlsx", "Результат")',
        ],
        'errors': {
            'SAVEEXCEL_BAD_SYNTAX': {
                'message': (
                    "SaveExcel: неверный синтаксис.\n"
                    "  Нужны данные и путь к файлу."
                ),
                'wrong': 'SaveExcel(m)',
                'right': 'SaveExcel(m, "out.xlsx")',
                'explanation': (
                    "SaveExcel принимает 2 или 3 аргумента:\n"
                    "     SaveExcel(данные, \"file.xlsx\")\n"
                    "     SaveExcel(данные, \"file.xlsx\", \"Лист1\")\n"
                    "\n"
                    "Примеры:\n"
                    "     SaveExcel(m, \"out.xlsx\")\n"
                    "     SaveExcel(m, \"out.xlsx\", \"Результат\")"
                ),
                'variants': [
                    'SaveExcel(m, "out.xlsx")',
                    'SaveExcel(m, "out.xlsx", "Результат")',
                ],
            },
            'EXCEL_SAVE_ERROR': {
                'message': (
                    "SaveExcel: не удалось сохранить файл.\n"
                    "  Проверьте путь и права на запись."
                ),
                'wrong': 'SaveExcel(m, "C:\\no_folder\\out.xlsx")',
                'right': 'SaveExcel(m, "out.xlsx")',
                'explanation': (
                    "Возможные причины:\n"
                    "  • папка не существует\n"
                    "  • нет прав на запись\n"
                    "  • файл занят другим приложением (открыт в Excel)"
                ),
                'variants': [
                    'SaveExcel(m, "out.xlsx")',
                    'SaveExcel(m, "C:\\reports\\out.xlsx")',
                ],
            },
            'EXCEL_NOT_INSTALLED': {
                'message': (
                    "SaveExcel: pyexcelerate / openpyxl не установлены.\n"
                    "  Установите: pip install pyexcelerate openpyxl"
                ),
                'wrong': 'SaveExcel(m, "out.xlsx")',
                'right': (
                    'pip install pyexcelerate openpyxl\n'
                    'SaveExcel(m, "out.xlsx")'
                ),
                'explanation': (
                    "SaveExcel использует:\n"
                    "  • pyexcelerate — для нового файла (быстро)\n"
                    "  • openpyxl — для дописывания в существующий\n"
                    "\n"
                    "Установка обеих:\n"
                    "     pip install pyexcelerate openpyxl"
                ),
                'variants': [
                    'pip install pyexcelerate openpyxl\nSaveExcel(m, "out.xlsx")',
                ],
            },
        },
    },

    # ============================================================
    # EXCEL — OpenExcelShow
    # ============================================================
    'OpenExcelShow': {
        'name': 'OpenExcelShow',
        'category': 'excel',
        'signature': 'OpenExcelShow([all])',
        'description': (
            'Диалог выбора Excel + окно выбора листов (чекбоксы).\n'
            '  • Без параметра — пользователь выбирает листы.\n'
            '  • all — загрузить все листы без диалога.'
        ),
        'examples': [
            'm = OpenExcelShow()',
            'm = OpenExcelShow(all)',
        ],
        'errors': {
            'OPENEXCELSHOW_BAD_SYNTAX': {
                'message': (
                    "OpenExcelShow: неверный синтаксис.\n"
                    "  Либо без аргументов, либо all."
                ),
                'wrong': 'OpenExcelShow("file.xlsx")',
                'right': 'OpenExcelShow()',
                'explanation': (
                    "OpenExcelShow сам открывает диалог выбора файла.\n"
                    "Путь передавать НЕ нужно.\n"
                    "\n"
                    "Правильно:\n"
                    "     OpenExcelShow()        # диалог + выбор листов\n"
                    "     OpenExcelShow(all)     # диалог + все листы"
                ),
                'variants': [
                    'OpenExcelShow()',
                    'OpenExcelShow(all)',
                ],
            },
            'EXCEL_NOT_INSTALLED': {
                'message': (
                    "OpenExcelShow: python-calamine не установлен.\n"
                    "  Установите: pip install python-calamine"
                ),
                'wrong': 'OpenExcelShow()',
                'right': (
                    'pip install python-calamine\n'
                    'OpenExcelShow()'
                ),
                'explanation': (
                    "OpenExcelShow использует python-calamine для чтения."
                ),
                'variants': [
                    'pip install python-calamine\nOpenExcelShow()',
                ],
            },
        },
    },

    # ============================================================
    # EXCEL — SaveExcelShow
    # ============================================================
    'SaveExcelShow': {
        'name': 'SaveExcelShow',
        'category': 'excel',
        'signature': 'SaveExcelShow(данные [, "Лист1"])',
        'description': 'Диалог сохранения в Excel.',
        'examples': [
            'SaveExcelShow(m)',
            'SaveExcelShow(m, "Результат")',
        ],
        'errors': {
            'SAVEEXCELSHOW_BAD_SYNTAX': {
                'message': (
                    "SaveExcelShow: неверный синтаксис.\n"
                    "  Нужны данные и, опционально, имя листа."
                ),
                'wrong': 'SaveExcelShow()',
                'right': 'SaveExcelShow(m)',
                'explanation': (
                    "SaveExcelShow принимает 1 или 2 аргумента:\n"
                    "     SaveExcelShow(данные)\n"
                    "     SaveExcelShow(данные, \"Лист1\")"
                ),
                'variants': [
                    'SaveExcelShow(m)',
                    'SaveExcelShow(m, "Результат")',
                ],
            },
            'EXCEL_SAVE_ERROR': {
                'message': (
                    "SaveExcelShow: не удалось сохранить файл.\n"
                    "  Проверьте путь и права на запись."
                ),
                'wrong': 'SaveExcelShow(m)   # нет прав на запись',
                'right': 'SaveExcelShow(m)   # папка доступна',
                'explanation': (
                    "Возможные причины:\n"
                    "  • папка не существует\n"
                    "  • нет прав на запись\n"
                    "  • файл занят другим приложением"
                ),
                'variants': [
                    'SaveExcelShow(m)',
                ],
            },
        },
    },

    # ============================================================
    # CSV — OpenCSV
    # ============================================================
    'OpenCSV': {
        'name': 'OpenCSV',
        'category': 'csv',
        'signature': 'OpenCSV("file.csv" [, BigData | Table])',
        'description': (
            'Загрузка из CSV.\n'
            '  • Без режима — авто (по размеру файла).\n'
            '  • BigData — принудительно DuckDB (до 1 млрд строк).\n'
            '  • Table — принудительно RAM (MatrExMatrix).\n'
            '  • Порог авто: 250 МБ.'
        ),
        'examples': [
            'm = OpenCSV("data.csv")              # авто',
            'm = OpenCSV("big.csv", BigData)      # DuckDB',
            'm = OpenCSV("small.csv", Table)      # RAM',
        ],
        'errors': {
            'OPENCSV_BAD_SYNTAX': {
                'message': (
                    "OpenCSV: неверный синтаксис.\n"
                    "  Нужен путь к файлу и, опционально, режим."
                ),
                'wrong': 'OpenCSV()',
                'right': 'OpenCSV("data.csv")',
                'explanation': (
                    "OpenCSV принимает 1 или 2 аргумента:\n"
                    "     OpenCSV(\"file.csv\")\n"
                    "     OpenCSV(\"file.csv\", BigData)\n"
                    "     OpenCSV(\"file.csv\", Table)"
                ),
                'variants': [
                    'OpenCSV("data.csv")',
                    'OpenCSV("big.csv", BigData)',
                    'OpenCSV("small.csv", Table)',
                ],
            },
            'OPENCSV_PATH_NOT_STRING': {
                'message': (
                    "OpenCSV: путь к файлу должен быть строкой в кавычках."
                ),
                'wrong': 'OpenCSV(data.csv)',
                'right': 'OpenCSV("data.csv")',
                'explanation': (
                    "Путь — СТРОКА В КАВЫЧКАХ:\n"
                    "     OpenCSV(\"data.csv\")\n"
                    "     OpenCSV(\"C:\\\\data\\\\file.csv\")"
                ),
                'variants': [
                    'OpenCSV("data.csv")',
                    'OpenCSV("C:\\data\\file.csv")',
                ],
            },
            'CSV_FILE_NOT_FOUND': {
                'message': (
                    "OpenCSV: файл не найден.\n"
                    "  Проверьте путь и имя файла."
                ),
                'wrong': 'OpenCSV("no_such_file.csv")',
                'right': 'OpenCSV("data.csv")',
                'explanation': (
                    "Файл должен существовать на диске.\n"
                    "Проверьте путь и имя.\n"
                    "\n"
                    "Относительный путь ищется от рабочей папки\n"
                    "(где запущен ArrayVator)."
                ),
                'variants': [
                    'OpenCSV("data.csv")',
                    'OpenCSV("C:\\data\\file.csv")',
                ],
            },
            'CSV_BAD_MODE': {
                'message': (
                    "OpenCSV: неверный режим.\n"
                    "  Допустимо: BigData, Table."
                ),
                'wrong': 'OpenCSV("f.csv", Auto)',
                'right': 'OpenCSV("f.csv", BigData)',
                'explanation': (
                    "Режим указывается ВТОРЫМ аргументом, БЕЗ кавычек:\n"
                    "     BigData — данные на диске (DuckDB), RAM ~50 МБ\n"
                    "     Table   — данные в RAM (MatrExMatrix)\n"
                    "\n"
                    "НЕ:\n"
                    "     Auto  ❌\n"
                    "     Big   ❌\n"
                    "     \"BigData\"  ❌ (не строка!)\n"
                    "\n"
                    "Если режим не указан — авто по размеру файла."
                ),
                'variants': [
                    'OpenCSV("file.csv")',
                    'OpenCSV("file.csv", BigData)',
                    'OpenCSV("file.csv", Table)',
                ],
            },
            'CSV_MODE_NOT_STRING': {
                'message': (
                    "OpenCSV: режим должен быть BigData или Table."
                ),
                'wrong': 'OpenCSV("f.csv", "BigData")',
                'right': 'OpenCSV("f.csv", BigData)',
                'explanation': (
                    "Режим — КЛЮЧЕВОЕ СЛОВО без кавычек:\n"
                    "     OpenCSV(\"file.csv\", BigData)   # DuckDB\n"
                    "     OpenCSV(\"file.csv\", Table)     # RAM"
                ),
                'variants': [
                    'OpenCSV("file.csv", BigData)',
                    'OpenCSV("file.csv", Table)',
                ],
            },
            'CSV_BIGDATA_NOT_AVAILABLE': {
                'message': (
                    "OpenCSV: режим BigData требует DuckDB.\n"
                    "  Установите: pip install duckdb"
                ),
                'wrong': 'OpenCSV("big.csv", BigData)',
                'right': (
                    'pip install duckdb\n'
                    'OpenCSV("big.csv", BigData)'
                ),
                'explanation': (
                    "Режим BigData работает через DuckDB.\n"
                    "\n"
                    "Установка:\n"
                    "     pip install duckdb\n"
                    "\n"
                    "После установки:\n"
                    "     m = OpenCSV(\"big.csv\", BigData)"
                ),
                'variants': [
                    'pip install duckdb\nOpenCSV("big.csv", BigData)',
                ],
            },
            'CSV_LOAD_ERROR': {
                'message': (
                    "OpenCSV: ошибка чтения файла.\n"
                    "  Файл повреждён или кодировка не поддерживается."
                ),
                'wrong': 'OpenCSV("broken.csv")',
                'right': 'OpenCSV("valid.csv")',
                'explanation': (
                    "Возможные причины:\n"
                    "  • файл повреждён\n"
                    "  • кодировка не utf-8/cp1251/latin-1\n"
                    "  • неверный разделитель в первой строке\n"
                    "\n"
                    "OpenCSV автоопределяет: разделитель (, ; \\t |)\n"
                    "и кодировку (utf-8, cp1251, latin-1)."
                ),
                'variants': [
                    'OpenCSV("data.csv")',
                ],
            },
            'CSV_ENCODING_ERROR': {
                'message': (
                    "OpenCSV: не удалось определить кодировку файла."
                ),
                'wrong': 'OpenCSV("unknown_encoding.csv")',
                'right': 'OpenCSV("utf8_file.csv")',
                'explanation': (
                    "OpenCSV пробует кодировки по порядку:\n"
                    "     utf-8, cp1251, latin-1\n"
                    "\n"
                    "Если ни одна не подошла — пересохраните файл в UTF-8."
                ),
                'variants': [
                    'OpenCSV("data.csv")',
                ],
            },
        },
    },

    # ============================================================
    # CSV — SaveCSV
    # ============================================================
    'SaveCSV': {
        'name': 'SaveCSV',
        'category': 'csv',
        'signature': 'SaveCSV(данные, "file.csv")',
        'description': (
            'Сохранение в CSV.\n'
            '  • Кодировка utf-8-sig (с BOM для Excel).\n'
            '  • Разделитель — запятая.'
        ),
        'examples': [
            'SaveCSV(m, "out.csv")',
        ],
        'errors': {
            'SAVECSV_BAD_SYNTAX': {
                'message': (
                    "SaveCSV: неверный синтаксис.\n"
                    "  Нужны данные и путь к файлу."
                ),
                'wrong': 'SaveCSV(m)',
                'right': 'SaveCSV(m, "out.csv")',
                'explanation': (
                    "SaveCSV принимает ДВА аргумента:\n"
                    "     SaveCSV(данные, \"file.csv\")"
                ),
                'variants': [
                    'SaveCSV(m, "out.csv")',
                ],
            },
            'CSV_SAVE_ERROR': {
                'message': (
                    "SaveCSV: не удалось сохранить файл.\n"
                    "  Проверьте путь и права на запись."
                ),
                'wrong': 'SaveCSV(m, "C:\\no_folder\\out.csv")',
                'right': 'SaveCSV(m, "out.csv")',
                'explanation': (
                    "Возможные причины:\n"
                    "  • папка не существует\n"
                    "  • нет прав на запись\n"
                    "  • файл занят другим приложением"
                ),
                'variants': [
                    'SaveCSV(m, "out.csv")',
                ],
            },
        },
    },

    # ============================================================
    # CSV — OpenCSVShow
    # ============================================================
    'OpenCSVShow': {
        'name': 'OpenCSVShow',
        'category': 'csv',
        'signature': 'OpenCSVShow([BigData | Table])',
        'description': 'Диалог выбора CSV-файла.',
        'examples': [
            'm = OpenCSVShow()',
            'm = OpenCSVShow(BigData)',
            'm = OpenCSVShow(Table)',
        ],
        'errors': {
            'OPENCSVSHOW_BAD_SYNTAX': {
                'message': (
                    "OpenCSVShow: неверный синтаксис.\n"
                    "  Либо без аргументов, либо BigData | Table."
                ),
                'wrong': 'OpenCSVShow("file.csv")',
                'right': 'OpenCSVShow()',
                'explanation': (
                    "OpenCSVShow сам открывает диалог выбора файла.\n"
                    "Путь передавать НЕ нужно.\n"
                    "\n"
                    "Правильно:\n"
                    "     OpenCSVShow()             # авто\n"
                    "     OpenCSVShow(BigData)      # DuckDB\n"
                    "     OpenCSVShow(Table)        # RAM"
                ),
                'variants': [
                    'OpenCSVShow()',
                    'OpenCSVShow(BigData)',
                    'OpenCSVShow(Table)',
                ],
            },
            'CSV_BAD_MODE': {
                'message': (
                    "OpenCSVShow: неверный режим.\n"
                    "  Допустимо: BigData, Table."
                ),
                'wrong': 'OpenCSVShow(Auto)',
                'right': 'OpenCSVShow(BigData)',
                'explanation': (
                    "Режим — ключевое слово без кавычек:\n"
                    "     OpenCSVShow()             # авто\n"
                    "     OpenCSVShow(BigData)      # DuckDB\n"
                    "     OpenCSVShow(Table)        # RAM"
                ),
                'variants': [
                    'OpenCSVShow()',
                    'OpenCSVShow(BigData)',
                    'OpenCSVShow(Table)',
                ],
            },
        },
    },

    # ============================================================
    # CSV — SaveCSVShow
    # ============================================================
    'SaveCSVShow': {
        'name': 'SaveCSVShow',
        'category': 'csv',
        'signature': 'SaveCSVShow(данные)',
        'description': 'Диалог сохранения в CSV.',
        'examples': [
            'SaveCSVShow(m)',
        ],
        'errors': {
            'SAVECSVSHOW_BAD_SYNTAX': {
                'message': (
                    "SaveCSVShow: неверный синтаксис.\n"
                    "  Нужны данные."
                ),
                'wrong': 'SaveCSVShow()',
                'right': 'SaveCSVShow(m)',
                'explanation': (
                    "SaveCSVShow принимает ОДИН аргумент:\n"
                    "     SaveCSVShow(данные)"
                ),
                'variants': [
                    'SaveCSVShow(m)',
                ],
            },
            'CSV_SAVE_ERROR': {
                'message': (
                    "SaveCSVShow: не удалось сохранить файл.\n"
                    "  Проверьте путь и права на запись."
                ),
                'wrong': 'SaveCSVShow(m)   # папка недоступна',
                'right': 'SaveCSVShow(m)   # папка доступна',
                'explanation': (
                    "Возможные причины:\n"
                    "  • папка не существует\n"
                    "  • нет прав на запись\n"
                    "  • файл занят другим приложением"
                ),
                'variants': [
                    'SaveCSVShow(m)',
                ],
            },
        },
    },
}


EN = {
    # ============================================================
    # EXCEL — OpenExcel
    # ============================================================
    'OpenExcel': {
        'name': 'OpenExcel',
        'category': 'excel',
        'signature': 'OpenExcel("file.xlsx" [, sheet])',
        'description': (
            'Load from Excel.\n'
            '  • No sheet — first sheet.\n'
            '  • "Sheet1" — by name.\n'
            '  • 1, 2, ... — by number (1-based).\n'
            '  • all — all sheets in a row.\n'
            '  • Reading — python-calamine (~10x faster than openpyxl).'
        ),
        'examples': [
            'm = OpenExcel("data.xlsx")',
            'm = OpenExcel("data.xlsx", "Sales")',
            'm = OpenExcel("data.xlsx", 1)',
            'm = OpenExcel("data.xlsx", all)',
        ],
        'errors': {
            'OPENEXCEL_BAD_SYNTAX': {
                'message': (
                    "OpenExcel: invalid syntax.\n"
                    "  Need a file path and optionally a sheet."
                ),
                'wrong': 'OpenExcel()',
                'right': 'OpenExcel("data.xlsx")',
                'explanation': (
                    "OpenExcel takes 1 or 2 arguments:\n"
                    "     OpenExcel(\"file.xlsx\")\n"
                    "     OpenExcel(\"file.xlsx\", \"Sheet1\")\n"
                    "     OpenExcel(\"file.xlsx\", 1)\n"
                    "     OpenExcel(\"file.xlsx\", all)"
                ),
                'variants': [
                    'OpenExcel("data.xlsx")',
                    'OpenExcel("data.xlsx", "Sales")',
                    'OpenExcel("data.xlsx", 1)',
                    'OpenExcel("data.xlsx", all)',
                ],
            },
            'OPENEXCEL_PATH_NOT_STRING': {
                'message': (
                    "OpenExcel: file path must be a quoted string."
                ),
                'wrong': 'OpenExcel(data.xlsx)',
                'right': 'OpenExcel("data.xlsx")',
                'explanation': (
                    "Path is a STRING IN QUOTES:\n"
                    "     OpenExcel(\"data.xlsx\")\n"
                    "     OpenExcel(\"C:\\\\reports\\\\data.xlsx\")"
                ),
                'variants': [
                    'OpenExcel("data.xlsx")',
                    'OpenExcel("C:\\reports\\data.xlsx")',
                ],
            },
            'EXCEL_FILE_NOT_FOUND': {
                'message': (
                    "OpenExcel: file not found.\n"
                    "  Check the path and file name."
                ),
                'wrong': 'OpenExcel("no_such_file.xlsx")',
                'right': 'OpenExcel("data.xlsx")',
                'explanation': (
                    "The file must exist on disk.\n"
                    "\n"
                    "Possible reasons:\n"
                    "  • typo in the file name\n"
                    "  • file is in another folder\n"
                    "  • relative path without a folder\n"
                    "\n"
                    "Correct:\n"
                    "     OpenExcel(\"C:\\\\data\\\\file.xlsx\")"
                ),
                'variants': [
                    'OpenExcel("data.xlsx")',
                    'OpenExcel("C:\\data\\file.xlsx")',
                ],
            },
            'EXCEL_SHEET_NOT_FOUND': {
                'message': (
                    "OpenExcel: sheet not found in the file.\n"
                    "  Check the sheet name or number."
                ),
                'wrong': 'OpenExcel("data.xlsx", "NoSuchSheet")',
                'right': 'OpenExcel("data.xlsx", "Sales")',
                'explanation': (
                    "Sheet is specified by name, number, or all:\n"
                    "     OpenExcel(\"file.xlsx\", \"Sales\")   # by name\n"
                    "     OpenExcel(\"file.xlsx\", 1)          # first sheet\n"
                    "     OpenExcel(\"file.xlsx\", all)        # all sheets"
                ),
                'variants': [
                    'OpenExcel("data.xlsx", "Sales")',
                    'OpenExcel("data.xlsx", 1)',
                    'OpenExcel("data.xlsx", all)',
                ],
            },
            'EXCEL_LOAD_ERROR': {
                'message': (
                    "OpenExcel: failed to read the file.\n"
                    "  File is corrupted or not .xlsx."
                ),
                'wrong': 'OpenExcel("broken.xlsx")',
                'right': 'OpenExcel("valid.xlsx")',
                'explanation': (
                    "Check:\n"
                    "  • file opens in Excel\n"
                    "  • format is .xlsx or .xls\n"
                    "  • no extra extensions (e.g., .xlsx.txt)"
                ),
                'variants': [
                    'OpenExcel("data.xlsx")',
                ],
            },
            'EXCEL_NOT_INSTALLED': {
                'message': (
                    "OpenExcel: python-calamine is not installed.\n"
                    "  Install: pip install python-calamine"
                ),
                'wrong': 'OpenExcel("data.xlsx")',
                'right': (
                    'pip install python-calamine\n'
                    'OpenExcel("data.xlsx")'
                ),
                'explanation': (
                    "OpenExcel uses python-calamine (Rust/calamine).\n"
                    "\n"
                    "Install:\n"
                    "     pip install python-calamine"
                ),
                'variants': [
                    'pip install python-calamine\nOpenExcel("data.xlsx")',
                ],
            },
        },
    },

    # ============================================================
    # EXCEL — SaveExcel
    # ============================================================
    'SaveExcel': {
        'name': 'SaveExcel',
        'category': 'excel',
        'signature': 'SaveExcel(data, "file.xlsx" [, "Sheet1"])',
        'description': (
            'Save to Excel.\n'
            '  • New file — pyexcelerate (fast).\n'
            '  • Existing — openpyxl (append/replace sheet).'
        ),
        'examples': [
            'SaveExcel(m, "out.xlsx")',
            'SaveExcel(m, "out.xlsx", "Result")',
        ],
        'errors': {
            'SAVEEXCEL_BAD_SYNTAX': {
                'message': (
                    "SaveExcel: invalid syntax.\n"
                    "  Need data and a file path."
                ),
                'wrong': 'SaveExcel(m)',
                'right': 'SaveExcel(m, "out.xlsx")',
                'explanation': (
                    "SaveExcel takes 2 or 3 arguments:\n"
                    "     SaveExcel(data, \"file.xlsx\")\n"
                    "     SaveExcel(data, \"file.xlsx\", \"Sheet1\")"
                ),
                'variants': [
                    'SaveExcel(m, "out.xlsx")',
                    'SaveExcel(m, "out.xlsx", "Result")',
                ],
            },
            'EXCEL_SAVE_ERROR': {
                'message': (
                    "SaveExcel: failed to save the file.\n"
                    "  Check the path and write permissions."
                ),
                'wrong': 'SaveExcel(m, "C:\\no_folder\\out.xlsx")',
                'right': 'SaveExcel(m, "out.xlsx")',
                'explanation': (
                    "Possible reasons:\n"
                    "  • folder does not exist\n"
                    "  • no write permission\n"
                    "  • file is locked by another application"
                ),
                'variants': [
                    'SaveExcel(m, "out.xlsx")',
                ],
            },
            'EXCEL_NOT_INSTALLED': {
                'message': (
                    "SaveExcel: pyexcelerate / openpyxl not installed.\n"
                    "  Install: pip install pyexcelerate openpyxl"
                ),
                'wrong': 'SaveExcel(m, "out.xlsx")',
                'right': (
                    'pip install pyexcelerate openpyxl\n'
                    'SaveExcel(m, "out.xlsx")'
                ),
                'explanation': (
                    "SaveExcel uses:\n"
                    "  • pyexcelerate — for a new file (fast)\n"
                    "  • openpyxl — for appending to an existing one"
                ),
                'variants': [
                    'pip install pyexcelerate openpyxl\nSaveExcel(m, "out.xlsx")',
                ],
            },
        },
    },

    # ============================================================
    # EXCEL — OpenExcelShow
    # ============================================================
    'OpenExcelShow': {
        'name': 'OpenExcelShow',
        'category': 'excel',
        'signature': 'OpenExcelShow([all])',
        'description': (
            'Dialog for Excel file + sheet selection (checkboxes).\n'
            '  • No parameter — user chooses sheets.\n'
            '  • all — load all sheets without dialog.'
        ),
        'examples': [
            'm = OpenExcelShow()',
            'm = OpenExcelShow(all)',
        ],
        'errors': {
            'OPENEXCELSHOW_BAD_SYNTAX': {
                'message': (
                    "OpenExcelShow: invalid syntax.\n"
                    "  Either no arguments or all."
                ),
                'wrong': 'OpenExcelShow("file.xlsx")',
                'right': 'OpenExcelShow()',
                'explanation': (
                    "OpenExcelShow itself opens the file dialog.\n"
                    "No path is needed.\n"
                    "\n"
                    "Correct:\n"
                    "     OpenExcelShow()        # dialog + sheet selection\n"
                    "     OpenExcelShow(all)     # dialog + all sheets"
                ),
                'variants': [
                    'OpenExcelShow()',
                    'OpenExcelShow(all)',
                ],
            },
            'EXCEL_NOT_INSTALLED': {
                'message': (
                    "OpenExcelShow: python-calamine is not installed.\n"
                    "  Install: pip install python-calamine"
                ),
                'wrong': 'OpenExcelShow()',
                'right': (
                    'pip install python-calamine\n'
                    'OpenExcelShow()'
                ),
                'explanation': (
                    "OpenExcelShow uses python-calamine for reading."
                ),
                'variants': [
                    'pip install python-calamine\nOpenExcelShow()',
                ],
            },
        },
    },

    # ============================================================
    # EXCEL — SaveExcelShow
    # ============================================================
    'SaveExcelShow': {
        'name': 'SaveExcelShow',
        'category': 'excel',
        'signature': 'SaveExcelShow(data [, "Sheet1"])',
        'description': 'Dialog for saving to Excel.',
        'examples': [
            'SaveExcelShow(m)',
            'SaveExcelShow(m, "Result")',
        ],
        'errors': {
            'SAVEEXCELSHOW_BAD_SYNTAX': {
                'message': (
                    "SaveExcelShow: invalid syntax.\n"
                    "  Need data and optionally a sheet name."
                ),
                'wrong': 'SaveExcelShow()',
                'right': 'SaveExcelShow(m)',
                'explanation': (
                    "SaveExcelShow takes 1 or 2 arguments:\n"
                    "     SaveExcelShow(data)\n"
                    "     SaveExcelShow(data, \"Sheet1\")"
                ),
                'variants': [
                    'SaveExcelShow(m)',
                    'SaveExcelShow(m, "Result")',
                ],
            },
            'EXCEL_SAVE_ERROR': {
                'message': (
                    "SaveExcelShow: failed to save the file.\n"
                    "  Check the path and write permissions."
                ),
                'wrong': 'SaveExcelShow(m)   # no write permission',
                'right': 'SaveExcelShow(m)   # folder is writable',
                'explanation': (
                    "Possible reasons:\n"
                    "  • folder does not exist\n"
                    "  • no write permission\n"
                    "  • file is locked"
                ),
                'variants': [
                    'SaveExcelShow(m)',
                ],
            },
        },
    },

    # ============================================================
    # CSV — OpenCSV
    # ============================================================
    'OpenCSV': {
        'name': 'OpenCSV',
        'category': 'csv',
        'signature': 'OpenCSV("file.csv" [, BigData | Table])',
        'description': (
            'Load from CSV.\n'
            '  • No mode — auto (by file size).\n'
            '  • BigData — force DuckDB (up to 1 billion rows).\n'
            '  • Table — force RAM (MatrExMatrix).\n'
            '  • Auto threshold: 250 MB.'
        ),
        'examples': [
            'm = OpenCSV("data.csv")              # auto',
            'm = OpenCSV("big.csv", BigData)      # DuckDB',
            'm = OpenCSV("small.csv", Table)      # RAM',
        ],
        'errors': {
            'OPENCSV_BAD_SYNTAX': {
                'message': (
                    "OpenCSV: invalid syntax.\n"
                    "  Need a file path and optionally a mode."
                ),
                'wrong': 'OpenCSV()',
                'right': 'OpenCSV("data.csv")',
                'explanation': (
                    "OpenCSV takes 1 or 2 arguments:\n"
                    "     OpenCSV(\"file.csv\")\n"
                    "     OpenCSV(\"file.csv\", BigData)\n"
                    "     OpenCSV(\"file.csv\", Table)"
                ),
                'variants': [
                    'OpenCSV("data.csv")',
                    'OpenCSV("big.csv", BigData)',
                    'OpenCSV("small.csv", Table)',
                ],
            },
            'OPENCSV_PATH_NOT_STRING': {
                'message': (
                    "OpenCSV: file path must be a quoted string."
                ),
                'wrong': 'OpenCSV(data.csv)',
                'right': 'OpenCSV("data.csv")',
                'explanation': (
                    "Path is a STRING IN QUOTES:\n"
                    "     OpenCSV(\"data.csv\")\n"
                    "     OpenCSV(\"C:\\\\data\\\\file.csv\")"
                ),
                'variants': [
                    'OpenCSV("data.csv")',
                    'OpenCSV("C:\\data\\file.csv")',
                ],
            },
            'CSV_FILE_NOT_FOUND': {
                'message': (
                    "OpenCSV: file not found.\n"
                    "  Check the path and file name."
                ),
                'wrong': 'OpenCSV("no_such_file.csv")',
                'right': 'OpenCSV("data.csv")',
                'explanation': (
                    "The file must exist on disk.\n"
                    "\n"
                    "Relative path is resolved from the working folder\n"
                    "(where ArrayVator is running)."
                ),
                'variants': [
                    'OpenCSV("data.csv")',
                    'OpenCSV("C:\\data\\file.csv")',
                ],
            },
            'CSV_BAD_MODE': {
                'message': (
                    "OpenCSV: invalid mode.\n"
                    "  Allowed: BigData, Table."
                ),
                'wrong': 'OpenCSV("f.csv", Auto)',
                'right': 'OpenCSV("f.csv", BigData)',
                'explanation': (
                    "Mode is the SECOND argument, WITHOUT quotes:\n"
                    "     BigData — data on disk (DuckDB), RAM ~50 MB\n"
                    "     Table   — data in RAM (MatrExMatrix)\n"
                    "\n"
                    "NOT:\n"
                    "     Auto  ❌\n"
                    "     Big   ❌\n"
                    "     \"BigData\"  ❌ (not a string!)\n"
                    "\n"
                    "If the mode is omitted — auto by file size."
                ),
                'variants': [
                    'OpenCSV("file.csv")',
                    'OpenCSV("file.csv", BigData)',
                    'OpenCSV("file.csv", Table)',
                ],
            },
            'CSV_MODE_NOT_STRING': {
                'message': (
                    "OpenCSV: mode must be BigData or Table."
                ),
                'wrong': 'OpenCSV("f.csv", "BigData")',
                'right': 'OpenCSV("f.csv", BigData)',
                'explanation': (
                    "Mode is a KEYWORD without quotes:\n"
                    "     OpenCSV(\"file.csv\", BigData)   # DuckDB\n"
                    "     OpenCSV(\"file.csv\", Table)     # RAM"
                ),
                'variants': [
                    'OpenCSV("file.csv", BigData)',
                    'OpenCSV("file.csv", Table)',
                ],
            },
            'CSV_BIGDATA_NOT_AVAILABLE': {
                'message': (
                    "OpenCSV: BigData mode requires DuckDB.\n"
                    "  Install: pip install duckdb"
                ),
                'wrong': 'OpenCSV("big.csv", BigData)',
                'right': (
                    'pip install duckdb\n'
                    'OpenCSV("big.csv", BigData)'
                ),
                'explanation': (
                    "BigData mode works through DuckDB.\n"
                    "\n"
                    "Install:\n"
                    "     pip install duckdb"
                ),
                'variants': [
                    'pip install duckdb\nOpenCSV("big.csv", BigData)',
                ],
            },
            'CSV_LOAD_ERROR': {
                'message': (
                    "OpenCSV: failed to read the file.\n"
                    "  File is corrupted or encoding is unsupported."
                ),
                'wrong': 'OpenCSV("broken.csv")',
                'right': 'OpenCSV("valid.csv")',
                'explanation': (
                    "Possible reasons:\n"
                    "  • file is corrupted\n"
                    "  • encoding is not utf-8/cp1251/latin-1\n"
                    "  • wrong delimiter in the first line\n"
                    "\n"
                    "OpenCSV auto-detects: delimiter (, ; \\t |)\n"
                    "and encoding (utf-8, cp1251, latin-1)."
                ),
                'variants': [
                    'OpenCSV("data.csv")',
                ],
            },
            'CSV_ENCODING_ERROR': {
                'message': (
                    "OpenCSV: failed to detect file encoding."
                ),
                'wrong': 'OpenCSV("unknown_encoding.csv")',
                'right': 'OpenCSV("utf8_file.csv")',
                'explanation': (
                    "OpenCSV tries encodings in order:\n"
                    "     utf-8, cp1251, latin-1\n"
                    "\n"
                    "If none works — re-save the file as UTF-8."
                ),
                'variants': [
                    'OpenCSV("data.csv")',
                ],
            },
        },
    },

    # ============================================================
    # CSV — SaveCSV
    # ============================================================
    'SaveCSV': {
        'name': 'SaveCSV',
        'category': 'csv',
        'signature': 'SaveCSV(data, "file.csv")',
        'description': (
            'Save to CSV.\n'
            '  • Encoding: utf-8-sig (with BOM for Excel).\n'
            '  • Delimiter — comma.'
        ),
        'examples': [
            'SaveCSV(m, "out.csv")',
        ],
        'errors': {
            'SAVECSV_BAD_SYNTAX': {
                'message': (
                    "SaveCSV: invalid syntax.\n"
                    "  Need data and a file path."
                ),
                'wrong': 'SaveCSV(m)',
                'right': 'SaveCSV(m, "out.csv")',
                'explanation': (
                    "SaveCSV takes TWO arguments:\n"
                    "     SaveCSV(data, \"file.csv\")"
                ),
                'variants': [
                    'SaveCSV(m, "out.csv")',
                ],
            },
            'CSV_SAVE_ERROR': {
                'message': (
                    "SaveCSV: failed to save the file.\n"
                    "  Check the path and write permissions."
                ),
                'wrong': 'SaveCSV(m, "C:\\no_folder\\out.csv")',
                'right': 'SaveCSV(m, "out.csv")',
                'explanation': (
                    "Possible reasons:\n"
                    "  • folder does not exist\n"
                    "  • no write permission\n"
                    "  • file is locked"
                ),
                'variants': [
                    'SaveCSV(m, "out.csv")',
                ],
            },
        },
    },

    # ============================================================
    # CSV — OpenCSVShow
    # ============================================================
    'OpenCSVShow': {
        'name': 'OpenCSVShow',
        'category': 'csv',
        'signature': 'OpenCSVShow([BigData | Table])',
        'description': 'Dialog for selecting a CSV file.',
        'examples': [
            'm = OpenCSVShow()',
            'm = OpenCSVShow(BigData)',
            'm = OpenCSVShow(Table)',
        ],
        'errors': {
            'OPENCSVSHOW_BAD_SYNTAX': {
                'message': (
                    "OpenCSVShow: invalid syntax.\n"
                    "  Either no arguments or BigData | Table."
                ),
                'wrong': 'OpenCSVShow("file.csv")',
                'right': 'OpenCSVShow()',
                'explanation': (
                    "OpenCSVShow itself opens the file dialog.\n"
                    "No path is needed.\n"
                    "\n"
                    "Correct:\n"
                    "     OpenCSVShow()             # auto\n"
                    "     OpenCSVShow(BigData)      # DuckDB\n"
                    "     OpenCSVShow(Table)        # RAM"
                ),
                'variants': [
                    'OpenCSVShow()',
                    'OpenCSVShow(BigData)',
                    'OpenCSVShow(Table)',
                ],
            },
            'CSV_BAD_MODE': {
                'message': (
                    "OpenCSVShow: invalid mode.\n"
                    "  Allowed: BigData, Table."
                ),
                'wrong': 'OpenCSVShow(Auto)',
                'right': 'OpenCSVShow(BigData)',
                'explanation': (
                    "Mode is a keyword without quotes:\n"
                    "     OpenCSVShow()             # auto\n"
                    "     OpenCSVShow(BigData)      # DuckDB\n"
                    "     OpenCSVShow(Table)        # RAM"
                ),
                'variants': [
                    'OpenCSVShow()',
                    'OpenCSVShow(BigData)',
                    'OpenCSVShow(Table)',
                ],
            },
        },
    },

    # ============================================================
    # CSV — SaveCSVShow
    # ============================================================
    'SaveCSVShow': {
        'name': 'SaveCSVShow',
        'category': 'csv',
        'signature': 'SaveCSVShow(data)',
        'description': 'Dialog for saving to CSV.',
        'examples': [
            'SaveCSVShow(m)',
        ],
        'errors': {
            'SAVECSVSHOW_BAD_SYNTAX': {
                'message': (
                    "SaveCSVShow: invalid syntax.\n"
                    "  Need data."
                ),
                'wrong': 'SaveCSVShow()',
                'right': 'SaveCSVShow(m)',
                'explanation': (
                    "SaveCSVShow takes ONE argument:\n"
                    "     SaveCSVShow(data)"
                ),
                'variants': [
                    'SaveCSVShow(m)',
                ],
            },
            'CSV_SAVE_ERROR': {
                'message': (
                    "SaveCSVShow: failed to save the file.\n"
                    "  Check the path and write permissions."
                ),
                'wrong': 'SaveCSVShow(m)   # folder is locked',
                'right': 'SaveCSVShow(m)   # folder is writable',
                'explanation': (
                    "Possible reasons:\n"
                    "  • folder does not exist\n"
                    "  • no write permission\n"
                    "  • file is locked"
                ),
                'variants': [
                    'SaveCSVShow(m)',
                ],
            },
        },
    },
}