# syntax/signatures_data/numseq.py
"""
Сигнатуры функций range / Number.
"""

SIGNATURES = {
    'range': {
        'name': 'range',
        'category': 'create',
        'args': [
            'N',
            'a:b',
            'a:b, step S',
            'end | 2:end | end-2',
        ],
        'examples': [
            'm = matrix(5, 1)',
            'm[:, 1] = range(5)                # [1,2,3,4,5]',
            'm[:, 1] = range(1:10, step 2)     # [1,3,5,7,9]',
            'm[:, 1] = range(10:1, step -1)    # [10,9,...,1]',
            'm[2:end, 1] = range(2:end)',
        ],
    },

    'number': {
        'name': 'Number',
        'category': 'create',
        'args': [
            'N',
            'a:b',
            'a:b, step S',
        ],
        'examples': [
            'm = matrix(41, 1)',
            'm[:, 1] = Number(-10:10, step 0.5)',
        ],
    },
}