from .base import Node
from runtime.matrix import MatrExMatrix


class NumberNode(Node):
    def __init__(self, value):
        try:
            if isinstance(value, str):
                if '.' in value:
                    self.value = float(value)
                else:
                    self.value = int(value)
            else:
                self.value = value
        except:
            self.value = value
    def evaluate(self, env): return self.value
    def __repr__(self): return f"Number({self.value})"


class StringNode(Node):
    def __init__(self, value): self.value = str(value)
    def evaluate(self, env): return self.value
    def __repr__(self): return f"String('{self.value}')"


class BooleanNode(Node):
    def __init__(self, value): self.value = value
    def evaluate(self, env): return self.value
    def __repr__(self): return f"Boolean({self.value})"


class MatrixNode(Node):
    def __init__(self, data, is_2d=False):
        self.data = data
        self.is_2d = is_2d
    def evaluate(self, env):
        if not self.data:
            return MatrExMatrix([], self.is_2d)
        if self.data and isinstance(self.data[0], list):
            evaluated_data = []
            for row in self.data:
                eval_row = []
                for expr in row:
                    if hasattr(expr, 'evaluate'):
                        eval_row.append(expr.evaluate(env))
                    else:
                        eval_row.append(expr)
                evaluated_data.append(eval_row)
            return MatrExMatrix(evaluated_data, True)
        else:
            evaluated_data = []
            for expr in self.data:
                if hasattr(expr, 'evaluate'):
                    evaluated_data.append(expr.evaluate(env))
                else:
                    evaluated_data.append(expr)
            return MatrExMatrix(evaluated_data, False)
    def __repr__(self): return f"Matrix({self.data})"


# ДОБАВЛЯЕМ NullNode
class NullNode(Node):
    def __init__(self):
        self.value = None
    def evaluate(self, env): 
        return None
    def __repr__(self): 
        return "Null()"