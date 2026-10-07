# ast_nodes/operations.py
from .base import Node
from runtime.random_source import forbid_random


# ============================================================
# ХЕЛПЕР: ПОЭЛЕМЕНТНОЕ СРАВНЕНИЕ
# ============================================================
def _scalar_cmp(a, b, op):
    """
    Сравнение двух скаляров с поддержкой None.

    Правила:
        None == None  → True
        None != None  → False
        None == 5     → False
        5 == None     → False
        None != 5     → True
        5 != None     → True
        None < 5      → False (нельзя сравнивать None по величине)
    """
    # ============================================================
    # Спец-обработка None
    # ============================================================
    if a is None or b is None:
        if op == '==':
            return a is None and b is None
        if op == '!=':
            return not (a is None and b is None)
        # <, >, <=, >= — сравнение с None невозможно
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


def _is_vector(val):
    """True, если val — 1D MatrExMatrix (вектор)."""
    from runtime.matrix import MatrExMatrix
    return isinstance(val, MatrExMatrix) and not val.is_2d


def _is_matrix(val):
    """True, если val — 2D MatrExMatrix."""
    from runtime.matrix import MatrExMatrix
    return isinstance(val, MatrExMatrix) and val.is_2d


def _compare(left, right, op):
    """
    Поэлементное сравнение с поддержкой векторов.

    Возвращает:
        • скаляр (bool) — если оба операнда скаляры;
        • вектор (MatrExMatrix, is_2d=False) — если хотя бы один операнд вектор.
    """
    from runtime.matrix import MatrExMatrix

    left_vec = _is_vector(left)
    right_vec = _is_vector(right)

    # ============================================================
    # Оба вектора — поэлементно
    # ============================================================
    if left_vec and right_vec:
        n = min(len(left.data), len(right.data))
        result = []
        for i in range(n):
            result.append(_scalar_cmp(left.data[i], right.data[i], op))
        return MatrExMatrix(result, False)

    # ============================================================
    # Левый — вектор, правый — скаляр
    # ============================================================
    if left_vec:
        result = [_scalar_cmp(v, right, op) for v in left.data]
        return MatrExMatrix(result, False)

    # ============================================================
    # Левый — скаляр, правый — вектор
    # ============================================================
    if right_vec:
        result = [_scalar_cmp(left, v, op) for v in right.data]
        return MatrExMatrix(result, False)

    # ============================================================
    # Оба скаляры
    # ============================================================
    return _scalar_cmp(left, right, op)


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
            if isinstance(left, str) or isinstance(right, str):
                return str(left) + str(right)
            return left + right

        elif self.op == 'MINUS':
            return left - right

        elif self.op == 'STAR':
            if isinstance(left, str) and isinstance(right, int):
                return left * right
            if isinstance(left, int) and isinstance(right, str):
                return left * right
            return left * right

        elif self.op == 'SLASH':
            return left / right if right != 0 else float('inf')

        elif self.op == 'MOD':
            return left % right

        elif self.op == 'POW':
            return left ** right

        elif self.op == 'FLOORDIV':
            return left // right

        # ============================================================
        # СРАВНЕНИЕ — поэлементно, если есть вектор
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
            return left and right

        elif self.op == 'OR':
            return left or right

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

        if self.op == 'MINUS':
            return -right

        elif self.op == 'NOT':
            # Поэлементное отрицание для вектора
            from runtime.matrix import MatrExMatrix
            if isinstance(right, MatrExMatrix) and not right.is_2d:
                result = [not v for v in right.data]
                return MatrExMatrix(result, False)
            return not right

        else:
            raise RuntimeError(f"Неизвестный унарный оператор: {self.op}")

    def __repr__(self):
        return f"UnaryOp({self.op}, {self.right})"