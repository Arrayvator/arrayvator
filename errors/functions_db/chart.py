# errors/functions_db/chart.py
"""
База ошибок для функции CHART — построение графиков.

СИНТАКСИС:
    chart(тип, x [, y] [, опции])

ТИПЫ:
    bar      — столбчатая
    line     — линейная
    pie      — круговая
    hist     — гистограмма
    scatter  — точки
    box      — ящик с усами
    heatmap  — тепловая карта (требует матрицу)
    pair     — парные зависимости (требует ≥ 2 столбцов)

ОПЦИИ:
    title "..."      — заголовок
    xlabel "..."     — подпись X
    ylabel "..."     — подпись Y
    color "..."      — цвет
    save "file.png"  — сохранить в файл
    bins N           — корзин (hist)
    plotly           — интерактивный Plotly (HTML)
    static           — статичный Matplotlib (по умолчанию)

ВАЖНО:
    chart — ОПЕРАТОР, не требует присваивания.
    Вызывается как statement:
        chart(bar, m[:, "Отдел"], m[:, "Зарплата"])
"""

RU = {
    'chart': {
        'name': 'chart',
        'category': 'chart',
        'signature': 'chart(тип, x [, y] [, опции])',
        'description': (
            'Построение графиков.\n'
            '  • Типы: bar, line, pie, hist, scatter, box, heatmap, pair.\n'
            '  • Опции: title, xlabel, ylabel, color, save, bins,\n'
            '           plotly, static.\n'
            '  • Правый клик в окне — меню сохранения (PNG, PDF, SVG, JPG).\n'
            '  • chart — ОПЕРАТОР, присваивание не нужно.\n'
            '  • Работает с Matrix (RAM) и DuckDB (BigData).'
        ),
        'examples': [
            'chart(bar, m[:, "Отдел"], m[:, "Зарплата"])',
            'chart(line, m[:, "Месяц"], m[:, "Продажи"])',
            'chart(pie, m[:, "Отдел"], m[:, "Доля"])',
            'chart(hist, m[:, "Возраст"], bins 10)',
            'chart(scatter, m[:, "X"], m[:, "Y"])',
            'chart(box, m[:, "Отдел"], m[:, "Зарплата"])',
            'chart(heatmap, m[:, 2:end])',
            'chart(pair, m[:, 2:end])',
            'chart(bar, m[:, "Отдел"], m[:, "Зарплата"],\n'
            '      title "Зарплаты", color "red", save "chart.png")',
        ],
        'errors': {
            'CHART_BAD_KIND': {
                'message': (
                    "chart: неверный тип графика.\n"
                    "  Допустимо: bar, line, pie, hist, scatter, box, heatmap, pair."
                ),
                'wrong': 'chart(bars, m[:, "Отдел"], m[:, "Зарплата"])',
                'right': 'chart(bar, m[:, "Отдел"], m[:, "Зарплата"])',
                'explanation': (
                    "Тип указывается ПЕРВЫМ аргументом, БЕЗ кавычек:\n"
                    "     bar      — столбчатая\n"
                    "     line     — линейная\n"
                    "     pie      — круговая\n"
                    "     hist     — гистограмма\n"
                    "     scatter  — точки\n"
                    "     box      — ящик с усами\n"
                    "     heatmap  — тепловая карта\n"
                    "     pair     — парные зависимости\n"
                    "\n"
                    "Неправильно:\n"
                    "     chart(bars, ...)\n"
                    "     chart(\"bar\", ...)\n"
                    "\n"
                    "Правильно:\n"
                    "     chart(bar, m[:, \"Отдел\"], m[:, \"Зарплата\"])"
                ),
                'variants': [
                    'chart(bar, m[:, "Отдел"], m[:, "Зарплата"])',
                    'chart(line, m[:, "Месяц"], m[:, "Продажи"])',
                    'chart(hist, m[:, "Возраст"], bins 10)',
                    'chart(pie, m[:, "Отдел"], m[:, "Доля"])',
                ],
            },
            'CHART_NEED_X': {
                'message': (
                    "chart: не указаны данные X."
                ),
                'wrong': 'chart(bar)',
                'right': 'chart(bar, m[:, "Отдел"], m[:, "Зарплата"])',
                'explanation': (
                    "После типа графика нужен хотя бы ОДИН аргумент — данные X:\n"
                    "\n"
                    "Структура:\n"
                    "  chart(тип, x)\n"
                    "  chart(тип, x, y)\n"
                    "  chart(тип, x, y, опции...)\n"
                    "\n"
                    "Примеры:\n"
                    "     chart(bar, m[:, \"Отдел\"], m[:, \"Зарплата\"])\n"
                    "     chart(hist, m[:, \"Возраст\"], bins 10)\n"
                    "     chart(heatmap, m[:, 2:end])"
                ),
                'variants': [
                    'chart(bar, m[:, "Отдел"], m[:, "Зарплата"])',
                    'chart(hist, m[:, "Возраст"], bins 10)',
                    'chart(heatmap, m[:, 2:end])',
                ],
            },
            'CHART_NEED_Y': {
                'message': (
                    "chart: для этого типа графика нужны данные Y."
                ),
                'wrong': 'chart(bar, m[:, "Отдел"])',
                'right': 'chart(bar, m[:, "Отдел"], m[:, "Зарплата"])',
                'explanation': (
                    "Типы bar, line, scatter, box, pie требуют ДВА аргумента:\n"
                    "     chart(bar, x, y)\n"
                    "     chart(line, x, y)\n"
                    "     chart(scatter, x, y)\n"
                    "\n"
                    "Типы hist, heatmap, pair — только X:\n"
                    "     chart(hist, x, bins N)\n"
                    "     chart(heatmap, matrix)\n"
                    "     chart(pair, matrix)"
                ),
                'variants': [
                    'chart(bar, m[:, "Отдел"], m[:, "Зарплата"])',
                    'chart(line, m[:, "Месяц"], m[:, "Продажи"])',
                    'chart(scatter, m[:, "X"], m[:, "Y"])',
                    'chart(hist, m[:, "Возраст"], bins 10)',
                    'chart(heatmap, m[:, 2:end])',
                ],
            },
            'CHART_BAD_X': {
                'message': (
                    "chart: X должен быть срезом m[:, \"X\"] или матрицей."
                ),
                'wrong': 'chart(bar, "Отдел", m[:, "Зарплата"])',
                'right': 'chart(bar, m[:, "Отдел"], m[:, "Зарплата"])',
                'explanation': (
                    "X — это СРЕЗ столбца или матрица:\n"
                    "     m[:, \"Отдел\"]      — столбец\n"
                    "     m[:, 2:end]        — матрица (heatmap, pair)\n"
                    "     v                  — вектор\n"
                    "\n"
                    "Неправильно:\n"
                    "     chart(bar, \"Отдел\", ...)\n"
                    "\n"
                    "Правильно:\n"
                    "     chart(bar, m[:, \"Отдел\"], m[:, \"Зарплата\"])"
                ),
                'variants': [
                    'chart(bar, m[:, "Отдел"], m[:, "Зарплата"])',
                    'chart(hist, m[:, "Возраст"], bins 10)',
                ],
            },
            'CHART_BAD_BINS': {
                'message': (
                    "chart: bins должен быть числом >= 1."
                ),
                'wrong': 'chart(hist, m[:, "Возраст"], bins "10")',
                'right': 'chart(hist, m[:, "Возраст"], bins 10)',
                'explanation': (
                    "bins — число БЕЗ кавычек:\n"
                    "     chart(hist, m[:, \"Возраст\"], bins 10)\n"
                    "     chart(hist, m[:, \"Возраст\"], bins 20)\n"
                    "\n"
                    "Неправильно:\n"
                    "     chart(hist, m[:, \"Возраст\"], bins \"10\")\n"
                    "     chart(hist, m[:, \"Возраст\"], bins 0)"
                ),
                'variants': [
                    'chart(hist, m[:, "Возраст"], bins 10)',
                    'chart(hist, m[:, "Возраст"], bins 20)',
                ],
            },
            'CHART_NOT_INSTALLED_MATPLOTLIB': {
                'message': (
                    "chart: matplotlib не установлен.\n"
                    "  Установите: pip install matplotlib"
                ),
                'wrong': 'chart(bar, m[:, "X"], m[:, "Y"])',
                'right': (
                    'pip install matplotlib\n'
                    'chart(bar, m[:, "X"], m[:, "Y"])'
                ),
                'explanation': (
                    "chart (статичные графики) требует matplotlib.\n"
                    "\n"
                    "Установка:\n"
                    "     pip install matplotlib\n"
                    "\n"
                    "Если matplotlib недоступен — используйте plotly:\n"
                    "     chart(bar, m[:, \"X\"], m[:, \"Y\"], plotly)"
                ),
                'variants': [
                    'pip install matplotlib\nchart(bar, m[:, "X"], m[:, "Y"])',
                    'chart(bar, m[:, "X"], m[:, "Y"], plotly)',
                ],
            },
            'CHART_NOT_INSTALLED_PLOTLY': {
                'message': (
                    "chart: plotly не установлен.\n"
                    "  Установите: pip install plotly"
                ),
                'wrong': 'chart(bar, m[:, "X"], m[:, "Y"], plotly)',
                'right': (
                    'pip install plotly\n'
                    'chart(bar, m[:, "X"], m[:, "Y"], plotly)'
                ),
                'explanation': (
                    "Опция plotly требует plotly:\n"
                    "\n"
                    "Установка:\n"
                    "     pip install plotly\n"
                    "\n"
                    "Plotly сохраняет интерактивный HTML-файл."
                ),
                'variants': [
                    'pip install plotly\nchart(bar, m[:, "X"], m[:, "Y"], plotly)',
                    'chart(bar, m[:, "X"], m[:, "Y"])',
                ],
            },
            'CHART_HEATMAP_NEED_MATRIX': {
                'message': (
                    "chart: heatmap требует МАТРИЦУ.\n"
                    "  Нельзя передать один столбец."
                ),
                'wrong': 'chart(heatmap, m[:, "Отдел"])',
                'right': 'chart(heatmap, m[:, 2:end])',
                'explanation': (
                    "heatmap строит тепловую карту по 2D-данным.\n"
                    "Нужен срез с НЕСКОЛЬКИМИ столбцами:\n"
                    "     chart(heatmap, m[:, 2:end])\n"
                    "     chart(heatmap, m[:, 1:5])\n"
                    "\n"
                    "Неправильно:\n"
                    "     chart(heatmap, m[:, \"Отдел\"])   — один столбец"
                ),
                'variants': [
                    'chart(heatmap, m[:, 2:end])',
                    'chart(heatmap, m[:, 1:5])',
                ],
            },
            'CHART_PAIR_NEED_2COL': {
                'message': (
                    "chart: pair требует минимум ДВА столбца."
                ),
                'wrong': 'chart(pair, m[:, "Отдел"])',
                'right': 'chart(pair, m[:, 2:end])',
                'explanation': (
                    "pair строит матрицу зависимостей между столбцами.\n"
                    "Нужно минимум ДВА числовых столбца:\n"
                    "     chart(pair, m[:, 2:end])\n"
                    "     chart(pair, m[:, 1:4])\n"
                    "\n"
                    "Неправильно:\n"
                    "     chart(pair, m[:, \"Отдел\"])    — один столбец"
                ),
                'variants': [
                    'chart(pair, m[:, 2:end])',
                    'chart(pair, m[:, 1:4])',
                ],
            },
            'CHART_BAD_OPTION': {
                'message': (
                    "chart: неверная опция.\n"
                    "  Допустимо: title, xlabel, ylabel, color, save, "
                    "bins, plotly, static."
                ),
                'wrong': 'chart(bar, m[:, "X"], m[:, "Y"], colour "red")',
                'right': 'chart(bar, m[:, "X"], m[:, "Y"], color "red")',
                'explanation': (
                    "Только эти опции:\n"
                    "     title \"...\"      — заголовок\n"
                    "     xlabel \"...\"     — подпись X\n"
                    "     ylabel \"...\"     — подпись Y\n"
                    "     color \"...\"      — цвет\n"
                    "     save \"...\"       — сохранить в файл\n"
                    "     bins N           — корзин (hist)\n"
                    "     plotly           — интерактивный Plotly\n"
                    "     static           — статичный Matplotlib\n"
                    "\n"
                    "Неправильно:\n"
                    "     colour \"red\"\n"
                    "     label \"X\"\n"
                    "\n"
                    "Правильно:\n"
                    "     color \"red\"\n"
                    "     xlabel \"X\""
                ),
                'variants': [
                    'chart(bar, m[:, "X"], m[:, "Y"], title "Заголовок")',
                    'chart(bar, m[:, "X"], m[:, "Y"], color "red")',
                    'chart(bar, m[:, "X"], m[:, "Y"], save "chart.png")',
                ],
            },
        },
    },
}


EN = {
    'chart': {
        'name': 'chart',
        'category': 'chart',
        'signature': 'chart(kind, x [, y] [, options])',
        'description': (
            'Build charts.\n'
            '  • Kinds: bar, line, pie, hist, scatter, box, heatmap, pair.\n'
            '  • Options: title, xlabel, ylabel, color, save, bins,\n'
            '             plotly, static.\n'
            '  • Right-click in the chart window — save menu (PNG, PDF, SVG, JPG).\n'
            '  • chart is a STATEMENT, no assignment needed.\n'
            '  • Works with Matrix (RAM) and DuckDB (BigData).'
        ),
        'examples': [
            'chart(bar, m[:, "Department"], m[:, "Salary"])',
            'chart(line, m[:, "Month"], m[:, "Sales"])',
            'chart(pie, m[:, "Department"], m[:, "Share"])',
            'chart(hist, m[:, "Age"], bins 10)',
            'chart(scatter, m[:, "X"], m[:, "Y"])',
            'chart(box, m[:, "Department"], m[:, "Salary"])',
            'chart(heatmap, m[:, 2:end])',
            'chart(pair, m[:, 2:end])',
            'chart(bar, m[:, "Department"], m[:, "Salary"],\n'
            '      title "Salaries", color "red", save "chart.png")',
        ],
        'errors': {
            'CHART_BAD_KIND': {
                'message': (
                    "chart: invalid chart type.\n"
                    "  Allowed: bar, line, pie, hist, scatter, box, heatmap, pair."
                ),
                'wrong': 'chart(bars, m[:, "Department"], m[:, "Salary"])',
                'right': 'chart(bar, m[:, "Department"], m[:, "Salary"])',
                'explanation': (
                    "Kind is the FIRST argument, WITHOUT quotes:\n"
                    "     bar      — bar chart\n"
                    "     line     — line chart\n"
                    "     pie      — pie chart\n"
                    "     hist     — histogram\n"
                    "     scatter  — scatter plot\n"
                    "     box      — box plot\n"
                    "     heatmap  — heat map\n"
                    "     pair     — pair plot\n"
                    "\n"
                    "Incorrect:\n"
                    "     chart(bars, ...)\n"
                    "     chart(\"bar\", ...)\n"
                    "\n"
                    "Correct:\n"
                    "     chart(bar, m[:, \"Department\"], m[:, \"Salary\"])"
                ),
                'variants': [
                    'chart(bar, m[:, "Department"], m[:, "Salary"])',
                    'chart(line, m[:, "Month"], m[:, "Sales"])',
                    'chart(hist, m[:, "Age"], bins 10)',
                    'chart(pie, m[:, "Department"], m[:, "Share"])',
                ],
            },
            'CHART_NEED_X': {
                'message': "chart: X data is required.",
                'wrong': 'chart(bar)',
                'right': 'chart(bar, m[:, "Department"], m[:, "Salary"])',
                'explanation': (
                    "After the kind, at least ONE argument is required — X data:\n"
                    "\n"
                    "Structure:\n"
                    "  chart(kind, x)\n"
                    "  chart(kind, x, y)\n"
                    "  chart(kind, x, y, options...)\n"
                    "\n"
                    "Examples:\n"
                    "     chart(bar, m[:, \"Department\"], m[:, \"Salary\"])\n"
                    "     chart(hist, m[:, \"Age\"], bins 10)\n"
                    "     chart(heatmap, m[:, 2:end])"
                ),
                'variants': [
                    'chart(bar, m[:, "Department"], m[:, "Salary"])',
                    'chart(hist, m[:, "Age"], bins 10)',
                    'chart(heatmap, m[:, 2:end])',
                ],
            },
            'CHART_NEED_Y': {
                'message': "chart: Y data is required for this kind.",
                'wrong': 'chart(bar, m[:, "Department"])',
                'right': 'chart(bar, m[:, "Department"], m[:, "Salary"])',
                'explanation': (
                    "Kinds bar, line, scatter, box, pie require TWO args:\n"
                    "     chart(bar, x, y)\n"
                    "     chart(line, x, y)\n"
                    "     chart(scatter, x, y)\n"
                    "\n"
                    "Kinds hist, heatmap, pair — only X:\n"
                    "     chart(hist, x, bins N)\n"
                    "     chart(heatmap, matrix)\n"
                    "     chart(pair, matrix)"
                ),
                'variants': [
                    'chart(bar, m[:, "Department"], m[:, "Salary"])',
                    'chart(line, m[:, "Month"], m[:, "Sales"])',
                    'chart(hist, m[:, "Age"], bins 10)',
                ],
            },
            'CHART_BAD_X': {
                'message': (
                    "chart: X must be a slice m[:, \"X\"] or a matrix."
                ),
                'wrong': 'chart(bar, "Department", m[:, "Salary"])',
                'right': 'chart(bar, m[:, "Department"], m[:, "Salary"])',
                'explanation': (
                    "X is a column SLICE or a matrix:\n"
                    "     m[:, \"Department\"]      — column\n"
                    "     m[:, 2:end]              — matrix (heatmap, pair)\n"
                    "     v                        — vector\n"
                    "\n"
                    "Incorrect:\n"
                    "     chart(bar, \"Department\", ...)\n"
                    "\n"
                    "Correct:\n"
                    "     chart(bar, m[:, \"Department\"], m[:, \"Salary\"])"
                ),
                'variants': [
                    'chart(bar, m[:, "Department"], m[:, "Salary"])',
                    'chart(hist, m[:, "Age"], bins 10)',
                ],
            },
            'CHART_BAD_BINS': {
                'message': "chart: bins must be a number >= 1.",
                'wrong': 'chart(hist, m[:, "Age"], bins "10")',
                'right': 'chart(hist, m[:, "Age"], bins 10)',
                'explanation': (
                    "bins is a NUMBER without quotes:\n"
                    "     chart(hist, m[:, \"Age\"], bins 10)\n"
                    "     chart(hist, m[:, \"Age\"], bins 20)\n"
                    "\n"
                    "Incorrect:\n"
                    "     chart(hist, m[:, \"Age\"], bins \"10\")\n"
                    "     chart(hist, m[:, \"Age\"], bins 0)"
                ),
                'variants': [
                    'chart(hist, m[:, "Age"], bins 10)',
                    'chart(hist, m[:, "Age"], bins 20)',
                ],
            },
            'CHART_NOT_INSTALLED_MATPLOTLIB': {
                'message': (
                    "chart: matplotlib is not installed.\n"
                    "  Install: pip install matplotlib"
                ),
                'wrong': 'chart(bar, m[:, "X"], m[:, "Y"])',
                'right': (
                    'pip install matplotlib\n'
                    'chart(bar, m[:, "X"], m[:, "Y"])'
                ),
                'explanation': (
                    "chart (static plots) requires matplotlib.\n"
                    "\n"
                    "Install:\n"
                    "     pip install matplotlib\n"
                    "\n"
                    "If matplotlib is unavailable — use plotly:\n"
                    "     chart(bar, m[:, \"X\"], m[:, \"Y\"], plotly)"
                ),
                'variants': [
                    'pip install matplotlib\nchart(bar, m[:, "X"], m[:, "Y"])',
                    'chart(bar, m[:, "X"], m[:, "Y"], plotly)',
                ],
            },
            'CHART_NOT_INSTALLED_PLOTLY': {
                'message': (
                    "chart: plotly is not installed.\n"
                    "  Install: pip install plotly"
                ),
                'wrong': 'chart(bar, m[:, "X"], m[:, "Y"], plotly)',
                'right': (
                    'pip install plotly\n'
                    'chart(bar, m[:, "X"], m[:, "Y"], plotly)'
                ),
                'explanation': (
                    "The plotly option requires plotly:\n"
                    "\n"
                    "Install:\n"
                    "     pip install plotly\n"
                    "\n"
                    "Plotly saves an interactive HTML file."
                ),
                'variants': [
                    'pip install plotly\nchart(bar, m[:, "X"], m[:, "Y"], plotly)',
                    'chart(bar, m[:, "X"], m[:, "Y"])',
                ],
            },
            'CHART_HEATMAP_NEED_MATRIX': {
                'message': (
                    "chart: heatmap requires a MATRIX.\n"
                    "  Cannot pass a single column."
                ),
                'wrong': 'chart(heatmap, m[:, "Department"])',
                'right': 'chart(heatmap, m[:, 2:end])',
                'explanation': (
                    "heatmap builds a heat map from 2D data.\n"
                    "Needs a slice with MULTIPLE columns:\n"
                    "     chart(heatmap, m[:, 2:end])\n"
                    "     chart(heatmap, m[:, 1:5])\n"
                    "\n"
                    "Incorrect:\n"
                    "     chart(heatmap, m[:, \"Department\"])   — one column"
                ),
                'variants': [
                    'chart(heatmap, m[:, 2:end])',
                    'chart(heatmap, m[:, 1:5])',
                ],
            },
            'CHART_PAIR_NEED_2COL': {
                'message': "chart: pair requires at least TWO columns.",
                'wrong': 'chart(pair, m[:, "Department"])',
                'right': 'chart(pair, m[:, 2:end])',
                'explanation': (
                    "pair builds a matrix of dependencies between columns.\n"
                    "At least TWO numeric columns are required:\n"
                    "     chart(pair, m[:, 2:end])\n"
                    "     chart(pair, m[:, 1:4])\n"
                    "\n"
                    "Incorrect:\n"
                    "     chart(pair, m[:, \"Department\"])    — one column"
                ),
                'variants': [
                    'chart(pair, m[:, 2:end])',
                    'chart(pair, m[:, 1:4])',
                ],
            },
            'CHART_BAD_OPTION': {
                'message': (
                    "chart: invalid option.\n"
                    "  Allowed: title, xlabel, ylabel, color, save, "
                    "bins, plotly, static."
                ),
                'wrong': 'chart(bar, m[:, "X"], m[:, "Y"], colour "red")',
                'right': 'chart(bar, m[:, "X"], m[:, "Y"], color "red")',
                'explanation': (
                    "Only these options:\n"
                    "     title \"...\"      — title\n"
                    "     xlabel \"...\"     — X label\n"
                    "     ylabel \"...\"     — Y label\n"
                    "     color \"...\"      — color\n"
                    "     save \"...\"       — save to file\n"
                    "     bins N           — bins (hist)\n"
                    "     plotly           — interactive Plotly\n"
                    "     static           — static Matplotlib\n"
                    "\n"
                    "Incorrect:\n"
                    "     colour \"red\"\n"
                    "     label \"X\"\n"
                    "\n"
                    "Correct:\n"
                    "     color \"red\"\n"
                    "     xlabel \"X\""
                ),
                'variants': [
                    'chart(bar, m[:, "X"], m[:, "Y"], title "Title")',
                    'chart(bar, m[:, "X"], m[:, "Y"], color "red")',
                    'chart(bar, m[:, "X"], m[:, "Y"], save "chart.png")',
                ],
            },
        },
    },
}