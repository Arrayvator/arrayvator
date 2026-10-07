from ast_nodes import Node


class BreakNode(Node):
    def execute(self, env):
        raise BreakException()
    
    def __repr__(self):
        return "Break()"


class BreakException(Exception):
    pass