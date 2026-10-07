# runtime/random_source.py
"""
Маркер "источник случайных чисел".
"""

import random as py_random


class RandomSource:
    def __init__(self, start, end, precision):
        self.start = start
        self.end = end
        self.precision = int(precision)
    
    def generate_one(self):
        if self.precision == 0:
            return py_random.randint(int(self.start), int(self.end))
        val = py_random.uniform(float(self.start), float(self.end))
        return round(val, self.precision)
    
    def generate(self, count):
        return [self.generate_one() for _ in range(count)]
    
    def generate_2d(self, rows, cols):
        return [[self.generate_one() for _ in range(cols)] for _ in range(rows)]
    
    def __repr__(self):
        return f"RandomSource({self.start}:{self.end}, {self.precision})"


class RandomMisuseError(Exception):
    """Ошибка: random() использован вне присваивания"""
    pass


def forbid_random(val, context=""):
    """
    Проверяет: если val — RandomSource, бросает понятную ошибку.
    """
    if not isinstance(val, RandomSource):
        return
    
    ctx = f" в '{context}'" if context else ""
    
    example_bad = f"    {context}(random(...))" if context else "    x = f(random(...))"
    
    msg = (
        f"\n"
        f"❌ random() нельзя использовать{ctx} — только в присваивании.\n"
        f"\n"
        f"  ❌ Так нельзя:\n"
        f"{example_bad}\n"
        f"\n"
        f"  ✅ Правильно:\n"
        f"      x = random(0:10, 0)               — скаляр\n"
        f"      m = random(0:10, 0)               — заполнить всю матрицу/вектор\n"
        f"      m[1, all] = random(0:10, 0)       — заполнить строку\n"
        f"      m[all, 2] = random(0:10, 0)       — заполнить столбец\n"
        f"      m[2:3, 2:3] = random(0:10, 0)     — заполнить диапазон\n"
        f"      m[all, all] = random(0:10, 0)     — заполнить всю матрицу"
    )
    raise RandomMisuseError(msg)