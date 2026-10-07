# ast_nodes/functions/math.py
"""Математические функции: RoundNode, IntNode, FracNode, FracDigitsNode"""

import math
from ..base import Node
from runtime.random_source import forbid_random


class RoundNode(Node):
    def __init__(self, arg, digits=None):
        self.arg = arg
        self.digits = digits

    def _round_single(self, value, digits=None):
        if digits is not None:
            return round(value, int(digits))
        return round(value)

    def evaluate(self, env):
        from runtime.matrix import MatrExMatrix

        value = self.arg.evaluate(env)
        forbid_random(value, "round")

        digits_val = None
        if self.digits is not None:
            digits_val = self.digits.evaluate(env)
            forbid_random(digits_val, "round")
            if not isinstance(digits_val, (int, float)):
                raise TypeError(f"Количество знаков должно быть числом, получен {type(digits_val)}")

        if isinstance(value, (int, float)):
            return self._round_single(value, digits_val)

        if hasattr(value, 'data'):
            if not value.is_2d:
                result = []
                for item in value.data:
                    if isinstance(item, (int, float)):
                        result.append(self._round_single(item, digits_val))
                    else:
                        result.append(item)
                return MatrExMatrix(result, False)
            else:
                result = []
                for row in value.data:
                    new_row = []
                    for item in row:
                        if isinstance(item, (int, float)):
                            new_row.append(self._round_single(item, digits_val))
                        else:
                            new_row.append(item)
                    result.append(new_row)
                return MatrExMatrix(result, True)

        if isinstance(value, list):
            if value and isinstance(value[0], list):
                result = []
                for row in value:
                    new_row = []
                    for item in row:
                        if isinstance(item, (int, float)):
                            new_row.append(self._round_single(item, digits_val))
                        else:
                            new_row.append(item)
                    result.append(new_row)
                return MatrExMatrix(result, True)
            else:
                result = []
                for item in value:
                    if isinstance(item, (int, float)):
                        result.append(self._round_single(item, digits_val))
                    else:
                        result.append(item)
                return MatrExMatrix(result, False)

        raise TypeError(f"round() работает с числами, векторами и матрицами, получен {type(value)}")

    def __repr__(self):
        if self.digits is not None:
            return f"round({self.arg}, {self.digits})"
        return f"round({self.arg})"


class IntNode(Node):
    def __init__(self, arg):
        self.arg = arg

    def _int_single(self, value):
        return math.trunc(value)

    def evaluate(self, env):
        from runtime.matrix import MatrExMatrix

        value = self.arg.evaluate(env)
        forbid_random(value, "int")

        if isinstance(value, (int, float)):
            return self._int_single(value)

        if hasattr(value, 'data'):
            if not value.is_2d:
                result = []
                for item in value.data:
                    if isinstance(item, (int, float)):
                        result.append(self._int_single(item))
                    else:
                        result.append(item)
                return MatrExMatrix(result, False)
            else:
                result = []
                for row in value.data:
                    new_row = []
                    for item in row:
                        if isinstance(item, (int, float)):
                            new_row.append(self._int_single(item))
                        else:
                            new_row.append(item)
                    result.append(new_row)
                return MatrExMatrix(result, True)

        if isinstance(value, list):
            if value and isinstance(value[0], list):
                result = []
                for row in value:
                    new_row = []
                    for item in row:
                        if isinstance(item, (int, float)):
                            new_row.append(self._int_single(item))
                        else:
                            new_row.append(item)
                    result.append(new_row)
                return MatrExMatrix(result, True)
            else:
                result = []
                for item in value:
                    if isinstance(item, (int, float)):
                        result.append(self._int_single(item))
                    else:
                        result.append(item)
                return MatrExMatrix(result, False)

        raise TypeError(f"int() работает с числами, векторами и матрицами, получен {type(value)}")

    def __repr__(self):
        return f"int({self.arg})"


class FracNode(Node):
    def __init__(self, arg, digits=None):
        self.arg = arg
        self.digits = digits

    def _frac_single(self, value, digits=None):
        result = value - math.trunc(value)

        if digits is not None:
            return round(result, int(digits))

        # Автоматически определяем число знаков из строкового представления
        # исходного числа, чтобы убрать хвост float.
        str_val = str(value)
        if '.' in str_val and 'e' not in str_val.lower():
            frac_part = str_val.split('.')[1]
            auto_digits = len(frac_part)
            if auto_digits > 0:
                return round(result, auto_digits)

        return result

    def evaluate(self, env):
        from runtime.matrix import MatrExMatrix

        value = self.arg.evaluate(env)
        forbid_random(value, "frac")

        digits_val = None
        if self.digits is not None:
            digits_val = self.digits.evaluate(env)
            forbid_random(digits_val, "frac")
            if not isinstance(digits_val, (int, float)):
                raise TypeError(f"Количество знаков должно быть числом, получен {type(digits_val)}")

        if isinstance(value, (int, float)):
            return self._frac_single(value, digits_val)

        if hasattr(value, 'data'):
            if not value.is_2d:
                result = []
                for item in value.data:
                    if isinstance(item, (int, float)):
                        result.append(self._frac_single(item, digits_val))
                    else:
                        result.append(item)
                return MatrExMatrix(result, False)
            else:
                result = []
                for row in value.data:
                    new_row = []
                    for item in row:
                        if isinstance(item, (int, float)):
                            new_row.append(self._frac_single(item, digits_val))
                        else:
                            new_row.append(item)
                    result.append(new_row)
                return MatrExMatrix(result, True)

        if isinstance(value, list):
            if value and isinstance(value[0], list):
                result = []
                for row in value:
                    new_row = []
                    for item in row:
                        if isinstance(item, (int, float)):
                            new_row.append(self._frac_single(item, digits_val))
                        else:
                            new_row.append(item)
                    result.append(new_row)
                return MatrExMatrix(result, True)
            else:
                result = []
                for item in value:
                    if isinstance(item, (int, float)):
                        result.append(self._frac_single(item, digits_val))
                    else:
                        result.append(item)
                return MatrExMatrix(result, False)

        raise TypeError(f"frac() работает с числами, векторами и матрицами, получен {type(value)}")

    def __repr__(self):
        if self.digits is not None:
            return f"frac({self.arg}, {self.digits})"
        return f"frac({self.arg})"


class FracDigitsNode(Node):
    def __init__(self, arg):
        self.arg = arg

    def _frac_digits_single(self, value):
        str_val = str(value)
        if '.' in str_val:
            frac_part = str_val.split('.')[1]
            frac_part = frac_part.lstrip('0')
            if frac_part == '':
                return 0
            return int(frac_part)
        return 0

    def evaluate(self, env):
        from runtime.matrix import MatrExMatrix

        value = self.arg.evaluate(env)
        forbid_random(value, "frac_digits")

        if isinstance(value, (int, float)):
            return self._frac_digits_single(value)

        if hasattr(value, 'data'):
            if not value.is_2d:
                result = []
                for item in value.data:
                    if isinstance(item, (int, float)):
                        result.append(self._frac_digits_single(item))
                    else:
                        result.append(item)
                return MatrExMatrix(result, False)
            else:
                result = []
                for row in value.data:
                    new_row = []
                    for item in row:
                        if isinstance(item, (int, float)):
                            new_row.append(self._frac_digits_single(item))
                        else:
                            new_row.append(item)
                    result.append(new_row)
                return MatrExMatrix(result, True)

        if isinstance(value, list):
            if value and isinstance(value[0], list):
                result = []
                for row in value:
                    new_row = []
                    for item in row:
                        if isinstance(item, (int, float)):
                            new_row.append(self._frac_digits_single(item))
                        else:
                            new_row.append(item)
                    result.append(new_row)
                return MatrExMatrix(result, True)
            else:
                result = []
                for item in value:
                    if isinstance(item, (int, float)):
                        result.append(self._frac_digits_single(item))
                    else:
                        result.append(item)
                return MatrExMatrix(result, False)

        raise TypeError(f"frac_digits() работает с числами, векторами и матрицами, получен {type(value)}")

    def __repr__(self):
        return f"frac_digits({self.arg})"