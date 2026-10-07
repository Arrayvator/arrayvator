from ..base_nodes import Node


class BaseStatNode(Node):
    def _get_numbers_from_index(self, data, env):
        """Получает числа из IndexNode (data[:, 2]) или из матрицы"""
        
        if hasattr(data, 'matrix') and hasattr(data, 'indices'):
            matrix_obj = data.matrix.evaluate(env)
            indices = data.indices
            
            if len(indices) != 2:
                return []
            
            row_idx = indices[0]
            col_idx = indices[1]
            
            row_val = row_idx.evaluate(env) if hasattr(row_idx, 'evaluate') else row_idx
            col_val = col_idx.evaluate(env) if hasattr(col_idx, 'evaluate') else col_idx
            
            # ===== ОБРАБОТКА ДИАПАЗОНОВ =====
            
            if hasattr(col_idx, 'op') and col_idx.op == 'RANGE':
                start_node = col_idx.left
                end_node = col_idx.right
                
                start = start_node.evaluate(env) if hasattr(start_node, 'evaluate') else start_node
                end = end_node.evaluate(env) if hasattr(end_node, 'evaluate') else end_node
                
                if isinstance(end, str) and end == 'end':
                    end = matrix_obj.cols
                
                start = int(start) if start is not None else 1
                end = int(end) if end is not None else matrix_obj.cols
                
                row_val = row_idx.evaluate(env) if hasattr(row_idx, 'evaluate') else row_idx
                
                if isinstance(row_val, str):
                    row_num = self._find_row_by_name(matrix_obj, row_val)
                else:
                    row_num = row_val
                
                if row_num is None or not isinstance(row_num, int):
                    return []
                
                row_idx_num = row_num - 1
                
                numbers = []
                for j in range(start - 1, min(end, matrix_obj.cols)):
                    if j < len(matrix_obj.data[row_idx_num]):
                        val = matrix_obj.data[row_idx_num][j]
                        if isinstance(val, (int, float)):
                            numbers.append(val)
                
                return numbers
            
            if hasattr(row_idx, 'op') and row_idx.op == 'RANGE':
                start_node = row_idx.left
                end_node = row_idx.right
                
                start = start_node.evaluate(env) if hasattr(start_node, 'evaluate') else start_node
                end = end_node.evaluate(env) if hasattr(end_node, 'evaluate') else end_node
                
                if isinstance(end, str) and end == 'end':
                    end = matrix_obj.rows
                
                start = int(start) if start is not None else 1
                end = int(end) if end is not None else matrix_obj.rows
                
                col_val = col_idx.evaluate(env) if hasattr(col_idx, 'evaluate') else col_idx
                
                if isinstance(col_val, str):
                    col_num = self._find_column_by_name(matrix_obj, col_val)
                else:
                    col_num = col_val
                
                if col_num is None or not isinstance(col_num, int):
                    return []
                
                col_idx_num = col_num - 1
                
                numbers = []
                for i in range(start - 1, min(end, matrix_obj.rows)):
                    if col_idx_num < len(matrix_obj.data[i]):
                        val = matrix_obj.data[i][col_idx_num]
                        if isinstance(val, (int, float)):
                            numbers.append(val)
                
                return numbers
            
            numbers = []
            
            # ===== ВСЯ МАТРИЦА: data[:, :] =====
            if (row_val == 'all' or row_val == ':') and (col_val == 'all' or col_val == ':'):
                for i in range(matrix_obj.rows):
                    for j in range(matrix_obj.cols):
                        if j < len(matrix_obj.data[i]):
                            val = matrix_obj.data[i][j]
                            if isinstance(val, (int, float)):
                                numbers.append(val)
                return numbers
            
            # ===== СТОЛБЕЦ: data[:, столбец] =====
            if row_val == 'all' or row_val == ':':
                if isinstance(col_val, str):
                    col_num = self._find_column_by_name(matrix_obj, col_val)
                else:
                    col_num = col_val
                
                if col_num is None or not isinstance(col_num, int):
                    return []
                
                col_idx_num = col_num - 1
                
                for i in range(matrix_obj.rows):
                    if col_idx_num < len(matrix_obj.data[i]):
                        val = matrix_obj.data[i][col_idx_num]
                        if isinstance(val, (int, float)):
                            numbers.append(val)
                
                return numbers
            
            # ===== СТРОКА: data[строка, :] =====
            if col_val == 'all' or col_val == ':':
                if isinstance(row_val, str):
                    row_num = self._find_row_by_name(matrix_obj, row_val)
                else:
                    row_num = row_val
                
                if row_num is None or not isinstance(row_num, int):
                    return []
                
                row_idx_num = row_num - 1
                
                for j in range(matrix_obj.cols):
                    if j < len(matrix_obj.data[row_idx_num]):
                        val = matrix_obj.data[row_idx_num][j]
                        if isinstance(val, (int, float)):
                            numbers.append(val)
                
                return numbers
            
            # ===== КОНКРЕТНАЯ ЯЧЕЙКА: data[строка, столбец] =====
            if isinstance(row_val, str):
                row_num = self._find_row_by_name(matrix_obj, row_val)
            else:
                row_num = row_val
            
            if isinstance(col_val, str):
                col_num = self._find_column_by_name(matrix_obj, col_val)
            else:
                col_num = col_val
            
            if row_num is None or col_num is None:
                return []
            if not isinstance(row_num, int) or not isinstance(col_num, int):
                return []
            
            row_idx_num = row_num - 1
            col_idx_num = col_num - 1
            
            if row_idx_num < matrix_obj.rows and col_idx_num < matrix_obj.cols:
                val = matrix_obj.data[row_idx_num][col_idx_num]
                if isinstance(val, (int, float)):
                    return [val]
            
            return []
        
        if isinstance(data, str):
            obj = env.get(data)
        else:
            obj = data.evaluate(env) if hasattr(data, 'evaluate') else data
        
        return self._get_numbers(obj)
    
    def _get_numbers(self, obj):
        """Получает все числа из матрицы"""
        if hasattr(obj, 'is_2d') and obj.is_2d:
            numbers = []
            for row in obj.data:
                for val in row:
                    if isinstance(val, (int, float)):
                        numbers.append(val)
            return numbers
        if hasattr(obj, 'data'):
            return [x for x in obj.data if isinstance(x, (int, float))]
        if isinstance(obj, list):
            return [x for x in obj if isinstance(x, (int, float))]
        if isinstance(obj, (int, float)):
            return [obj]
        return []
    
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


class SumNode(BaseStatNode):
    def __init__(self, data):
        self.data = data
    
    def evaluate(self, env):
        numbers = self._get_numbers_from_index(self.data, env)
        return sum(numbers) if numbers else 0
    
    def execute(self, env):
        return self.evaluate(env)
    
    def __repr__(self):
        return f"Sum({self.data})"


class MinNode(BaseStatNode):
    def __init__(self, data):
        self.data = data
    
    def evaluate(self, env):
        numbers = self._get_numbers_from_index(self.data, env)
        return min(numbers) if numbers else 0
    
    def execute(self, env):
        return self.evaluate(env)
    
    def __repr__(self):
        return f"Min({self.data})"


class MaxNode(BaseStatNode):
    def __init__(self, data):
        self.data = data
    
    def evaluate(self, env):
        numbers = self._get_numbers_from_index(self.data, env)
        return max(numbers) if numbers else 0
    
    def execute(self, env):
        return self.evaluate(env)
    
    def __repr__(self):
        return f"Max({self.data})"


class AvgNode(BaseStatNode):
    def __init__(self, data):
        self.data = data
    
    def evaluate(self, env):
        numbers = self._get_numbers_from_index(self.data, env)
        return sum(numbers) / len(numbers) if numbers else 0
    
    def execute(self, env):
        return self.evaluate(env)
    
    def __repr__(self):
        return f"Avg({self.data})"


class CountNode(BaseStatNode):
    def __init__(self, data):
        self.data = data
    
    def evaluate(self, env):
        numbers = self._get_numbers_from_index(self.data, env)
        return len(numbers) if numbers else 0
    
    def execute(self, env):
        return self.evaluate(env)
    
    def __repr__(self):
        return f"Count({self.data})"