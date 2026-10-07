# syntax/autocomplete/items_dedup.py
"""
Описания функций работы с дубликатами:
Unique, CountDistinct, ValueCounts, DeleteDuplicate.
"""

RU = {
    'Unique': {
        'signature': 'Unique(срез)',
        'description': (
            '🎯 УНИКАЛЬНЫЕ ЗНАЧЕНИЯ\n'
            '\n'
            'ЗАЧЕМ НУЖНА:\n'
            '  • Оставить только УНИКАЛЬНЫЕ строки по столбцу.\n'
            '  • Из дублей берётся ПЕРВОЕ появление.\n'
            '  • Классика: "какие отделы есть в компании".\n'
            '\n'
            'ДВА ВАРИАНТА:\n'
            '  • Unique(m[:, "X"]) — по значению в столбце X.\n'
            '  • Unique(m)          — по всей строке целиком.\n'
            '\n'
            'КАКИЕ ЗАДАЧИ РЕШАЕТ:\n'
            '  • "Уникальные отделы" / "Уникальные города".\n'
            '  • Список клиентов без повторов.\n'
            '  • Убрать дубли, оставив первое появление.\n'
            '\n'
            'ВАЖНО:\n'
            '  • Возвращает НОВУЮ матрицу.\n'
            '  • Исходная НЕ меняется.\n'
            '  • Порядок строк — по первому появлению.\n'
            '  • Работает с Matrix и DuckDB.'
        ),
        'example': (
            'r = Unique(m[:, "Отдел"])\n'
            'r = Unique(v)\n'
            'r = Unique(m)'
        ),
        'matrix_example': (
            '# ДАНО:\n'
            '#\n'
            '#   m = ["Отдел", "Имя", "Город";\n'
            '#        "IT",    "Аня", "Москва";\n'
            '#        "IT",    "Боб", "Питер";\n'
            '#        "HR",    "Света","Москва";\n'
            '#        "IT",    "Гена","Питер";\n'
            '#        "HR",    "Даша","Москва"]\n'
            '\n'
            '# ЗАДАЧА: уникальные отделы (первое появление)\n'
            'r = Unique(m[:, "Отдел"])\n'
            'print(r)\n'
            '\n'
            '# ВЫВОД:\n'
            '#\n'
            '#   Отдел  Имя    Город\n'
            '#   IT     Аня    Москва\n'
            '#   HR     Света  Москва'
        ),
    },

    'ValueCounts': {
        'signature': 'ValueCounts(срез)',
        'description': (
            '📊 ЧАСТОТНАЯ ТАБЛИЦА\n'
            '\n'
            'ЗАЧЕМ НУЖНА:\n'
            '  • Показать, СКОЛЬКО РАЗ каждое значение встречается.\n'
            '  • Аналог value_counts() в pandas.\n'
            '  • Классика: "сколько клиентов в каждом городе".\n'
            '\n'
            'РЕЗУЛЬТАТ:\n'
            '  • 2 столбца: Значение | Частота.\n'
            '  • Отсортирован по частоте (убывание).\n'
            '\n'
            'КАКИЕ ЗАДАЧИ РЕШАЕТ:\n'
            '  • Частотный анализ: топ значений.\n'
            '  • "Сколько раз каждый товар продан".\n'
            '  • Распределение клиентов по городам.\n'
            '  • Поиск редких категорий.\n'
            '\n'
            '  • Работает с Matrix и DuckDB.'
        ),
        'example': (
            'r = ValueCounts(m[:, "Отдел"])\n'
            'r = ValueCounts(v)'
        ),
        'matrix_example': (
            '# ДАНО:\n'
            '#\n'
            '#   m = ["Отдел";\n'
            '#        "IT";\n'
            '#        "IT";\n'
            '#        "HR";\n'
            '#        "IT"]\n'
            '\n'
            '# ЗАДАЧА: сколько раз каждый отдел встречается\n'
            'r = ValueCounts(m[:, "Отдел"])\n'
            'print(r)\n'
            '\n'
            '# ВЫВОД (сортировка по частоте):\n'
            '#\n'
            '#   Значение  Частота\n'
            '#   IT        3\n'
            '#   HR        1'
        ),
    },

    'DeleteDuplicate': {
        'signature': 'DeleteDuplicate(срез)',
        'description': (
            '🗑️ УДАЛИТЬ ДУБЛИКАТЫ\n'
            '\n'
            'ЗАЧЕМ НУЖНА:\n'
            '  • Полный аналог Unique.\n'
            '  • Оставляет ПЕРВОЕ появление.\n'
            '  • Более понятное имя для "удалить дубликаты".\n'
            '\n'
            'ОТЛИЧИЕ ОТ Unique:\n'
            '  • Технически ничего — делают одно и то же.\n'
            '  • Используйте DeleteDuplicate, когда хотите\n'
            '    подчеркнуть "удаление" (семантика).\n'
            '  • Используйте Unique, когда хотите подчеркнуть\n'
            '    "получить уникальные значения".\n'
            '\n'
            'КАКИЕ ЗАДАЧИ РЕШАЕТ:\n'
            '  • Убрать дубли из справочника.\n'
            '  • Оставить по одному клиенту.\n'
            '  • Список без повторов.\n'
            '\n'
            '  • Работает с Matrix и DuckDB.'
        ),
        'example': (
            'r = DeleteDuplicate(m[:, "Отдел"])\n'
            'r = DeleteDuplicate(v)'
        ),
        'matrix_example': (
            '# ДАНО:\n'
            '#\n'
            '#   m = ["Отдел";\n'
            '#        "IT";\n'
            '#        "IT";\n'
            '#        "HR";\n'
            '#        "IT"]\n'
            '\n'
            'r = DeleteDuplicate(m[:, "Отдел"])\n'
            'print(r)\n'
            '\n'
            '# ВЫВОД:\n'
            '#\n'
            '#   Отдел\n'
            '#   IT\n'
            '#   HR'
        ),
    },
}


EN = {
    'Unique': {
        'signature': 'Unique(slice)',
        'description': (
            '🎯 UNIQUE VALUES\n'
            '\n'
            'WHY NEEDED:\n'
            '  • Keep only UNIQUE rows by column.\n'
            '  • First appearance is taken.\n'
            '  • Classic: "which departments exist in the company".\n'
            '\n'
            'TWO VARIANTS:\n'
            '  • Unique(m[:, "X"]) — by value in column X.\n'
            '  • Unique(m)          — by whole row.\n'
            '\n'
            'TASKS IT SOLVES:\n'
            '  • "Unique departments" / "Unique cities".\n'
            '  • Client list without duplicates.\n'
            '  • Remove duplicates keeping first appearance.\n'
            '\n'
            '  • Returns a NEW matrix.\n'
            '  • Source is NOT changed.\n'
            '  • Row order — first appearance.\n'
            '  • Works with Matrix and DuckDB.'
        ),
        'example': (
            'r = Unique(m[:, "Department"])\n'
            'r = Unique(v)\n'
            'r = Unique(m)'
        ),
    },

    'ValueCounts': {
        'signature': 'ValueCounts(slice)',
        'description': (
            '📊 FREQUENCY TABLE\n'
            '\n'
            'WHY NEEDED:\n'
            '  • Show HOW MANY TIMES each value appears.\n'
            '  • Analog of value_counts() in pandas.\n'
            '  • Classic: "how many clients in each city".\n'
            '\n'
            'RESULT:\n'
            '  • 2 columns: Value | Frequency.\n'
            '  • Sorted by frequency (descending).\n'
            '\n'
            'TASKS IT SOLVES:\n'
            '  • Frequency analysis: top values.\n'
            '  • "How many times each product sold".\n'
            '  • Distribution of clients by city.\n'
            '  • Find rare categories.\n'
            '\n'
            '  • Works with Matrix and DuckDB.'
        ),
        'example': (
            'r = ValueCounts(m[:, "Department"])\n'
            'r = ValueCounts(v)'
        ),
    },

    'DeleteDuplicate': {
        'signature': 'DeleteDuplicate(slice)',
        'description': (
            '🗑️ REMOVE DUPLICATES\n'
            '\n'
            'WHY NEEDED:\n'
            '  • Full analog of Unique.\n'
            '  • Keeps FIRST appearance.\n'
            '  • Clearer name for "remove duplicates".\n'
            '\n'
            'HOW IT DIFFERS FROM Unique:\n'
            '  • Technically — nothing, they do the same.\n'
            '  • Use DeleteDuplicate for "removal" semantics.\n'
            '  • Use Unique for "get unique values" semantics.\n'
            '\n'
            '  • Works with Matrix and DuckDB.'
        ),
        'example': (
            'r = DeleteDuplicate(m[:, "Department"])\n'
            'r = DeleteDuplicate(v)'
        ),
    },
}