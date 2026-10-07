from ..base_nodes import Node


class ReplaceNode(Node):
    def __init__(self, data, old_value, new_value):
        self.data = data
        self.old_value = old_value
        self.new_value = new_value
    
    def evaluate(self, env):
        if hasattr(self.data, 'matrix') and hasattr(self.data, 'indices'):
            matrix_obj = self.data.matrix.evaluate(env)
            indices = self.data.indices
            
            old_val = self.old_value.evaluate(env) if hasattr(self.old_value, 'evaluate') else self.old_value
            new_val = self.new_value.evaluate(env) if hasattr(self.new_value, 'evaluate') else self.new_value
            
            if len(indices) == 2:
                row_idx = indices[0]
                col_idx = indices[1]
                
                row_val = row_idx.evaluate(env) if hasattr(row_idx, 'evaluate') else row_idx
                col_val = col_idx.evaluate(env) if hasattr(col_idx, 'evaluate') else col_idx
                
                # ============================================================
                # ДЛЯ ВЕКТОРА (одномерная матрица)
                # ============================================================
                if hasattr(matrix_obj, 'is_2d') and not matrix_obj.is_2d:
                    # Вектор-строка (1 × N)
                    if matrix_obj.rows == 1:
                        if row_val == 1 or row_val == 'all' or row_val == ':':
                            for j in range(len(matrix_obj.data)):
                                if matrix_obj.data[j] == old_val:
                                    matrix_obj.data[j] = new_val
                        return matrix_obj
                    
                    # Вектор-столбец (N × 1)
                    else:
                        if col_val == 1 or col_val == 'all' or col_val == ':':
                            for i in range(len(matrix_obj.data)):
                                if matrix_obj.data[i] == old_val:
                                    matrix_obj.data[i] = new_val
                        return matrix_obj
                
                # ============================================================
                # ДЛЯ МАТРИЦЫ (2D)
                # ============================================================
                
                # ===== ЗАМЕНА ПО ВСЕЙ МАТРИЦЕ: data[:, :] =====
                if (row_val == 'all' or row_val == ':') and (col_val == 'all' or col_val == ':'):
                    for i in range(matrix_obj.rows):
                        for j in range(matrix_obj.cols):
                            if matrix_obj.data[i][j] == old_val:
                                matrix_obj.data[i][j] = new_val
                    return matrix_obj
                
                # Замена в столбце: data[:, столбец]
                if row_val == 'all' or row_val == ':':
                    if isinstance(col_val, str):
                        col_num = self._find_column_by_name(matrix_obj, col_val)
                        if col_num is None:
                            return matrix_obj
                    elif isinstance(col_val, int):
                        col_num = col_val
                    else:
                        return matrix_obj
                    
                    if col_num < 1 or col_num > matrix_obj.cols:
                        return matrix_obj
                    
                    col_idx_num = col_num - 1
                    
                    for i in range(matrix_obj.rows):
                        if col_idx_num < len(matrix_obj.data[i]):
                            if matrix_obj.data[i][col_idx_num] == old_val:
                                matrix_obj.data[i][col_idx_num] = new_val
                    
                    return matrix_obj
                
                # Замена в строке: data[строка, :]
                elif col_val == 'all' or col_val == ':':
                    if isinstance(row_val, str):
                        row_num = self._find_row_by_name(matrix_obj, row_val)
                        if row_num is None:
                            return matrix_obj
                    elif isinstance(row_val, int):
                        row_num = row_val
                    else:
                        return matrix_obj
                    
                    if row_num < 1 or row_num > matrix_obj.rows:
                        return matrix_obj
                    
                    row_idx_num = row_num - 1
                    
                    for j in range(matrix_obj.cols):
                        if j < len(matrix_obj.data[row_idx_num]):
                            if matrix_obj.data[row_idx_num][j] == old_val:
                                matrix_obj.data[row_idx_num][j] = new_val
                    
                    return matrix_obj
                
                # Замена в конкретной ячейке: data[строка, столбец]
                else:
                    if isinstance(row_val, str):
                        row_num = self._find_row_by_name(matrix_obj, row_val)
                        if row_num is None:
                            return matrix_obj
                    elif isinstance(row_val, int):
                        row_num = row_val
                    else:
                        return matrix_obj
                    
                    if isinstance(col_val, str):
                        col_num = self._find_column_by_name(matrix_obj, col_val)
                        if col_num is None:
                            return matrix_obj
                    elif isinstance(col_val, int):
                        col_num = col_val
                    else:
                        return matrix_obj
                    
                    if row_num < 1 or row_num > matrix_obj.rows:
                        return matrix_obj
                    if col_num < 1 or col_num > matrix_obj.cols:
                        return matrix_obj
                    
                    row_idx_num = row_num - 1
                    col_idx_num = col_num - 1
                    
                    if matrix_obj.data[row_idx_num][col_idx_num] == old_val:
                        matrix_obj.data[row_idx_num][col_idx_num] = new_val
                    
                    return matrix_obj
            
            return matrix_obj
        
        # Если data не индекс - заменяем везде
        if isinstance(self.data, str):
            matrix_obj = env.get(self.data)
        else:
            matrix_obj = self.data.evaluate(env)
        
        if matrix_obj is None:
            return None
        
        old_val = self.old_value.evaluate(env) if hasattr(self.old_value, 'evaluate') else self.old_value
        new_val = self.new_value.evaluate(env) if hasattr(self.new_value, 'evaluate') else self.new_value
        
        # Для вектора
        if hasattr(matrix_obj, 'is_2d') and not matrix_obj.is_2d:
            for i in range(len(matrix_obj.data)):
                if matrix_obj.data[i] == old_val:
                    matrix_obj.data[i] = new_val
            return matrix_obj
        
        # Для матрицы
        for i in range(matrix_obj.rows):
            for j in range(matrix_obj.cols):
                if matrix_obj.data[i][j] == old_val:
                    matrix_obj.data[i][j] = new_val
        
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
        return f"Replace({self.data}, {self.old_value}, {self.new_value})"