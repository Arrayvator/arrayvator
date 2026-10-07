# errors/functions_db/search.py
"""
База ошибок для vlookup и find.
"""

RU = {
    'vlookup': {
        'name': 'vlookup',
        'category': 'search',
        'signature': 'vlookup(где_искать, что_искать, что_возвращать)',
        'description': (
            'Аналог ВПР. Ищет значения в справочнике.\n'
            '\n'
            'МНЕМОНИКА:\n'
            '     vlookup( где_искать,  что_искать,  что_возвращать )\n'
            '             └── a ───┘  └── b ───┘  └── a ───┘\n'
            '             справочник    запрос      справочник\n'
            '\n'
            '  1-й и 3-й — из ОДНОЙ таблицы (справочника).\n'
            '  2-й — из ЛЮБОЙ таблицы (источник запроса).'
        ),
        'examples': [
            'r = vlookup(a[:, "ID"], 101, a[:, "Отдел"])',
            'b[:, end+1] = vlookup(a[:, "ID"], b[:, "ID"], a[:, "Отдел"])',
        ],
        'errors': {
            'VLOOKUP_BAD_SEARCH_SLICE': {
                'message': (
                    "vlookup: 1-й аргумент — срез столбца поиска."
                ),
                'wrong': 'vlookup(a, 101, a[:, "Отдел"])',
                'right': 'vlookup(a[:, "ID"], 101, a[:, "Отдел"])',
                'explanation': (
                    "1-й аргумент — СРЕЗ столбца-ключа в справочнике.\n"
                    "\n"
                    "Правильно:\n"
                    "     vlookup(a[:, \"ID\"], 101, a[:, \"Отдел\"])"
                ),
                'variants': [
                    'vlookup(a[:, "ID"], 101, a[:, "Отдел"])',
                    'vlookup(a[:, 1], 101, a[:, 3])',
                ],
            },
            'VLOOKUP_BAD_RETURN_SLICE': {
                'message': (
                    "vlookup: 3-й аргумент — срез столбца возврата."
                ),
                'wrong': 'vlookup(a[:, "ID"], 101, "Отдел")',
                'right': 'vlookup(a[:, "ID"], 101, a[:, "Отдел"])',
                'explanation': (
                    "3-й аргумент — СРЕЗ столбца значений справочника.\n"
                    "\n"
                    "Правильно:\n"
                    "     vlookup(a[:, \"ID\"], 101, a[:, \"Отдел\"])"
                ),
                'variants': [
                    'vlookup(a[:, "ID"], 101, a[:, "Отдел"])',
                    'vlookup(a[:, 1], 101, a[:, 3])',
                ],
            },
        },
    },
}


EN = {
    'vlookup': {
        'name': 'vlookup',
        'category': 'search',
        'signature': 'vlookup(where_lookup, what_search, what_return)',
        'description': (
            'VLOOKUP analog. Searches values in a lookup table.\n'
            '\n'
            'MNEMONIC:\n'
            '     vlookup( where_lookup,  what_search,  what_return )\n'
            '              └─── a ────┘  └─── b ────┘  └─── a ────┘\n'
            '              lookup table    query        lookup table\n'
            '\n'
            '  1st and 3rd — from the SAME table (lookup).\n'
            '  2nd — from ANY table (source of query).'
        ),
        'examples': [
            'r = vlookup(a[:, "ID"], 101, a[:, "Dept"])',
            'b[:, end+1] = vlookup(a[:, "ID"], b[:, "ID"], a[:, "Dept"])',
        ],
        'errors': {
            'VLOOKUP_BAD_SEARCH_SLICE': {
                'message': "vlookup: 1st argument — slice of the key column.",
                'wrong': 'vlookup(a, 101, a[:, "Dept"])',
                'right': 'vlookup(a[:, "ID"], 101, a[:, "Dept"])',
                'explanation': (
                    "1st argument is a SLICE of the key column in the lookup table.\n"
                    "\n"
                    "Correct:\n"
                    "     vlookup(a[:, \"ID\"], 101, a[:, \"Dept\"])"
                ),
                'variants': [
                    'vlookup(a[:, "ID"], 101, a[:, "Dept"])',
                    'vlookup(a[:, 1], 101, a[:, 3])',
                ],
            },
            'VLOOKUP_BAD_RETURN_SLICE': {
                'message': "vlookup: 3rd argument — slice of the value column.",
                'wrong': 'vlookup(a[:, "ID"], 101, "Dept")',
                'right': 'vlookup(a[:, "ID"], 101, a[:, "Dept"])',
                'explanation': (
                    "3rd argument is a SLICE of the value column in the lookup table.\n"
                    "\n"
                    "Correct:\n"
                    "     vlookup(a[:, \"ID\"], 101, a[:, \"Dept\"])"
                ),
                'variants': [
                    'vlookup(a[:, "ID"], 101, a[:, "Dept"])',
                    'vlookup(a[:, 1], 101, a[:, 3])',
                ],
            },
        },
    },
}