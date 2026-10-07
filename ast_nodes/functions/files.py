from ..base_nodes import Node


class OpenExcelNode(Node):
    def __init__(self, filename, sheet=None):
        self.filename = filename
        self.sheet = sheet
    
    def evaluate(self, env):
        from runtime.excel import ExcelHandler
        file_name = self.filename.evaluate(env)
        if self.sheet is not None:
            sheet_val = self.sheet.evaluate(env)
            if isinstance(sheet_val, str):
                return ExcelHandler.load(file_name, sheet_name=sheet_val)
            elif isinstance(sheet_val, (int, float)):
                return ExcelHandler.load(file_name, sheet_index=int(sheet_val))
            else:
                raise TypeError("Вкладка должна быть строкой или числом")
        else:
            return ExcelHandler.load(file_name)
    
    def execute(self, env):
        return self.evaluate(env)
    
    def __repr__(self):
        return f"OpenExcel({self.filename}, {self.sheet})"


class OpenExcelShowNode(Node):
    def evaluate(self, env):
        from runtime.excel import ExcelHandler
        return ExcelHandler.load_with_dialog()
    
    def execute(self, env):
        return self.evaluate(env)
    
    def __repr__(self):
        return "OpenExcelShow()"


class SaveExcelNode(Node):
    def __init__(self, data, filename, sheet=None):
        self.data = data
        self.filename = filename
        self.sheet = sheet
    
    def evaluate(self, env):
        from runtime.excel import ExcelHandler
        if isinstance(self.data, str):
            matrix_obj = env.get(self.data)
        else:
            matrix_obj = self.data.evaluate(env)
        
        file_name = self.filename.evaluate(env)
        sheet_name = self.sheet.evaluate(env) if self.sheet else "Sheet1"
        
        return ExcelHandler.save(matrix_obj, file_name, sheet_name)
    
    def execute(self, env):
        return self.evaluate(env)
    
    def __repr__(self):
        return f"SaveExcel({self.data}, {self.filename}, {self.sheet})"


class SaveExcelShowNode(Node):
    def __init__(self, data):
        self.data = data
    
    def evaluate(self, env):
        from runtime.excel import ExcelHandler
        if isinstance(self.data, str):
            matrix_obj = env.get(self.data)
        else:
            matrix_obj = self.data.evaluate(env)
        return ExcelHandler.save_with_dialog(matrix_obj)
    
    def execute(self, env):
        return self.evaluate(env)
    
    def __repr__(self):
        return f"SaveExcelShow({self.data})"


class OpenTxtNode(Node):
    def __init__(self, filename):
        self.filename = filename
    
    def evaluate(self, env):
        from runtime.txt import TxtHandler
        return TxtHandler.load(self.filename.evaluate(env))
    
    def execute(self, env):
        return self.evaluate(env)
    
    def __repr__(self):
        return f"OpenTxt({self.filename})"


class OpenTxtShowNode(Node):
    def evaluate(self, env):
        from runtime.txt import TxtHandler
        return TxtHandler.load_with_dialog()
    
    def execute(self, env):
        return self.evaluate(env)
    
    def __repr__(self):
        return "OpenTxtShow()"


class SaveTxtNode(Node):
    def __init__(self, data, filename):
        self.data = data
        self.filename = filename
    
    def evaluate(self, env):
        from runtime.txt import TxtHandler
        if isinstance(self.data, str):
            content = env.get(self.data)
        else:
            content = self.data.evaluate(env)
        if not isinstance(content, str):
            content = str(content)
        return TxtHandler.save(content, self.filename.evaluate(env))
    
    def execute(self, env):
        return self.evaluate(env)
    
    def __repr__(self):
        return f"SaveTxt({self.data}, {self.filename})"


class SaveTxtShowNode(Node):
    def __init__(self, data):
        self.data = data
    
    def evaluate(self, env):
        from runtime.txt import TxtHandler
        if isinstance(self.data, str):
            content = env.get(self.data)
        else:
            content = self.data.evaluate(env)
        if not isinstance(content, str):
            content = str(content)
        return TxtHandler.save_with_dialog(content)
    
    def execute(self, env):
        return self.evaluate(env)
    
    def __repr__(self):
        return f"SaveTxtShow({self.data})"


class OpenDBNode(Node):
    def __init__(self, filename, table):
        self.filename = filename
        self.table = table
    
    def evaluate(self, env):
        from runtime.database import DBHandler
        return DBHandler.load(self.filename.evaluate(env), self.table.evaluate(env))
    
    def execute(self, env):
        return self.evaluate(env)
    
    def __repr__(self):
        return f"OpenDB({self.filename}, {self.table})"