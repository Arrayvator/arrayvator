from ..base_nodes import Node


class DeleteVectorNode(Node):
    def __init__(self, data):
        self.data = data
    
    def evaluate(self, env):
        if not hasattr(self.data, 'matrix') or not hasattr(self.data, 'indices'):
            raise TypeError("DeleteVector ожидает индекс вида data[строка, столбец]")
        
        matrix_obj = self.data.matrix.evaluate(env)
        indices = self.data.indices
        
        if len(indices) != 2:
            return matrix_obj
        
        row_idx = indices[0]
        col_idx = indices[1]
        
        row_val = row_idx.evaluate(env) if hasattr(row_idx, 'evaluate') else row_idx
        col_val = col_idx.evaluate(env) if hasattr(col_idx, 'evaluate') else col_idx
        
        # ============================================================
        # ВЕКТОР-СТРОКА (1 × N) — удаляем СТОЛБЕЦ
        # ============================================================
        if matrix_obj.rows == 1:
            if isinstance(col_val, int):
                col_num = col_val
            elif isinstance(col_val, str):
                col_num = self._find_column_by_name(matrix_obj, col_val)
                if col_num is None:
                    return matrix_obj
            else:
                return matrix_obj
            
            if col_num < 1 or col_num > matrix_obj.cols:
                return matrix_obj
            
            new_row = []
            for j in range(matrix_obj.cols):
                if j != col_num - 1:
                    new_row.append(matrix_obj.data[0][j])
            
            matrix_obj.data = [new_row]
            matrix_obj.cols = len(new_row)
            matrix_obj.rows = 1
            return matrix_obj
        
        # ============================================================
        # ВЕКТОР-СТОЛБЕЦ (N × 1) — удаляем СТРОКУ
        # ============================================================
        if matrix_obj.cols == 1:
            # Если col_val > 1, используем его как номер строки
            if isinstance(col_val, int) and col_val > 1:
                row_num = col_val
            elif isinstance(row_val, int):
                row_num = row_val
            elif isinstance(row_val, str):
                row_num = self._find_row_by_name(matrix_obj, row_val)
                if row_num is None:
                    return matrix_obj
            else:
                return matrix_obj
            
            if row_num < 1 or row_num > matrix_obj.rows:
                return matrix_obj
            
            new_data = []
            for i in range(matrix_obj.rows):
                if i != row_num - 1:
                    new_data.append(matrix_obj.data[i])
            
            matrix_obj.data = new_data
            matrix_obj.rows = len(new_data)
            return matrix_obj
        
        return matrix_obj
    
    def _find_column_by_name(self, obj, name):
        if obj.rows > 0 and obj.data:
            for j in range(obj.cols):
                if j < len(obj.data[0]):
                    if str(obj.data[0][j]).strip().lower() == name.lower():
                        return j + 1
        return None
    
    def _find_row_by_name(self, obj, name):
        for i in range(obj.rows):
            if obj.data[i] and len(obj.data[i]) > 0:
                if str(obj.data[i][0]).strip().lower() == name.lower():
                    return i + 1
        return None
    
    def execute(self, env):
        return self.evaluate(env)
    
    def __repr__(self):
        return f"DeleteVector({self.data})"