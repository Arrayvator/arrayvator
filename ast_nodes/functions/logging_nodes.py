# ast_nodes/functions/logging_nodes.py
"""
LogToFile / LogOff — управление логированием

СИНТАКСИС:
    LogToFile("log.txt")                # уровень "all"
    LogToFile("log.txt", "matrix")      # без содержимого матриц
    LogToFile("log.txt", "summary")     # только итоги
    LogOff()                             # выключить
"""

from ..base import Node


class LogToFileNode(Node):
    """LogToFile("file.txt" [, level]) — включить логирование"""

    def __init__(self, file_path, level=None):
        self.file_path = file_path
        self.level = level

    def evaluate(self, env):
        from runtime.logger import logger

        path = self.file_path.evaluate(env) if hasattr(self.file_path, 'evaluate') else self.file_path
        level_val = None
        if self.level is not None:
            level_val = self.level.evaluate(env) if hasattr(self.level, 'evaluate') else self.level

        if not isinstance(path, str):
            raise TypeError(f"Путь должен быть строкой, получен {type(path)}")

        if level_val is None:
            level_val = 'all'
        elif not isinstance(level_val, str):
            raise TypeError(f"Уровень должен быть строкой, получен {type(level_val)}")

        if level_val not in ('all', 'matrix', 'summary'):
            raise ValueError(
                f"Уровень должен быть 'all', 'matrix' или 'summary', "
                f"получено '{level_val}'"
            )

        success, message = logger.start(path, level_val)
        if not success:
            raise RuntimeError(message)

        return message

    def __repr__(self):
        if self.level is not None:
            return f"LogToFile({self.file_path}, {self.level})"
        return f"LogToFile({self.file_path})"


class LogOffNode(Node):
    """LogOff() — выключить логирование"""

    def __init__(self):
        pass

    def evaluate(self, env):
        from runtime.logger import logger
        return logger.stop()

    def __repr__(self):
        return "LogOff()"