# ast_nodes/functions/vector.py
"""Функция VECTOR - создание вектора с размером"""

from ..base import Node
from runtime.random_source import forbid_random
from runtime.matrix import MatrExMatrix


class VectorNode(Node):
    def __init__(self, size):
        self.size = size

    def evaluate(self, env):
        size_val = self.size.evaluate(env) if hasattr(self.size, 'evaluate') else self.size
        forbid_random(size_val, "vector")
        
        if not isinstance(size_val, (int, float)):
            raise TypeError(f"Размер вектора должен быть числом, получен {type(size_val)}")
        
        size_int = int(size_val)
        
        if size_int < 0:
            raise ValueError(f"Размер вектора не может быть отрицательным: {size_int}")
        
        data = [None] * size_int
        return MatrExMatrix(data, False)

    def __repr__(self):
        return f"Vector({self.size})"