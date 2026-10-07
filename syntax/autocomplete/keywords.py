# syntax/autocomplete/keywords.py
"""
Полный список ключевых слов ArrayVator.
Один для обоих языков — ключевые слова не переводятся.

ВАЖНО:
    Слово 'null' НЕ ключевое и НЕ литерал.
    Единственный литерал пустого значения — None.
    Слова 'null' и 'nan' ловятся лексером как ошибка
    (BANNED_NULL_LITERAL / BANNED_NAN_LITERAL).

    Функция noneif (ранее null_if) — ключевое слово.
"""

KEYWORDS = [
    # Управляющие
    'if', 'then', 'else', 'for', 'while', 'break',
    # Логические
    'and', 'or', 'not', 'true', 'false', 'None',
    # Индексация
    'all', 'end', 'begin', 'last',
    # Модификаторы
    'before', 'after', 'AZ', 'ZA', 'inside', 'ignore', 'skip', 'approx',
    'vertical', 'horizontal', 'when',
    # Строковые функции очистки
    'trim', 'trimleft', 'trimright',
    # Даты — извлечение компонентов
    'year', 'month', 'day', 'quarter',
    'weekday', 'weekdayname', 'monthname',
    # Даты — арифметика
    'adddays', 'addmonths', 'addyears',
    # Даты — обрезка
    'datetrunc',
    # Ввод/вывод
    'print', 'println', 'input',
    # Режимы
    'BigData', 'Table',
    # Groupby
    'by', 'agg', 'having',
    # Оконные
    'order',
    # Обработка ошибок
    'try', 'catch', 'error',
    # Графики: типы
    'chart', 'bar', 'line', 'pie', 'hist', 'scatter', 'box', 'heatmap', 'pair',
    # Графики: опции
    'title', 'save', 'bins', 'color', 'xlabel', 'ylabel', 'plotly', 'static',
    # Отчёты
    'report', 'report_section', 'report_text', 'report_table',
    'report_chart', 'report_save', 'report_show', 'report_save_pdf',
    # Блочные / строки
    'addrows', 'groupagg', 'filldown',
    # Оконные функции
    'rownumber', 'rank', 'denserank', 'percentrank', 'cumedist', 'ntile',
    'lag', 'lead', 'firstvalue', 'lastvalue', 'nthvalue',
    'winsum', 'winavg', 'wincount', 'winmin', 'winmax',
    'winmedian', 'winstdev', 'qualify',
    # None-функции
    'isnone', 'fillna', 'dropna', 'coalesce', 'noneif',
    # Прочее
    'addcolumn',
    # Аналитические
    'abc', 'percentof', 'anomaly',
    'coef', 'iqr', 'zscore', 'percentile', 'only',
    # Условные агрегаты
    'sumif', 'countif', 'avgif', 'minif', 'maxif',
    'medianif', 'countuniqueif', 'sumproduct',
]