# ============================================================
# ФАЙЛ: ast_nodes/functions/delete_txt.py
# УНИВЕРСАЛЬНАЯ ФУНКЦИЯ УДАЛЕНИЯ ТЕКСТА
# ============================================================

from ..base_nodes import Node


class DeleteTXTNode(Node):
    """
    Универсальная функция удаления текста (изменяет данные напрямую)
    
    Синтаксис:
        DeleteTXT(данные, позиция, количество)
    
    Параметры:
        данные     - ячейка, столбец, диапазон или вся матрица
        позиция    - Left (слева) или Right (справа)
        количество - сколько символов удалить
    
    ПРАВИЛА:
        - Если указан НОМЕР столбца/строки → удаляем ВСЁ (включая заголовки)
        - Если указано НАЗВАНИЕ столбца → заголовок НЕ ТРОГАЕМ
        - Если указано НАЗВАНИЕ строки → ИМЯ В ПЕРВОМ СТОЛБЦЕ НЕ ТРОГАЕМ!
        - Если указана вся матрица (data) → заголовки НЕ ТРОГАЕМ
    
    Примеры:
        DeleteTXT(data[:, 2], Left, 3)           # столбец ПО НОМЕРУ → удаляем и заголовок
        DeleteTXT(data[:, "Телефон"], Left, 3)   # столбец ПО ИМЕНИ → заголовок НЕ ТРОГАЕМ
        DeleteTXT(data["Анна", :], Left, 3)      # строка ПО ИМЕНИ → имя НЕ ТРОГАЕМ!
        DeleteTXT(data, Left, 3)                 # вся матрица → заголовки НЕ ТРОГАЕМ
        DeleteTXT(data[2, 2], Left, 3)           # ячейка → всегда меняем
    """
    
    def __init__(self, data, position, count):
        self.data = data
        self.position = position
        self.count = count
    
    def _delete_left(self, text, count):
        """Удаляет N символов слева"""
        if not isinstance(text, str):
            text = str(text)
        
        if len(text) <= count:
            return ""
        
        return text[count:]
    
    def _delete_right(self, text, count):
        """Удаляет N символов справа"""
        if not isinstance(text, str):
            text = str(text)
        
        if len(text) <= count:
            return ""
        
        return text[:-count]
    
    def _process_value(self, value, position, count):
        """Обрабатывает одно значение"""
        if not isinstance(value, str):
            value = str(value)
        
        if position == "Left":
            return self._delete_left(value, count)
        elif position == "Right":
            return self._delete_right(value, count)
        else:
            return value
    
    def _process_matrix(self, matrix, position, count, start_row=0, skip_first_col=False):
        """Обрабатывает матрицу, начиная с указанной строки"""
        for i in range(start_row, matrix.rows):
            start_col = 1 if skip_first_col and i == start_row else 0
            for j in range(start_col, matrix.cols):
                if j < len(matrix.data[i]):
                    matrix.data[i][j] = self._process_value(matrix.data[i][j], position, count)
        return matrix
    
    def evaluate(self, env):
        # Получаем данные
        if isinstance(self.data, str):
            obj = env.get(self.data)
        else:
            obj = self.data.evaluate(env)
        
        # Получаем позицию (Left или Right)
        position = self.position.evaluate(env)
        if not isinstance(position, str):
            position = str(position)
        
        # Получаем количество символов
        count = self.count.evaluate(env)
        if not isinstance(count, (int, float)):
            count = int(count)
        else:
            count = int(count)
        
        # ============================================================
        # СЛУЧАЙ 1: IndexNode (data[строка, столбец])
        # ============================================================
        if hasattr(self.data, 'matrix') and hasattr(self.data, 'indices'):
            matrix = self.data.matrix.evaluate(env)
            indices = self.data.indices
            
            if len(indices) == 2:
                row_idx = indices[0]
                col_idx = indices[1]
                
                row_val = row_idx.evaluate(env) if hasattr(row_idx, 'evaluate') else row_idx
                col_val = col_idx.evaluate(env) if hasattr(col_idx, 'evaluate') else col_idx
                
                # ============================================================
                # КОНКРЕТНАЯ ЯЧЕЙКА: data[строка, столбец]
                # ============================================================
                if not isinstance(row_val, str) and not isinstance(col_val, str):
                    row_num = int(row_val) - 1
                    col_num = int(col_val) - 1
                    
                    if 0 <= row_num < matrix.rows and 0 <= col_num < matrix.cols:
                        # ✅ Ячейка - всегда меняем
                        matrix.data[row_num][col_num] = self._process_value(
                            matrix.data[row_num][col_num], position, count
                        )
                    return matrix
                
                # ============================================================
                # ЦЕЛЫЙ СТОЛБЕЦ
                # ============================================================
                if isinstance(row_val, str) and (row_val == 'all' or row_val == ':'):
                    # Определяем столбец
                    if isinstance(col_val, str):
                        # ===== ПО ИМЕНИ =====
                        col_num = self._find_column_by_name(matrix, col_val)
                        if col_num is None:
                            return matrix
                        # ✅ ПО ИМЕНИ → заголовок НЕ ТРОГАЕМ (начинаем со строки 1)
                        start_row = 1
                    else:
                        # ===== ПО НОМЕРУ =====
                        col_num = int(col_val) - 1
                        # ✅ ПО НОМЕРУ → удаляем ВСЁ (включая заголовок)
                        start_row = 0
                    
                    if col_num is not None and 0 <= col_num < matrix.cols:
                        for i in range(start_row, matrix.rows):
                            if col_num < len(matrix.data[i]):
                                matrix.data[i][col_num] = self._process_value(
                                    matrix.data[i][col_num], position, count
                                )
                    return matrix
                
                # ============================================================
                # ЦЕЛАЯ СТРОКА
                # ============================================================
                if isinstance(col_val, str) and (col_val == 'all' or col_val == ':'):
                    if isinstance(row_val, str):
                        # ===== ПО ИМЕНИ =====
                        row_num = self._find_row_by_name(matrix, row_val)
                        if row_num is None:
                            return matrix
                        
                        # ✅ ПО ИМЕНИ → имя (первый столбец) НЕ ТРОГАЕМ!
                        if row_num > 0:
                            # Пропускаем первый столбец (где имя)
                            for j in range(1, matrix.cols):
                                if j < len(matrix.data[row_num]):
                                    matrix.data[row_num][j] = self._process_value(
                                        matrix.data[row_num][j], position, count
                                    )
                    else:
                        # ===== ПО НОМЕРУ =====
                        row_num = int(row_val) - 1
                        if 0 <= row_num < matrix.rows:
                            # ✅ ПО НОМЕРУ → удаляем ВСЁ (включая первый столбец)
                            for j in range(matrix.cols):
                                if j < len(matrix.data[row_num]):
                                    matrix.data[row_num][j] = self._process_value(
                                        matrix.data[row_num][j], position, count
                                    )
                    return matrix
        
        # ============================================================
        # СЛУЧАЙ 2: Обычная матрица или вектор
        # ============================================================
        elif hasattr(obj, 'data') and hasattr(obj, 'rows'):
            # ✅ ВСЯ МАТРИЦА → заголовки НЕ ТРОГАЕМ (начинаем со строки 1)
            if hasattr(obj, 'is_2d') and obj.is_2d:
                self._process_matrix(obj, position, count, start_row=1)
            else:
                # Вектор - обрабатываем все элементы
                self._process_matrix(obj, position, count, start_row=0)
            return obj
        
        # ============================================================
        # СЛУЧАЙ 3: Строка
        # ============================================================
        elif isinstance(obj, str):
            return self._process_value(obj, position, count)
        
        return obj
    
    def _find_column_by_name(self, obj, name):
        """Находит номер столбца по имени (в заголовке)"""
        if obj.rows > 0 and obj.data:
            for j in range(obj.cols):
                if j < len(obj.data[0]):
                    if str(obj.data[0][j]).strip().lower() == name.lower():
                        return j
        return None
    
    def _find_row_by_name(self, obj, name):
        """Находит номер строки по имени (в первом столбце)"""
        for i in range(obj.rows):
            if obj.data[i] and len(obj.data[i]) > 0:
                if str(obj.data[i][0]).strip().lower() == name.lower():
                    return i
        return None
    
    def execute(self, env):
        return self.evaluate(env)
    
    def __repr__(self):
        return f"DeleteTXT({self.data}, {self.position}, {self.count})"