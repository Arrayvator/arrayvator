# operators/print_stmt.py
from ast_nodes import Node
from runtime.random_source import forbid_random


class PrintNode(Node):
    """Обычный вывод - горизонтально через пробел"""
    def __init__(self, expressions):
        self.expressions = expressions
    
    def execute(self, env):
        values = []
        for expr in self.expressions:
            val = expr.evaluate(env)
            forbid_random(val, "print")
            values.append(str(val))
        print(" ".join(values))
    
    def __repr__(self):
        return f"Print({self.expressions})"


class PrintlnNode(Node):
    """Вертикальный вывод - каждый элемент с новой строки"""
    def __init__(self, expressions):
        self.expressions = expressions
    
    def execute(self, env):
        for expr in self.expressions:
            val = expr.evaluate(env)
            forbid_random(val, "println")
            
            if hasattr(val, 'data') and hasattr(val, 'is_2d'):
                if val.is_2d:
                    for row in val.data:
                        print(row)
                else:
                    for item in val.data:
                        print(item)
            elif isinstance(val, list):
                if val and isinstance(val[0], list):
                    for row in val:
                        print(row)
                else:
                    for item in val:
                        print(item)
            else:
                print(val)
    
    def __repr__(self):
        return f"Println({self.expressions})"


def parse_print(parser):
    parser.expect('PRINT')
    expressions = []
    
    if parser.check('LPAREN'):
        parser.expect('LPAREN')
        if not parser.check('RPAREN'):
            while not parser.check('RPAREN'):
                expr = parser.parse_expression()
                expressions.append(expr)
                if parser.check('COMMA'):
                    parser.expect('COMMA')
                else:
                    break
        parser.expect('RPAREN')
    else:
        expr = parser.parse_expression()
        expressions.append(expr)
    
    return PrintNode(expressions)


def parse_println(parser):
    parser.expect('PRINTLN')
    expressions = []
    
    if parser.check('LPAREN'):
        parser.expect('LPAREN')
        if not parser.check('RPAREN'):
            while not parser.check('RPAREN'):
                expr = parser.parse_expression()
                expressions.append(expr)
                if parser.check('COMMA'):
                    parser.expect('COMMA')
                else:
                    break
        parser.expect('RPAREN')
    else:
        expr = parser.parse_expression()
        expressions.append(expr)
    
    return PrintlnNode(expressions)