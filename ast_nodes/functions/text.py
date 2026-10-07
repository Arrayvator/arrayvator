from ..base_nodes import Node


class SplitNode(Node):
    def __init__(self, text, delimiter=None):
        self.text = text
        self.delimiter = delimiter
    
    def evaluate(self, env):
        text_val = self.text.evaluate(env)
        if not isinstance(text_val, str):
            text_val = str(text_val)
        
        if self.delimiter is None:
            delimiter = ""
        else:
            delimiter = self.delimiter.evaluate(env)
            if not isinstance(delimiter, str):
                delimiter = str(delimiter)
        
        if delimiter == "":
            result = list(text_val)
        else:
            result = text_val.split(delimiter)
        
        from runtime.matrix import MatrExMatrix
        return MatrExMatrix(result, False)
    
    def execute(self, env):
        return self.evaluate(env)
    
    def __repr__(self):
        return f"Split({self.text}, {self.delimiter})" if self.delimiter else f"Split({self.text})"


class JoinNode(Node):
    def __init__(self, data, delimiter):
        self.data = data
        self.delimiter = delimiter
    
    def evaluate(self, env):
        if isinstance(self.data, str):
            obj = env.get(self.data)
        else:
            obj = self.data.evaluate(env)
        
        delimiter = self.delimiter.evaluate(env)
        if not isinstance(delimiter, str):
            delimiter = str(delimiter)
        
        if hasattr(obj, 'data') and isinstance(obj.data, list):
            if hasattr(obj, 'is_2d') and obj.is_2d:
                result = []
                for row in obj.data:
                    result.append(delimiter.join(str(x) for x in row))
                return "\n".join(result)
            return delimiter.join(str(x) for x in obj.data)
        if isinstance(obj, list):
            return delimiter.join(str(x) for x in obj)
        return str(obj)
    
    def execute(self, env):
        return self.evaluate(env)
    
    def __repr__(self):
        return f"Join({self.data}, {self.delimiter})"


class UpperNode(Node):
    def __init__(self, data):
        self.data = data
    
    def evaluate(self, env):
        if isinstance(self.data, str):
            obj = env.get(self.data)
        else:
            obj = self.data.evaluate(env)
        return str(obj).upper()
    
    def execute(self, env):
        return self.evaluate(env)
    
    def __repr__(self):
        return f"Upper({self.data})"


class LowerNode(Node):
    def __init__(self, data):
        self.data = data
    
    def evaluate(self, env):
        if isinstance(self.data, str):
            obj = env.get(self.data)
        else:
            obj = self.data.evaluate(env)
        return str(obj).lower()
    
    def execute(self, env):
        return self.evaluate(env)
    
    def __repr__(self):
        return f"Lower({self.data})"


class TrimNode(Node):
    def __init__(self, data):
        self.data = data
    
    def evaluate(self, env):
        if isinstance(self.data, str):
            obj = env.get(self.data)
        else:
            obj = self.data.evaluate(env)
        return str(obj).strip()
    
    def execute(self, env):
        return self.evaluate(env)
    
    def __repr__(self):
        return f"Trim({self.data})"


class ContainsNode(Node):
    def __init__(self, text, substring):
        self.text = text
        self.substring = substring
    
    def evaluate(self, env):
        text_val = self.text.evaluate(env)
        sub_val = self.substring.evaluate(env)
        return str(sub_val) in str(text_val)
    
    def execute(self, env):
        return self.evaluate(env)
    
    def __repr__(self):
        return f"Contains({self.text}, {self.substring})"