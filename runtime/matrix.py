# runtime/matrix.py
class MatrExMatrix:
    def __init__(self, data, is_2d=False):
        if not isinstance(data, list):
            raise TypeError("Матрица должна быть списком")
        self.data = data
        self.rows = len(data)
        self.is_2d = is_2d
        
        # Проверяем, является ли это 2D матрицей
        if is_2d or (data and isinstance(data[0], list)):
            self.is_2d = True
            # Находим максимальную длину строки
            max_cols = 0
            for row in data:
                if isinstance(row, list):
                    if len(row) > max_cols:
                        max_cols = len(row)
                else:
                    if 1 > max_cols:
                        max_cols = 1
            # Выравниваем все строки
            for i in range(len(data)):
                if not isinstance(data[i], list):
                    data[i] = [data[i]]
                while len(data[i]) < max_cols:
                    data[i].append(None)
            self.cols = max_cols
        else:
            self.is_2d = False
            self.cols = 1
            # Убеждаемся, что все элементы не являются списками
            for i in range(len(data)):
                if isinstance(data[i], list):
                    data[i] = data[i][0] if data[i] else None
    
    def __str__(self):
        if self.rows == 0:
            return "[]"
        
        # ============================================================
        # ВЕКТОР (1D)
        # ============================================================
        if not self.is_2d:
            result = "["
            items = []
            for x in self.data:
                if x is None:
                    items.append("None")
                else:
                    items.append(str(x))
            result += ", ".join(items) + "]"
            return result
        
        # ============================================================
        # 2D МАТРИЦА — красивое выравнивание
        # ============================================================
        
        # Приводим все значения к строкам
        display_data = []
        for i in range(self.rows):
            row = []
            for j in range(self.cols):
                if i < len(self.data) and j < len(self.data[i]):
                    val = self.data[i][j]
                    if val is None:
                        row.append("None")
                    else:
                        row.append(str(val))
                else:
                    row.append("None")
            display_data.append(row)
        
        # ============================================================
        # ОПРЕДЕЛЯЕМ ШИРИНУ СТОЛБЦОВ
        # ============================================================
        col_widths = []
        for j in range(self.cols):
            max_width = 0
            for i in range(self.rows):
                val = display_data[i][j] if j < len(display_data[i]) else "None"
                if len(val) > max_width:
                    max_width = len(val)
            # Минимум 4 символа
            col_widths.append(max(4, max_width))
        
        # ============================================================
        # ОПРЕДЕЛЯЕМ ВЫРАВНИВАНИЕ ДЛЯ КАЖДОГО СТОЛБЦА
        # ============================================================
        # Логика:
        #   - Если в столбце есть строки → влево (<)
        #   - Если только числа (int/float) → вправо (>)
        #   - None игнорируется при определении
        # ============================================================
        col_aligns = []
        for j in range(self.cols):
            has_string = False
            has_number = False
            
            for i in range(self.rows):
                if i < len(self.data) and j < len(self.data[i]):
                    val = self.data[i][j]
                    if val is None:
                        continue
                    if isinstance(val, str):
                        has_string = True
                    elif isinstance(val, (int, float)):
                        has_number = True
            
            # Если в столбце есть строки — влево
            # Если только числа — вправо
            if has_string:
                col_aligns.append('<')   # влево
            elif has_number:
                col_aligns.append('>')   # вправо
            else:
                col_aligns.append('<')   # по умолчанию влево
        
        # ============================================================
        # ФОРМИРУЕМ СТРОКИ
        # ============================================================
        result = []
        
        for i in range(self.rows):
            row = display_data[i]
            row_parts = []
            
            for j in range(self.cols):
                val = row[j] if j < len(row) else "None"
                align = col_aligns[j]
                width = col_widths[j]
                
                if align == '>':
                    row_parts.append(f"{val:>{width}}")
                elif align == '^':
                    row_parts.append(f"{val:^{width}}")
                else:  # '<'
                    row_parts.append(f"{val:<{width}}")
            
            # Разделитель между столбцами — двойной пробел
            result.append("  ".join(row_parts))
        
        return "\n".join(result)
    
    def __repr__(self):
        return self.__str__()
    
    def __len__(self):
        return self.rows
    
    def sum(self):
        if self.rows == 0:
            return 0
        if not self.is_2d:
            total = 0
            for val in self.data:
                if isinstance(val, (int, float)):
                    total += val
            return total
        total = 0
        for row in self.data:
            for val in row:
                if isinstance(val, (int, float)):
                    total += val
        return total
    
    # ============================================================
    # НОВЫЕ МЕТОДЫ для поддержки random()
    # ============================================================
    
    def is_empty(self):
        """Пустая матрица или вектор"""
        return self.rows == 0
    
    def replace_data(self, new_data, is_2d=None):
        """
        Заменяет данные матрицы НА МЕСТЕ (сохраняя ссылку на объект).
        Нужно для случая m = random(...) — мы меняем существующий объект,
        чтобы все ссылки на него (в env, в других переменных) увидели новые данные.
        """
        if is_2d is None:
            is_2d = self.is_2d
        
        tmp = MatrExMatrix(new_data, is_2d)
        self.data = tmp.data
        self.rows = tmp.rows
        self.cols = tmp.cols
        self.is_2d = tmp.is_2d