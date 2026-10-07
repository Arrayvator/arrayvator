# syntax/signatures_data/calendar.py
"""
Сигнатуры calendar / calendarpro.
"""

SIGNATURES = {
    'calendar': {
        'name': 'calendar',
        'category': 'dates',
        'args': [
            'формат ("dd.mm.yyyy", "yyyy-mm-dd", ...)',
            'месяц: 1-12 или all',
            'год: 1981, 2026, datenow()',
        ],
        'examples': [
            'v = calendar("dd.mm.yyyy", 1, 2026)',
            'm = calendar("dd.mm.yyyy", all, 2026)',
            'v = calendar("yyyy-mm-dd", datenow(), datenow())',
        ],
    },
    'calendarpro': {
        'name': 'calendarpro',
        'category': 'dates',
        'args': [
            'год: 2026, datenow()',
            'месяц: 1-12 или all',
            'страна: "ru" | "en" (опц.)',
        ],
        'examples': [
            'm = calendarpro(2026, 1)',
            'm = calendarpro(2026, all)',
            'm = calendarpro(datenow(), datenow())',
        ],
    },
}