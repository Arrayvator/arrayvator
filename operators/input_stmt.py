from ast_nodes import Node


class InputNode(Node):
    def __init__(self, prompt=None):
        self.prompt = prompt
    
    def evaluate(self, env):
        prompt_text = self.prompt.evaluate(env) if self.prompt else ""
        user_input = input(prompt_text)
        try:
            return float(user_input)
        except:
            return user_input
    
    def execute(self, env):
        return self.evaluate(env)
    
    def __repr__(self):
        return f"Input({self.prompt})"


def parse_input(parser):
    parser.expect('INPUT')
    parser.expect('LPAREN')
    prompt = None
    if not parser.check('RPAREN'):
        prompt = parser.parse_expression()
    parser.expect('RPAREN')
    return InputNode(prompt)