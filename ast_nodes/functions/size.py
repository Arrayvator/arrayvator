# ast_nodes/functions/size.py
"""
Функции размеров: LenRowNode, LenColNode, LenNode

len() — длина:
    - для строки: количество символов
    - для числа: количество символов в строковом представлении
    - для вектора: количество элементов
    - для None: 0
    - для матрицы: ОШИБКА (используй lenrow или lencol)

lenrow() — количество строк:
    - для матрицы/вектора: rows
    - для DuckDBTable: COUNT(*) через SQL

lencol() — количество столбцов:
    - для матрицы/вектора: cols
    - для DuckDBTable: количество столбцов через SQL
"""

from ..base import Node
from ast_nodes.base import unwrap_random


# ============================================================
# ХЕЛПЕР: определение DuckDBTable
# ============================================================
def _is_duckdb(val):
    """Проверяет, является ли значение DuckDBTable."""
    try:
        from duckdb_engine import DuckDBTable
        return isinstance(val, DuckDBTable)
    except ImportError:
        return False


# ============================================================
# LENROW — количество строк
# ============================================================
class LenRowNode(Node):
    """lenrow() — количество строк"""
    def __init__(self, arg):
        self.arg = arg

    def evaluate(self, env):
        value = unwrap_random(self.arg.evaluate(env))

        # --- DuckDBTable ---
        if _is_duckdb(value):
            return value.get_row_count()

        # --- MatrExMatrix ---
        if hasattr(value, 'rows'):
            return value.rows

        # --- Список ---
        if isinstance(value, list):
            return len(value)

        raise TypeError("lenrow() работает только с матрицами и векторами")

    def __repr__(self):
        return f"LenRow({self.arg})"


# ============================================================
# LENCOL — количество столбцов
# ============================================================
class LenColNode(Node):
    """lencol() — количество столбцов"""
    def __init__(self, arg):
        self.arg = arg

    def evaluate(self, env):
        value = unwrap_random(self.arg.evaluate(env))

        # --- DuckDBTable ---
        if _is_duckdb(value):
            return len(value.get_columns())

        # --- MatrExMatrix ---
        if hasattr(value, 'cols'):
            return value.cols

        # --- Список ---
        if isinstance(value, list):
            if value and isinstance(value[0], list):
                return len(value[0])
            return 1

        raise TypeError("lencol() работает только с матрицами и векторами")

    def __repr__(self):
        return f"LenCol({self.arg})"


# ============================================================
# LEN — универсальная длина
# ============================================================
class LenNode(Node):
    """
    len() — универсальная длина.

    Работает для:
        - строки (количество символов)
        - числа (количество символов, включая . и -)
        - вектора (количество элементов)
        - None (возвращает 0)

    НЕ работает для матриц — используй lenrow() или lencol().
    """
    def __init__(self, arg):
        self.arg = arg

    def evaluate(self, env):
        value = unwrap_random(self.arg.evaluate(env))

        # ============================================================
        # DuckDBTable — возвращаем количество строк
        # ============================================================
        if _is_duckdb(value):
            return value.get_row_count()

        # ============================================================
        # None — 0
        # ============================================================
        if value is None:
            return 0

        # ============================================================
        # Матрица — ошибка
        # ============================================================
        if hasattr(value, 'is_2d') and value.is_2d:
            raise TypeError(
                "len() не работает с двумерной матрицей. "
                "Используйте lenrow() для строк или lencol() для столбцов."
            )

        # ============================================================
        # Вектор (MatrExMatrix с is_2d=False)
        # ============================================================
        if hasattr(value, 'data') and not value.is_2d:
            return len(value.data)

        # ============================================================
        # Список (Python)
        # ============================================================
        if isinstance(value, list):
            if value and isinstance(value[0], list):
                raise TypeError(
                    "len() не работает с двумерным списком. "
                    "Используйте lenrow() или lencol()."
                )
            return len(value)

        # ============================================================
        # Числа, строки, bool — длина строкового представления
        # ============================================================
        if isinstance(value, (int, float, str, bool)):
            return len(str(value))

        raise TypeError(f"len() не работает с типом {type(value).__name__}")

    def __repr__(self):
        return f"Len({self.arg})"