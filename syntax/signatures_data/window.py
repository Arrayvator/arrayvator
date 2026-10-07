# syntax/signatures_data/window.py
"""
Сигнатуры оконных функций.
"""

SIGNATURES = {
    'rownumber': {
        'name': 'rownumber',
        'category': 'window',
        'args': ['таблица', 'by срез (опц.)', 'order срез (опц.)', 'AZ | ZA'],
        'examples': [
            'r = rownumber(m, by m[:, "Отдел"], order m[:, "Зарплата"], ZA)',
        ],
    },

    'rank': {
        'name': 'rank',
        'category': 'window',
        'args': ['таблица', 'by срез (опц.)', 'order срез (опц.)', 'AZ | ZA'],
        'examples': [
            'r = rank(m, by m[:, "Отдел"], order m[:, "Зарплата"], ZA)',
        ],
    },

    'denserank': {
        'name': 'denserank',
        'category': 'window',
        'args': ['таблица', 'by срез (опц.)', 'order срез (опц.)', 'AZ | ZA'],
        'examples': [
            'r = denserank(m, by m[:, "Отдел"], order m[:, "Зарплата"], ZA)',
        ],
    },

    'percentrank': {
        'name': 'percentrank',
        'category': 'window',
        'args': ['таблица', 'by срез (опц.)', 'order срез (опц.)', 'AZ | ZA'],
        'examples': [
            'r = percentrank(m, by m[:, "Отдел"], order m[:, "Зарплата"], ZA)',
        ],
    },

    'cumedist': {
        'name': 'cumedist',
        'category': 'window',
        'args': ['таблица', 'by срез (опц.)', 'order срез (опц.)', 'AZ | ZA'],
        'examples': [
            'r = cumedist(m, by m[:, "Отдел"], order m[:, "Зарплата"], ZA)',
        ],
    },

    'ntile': {
        'name': 'ntile',
        'category': 'window',
        'args': ['таблица', 'N', 'by срез (опц.)', 'order срез (опц.)', 'AZ | ZA'],
        'examples': [
            'r = ntile(m, 4, by m[:, "Отдел"], order m[:, "Зарплата"], ZA)',
        ],
    },

    'lag': {
        'name': 'lag',
        'category': 'window',
        'args': ['срез', 'offset (опц.)', 'default (опц.)', 'by ...', 'order ...'],
        'examples': [
            'r = lag(m[:, "Зарплата"], 1, 0)',
        ],
    },

    'lead': {
        'name': 'lead',
        'category': 'window',
        'args': ['срез', 'offset (опц.)', 'default (опц.)', 'by ...', 'order ...'],
        'examples': [
            'r = lead(m[:, "Зарплата"], 1, 0)',
        ],
    },

    'firstvalue': {
        'name': 'firstvalue',
        'category': 'window',
        'args': ['срез', 'by ...', 'order ...', 'AZ | ZA'],
        'examples': [
            'r = firstvalue(m[:, "Зарплата"], by m[:, "Отдел"], order m[:, "Дата"], AZ)',
        ],
    },

    'lastvalue': {
        'name': 'lastvalue',
        'category': 'window',
        'args': ['срез', 'by ...', 'order ...', 'AZ | ZA'],
        'examples': [
            'r = lastvalue(m[:, "Зарплата"], by m[:, "Отдел"], order m[:, "Дата"], AZ)',
        ],
    },

    'nthvalue': {
        'name': 'nthvalue',
        'category': 'window',
        'args': ['срез', 'N', 'by ...', 'order ...', 'AZ | ZA'],
        'examples': [
            'r = nthvalue(m[:, "Зарплата"], 2, by m[:, "Отдел"], order m[:, "Дата"], AZ)',
        ],
    },

    'winsum': {
        'name': 'winsum',
        'category': 'window',
        'args': ['срез', 'by ... (опц.)', 'order ... (опц.)'],
        'examples': [
            'r = winsum(m[:, "Зарплата"], by m[:, "Отдел"])',
        ],
    },

    'winavg': {
        'name': 'winavg',
        'category': 'window',
        'args': ['срез', 'by ... (опц.)', 'order ... (опц.)'],
        'examples': [
            'r = winavg(m[:, "Зарплата"], by m[:, "Отдел"])',
        ],
    },

    'wincount': {
        'name': 'wincount',
        'category': 'window',
        'args': ['срез', 'by ... (опц.)', 'order ... (опц.)'],
        'examples': [
            'r = wincount(m[:, "Зарплата"], by m[:, "Отдел"])',
        ],
    },

    'winmin': {
        'name': 'winmin',
        'category': 'window',
        'args': ['срез', 'by ... (опц.)', 'order ... (опц.)'],
        'examples': [
            'r = winmin(m[:, "Зарплата"], by m[:, "Отдел"])',
        ],
    },

    'winmax': {
        'name': 'winmax',
        'category': 'window',
        'args': ['срез', 'by ... (опц.)', 'order ... (опц.)'],
        'examples': [
            'r = winmax(m[:, "Зарплата"], by m[:, "Отдел"])',
        ],
    },

    'winmedian': {
        'name': 'winmedian',
        'category': 'window',
        'args': ['срез', 'by ... (опц.)', 'order ... (опц.)'],
        'examples': [
            'r = winmedian(m[:, "Зарплата"], by m[:, "Отдел"])',
        ],
    },

    'winstdev': {
        'name': 'winstdev',
        'category': 'window',
        'args': ['срез', 'by ... (опц.)', 'order ... (опц.)'],
        'examples': [
            'r = winstdev(m[:, "Зарплата"], by m[:, "Отдел"])',
        ],
    },

    'qualify': {
        'name': 'qualify',
        'category': 'window',
        'args': ['таблица', 'оконная_функция ОП порог'],
        'examples': [
            'r = qualify(m, rownumber(m, by m[:, "Отдел"], order m[:, "Зарплата"], ZA) <= 3)',
        ],
    },
}