# syntax/autocomplete/items_case.py
"""
Описания функций условного преобразования: case, applyif.
"""

RU = {
    'case': {
        'signature': (
            'case(m[:, "X"], when условие then значение, ... '
            '[, else значение])'
        ),
        'description': (
            '🔀 УСЛОВНОЕ ПРЕОБРАЗОВАНИЕ (аналог SQL CASE WHEN)\n'
            '\n'
            'ЗАЧЕМ НУЖНА:\n'
            '  • Заменить значения по нескольким условиям.\n'
            '  • Классика: "категория по возрасту", "статус по сумме".\n'
            '  • Аналог if-else, но для целого столбца за раз.\n'
            '\n'
            'МНЕМОНИКА:\n'
            '     case( столбец ,\n'
            '           when условие1 then значение1 ,\n'
            '           when условие2 then значение2 ,\n'
            '           ... ,\n'
            '           else значение_по_умолчанию )\n'
            '\n'
            'ОПЕРАТОРЫ В when:\n'
            '  • <   меньше\n'
            '  • >   больше\n'
            '  • <=  меньше или равно\n'
            '  • >=  больше или равно\n'
            '  • ==  равно\n'
            '  • !=  не равно\n'
            '\n'
            'ЧТО МОЖНО В then / else:\n'
            '  • строка — "Дитя", "IT"\n'
            '  • число — 5, 3.14\n'
            '  • boolean — true, false\n'
            '  • None\n'
            '  • другой столбец — m[:, "Резерв"]\n'
            '  • функция — round(m[:, "X"] * 1.2, 2)\n'
            '\n'
            'КАКИЕ ЗАДАЧИ РЕШАЕТ:\n'
            '  • Категоризация по возрасту / сумме / дате.\n'
            '  • Замена значений по условию.\n'
            '  • Создание новых групп из числовых значений.\n'
            '  • Замена None на "—".\n'
            '\n'
            'ПРАВИЛА:\n'
            '  • Условия проверяются СВЕРХУ ВНИЗ.\n'
            '  • Первое подходящее условие выигрывает.\n'
            '  • Хотя бы один when обязателен.\n'
            '  • else — опционален (без него → None).\n'
            '  • else — последний, не более одного.\n'
            '  • Возвращает ВЕКТОР.\n'
            '  • НЕ мутирует исходную матрицу.'
        ),
        'example': (
            '# Простая категоризация\n'
            'r = case(m[:, "Возраст"],\n'
            '         when < 18 then "Дитя",\n'
            '         when < 30 then "Молодой",\n'
            '         else "Взрослый")\n'
            '\n'
            '# Присваивание в столбец\n'
            'm[:, "Категория"] = case(m[:, "Возраст"],\n'
            '                          when < 18 then "Дитя",\n'
            '                          else "Взрослый")'
        ),
        'matrix_example': (
            '# ДАНО:\n'
            '#\n'
            '#   m = ["Имя",   "Возраст";\n'
            '#        "Аня",   25;\n'
            '#        "Боб",   15;\n'
            '#        "Света", 32;\n'
            '#        "Гена",  41]\n'
            '\n'
            '# ЗАДАЧА: разделить на категории по возрасту\n'
            'r = case(m[:, "Возраст"],\n'
            '         when < 18 then "Дитя",\n'
            '         when < 30 then "Молодой",\n'
            '         else "Взрослый")\n'
            'print(r)\n'
            '\n'
            '# ВЫВОД (вектор категорий):\n'
            '#\n'
            '#   ["Молодой", "Дитя", "Взрослый", "Взрослый"]\n'
            '\n'
            '# Присваивание результата в столбец:\n'
            'm = addcolumn(m, "Категория", r)\n'
            'print(m)\n'
            '\n'
            '# ВЫВОД:\n'
            '#\n'
            '#   Имя    Возраст  Категория\n'
            '#   Аня    25       Молодой\n'
            '#   Боб    15       Дитя\n'
            '#   Света  32       Взрослый\n'
            '#   Гена   41       Взрослый'
        ),
    },

    'applyif': {
        'signature': 'applyif(условие, m[:, "X"] = значение)',
        'description': (
            '✏️ УСЛОВНОЕ ПРИСВАИВАНИЕ\n'
            '\n'
            'ЗАЧЕМ НУЖНА:\n'
            '  • Заменить значения ТОЛЬКО там, где условие истинно.\n'
            '  • Где условие ложно — оставить как было.\n'
            '  • Классика: "повысить оклад только IT-отделу".\n'
            '\n'
            'СИНТАКСИС:\n'
            '  applyif( условие , m[:, "X"] = новое_значение )\n'
            '\n'
            'ЧЕМ ОТЛИЧАЕТСЯ ОТ filterif + присваивание:\n'
            '  filterif  — вернёт только подходящие строки (потеряет остальные).\n'
            '  applyif   — вернёт ВСЕ строки, но подходящие — изменённые.\n'
            '\n'
            'КАКИЕ ЗАДАЧИ РЕШАЕТ:\n'
            '  • "Повысить зарплату всем IT на 10%".\n'
            '  • "Поставить VIP-статус клиентам с чеком > 100000".\n'
            '  • "Заполнить поле только для активных".\n'
            '  • Условная модификация одной колонки по другой.\n'
            '\n'
            'ПРАВИЛА:\n'
            '  • Возвращает НОВУЮ матрицу.\n'
            '  • НЕ мутирует исходную (нужно присвоить: m = applyif(...)).\n'
            '  • Можно писать в новый столбец: m[:, end+1].\n'
            '  • Работает с Matrix и DuckDB.'
        ),
        'example': (
            'r = applyif(m[:, "Отдел"] == "IT", m[:, "Статус"] = "VIP")\n'
            'm = applyif(m[:, "Отдел"] == "IT", m[:, "Статус"] = "VIP")'
        ),
        'matrix_example': (
            '# ДАНО:\n'
            '#\n'
            '#   m = ["Имя", "Отдел", "Статус";\n'
            '#        "Аня", "IT",    "";\n'
            '#        "Боб", "HR",    "";\n'
            '#        "Света","IT",   ""]\n'
            '\n'
            '# ЗАДАЧА: проставить "VIP" только сотрудникам IT\n'
            'r = applyif(m[:, "Отдел"] == "IT", m[:, "Статус"] = "VIP")\n'
            'print(r)\n'
            '\n'
            '# ВЫВОД (HR-сотрудник не тронут):\n'
            '#\n'
            '#   Имя    Отдел  Статус\n'
            '#   Аня    IT     VIP\n'
            '#   Боб    HR\n'
            '#   Света  IT     VIP'
        ),
    },
}


EN = {
    'case': {
        'signature': (
            'case(m[:, "X"], when condition then value, ... '
            '[, else value])'
        ),
        'description': (
            '🔀 CONDITIONAL TRANSFORMATION (SQL CASE WHEN analog)\n'
            '\n'
            'WHY NEEDED:\n'
            '  • Replace values by multiple conditions.\n'
            '  • Classic: "category by age", "status by amount".\n'
            '  • if-else analog, but for the whole column at once.\n'
            '\n'
            'MNEMONIC:\n'
            '     case( column ,\n'
            '           when condition1 then value1 ,\n'
            '           when condition2 then value2 ,\n'
            '           ... ,\n'
            '           else default_value )\n'
            '\n'
            'TASKS IT SOLVES:\n'
            '  • Categorization by age / amount / date.\n'
            '  • Replace values by condition.\n'
            '  • Create groups from numeric values.\n'
            '  • Replace None with "—".\n'
            '\n'
            'RULES:\n'
            '  • Conditions are checked TOP-DOWN.\n'
            '  • First match wins.\n'
            '  • At least one when is required.\n'
            '  • else — optional (without it → None).\n'
            '  • Returns a VECTOR.\n'
            '  • Does NOT mutate the source matrix.'
        ),
        'example': (
            'r = case(m[:, "Age"],\n'
            '         when < 18 then "Child",\n'
            '         when < 30 then "Young",\n'
            '         else "Adult")'
        ),
    },

    'applyif': {
        'signature': 'applyif(condition, m[:, "X"] = value)',
        'description': (
            '✏️ CONDITIONAL ASSIGNMENT\n'
            '\n'
            'WHY NEEDED:\n'
            '  • Replace values ONLY where condition is true.\n'
            '  • Where false — leave as is.\n'
            '  • Classic: "raise salary only for IT dept".\n'
            '\n'
            'TASKS IT SOLVES:\n'
            '  • "Raise salary 10% for all IT".\n'
            '  • "Set VIP status for clients with check > 100000".\n'
            '  • Conditional modification of one column by another.\n'
            '\n'
            'RULES:\n'
            '  • Returns a NEW matrix.\n'
            '  • Does NOT mutate the source (assign: m = applyif(...)).\n'
            '  • Can write into a new column: m[:, end+1].\n'
            '  • Works with Matrix and DuckDB.'
        ),
        'example': (
            'r = applyif(m[:, "Dept"] == "IT", m[:, "Status"] = "VIP")\n'
            'm = applyif(m[:, "Dept"] == "IT", m[:, "Status"] = "VIP")'
        ),
    },
}