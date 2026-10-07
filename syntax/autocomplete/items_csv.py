# syntax/autocomplete/items_csv.py
"""
Описания функций CSV: OpenCSV, SaveCSV, OpenCSVShow, SaveCSVShow.
"""

RU = {
    'OpenCSV': {
        'signature': 'OpenCSV("file.csv" [, BigData | Table])',
        'description': (
            'Загрузка из CSV.\n'
            '  • без режима — авто (по размеру файла)\n'
            '  • BigData — принудительно DuckDB (до 1 млрд строк)\n'
            '  • Table — принудительно RAM (MatrExMatrix)'
        ),
        'example': (
            'm = OpenCSV("data.csv")              # авто\n'
            'm = OpenCSV("big.csv", BigData)      # DuckDB\n'
            'm = OpenCSV("small.csv", Table)      # RAM'
        ),
    },
    'SaveCSV': {
        'signature': 'SaveCSV(данные, "file.csv")',
        'description': 'Сохранение в CSV.',
        'example': 'SaveCSV(m, "out.csv")',
    },
    'OpenCSVShow': {
        'signature': 'OpenCSVShow([BigData | Table])',
        'description': 'Диалог выбора CSV-файла.',
        'example': 'm = OpenCSVShow()',
    },
    'SaveCSVShow': {
        'signature': 'SaveCSVShow(данные)',
        'description': 'Диалог сохранения в CSV.',
        'example': 'SaveCSVShow(m)',
    },
}


EN = {
    'OpenCSV': {
        'signature': 'OpenCSV("file.csv" [, BigData | Table])',
        'description': (
            'Load from CSV.\n'
            '  • no mode — auto (by file size)\n'
            '  • BigData — force DuckDB (up to 1 billion rows)\n'
            '  • Table — force RAM (MatrExMatrix)'
        ),
        'example': (
            'm = OpenCSV("data.csv")              # auto\n'
            'm = OpenCSV("big.csv", BigData)      # DuckDB\n'
            'm = OpenCSV("small.csv", Table)      # RAM'
        ),
    },
    'SaveCSV': {
        'signature': 'SaveCSV(data, "file.csv")',
        'description': 'Save to CSV.',
        'example': 'SaveCSV(m, "out.csv")',
    },
    'OpenCSVShow': {
        'signature': 'OpenCSVShow([BigData | Table])',
        'description': 'Dialog for selecting CSV file.',
        'example': 'm = OpenCSVShow()',
    },
    'SaveCSVShow': {
        'signature': 'SaveCSVShow(data)',
        'description': 'Dialog for saving to CSV.',
        'example': 'SaveCSVShow(m)',
    },
}