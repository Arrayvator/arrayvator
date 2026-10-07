# syntax/autocomplete/items_conditional.py
"""
Описания условных агрегатов:
sumif, countif, avgif, minif, maxif, medianif, countuniqueif, sumproduct.
"""

RU = {
    'sumif': {
        'signature': 'sumif(условие, срез) | sumif(by m[:, "X"], срез)',
        'description': (
            'Сумма по условию.\n'
            '  • Без by — скаляр: сумма по всей таблице с фильтром.\n'
            '  • С by — вектор: сумма группы для каждой строки.\n'
            'Работает с Matrix и DuckDB.'
        ),
        'example': (
            'r = sumif(m[:, "Отдел"] == "IT", m[:, "Зарплата"])   # 245000\n'
            'm = addcolumn(m, "Итого_по_отделу",\n'
            '              sumif(by m[:, "Отдел"], m[:, "Зарплата"]))'
        ),
        'matrix_example': (
            'm = ["Отдел", "Зарплата";\n'
            '     "IT", 80000;\n'
            '     "IT", 95000;\n'
            '     "HR", 60000]\n'
            'print(sumif(m[:, "Отдел"] == "IT", m[:, "Зарплата"]))\n'
            '# 175000'
        ),
    },
    'countif': {
        'signature': 'countif(условие) | countif(by m[:, "X"])',
        'description': (
            'Количество строк по условию.\n'
            '  • Без by — скаляр: сколько строк удовлетворяют.\n'
            '  • С by — вектор: количество строк в группе.\n'
            'Работает с Matrix и DuckDB.'
        ),
        'example': (
            'r = countif(m[:, "Отдел"] == "IT")   # 3\n'
            'm = addcolumn(m, "Всего_в_отделе",\n'
            '              countif(by m[:, "Отдел"]))'
        ),
    },
    'avgif': {
        'signature': 'avgif(условие, срез) | avgif(by m[:, "X"], срез)',
        'description': (
            'Среднее по условию.\n'
            '  • Без by — скаляр.\n'
            '  • С by — вектор: среднее группы для каждой строки.\n'
            'Работает с Matrix и DuckDB.'
        ),
        'example': (
            'r = avgif(m[:, "Отдел"] == "IT", m[:, "Зарплата"])   # 81666.67\n'
            'm = addcolumn(m, "Среднее_по_отделу",\n'
            '              avgif(by m[:, "Отдел"], m[:, "Зарплата"]))'
        ),
    },
    'minif': {
        'signature': 'minif(условие, срез) | minif(by m[:, "X"], срез)',
        'description': (
            'Минимум по условию.\n'
            '  • Без by — скаляр.\n'
            '  • С by — вектор: минимум группы для каждой строки.\n'
            'Работает с Matrix и DuckDB.'
        ),
        'example': (
            'r = minif(m[:, "Отдел"] == "IT", m[:, "Зарплата"])   # 70000\n'
            'm = addcolumn(m, "Мин_ЗП_отдела",\n'
            '              minif(by m[:, "Отдел"], m[:, "Зарплата"]))'
        ),
    },
    'maxif': {
        'signature': 'maxif(условие, срез) | maxif(by m[:, "X"], срез)',
        'description': (
            'Максимум по условию.\n'
            '  • Без by — скаляр.\n'
            '  • С by — вектор: максимум группы для каждой строки.\n'
            'Работает с Matrix и DuckDB.'
        ),
        'example': (
            'r = maxif(m[:, "Отдел"] == "IT", m[:, "Зарплата"])   # 95000\n'
            'm = addcolumn(m, "Макс_ЗП_отдела",\n'
            '              maxif(by m[:, "Отдел"], m[:, "Зарплата"]))'
        ),
    },
    'medianif': {
        'signature': 'medianif(условие, срез)',
        'description': (
            'Медиана по условию.\n'
            'Скаляр. Работает с Matrix и DuckDB.'
        ),
        'example': 'r = medianif(m[:, "Отдел"] == "IT", m[:, "Зарплата"])',
    },
    'countuniqueif': {
        'signature': 'countuniqueif(условие, срез)',
        'description': (
            'Количество уникальных значений по условию.\n'
            'Скаляр. Работает с Matrix и DuckDB.'
        ),
        'example': 'r = countuniqueif(m[:, "Отдел"] == "IT", m[:, "Город"])',
    },
    'sumproduct': {
        'signature': 'sumproduct(срез1, срез2 [, срез3, ...])',
        'description': (
            'Сумма произведений элементов по строкам.\n'
            'Скаляр. Работает с Matrix и DuckDB.'
        ),
        'example': 'r = sumproduct(m[:, "Цена"], m[:, "Количество"])',
    },
}


EN = {
    'sumif': {
        'signature': 'sumif(condition, slice) | sumif(by m[:, "X"], slice)',
        'description': (
            'Sum by condition.\n'
            '  • Without by — scalar: total with filter.\n'
            '  • With by — vector: group sum for each row.\n'
            'Works with Matrix and DuckDB.'
        ),
        'example': (
            'r = sumif(m[:, "Department"] == "IT", m[:, "Salary"])   # 245000\n'
            'm = addcolumn(m, "Total_by_dept",\n'
            '              sumif(by m[:, "Department"], m[:, "Salary"]))'
        ),
    },
    'countif': {
        'signature': 'countif(condition) | countif(by m[:, "X"])',
        'description': (
            'Count rows by condition.\n'
            '  • Without by — scalar.\n'
            '  • With by — vector: count per group.\n'
            'Works with Matrix and DuckDB.'
        ),
        'example': (
            'r = countif(m[:, "Department"] == "IT")   # 3\n'
            'm = addcolumn(m, "Total_in_dept",\n'
            '              countif(by m[:, "Department"]))'
        ),
    },
    'avgif': {
        'signature': 'avgif(condition, slice) | avgif(by m[:, "X"], slice)',
        'description': (
            'Average by condition.\n'
            '  • Without by — scalar.\n'
            '  • With by — vector: group average for each row.\n'
            'Works with Matrix and DuckDB.'
        ),
        'example': (
            'r = avgif(m[:, "Department"] == "IT", m[:, "Salary"])   # 81666.67\n'
            'm = addcolumn(m, "Avg_by_dept",\n'
            '              avgif(by m[:, "Department"], m[:, "Salary"]))'
        ),
    },
    'minif': {
        'signature': 'minif(condition, slice) | minif(by m[:, "X"], slice)',
        'description': (
            'Minimum by condition.\n'
            '  • Without by — scalar.\n'
            '  • With by — vector.\n'
            'Works with Matrix and DuckDB.'
        ),
        'example': (
            'r = minif(m[:, "Department"] == "IT", m[:, "Salary"])   # 70000\n'
            'm = addcolumn(m, "Min_by_dept",\n'
            '              minif(by m[:, "Department"], m[:, "Salary"]))'
        ),
    },
    'maxif': {
        'signature': 'maxif(condition, slice) | maxif(by m[:, "X"], slice)',
        'description': (
            'Maximum by condition.\n'
            '  • Without by — scalar.\n'
            '  • With by — vector.\n'
            'Works with Matrix and DuckDB.'
        ),
        'example': (
            'r = maxif(m[:, "Department"] == "IT", m[:, "Salary"])   # 95000\n'
            'm = addcolumn(m, "Max_by_dept",\n'
            '              maxif(by m[:, "Department"], m[:, "Salary"]))'
        ),
    },
    'medianif': {
        'signature': 'medianif(condition, slice)',
        'description': (
            'Median by condition.\n'
            'Scalar. Works with Matrix and DuckDB.'
        ),
        'example': 'r = medianif(m[:, "Department"] == "IT", m[:, "Salary"])',
    },
    'countuniqueif': {
        'signature': 'countuniqueif(condition, slice)',
        'description': (
            'Count unique values by condition.\n'
            'Scalar. Works with Matrix and DuckDB.'
        ),
        'example': 'r = countuniqueif(m[:, "Department"] == "IT", m[:, "City"])',
    },
    'sumproduct': {
        'signature': 'sumproduct(slice1, slice2 [, slice3, ...])',
        'description': (
            'Sum of row-wise products.\n'
            'Scalar. Works with Matrix and DuckDB.'
        ),
        'example': 'r = sumproduct(m[:, "Price"], m[:, "Quantity"])',
    },
}