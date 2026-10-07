# syntax/autocomplete/items_logging.py
"""
Описания функций логирования: LogToFile, LogOff.
"""

RU = {
    'LogToFile': {
        'signature': 'LogToFile("file.txt" [, "all"|"matrix"|"summary"])',
        'description': 'Включает логирование.',
        'example': 'LogToFile("log.txt")',
    },
    'LogOff': {
        'signature': 'LogOff()',
        'description': 'Отключает логирование.',
        'example': 'LogOff()',
    },
}


EN = {
    'LogToFile': {
        'signature': 'LogToFile("file.txt" [, "all"|"matrix"|"summary"])',
        'description': 'Enable logging.',
        'example': 'LogToFile("log.txt")',
    },
    'LogOff': {
        'signature': 'LogOff()',
        'description': 'Disable logging.',
        'example': 'LogOff()',
    },
}