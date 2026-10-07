"""
Функции для работы с диапазонами:
    range() - создание диапазона значений
"""

from ..base import Node


class RangeNode(Node):
    """Создает диапазон значений"""
    def __init__(self, start, end, step=None):
        self.start = start
        self.end = end
        self.step = step

    def evaluate(self, env):
        from runtime.matrix import MatrExMatrix
        
        start_val = self.start.evaluate(env) if hasattr(self.start, 'evaluate') else self.start
        end_val = self.end.evaluate(env) if hasattr(self.end, 'evaluate') else self.end
        
        if self.step is not None:
            step_val = self.step.evaluate(env) if hasattr(self.step, 'evaluate') else self.step
        else:
            step_val = 1
        
        data = list(range(start_val, end_val + 1, step_val))
        return MatrExMatrix(data, False)

    def __repr__(self):
        if self.step is not None:
            return f"range({self.start}, {self.end}, {self.step})"
        return f"range({self.start}, {self.end})"