# parser/program.py
"""
Парсинг программы.
"""

from environment import Environment
from errors import ArrayVatorError
from .base import Parser
from .statements import parse_statement


def parse_program(self):
    env = Environment()
    env.set('error', None)

    statements = []

    # ============================================================
    # ЭТАП 1: ПАРСИНГ
    # ============================================================
    while self.peek():
        try:
            stmt = parse_statement(self)
            if stmt:
                statements.append(stmt)
        except ArrayVatorError:
            raise
        except SyntaxError as e:
            token = self.peek()
            ctx = self._get_context(token)
            raise ArrayVatorError(
                code="UNEXPECTED_TOKEN",
                context=ctx,
                message=str(e),
            )

    # ============================================================
    # ЭТАП 2: ВЫПОЛНЕНИЕ
    # ============================================================
    #
    # Логика:
    #   - ArrayVatorError — ПРОБРАСЫВАЕТСЯ наверх (прерывает программу).
    #     Это "логические" ошибки: неверный индекс, неизвестная функция,
    #     неверная единица datetrunc и т.д.
    #
    #   - Другие исключения (TypeError, ValueError, IndexError, ...)
    #     — превращаются в ArrayVatorError с понятным текстом
    #     и ТОЖЕ ПРОБРАСЫВАЮТСЯ. Программа останавливается.
    #
    #   - Исключение: если исключение возникло внутри `try { ... } catch { ... }`,
    #     оно ловится TryNode — не пробрасывается.
    #
    # Это значит: пользователь ВСЕГДА видит ошибку. Никаких "пустых экранов".
    #

    for stmt in statements:
        try:
            if hasattr(stmt, 'execute'):
                stmt.execute(env)
            else:
                stmt.evaluate(env)
        except ArrayVatorError:
            # Логическая ошибка — прерываем.
            raise
        except Exception as e:
            # Любая другая ошибка — превращаем в ArrayVatorError
            # и прерываем. Пользователь должен её увидеть.
            raise _wrap_exception(e, stmt)

    return env


def _wrap_exception(e, stmt=None):
    """
    Превращает любое исключение в ArrayVatorError с понятным текстом.
    """
    # Уже ArrayVatorError — не трогаем
    if isinstance(e, ArrayVatorError):
        return e

    # Имя типа — для сообщения
    type_name = type(e).__name__
    message = str(e) if str(e) else type_name

    # Спец-обработка известных типов
    if isinstance(e, TypeError):
        text = (
            f"Ошибка типа: {message}\n"
            f"  Проверьте типы аргументов."
        )
    elif isinstance(e, ValueError):
        text = (
            f"Ошибка значения: {message}\n"
            f"  Проверьте значения аргументов."
        )
    elif isinstance(e, IndexError):
        text = (
            f"Ошибка индекса: {message}\n"
            f"  Проверьте индексы (номера строк/столбцов)."
        )
    elif isinstance(e, NameError):
        text = (
            f"Ошибка имени: {message}\n"
            f"  Переменная не определена."
        )
    elif isinstance(e, ZeroDivisionError):
        text = (
            f"Деление на ноль: {message}"
        )
    elif isinstance(e, MemoryError):
        text = (
            f"Недостаточно памяти: {message}\n"
            f"  Попробуйте уменьшить объём данных."
        )
    else:
        text = (
            f"Ошибка выполнения: {message}\n"
            f"  Тип: {type_name}"
        )

    return ArrayVatorError(
        code="RUNTIME_ERROR",
        context=None,
        message=text,
    )


Parser.parse_program = parse_program