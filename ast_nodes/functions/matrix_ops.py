# ast_nodes/functions/matrix_ops.py
"""Функции zeros, ones, fill"""

from ..base import Node
from runtime.random_source import forbid_random


class ZerosNode(Node):
    def __init__(self, rows, cols=None):
        self.rows = rows
        self.cols = cols

    def evaluate(self, env):
        from runtime.matrix import MatrExMatrix
        
        rows_val = self.rows.evaluate(env) if hasattr(self.rows, 'evaluate') else self.rows
        forbid_random(rows_val, "zeros")
        
        cols_val = None
        if self.cols is not None:
            cols_val = self.cols.evaluate(env) if hasattr(self.cols, 'evaluate') else self.cols
            forbid_random(cols_val, "zeros")
        
        if not isinstance(rows_val, (int, float)):
            raise TypeError(f"Количество строк должно быть числом, получен {type(rows_val)}")
        
        rows_int = int(rows_val)
        
        if cols_val is None:
            data = [0] * rows_int
            return MatrExMatrix(data, False)
        else:
            if not isinstance(cols_val, (int, float)):
                raise TypeError(f"Количество столбцов должно быть числом, получен {type(cols_val)}")
            cols_int = int(cols_val)
            data = [[0] * cols_int for _ in range(rows_int)]
            return MatrExMatrix(data, True)

    def __repr__(self):
        if self.cols is None:
            return f"zeros({self.rows})"
        return f"zeros({self.rows}, {self.cols})"


class OnesNode(Node):
    def __init__(self, rows, cols=None):
        self.rows = rows
        self.cols = cols

    def evaluate(self, env):
        from runtime.matrix import MatrExMatrix
        
        rows_val = self.rows.evaluate(env) if hasattr(self.rows, 'evaluate') else self.rows
        forbid_random(rows_val, "ones")
        
        cols_val = None
        if self.cols is not None:
            cols_val = self.cols.evaluate(env) if hasattr(self.cols, 'evaluate') else self.cols
            forbid_random(cols_val, "ones")
        
        if not isinstance(rows_val, (int, float)):
            raise TypeError(f"Количество строк должно быть числом, получен {type(rows_val)}")
        
        rows_int = int(rows_val)
        
        if cols_val is None:
            data = [1] * rows_int
            return MatrExMatrix(data, False)
        else:
            if not isinstance(cols_val, (int, float)):
                raise TypeError(f"Количество столбцов должно быть числом, получен {type(cols_val)}")
            cols_int = int(cols_val)
            data = [[1] * cols_int for _ in range(rows_int)]
            return MatrExMatrix(data, True)

    def __repr__(self):
        if self.cols is None:
            return f"ones({self.rows})"
        return f"ones({self.rows}, {self.cols})"


class FillNode(Node):
    def __init__(self, matrix, value):
        self.matrix = matrix
        self.value = value

    def evaluate(self, env):
        from runtime.matrix import MatrExMatrix
        from runtime.random_source import forbid_random
        
        matrix_obj = self.matrix.evaluate(env)
        val = self.value.evaluate(env) if hasattr(self.value, 'evaluate') else self.value
        forbid_random(val, "fill")
        
        if hasattr(matrix_obj, 'data'):
            if not matrix_obj.is_2d:
                data = [val] * len(matrix_obj.data)
                return MatrExMatrix(data, False)
            else:
                data = [[val] * matrix_obj.cols for _ in range(matrix_obj.rows)]
                return MatrExMatrix(data, True)
        
        return matrix_obj

    def __repr__(self):
        return f"fill({self.matrix}, {self.value})"