from ..base_nodes import Node, VariableNode


class FilterNode(Node):
    def __init__(self, condition):
        self.condition = condition
    
    def evaluate(self, env):
        if not hasattr(self.condition, 'evaluate'):
            return None
        
        matrix_obj = self._get_matrix_from_condition(self.condition, env)
        
        if matrix_obj is None or matrix_obj.rows == 0:
            return matrix_obj
        
        condition_tree = self._build_condition_tree(self.condition, env)
        
        if condition_tree is None:
            return matrix_obj
        
        # ============================================================
        # ФИЛЬТРАЦИЯ ВЕКТОРА (одномерная матрица)
        # ============================================================
        if hasattr(matrix_obj, 'is_2d') and not matrix_obj.is_2d:
            filtered_data = []
            for i in range(matrix_obj.rows):
                # Для вектора-строки: элемент — это значение
                # Для вектора-столбца: элемент — это список с одним значением
                if matrix_obj.rows == 1:
                    row_for_check = [matrix_obj.data[i]]
                else:
                    row_for_check = [matrix_obj.data[i]]
                
                if self._evaluate_condition_tree(condition_tree, row_for_check, env):
                    filtered_data.append(matrix_obj.data[i])
            
            from runtime.matrix import MatrExMatrix
            matrix_obj.data = filtered_data
            matrix_obj.rows = len(filtered_data)
            return matrix_obj
        
        # ============================================================
        # ФИЛЬТРАЦИЯ МАТРИЦЫ (2D)
        # ============================================================
        filtered = []
        
        if matrix_obj.rows > 0:
            filtered.append(matrix_obj.data[0])
        
        for i in range(1, matrix_obj.rows):
            row = matrix_obj.data[i]
            if self._evaluate_condition_tree(condition_tree, row, env):
                filtered.append(row)
        
        matrix_obj.data = filtered
        matrix_obj.rows = len(filtered)
        return matrix_obj
    
    def _build_condition_tree(self, condition, env):
        if condition is None:
            return None
        
        if hasattr(condition, 'op') and condition.op in ['AND', 'OR']:
            left = self._build_condition_tree(condition.left, env)
            right = self._build_condition_tree(condition.right, env)
            return {
                'type': 'operator',
                'op': condition.op,
                'left': left,
                'right': right
            }
        
        elif hasattr(condition, 'op') and condition.op in ['EQUALS', 'NOTEQUAL', 'LESS', 'GREATER', 'LESSEQUAL', 'GREATEREQUAL']:
            left = condition.left
            right = condition.right
            
            if hasattr(right, 'evaluate'):
                compare_val = right.evaluate(env)
            else:
                compare_val = right
            
            # ===== ОБРАБОТКА VariableNode (для векторов без индексов) =====
            if isinstance(left, VariableNode):
                matrix_obj = left.evaluate(env)
                if matrix_obj is not None and hasattr(matrix_obj, 'data'):
                    return {
                        'type': 'comparison',
                        'op': condition.op,
                        'row_val': 'all',
                        'col_val': 'all',
                        'compare_val': compare_val,
                        'matrix': left,
                        'is_vector': True
                    }
            
            # ===== ОБРАБОТКА IndexNode (для матриц и векторов с индексами) =====
            if hasattr(left, 'matrix') and hasattr(left, 'indices'):
                indices = left.indices
                if len(indices) == 2:
                    row_idx = indices[0]
                    col_idx = indices[1]
                    
                    row_val = row_idx.evaluate(env) if hasattr(row_idx, 'evaluate') else row_idx
                    col_val = col_idx.evaluate(env) if hasattr(col_idx, 'evaluate') else col_idx
                    
                    # Если это вектор-строка (row_val == 1, col_val == ':')
                    # или вектор-столбец (row_val == ':', col_val == 1)
                    matrix_obj = left.matrix.evaluate(env)
                    if hasattr(matrix_obj, 'is_2d') and not matrix_obj.is_2d:
                        return {
                            'type': 'comparison',
                            'op': condition.op,
                            'row_val': 'all',
                            'col_val': 'all',
                            'compare_val': compare_val,
                            'matrix': left.matrix,
                            'is_vector': True
                        }
                    
                    return {
                        'type': 'comparison',
                        'op': condition.op,
                        'row_val': row_val,
                        'col_val': col_val,
                        'compare_val': compare_val,
                        'matrix': left.matrix,
                        'is_vector': False
                    }
        
        return None
    
    def _get_matrix_from_condition(self, condition, env):
        if condition is None:
            return None
        
        if hasattr(condition, 'op') and condition.op in ['AND', 'OR']:
            left_matrix = self._get_matrix_from_condition(condition.left, env)
            if left_matrix is not None:
                return left_matrix
            return self._get_matrix_from_condition(condition.right, env)
        
        if hasattr(condition, 'left') and hasattr(condition.left, 'matrix'):
            return condition.left.matrix.evaluate(env)
        if hasattr(condition, 'right') and hasattr(condition.right, 'matrix'):
            return condition.right.matrix.evaluate(env)
        
        if hasattr(condition, 'left') and isinstance(condition.left, VariableNode):
            return condition.left.evaluate(env)
        if hasattr(condition, 'right') and isinstance(condition.right, VariableNode):
            return condition.right.evaluate(env)
        
        return None
    
    def _evaluate_condition_tree(self, tree, row, env):
        if tree is None:
            return True
        
        if tree.get('type') == 'operator':
            left_result = self._evaluate_condition_tree(tree['left'], row, env)
            right_result = self._evaluate_condition_tree(tree['right'], row, env)
            
            if tree['op'] == 'AND':
                return left_result and right_result
            elif tree['op'] == 'OR':
                return left_result or right_result
        
        elif tree.get('type') == 'comparison':
            return self._evaluate_comparison(tree, row, env)
        
        return True
    
    def _evaluate_comparison(self, tree, row, env):
        row_val = tree['row_val']
        col_val = tree['col_val']
        compare_val = tree['compare_val']
        op = tree['op']
        is_vector = tree.get('is_vector', False)
        
        # ============================================================
        # ДЛЯ ВЕКТОРА (is_vector = True)
        # ============================================================
        if is_vector:
            # Проверяем все элементы вектора
            for value in row:
                if self._check_condition(value, compare_val, op):
                    return True
            return False
        
        # ============================================================
        # ДЛЯ МАТРИЦЫ (2D)
        # ============================================================
        matrix_obj = tree['matrix'].evaluate(env)
        
        if row_val == 'all' or row_val == ':':
            if isinstance(col_val, str):
                col_num = self._find_column_by_name(matrix_obj, col_val)
                if col_num is None:
                    return False
                col_idx = col_num - 1
            elif isinstance(col_val, int):
                col_idx = col_val - 1
            else:
                return False
            
            if col_idx < len(row):
                value = row[col_idx]
                return self._check_condition(value, compare_val, op)
            return False
        
        elif col_val == 'all' or col_val == ':':
            if isinstance(row_val, str):
                row_num = self._find_row_by_name(matrix_obj, row_val)
                if row_num is None:
                    return False
            elif isinstance(row_val, int):
                row_num = row_val
            else:
                return False
            
            for value in row:
                if self._check_condition(value, compare_val, op):
                    return True
            return False
        
        return False
    
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
    
    def _check_condition(self, value, compare_val, op):
        if isinstance(value, (int, float)) and isinstance(compare_val, (int, float)):
            if op == 'EQUALS':
                return value == compare_val
            elif op == 'NOTEQUAL':
                return value != compare_val
            elif op == 'LESS':
                return value < compare_val
            elif op == 'GREATER':
                return value > compare_val
            elif op == 'LESSEQUAL':
                return value <= compare_val
            elif op == 'GREATEREQUAL':
                return value >= compare_val
        else:
            str_val = str(value).lower()
            str_compare = str(compare_val).lower()
            
            if op == 'EQUALS':
                return str_val == str_compare
            elif op == 'NOTEQUAL':
                return str_val != str_compare
            elif op == 'LESS':
                return str_val < str_compare
            elif op == 'GREATER':
                return str_val > str_compare
            elif op == 'LESSEQUAL':
                return str_val <= str_compare
            elif op == 'GREATEREQUAL':
                return str_val >= str_compare
        
        return False
    
    def execute(self, env):
        return self.evaluate(env)
    
    def __repr__(self):
        return f"Filter({self.condition})"