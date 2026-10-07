# syntax/signatures_data/strings.py
"""
Сигнатуры строковых функций.
"""

SIGNATURES = {
    'deletetextleft': {
        'name': 'deletetextleft',
        'category': 'string',
        'args': ['данные', 'N'],
        'examples': [
            'r = deletetextleft("PR-001", 3)',
            'm = deletetextleft(m[:, "Код"], 4)',
        ],
    },

    'deletetextright': {
        'name': 'deletetextright',
        'category': 'string',
        'args': ['данные', 'N'],
        'examples': [
            'r = deletetextright("PR-001", 2)',
            'm = deletetextright(m[:, "Город"], 2)',
        ],
    },

    'trim': {
        'name': 'trim',
        'category': 'string',
        'args': ['данные', '"символы" (опц.)'],
        'examples': [
            'r = trim("  hello  ")               # "hello"',
            'm = trim(m[:, "Имя"])',
            'm = trim(m[:, "Телефон"], "+- ()")',
        ],
    },

    'trimleft': {
        'name': 'trimleft',
        'category': 'string',
        'args': ['данные', '"символы" (опц.)'],
        'examples': [
            'r = trimleft("  hello")             # "hello"',
            'm = trimleft(m[:, "Код"], "0")',
        ],
    },

    'trimright': {
        'name': 'trimright',
        'category': 'string',
        'args': ['данные', '"символы" (опц.)'],
        'examples': [
            'r = trimright("hello  ")            # "hello"',
            'm = trimright(m[:, "Хвост"], "0")',
        ],
    },

    'replacetext': {
        'name': 'replacetext',
        'category': 'string',
        'args': ['данные', '"что"', '"на_что"', 'ignore (опц.)'],
        'examples': [
            'r = replacetext("Hello", "l", "L")',
            'r = replacetext(m, "IT", "--")',
            'm = replacetext(m[:, "Отдел"], "IT", "--")',
            'm = replacetext(m, "it", "--", ignore)',
        ],
    },

    'split': {
        'name': 'split',
        'category': 'string',
        'args': ['текст', 'разделитель (опц.)', 'skip (опц.)'],
        'examples': [
            'r = split("a,b,c", ",")',
            'r = split("Hello")',
            'r = split("a,,b", ",", skip)',
        ],
    },

    'join': {
        'name': 'join',
        'category': 'string',
        'args': ['вектор', 'разделитель (опц.)'],
        'examples': ['r = join(["a","b"], "-")', 'r = join(v)'],
    },

    'clean': {
        'name': 'clean',
        'category': 'string',
        'args': ['данные', '"digits" | "letters" | "special" | "alnum"'],
        'examples': [
            'r = clean("a1b2c3", "digits")',
            'm = clean(m[:, "Код"], "digits")',
        ],
    },
}