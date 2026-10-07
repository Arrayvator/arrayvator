from ..base_nodes import Node


class InsertAfterMatrixNode(Node):
    """Вставка после строки или столбца в матрице"""
    
    def __init__(self, data):
        self.data = data
    
    def evaluate(self, env):
        if not hasattr(self.data, 'matrix') or not hasattr(self.data, 'indices'):
            raise TypeError("InsertAfterMatrix ожидает индекс вида data[строка, :] или data[:, столбец]")
        
        matrix_obj = self.data.matrix.evaluate(env)
        indices = self.data.indices
        
        if len(indices) != 2:
            return matrix_obj
        
        row_idx = indices[0]
        col_idx = indices[1]
        
        row_val = row_idx.evaluate(env) if hasattr(row_idx, 'evaluate') else row_idx
        col_val = col_idx.evaluate(env) if hasattr(col_idx, 'evaluate') else col_idx
        
        # ============================================================
        # ВСТАВКА СТРОКИ: data[строка, :]
        # ============================================================
        if col_val == 'all' or col_val == ':':
            if isinstance(row_val, str):
                row_num = self._find_row_by_name(matrix_obj, row_val)
                if row_num is None:
                    raise RuntimeError(f"Строка '{row_val}' не найдена")
            elif isinstance(row_val, int):
                row_num = row_val
            else:
                raise TypeError(f"Неверный тип индекса: {type(row_val)}")
            
            if row_num < 1:
                row_num = 1
            if row_num > matrix_obj.rows:
                row_num = matrix_obj.rows
            
            matrix_obj.data.insert(row_num, [0] * matrix_obj.cols)
            matrix_obj.rows = len(matrix_obj.data)
            return matrix_obj
        
        # ============================================================
        # ВСТАВКА СТОЛБЦА: data[:, столбец]
        # ============================================================
        if row_val == 'all' or row_val == ':':
            if isinstance(col_val, str):
                col_num = self._find_column_by_name(matrix_obj, col_val)
                if col_num is None:
                    raise RuntimeError(f"Столбец '{col_val}' не найден")
            elif isinstance(col_val, int):
                col_num = col_val
            else:
                raise TypeError(f"Неверный тип индекса: {type(col_val)}")
            
            if col_num < 1:
                col_num = 1
            if col_num > matrix_obj.cols:
                col_num = matrix_obj.cols
            
            for row in matrix_obj.data:
                row.insert(col_num, 0)
            matrix_obj.cols = len(matrix_obj.data[0]) if matrix_obj.data else 0
            return matrix_obj
        
        # ============================================================
        # ОШИБКА: попытка вставить ячейку
        # ============================================================
        raise RuntimeError(
            f"Вставка ячейки невозможна! Используйте:\n"
            f"  InsertAfter(data[строка, :])  - вставка строки\n"
            f"  InsertAfter(data[:, столбец]) - вставка столбца"
        )
    
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
        return f"InsertAfterMatrix({self.data})"