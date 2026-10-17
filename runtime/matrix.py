# runtime/matrix.py
"""
Класс MatrExMatrix + поэлементная арифметика.
"""

# ============================================================
# ХЕЛПЕРЫ
# ============================================================

def _is_scalar(v):
    return isinstance(v, (int, float, str, bool)) or v is None


def _is_number(v):
    return isinstance(v, (int, float)) and not isinstance(v, bool)


def _apply_elementwise(self, other, op, op_name="+"):
    """
    Поэлементное применение операции op к self и other.

    op — функция (a, b) → результат.
    op_name — для сообщения об ошибке.

    Возвращает НОВЫЙ MatrExMatrix.
    """
    # ============================================================
    # 1. other — скаляр
    # ============================================================
    if _is_scalar(other):
        def fn(v):
            if v is None or other is None:
                return None
            try:
                return op(v, other)
            except (TypeError, ValueError, ZeroDivisionError):
                return None

        if self.is_2d:
            return MatrExMatrix(
                [[fn(v) for v in row] for row in self.data],
                True
            )
        return MatrExMatrix([fn(v) for v in self.data], False)

    # ============================================================
    # 2. other — MatrExMatrix
    # ============================================================
    if isinstance(other, MatrExMatrix):
        # 2.1. Оба 1D
        if not self.is_2d and not other.is_2d:
            if len(self.data) != len(other.data):
                raise ValueError(
                    f"Операция '{op_name}': нельзя работать с векторами "
                    f"разной длины ({len(self.data)} и {len(other.data)})."
                )
            result = []
            for a, b in zip(self.data, other.data):
                if a is None or b is None:
                    result.append(None)
                    continue
                try:
                    result.append(op(a, b))
                except (TypeError, ValueError, ZeroDivisionError):
                    result.append(None)
            return MatrExMatrix(result, False)

        # 2.2. Оба 2D
        if self.is_2d and other.is_2d:
            if self.rows != other.rows or self.cols != other.cols:
                raise ValueError(
                    f"Операция '{op_name}': нельзя работать с матрицами "
                    f"разных размеров "
                    f"({self.rows}×{self.cols} и "
                    f"{other.rows}×{other.cols})."
                )
            result = []
            for i in range(self.rows):
                row = []
                for j in range(self.cols):
                    a = self.data[i][j]
                    b = other.data[i][j]
                    if a is None or b is None:
                        row.append(None)
                        continue
                    try:
                        row.append(op(a, b))
                    except (TypeError, ValueError, ZeroDivisionError):
                        row.append(None)
                result.append(row)
            return MatrExMatrix(result, True)

        # 2.3. Смешанные
        raise TypeError(
            f"Операция '{op_name}': нельзя смешивать вектор и матрицу.\n"
            f"  Слева: {'матрица' if self.is_2d else 'вектор'}\n"
            f"  Справа: {'матрица' if other.is_2d else 'вектор'}"
        )

    # ============================================================
    # 3. other — list
    # ============================================================
    if isinstance(other, list):
        if other and isinstance(other[0], list):
            return _apply_elementwise(
                self, MatrExMatrix(other, True), op, op_name
            )
        return _apply_elementwise(
            self, MatrExMatrix(other, False), op, op_name
        )

    # ============================================================
    # 4. Несовместимый тип
    # ============================================================
    raise TypeError(
        f"Операция '{op_name}': несовместимый тип {type(other).__name__}."
    )


# ============================================================
# КЛАСС
# ============================================================

class MatrExMatrix:
    def __init__(self, data, is_2d=False):
        self.data = data
        self.is_2d = is_2d
        self.rows = len(data) if is_2d else (1 if data else 0)
        self.cols = len(data[0]) if (is_2d and data) else (len(data) if not is_2d else 0)

    def replace_data(self, new_data, is_2d):
        self.data = new_data
        self.is_2d = is_2d
        self.rows = len(new_data) if is_2d else (1 if new_data else 0)
        self.cols = len(new_data[0]) if (is_2d and new_data) else (len(new_data) if not is_2d else 0)

    def __repr__(self):
        if self.is_2d:
            return f"MatrExMatrix({self.data}, 2D)"
        return f"MatrExMatrix({self.data})"

    # ============================================================
    # АРИФМЕТИКА
    # ============================================================

    def __add__(self, other):
        return _apply_elementwise(self, other, lambda a, b: a + b, "+")

    def __radd__(self, other):
        return _apply_elementwise(self, other, lambda a, b: b + a, "+")

    def __sub__(self, other):
        return _apply_elementwise(self, other, lambda a, b: a - b, "-")

    def __rsub__(self, other):
        return _apply_elementwise(self, other, lambda a, b: b - a, "-")

    def __mul__(self, other):
        return _apply_elementwise(self, other, lambda a, b: a * b, "*")

    def __rmul__(self, other):
        return _apply_elementwise(self, other, lambda a, b: b * a, "*")

    def __truediv__(self, other):
        return _apply_elementwise(
            self, other,
            lambda a, b: (a / b) if b != 0 else None,
            "/"
        )

    def __rtruediv__(self, other):
        return _apply_elementwise(
            self, other,
            lambda a, b: (b / a) if a != 0 else None,
            "/"
        )

    def __mod__(self, other):
        return _apply_elementwise(
            self, other,
            lambda a, b: (a % b) if b != 0 else None,
            "%"
        )

    def __rmod__(self, other):
        return _apply_elementwise(
            self, other,
            lambda a, b: (b % a) if a != 0 else None,
            "%"
        )

    def __pow__(self, other):
        return _apply_elementwise(self, other, lambda a, b: a ** b, "**")

    def __rpow__(self, other):
        return _apply_elementwise(self, other, lambda a, b: b ** a, "**")

    def __floordiv__(self, other):
        return _apply_elementwise(
            self, other,
            lambda a, b: (a // b) if b != 0 else None,
            "//"
        )

    def __rfloordiv__(self, other):
        return _apply_elementwise(
            self, other,
            lambda a, b: (b // a) if a != 0 else None,
            "//"
        )

    def __neg__(self):
        if self.is_2d:
            return MatrExMatrix(
                [[-v if _is_number(v) else v for v in row]
                 for row in self.data],
                True
            )
        return MatrExMatrix(
            [-v if _is_number(v) else v for v in self.data],
            False
        )

    def __pos__(self):
        return self

    # ============================================================
    # ЛОГИКА (поэлементно)
    # ============================================================

    def __and__(self, other):
        return _apply_elementwise(
            self, other,
            lambda a, b: bool(a) and bool(b),
            "and"
        )

    def __rand__(self, other):
        return _apply_elementwise(
            self, other,
            lambda a, b: bool(b) and bool(a),
            "and"
        )

    def __or__(self, other):
        return _apply_elementwise(
            self, other,
            lambda a, b: bool(a) or bool(b),
            "or"
        )

    def __ror__(self, other):
        return _apply_elementwise(
            self, other,
            lambda a, b: bool(b) or bool(a),
            "or"
        )

    # ============================================================
    # СРАВНЕНИЯ (поэлементно)
    # ============================================================

    def __eq__(self, other):
        return _apply_elementwise(self, other, lambda a, b: a == b, "==")

    def __ne__(self, other):
        return _apply_elementwise(self, other, lambda a, b: a != b, "!=")

    def __lt__(self, other):
        return _apply_elementwise(self, other, lambda a, b: a < b, "<")

    def __le__(self, other):
        return _apply_elementwise(self, other, lambda a, b: a <= b, "<=")

    def __gt__(self, other):
        return _apply_elementwise(self, other, lambda a, b: a > b, ">")

    def __ge__(self, other):
        return _apply_elementwise(self, other, lambda a, b: a >= b, ">=")

    # __hash__ нужен, если переопределён __eq__
    __hash__ = None