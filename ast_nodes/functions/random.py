# ast_nodes/functions/random.py
"""
Функция RANDOM - генерация случайных чисел

СИНТАКСИС:
    random(диапазон, точность)

ПРИМЕРЫ:
    x = random(1:10, 0)              # одно число (если x — новая переменная)
    m[all, all] = random(1:10, 0)    # вся матрица
    m[1, all] = random(1:10, 0)      # строка
    m[2:4, 2:4] = random(1:10, 0)    # диапазон
    print(random(1:10, 0))           # одно число

ВАЖНО:
    RandomNode.evaluate() возвращает RandomSource, а не число.
    Разворот в число/вектор/матрицу происходит в AssignNode, PrintNode
    и других потребителях (см. runtime/random_source.py).
"""

from ..base import Node
from runtime.random_source import RandomSource


class RandomNode(Node):
    def __init__(self, range_start, range_end, precision):
        self.range_start = range_start
        self.range_end = range_end
        self.precision = precision

    def evaluate(self, env):
        start_val = (self.range_start.evaluate(env)
                     if hasattr(self.range_start, 'evaluate')
                     else self.range_start)
        end_val = (self.range_end.evaluate(env)
                   if hasattr(self.range_end, 'evaluate')
                   else self.range_end)
        precision_val = (self.precision.evaluate(env)
                         if hasattr(self.precision, 'evaluate')
                         else self.precision)
        
        return RandomSource(start_val, end_val, int(precision_val))

    def __repr__(self):
        return f"Random({self.range_start}:{self.range_end}, {self.precision})"