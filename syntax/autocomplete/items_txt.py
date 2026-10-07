# syntax/autocomplete/items_txt.py
"""
Описания функций TXT: OpenTXT, SaveTXT, OpenTXTShow, SaveTXTShow.
"""

RU = {
    'OpenTXT': {
        'signature': 'OpenTXT("file.txt" [, "разделитель"])',
        'description': 'Загрузка из TXT.',
        'example': 'm = OpenTXT("data.txt", ";")',
    },
    'SaveTXT': {
        'signature': 'SaveTXT(данные, "file.txt" [, "разделитель"])',
        'description': 'Сохранение в TXT.',
        'example': 'SaveTXT(m, "out.txt", "\\t")',
    },
    'OpenTXTShow': {
        'signature': 'OpenTXTShow([разделитель])',
        'description': 'Диалог выбора TXT-файла.',
        'example': 'm = OpenTXTShow()',
    },
    'SaveTXTShow': {
        'signature': 'SaveTXTShow(данные [, разделитель])',
        'description': 'Диалог сохранения в TXT.',
        'example': 'SaveTXTShow(m, ";")',
    },
}


EN = {
    'OpenTXT': {
        'signature': 'OpenTXT("file.txt" [, "delimiter"])',
        'description': 'Load from TXT.',
        'example': 'm = OpenTXT("data.txt", ";")',
    },
    'SaveTXT': {
        'signature': 'SaveTXT(data, "file.txt" [, "delimiter"])',
        'description': 'Save to TXT.',
        'example': 'SaveTXT(m, "out.txt", "\\t")',
    },
    'OpenTXTShow': {
        'signature': 'OpenTXTShow([delimiter])',
        'description': 'Dialog for selecting TXT file.',
        'example': 'm = OpenTXTShow()',
    },
    'SaveTXTShow': {
        'signature': 'SaveTXTShow(data [, delimiter])',
        'description': 'Dialog for saving to TXT.',
        'example': 'SaveTXTShow(m, ";")',
    },
}