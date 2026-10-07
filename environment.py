# environment.py
"""
Окружение выполнения ArrayVator.

Хранит переменные: name → value.
Специальная переменная `error` — текст последней ошибки (или None).
"""


class Environment:
    def __init__(self, parent=None):
        self.vars = {}
        self.parent = parent
        # error всегда доступно — как встроенная переменная
        self.vars['error'] = None

    def get(self, name):
        # ПРИВОДИМ ИМЯ К НИЖНЕМУ РЕГИСТРУ
        name = name.lower()
        if name in self.vars:
            return self.vars[name]
        if self.parent:
            return self.parent.get(name)
        raise NameError(f"Переменная '{name}' не определена")

    def set(self, name, value):
        # ПРИВОДИМ ИМЯ К НИЖНЕМУ РЕГИСТРУ
        name = name.lower()
        self.vars[name] = value

    def has(self, name):
        """Проверяет, существует ли переменная."""
        name = name.lower()
        if name in self.vars:
            return True
        if self.parent:
            return self.parent.has(name)
        return False

    def create_child(self):
        return Environment(parent=self)

    def __repr__(self):
        return f"Environment({self.vars})"