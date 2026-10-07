# parser/parse_functions/vlookup.py
"""
Парсинг VLOOKUP (только программист).

СИНТАКСИС:
    vlookup(срез_поиска, что_искать, срез_возврата)

МНЕМОНИКА:
    vlookup( где_искать, что_искать, что_возвращать )
             └── a ───┘  └── b ───┘  └── a ───┘
             справочник    запрос     справочник

ПРАВИЛА:
    - 1-й аргумент — срез столбца-ключа в справочнике (a).
    - 2-й аргумент — что искать: скаляр или вектор.
    - 3-й аргумент — срез столбца возврата в справочнике (a).
    - 1-й и 3-й — из ОДНОЙ таблицы (справочника).
    - 2-й — из ЛЮБОЙ таблицы (источник запроса).

ПРИМЕРЫ:
    # Скаляр
    r = vlookup(a[:, "ID"], 101, a[:, "Отдел"])
    # → "IT"

    # Вектор (обогащение таблицы b)
    b[:, end+1] = vlookup(a[:, "ID"], b[:, "ID"], a[:, "Отдел"])

    # По имени
    r = vlookup(a[:, "Имя"], "Аня", a[:, "Отдел"])
"""

from ast_nodes import VLookupNode
from ast_nodes.index import IndexNode
from errors import ArrayVatorError


def parse_vlookup(self):
    """Парсинг VLOOKUP."""
    self.expect('LPAREN')

    # ============================================================
    # 1. Срез поиска (справочник)
    # ============================================================
    search_slice = self.parse_primary()
    if not isinstance(search_slice, IndexNode):
        raise ArrayVatorError(
            code="VLOOKUP_BAD_SEARCH_SLICE",
            context=self._get_context(),
            message=(
                "vlookup: 1-й аргумент — срез столбца поиска.\n"
                "  Пример: vlookup(a[:, \"ID\"], ...)"
            ),
            suggestion=(
                "Синтаксис:\n"
                "     vlookup(где_искать, что_искать, что_возвращать)\n"
                "             └── a ──┘   └── b ──┘   └── a ──┘\n"
                "             справочник  запрос     справочник\n"
                "\n"
                "Пример:\n"
                "     vlookup(a[:, \"ID\"], b[:, \"ID\"], a[:, \"Отдел\"])"
            ),
        )

    self.expect('COMMA')

    # ============================================================
    # 2. Что искать (скаляр или вектор)
    # ============================================================
    search_val = self.parse_expression()

    self.expect('COMMA')

    # ============================================================
    # 3. Срез возврата (справочник)
    # ============================================================
    return_slice = self.parse_primary()
    if not isinstance(return_slice, IndexNode):
        raise ArrayVatorError(
            code="VLOOKUP_BAD_RETURN_SLICE",
            context=self._get_context(),
            message=(
                "vlookup: 3-й аргумент — срез столбца возврата.\n"
                "  Пример: vlookup(a[:, \"ID\"], b[:, \"ID\"], a[:, \"Отдел\"])"
            ),
            suggestion=(
                "Синтаксис:\n"
                "     vlookup(где_искать, что_искать, что_возвращать)\n"
                "\n"
                "Пример:\n"
                "     vlookup(a[:, \"ID\"], b[:, \"ID\"], a[:, \"Отдел\"])"
            ),
        )

    self.expect('RPAREN')

    return VLookupNode(search_val, search_slice, return_slice)