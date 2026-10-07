# runtime/logger.py
"""
Логирование операций ArrayVator в файл.

Уровни:
    "all"     — всё: имена операций + содержимое матриц
    "matrix"  — имена операций + содержимое матриц (без скаляров)
    "summary" — только имена операций + размеры

Использование:
    LogToFile("log.txt")
    LogToFile("log.txt", "matrix")
    LogToFile("log.txt", "summary")
    LogOff()
"""

import datetime
import os
from pathlib import Path


# ============================================================
# LOGGER
# ============================================================
class Logger:
    def __init__(self):
        self.enabled = False
        self.level = 'all'
        self.file_path = None
        self._file = None
        self._counter = 0
        self._depth = 0

    # ============================================================
    # СТАРТ
    # ============================================================
    def start(self, path, level='all'):
        if self.enabled:
            self.stop()

        try:
            self.file_path = Path(path).resolve()
            self.file_path.parent.mkdir(parents=True, exist_ok=True)

            self._file = open(self.file_path, 'w', encoding='utf-8')

            self.enabled = True
            self.level = level
            self._counter = 0

            ts = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            self._file.write("=" * 70 + "\n")
            self._file.write(f"  ARRAYVATOR LOG\n")
            self._file.write(f"  Начат: {ts}\n")
            self._file.write(f"  Файл: {self.file_path.name}\n")
            self._file.write(f"  Уровень: {level}\n")
            self._file.write("=" * 70 + "\n\n")
            self._file.flush()

            return True, f"Logging started: {self.file_path}"

        except Exception as e:
            self.enabled = False
            self._file = None
            return False, f"Failed to start logging: {e}"

    # ============================================================
    # СТОП
    # ============================================================
    def stop(self):
        if not self._file:
            self.enabled = False
            return False, "Logging was not active"

        try:
            ts = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            self._file.write("\n" + "=" * 70 + "\n")
            self._file.write(f"  КОНЕЦ ЛОГА: {ts}\n")
            self._file.write(f"  Всего записей: {self._counter}\n")
            self._file.write("=" * 70 + "\n")
            self._file.flush()
            self._file.close()

        except Exception:
            pass

        finally:
            self._file = None
            self.enabled = False
            self.file_path = None

        return True, "Logging stopped"

    # ============================================================
    # ЛОГИРОВАНИЕ ОПЕРАЦИИ
    # ============================================================
    def log_operation(self, op_name, description, before=None, after=None):
        if not self.enabled:
            return

        if not self._file:
            return

        try:
            self._counter += 1
            ts = datetime.datetime.now().strftime("%H:%M:%S")
            indent = "  " * self._depth

            self._file.write(
                f"{indent}[{self._counter}] {ts} — {op_name}\n"
            )

            if description:
                self._file.write(f"{indent}    {description}\n")

            if before is not None and self.level in ('all', 'matrix'):
                self._file.write(f"{indent}    До:\n")
                self._file.write(self._format(before, indent + "      "))

            if after is not None and self.level in ('all', 'matrix'):
                self._file.write(f"{indent}    После:\n")
                self._file.write(self._format(after, indent + "      "))

            if self.level == 'summary':
                if before is not None and after is not None:
                    self._file.write(
                        f"{indent}    {self._shape(before)} → "
                        f"{self._shape(after)}\n"
                    )

            self._file.write("\n")
            self._file.flush()

        except Exception:
            pass

    # ============================================================
    # КРАТКОЕ ОПИСАНИЕ РАЗМЕРА
    # ============================================================
    def _shape(self, obj):
        try:
            if obj is None:
                return "None"
            if hasattr(obj, 'is_2d'):
                if obj.is_2d:
                    return f"{obj.rows}×{obj.cols}"
                return f"вектор[{len(obj.data)}]"
            if hasattr(obj, 'table_name') and hasattr(obj, 'get_columns'):
                cols = obj.get_columns()
                rows = obj.get_row_count()
                return f"DuckDB[{rows}×{len(cols)}]"
            if isinstance(obj, list):
                if obj and isinstance(obj[0], list):
                    return f"{len(obj)}×{len(obj[0])}"
                return f"список[{len(obj)}]"
            return type(obj).__name__
        except Exception:
            return "?"

    # ============================================================
    # ФОРМАТИРОВАНИЕ ОБЪЕКТА ДЛЯ ФАЙЛА
    # ============================================================
    def _format(self, obj, indent, max_rows=10, max_cols=6):
        if obj is None:
            return f"{indent}<None>\n"

        try:
            # ---- MatrExMatrix ----
            if hasattr(obj, 'is_2d'):
                data = obj.data

                if not obj.is_2d:
                    lines = []
                    for i, item in enumerate(data[:max_rows]):
                        lines.append(f"{indent}[{i + 1}] {item}")
                    if len(data) > max_rows:
                        lines.append(
                            f"{indent}... (всего {len(data)} элементов)"
                        )
                    return "\n".join(lines) + "\n"

                # 2D
                lines = []
                for i, row in enumerate(data[:max_rows]):
                    if isinstance(row, list):
                        cells = row[:max_cols]
                        row_str = " | ".join(str(c) for c in cells)
                        if len(row) > max_cols:
                            row_str += " | ..."
                    else:
                        row_str = str(row)
                    lines.append(f"{indent}[{i + 1}] {row_str}")
                if len(data) > max_rows:
                    lines.append(f"{indent}... (всего {len(data)} строк)")
                return "\n".join(lines) + "\n"

            # ---- DuckDBTable ----
            if hasattr(obj, 'table_name') and hasattr(obj, 'get_columns'):
                try:
                    cols = obj.get_columns()
                    rows = obj.get_row_count()
                    return (
                        f"{indent}DuckDBTable: {rows} строк × "
                        f"{len(cols)} столбцов\n"
                    )
                except Exception:
                    return f"{indent}DuckDBTable\n"

            # ---- list ----
            if isinstance(obj, list):
                if obj and isinstance(obj[0], list):
                    lines = []
                    for i, row in enumerate(obj[:max_rows]):
                        row_str = " | ".join(
                            str(c) for c in row[:max_cols]
                        )
                        lines.append(f"{indent}[{i + 1}] {row_str}")
                    if len(obj) > max_rows:
                        lines.append(
                            f"{indent}... (всего {len(obj)} строк)"
                        )
                    return "\n".join(lines) + "\n"
                return f"{indent}{obj}\n"

            # ---- скаляр ----
            return f"{indent}{obj}\n"

        except Exception as e:
            return f"{indent}<ошибка форматирования: {e}>\n"


# ============================================================
# ГЛОБАЛЬНЫЙ ЭКЗЕМПЛЯР
# ============================================================
logger = Logger()