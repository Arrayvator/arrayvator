# ast_nodes/functions/type_handling.py
"""
Функции для работы с типами данных:
    type()         - тип значения
    is_number()    - проверка на число
    is_integer()   - проверка на целое число
    is_float()     - проверка на число с плавающей точкой
    is_string()    - проверка на строку
    is_boolean()   - проверка на логический тип
    isnone()       - проверка на None
    to_string()    - преобразование в строку
    to_number()    - преобразование в число

ВСЕ проверки is_* работают поэлементно для векторов и матриц.
"""

import datetime
from ..base import Node


def _is_duckdb(val):
    try:
        from duckdb_engine import DuckDBTable
        return isinstance(val, DuckDBTable)
    except ImportError:
        return False


def _apply_elementwise(val, fn, is_2d):
    from runtime.matrix import MatrExMatrix

    if isinstance(val, MatrExMatrix) and not val.is_2d:
        result = [fn(v) for v in val.data]
        return MatrExMatrix(result, False)

    if isinstance(val, MatrExMatrix) and val.is_2d:
        result = []
        for row in val.data:
            new_row = [fn(v) for v in row]
            result.append(new_row)
        return MatrExMatrix(result, True)

    return fn(val)


class TypeNode(Node):
    def __init__(self, value):
        self.value = value

    def evaluate(self, env):
        val = self.value.evaluate(env) if hasattr(self.value, 'evaluate') else self.value

        if _is_duckdb(val):
            return "duckdb"

        if hasattr(val, 'is_2d'):
            if val.is_2d:
                return "matrix"
            else:
                return "vector"

        if val is None:
            return "null"
        elif isinstance(val, bool):
            return "boolean"
        elif isinstance(val, int):
            return "integer"
        elif isinstance(val, float):
            return "float"
        elif isinstance(val, str):
            return "string"
        elif isinstance(val, datetime.datetime):
            return "datetime"
        elif isinstance(val, datetime.date):
            return "date"
        elif isinstance(val, datetime.time):
            return "time"
        elif isinstance(val, list):
            return "list"
        else:
            return "unknown"

    def __repr__(self):
        return f"type({self.value})"


class IsNumberNode(Node):
    def __init__(self, value):
        self.value = value

    def evaluate(self, env):
        val = self.value.evaluate(env) if hasattr(self.value, 'evaluate') else self.value

        def fn(v):
            return isinstance(v, (int, float)) and not isinstance(v, bool)

        return _apply_elementwise(val, fn, hasattr(val, 'is_2d') and val.is_2d)

    def __repr__(self):
        return f"is_number({self.value})"


class IsIntegerNode(Node):
    def __init__(self, value):
        self.value = value

    def evaluate(self, env):
        val = self.value.evaluate(env) if hasattr(self.value, 'evaluate') else self.value

        def fn(v):
            return isinstance(v, int) and not isinstance(v, bool)

        return _apply_elementwise(val, fn, hasattr(val, 'is_2d') and val.is_2d)

    def __repr__(self):
        return f"is_integer({self.value})"


class IsFloatNode(Node):
    def __init__(self, value):
        self.value = value

    def evaluate(self, env):
        val = self.value.evaluate(env) if hasattr(self.value, 'evaluate') else self.value

        def fn(v):
            return isinstance(v, float)

        return _apply_elementwise(val, fn, hasattr(val, 'is_2d') and val.is_2d)

    def __repr__(self):
        return f"is_float({self.value})"


class IsStringNode(Node):
    def __init__(self, value):
        self.value = value

    def evaluate(self, env):
        val = self.value.evaluate(env) if hasattr(self.value, 'evaluate') else self.value

        def fn(v):
            return isinstance(v, str)

        return _apply_elementwise(val, fn, hasattr(val, 'is_2d') and val.is_2d)

    def __repr__(self):
        return f"is_string({self.value})"


class IsBooleanNode(Node):
    def __init__(self, value):
        self.value = value

    def evaluate(self, env):
        val = self.value.evaluate(env) if hasattr(self.value, 'evaluate') else self.value

        def fn(v):
            return isinstance(v, bool)

        return _apply_elementwise(val, fn, hasattr(val, 'is_2d') and val.is_2d)

    def __repr__(self):
        return f"is_boolean({self.value})"


class IsNullNode(Node):
    """Проверка на None. Поэлементно."""
    def __init__(self, value):
        self.value = value

    def evaluate(self, env):
        val = self.value.evaluate(env) if hasattr(self.value, 'evaluate') else self.value

        def fn(v):
            return v is None

        return _apply_elementwise(val, fn, hasattr(val, 'is_2d') and val.is_2d)

    def __repr__(self):
        return f"isnone({self.value})"


class ToStringNode(Node):
    """Преобразование в строку. Поэлементно."""
    def __init__(self, value):
        self.value = value

    def evaluate(self, env):
        val = self.value.evaluate(env) if hasattr(self.value, 'evaluate') else self.value

        def fn(v):
            if v is None:
                return ""
            if _is_duckdb(v):
                return str(v)
            return str(v)

        return _apply_elementwise(val, fn, hasattr(val, 'is_2d') and val.is_2d)

    def __repr__(self):
        return f"to_string({self.value})"


class ToNumberNode(Node):
    """Преобразование в число. Поэлементно."""
    def __init__(self, value):
        self.value = value

    def evaluate(self, env):
        val = self.value.evaluate(env) if hasattr(self.value, 'evaluate') else self.value

        def fn(v):
            if v is None:
                return None
            if _is_duckdb(v):
                return None
            try:
                if isinstance(v, str):
                    s = v.strip()
                    if s == "":
                        return None
                    if '.' in s:
                        return float(s)
                    else:
                        return int(s)
                return v
            except (ValueError, TypeError):
                return None

        return _apply_elementwise(val, fn, hasattr(val, 'is_2d') and val.is_2d)

    def __repr__(self):
        return f"to_number({self.value})"