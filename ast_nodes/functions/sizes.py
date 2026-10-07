from ..base_nodes import Node


class RowNode(Node):
    def __init__(self, data):
        self.data = data
    
    def evaluate(self, env):
        if isinstance(self.data, str):
            obj = env.get(self.data)
        else:
            obj = self.data.evaluate(env)
        
        if hasattr(obj, 'rows'):
            return obj.rows
        if isinstance(obj, list):
            return len(obj)
        return 0
    
    def execute(self, env):
        return self.evaluate(env)
    
    def __repr__(self):
        return f"Row({self.data})"


class ColumnNode(Node):
    def __init__(self, data):
        self.data = data
    
    def evaluate(self, env):
        if isinstance(self.data, str):
            obj = env.get(self.data)
        else:
            obj = self.data.evaluate(env)
        
        if hasattr(obj, 'cols'):
            return obj.cols
        if hasattr(obj, 'is_2d') and obj.is_2d:
            return obj.cols
        if isinstance(obj, list) and obj and isinstance(obj[0], list):
            return len(obj[0])
        if isinstance(obj, list):
            return 1
        return 0
    
    def execute(self, env):
        return self.evaluate(env)
    
    def __repr__(self):
        return f"Column({self.data})"


class LenNode(Node):
    def __init__(self, data):
        self.data = data
    
    def evaluate(self, env):
        if isinstance(self.data, str):
            obj = env.get(self.data)
        else:
            obj = self.data.evaluate(env)
        
        if isinstance(obj, str):
            return len(obj)
        
        if hasattr(obj, 'rows') and hasattr(obj, 'cols'):
            return obj.rows
        
        if isinstance(obj, list):
            return len(obj)
        
        if hasattr(obj, '__len__'):
            return len(obj)
        
        return 0
    
    def execute(self, env):
        return self.evaluate(env)
    
    def __repr__(self):
        return f"Len({self.data})"