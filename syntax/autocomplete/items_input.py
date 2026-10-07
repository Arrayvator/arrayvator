# syntax/autocomplete/items_input.py
"""
Описания функций ввода: InputShow, InputShowForm, InputListShow.
"""

RU = {
    'InputShow': {
        'signature': 'InputShow([подпись] [, "матрица"])',
        'description': 'Окно ввода одного значения.',
        'example': 'x = InputShow("Введите число:")',
    },
    'InputShowForm': {
        'signature': 'InputShowForm("Заголовок", "Поле1", ...)',
        'description': 'Форма с несколькими полями.',
        'example': 'data = InputShowForm("Анкета", "Имя", "Возраст")',
    },
    'InputListShow': {
        'signature': 'InputListShow([title: "..."], "подпись1", цель1, ...)',
        'description': 'Последовательный ввод в несколько целей.',
        'example': 'a = vector(3)\nInputListShow("A:", a[1], "B:", a[2])',
    },
}


EN = {
    'InputShow': {
        'signature': 'InputShow([prompt] [, "matrix"])',
        'description': 'Dialog for entering a single value.',
        'example': 'x = InputShow("Enter a number:")',
    },
    'InputShowForm': {
        'signature': 'InputShowForm("Title", "Field1", ...)',
        'description': 'Form with multiple input fields.',
        'example': 'data = InputShowForm("Form", "Name", "Age")',
    },
    'InputListShow': {
        'signature': 'InputListShow([title: "..."], "label1", target1, ...)',
        'description': 'Sequential input into multiple targets.',
        'example': 'a = vector(3)\nInputListShow("A:", a[1], "B:", a[2])',
    },
}