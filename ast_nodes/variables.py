from .base import Node


class VariableNode(Node):
    def __init__(self, name): 
        # ПРИВОДИМ ИМЯ К НИЖНЕМУ РЕГИСТРУ
        self.name = name.lower()
    
    def evaluate(self, env): 
        return env.get(self.name)
    
    def __repr__(self): 
        return f"Variable({self.name})"


class PropertyNode(Node):
    def __init__(self, obj_name, prop_name):
        # ПРИВОДИМ ИМЕНА К НИЖНЕМУ РЕГИСТРУ
        self.obj_name = obj_name.lower()
        self.prop_name = prop_name.lower()
    
    def evaluate(self, env):
        obj = env.get(self.obj_name)
        if hasattr(obj, self.prop_name):
            return getattr(obj, self.prop_name)
        raise RuntimeError(f"У объекта {self.obj_name} нет свойства {self.prop_name}")
    
    def __repr__(self): 
        return f"Property({self.obj_name}.{self.prop_name})"