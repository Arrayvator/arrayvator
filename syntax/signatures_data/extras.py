# syntax/signatures_data/extras.py
"""
Сигнатуры для функций, которые есть в AUTOCOMPLETE,
но не имеют отдельного модуля в signatures_data/.

Дополняет: control, files (Excel), chart, report, index, insertif,
joinvector, matrixmod, print, println.
"""

SIGNATURES = {
    # ============================================================
    # Управляющие конструкции
    # ============================================================
    'if': {
        'name': 'if',
        'category': 'control',
        'args': ['условие', 'then { ... }', 'else { ... } (опц.)'],
        'examples': [
            'if x > 5 then { print("X") }',
            'if x > 5 then { ... } else { ... }',
        ],
    },

    'while': {
        'name': 'while',
        'category': 'control',
        'args': ['условие', '{ ... }'],
        'examples': [
            'while i <= 5 { i = i + 1 }',
        ],
    },

    'for': {
        'name': 'for',
        'category': 'control',
        'args': ['переменная', '(начало:конец)', '{ ... }'],
        'examples': [
            'for i(1:5) { print(i) }',
            'for i(5:1) { print(i) }',
        ],
    },

    # ============================================================
    # Excel
    # ============================================================
    'openexcel': {
        'name': 'OpenExcel',
        'category': 'excel',
        'args': ['"file.xlsx"', 'лист (опц.)'],
        'examples': [
            'm = OpenExcel("data.xlsx")',
            'm = OpenExcel("data.xlsx", "Лист1")',
            'm = OpenExcel("data.xlsx", all)',
        ],
    },

    'saveexcel': {
        'name': 'SaveExcel',
        'category': 'excel',
        'args': ['данные', '"file.xlsx"', 'лист (опц.)'],
        'examples': [
            'SaveExcel(m, "out.xlsx")',
            'SaveExcel(m, "out.xlsx", "Лист1")',
        ],
    },

    'openexcelshow': {
        'name': 'OpenExcelShow',
        'category': 'excel',
        'args': ['all (опц.)'],
        'examples': ['m = OpenExcelShow()', 'm = OpenExcelShow(all)'],
    },

    'saveexcelshow': {
        'name': 'SaveExcelShow',
        'category': 'excel',
        'args': ['данные', 'имя листа (опц.)'],
        'examples': ['SaveExcelShow(m)'],
    },

    # ============================================================
    # Графики
    # ============================================================
    'chart': {
        'name': 'chart',
        'category': 'chart',
        'args': [
            'тип (bar | line | pie | hist | scatter | box | heatmap | pair)',
            'x',
            'y (опц.)',
            'опции (title, xlabel, ylabel, color, save, bins, plotly, static)',
        ],
        'examples': [
            'chart(bar, m[:, "Отдел"], m[:, "Зарплата"])',
            'chart(line, m[:, "Месяц"], m[:, "Продажи"])',
            'chart(hist, m[:, "Возраст"], bins 10)',
        ],
    },

    # ============================================================
    # Отчёты
    # ============================================================
    'report': {
        'name': 'report',
        'category': 'report',
        'args': ['"Заголовок"', '"file.html"'],
        'examples': ['report("Анализ", "report.html")'],
    },

    'report_section': {
        'name': 'report_section',
        'category': 'report',
        'args': ['"Заголовок"'],
        'examples': ['report_section("1. Общая информация")'],
    },

    'report_text': {
        'name': 'report_text',
        'category': 'report',
        'args': ['"Текст"'],
        'examples': ['report_text("Отчёт создан автоматически.")'],
    },

    'report_table': {
        'name': 'report_table',
        'category': 'report',
        'args': ['данные', 'title "..." (опц.)'],
        'examples': ['report_table(m, title "Зарплаты")'],
    },

    'report_chart': {
        'name': 'report_chart',
        'category': 'report',
        'args': ['тип', 'x', 'y', 'title "..." (опц.)'],
        'examples': [
            'report_chart(bar, m[:, "X"], m[:, "Y"], title "Сравнение")',
        ],
    },

    'report_save': {
        'name': 'report_save',
        'category': 'report',
        'args': ['show (опц.)'],
        'examples': ['report_save()', 'report_save(true)'],
    },

    'report_show': {
        'name': 'report_show',
        'category': 'report',
        'args': [],
        'examples': ['report_show()'],
    },

    'report_save_pdf': {
        'name': 'report_save_pdf',
        'category': 'report',
        'args': ['"file.pdf"'],
        'examples': ['report_save_pdf("report.pdf")'],
    },

    # ============================================================
    # Поиск (алиас find)
    # ============================================================
    'index': {
        'name': 'index',
        'category': 'search',
        'args': ['m[:, "X"] == "Y"', 'inside | ignore (опц.)'],
        'examples': ['r = index(m[:, "Имя"] == "Аня")'],
    },

    # ============================================================
    # Вставка по условию
    # ============================================================
    'insertif': {
        'name': 'insertif',
        'category': 'modify',
        'args': ['условие', 'before | after'],
        'examples': [
            'r = insertif(m[:, "Отдел"] == "IT", after)',
            'r = insertif(m[:, "Возраст"] > 25, before)',
        ],
    },

    # ============================================================
    # Соединение вектора
    # ============================================================
    'joinvector': {
        'name': 'joinvector',
        'category': 'string',
        'args': ['вектор', 'разделитель (опц.)'],
        'examples': [
            'r = joinvector(["a", "b", "c"], "-")',
            'r = joinvector(v)',
        ],
    },

    # ============================================================
    # Модификация строк
    # ============================================================
    'matrixmod': {
        'name': 'matrixmod',
        'category': 'modify',
        'args': [
            'таблица',
            'действие (delete | insert | duplicate | clear | keep | swap)',
            'N',
            'before | after (опц.)',
        ],
        'examples': [
            'r = matrixmod(m, delete, 2)',
            'r = matrixmod(m, insert, 2, before)',
            'r = matrixmod(m, duplicate, [2, 4], after)',
            'r = matrixmod(m, keep, [1, 3])',
            'r = matrixmod(m, swap, [2, 5])',
        ],
    },

    # ============================================================
    # Вывод
    # ============================================================
    'print': {
        'name': 'print',
        'category': 'output',
        'args': ['значение1 [, значение2, ...]'],
        'examples': [
            'print("Hello")',
            'print("Имя:", x, "Возраст:", y)',
        ],
    },

    'println': {
        'name': 'println',
        'category': 'output',
        'args': ['значение1 [, значение2, ...]'],
        'examples': [
            'println(v)',
            'println(m)',
        ],
    },
}