# syntax/autocomplete/items_reports.py
"""
Описания функций отчётов.

Отчёт — это HTML-файл с таблицами и графиками Plotly.
СТРУКТУРА (одинаковая для всех report-функций):
    1. report("Название", "file.html")   — начать
    2. report_section("Заголовок")        — секция
       report_text("Текст")               — абзац
       report_table(m)                    — таблица
       report_chart(bar, x, y)            — график
    3. report_save()                      — сохранить HTML
    4. report_save_pdf("file.pdf")        — (опц.) PDF
"""


# ============================================================
# ОБЩАЯ СТРУКТУРА (одинаковая для всех функций)
# ============================================================
_STRUCTURE = (
    '📋 СТРУКТУРА ОТЧЁТА:\n'
    '\n'
    '  1. report("Название", "file.html")   — начать\n'
    '  2. report_section("Заголовок")        — секция\n'
    '     report_text("Текст")               — абзац\n'
    '     report_table(m)                    — таблица\n'
    '     report_chart(bar, x, y)            — график\n'
    '  3. report_save()                      — сохранить HTML\n'
    '  4. report_save_pdf("file.pdf")        — (опц.) PDF\n'
)


RU = {
    'report': {
        'signature': 'report("Название", "file.html")',
        'description': (
            '📊 НАЧАТЬ ОТЧЁТ — HTML с таблицами и графиками Plotly.\n'
            '\n'
            + _STRUCTURE +
            '\n'
            'ПРАВИЛА:\n'
            '  • report — ОПЕРАТОР, присваивание не нужно.\n'
            '  • Вызывается ОДИН РАЗ в начале.\n'
            '  • Все report_* работают ПОСЛЕ report().\n'
            '  • При первом report_save() откроется браузер.\n'
            '\n'
            'ТИПЫ ГРАФИКОВ (в report_chart):\n'
            '  bar, line, pie, hist, scatter, box, heatmap, pair.\n'
            '\n'
            'ОПЦИИ (в report_chart):\n'
            '  title "...", xlabel "...", ylabel "...", color "...",\n'
            '  save "...", bins N, plotly, static.'
        ),
        'example': (
            '# 1. Начать отчёт\n'
            'report("Анализ продаж", "report.html")\n'
            '\n'
            '# 2. Секция + данные\n'
            'report_section("1. Данные")\n'
            'report_table(m, title "Таблица")\n'
            '\n'
            '# 3. Секция + график\n'
            'report_section("2. График")\n'
            'report_chart(bar, m[:, "Товар"], m[:, "Продажи"])\n'
            '\n'
            '# 4. Сохранить HTML (откроется в браузере)\n'
            'report_save()\n'
            '\n'
            '# 5. (опц.) Сохранить PDF\n'
            '# report_save_pdf("report.pdf")'
        ),
        'matrix_example': (
            '# ДАНО:\n'
            '#\n'
            '#   m = ["Товар",  "Продажи";\n'
            '#        "Яблоки", 120;\n'
            '#        "Бананы", 80;\n'
            '#        "Груши",  150;\n'
            '#        "Сливы",  50]\n'
            '\n'
            '# ШАГ 1\n'
            'report("Продажи фруктов", "fruits.html")\n'
            '\n'
            '# ШАГ 2\n'
            'report_section("1. Данные")\n'
            'report_table(m, title "Таблица продаж")\n'
            '\n'
            '# ШАГ 3\n'
            'report_section("2. График")\n'
            'report_chart(bar, m[:, "Товар"], m[:, "Продажи"],\n'
            '             title "Продажи по товарам")\n'
            '\n'
            '# ШАГ 4 — откроется в браузере\n'
            'report_save()\n'
            '\n'
            '# РЕЗУЛЬТАТ:\n'
            '#   fruits.html — таблица + график.\n'
            '#   Для PDF: Ctrl+P в браузере.'
        ),
    },

    'report_section': {
        'signature': 'report_section("Заголовок")',
        'description': (
            '📑 СЕКЦИЯ отчёта  ← вы здесь\n'
            '\n'
            + _STRUCTURE +
            '\n'
            '  • Заголовок — строка в кавычках.\n'
            '  • Добавляет раздел в отчёт.\n'
            '  • Работает ПОСЛЕ report().'
        ),
        'example': (
            'report("Анализ", "report.html")\n'
            'report_section("1. Исходные данные")   # ← вы здесь\n'
            'report_table(m)\n'
            'report_save()'
        ),
        'matrix_example': (
            'report("Продажи", "sales.html")\n'
            'report_section("1. Данные")\n'
            'report_table(m)\n'
            'report_section("2. Графики")\n'
            'report_chart(bar, m[:, "X"], m[:, "Y"])\n'
            'report_save()'
        ),
    },

    'report_text': {
        'signature': 'report_text("Текст")',
        'description': (
            '📝 АБЗАЦ текста  ← вы здесь\n'
            '\n'
            + _STRUCTURE +
            '\n'
            '  • Текст — строка в кавычках.\n'
            '  • Работает ПОСЛЕ report().'
        ),
        'example': (
            'report("Анализ", "report.html")\n'
            'report_section("1. Данные")\n'
            'report_text("Продажи за 6 месяцев.")   # ← вы здесь\n'
            'report_table(m)\n'
            'report_save()'
        ),
        'matrix_example': (
            'report("Продажи", "sales.html")\n'
            'report_section("1. Итоги")\n'
            'report_text("Общая сумма: 400")\n'
            'report_table(m)\n'
            'report_save()'
        ),
    },

    'report_table': {
        'signature': 'report_table(данные [, title "Заголовок"])',
        'description': (
            '📋 ТАБЛИЦА в отчёте  ← вы здесь\n'
            '\n'
            + _STRUCTURE +
            '\n'
            '  • Данные — матрица или срез.\n'
            '  • title "..." — опциональный заголовок.\n'
            '  • Работает ПОСЛЕ report().'
        ),
        'example': (
            'report("Анализ", "report.html")\n'
            'report_section("1. Данные")\n'
            'report_table(m, title "Продажи")   # ← вы здесь\n'
            'report_save()'
        ),
        'matrix_example': (
            'report("Продажи", "sales.html")\n'
            'report_section("1. Данные")\n'
            'report_table(m, title "Таблица продаж")\n'
            'report_save()'
        ),
    },

    'report_chart': {
        'signature': 'report_chart(тип, x [, y] [, опции])',
        'description': (
            '📈 ГРАФИК Plotly  ← вы здесь\n'
            '\n'
            + _STRUCTURE +
            '\n'
            'ТИПЫ:\n'
            '  bar, line, pie, hist, scatter, box, heatmap, pair.\n'
            '\n'
            'ОПЦИИ:\n'
            '  title "...", xlabel "...", ylabel "...", color "...",\n'
            '  save "...", bins N, plotly, static.\n'
            '\n'
            '  • Работает ПОСЛЕ report().'
        ),
        'example': (
            'report("Анализ", "report.html")\n'
            'report_section("1. График")\n'
            'report_chart(bar, m[:, "Товар"], m[:, "Продажи"],\n'
            '             title "Продажи")   # ← вы здесь\n'
            'report_save()'
        ),
        'matrix_example': (
            'report("Продажи", "sales.html")\n'
            'report_section("1. Графики")\n'
            'report_chart(bar, m[:, "Товар"], m[:, "Продажи"],\n'
            '             title "Столбцы")\n'
            'report_chart(line, m[:, "Товар"], m[:, "Продажи"],\n'
            '             title "Линия")\n'
            'report_chart(pie, m[:, "Товар"], m[:, "Продажи"],\n'
            '             title "Доли")\n'
            'report_save()'
        ),
    },

    'report_save': {
        'signature': 'report_save([show])',
        'description': (
            '💾 СОХРАНИТЬ ОТЧЁТ в HTML  ← вы здесь\n'
            '\n'
            + _STRUCTURE +
            '\n'
            '  • Без аргумента:\n'
            '      – 1-й вызов в запуске — сохранить + открыть браузер\n'
            '      – дальше — только сохранить\n'
            '  • report_save(true)  — всегда открыть.\n'
            '  • report_save(false) — только сохранить.'
        ),
        'example': (
            'report("Анализ", "report.html")\n'
            'report_section("1. Данные")\n'
            'report_table(m)\n'
            'report_chart(bar, m[:, "X"], m[:, "Y"])\n'
            'report_save()   # ← вы здесь — сохранить + открыть'
        ),
        'matrix_example': (
            'report("Продажи", "sales.html")\n'
            'report_section("1. Данные")\n'
            'report_table(m)\n'
            'report_chart(bar, m[:, "Товар"], m[:, "Продажи"])\n'
            'report_save()\n'
            '\n'
            '# РЕЗУЛЬТАТ:\n'
            '#   sales.html — открывается в браузере.\n'
            '#   Ctrl+P → «Сохранить как PDF»'
        ),
    },

    'report_show': {
        'signature': 'report_show()',
        'description': (
            '🌐 ОТКРЫТЬ последний сохранённый HTML  ← вы здесь\n'
            '\n'
            + _STRUCTURE +
            '\n'
            '  • Работает ПОСЛЕ report_save().\n'
            '  • Открывает HTML в браузере.'
        ),
        'example': (
            'report("Анализ", "report.html")\n'
            'report_table(m)\n'
            'report_save(false)   # только сохранить\n'
            'report_show()        # ← вы здесь — открыть'
        ),
        'matrix_example': (
            'report("Продажи", "sales.html")\n'
            'report_table(m)\n'
            'report_chart(bar, m[:, "X"], m[:, "Y"])\n'
            'report_save(false)\n'
            'report_show()'
        ),
    },

    'report_save_pdf': {
        'signature': 'report_save_pdf("file.pdf")',
        'description': (
            '📄 СОХРАНИТЬ отчёт в PDF  ← вы здесь\n'
            '\n'
            + _STRUCTURE +
            '\n'
            '  • Работает ПОСЛЕ report() и report_save().\n'
            '  • Требует Playwright:\n'
            '      pip install playwright\n'
            '      python -m playwright install chromium\n'
            '  • Без Playwright: откроет HTML в браузере\n'
            '    и подскажет Ctrl+P → «Сохранить как PDF».'
        ),
        'example': (
            'report("Анализ", "report.html")\n'
            'report_section("1. Данные")\n'
            'report_table(m)\n'
            'report_chart(bar, m[:, "X"], m[:, "Y"])\n'
            'report_save(false)\n'
            'report_save_pdf("report.pdf")   # ← вы здесь'
        ),
        'matrix_example': (
            'report("Продажи", "sales.html")\n'
            'report_table(m)\n'
            'report_chart(bar, m[:, "Товар"], m[:, "Продажи"])\n'
            'report_save(false)\n'
            'report_save_pdf("sales.pdf")\n'
            '\n'
            '# РЕЗУЛЬТАТ:\n'
            '#   sales.html + sales.pdf'
        ),
    },
}


EN = {
    'report': {
        'signature': 'report("Title", "file.html")',
        'description': (
            '📊 START REPORT — HTML with tables and Plotly charts.\n'
            '\n'
            '📋 REPORT STRUCTURE:\n'
            '\n'
            '  1. report("Title", "file.html")      — start\n'
            '  2. report_section("Heading")         — section\n'
            '     report_text("Text")               — paragraph\n'
            '     report_table(m)                   — table\n'
            '     report_chart(bar, x, y)           — chart\n'
            '  3. report_save()                      — save HTML\n'
            '  4. report_save_pdf("file.pdf")        — (opt.) PDF\n'
            '\n'
            'RULES:\n'
            '  • report is a STATEMENT, no assignment needed.\n'
            '  • Called ONCE at the beginning.\n'
            '  • All report_* work AFTER report().\n'
            '  • On first report_save() browser opens.\n'
            '\n'
            'CHART KINDS (in report_chart):\n'
            '  bar, line, pie, hist, scatter, box, heatmap, pair.\n'
            '\n'
            'OPTIONS (in report_chart):\n'
            '  title "...", xlabel "...", ylabel "...", color "...",\n'
            '  save "...", bins N, plotly, static.'
        ),
        'example': (
            '# 1. Start report\n'
            'report("Sales analysis", "report.html")\n'
            '\n'
            '# 2. Section + data\n'
            'report_section("1. Data")\n'
            'report_table(m, title "Table")\n'
            '\n'
            '# 3. Section + chart\n'
            'report_section("2. Chart")\n'
            'report_chart(bar, m[:, "Product"], m[:, "Sales"])\n'
            '\n'
            '# 4. Save HTML (opens in browser)\n'
            'report_save()\n'
            '\n'
            '# 5. (opt.) Save PDF\n'
            '# report_save_pdf("report.pdf")'
        ),
        'matrix_example': (
            '# INPUT:\n'
            '#\n'
            '#   m = ["Product", "Sales";\n'
            '#        "Apples",  120;\n'
            '#        "Bananas", 80;\n'
            '#        "Pears",   150;\n'
            '#        "Plums",   50]\n'
            '\n'
            '# STEP 1\n'
            'report("Fruit sales", "fruits.html")\n'
            '\n'
            '# STEP 2\n'
            'report_section("1. Data")\n'
            'report_table(m, title "Sales table")\n'
            '\n'
            '# STEP 3\n'
            'report_section("2. Chart")\n'
            'report_chart(bar, m[:, "Product"], m[:, "Sales"],\n'
            '             title "Sales by product")\n'
            '\n'
            '# STEP 4 — opens in browser\n'
            'report_save()\n'
            '\n'
            '# RESULT:\n'
            '#   fruits.html — table + chart.\n'
            '#   For PDF: Ctrl+P in browser.'
        ),
    },

    'report_section': {
        'signature': 'report_section("Heading")',
        'description': (
            '📑 SECTION of report  ← you are here\n'
            '\n'
            '📋 REPORT STRUCTURE:\n'
            '\n'
            '  1. report("Title", "file.html")      — start\n'
            '  2. report_section("Heading")         — section       ← you\n'
            '     report_text("Text")               — paragraph\n'
            '     report_table(m)                   — table\n'
            '     report_chart(bar, x, y)           — chart\n'
            '  3. report_save()                      — save HTML\n'
            '  4. report_save_pdf("file.pdf")        — (opt.) PDF\n'
            '\n'
            '  • Heading — quoted string.\n'
            '  • Adds a section.\n'
            '  • Works AFTER report().'
        ),
        'example': (
            'report("Analysis", "report.html")\n'
            'report_section("1. Data")   # ← you are here\n'
            'report_table(m)\n'
            'report_save()'
        ),
        'matrix_example': (
            'report("Sales", "sales.html")\n'
            'report_section("1. Data")\n'
            'report_table(m)\n'
            'report_section("2. Charts")\n'
            'report_chart(bar, m[:, "X"], m[:, "Y"])\n'
            'report_save()'
        ),
    },

    'report_text': {
        'signature': 'report_text("Text")',
        'description': (
            '📝 PARAGRAPH of text  ← you are here\n'
            '\n'
            '📋 REPORT STRUCTURE:\n'
            '\n'
            '  1. report("Title", "file.html")      — start\n'
            '  2. report_section("Heading")         — section\n'
            '     report_text("Text")               — paragraph     ← you\n'
            '     report_table(m)                   — table\n'
            '     report_chart(bar, x, y)           — chart\n'
            '  3. report_save()                      — save HTML\n'
            '  4. report_save_pdf("file.pdf")        — (opt.) PDF\n'
            '\n'
            '  • Text — quoted string.\n'
            '  • Works AFTER report().'
        ),
        'example': (
            'report("Analysis", "report.html")\n'
            'report_section("1. Data")\n'
            'report_text("Sales over 6 months.")   # ← you are here\n'
            'report_table(m)\n'
            'report_save()'
        ),
        'matrix_example': (
            'report("Sales", "sales.html")\n'
            'report_section("1. Summary")\n'
            'report_text("Total: 400")\n'
            'report_table(m)\n'
            'report_save()'
        ),
    },

    'report_table': {
        'signature': 'report_table(data [, title "Title"])',
        'description': (
            '📋 TABLE in report  ← you are here\n'
            '\n'
            '📋 REPORT STRUCTURE:\n'
            '\n'
            '  1. report("Title", "file.html")      — start\n'
            '  2. report_section("Heading")         — section\n'
            '     report_text("Text")               — paragraph\n'
            '     report_table(m)                   — table         ← you\n'
            '     report_chart(bar, x, y)           — chart\n'
            '  3. report_save()                      — save HTML\n'
            '  4. report_save_pdf("file.pdf")        — (opt.) PDF\n'
            '\n'
            '  • Data — matrix or slice.\n'
            '  • title "..." — optional heading.\n'
            '  • Works AFTER report().'
        ),
        'example': (
            'report("Analysis", "report.html")\n'
            'report_section("1. Data")\n'
            'report_table(m, title "Sales")   # ← you are here\n'
            'report_save()'
        ),
        'matrix_example': (
            'report("Sales", "sales.html")\n'
            'report_section("1. Data")\n'
            'report_table(m, title "Sales table")\n'
            'report_save()'
        ),
    },

    'report_chart': {
        'signature': 'report_chart(kind, x [, y] [, options])',
        'description': (
            '📈 PLOTLY CHART  ← you are here\n'
            '\n'
            '📋 REPORT STRUCTURE:\n'
            '\n'
            '  1. report("Title", "file.html")      — start\n'
            '  2. report_section("Heading")         — section\n'
            '     report_text("Text")               — paragraph\n'
            '     report_table(m)                   — table\n'
            '     report_chart(bar, x, y)           — chart         ← you\n'
            '  3. report_save()                      — save HTML\n'
            '  4. report_save_pdf("file.pdf")        — (opt.) PDF\n'
            '\n'
            'KINDS:\n'
            '  bar, line, pie, hist, scatter, box, heatmap, pair.\n'
            '\n'
            'OPTIONS:\n'
            '  title "...", xlabel "...", ylabel "...", color "...",\n'
            '  save "...", bins N, plotly, static.\n'
            '\n'
            '  • Works AFTER report().'
        ),
        'example': (
            'report("Analysis", "report.html")\n'
            'report_section("1. Chart")\n'
            'report_chart(bar, m[:, "Product"], m[:, "Sales"],\n'
            '             title "Sales")   # ← you are here\n'
            'report_save()'
        ),
        'matrix_example': (
            'report("Sales", "sales.html")\n'
            'report_section("1. Charts")\n'
            'report_chart(bar, m[:, "Product"], m[:, "Sales"],\n'
            '             title "Bars")\n'
            'report_chart(line, m[:, "Product"], m[:, "Sales"],\n'
            '             title "Line")\n'
            'report_chart(pie, m[:, "Product"], m[:, "Sales"],\n'
            '             title "Share")\n'
            'report_save()'
        ),
    },

    'report_save': {
        'signature': 'report_save([show])',
        'description': (
            '💾 SAVE REPORT as HTML  ← you are here\n'
            '\n'
            '📋 REPORT STRUCTURE:\n'
            '\n'
            '  1. report("Title", "file.html")      — start\n'
            '  2. report_section("Heading")         — section\n'
            '     report_text("Text")               — paragraph\n'
            '     report_table(m)                   — table\n'
            '     report_chart(bar, x, y)           — chart\n'
            '  3. report_save()                      — save HTML     ← you\n'
            '  4. report_save_pdf("file.pdf")        — (opt.) PDF\n'
            '\n'
            '  • No argument:\n'
            '      – 1st call in run — save + open browser\n'
            '      – then — save only\n'
            '  • report_save(true)  — always open.\n'
            '  • report_save(false) — save only.'
        ),
        'example': (
            'report("Analysis", "report.html")\n'
            'report_section("1. Data")\n'
            'report_table(m)\n'
            'report_chart(bar, m[:, "X"], m[:, "Y"])\n'
            'report_save()   # ← you are here — save + open'
        ),
        'matrix_example': (
            'report("Sales", "sales.html")\n'
            'report_section("1. Data")\n'
            'report_table(m)\n'
            'report_chart(bar, m[:, "Product"], m[:, "Sales"])\n'
            'report_save()\n'
            '\n'
            '# RESULT:\n'
            '#   sales.html — opens in browser.\n'
            '#   Ctrl+P → Save as PDF'
        ),
    },

    'report_show': {
        'signature': 'report_show()',
        'description': (
            '🌐 OPEN last saved HTML  ← you are here\n'
            '\n'
            '📋 REPORT STRUCTURE:\n'
            '\n'
            '  1. report("Title", "file.html")      — start\n'
            '  2. report_section("Heading")         — section\n'
            '     report_text("Text")               — paragraph\n'
            '     report_table(m)                   — table\n'
            '     report_chart(bar, x, y)           — chart\n'
            '  3. report_save()                      — save HTML\n'
            '  4. report_show()                      — open in browser  ← you\n'
            '\n'
            '  • Works AFTER report_save().'
        ),
        'example': (
            'report("Analysis", "report.html")\n'
            'report_table(m)\n'
            'report_save(false)   # save only\n'
            'report_show()        # ← you are here — open'
        ),
        'matrix_example': (
            'report("Sales", "sales.html")\n'
            'report_table(m)\n'
            'report_chart(bar, m[:, "X"], m[:, "Y"])\n'
            'report_save(false)\n'
            'report_show()'
        ),
    },

    'report_save_pdf': {
        'signature': 'report_save_pdf("file.pdf")',
        'description': (
            '📄 SAVE REPORT as PDF  ← you are here\n'
            '\n'
            '📋 REPORT STRUCTURE:\n'
            '\n'
            '  1. report("Title", "file.html")      — start\n'
            '  2. report_section("Heading")         — section\n'
            '     report_text("Text")               — paragraph\n'
            '     report_table(m)                   — table\n'
            '     report_chart(bar, x, y)           — chart\n'
            '  3. report_save()                      — save HTML\n'
            '  4. report_save_pdf("file.pdf")        — (opt.) PDF   ← you\n'
            '\n'
            '  • Works AFTER report() and report_save().\n'
            '  • Requires Playwright:\n'
            '      pip install playwright\n'
            '      python -m playwright install chromium\n'
            '  • Without Playwright: opens HTML in browser\n'
            '    and suggests Ctrl+P → Save as PDF.'
        ),
        'example': (
            'report("Analysis", "report.html")\n'
            'report_section("1. Data")\n'
            'report_table(m)\n'
            'report_chart(bar, m[:, "X"], m[:, "Y"])\n'
            'report_save(false)\n'
            'report_save_pdf("report.pdf")   # ← you are here'
        ),
        'matrix_example': (
            'report("Sales", "sales.html")\n'
            'report_table(m)\n'
            'report_chart(bar, m[:, "Product"], m[:, "Sales"])\n'
            'report_save(false)\n'
            'report_save_pdf("sales.pdf")\n'
            '\n'
            '# RESULT:\n'
            '#   sales.html + sales.pdf'
        ),
    },
}