# errors/messages/ru/window.py
"""
Ошибки оконных функций.
"""

MESSAGES = {
    "WINDOW_BAD_SYNTAX":
        "Неверный синтаксис оконной функции.\n"
        "  Формат: <имя>(m, by m[:, \"X\"], order m[:, \"Y\"], AZ|ZA)\n"
        "  Пример: rownumber(m, by m[:, \"Отдел\"], order m[:, \"Зарплата\"], ZA)",
    "WINDOW_NEED_BY":
        "Оконная функция: укажите 'by' для партиции.",
    "WINDOW_NEED_ORDER":
        "Оконная функция: укажите 'order' для сортировки.",
    "QUALIFY_BAD_SYNTAX":
        "Неверный синтаксис qualify().\n"
        "  Формат: qualify(m, оконная_функция ОП значение)\n"
        "  Пример: qualify(m, rownumber(m, by m[:, \"Отдел\"], "
        "order m[:, \"Зарплата\"], ZA) <= 3)",
}