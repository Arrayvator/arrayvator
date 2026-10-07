# parser/parse_functions/insertif.py
"""
Парсинг INSERTIF.

СИНТАКСИС:
    insertif(условие, before)
    insertif(условие, after)

ПРИМЕРЫ:
    r = insertif(m[:, "Отдел"] == "IT", after)
    r = insertif(m[:, "Возраст"] > 25, before)
    m = insertif(m[:, "Отдел"] == "IT", after)
    r = insertif(m[2:10, "Отдел"] == "IT", after)

ПРАВИЛА:
    - insertif работает ТОЛЬКО с Matrix (RAM).
    - NOT с DuckDB (BigData).
    - Направление указывается БЕЗ кавычек:
        Правильно: insertif(..., after)
        Правильно: insertif(..., before)
        Неправильно: insertif(..., "after")
"""

from ast_nodes.functions.insertif import InsertIfNode
from errors import ArrayVatorError


def parse_insertif(self):
    """Парсинг INSERTIF"""
    self.expect('LPAREN')

    # ============================================================
    # 1. Условие
    # ============================================================
    try:
        condition = self.parse_expression()
    except Exception:
        raise ArrayVatorError(
            code="INSERTIF_BAD_SYNTAX",
            context=self._get_context(),
        )

    # ============================================================
    # 2. Запятая
    # ============================================================
    if not self.check('COMMA'):
        raise ArrayVatorError(
            code="INSERTIF_BAD_SYNTAX",
            context=self._get_context(),
        )
    self.expect('COMMA')

    # ============================================================
    # 3. Направление (before | after) — БЕЗ кавычек
    # ============================================================
    dir_token = self.peek()

    # ------------------------------------------------------------
    # 3.1. Случай: "after" / "before" в кавычках → STRING
    # ------------------------------------------------------------
    if dir_token and dir_token[0] == 'STRING':
        val = str(dir_token[1]).strip().lower()
        if val in ('before', 'after'):
            raise ArrayVatorError(
                code="INSERTIF_MISSING_DIRECTION",
                context=self._get_context(dir_token),
            )

    # ------------------------------------------------------------
    # 3.2. Должен быть BEFORE или AFTER (ключевое слово)
    # ------------------------------------------------------------
    if not dir_token or dir_token[0] not in ('BEFORE', 'AFTER'):
        raise ArrayVatorError(
            code="INSERTIF_BAD_SYNTAX",
            context=self._get_context(dir_token),
        )

    direction = dir_token[1].lower()
    self.pos += 1

    # ============================================================
    # 4. Закрывающая скобка
    # ============================================================
    self.expect('RPAREN')

    return InsertIfNode(condition, direction)