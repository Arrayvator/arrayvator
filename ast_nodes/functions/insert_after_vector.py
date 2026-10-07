from ..base_nodes import Node


class InsertAfterVectorNode(Node):
    def __init__(self, data):
        self.data = data
    
    def evaluate(self, env):
        if not hasattr(self.data, 'matrix') or not hasattr(self.data, 'indices'):
            raise TypeError("InsertAfterVector ожидает индекс вида data[строка, столбец]")
        
        matrix_obj = self.data.matrix.evaluate(env)
        indices = self.data.indices
        
        if len(indices) != 2:
            return matrix_obj
        
        row_idx = indices[0]
        col_idx = indices[1]
        
        row_val = row_idx.evaluate(env) if hasattr(row_idx, 'evaluate') else row_idx
        col_val = col_idx.evaluate(env) if hasattr(col_idx, 'evaluate') else col_idx
        
        # ============================================================
        # ПРОВЕРЯЕМ: если это список (не матрица) — превращаем в матрицу
        # ============================================================
        if isinstance(matrix_obj, list):
            from runtime.matrix import MatrExMatrix
            matrix_obj = MatrExMatrix([matrix_obj], True)
        
        # ============================================================
        # ВЕКТОР-СТРОКА (1 × N)
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
            
            if col_num < 1:
                col_num = 1
            if col_num > matrix_obj.cols:
                col_num = matrix_obj.cols
            
            # ===== 1. СОЗДАЁМ ФИКТИВНУЮ СТРОКУ =====
            if isinstance(matrix_obj.data[0], list):
                dummy_row = matrix_obj.data[0].copy()
            else:
                dummy_row = matrix_obj.data.copy()
            
            matrix_obj.data.append(dummy_row)
            matrix_obj.rows = 2
            
            # ===== 2. ВСТАВЛЯЕМ СТОЛБЕЦ =====
            for row in matrix_obj.data:
                row.insert(col_num, 0)
            matrix_obj.cols = len(matrix_obj.data[0])
            
            # ===== 3. УДАЛЯЕМ ФИКТИВНУЮ СТРОКУ =====
            del matrix_obj.data[1]
            matrix_obj.rows = 1
            
            # ===== 4. ВОЗВРАЩАЕМ В ВЕКТОР =====
            if len(matrix_obj.data) == 1:
                matrix_obj.data = matrix_obj.data[0]
                matrix_obj.is_2d = False
                matrix_obj.rows = 1
                matrix_obj.cols = len(matrix_obj.data)
            
            return matrix_obj
        
        # ============================================================
        # ВЕКТОР-СТОЛБЕЦ (N × 1)
        # ============================================================
        if matrix_obj.cols == 1:
            if isinstance(row_val, int):
                row_num = row_val
            elif isinstance(row_val, str):
                row_num = self._find_row_by_name(matrix_obj, row_val)
                if row_num is None:
                    return matrix_obj
            else:
                if isinstance(col_val, int):
                    row_num = col_val
                else:
                    return matrix_obj
            
            if row_num < 1:
                row_num = 1
            if row_num > matrix_obj.rows:
                row_num = matrix_obj.rows
            
            matrix_obj.data.insert(row_num, [0])
            matrix_obj.rows = len(matrix_obj.data)
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
        return f"InsertAfterVector({self.data})"