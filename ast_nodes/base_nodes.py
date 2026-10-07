class Node:
    pass


class ColumnView:
    def __init__(self, matrix_obj, col_index):
        self.matrix = matrix_obj
        self.col_index = col_index
    
    def __getitem__(self, row_idx):
        if isinstance(row_idx, int):
            return self.matrix.data[row_idx][self.col_index]
        return None
    
    def __setitem__(self, row_idx, value):
        self.matrix.data[row_idx][self.col_index] = value
    
    def __len__(self):
        return self.matrix.rows
    
    def __iter__(self):
        for i in range(self.matrix.rows):
            yield self.matrix.data[i][self.col_index]
    
    def __repr__(self):
        return str([self.matrix.data[i][self.col_index] for i in range(self.matrix.rows)])


class RowView:
    def __init__(self, matrix_obj, row_index):
        self.matrix = matrix_obj
        self.row_index = row_index
    
    def __getitem__(self, col_idx):
        if isinstance(col_idx, int):
            return self.matrix.data[self.row_index][col_idx]
        return None
    
    def __setitem__(self, col_idx, value):
        self.matrix.data[self.row_index][col_idx] = value
    
    def __len__(self):
        return self.matrix.cols
    
    def __iter__(self):
        for j in range(self.matrix.cols):
            yield self.matrix.data[self.row_index][j]
    
    def __repr__(self):
        return str(self.matrix.data[self.row_index])


class NumberNode(Node):
    def __init__(self, value):
        try:
            if isinstance(value, str):
                if '.' in value:
                    self.value = float(value)
                else:
                    self.value = int(value)
            else:
                self.value = value
        except:
            self.value = value
    
    def evaluate(self, env):
        return self.value
    
    def __repr__(self):
        return f"Number({self.value})"


class StringNode(Node):
    def __init__(self, value):
        self.value = str(value)
    
    def evaluate(self, env):
        return self.value
    
    def __repr__(self):
        return f"String('{self.value}')"


class VariableNode(Node):
    def __init__(self, name):
        self.name = name
    
    def evaluate(self, env):
        return env.get(self.name)
    
    def __repr__(self):
        return f"Variable({self.name})"


class BinaryOp(Node):
    def __init__(self, op, left, right):
        self.op = op
        self.left = left
        self.right = right
    
    def evaluate(self, env):
        left = self.left.evaluate(env) if hasattr(self.left, 'evaluate') else self.left
        right = self.right.evaluate(env) if hasattr(self.right, 'evaluate') else self.right
        
        if self.op == 'RANGE':
            return [left, right]
        
        if self.op == 'PLUS':
            if isinstance(left, str) or isinstance(right, str):
                return str(left) + str(right)
            return left + right
        elif self.op == 'MINUS':
            return left - right
        elif self.op == 'STAR':
            return left * right
        elif self.op == 'SLASH':
            return left / right if right != 0 else float('inf')
        elif self.op == 'MOD':
            return left % right
        elif self.op == 'LESS':
            return left < right
        elif self.op == 'GREATER':
            return left > right
        elif self.op == 'LESSEQUAL':
            return left <= right
        elif self.op == 'GREATEREQUAL':
            return left >= right
        elif self.op == 'NOTEQUAL':
            return left != right
        elif self.op == 'EQUALS':
            return left == right
        elif self.op == 'AND':
            return left and right
        elif self.op == 'OR':
            return left or right
        else:
            raise RuntimeError(f"Неизвестный оператор: {self.op}")
    
    def __repr__(self):
        return f"BinaryOp({self.op}, {self.left}, {self.right})"


class UnaryOp(Node):
    def __init__(self, op, right):
        self.op = op
        self.right = right
    
    def evaluate(self, env):
        right = self.right.evaluate(env)
        if self.op == 'MINUS':
            return -right
        elif self.op == 'NOT':
            return not right
        else:
            raise RuntimeError(f"Неизвестный унарный оператор: {self.op}")
    
    def __repr__(self):
        return f"UnaryOp({self.op}, {self.right})"


class MatrixNode(Node):
    def __init__(self, data, is_2d=False):
        self.data = data
        self.is_2d = is_2d
    
    def evaluate(self, env):
        from runtime.matrix import MatrExMatrix
        if not self.data:
            return MatrExMatrix([], self.is_2d)
        if isinstance(self.data[0], list):
            return MatrExMatrix(self.data, True)
        return MatrExMatrix(self.data, False)
    
    def __repr__(self):
        return f"Matrix({self.data})"


class EndNode(Node):
    def __init__(self):
        pass
    
    def evaluate(self, env):
        return 'end'
    
    def __repr__(self):
        return "End()"


class IndexNode(Node):
    def __init__(self, matrix, indices):
        self.matrix = matrix
        self.indices = indices
    
    def evaluate(self, env):
        matrix_obj = self.matrix.evaluate(env)
        
        if matrix_obj is None:
            return 0
        
        values = []
        for idx in self.indices:
            val = idx.evaluate(env) if hasattr(idx, 'evaluate') else idx
            if val == 'end' or val == 'all' or val == ':':
                values.append(val)
            else:
                try:
                    values.append(int(val))
                except:
                    values.append(val)
        
        # ============================================================
        # ОДИН ИНДЕКС (для векторов)
        # ============================================================
        if len(values) == 1:
            idx = values[0]
            
            # Вектор (одномерная матрица)
            if hasattr(matrix_obj, 'is_2d') and not matrix_obj.is_2d:
                if idx == 'all' or idx == ':':
                    from runtime.matrix import MatrExMatrix
                    return MatrExMatrix(matrix_obj.data[:], False)
                if idx == 'end':
                    idx = len(matrix_obj.data)
                if isinstance(idx, int):
                    if 1 <= idx <= len(matrix_obj.data):
                        return matrix_obj.data[idx - 1]
                return 0
            
            # Двумерная матрица с одним индексом — строка
            if hasattr(matrix_obj, 'is_2d') and matrix_obj.is_2d:
                if idx == 'end':
                    idx = matrix_obj.rows
                if idx == 'all' or idx == ':':
                    from runtime.matrix import MatrExMatrix
                    return MatrExMatrix(matrix_obj.data[:], True)
                if isinstance(idx, int):
                    if 1 <= idx <= matrix_obj.rows:
                        from runtime.matrix import MatrExMatrix
                        return MatrExMatrix([matrix_obj.data[idx - 1][:]], True)
                # Поиск по названию строки (первый столбец)
                if isinstance(idx, str):
                    for i in range(matrix_obj.rows):
                        if matrix_obj.data[i] and len(matrix_obj.data[i]) > 0:
                            if str(matrix_obj.data[i][0]).lower() == idx.lower():
                                from runtime.matrix import MatrExMatrix
                                return MatrExMatrix([matrix_obj.data[i][:]], True)
                return 0
            
            return 0
        
        # ============================================================
        # ДВА ИНДЕКСА: data[строка, столбец]
        # ============================================================
        elif len(values) == 2:
            row = values[0]
            col = values[1]
            
            # ============================================================
            # ВЕКТОР (одномерная матрица)
            # ============================================================
            if hasattr(matrix_obj, 'is_2d') and not matrix_obj.is_2d:
                if row == 'end':
                    row = 1
                if col == 'end':
                    col = len(matrix_obj.data)
                
                if row == 'all' or row == ':':
                    if col == 'all' or col == ':':
                        from runtime.matrix import MatrExMatrix
                        return MatrExMatrix(matrix_obj.data[:], False)
                    if isinstance(col, int) and 1 <= col <= len(matrix_obj.data):
                        return matrix_obj.data[col - 1]
                    return 0
                if col == 'all' or col == ':':
                    if isinstance(row, int) and row == 1:
                        from runtime.matrix import MatrExMatrix
                        return MatrExMatrix(matrix_obj.data[:], False)
                    return 0
                if isinstance(row, int) and isinstance(col, int):
                    if row == 1 and 1 <= col <= len(matrix_obj.data):
                        return matrix_obj.data[col - 1]
                return 0
            
            # ============================================================
            # ДВУМЕРНАЯ МАТРИЦА
            # ============================================================
            if hasattr(matrix_obj, 'is_2d') and matrix_obj.is_2d:
                # Преобразуем end
                if row == 'end':
                    row = matrix_obj.rows
                if col == 'end':
                    col = matrix_obj.cols
                
                # ===== ПОИСК ПО НАЗВАНИЮ СТРОКИ =====
                if isinstance(row, str) and row != 'all' and row != ':' and row != 'end':
                    found = False
                    for i in range(matrix_obj.rows):
                        if matrix_obj.data[i] and len(matrix_obj.data[i]) > 0:
                            if str(matrix_obj.data[i][0]).lower() == row.lower():
                                row = i + 1
                                found = True
                                break
                    if not found:
                        return 0
                
                # ===== ПОИСК ПО НАЗВАНИЮ СТОЛБЦА =====
                if isinstance(col, str) and col != 'all' and col != ':' and col != 'end':
                    found = False
                    if matrix_obj.rows > 0:
                        for j in range(matrix_obj.cols):
                            if matrix_obj.data[0] and j < len(matrix_obj.data[0]):
                                if str(matrix_obj.data[0][j]).lower() == col.lower():
                                    col = j + 1
                                    found = True
                                    break
                    if not found:
                        return 0
                
                # Преобразуем row и col в числа
                row_is_all = (row == 'all' or row == ':')
                col_is_all = (col == 'all' or col == ':')
                
                if not isinstance(row, int) and not row_is_all:
                    try:
                        row = int(row)
                    except:
                        return 0
                
                if not isinstance(col, int) and not col_is_all:
                    try:
                        col = int(col)
                    except:
                        return 0
                
                # ===== ВСЯ МАТРИЦА =====
                if row_is_all and col_is_all:
                    from runtime.matrix import MatrExMatrix
                    return MatrExMatrix([row[:] for row in matrix_obj.data], True)
                
                # ===== ЦЕЛАЯ СТРОКА =====
                if not row_is_all and col_is_all:
                    if isinstance(row, int):
                        row_idx = row - 1
                        if 0 <= row_idx < matrix_obj.rows:
                            from runtime.matrix import MatrExMatrix
                            return MatrExMatrix([matrix_obj.data[row_idx][:]], True)
                    return 0
                
                # ===== ЦЕЛЫЙ СТОЛБЕЦ =====
                if row_is_all and not col_is_all:
                    if isinstance(col, int):
                        col_idx = col - 1
                        if 0 <= col_idx < matrix_obj.cols:
                            from runtime.matrix import MatrExMatrix
                            col_data = [[matrix_obj.data[i][col_idx]] for i in range(matrix_obj.rows)]
                            return MatrExMatrix(col_data, True)
                    return 0
                
                # ===== КОНКРЕТНАЯ ЯЧЕЙКА =====
                if isinstance(row, int) and isinstance(col, int):
                    row_idx = row - 1
                    col_idx = col - 1
                    if row_idx < 0 or col_idx < 0:
                        return 0
                    if matrix_obj.rows == 0:
                        return 0
                    if row_idx >= matrix_obj.rows or col_idx >= matrix_obj.cols:
                        return 0
                    return matrix_obj.data[row_idx][col_idx]
                
                return 0
            
            return 0
        
        return 0
    
    def execute(self, env):
        self.evaluate(env)
    
    def __repr__(self):
        return f"Index({self.matrix}[{self.indices}])"


class PropertyNode(Node):
    def __init__(self, obj_name, prop_name):
        self.obj_name = obj_name
        self.prop_name = prop_name
    
    def evaluate(self, env):
        obj = env.get(self.obj_name)
        if hasattr(obj, self.prop_name):
            return getattr(obj, self.prop_name)
        raise RuntimeError(f"У объекта {self.obj_name} нет свойства {self.prop_name}")
    
    def __repr__(self):
        return f"Property({self.obj_name}.{self.prop_name})"


class InputNode(Node):
    def __init__(self, prompt=None):
        self.prompt = prompt
    
    def evaluate(self, env):
        import tkinter as tk
        from tkinter import simpledialog
        prompt_text = self.prompt.evaluate(env) if self.prompt else ""
        root = tk.Tk()
        root.withdraw()
        root.attributes('-topmost', True)
        user_input = simpledialog.askstring("Arrayvator - Ввод данных", prompt_text, parent=root)
        root.destroy()
        if user_input is None:
            user_input = ""
        try:
            return float(user_input)
        except:
            return user_input
    
    def execute(self, env):
        return self.evaluate(env)
    
    def __repr__(self):
        return f"Input({self.prompt})"


class BreakException(Exception):
    pass


class BreakNode(Node):
    def __init__(self):
        pass
    
    def execute(self, env):
        raise BreakException()
    
    def __repr__(self):
        return "Break()"


class ForNoEndNode(Node):
    def __init__(self, body):
        self.body = body
    
    def execute(self, env):
        try:
            while True:
                for stmt in self.body:
                    stmt.execute(env)
        except BreakException:
            pass
    
    def __repr__(self):
        return f"ForNoEnd({self.body})"