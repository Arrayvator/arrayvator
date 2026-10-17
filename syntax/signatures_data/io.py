# syntax/signatures_data/io.py
"""
Сигнатуры: ввод, вывод, логирование.
"""

SIGNATURES = {
    'inputshow': {
        'name': 'InputShow',
        'category': 'input',
        'args': ['подпись (опц.)', '"матрица" для многострочного ввода'],
        'examples': [
            'x = InputShow("Введите число:")',
            'x = InputShow()',
            'm = InputShow("Матрица:", "матрица")',
        ],
    },

    'inputshowform': {
        'name': 'InputShowForm',
        'category': 'input',
        'args': ['"Заголовок"', '"Поле1"', '"Поле2"', '...'],
        'examples': [
            'data = InputShowForm("Анкета", "Имя", "Возраст", "Город")',
        ],
    },

    'inputlistshow': {
        'name': 'InputListShow',
        'category': 'input',
        'args': [
            'title: "Заголовок" (опц.)',
            '"подпись1", цель1',
            '"подпись2", цель2',
        ],
        'examples': [
            'InputListShow(title: "Анкета", "Имя:", x, "Возраст:", y)',
            'a = vector(3)\nInputListShow("A:", a[1], "B:", a[2], "C:", a[3])',
        ],
    },

    # ============================================================
    # INPUTINMATRIX — НОВОЕ
    # ============================================================
    'inputinmatrix': {
        'name': 'InputInMatrix',
        'category': 'input',
        'args': [
            'матрица',
            '"Заголовок окна" (опц.)',
            'количество строк контекста (опц., по умолчанию 10)',
        ],
        'examples': [
            'm = InputInMatrix(m)',
            'm = InputInMatrix(m, "Сотрудники")',
            'm = InputInMatrix(m, "Сотрудники", 5)',
            'm = InputInMatrix(m, "Товары", 20)',
        ],
    },

    'printshow': {
        'name': 'printshow',
        'category': 'output',
        'args': ['данные', 'заголовок (опц.)'],
        'examples': [
            'printshow(m)',
            'printshow(m, "Результат")',
        ],
    },

    'logtofile': {
        'name': 'LogToFile',
        'category': 'logging',
        'args': ['"путь.txt"', '"all" | "matrix" | "summary" (опц.)'],
        'examples': [
            'LogToFile("log.txt")',
            'LogToFile("log.txt", "matrix")',
        ],
    },

    'logoff': {
        'name': 'LogOff',
        'category': 'logging',
        'args': [],
        'examples': ['LogOff()'],
    },
}