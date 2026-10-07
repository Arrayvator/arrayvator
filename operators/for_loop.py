# operators/for_loop.py
"""
Цикл FOR.

СИНТАКСИС:
    for i = 1 to 10 do
    {
        команды
    }

    for i = 1 to 10 do команда

    for i = 10 to 1 do { ... }         # обратный (шаг -1)
    for i = 1 to 10 step 2 do { ... }  # с шагом

ОБА КОНЦА ВКЛЮЧИТЕЛЬНО:
    for i = 1 to 5 do print(i)   # 1 2 3 4 5
"""

from ast_nodes import Node, VariableNode
from runtime.random_source import forbid_random
from .break_stmt import BreakException
from errors import ArrayVatorError


# ============================================================
# ХЕЛПЕР: проверка на 'end' в for
# ============================================================
def _is_bare_end(node):
    """
    Проверяет, что узел — это чистое ключевое слово 'end'.

    Возвращает True, если:
      • VariableNode с именем 'end'
      • StringNode со значением 'end'

    НЕ возвращает True для:
      • end-1, end+2, last 3 — это отдельные конструкции
      • 'end' внутри выражений (например, 'myend' — это переменная)
    """
    if node is None:
        return False

    # VariableNode('end')
    if hasattr(node, 'name'):
        name = getattr(node, 'name', '')
        if isinstance(name, str) and name.lower() == 'end':
            return True

    # StringNode('end')
    if hasattr(node, 'value'):
        value = getattr(node, 'value', '')
        if isinstance(value, str) and value.lower() == 'end':
            return True

    return False


class ForNode(Node):
    def __init__(self, var_name, start, end, step=None, body=None):
        self.var_name = var_name.lower()
        self.start = start
        self.end = end
        self.step = step
        self.body = body or []

    def _get_length(self, value):
        if hasattr(value, 'rows') and hasattr(value, 'cols'):
            return value.rows if value.is_2d else len(value.data)
        if isinstance(value, list):
            return len(value)
        if isinstance(value, (int, float)):
            return int(value)
        if isinstance(value, str):
            try:
                return int(value)
            except ValueError:
                raise TypeError(f"Нельзя определить длину для '{value}'")
        raise TypeError(f"Нельзя определить длину для типа {type(value)}")

    def execute(self, env):
        # --- Начало ---
        start_val = self.start.evaluate(env)
        forbid_random(start_val, "for")
        start_int = int(start_val)

        # --- Конец ---
        if isinstance(self.end, VariableNode):
            try:
                var_value = env.get(self.end.name)
                end_val = self._get_length(var_value)
            except NameError:
                end_val = self.end.evaluate(env)
                forbid_random(end_val, "for")
        else:
            end_val = self.end.evaluate(env)
            forbid_random(end_val, "for")

        end_int = int(end_val)

        # --- Шаг ---
        step_int = None
        if self.step is not None:
            step_val = self.step.evaluate(env)
            forbid_random(step_val, "for")
            step_int = int(step_val)

        # --- Проверки ---
        if start_int < 1:
            raise IndexError(
                f"Начальный индекс должен быть >= 1, получен {start_int}"
            )
        if end_int < 1:
            raise IndexError(
                f"Конечный индекс должен быть >= 1, получен {end_int}"
            )
        if step_int == 0:
            raise ValueError("for: step не может быть 0")

        # --- Диапазон ---
        if step_int is None:
            if start_int <= end_int:
                rng = range(start_int, end_int + 1)
            else:
                rng = range(start_int, end_int - 1, -1)
        else:
            if step_int > 0:
                rng = range(start_int, end_int + 1, step_int)
            else:
                rng = range(start_int, end_int - 1, step_int)

        # --- Выполнение ---
        try:
            for i in rng:
                env.set(self.var_name, i)
                for stmt in self.body:
                    stmt.execute(env)
        except BreakException:
            pass

    def __repr__(self):
        if self.step is not None:
            return (f"For({self.var_name} = {self.start} to {self.end} "
                    f"step {self.step}, body={len(self.body)})")
        return f"For({self.var_name} = {self.start} to {self.end}, body={len(self.body)})"


# ============================================================
# ПАРСЕР
# ============================================================
def parse_for(parser):
    """
    Парсит:
        for i = 1 to 10 do { ... }
        for i = 1 to 10 do команда
        for i = 1 to 10 step 2 do { ... }
    """
    parser.expect('FOR')

    # ============================================================
    # ПРОВЕРКА 1: СТАРЫЙ СИНТАКСИС for i(1:10)
    # ============================================================
    # Если после FOR идёт IDENTIFIER, а потом сразу LPAREN — это старый синтаксис
    if parser.check('IDENTIFIER'):
        save_pos = parser.pos
        parser.pos += 1  # пропускаем переменную
        if parser.check('LPAREN'):
            parser.pos = save_pos
            raise ArrayVatorError(
                code="FOR_OLD_SYNTAX",
                context=parser._get_context(),
            )
        parser.pos = save_pos

    # ============================================================
    # ПРОВЕРКА 2: 'in' вместо '=' (Python-стиль)
    # ============================================================
    if parser.check('IDENTIFIER'):
        save_pos = parser.pos
        parser.pos += 1
        if parser.check('IDENTIFIER') and parser.peek()[1].lower() == 'in':
            parser.pos = save_pos
            raise ArrayVatorError(
                code="FOR_IN_SYNTAX",
                context=parser._get_context(),
            )
        parser.pos = save_pos

    # ============================================================
    # ПЕРЕМЕННАЯ
    # ============================================================
    var_token = parser.peek()
    if not var_token or var_token[0] != 'IDENTIFIER':
        raise ArrayVatorError(
            code="FOR_BAD_VAR",
            context=parser._get_context(var_token),
        )
    var_name = parser.expect('IDENTIFIER')[1]

    # ============================================================
    # '='
    # ============================================================
    if not parser.check('ASSIGN'):
        raise ArrayVatorError(
            code="FOR_NO_ASSIGN",
            context=parser._get_context(),
        )
    parser.expect('ASSIGN')

    # ============================================================
    # НАЧАЛО
    # ============================================================
    start = parser.parse_expression()

    # ============================================================
    # 'to'
    # ============================================================
    if not parser.check('TO'):
        raise ArrayVatorError(
            code="FOR_NO_TO",
            context=parser._get_context(),
        )
    parser.expect('TO')

    # ============================================================
    # КОНЕЦ
    # ============================================================
    end = parser.parse_expression()

    # ============================================================
    # ПРОВЕРКА: 'end' в for запрещён
    # ============================================================
    if _is_bare_end(end):
        raise ArrayVatorError(
            code="FOR_END_KEYWORD",
            context=parser._get_context(),
        )

    # ============================================================
    # step (опционально)
    # ============================================================
    step = None
    if parser.check('STEP'):
        parser.expect('STEP')
        step = parser.parse_expression()

    # ============================================================
    # 'do'
    # ============================================================
    if not parser.check('DO'):
        raise ArrayVatorError(
            code="FOR_NO_DO",
            context=parser._get_context(),
        )
    parser.expect('DO')

    # ============================================================
    # ТЕЛО
    # ============================================================
    body = []
    if parser.check('LBRACE'):
        parser.expect('LBRACE')
        while not parser.check('RBRACE') and parser.peek():
            stmt = parser.parse_statement()
            if stmt:
                body.append(stmt)
        parser.expect('RBRACE')
    else:
        stmt = parser.parse_statement()
        if stmt:
            body.append(stmt)

    return ForNode(var_name, start, end, step, body)