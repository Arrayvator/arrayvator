# syntax/autocomplete/aliases.py
"""
Алиасы (русские и английские синонимы) для функций ArrayVator.

Использование:
    пользователь набирает "сводная" → автодополнение предлагает pivot
    пользователь набирает "впр"     → автодополнение предлагает vlookup

Структура:
    RU_ALIASES = { 'алиас': ['функция1', 'функция2', ...] }
    EN_ALIASES = { ... }

ПРАВИЛА:
    - Ключи — в нижнем регистре, без пробелов.
    - Значения — имена функций (как в AUTOCOMPLETE_ITEMS).
    - Одна функция может иметь много алиасов.
    - Один алиас может указывать на несколько функций.
"""


# ============================================================
# РУССКИЕ АЛИАСЫ
# ============================================================
RU_ALIASES = {
    # ---------- Сводные таблицы / группировка ----------
    'сводная':      ['pivot'],
    'своднаятаблица': ['pivot'],
    'пивот':        ['pivot'],
    'группировка':  ['groupby'],
    'группировать': ['groupby'],
    'сгруппировать': ['groupby'],
    'итоги':        ['groupby', 'groupagg'],
    'подытог':      ['groupagg'],
    'подытоги':     ['groupagg'],
    'развернуть':   ['unpivot'],
    'свернуть':     ['pivot'],

    # ---------- Поиск / ВПР ----------
    'впр':          ['vlookup'],
    'впрв':         ['vlookup'],
    'поискзначения': ['vlookup'],
    'справочник':   ['vlookup'],
    'подстановка':  ['vlookup'],
    'найти':        ['find'],
    'искать':       ['find'],
    'поиск':        ['find'],
    'координаты':   ['find'],
    'индекс':       ['find', 'index'],

    # ---------- Фильтрация / удаление ----------
    'фильтр':       ['filterif'],
    'фильтровать':  ['filterif'],
    'отфильтровать': ['filterif'],
    'удалитьстроки': ['deleteif'],
    'удалитьпо':    ['deleteif'],
    'очистить':     ['clean'],
    'удалить':      ['delete'],

    # ---------- Сортировка ----------
    'сортировка':   ['sort'],
    'сортировать':  ['sort'],
    'отсортировать': ['sort'],
    'сортироватьпо': ['sort'],
    'поубыванию':   ['sort'],
    'повозрастанию': ['sort'],

    # ---------- Дубликаты ----------
    'уникальные':   ['Unique'],
    'уникальныезначения': ['Unique'],
    'дубликаты':    ['DeleteDuplicate'],
    'удалитьдубликаты': ['DeleteDuplicate'],
    'частоты':      ['ValueCounts'],
    'частотность':  ['ValueCounts'],
    'количествоуникальных': ['CountDistinct'],
    'числоуникальных': ['CountDistinct'],

    # ---------- Статистика ----------
    'сумма':        ['sum'],
    'суммировать':  ['sum'],
    'сложить':      ['sum'],
    'среднее':      ['avg'],
    'усреднить':    ['avg'],
    'минимум':      ['min'],
    'максимум':     ['max'],
    'минимумчисла': ['min'],
    'максимумчисла': ['max'],
    'количество':   ['len', 'count'],
    'длина':        ['len'],
    'размер':       ['len', 'lenrow', 'lencol'],
    'строк':        ['lenrow'],
    'столбцов':     ['lencol'],
    'округлять':    ['round'],
    'округлить':    ['round'],
    'целое':        ['int'],
    'целаячасть':   ['int'],
    'дробное':      ['frac'],
    'дробнаячасть': ['frac'],

    # ---------- Аналитика ----------
    'абсанализ':    ['abc'],
    'абц':          ['abc'],
    'abcанализ':    ['abc'],
    'анализ':       ['abc', 'percentof', 'anomaly'],
    'доля':         ['percentof'],
    'процент':      ['percentof'],
    'проценты':     ['percentof'],
    'доляот':       ['percentof'],
    'процентот':    ['percentof'],
    'аномалии':     ['anomaly'],
    'аномалия':     ['anomaly'],
    'выбросы':      ['anomaly'],
    'выброс':       ['anomaly'],
    'отклонения':   ['anomaly'],

    # ---------- Условные агрегаты ----------
    'суммаесли':    ['sumif'],
    'суммапо':      ['sumif'],
    'суммасли':     ['sumif'],
    'среднееесли':  ['avgif'],
    'среднеепо':    ['avgif'],
    'количествоесли': ['countif'],
    'количествопо': ['countif'],
    'минимумесли':  ['minif'],
    'максимумесли': ['maxif'],
    'медианаесли':  ['medianif'],

    # ---------- Строки ----------
    'объединить':   ['joinvector'],
    'соединить':    ['joinvector', 'join'],
    'разделить':    ['split'],
    'разбить':      ['split'],
    'заменить':     ['replacetext'],
    'замена':       ['replacetext'],
    'очиститьтекст': ['clean'],
    'убратьпробелы': ['trim'],
    'обрезать':     ['trim', 'trimleft', 'trimright'],
    'удалитьслева': ['deletetextleft'],
    'удалитьсправа': ['deletetextright'],
    'удалитьсимволы': ['deletetextleft', 'deletetextright'],

    # ---------- Даты и время ----------
    'дата':         ['date', 'datenow'],
    'сегодня':      ['datenow'],
    'сейчас':       ['datenow', 'timenow'],
    'время':        ['timenow', 'time'],
    'год':          ['year'],
    'месяц':        ['month'],
    'день':         ['day'],
    'квартал':      ['quarter'],
    'деньнедели':   ['weekday', 'weekdayname'],
    'названиемесяца': ['monthname'],
    'разницадат':   ['DateDiff'],
    'разница':      ['DateDiff'],
    'прибавитьдней': ['adddays'],
    'прибавитьмесяцев': ['addmonths'],
    'прибавитьлет': ['addyears'],
    'часы':         ['hour'],
    'минуты':       ['minute'],
    'секунды':      ['second'],
    'прибавитьчасов': ['addhours'],
    'прибавитьминут': ['addminutes'],
    'обрезкадаты':  ['datetrunc'],
    'календарь':    ['calendar', 'calendarpro'],

    # ---------- Файлы ----------
    'открытьcsv':   ['OpenCSV'],
    'сохранитьcsv': ['SaveCSV'],
    'открытьexcel': ['OpenExcel'],
    'сохранитьexcel': ['SaveExcel'],
    'открытьtxt':   ['OpenTXT'],
    'сохранитьtxt': ['SaveTXT'],
    'открытьparquet': ['OpenParquet'],
    'сохранитьparquet': ['SaveParquet'],
    'открытьsqlite': ['OpenSQLite'],
    'сохранитьsqlite': ['SaveSQLite'],
    'запрос':       ['QuerySQLite'],
    'sqlзапрос':    ['QuerySQLite'],

    # ---------- BigData ----------
    'большиеданные': ['ToBigData', 'BigData'],
    'матрица':      ['ToMatrix', 'matrix'],
    'вматрицу':     ['ToMatrix'],
    'вbigdata':     ['ToBigData'],
    'duckdb':       ['ToBigData', 'BigData'],

    # ---------- None ----------
    'пусто':        ['isnone'],
    'пустое':       ['isnone'],
    'проверитьпусто': ['isnone'],
    'заполнитьпусто': ['fillna'],
    'удалитьпусто': ['dropna'],
    'первоезначение': ['coalesce'],

    # ---------- Типы ----------
    'тип':          ['type'],
    'число':        ['is_number', 'to_number'],
    'целоечисло':   ['is_integer'],
    'строка':       ['is_string', 'to_string'],
    'логическое':   ['is_boolean'],

    # ---------- Оконные ----------
    'номерстроки':  ['rownumber'],
    'ранг':         ['rank', 'denserank', 'percentrank'],
    'плотныйранг':  ['denserank'],
    'процентиль':   ['percentrank', 'percentile'],
    'накопительнаясумма': ['winsum'],
    'накопительноесреднее': ['winavg'],
    'накопительноеминимум': ['winmin'],
    'накопительныймаксимум': ['winmax'],
    'предыдущаястрока': ['lag'],
    'следующаястрока': ['lead'],
    'первое':       ['firstvalue'],
    'последнее':    ['lastvalue'],
    'nное':         ['nthvalue'],
    'фильтрпоокну': ['qualify'],

    # ---------- Создание ----------
    'нули':         ['zeros'],
    'единицы':      ['ones'],
    'заполнить':    ['fill'],
    'диапазон':     ['range'],
    'случайное':    ['random'],
    'случайные':    ['random'],
    'вектор':       ['vector'],
    'транспонировать': ['transpose'],

    # ---------- Изменение ----------
    'вставить':     ['insert'],
    'вставитьесли': ['insertif'],
    'копировать':   ['copy'],
    'переместить':  ['move'],
    'объединитьмассивы': ['joinarray'],
    'соединитьтаблицы': ['join'],
    'джойн':        ['join'],
    'применить':    ['applyif'],
    'применитьесли': ['applyif'],
    'случайнаявыборка': ['sample'],
    'выборка':      ['sample'],

    # ---------- Графики ----------
    'график':       ['chart'],
    'диаграмма':    ['chart'],
    'столбчатая':   ['chart', 'bar'],
    'линейная':     ['chart', 'line'],
    'круговая':     ['chart', 'pie'],
    'гистограмма':  ['chart', 'hist'],
    'точечная':     ['chart', 'scatter'],
    'ящик':         ['chart', 'box'],
    'тепловаякарта': ['chart', 'heatmap'],
    'парные':       ['chart', 'pair'],

    # ---------- Отчёты ----------
    'отчёт':        ['report'],
    'отчет':        ['report'],
    'отчётсекция':  ['report_section'],
    'отчёттекст':   ['report_text'],
    'отчёттаблица': ['report_table'],
    'отчётграфик':  ['report_chart'],
    'отчётсохранить': ['report_save'],

    # ---------- Ввод / вывод ----------
    'печать':       ['print', 'println'],
    'вывести':      ['print', 'println'],
    'показать':     ['printshow'],
    'ввод':         ['InputShow', 'input'],
    'форма':        ['InputShowForm'],
    'списокввода':  ['InputListShow'],

    # ---------- Прочее ----------
    'лог':          ['LogToFile'],
    'логирование':  ['LogToFile'],
    'выключитьлог': ['LogOff'],
    'добавитьстолбец': ['addcolumn'],
    'добавитьстроки': ['addrows'],
    'добавить':     ['addcolumn', 'addrows'],
    'вычислить':    ['addcolumn'],
    'пример':       ['sample'],
    'обработатьошибки': ['try'],
}


# ============================================================
# АНГЛИЙСКИЕ АЛИАСЫ
# ============================================================
EN_ALIASES = {
    # ---------- Pivot / Group ----------
    'pivot':        ['pivot'],
    'pivottable':   ['pivot'],
    'crosstab':     ['pivot'],
    'group':        ['groupby'],
    'grouping':     ['groupby'],
    'summarize':    ['groupby', 'groupagg'],
    'rollup':       ['groupagg'],
    'unpivot':      ['unpivot'],
    'melt':         ['unpivot'],

    # ---------- Lookup / Find ----------
    'lookup':       ['vlookup'],
    'vlookup':      ['vlookup'],
    'search':       ['find'],
    'find':         ['find'],
    'locate':       ['find'],
    'index':        ['find', 'index'],

    # ---------- Filter / Delete ----------
    'filter':       ['filterif'],
    'where':        ['filterif'],
    'removeif':     ['deleteif'],
    'remove':       ['delete'],
    'delete':       ['delete', 'deleteif'],

    # ---------- Sort ----------
    'sort':         ['sort'],
    'order':        ['sort'],
    'ascending':    ['sort'],
    'descending':   ['sort'],

    # ---------- Dedup ----------
    'unique':       ['Unique'],
    'distinct':     ['Unique', 'CountDistinct'],
    'dedup':        ['DeleteDuplicate'],
    'duplicates':   ['DeleteDuplicate'],
    'frequencies':  ['ValueCounts'],
    'valuecounts':  ['ValueCounts'],

    # ---------- Stats ----------
    'sum':          ['sum'],
    'total':        ['sum'],
    'avg':          ['avg'],
    'average':      ['avg'],
    'mean':         ['avg'],
    'min':          ['min'],
    'minimum':      ['min'],
    'max':          ['max'],
    'maximum':      ['max'],
    'count':        ['len', 'count'],
    'length':       ['len'],
    'rows':         ['lenrow'],
    'cols':         ['lencol'],
    'columns':      ['lencol'],
    'round':        ['round'],
    'int':          ['int'],
    'frac':         ['frac'],
    'fraction':     ['frac'],

    # ---------- Analytics ----------
    'abc':          ['abc'],
    'pareto':       ['abc'],
    'percent':      ['percentof'],
    'percentage':   ['percentof'],
    'share':        ['percentof'],
    'ratio':        ['percentof'],
    'anomaly':      ['anomaly'],
    'outlier':      ['anomaly'],
    'outliers':     ['anomaly'],

    # ---------- Conditional ----------
    'sumif':        ['sumif'],
    'countif':      ['countif'],
    'avgif':        ['avgif'],
    'minif':        ['minif'],
    'maxif':        ['maxif'],

    # ---------- Strings ----------
    'concat':       ['joinvector'],
    'concatarray':  ['joinvector'],
    'join':         ['joinvector', 'join'],
    'split':        ['split'],
    'replace':      ['replacetext'],
    'clean':        ['clean'],
    'trim':         ['trim'],
    'strip':        ['trim'],
    'ltrim':        ['trimleft'],
    'rtrim':        ['trimright'],

    # ---------- Dates ----------
    'date':         ['date', 'datenow'],
    'today':        ['datenow'],
    'now':          ['datenow', 'timenow'],
    'time':         ['timenow', 'time'],
    'year':         ['year'],
    'month':        ['month'],
    'day':          ['day'],
    'quarter':      ['quarter'],
    'weekday':      ['weekday'],
    'datediff':     ['DateDiff'],
    'adddays':      ['adddays'],
    'addmonths':    ['addmonths'],
    'addyears':     ['addyears'],
    'datetrunc':    ['datetrunc'],
    'calendar':     ['calendar', 'calendarpro'],

    # ---------- Files ----------
    'opencsv':      ['OpenCSV'],
    'savecsv':      ['SaveCSV'],
    'openexcel':    ['OpenExcel'],
    'saveexcel':    ['SaveExcel'],
    'opentxt':      ['OpenTXT'],
    'savetxt':      ['SaveTXT'],
    'opensqlite':   ['OpenSQLite'],
    'query':        ['QuerySQLite'],
    'sql':          ['QuerySQLite'],

    # ---------- BigData ----------
    'bigdata':      ['ToBigData', 'BigData'],
    'duckdb':       ['ToBigData', 'BigData'],
    'matrix':       ['ToMatrix', 'matrix'],
    'loadmatrix':   ['ToMatrix'],
    'toloadmatrix': ['ToMatrix'],

    # ---------- None ----------
    'isnone':       ['isnone'],
    'isnull':       ['isnone'],
    'isna':         ['isnone'],
    'fillna':       ['fillna'],
    'fillnull':     ['fillna'],
    'dropna':       ['dropna'],
    'coalesce':     ['coalesce'],

    # ---------- Types ----------
    'type':         ['type'],
    'isnumber':     ['is_number'],
    'isstring':     ['is_string'],
    'isboolean':    ['is_boolean'],
    'tostring':     ['to_string'],
    'tonumber':     ['to_number'],

    # ---------- Window ----------
    'rownumber':    ['rownumber'],
    'rank':         ['rank'],
    'denserank':    ['denserank'],
    'percentrank':  ['percentrank'],
    'ntile':        ['ntile'],
    'lag':          ['lag'],
    'lead':         ['lead'],
    'winsum':       ['winsum'],
    'winavg':       ['winavg'],
    'wincount':     ['wincount'],
    'winmin':       ['winmin'],
    'winmax':       ['winmax'],
    'qualify':      ['qualify'],

    # ---------- Create ----------
    'zeros':        ['zeros'],
    'ones':         ['ones'],
    'fill':         ['fill'],
    'range':        ['range'],
    'random':       ['random'],
    'vector':       ['vector'],
    'transpose':    ['transpose'],

    # ---------- Modify ----------
    'insert':       ['insert'],
    'copy':         ['copy'],
    'move':         ['move'],
    'joinarrays':   ['joinarray'],
    'apply':        ['applyif'],
    'applyif':      ['applyif'],
    'sample':       ['sample'],

    # ---------- Charts ----------
    'chart':        ['chart'],
    'plot':         ['chart'],
    'bar':          ['chart', 'bar'],
    'line':         ['chart', 'line'],
    'pie':          ['chart', 'pie'],
    'hist':         ['chart', 'hist'],
    'scatter':      ['chart', 'scatter'],
    'box':          ['chart', 'box'],
    'heatmap':      ['chart', 'heatmap'],

    # ---------- Reports ----------
    'report':       ['report'],
    'section':      ['report_section'],
    'text':         ['report_text'],
    'table':        ['report_table'],
    'chartreport':  ['report_chart'],

    # ---------- I/O ----------
    'print':        ['print', 'println'],
    'show':         ['printshow'],
    'input':        ['InputShow', 'input'],
    'form':         ['InputShowForm'],

    # ---------- Misc ----------
    'log':          ['LogToFile'],
    'logfile':      ['LogToFile'],
    'addcolumn':    ['addcolumn'],
    'addrows':      ['addrows'],
    'add':          ['addcolumn', 'addrows'],
}


# ============================================================
# ОБЪЕДИНЕНИЕ
# ============================================================
def get_aliases(lang='ru'):
    """Возвращает словарь алиасов для языка."""
    return RU_ALIASES if lang == 'ru' else EN_ALIASES


def get_all_aliases():
    """Все алиасы (RU + EN)."""
    result = dict(RU_ALIASES)
    result.update(EN_ALIASES)
    return result


def find_by_alias(word):
    """
    Ищет функции по алиасу.
    Возвращает список имён функций (может быть пустым).
    """
    word = word.lower().strip()
    if not word:
        return []

    all_aliases = get_all_aliases()
    if word in all_aliases:
        return list(all_aliases[word])

    # Поиск по частичному совпадению (начинается с word)
    results = []
    for alias, funcs in all_aliases.items():
        if alias.startswith(word):
            for f in funcs:
                if f not in results:
                    results.append(f)
    return results