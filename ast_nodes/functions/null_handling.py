# ast_nodes/functions/null_handling.py
"""
Функции для работы с None:
    isnone(x)              — проверить, что x == None (поэлементно)
    fillna(data, value)    — заменить None на value
    dropna(data)           — удалить строки, где есть None
    coalesce(a, b, ...)    — первое значение, не равное None
    noneif(value, cond)    — None, если cond == True, иначе value
"""

from ..base import Node


# ============================================================
# ХЕЛПЕР: ПОЭЛЕМЕНТНОЕ ПРИМЕНЕНИЕ
# ============================================================
def _apply_elementwise(val, fn):
    """
    Применяет fn к каждому элементу вектора/матрицы.
    Для скаляра возвращает fn(val).
    """
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


# ============================================================
# IS_NONE (isnone)
# ============================================================
class IsNullNode(Node):
    """Проверка на None. Поэлементно для векторов и матриц."""
    def __init__(self, value):
        self.value = value

    def evaluate(self, env):
        val = (self.value.evaluate(env)
               if hasattr(self.value, 'evaluate')
               else self.value)

        def fn(v):
            return v is None

        return _apply_elementwise(val, fn)

    def __repr__(self):
        return f"isnone({self.value})"


# ============================================================
# FILLNA
# ============================================================
class FillnaNode(Node):
    def __init__(self, data, fill_value, column=None):
        self.data = data
        self.fill_value = fill_value
        self.column = column

    def evaluate(self, env):
        from runtime.matrix import MatrExMatrix

        data_obj = self.data.evaluate(env)
        fill_val = (self.fill_value.evaluate(env)
                    if hasattr(self.fill_value, 'evaluate')
                    else self.fill_value)

        if hasattr(data_obj, 'data'):
            if not data_obj.is_2d:
                result = [fill_val if item is None else item
                          for item in data_obj.data]
                return MatrExMatrix(result, False)
            else:
                result = []
                for row in data_obj.data:
                    result.append([fill_val if item is None else item
                                   for item in row])
                return MatrExMatrix(result, True)

        if isinstance(data_obj, list):
            if data_obj and isinstance(data_obj[0], list):
                result = []
                for row in data_obj:
                    result.append([fill_val if item is None else item
                                   for item in row])
                return MatrExMatrix(result, True)
            else:
                result = [fill_val if item is None else item
                          for item in data_obj]
                return MatrExMatrix(result, False)

        return fill_val if data_obj is None else data_obj

    def __repr__(self):
        return f"fillna({self.data}, {self.fill_value})"


# ============================================================
# DROPNA
# ============================================================
class DropnaNode(Node):
    def __init__(self, data, column=None):
        self.data = data
        self.column = column

    def _has_null(self, row):
        return any(item is None for item in row)

    def evaluate(self, env):
        from runtime.matrix import MatrExMatrix

        data_obj = self.data.evaluate(env)

        if hasattr(data_obj, 'data'):
            if not data_obj.is_2d:
                result = [item for item in data_obj.data
                          if item is not None]
                return MatrExMatrix(result, False)
            else:
                result = [data_obj.data[0]] if data_obj.rows > 0 else []
                for i in range(1, data_obj.rows):
                    if not self._has_null(data_obj.data[i]):
                        result.append(data_obj.data[i])
                return MatrExMatrix(result, True)

        return data_obj

    def __repr__(self):
        return f"dropna({self.data})"


# ============================================================
# COALESCE
# ============================================================
class CoalesceNode(Node):
    def __init__(self, *values):
        self.values = values

    def evaluate(self, env):
        for val_node in self.values:
            val = (val_node.evaluate(env)
                   if hasattr(val_node, 'evaluate')
                   else val_node)
            if val is not None:
                return val
        return None

    def __repr__(self):
        return f"coalesce({', '.join(str(v) for v in self.values)})"


# ============================================================
# NULL_IF / NONE_IF
# ============================================================
class NullIfNode(Node):
    def __init__(self, value, condition):
        self.value = value
        self.condition = condition

    def evaluate(self, env):
        val = (self.value.evaluate(env)
               if hasattr(self.value, 'evaluate')
               else self.value)
        cond = (self.condition.evaluate(env)
                if hasattr(self.condition, 'evaluate')
                else self.condition)
        return None if cond else val

    def __repr__(self):
        return f"null_if({self.value}, {self.condition})"