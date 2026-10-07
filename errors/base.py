# errors/base.py
"""
Базовые классы ошибок ArrayVator.
"""

from .i18n import t


class ErrorContext:
    """
    Контекст ошибки: строка, столбец, фрагмент кода.
    """
    def __init__(self, line=None, column=None, source_line=None,
                 source_code=None, token=None):
        self.line = line
        self.column = column
        self.source_line = source_line   # сама строка кода
        self.source_code = source_code   # весь исходник
        self.token = token               # токен, на котором упали
    
    def has_location(self):
        return self.line is not None or self.column is not None


class ArrayVatorError(Exception):
    """
    Базовая ошибка ArrayVator.
    
    Параметры:
        code       — код ошибки из базы (например 'MISSING_RPAREN')
        message    — готовое сообщение (если задано — используется вместо базы)
        context    — ErrorContext с координатами
        suggestion — готовая подсказка (если задана)
        example    — пример правильного кода
    """
    def __init__(self, code=None, message=None, context=None,
                 suggestion=None, example=None):
        self.code = code
        self.message = message
        self.context = context
        self.suggestion = suggestion
        self.example = example
        
        # Формируем финальный текст
        final = self._build_final_message()
        super().__init__(final)
    
    def _build_final_message(self):
        if self.message:
            return self.message
        if self.code:
            from .db_ru import MESSAGES_RU
            from .i18n import get_language
            db = MESSAGES_RU if get_language() == "ru" else None
            if db and self.code in db:
                return db[self.code]
            return f"Ошибка: {self.code}"
        return "Неизвестная ошибка ArrayVator"


# ============================================================
# БЫСТРЫЕ ФАБРИКИ
# ============================================================
def make_error(code, context=None, **kwargs):
    """Создаёт ArrayVatorError с базой сообщений"""
    return ArrayVatorError(code=code, context=context, **kwargs)


def syntax_error(code, line=None, column=None, source_line=None, **kwargs):
    """Быстрая фабрика синтаксической ошибки"""
    ctx = ErrorContext(line=line, column=column, source_line=source_line)
    return ArrayVatorError(code=code, context=ctx, **kwargs)