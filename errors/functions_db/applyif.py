# errors/functions_db/applyif.py
"""
База ошибок для функции APPLYIF — условное присваивание.

СИНТАКСИС:
    applyif(условие, m[:, "X"] = значение)
    applyif(условие, m[:, end+1] = значение)

ЛОГИКА:
    Где условие истинно — присвоить значение.
    Где ложно — оставить как было.
"""


RU = {
    'applyif': {
        'name': 'applyif',
        'category': 'case',
        'signature': 'applyif(условие, m[:, "X"] = значение)',
        'description': (
            'Условное присваивание.\n'
            '  • Где условие истинно — присвоить значение.\n'
            '  • Где ложно — оставить как было.\n'
            '  • Работает с Matrix и DuckDB.\n'
            '  • Возвращает НОВУЮ матрицу.\n'
            '  • Строки НЕ удаляются и НЕ копируются.'
        ),
        'examples': [
            'r = applyif(m[:, "Отдел"] == "IT", m[:, "Статус"] = "VIP")',
            'm = applyif(m[:, "Отдел"] == "IT", m[:, "Статус"] = "VIP")',
            'r = applyif(m[2:10, "Отдел"] == "IT", m[:, "Статус"] = "VIP")',
            'r = applyif(m[:, "Отдел"] == "IT" and m[:, "Возраст"] > 30, m[:, "Статус"] = "VIP")',
        ],
        'errors': {
            'APPLYIF_NEED_ASSIGN': {
                'message': (
                    "applyif: внутри нужен '=' для присваивания.\n"
                    "  Второй аргумент должен быть m[:, \"X\"] = значение."
                ),
                'wrong': 'r = applyif(m[:, "Отдел"] == "IT", "VIP")',
                'right': (
                    'r = applyif(m[:, "Отдел"] == "IT", '
                    'm[:, "Статус"] = "VIP")'
                ),
                'explanation': (
                    "applyif ВСЕГДА принимает второй аргумент в виде\n"
                    "'срез = значение'. Без '=' он не знает, КУДА писать.\n"
                    "\n"
                    "Структура:\n"
                    "  applyif(условие, m[:, \"X\"] = значение)"
                ),
                'variants': [
                    'r = applyif(m[:, "Отдел"] == "IT", m[:, "Статус"] = "VIP")',
                    'r = applyif(m[2:10, "Отдел"] == "IT", m[:, "Статус"] = "VIP")',
                    'r = applyif(m[:, "Возраст"] < 18, m[:, "Статус"] = "Дитя")',
                ],
            },
            'APPLYIF_BAD_SYNTAX': {
                'message': (
                    "applyif: неверный синтаксис.\n"
                    "  Нужно условие и целевой срез с '='."
                ),
                'wrong': 'r = applyif(m[:, "Отдел"] == "IT")',
                'right': (
                    'r = applyif(m[:, "Отдел"] == "IT", '
                    'm[:, "Статус"] = "VIP")'
                ),
                'explanation': (
                    "applyif принимает ДВА аргумента:\n"
                    "  1. условие\n"
                    "  2. m[:, \"X\"] = значение\n"
                    "\n"
                    "Структура:\n"
                    "  applyif(условие, m[:, \"X\"] = значение)"
                ),
                'variants': [
                    'r = applyif(m[:, "Отдел"] == "IT", m[:, "Статус"] = "VIP")',
                    'r = applyif(m[2:10, "Отдел"] == "IT", m[:, "Статус"] = "VIP")',
                    'r = applyif(m[:, "Возраст"] < 18, m[:, "Статус"] = "Дитя")',
                ],
            },
            'APPLYIF_BAD_TARGET': {
                'message': (
                    "applyif: цель должна быть срезом m[:, \"X\"]."
                ),
                'wrong': 'r = applyif(m[:, "Отдел"] == "IT", "Статус" = "VIP")',
                'right': (
                    'r = applyif(m[:, "Отдел"] == "IT", '
                    'm[:, "Статус"] = "VIP")'
                ),
                'explanation': (
                    "Целевой столбец указывается СРЕЗОМ m[:, \"X\"].\n"
                    "Это нужно, чтобы applyif знал, к какому столбцу\n"
                    "применять присваивание.\n"
                    "\n"
                    "Неправильно: \"Статус\" = \"VIP\"\n"
                    "Правильно: m[:, \"Статус\"] = \"VIP\""
                ),
                'variants': [
                    'r = applyif(m[:, "Отдел"] == "IT", m[:, "Статус"] = "VIP")',
                    'r = applyif(m[2:10, "Отдел"] == "IT", m[:, "Статус"] = "VIP")',
                    'r = applyif(m[:, "Отдел"] == "IT", m[:, end+1] = "VIP")',
                ],
            },
            'APPLYIF_REQUIRES_ASSIGNMENT': {
                'message': (
                    "applyif() возвращает значение — "
                    "результат нужно сохранить."
                ),
                'wrong': 'applyif(m[:, "Отдел"] == "IT", m[:, "Статус"] = "VIP")',
                'right': (
                    'r = applyif(m[:, "Отдел"] == "IT", '
                    'm[:, "Статус"] = "VIP")'
                ),
                'explanation': (
                    "applyif НЕ изменяет исходную матрицу.\n"
                    "Он ВОЗВРАЩАЕТ НОВУЮ.\n"
                    "\n"
                    "Правильно:\n"
                    "  r = applyif(...)     — в новую переменную\n"
                    "  m = applyif(...)     — мутация"
                ),
                'variants': [
                    'r = applyif(m[:, "Отдел"] == "IT", m[:, "Статус"] = "VIP")',
                    'm = applyif(m[:, "Отдел"] == "IT", m[:, "Статус"] = "VIP")',
                ],
            },
        },
    },
}


EN = {
    'applyif': {
        'name': 'applyif',
        'category': 'case',
        'signature': 'applyif(condition, m[:, "X"] = value)',
        'description': (
            'Conditional assignment.\n'
            '  • Where condition is true — assign the value.\n'
            '  • Where false — leave as is.\n'
            '  • Works with Matrix and DuckDB.\n'
            '  • Returns a NEW matrix.\n'
            '  • Rows are NOT deleted or copied.'
        ),
        'examples': [
            'r = applyif(m[:, "Dept"] == "IT", m[:, "Status"] = "VIP")',
            'm = applyif(m[:, "Dept"] == "IT", m[:, "Status"] = "VIP")',
            'r = applyif(m[2:10, "Dept"] == "IT", m[:, "Status"] = "VIP")',
            'r = applyif(m[:, "Dept"] == "IT" and m[:, "Age"] > 30, m[:, "Status"] = "VIP")',
        ],
        'errors': {
            'APPLYIF_NEED_ASSIGN': {
                'message': (
                    "applyif: '=' is required inside.\n"
                    "  Second argument must be m[:, \"X\"] = value."
                ),
                'wrong': 'r = applyif(m[:, "Dept"] == "IT", "VIP")',
                'right': (
                    'r = applyif(m[:, "Dept"] == "IT", '
                    'm[:, "Status"] = "VIP")'
                ),
                'explanation': (
                    "applyif ALWAYS takes the second argument as\n"
                    "'slice = value'. Without '=' it doesn't know WHERE to write.\n"
                    "\n"
                    "Structure:\n"
                    "  applyif(condition, m[:, \"X\"] = value)"
                ),
                'variants': [
                    'r = applyif(m[:, "Dept"] == "IT", m[:, "Status"] = "VIP")',
                    'r = applyif(m[2:10, "Dept"] == "IT", m[:, "Status"] = "VIP")',
                    'r = applyif(m[:, "Age"] < 18, m[:, "Status"] = "Child")',
                ],
            },
            'APPLYIF_BAD_SYNTAX': {
                'message': (
                    "applyif: invalid syntax.\n"
                    "  Need a condition and a target slice with '='."
                ),
                'wrong': 'r = applyif(m[:, "Dept"] == "IT")',
                'right': (
                    'r = applyif(m[:, "Dept"] == "IT", '
                    'm[:, "Status"] = "VIP")'
                ),
                'explanation': (
                    "applyif takes TWO arguments:\n"
                    "  1. condition\n"
                    "  2. m[:, \"X\"] = value\n"
                    "\n"
                    "Structure:\n"
                    "  applyif(condition, m[:, \"X\"] = value)"
                ),
                'variants': [
                    'r = applyif(m[:, "Dept"] == "IT", m[:, "Status"] = "VIP")',
                    'r = applyif(m[2:10, "Dept"] == "IT", m[:, "Status"] = "VIP")',
                    'r = applyif(m[:, "Age"] < 18, m[:, "Status"] = "Child")',
                ],
            },
            'APPLYIF_BAD_TARGET': {
                'message': (
                    "applyif: target must be a slice m[:, \"X\"]."
                ),
                'wrong': 'r = applyif(m[:, "Dept"] == "IT", "Status" = "VIP")',
                'right': (
                    'r = applyif(m[:, "Dept"] == "IT", '
                    'm[:, "Status"] = "VIP")'
                ),
                'explanation': (
                    "The target column is given as a SLICE m[:, \"X\"].\n"
                    "This tells applyif which column to write to.\n"
                    "\n"
                    "Неправильно: \"Status\" = \"VIP\"\n"
                    "Правильно: m[:, \"Status\"] = \"VIP\""
                ),
                'variants': [
                    'r = applyif(m[:, "Dept"] == "IT", m[:, "Status"] = "VIP")',
                    'r = applyif(m[2:10, "Dept"] == "IT", m[:, "Status"] = "VIP")',
                    'r = applyif(m[:, "Dept"] == "IT", m[:, end+1] = "VIP")',
                ],
            },
            'APPLYIF_REQUIRES_ASSIGNMENT': {
                'message': (
                    "applyif() returns a value — "
                    "the result must be saved."
                ),
                'wrong': 'applyif(m[:, "Dept"] == "IT", m[:, "Status"] = "VIP")',
                'right': (
                    'r = applyif(m[:, "Dept"] == "IT", '
                    'm[:, "Status"] = "VIP")'
                ),
                'explanation': (
                    "applyif does NOT modify the source matrix.\n"
                    "It RETURNS a NEW one.\n"
                    "\n"
                    "Correct:\n"
                    "  r = applyif(...)     — to a new variable\n"
                    "  m = applyif(...)     — mutation"
                ),
                'variants': [
                    'r = applyif(m[:, "Dept"] == "IT", m[:, "Status"] = "VIP")',
                    'm = applyif(m[:, "Dept"] == "IT", m[:, "Status"] = "VIP")',
                ],
            },
        },
    },
}