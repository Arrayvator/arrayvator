# ast_nodes/base.py
"""
Базовый класс узлов AST.
"""


class Node:
    """Базовый класс для всех узлов AST"""
    pass


def unwrap_random(val):
    """
    Разворачивает RandomSource в одно число.
    """
    from runtime.random_source import RandomSource
    if isinstance(val, RandomSource):
        return val.generate_one()
    return val


# ============================================================
# TRY NODE
# ============================================================
class TryNode(Node):
    """
    Узел обработки ошибок.

    СИНТАКСИС:
        try
        {
            ...
        }
        catch
        {
            ...
        }

        try
        {
            ...
        }
        catch (e)
        {
            ...
        }

    ВНУТРЕННЕЕ:
        - try_body   — список операторов внутри try
        - catch_body — список операторов внутри catch
        - var_name   — имя переменной (по умолчанию 'error')
    """

    def __init__(self, try_body, catch_body, var_name='error'):
        self.try_body = try_body
        self.catch_body = catch_body
        self.var_name = var_name

    def execute(self, env):
        """Выполняет try, при ошибке — catch."""
        try:
            # Сбрасываем error
            env.set('error', None)

            for stmt in self.try_body:
                if hasattr(stmt, 'execute'):
                    stmt.execute(env)
                else:
                    stmt.evaluate(env)

            # Успех — error остаётся None
            env.set('error', None)

        except Exception as e:
            # Ошибка — переходим в catch
            error_text = self._format_error(e)
            env.set('error', error_text)
            env.set(self.var_name, error_text)

            for stmt in self.catch_body:
                if hasattr(stmt, 'execute'):
                    stmt.execute(env)
                else:
                    stmt.evaluate(env)

            # После catch — сбрасываем error
            env.set('error', None)

    def _format_error(self, e):
        """Форматирует исключение в строку."""
        try:
            from errors import ArrayVatorError
            if isinstance(e, ArrayVatorError):
                return str(e)
        except ImportError:
            pass
        return str(e)

    def __repr__(self):
        return f"Try(try={len(self.try_body)}, catch={len(self.catch_body)})"