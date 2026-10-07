# errors/messages/ru/strings.py
"""
Ошибки строковых функций: trim, replacetext, deletetext, clean, split.
"""

MESSAGES = {
    "DELETETEXTLEFT_BAD_SYNTAX":
        "Неверный синтаксис deletetextleft().\n"
        "  Формат: deletetextleft(данные, N)",
    "DELETETEXTRIGHT_BAD_SYNTAX":
        "Неверный синтаксис deletetextright().\n"
        "  Формат: deletetextright(данные, N)",

    "TRIM_BAD_SYNTAX":
        "Неверный синтаксис trim / trimleft / trimright.\n"
        "  Формат: trim(данные [, \"символы\"])\n"
        "  Пример: trim(m[:, \"Имя\"])\n"
        "  Пример: trimleft(m[:, \"Код\"], \"0\")\n"
        "  Пример: trimright(m[:, \"Имя\"])",

    "REPLACETEXT_BAD_SYNTAX":
        "Неверный синтаксис replacetext().\n"
        "  Формат: replacetext(данные, \"что\", \"на_что\" [, ignore])",

    "SPLIT_BAD_SYNTAX":
        "Неверный синтаксис split().\n"
        "  Формат: split(текст [, разделитель] [, skip])",

    "CLEAN_BAD_SYNTAX":
        "Неверный синтаксис clean().\n"
        "  Формат: clean(данные, \"digits\"|\"letters\"|\"special\"|\"alnum\")",

    "DELETETEXT_NEGATIVE_COUNT":
        "Количество символов не может быть отрицательным.",
    "DELETETEXT_COLUMN_NOT_FOUND":
        "Столбец не найден в матрице.\n"
        "  Проверьте имя или номер столбца.",
    "DELETETEXT_ROW_NOT_FOUND":
        "Строка не найдена в матрице.\n"
        "  Проверьте номер строки или значение в первом столбце.",
}