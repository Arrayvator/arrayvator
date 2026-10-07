# parser/parse_functions/numseq.py
"""
Парсинг range / Number.

ФОРМАТЫ:
    range(N)
    range(end)
    range(a:b)
    range(a:b, step S)
    range(2:end)
    range(2:end, step S)

    Number(N)
    Number(end)
    Number(a:b, step S)
    Number(2:end)
"""

from ast_nodes.functions.numseq import NumberSeqNode
from ast_nodes.literals import StringNode, NumberNode
from errors import ArrayVatorError


def parse_numseq(self):
    """Парсит range(...) или Number(...)."""
    self.expect('LPAREN')

    # ============================================================
    # 1. Первый аргумент: число, end или выражение
    # ============================================================
    token = self.peek()
    if token is None:
        raise ArrayVatorError(
            code="NUMSEQ_BAD_SYNTAX",
            context=self._get_context(),
            message="range / Number: пустой вызов.",
        )

    # ------------------------------------------------------------
    # range(end)  — от 1 до конца целевого среза
    # range(end:N) — не поддерживаем, это нелогично
    # ------------------------------------------------------------
    if token[0] == 'END_KEYWORD':
        self.pos += 1

        # range(end)
        if self.check('RPAREN'):
            self.pos += 1
            return NumberSeqNode(
                mode='range',
                start_node=NumberNode(1),
                end_node=StringNode('end'),
                step_node=None,
            )

        # range(end: ...) — не поддерживаем
        raise ArrayVatorError(
            code="NUMSEQ_BAD_SYNTAX",
            context=self._get_context(),
            message=(
                "range / Number: 'end' может быть только вторым.\n"
                "  Допустимо: range(end)\n"
                "             range(2:end)"
            ),
        )

    # ------------------------------------------------------------
    # range(end-N) — тоже поддерживаем как «от 1 до end-N»
    # ------------------------------------------------------------
    if token[0] == 'END_MINUS':
        self.pos += 1
        end_val = token[1]  # строка вида 'end-2'

        if self.check('RPAREN'):
            self.pos += 1
            return NumberSeqNode(
                mode='range',
                start_node=NumberNode(1),
                end_node=StringNode(end_val),
                step_node=None,
            )

        raise ArrayVatorError(
            code="NUMSEQ_BAD_SYNTAX",
            context=self._get_context(),
            message=(
                "range / Number: после end-N ожидается ')'.\n"
                "  Допустимо: range(end-5)"
            ),
        )

    # ============================================================
    # 2. Обычный первый аргумент: число / выражение
    # ============================================================
    first_node = self.parse_expression()

    # ============================================================
    # 3. Проверяем следующий токен
    # ============================================================
    if self.check('COLON'):
        # Диапазон a:b
        self.expect('COLON')
        end_node = _parse_range_end(self)
        step_node = _parse_optional_step(self)
        self.expect('RPAREN')

        return NumberSeqNode(
            mode='range',
            start_node=first_node,
            end_node=end_node,
            step_node=step_node,
        )

    # ============================================================
    # 4. Одиночное N → range(N)
    # ============================================================
    if self.check('RPAREN'):
        self.expect('RPAREN')
        return NumberSeqNode(
            mode='simple',
            n_node=first_node,
        )

    # ============================================================
    # 5. Ошибка: step без диапазона
    # ============================================================
    if self.check('COMMA'):
        save_pos = self.pos
        self.expect('COMMA')
        if self.check('STEP'):
            raise ArrayVatorError(
                code="NUMSEQ_STEP_WITHOUT_RANGE",
                context=self._get_context(),
                message=(
                    "range / Number: range(10, step 2) — неверно.\n"
                    "  Укажите диапазон: range(1:10, step 2)\n"
                    "  Или просто:       range(10)"
                ),
            )
        self.pos = save_pos

    raise ArrayVatorError(
        code="NUMSEQ_BAD_SYNTAX",
        context=self._get_context(),
        message=(
            "range / Number: неверный синтаксис.\n"
            "  Допустимо:\n"
            "     range(10)\n"
            "     range(end)\n"
            "     range(2:end)\n"
            "     range(1:10)\n"
            "     range(1:10, step 2)"
        ),
    )


# ============================================================
# ХЕЛПЕРЫ
# ============================================================
def _parse_range_end(self):
    """Парсит конец диапазона: число, end, end-N, end+N, выражение."""
    token = self.peek()

    if token is None:
        raise ArrayVatorError(
            code="NUMSEQ_MISSING_END",
            context=self._get_context(),
            message="range / Number: не указан конец диапазона.",
        )

    if token[0] == 'END_KEYWORD':
        self.pos += 1
        return StringNode('end')

    if token[0] == 'END_MINUS':
        self.pos += 1
        return StringNode(token[1])

    if token[0] == 'END_PLUS':
        self.pos += 1
        return StringNode(token[1])

    if token[0] == 'IDENTIFIER' and token[1].lower() == 'end':
        self.pos += 1
        return StringNode('end')

    return self.parse_expression()


def _parse_optional_step(self):
    """Парсит опциональный `, step N`. Возвращает узел или None."""
    if not self.check('COMMA'):
        return None

    self.expect('COMMA')

    if not self.check('STEP'):
        raise ArrayVatorError(
            code="NUMSEQ_EXPECTED_STEP",
            context=self._get_context(),
            message=(
                "range / Number: после запятой ожидается 'step N'.\n"
                "  Пример: range(1:10, step 2)"
            ),
        )

    self.expect('STEP')
    return self.parse_expression()