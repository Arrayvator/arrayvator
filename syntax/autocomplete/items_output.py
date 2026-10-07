# syntax/autocomplete/items_output.py
"""
Описания функций вывода: print, println, printshow.
"""

RU = {
    'print': {
        'signature': 'print(значение1 [, значение2, ...])',
        'description': 'Горизонтальный вывод.',
        'example': 'print("Имя:", x, "Возраст:", y)',
    },
    'println': {
        'signature': 'println(значение1 [, значение2, ...])',
        'description': 'Вертикальный вывод.',
        'example': 'println(v)',
    },
    'printshow': {
        'signature': 'printshow(данные [, "Заголовок"])',
        'description': 'Вывод в отдельном окне (виртуализация, 1 млн строк).',
        'example': 'printshow(m, "Результат")',
    },
}


EN = {
    'print': {
        'signature': 'print(value1 [, value2, ...])',
        'description': 'Horizontal output.',
        'example': 'print("Name:", x, "Age:", y)',
    },
    'println': {
        'signature': 'println(value1 [, value2, ...])',
        'description': 'Vertical output.',
        'example': 'println(v)',
    },
    'printshow': {
        'signature': 'printshow(data [, "Title"])',
        'description': 'Output in a separate window (virtualization, 1M rows).',
        'example': 'printshow(m, "Result")',
    },
}