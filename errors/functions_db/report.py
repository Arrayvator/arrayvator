# errors/functions_db/report.py
"""
База ошибок для функций отчёта:
    report, report_section, report_text, report_table,
    report_chart, report_save, report_show, report_save_pdf.

СИНТАКСИС:
    report("Название", "file.html")
    report_section("1. Статистика")
    report_text("Текст")
    report_table(m [, title "Таблица"])
    report_chart(bar, x, y, title "...")
    report_save([show])
    report_show()
    report_save_pdf("file.pdf")

ВАЖНО:
    report — ОПЕРАТОР, не требует присваивания.
"""

RU = {
    'report': {
        'name': 'report',
        'category': 'report',
        'signature': 'report("Название", "file.html")',
        'description': (
            'Начинает отчёт — HTML с интерактивными графиками Plotly.\n'
            '  • Вызывается ОДИН РАЗ в начале.\n'
            '  • Дальше — report_section, report_text, report_table,\n'
            '    report_chart.\n'
            '  • report_save() — сохраняет HTML.\n'
            '  • report — ОПЕРАТОР, присваивание не нужно.\n'
            '  • При первом report_save() отчёт откроется в браузере.'
        ),
        'examples': [
            'report("Анализ продаж", "report.html")',
            'report("Отчёт", "report.html")',
        ],
        'errors': {
            'REPORT_BAD_SYNTAX': {
                'message': (
                    "report: неверный синтаксис.\n"
                    "  Нужны название и путь к HTML-файлу."
                ),
                'wrong': 'report("Анализ")',
                'right': 'report("Анализ", "report.html")',
                'explanation': (
                    "report принимает ДВА аргумента:\n"
                    "  1. Название — строка в кавычках\n"
                    "  2. Путь к HTML — строка в кавычках\n"
                    "\n"
                    "Структура:\n"
                    "  report(\"Название\", \"file.html\")"
                ),
                'variants': [
                    'report("Анализ продаж", "report.html")',
                    'report("Отчёт", "report_2025.html")',
                ],
            },
            'REPORT_NEED_TITLE': {
                'message': "report: не указано название.",
                'wrong': 'report()',
                'right': 'report("Анализ", "report.html")',
                'explanation': (
                    "Первый аргумент — НАЗВАНИЕ отчёта.\n"
                    "Это строка в кавычках.\n"
                    "\n"
                    "Правильно:\n"
                    "  report(\"Анализ продаж\", \"report.html\")"
                ),
                'variants': [
                    'report("Анализ продаж", "report.html")',
                    'report("Отчёт за 2025", "report_2025.html")',
                ],
            },
            'REPORT_NEED_PATH': {
                'message': "report: не указан путь к HTML-файлу.",
                'wrong': 'report("Анализ")',
                'right': 'report("Анализ", "report.html")',
                'explanation': (
                    "Второй аргумент — ПУТЬ к HTML-файлу.\n"
                    "Это строка в кавычках.\n"
                    "\n"
                    "Правильно:\n"
                    "  report(\"Анализ\", \"report.html\")\n"
                    "  report(\"Отчёт\", \"C:\\\\reports\\\\report.html\")"
                ),
                'variants': [
                    'report("Анализ", "report.html")',
                    'report("Отчёт", "C:\\reports\\report.html")',
                ],
            },
            'REPORT_NOT_STARTED': {
                'message': (
                    "report: отчёт не начат.\n"
                    "  Сначала вызовите report(\"Название\", \"file.html\")"
                ),
                'wrong': 'report_save()',
                'right': (
                    'report("Анализ", "report.html")\n'
                    'report_save()'
                ),
                'explanation': (
                    "Функции report_section, report_text, report_table,\n"
                    "report_chart, report_save, report_show, report_save_pdf\n"
                    "работают ТОЛЬКО после report().\n"
                    "\n"
                    "Неправильно:\n"
                    "     report_save()\n"
                    "\n"
                    "Правильно:\n"
                    "     report(\"Анализ\", \"report.html\")\n"
                    "     report_save()"
                ),
                'variants': [
                    'report("Анализ", "report.html")\nreport_save()',
                    'report("Отчёт", "report.html")\nreport_show()',
                ],
            },
            'REPORT_SAVE_ERROR': {
                'message': "report_save: не удалось сохранить HTML-файл.",
                'wrong': 'report_save()  # путь указывает на недоступную папку',
                'right': 'report_save()  # путь доступен для записи',
                'explanation': (
                    "Проверьте:\n"
                    "  • существует ли папка для сохранения\n"
                    "  • есть ли права на запись\n"
                    "  • не занят ли файл другим приложением"
                ),
                'variants': [
                    'report("Анализ", "C:\\reports\\report.html")\nreport_save()',
                    'report("Анализ", "report.html")\nreport_save()',
                ],
            },
            'REPORT_PLAYWRIGHT_MISSING': {
                'message': (
                    "report_save_pdf: Playwright не установлен.\n"
                    "  Установите: pip install playwright\n"
                    "  Затем:      python -m playwright install chromium"
                ),
                'wrong': 'report_save_pdf("report.pdf")',
                'right': (
                    'pip install playwright\n'
                    'python -m playwright install chromium\n'
                    'report_save_pdf("report.pdf")'
                ),
                'explanation': (
                    "report_save_pdf использует Playwright для рендера HTML → PDF.\n"
                    "\n"
                    "Если Playwright не установлен — откроется браузер\n"
                    "с готовым HTML, и PDF можно сохранить вручную:\n"
                    "     Ctrl+P → «Сохранить как PDF»"
                ),
                'variants': [
                    'pip install playwright\npython -m playwright install chromium\nreport_save_pdf("report.pdf")',
                    'report_save()  # затем Ctrl+P в браузере',
                ],
            },
            'REPORT_SAVE_PDF_ERROR': {
                'message': "report_save_pdf: не удалось сохранить PDF.",
                'wrong': 'report_save_pdf("C:\\no_folder\\report.pdf")',
                'right': 'report_save_pdf("report.pdf")',
                'explanation': (
                    "Проверьте:\n"
                    "  • существует ли папка для PDF\n"
                    "  • есть ли права на запись\n"
                    "  • установлен ли chromium для Playwright"
                ),
                'variants': [
                    'report_save_pdf("report.pdf")',
                    'report_save_pdf("C:\\reports\\report.pdf")',
                ],
            },
        },
    },

    # ============================================================
    # REPORT_SECTION
    # ============================================================
    'report_section': {
        'name': 'report_section',
        'category': 'report',
        'signature': 'report_section("Заголовок")',
        'description': (
            'Добавляет секцию (заголовок) в отчёт.\n'
            '  • Вызывается между report() и report_save().'
        ),
        'examples': [
            'report_section("1. Общая информация")',
            'report_section("2. Графики")',
        ],
        'errors': {
            'REPORT_SECTION_BAD_SYNTAX': {
                'message': "report_section: нужен заголовок.",
                'wrong': 'report_section()',
                'right': 'report_section("1. Общая информация")',
                'explanation': (
                    "report_section принимает ОДИН аргумент:\n"
                    "  • Заголовок — строка в кавычках"
                ),
                'variants': [
                    'report_section("1. Общая информация")',
                    'report_section("2. Графики")',
                ],
            },
        },
    },

    # ============================================================
    # REPORT_TEXT
    # ============================================================
    'report_text': {
        'name': 'report_text',
        'category': 'report',
        'signature': 'report_text("Текст")',
        'description': (
            'Добавляет абзац текста в отчёт.\n'
            '  • Вызывается между report() и report_save().'
        ),
        'examples': [
            'report_text("Отчёт создан автоматически.")',
            'report_text("Всего продаж: 100000")',
        ],
        'errors': {
            'REPORT_TEXT_BAD_SYNTAX': {
                'message': "report_text: нужен текст.",
                'wrong': 'report_text()',
                'right': 'report_text("Текст отчёта")',
                'explanation': (
                    "report_text принимает ОДИН аргумент:\n"
                    "  • Текст — строка в кавычках"
                ),
                'variants': [
                    'report_text("Отчёт создан автоматически.")',
                    'report_text("Итого: " + to_string(total))',
                ],
            },
        },
    },

    # ============================================================
    # REPORT_TABLE
    # ============================================================
    'report_table': {
        'name': 'report_table',
        'category': 'report',
        'signature': 'report_table(данные [, title "Заголовок"])',
        'description': (
            'Добавляет таблицу в отчёт.\n'
            '  • Данные — матрица или срез.\n'
            '  • title — опциональный заголовок.'
        ),
        'examples': [
            'report_table(m)',
            'report_table(m, title "Таблица продаж")',
        ],
        'errors': {
            'REPORT_TABLE_BAD_SYNTAX': {
                'message': "report_table: нужны данные (матрица).",
                'wrong': 'report_table()',
                'right': 'report_table(m)',
                'explanation': (
                    "report_table принимает 1 или 2 аргумента:\n"
                    "  1. Данные — матрица\n"
                    "  2. title \"...\" — опционально"
                ),
                'variants': [
                    'report_table(m)',
                    'report_table(m, title "Таблица продаж")',
                ],
            },
        },
    },

    # ============================================================
    # REPORT_CHART
    # ============================================================
    'report_chart': {
        'name': 'report_chart',
        'category': 'report',
        'signature': 'report_chart(тип, x [, y] [, опции])',
        'description': (
            'Добавляет интерактивный график Plotly в отчёт.\n'
            '  • Типы: bar, line, pie, hist, scatter, box, heatmap, pair.\n'
            '  • Опции: title, xlabel, ylabel, color, bins, plotly, static.'
        ),
        'examples': [
            'report_chart(bar, m[:, "Отдел"], m[:, "Зарплата"], title "Зарплаты")',
            'report_chart(line, m[:, "Месяц"], m[:, "Продажи"])',
            'report_chart(hist, m[:, "Возраст"], bins 10)',
        ],
        'errors': {
            'REPORT_CHART_BAD_KIND': {
                'message': (
                    "report_chart: неверный тип графика.\n"
                    "  Допустимо: bar, line, pie, hist, scatter, box, heatmap, pair."
                ),
                'wrong': 'report_chart(bars, m[:, "X"], m[:, "Y"])',
                'right': 'report_chart(bar, m[:, "X"], m[:, "Y"])',
                'explanation': (
                    "Тип указывается ПЕРВЫМ аргументом, БЕЗ кавычек:\n"
                    "     bar, line, pie, hist, scatter, box, heatmap, pair"
                ),
                'variants': [
                    'report_chart(bar, m[:, "X"], m[:, "Y"])',
                    'report_chart(line, m[:, "X"], m[:, "Y"])',
                    'report_chart(hist, m[:, "X"], bins 10)',
                ],
            },
            'REPORT_CHART_BAD_SYNTAX': {
                'message': (
                    "report_chart: неверный синтаксис.\n"
                    "  Нужны тип графика и данные X."
                ),
                'wrong': 'report_chart(bar)',
                'right': 'report_chart(bar, m[:, "X"], m[:, "Y"])',
                'explanation': (
                    "Структура:\n"
                    "  report_chart(тип, x)\n"
                    "  report_chart(тип, x, y)\n"
                    "  report_chart(тип, x, y, опции...)"
                ),
                'variants': [
                    'report_chart(bar, m[:, "X"], m[:, "Y"])',
                    'report_chart(hist, m[:, "X"], bins 10)',
                ],
            },
            'REPORT_CHART_NEED_Y': {
                'message': (
                    "report_chart: для этого типа графика нужны данные Y."
                ),
                'wrong': 'report_chart(bar, m[:, "X"])',
                'right': 'report_chart(bar, m[:, "X"], m[:, "Y"])',
                'explanation': (
                    "Типы bar, line, pie, scatter, box требуют ДВА аргумента:\n"
                    "     report_chart(bar, x, y)\n"
                    "     report_chart(line, x, y)\n"
                    "\n"
                    "Типы hist, heatmap, pair — только X:\n"
                    "     report_chart(hist, x, bins N)\n"
                    "     report_chart(heatmap, matrix)"
                ),
                'variants': [
                    'report_chart(bar, m[:, "X"], m[:, "Y"])',
                    'report_chart(line, m[:, "X"], m[:, "Y"])',
                    'report_chart(hist, m[:, "X"], bins 10)',
                ],
            },
            'REPORT_CHART_BAD_OPTION': {
                'message': (
                    "report_chart: неверная опция.\n"
                    "  Допустимо: title, xlabel, ylabel, color, "
                    "save, bins, plotly, static."
                ),
                'wrong': 'report_chart(bar, m[:, "X"], m[:, "Y"], colour "red")',
                'right': 'report_chart(bar, m[:, "X"], m[:, "Y"], color "red")',
                'explanation': (
                    "Только эти опции:\n"
                    "     title \"...\"\n"
                    "     xlabel \"...\"\n"
                    "     ylabel \"...\"\n"
                    "     color \"...\"\n"
                    "     save \"...\"\n"
                    "     bins N\n"
                    "     plotly / static"
                ),
                'variants': [
                    'report_chart(bar, m[:, "X"], m[:, "Y"], title "Заголовок")',
                    'report_chart(bar, m[:, "X"], m[:, "Y"], color "red")',
                ],
            },
        },
    },

    # ============================================================
    # REPORT_SAVE
    # ============================================================
    'report_save': {
        'name': 'report_save',
        'category': 'report',
        'signature': 'report_save([show])',
        'description': (
            'Сохраняет HTML-отчёт.\n'
            '  • Без аргумента — сохраняет и открывает браузер (первый раз).\n'
            '  • report_save(true) — всегда открыть.\n'
            '  • report_save(false) — только сохранить.'
        ),
        'examples': [
            'report_save()',
            'report_save(true)',
            'report_save(false)',
        ],
        'errors': {
            'REPORT_SAVE_BAD_SHOW': {
                'message': (
                    "report_save: аргумент должен быть true или false."
                ),
                'wrong': 'report_save("yes")',
                'right': 'report_save(true)',
                'explanation': (
                    "Аргумент report_save — boolean:\n"
                    "     report_save()         — авто\n"
                    "     report_save(true)     — открыть\n"
                    "     report_save(false)    — только сохранить"
                ),
                'variants': [
                    'report_save()',
                    'report_save(true)',
                    'report_save(false)',
                ],
            },
        },
    },

    # ============================================================
    # REPORT_SHOW
    # ============================================================
    'report_show': {
        'name': 'report_show',
        'category': 'report',
        'signature': 'report_show()',
        'description': (
            'Открывает последний сохранённый HTML в браузере.'
        ),
        'examples': [
            'report_show()',
        ],
        'errors': {},
    },

    # ============================================================
    # REPORT_SAVE_PDF
    # ============================================================
    'report_save_pdf': {
        'name': 'report_save_pdf',
        'category': 'report',
        'signature': 'report_save_pdf("file.pdf")',
        'description': (
            'Сохраняет отчёт в PDF через Playwright.\n'
            '  • Требует: pip install playwright\n'
            '  • Затем:   python -m playwright install chromium\n'
            '  • Если Playwright нет — откроет HTML в браузере\n'
            '    и подскажет Ctrl+P.'
        ),
        'examples': [
            'report_save_pdf("report.pdf")',
        ],
        'errors': {
            'REPORT_SAVE_PDF_BAD_PATH': {
                'message': (
                    "report_save_pdf: путь к PDF должен быть строкой."
                ),
                'wrong': 'report_save_pdf(42)',
                'right': 'report_save_pdf("report.pdf")',
                'explanation': (
                    "Путь к PDF — строка в кавычках:\n"
                    "     report_save_pdf(\"report.pdf\")\n"
                    "     report_save_pdf(\"C:\\\\reports\\\\report.pdf\")"
                ),
                'variants': [
                    'report_save_pdf("report.pdf")',
                    'report_save_pdf("C:\\reports\\report.pdf")',
                ],
            },
        },
    },
}


EN = {
    'report': {
        'name': 'report',
        'category': 'report',
        'signature': 'report("Title", "file.html")',
        'description': (
            'Starts a report — HTML with interactive Plotly charts.\n'
            '  • Called ONCE at the beginning.\n'
            '  • Then — report_section, report_text, report_table,\n'
            '    report_chart.\n'
            '  • report_save() — saves HTML.\n'
            '  • report is a STATEMENT, no assignment needed.\n'
            '  • On first report_save() the report opens in a browser.'
        ),
        'examples': [
            'report("Sales analysis", "report.html")',
            'report("Report", "report.html")',
        ],
        'errors': {
            'REPORT_BAD_SYNTAX': {
                'message': (
                    "report: invalid syntax.\n"
                    "  Need a title and a path to an HTML file."
                ),
                'wrong': 'report("Analysis")',
                'right': 'report("Analysis", "report.html")',
                'explanation': (
                    "report takes TWO arguments:\n"
                    "  1. Title — quoted string\n"
                    "  2. HTML path — quoted string\n"
                    "\n"
                    "Structure:\n"
                    "  report(\"Title\", \"file.html\")"
                ),
                'variants': [
                    'report("Sales analysis", "report.html")',
                    'report("Report", "report_2025.html")',
                ],
            },
            'REPORT_NEED_TITLE': {
                'message': "report: title is required.",
                'wrong': 'report()',
                'right': 'report("Analysis", "report.html")',
                'explanation': (
                    "First argument is the TITLE of the report.\n"
                    "It is a quoted string.\n"
                    "\n"
                    "Correct:\n"
                    "  report(\"Sales analysis\", \"report.html\")"
                ),
                'variants': [
                    'report("Sales analysis", "report.html")',
                    'report("Report 2025", "report_2025.html")',
                ],
            },
            'REPORT_NEED_PATH': {
                'message': "report: path to the HTML file is required.",
                'wrong': 'report("Analysis")',
                'right': 'report("Analysis", "report.html")',
                'explanation': (
                    "Second argument is the PATH to the HTML file.\n"
                    "It is a quoted string.\n"
                    "\n"
                    "Correct:\n"
                    "  report(\"Analysis\", \"report.html\")\n"
                    "  report(\"Report\", \"C:\\\\reports\\\\report.html\")"
                ),
                'variants': [
                    'report("Analysis", "report.html")',
                    'report("Report", "C:\\reports\\report.html")',
                ],
            },
            'REPORT_NOT_STARTED': {
                'message': (
                    "report: report not started.\n"
                    "  First call report(\"Title\", \"file.html\")"
                ),
                'wrong': 'report_save()',
                'right': (
                    'report("Analysis", "report.html")\n'
                    'report_save()'
                ),
                'explanation': (
                    "Functions report_section, report_text, report_table,\n"
                    "report_chart, report_save, report_show, report_save_pdf\n"
                    "work ONLY after report().\n"
                    "\n"
                    "Incorrect:\n"
                    "     report_save()\n"
                    "\n"
                    "Correct:\n"
                    "     report(\"Analysis\", \"report.html\")\n"
                    "     report_save()"
                ),
                'variants': [
                    'report("Analysis", "report.html")\nreport_save()',
                    'report("Report", "report.html")\nreport_show()',
                ],
            },
            'REPORT_SAVE_ERROR': {
                'message': "report_save: failed to save HTML file.",
                'wrong': 'report_save()  # path points to a locked folder',
                'right': 'report_save()  # path is writable',
                'explanation': (
                    "Check:\n"
                    "  • folder exists\n"
                    "  • write permission\n"
                    "  • file is not locked by another application"
                ),
                'variants': [
                    'report("Analysis", "C:\\reports\\report.html")\nreport_save()',
                    'report("Analysis", "report.html")\nreport_save()',
                ],
            },
            'REPORT_PLAYWRIGHT_MISSING': {
                'message': (
                    "report_save_pdf: Playwright is not installed.\n"
                    "  Install: pip install playwright\n"
                    "  Then:    python -m playwright install chromium"
                ),
                'wrong': 'report_save_pdf("report.pdf")',
                'right': (
                    'pip install playwright\n'
                    'python -m playwright install chromium\n'
                    'report_save_pdf("report.pdf")'
                ),
                'explanation': (
                    "report_save_pdf uses Playwright to render HTML → PDF.\n"
                    "\n"
                    "If Playwright is not installed — the browser opens\n"
                    "with the ready HTML, and PDF can be saved manually:\n"
                    "     Ctrl+P → Save as PDF"
                ),
                'variants': [
                    'pip install playwright\npython -m playwright install chromium\nreport_save_pdf("report.pdf")',
                    'report_save()  # then Ctrl+P in browser',
                ],
            },
            'REPORT_SAVE_PDF_ERROR': {
                'message': "report_save_pdf: failed to save PDF.",
                'wrong': 'report_save_pdf("C:\\no_folder\\report.pdf")',
                'right': 'report_save_pdf("report.pdf")',
                'explanation': (
                    "Check:\n"
                    "  • folder exists\n"
                    "  • write permission\n"
                    "  • chromium is installed for Playwright"
                ),
                'variants': [
                    'report_save_pdf("report.pdf")',
                    'report_save_pdf("C:\\reports\\report.pdf")',
                ],
            },
        },
    },

    # REPORT_SECTION
    'report_section': {
        'name': 'report_section',
        'category': 'report',
        'signature': 'report_section("Title")',
        'description': (
            'Adds a section (heading) to the report.\n'
            '  • Called between report() and report_save().'
        ),
        'examples': [
            'report_section("1. General info")',
            'report_section("2. Charts")',
        ],
        'errors': {
            'REPORT_SECTION_BAD_SYNTAX': {
                'message': "report_section: heading is required.",
                'wrong': 'report_section()',
                'right': 'report_section("1. General info")',
                'explanation': (
                    "report_section takes ONE argument:\n"
                    "  • Heading — quoted string"
                ),
                'variants': [
                    'report_section("1. General info")',
                    'report_section("2. Charts")',
                ],
            },
        },
    },

    # REPORT_TEXT
    'report_text': {
        'name': 'report_text',
        'category': 'report',
        'signature': 'report_text("Text")',
        'description': (
            'Adds a paragraph of text.\n'
            '  • Called between report() and report_save().'
        ),
        'examples': [
            'report_text("Generated automatically.")',
            'report_text("Total sales: 100000")',
        ],
        'errors': {
            'REPORT_TEXT_BAD_SYNTAX': {
                'message': "report_text: text is required.",
                'wrong': 'report_text()',
                'right': 'report_text("Text")',
                'explanation': (
                    "report_text takes ONE argument:\n"
                    "  • Text — quoted string"
                ),
                'variants': [
                    'report_text("Generated automatically.")',
                    'report_text("Total: " + to_string(total))',
                ],
            },
        },
    },

    # REPORT_TABLE
    'report_table': {
        'name': 'report_table',
        'category': 'report',
        'signature': 'report_table(data [, title "Title"])',
        'description': (
            'Adds a table to the report.\n'
            '  • Data — matrix or slice.\n'
            '  • title — optional heading.'
        ),
        'examples': [
            'report_table(m)',
            'report_table(m, title "Sales table")',
        ],
        'errors': {
            'REPORT_TABLE_BAD_SYNTAX': {
                'message': "report_table: data (matrix) is required.",
                'wrong': 'report_table()',
                'right': 'report_table(m)',
                'explanation': (
                    "report_table takes 1 or 2 arguments:\n"
                    "  1. Data — matrix\n"
                    "  2. title \"...\" — optional"
                ),
                'variants': [
                    'report_table(m)',
                    'report_table(m, title "Sales table")',
                ],
            },
        },
    },

    # REPORT_CHART
    'report_chart': {
        'name': 'report_chart',
        'category': 'report',
        'signature': 'report_chart(kind, x [, y] [, options])',
        'description': (
            'Adds an interactive Plotly chart to the report.\n'
            '  • Kinds: bar, line, pie, hist, scatter, box, heatmap, pair.\n'
            '  • Options: title, xlabel, ylabel, color, bins, plotly, static.'
        ),
        'examples': [
            'report_chart(bar, m[:, "Dept"], m[:, "Salary"], title "Salaries")',
            'report_chart(line, m[:, "Month"], m[:, "Sales"])',
            'report_chart(hist, m[:, "Age"], bins 10)',
        ],
        'errors': {
            'REPORT_CHART_BAD_KIND': {
                'message': (
                    "report_chart: invalid chart type.\n"
                    "  Allowed: bar, line, pie, hist, scatter, box, heatmap, pair."
                ),
                'wrong': 'report_chart(bars, m[:, "X"], m[:, "Y"])',
                'right': 'report_chart(bar, m[:, "X"], m[:, "Y"])',
                'explanation': (
                    "Kind is the FIRST argument, WITHOUT quotes:\n"
                    "     bar, line, pie, hist, scatter, box, heatmap, pair"
                ),
                'variants': [
                    'report_chart(bar, m[:, "X"], m[:, "Y"])',
                    'report_chart(line, m[:, "X"], m[:, "Y"])',
                    'report_chart(hist, m[:, "X"], bins 10)',
                ],
            },
            'REPORT_CHART_BAD_SYNTAX': {
                'message': (
                    "report_chart: invalid syntax.\n"
                    "  Need a kind and X data."
                ),
                'wrong': 'report_chart(bar)',
                'right': 'report_chart(bar, m[:, "X"], m[:, "Y"])',
                'explanation': (
                    "Structure:\n"
                    "  report_chart(kind, x)\n"
                    "  report_chart(kind, x, y)\n"
                    "  report_chart(kind, x, y, options...)"
                ),
                'variants': [
                    'report_chart(bar, m[:, "X"], m[:, "Y"])',
                    'report_chart(hist, m[:, "X"], bins 10)',
                ],
            },
            'REPORT_CHART_NEED_Y': {
                'message': (
                    "report_chart: Y data is required for this kind."
                ),
                'wrong': 'report_chart(bar, m[:, "X"])',
                'right': 'report_chart(bar, m[:, "X"], m[:, "Y"])',
                'explanation': (
                    "Kinds bar, line, pie, scatter, box require TWO args:\n"
                    "     report_chart(bar, x, y)\n"
                    "     report_chart(line, x, y)\n"
                    "\n"
                    "Kinds hist, heatmap, pair — only X:\n"
                    "     report_chart(hist, x, bins N)\n"
                    "     report_chart(heatmap, matrix)"
                ),
                'variants': [
                    'report_chart(bar, m[:, "X"], m[:, "Y"])',
                    'report_chart(line, m[:, "X"], m[:, "Y"])',
                    'report_chart(hist, m[:, "X"], bins 10)',
                ],
            },
            'REPORT_CHART_BAD_OPTION': {
                'message': (
                    "report_chart: invalid option.\n"
                    "  Allowed: title, xlabel, ylabel, color, "
                    "save, bins, plotly, static."
                ),
                'wrong': 'report_chart(bar, m[:, "X"], m[:, "Y"], colour "red")',
                'right': 'report_chart(bar, m[:, "X"], m[:, "Y"], color "red")',
                'explanation': (
                    "Only these options:\n"
                    "     title \"...\"\n"
                    "     xlabel \"...\"\n"
                    "     ylabel \"...\"\n"
                    "     color \"...\"\n"
                    "     save \"...\"\n"
                    "     bins N\n"
                    "     plotly / static"
                ),
                'variants': [
                    'report_chart(bar, m[:, "X"], m[:, "Y"], title "Title")',
                    'report_chart(bar, m[:, "X"], m[:, "Y"], color "red")',
                ],
            },
        },
    },

    # REPORT_SAVE
    'report_save': {
        'name': 'report_save',
        'category': 'report',
        'signature': 'report_save([show])',
        'description': (
            'Saves HTML report.\n'
            '  • No argument — saves and opens browser (first time).\n'
            '  • report_save(true) — always open.\n'
            '  • report_save(false) — save only.'
        ),
        'examples': [
            'report_save()',
            'report_save(true)',
            'report_save(false)',
        ],
        'errors': {
            'REPORT_SAVE_BAD_SHOW': {
                'message': (
                    "report_save: argument must be true or false."
                ),
                'wrong': 'report_save("yes")',
                'right': 'report_save(true)',
                'explanation': (
                    "report_save argument is boolean:\n"
                    "     report_save()         — auto\n"
                    "     report_save(true)     — open\n"
                    "     report_save(false)    — save only"
                ),
                'variants': [
                    'report_save()',
                    'report_save(true)',
                    'report_save(false)',
                ],
            },
        },
    },

    # REPORT_SHOW
    'report_show': {
        'name': 'report_show',
        'category': 'report',
        'signature': 'report_show()',
        'description': 'Opens the last saved HTML in browser.',
        'examples': ['report_show()'],
        'errors': {},
    },

    # REPORT_SAVE_PDF
    'report_save_pdf': {
        'name': 'report_save_pdf',
        'category': 'report',
        'signature': 'report_save_pdf("file.pdf")',
        'description': (
            'Saves the report as PDF via Playwright.\n'
            '  • Requires: pip install playwright\n'
            '  • Then:     python -m playwright install chromium\n'
            '  • If Playwright is not installed — opens HTML in browser\n'
            '    and suggests Ctrl+P.'
        ),
        'examples': [
            'report_save_pdf("report.pdf")',
        ],
        'errors': {
            'REPORT_SAVE_PDF_BAD_PATH': {
                'message': (
                    "report_save_pdf: PDF path must be a string."
                ),
                'wrong': 'report_save_pdf(42)',
                'right': 'report_save_pdf("report.pdf")',
                'explanation': (
                    "PDF path is a quoted string:\n"
                    "     report_save_pdf(\"report.pdf\")\n"
                    "     report_save_pdf(\"C:\\\\reports\\\\report.pdf\")"
                ),
                'variants': [
                    'report_save_pdf("report.pdf")',
                    'report_save_pdf("C:\\reports\\report.pdf")',
                ],
            },
        },
    },
}