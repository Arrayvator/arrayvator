"""
Парсинг Excel функций: OPENEXCEL, SAVEEXCEL, OPENEXCELSHOW, SAVEEXCELSHOW
"""

from ast_nodes import OpenExcelNode, SaveExcelNode, OpenExcelShowNode, SaveExcelShowNode


def parse_excel(self, token_type):
    """Парсинг Excel функций"""
    self.expect('LPAREN')
    
    if token_type == 'OPENEXCEL':
        file_path = self.parse_expression()
        sheet_param = None
        if self.check('COMMA'):
            self.expect('COMMA')
            if self.check('ALL'):
                sheet_param = self.parse_expression()
            else:
                sheet_param = self.parse_expression()
        self.expect('RPAREN')
        return OpenExcelNode(file_path, sheet_param)
    
    elif token_type == 'SAVEEXCEL':
        data = self.parse_expression()
        self.expect('COMMA')
        file_path = self.parse_expression()
        sheet_param = None
        if self.check('COMMA'):
            self.expect('COMMA')
            sheet_param = self.parse_expression()
        self.expect('RPAREN')
        return SaveExcelNode(data, file_path, sheet_param)
    
    elif token_type == 'OPENEXCELSHOW':
        self.expect('RPAREN')
        return OpenExcelShowNode()
    
    elif token_type == 'SAVEEXCELSHOW':
        data = self.parse_expression()
        sheet_name = None
        if self.check('COMMA'):
            self.expect('COMMA')
            sheet_name = self.parse_expression()
        self.expect('RPAREN')
        return SaveExcelShowNode(data, sheet_name)