# ast_nodes/functions/trimtext.py
"""Функция TrimText - удаление символов слева или справа"""

from ..base import Node
from runtime.random_source import forbid_random


class TrimTextNode(Node):
    def __init__(self, data, count, direction):
        self.data = data
        self.count = count
        self.direction = direction

    def _trim_single(self, value, count, direction):
        if value is None:
            return ""
        
        str_val = str(value)
        
        if direction == "left":
            return str_val[count:] if len(str_val) > count else ""
        elif direction == "right":
            return str_val[:-count] if len(str_val) > count else ""
        else:
            raise ValueError(f"Неизвестное направление: {direction}. Используйте 'left' или 'right'")

    def evaluate(self, env):
        from runtime.matrix import MatrExMatrix
        
        data_obj = self.data.evaluate(env)
        forbid_random(data_obj, "trimtext")
        
        count = self.count.evaluate(env)
        forbid_random(count, "trimtext")
        if not isinstance(count, (int, float)):
            raise TypeError(f"Количество должно быть числом, получен {type(count)}")
        count = int(count)
        
        direction = self.direction.evaluate(env)
        forbid_random(direction, "trimtext")
        if not isinstance(direction, str):
            raise TypeError(f"Направление должно быть строкой, получен {type(direction)}")
        direction = direction.lower()
        
        if direction not in ["left", "right"]:
            raise ValueError(f"Направление должно быть 'left' или 'right', получен {direction}")

        if isinstance(data_obj, (int, float, str)):
            return self._trim_single(data_obj, count, direction)

        if hasattr(data_obj, 'data') and not data_obj.is_2d:
            result = []
            for item in data_obj.data:
                result.append(self._trim_single(item, count, direction))
            return MatrExMatrix(result, False)

        if hasattr(data_obj, 'data') and data_obj.is_2d:
            result = []
            for row in data_obj.data:
                new_row = []
                for item in row:
                    new_row.append(self._trim_single(item, count, direction))
                result.append(new_row)
            return MatrExMatrix(result, True)

        if isinstance(data_obj, list):
            if data_obj and isinstance(data_obj[0], list):
                result = []
                for row in data_obj:
                    new_row = []
                    for item in row:
                        new_row.append(self._trim_single(item, count, direction))
                    result.append(new_row)
                return MatrExMatrix(result, True)
            else:
                result = []
                for item in data_obj:
                    result.append(self._trim_single(item, count, direction))
                return MatrExMatrix(result, False)

        raise TypeError(f"trimtext() работает со строками, числами, векторами и матрицами, получен {type(data_obj)}")

    def __repr__(self):
        return f"trimtext({self.data}, {self.count}, {self.direction})"