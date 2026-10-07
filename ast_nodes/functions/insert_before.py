from ..base_nodes import Node
from .insert_before_vector import InsertBeforeVectorNode
from .insert_before_matrix import InsertBeforeMatrixNode


class InsertBeforeNode(Node):
    def __init__(self, data):
        self.data = data
    
    def evaluate(self, env):
        if not hasattr(self.data, 'matrix') or not hasattr(self.data, 'indices'):
            raise TypeError("InsertBefore ожидает индекс вида data[строка, :] или data[:, столбец]")
        
        matrix_obj = self.data.matrix.evaluate(env)
        
        is_vector = False
        if hasattr(matrix_obj, 'is_2d'):
            if not matrix_obj.is_2d:
                is_vector = True
            elif matrix_obj.rows == 1 or matrix_obj.cols == 1:
                is_vector = True
        
        if is_vector:
            vector_insert = InsertBeforeVectorNode(self.data)
            return vector_insert.evaluate(env)
        
        matrix_insert = InsertBeforeMatrixNode(self.data)
        return matrix_insert.evaluate(env)
    
    def execute(self, env):
        return self.evaluate(env)
    
    def __repr__(self):
        return f"InsertBefore({self.data})"