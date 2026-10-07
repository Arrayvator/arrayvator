# syntax/autocomplete/items_parquet.py
"""
Описания функций Parquet: OpenParquet, SaveParquet.
"""

RU = {
    'OpenParquet': {
        'signature': 'OpenParquet("file.parquet")',
        'description': 'Загрузка из Parquet (DuckDB, потоково). 10x быстрее CSV.',
        'example': 'm = OpenParquet("data.parquet")',
    },
    'SaveParquet': {
        'signature': 'SaveParquet(данные, "file.parquet")',
        'description': 'Сохранение в Parquet (сжатие 5-10x).',
        'example': 'SaveParquet(m, "out.parquet")',
    },
}


EN = {
    'OpenParquet': {
        'signature': 'OpenParquet("file.parquet")',
        'description': 'Load from Parquet (DuckDB, streamed). 10x faster than CSV.',
        'example': 'm = OpenParquet("data.parquet")',
    },
    'SaveParquet': {
        'signature': 'SaveParquet(data, "file.parquet")',
        'description': 'Save to Parquet (compression 5-10x).',
        'example': 'SaveParquet(m, "out.parquet")',
    },
}