# ast_nodes/functions/matrix.py
"""Функция MATRIX - создание матрицы с размером"""

from ..base import Node
from runtime.random_source import forbid_random
from runtime.matrix import MatrExMatrix


class MatrixCreateNode(Node):
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols

    def evaluate(self, env):
        rows_val = self.rows.evaluate(env) if hasattr(self.rows, 'evaluate') else self.rows
        cols_val = self.cols.evaluate(env) if hasattr(self.cols, 'evaluate') else self.cols
        
        forbid_random(rows_val, "matrix")
        forbid_random(cols_val, "matrix")
        
        if not isinstance(rows_val, (int, float)):
            raise TypeError(f"Количество строк должно быть числом, получен {type(rows_val)}")
        if not isinstance(cols_val, (int, float)):
            raise TypeError(f"Количество столбцов должно быть числом, получен {type(cols_val)}")
        
        rows_int = int(rows_val)
        cols_int = int(cols_val)
        
        if rows_int < 0:
            raise ValueError(f"Количество строк не может быть отрицательным: {rows_int}")
        if cols_int < 0:
            raise ValueError(f"Количество столбцов не может быть отрицательным: {cols_int}")
        
        data = [[None] * cols_int for _ in range(rows_int)]
        return MatrExMatrix(data, True)

    def __repr__(self):
        return f"Matrix({self.rows}, {self.cols})"