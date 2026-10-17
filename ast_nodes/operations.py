# ast_nodes/operations.py
from .base import Node
from runtime.random_source import forbid_random


# ============================================================
# ХЕЛПЕРЫ ТИПОВ
# ============================================================
def _is_vector(val):
    from runtime.matrix import MatrExMatrix
    return isinstance(val, MatrExMatrix) and not val.is_2d


def _is_matrix(val):
    from runtime.matrix import MatrExMatrix
    return isinstance(val, MatrExMatrix) and val.is_2d


def _is_scalar(val):
    return isinstance(val, (int, float, bool)) or val is None


def _is_number(val):
    return isinstance(val, (int, float)) and not isinstance(val, bool)


# ============================================================
# ХЕЛПЕР: ПОЭЛЕМЕНТНОЕ СРАВНЕНИЕ
# ============================================================
def _scalar_cmp(a, b, op):
    if a is None or b is None:
        if op == '==':
            return a is None and b is None
        if op == '!=':
            return not (a is None and b is None)
        return False

    try:
        if op == '==':  return a == b
        if op == '!=':  return a != b
        if op == '<':   return a < b
        if op == '>':   return a > b
        if op == '<=':  return a <= b
        if op == '>=':  return a >= b
    except TypeError:
        return False

    return False


def _compare(left, right, op):
    from runtime.matrix import MatrExMatrix

    left_vec = _is_vector(left)
    right_vec = _is_vector(right)

    if left_vec and right_vec:
        n = min(len(left.data), len(right.data))
        result = [_scalar_cmp(left.data[i], right.data[i], op) for i in range(n)]
        return MatrExMatrix(result, False)

    if left_vec:
        result = [_scalar_cmp(v, right, op) for v in left.data]
        return MatrExMatrix(result, False)

    if right_vec:
        result = [_scalar_cmp(left, v, op) for v in right.data]
        return MatrExMatrix(result, False)

    return _scalar_cmp(left, right, op)


# ============================================================
# ХЕЛПЕР: ЛОГИКА
# ============================================================
def _logic_and(left, right):
    from runtime.matrix import MatrExMatrix

    left_vec = _is_vector(left)
    right_vec = _is_vector(right)

    if left_vec and right_vec:
        n = min(len(left.data), len(right.data))
        return MatrExMatrix(
            [bool(left.data[i]) and bool(right.data[i]) for i in range(n)],
            False
        )

    if left_vec:
        return MatrExMatrix(
            [bool(v) and bool(right) for v in left.data],
            False
        )

    if right_vec:
        return MatrExMatrix(
            [bool(left) and bool(v) for v in right.data],
            False
        )

    return bool(left) and bool(right)


def _logic_or(left, right):
    from runtime.matrix import MatrExMatrix

    left_vec = _is_vector(left)
    right_vec = _is_vector(right)

    if left_vec and right_vec:
        n = min(len(left.data), len(right.data))
        return MatrExMatrix(
            [bool(left.data[i]) or bool(right.data[i]) for i in range(n)],
            False
        )

    if left_vec:
        return MatrExMatrix(
            [bool(v) or bool(right) for v in left.data],
            False
        )

    if right_vec:
        return MatrExMatrix(
            [bool(left) or bool(v) for v in right.data],
            False
        )

    return bool(left) or bool(right)


def _logic_not(value):
    from runtime.matrix import MatrExMatrix

    if _is_vector(value):
        return MatrExMatrix(
            [not bool(v) for v in value.data],
            False
        )
    return not bool(value)


# ============================================================
# ПОЭЛЕМЕНТНАЯ АРИФМЕТИКА
#
# ПРАВИЛА:
#   • скаляр + скаляр        → скаляр
#   • вектор + скаляр        → вектор
#   • скаляр + вектор        → вектор
#   • вектор + вектор        → вектор (min длины)
#   • матрица + скаляр       → матрица
#   • матрица + матрица      → матрица (min размеров)
#   • матрица + вектор       → матрица (вектор по столбцам)
#
#   • None в любом операнде  → None в результате
#   • деление / остаток на 0 → None
# ============================================================

def _safe_op(a, b, op):
    """
    Безопасная операция над двумя скалярами.
    Возвращает None, если:
        • a или b — None
        • деление/остаток/целочисленное деление на 0
        • тип не подходит
    """
    if a is None or b is None:
        return None

    try:
        if op == 'PLUS':
            if isinstance(a, str) or isinstance(b, str):
                return str(a) + str(b)
            return a + b

        if op == 'MINUS':
            if not _is_number(a) or not _is_number(b):
                return None
            return a - b

        if op == 'STAR':
            if isinstance(a, str) and isinstance(b, int):
                return a * b
            if isinstance(a, int) and isinstance(b, str):
                return a * b
            if not _is_number(a) or not _is_number(b):
                return None
            return a * b

        if op == 'SLASH':
            if not _is_number(a) or not _is_number(b):
                return None
            if b == 0:
                return None
            return a / b

        if op == 'MOD':
            if not _is_number(a) or not _is_number(b):
                return None
            if b == 0:
                return None
            return a % b

        if op == 'POW':
            if not _is_number(a) or not _is_number(b):
                return None
            try:
                return a ** b
            except (OverflowError, ValueError):
                return None

        if op == 'FLOORDIV':
            if not _is_number(a) or not _is_number(b):
                return None
            if b == 0:
                return None
            return a // b

    except ZeroDivisionError:
        return None
    except (TypeError, ValueError):
        return None

    return None


def _apply_arith(left, right, op):
    """
    Универсальный диспетчер арифметики.
    Работает со скалярами, векторами, матрицами.
    """
    from runtime.matrix import MatrExMatrix

    left_vec = _is_vector(left)
    right_vec = _is_vector(right)
    left_mat = _is_matrix(left)
    right_mat = _is_matrix(right)

    # ============================================================
    # 1. ОБА СКАЛЯРЫ
    # ============================================================
    if not (left_vec or right_vec or left_mat or right_mat):
        return _safe_op(left, right, op)

    # ============================================================
    # 2. ВЕКТОР ↔ ВЕКТОР
    # ============================================================
    if left_vec and right_vec:
        n = min(len(left.data), len(right.data))
        result = [_safe_op(left.data[i], right.data[i], op) for i in range(n)]
        return MatrExMatrix(result, False)

    # ============================================================
    # 3. ВЕКТОР ↔ СКАЛЯР
    # ============================================================
    if left_vec and _is_scalar(right):
        result = [_safe_op(v, right, op) for v in left.data]
        return MatrExMatrix(result, False)

    if _is_scalar(left) and right_vec:
        result = [_safe_op(left, v, op) for v in right.data]
        return MatrExMatrix(result, False)

    # ============================================================
    # 4. МАТРИЦА ↔ СКАЛЯР
    # ============================================================
    if left_mat and _is_scalar(right):
        result = []
        for row in left.data:
            result.append([_safe_op(v, right, op) for v in row])
        return MatrExMatrix(result, True)

    if _is_scalar(left) and right_mat:
        result = []
        for row in right.data:
            result.append([_safe_op(left, v, op) for v in row])
        return MatrExMatrix(result, True)

    # ============================================================
    # 5. МАТРИЦА ↔ МАТРИЦА
    # ============================================================
    if left_mat and right_mat:
        rows = min(left.rows, right.rows)
        cols = min(left.cols, right.cols)
        result = []
        for i in range(rows):
            new_row = []
            for j in range(cols):
                new_row.append(
                    _safe_op(left.data[i][j], right.data[i][j], op)
                )
            result.append(new_row)
        return MatrExMatrix(result, True)

    # ============================================================
    # 6. МАТРИЦА ↔ ВЕКТОР (вектор — по столбцам)
    # ============================================================
    if left_mat and right_vec:
        result = []
        for i in range(left.rows):
            row = left.data[i]
            new_row = []
            for j in range(left.cols):
                rv = right.data[j] if j < len(right.data) else None
                new_row.append(_safe_op(row[j], rv, op))
            result.append(new_row)
        return MatrExMatrix(result, True)

    if left_vec and right_mat:
        result = []
        for i in range(right.rows):
            row = right.data[i]
            new_row = []
            for j in range(right.cols):
                lv = left.data[j] if j < len(left.data) else None
                new_row.append(_safe_op(lv, row[j], op))
            result.append(new_row)
        return MatrExMatrix(result, True)

    # ============================================================
    # 7. Неподдерживаемая комбинация
    # ============================================================
    return None


# ============================================================
# BINARY OP
# ============================================================
class BinaryOp(Node):
    def __init__(self, op, left, right):
        self.op = op
        self.left = left
        self.right = right

    def evaluate(self, env):
        left = self.left.evaluate(env)
        right = self.right.evaluate(env)

        forbid_random(left, "бинарная операция")
        forbid_random(right, "бинарная операция")

        # ============================================================
        # АРИФМЕТИКА
        # ============================================================
        if self.op == 'PLUS':
            return _apply_arith(left, right, 'PLUS')

        elif self.op == 'MINUS':
            return _apply_arith(left, right, 'MINUS')

        elif self.op == 'STAR':
            return _apply_arith(left, right, 'STAR')

        elif self.op == 'SLASH':
            return _apply_arith(left, right, 'SLASH')

        elif self.op == 'MOD':
            return _apply_arith(left, right, 'MOD')

        elif self.op == 'POW':
            return _apply_arith(left, right, 'POW')

        elif self.op == 'FLOORDIV':
            return _apply_arith(left, right, 'FLOORDIV')

        # ============================================================
        # СРАВНЕНИЕ
        # ============================================================
        elif self.op == 'EQUALS':
            return _compare(left, right, '==')

        elif self.op == 'NOTEQUAL':
            return _compare(left, right, '!=')

        elif self.op == 'LESS':
            return _compare(left, right, '<')

        elif self.op == 'GREATER':
            return _compare(left, right, '>')

        elif self.op == 'LESSEQUAL':
            return _compare(left, right, '<=')

        elif self.op == 'GREATEREQUAL':
            return _compare(left, right, '>=')

        # ============================================================
        # ЛОГИКА
        # ============================================================
        elif self.op == 'AND':
            return _logic_and(left, right)

        elif self.op == 'OR':
            return _logic_or(left, right)

        else:
            raise RuntimeError(f"Неизвестный оператор: {self.op}")

    def __repr__(self):
        return f"BinaryOp({self.op}, {self.left}, {self.right})"


# ============================================================
# UNARY OP
# ============================================================
class UnaryOp(Node):
    def __init__(self, op, right):
        self.op = op
        self.right = right

    def evaluate(self, env):
        right = self.right.evaluate(env)
        forbid_random(right, "унарная операция")

        # ============================================================
        # УНАРНЫЙ МИНУС
        # ============================================================
        if self.op == 'MINUS':
            from runtime.matrix import MatrExMatrix

            # Скаляр
            if right is None:
                return None
            if _is_number(right):
                return -right

            # Вектор
            if _is_vector(right):
                result = [(-v if _is_number(v) else None) for v in right.data]
                return MatrExMatrix(result, False)

            # Матрица
            if _is_matrix(right):
                result = []
                for row in right.data:
                    new_row = [(-v if _is_number(v) else None) for v in row]
                    result.append(new_row)
                return MatrExMatrix(result, True)

            return None

        # ============================================================
        # ЛОГИЧЕСКОЕ НЕ
        # ============================================================
        elif self.op == 'NOT':
            return _logic_not(right)

        else:
            raise RuntimeError(f"Неизвестный унарный оператор: {self.op}")

    def __repr__(self):
        return f"UnaryOp({self.op}, {self.right})"