# syntax/autocomplete/items_excel.py
"""
Описания функций Excel: OpenExcel, SaveExcel, OpenExcelShow, SaveExcelShow.
"""

RU = {
    'OpenExcel': {
        'signature': 'OpenExcel("file.xlsx" [, лист])',
        'description': (
            'Загрузка из Excel.\n'
            '  • без листа — первый лист\n'
            '  • "Лист1" — по имени\n'
            '  • 1, 2, ... — по номеру\n'
            '  • all — все листы подряд'
        ),
        'example': (
            'm = OpenExcel("data.xlsx")\n'
            'm = OpenExcel("data.xlsx", "Продажи")\n'
            'm = OpenExcel("data.xlsx", 1)\n'
            'm = OpenExcel("data.xlsx", all)'
        ),
    },
    'SaveExcel': {
        'signature': 'SaveExcel(данные, "file.xlsx" [, "Лист1"])',
        'description': (
            'Сохранение в Excel.\n'
            '  • если файл новый — быстро (pyexcelerate)\n'
            '  • если файл есть — дописывает лист (openpyxl)'
        ),
        'example': (
            'SaveExcel(m, "out.xlsx")\n'
            'SaveExcel(m, "out.xlsx", "Результат")'
        ),
    },
    'OpenExcelShow': {
        'signature': 'OpenExcelShow([all])',
        'description': 'Диалог выбора Excel + выбор листов.',
        'example': (
            'm = OpenExcelShow()\n'
            'm = OpenExcelShow(all)'
        ),
    },
    'SaveExcelShow': {
        'signature': 'SaveExcelShow(данные [, "Лист1"])',
        'description': 'Диалог сохранения в Excel.',
        'example': 'SaveExcelShow(m, "Результат")',
    },
}


EN = {
    'OpenExcel': {
        'signature': 'OpenExcel("file.xlsx" [, sheet])',
        'description': (
            'Load from Excel.\n'
            '  • no sheet — first sheet\n'
            '  • "Sheet1" — by name\n'
            '  • 1, 2, ... — by number\n'
            '  • all — all sheets in a row'
        ),
        'example': (
            'm = OpenExcel("data.xlsx")\n'
            'm = OpenExcel("data.xlsx", "Sales")\n'
            'm = OpenExcel("data.xlsx", 1)\n'
            'm = OpenExcel("data.xlsx", all)'
        ),
    },
    'SaveExcel': {
        'signature': 'SaveExcel(data, "file.xlsx" [, "Sheet1"])',
        'description': (
            'Save to Excel.\n'
            '  • new file — fast (pyexcelerate)\n'
            '  • existing file — adds a sheet (openpyxl)'
        ),
        'example': (
            'SaveExcel(m, "out.xlsx")\n'
            'SaveExcel(m, "out.xlsx", "Result")'
        ),
    },
    'OpenExcelShow': {
        'signature': 'OpenExcelShow([all])',
        'description': 'Dialog for Excel file + sheet selection.',
        'example': (
            'm = OpenExcelShow()\n'
            'm = OpenExcelShow(all)'
        ),
    },
    'SaveExcelShow': {
        'signature': 'SaveExcelShow(data [, "Sheet1"])',
        'description': 'Dialog for saving to Excel.',
        'example': 'SaveExcelShow(m, "Result")',
    },
}