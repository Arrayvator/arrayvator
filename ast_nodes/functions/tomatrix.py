# ast_nodes/functions/tomatrix.py
"""
Функции конвертации между Matrix и DuckDB (BigData):

    ToMatrix(m [, limit])                    — DuckDB → Matrix
    Convert_BigData_To_Matrix(m [, limit])   — синоним ToMatrix
    Convert_Matrix_To_BigData(m)             — Matrix → DuckDB
    ToBigData(m)                             — синоним Convert_Matrix_To_BigData
"""

import os
import sys
import atexit
import uuid
from pathlib import Path

from ..base import Node
from runtime.matrix import MatrExMatrix


# ============================================================
# ГЛОБАЛЬНЫЙ СПИСОК TEMP-ФАЙЛОВ
# ============================================================
_TEMP_FILES = set()


def _cleanup_temp_files():
    """Удаляет все зарегистрированные temp-файлы при выходе."""
    for path in list(_TEMP_FILES):
        try:
            if os.path.exists(path):
                os.remove(path)
            _TEMP_FILES.discard(path)
        except Exception:
            pass


atexit.register(_cleanup_temp_files)


def _register_temp_file(path):
    """Регистрирует temp-файл для удаления при выходе."""
    _TEMP_FILES.add(str(path))


# ============================================================
# ОПРЕДЕЛЕНИЕ DUCKDBTABLE
# ============================================================
def _is_duckdb(val):
    try:
        from duckdb_engine import DuckDBTable
        return isinstance(val, DuckDBTable)
    except ImportError:
        return False


# ============================================================
# РАБОЧАЯ ПАПКА
# ============================================================
def _get_work_dir():
    """
    Возвращает папку, куда класть временные файлы.

    Порядок:
        1. Frozen exe → папка с exe.
        2. Python-скрипт → папка запуска (cwd).
        3. Fallback → папка этого файла.
    """
    # 1. Запущено из exe
    if getattr(sys, 'frozen', False):
        try:
            exe_dir = Path(sys.executable).parent
            if exe_dir.exists() and os.access(str(exe_dir), os.W_OK):
                return exe_dir
        except Exception:
            pass

    # 2. Python-скрипт — текущая папка
    try:
        cwd = Path(os.getcwd())
        if cwd.exists() and os.access(str(cwd), os.W_OK):
            return cwd
    except Exception:
        pass

    # 3. Fallback — папка этого файла
    try:
        return Path(__file__).parent
    except Exception:
        return Path(".")


def _make_temp_csv_path():
    """
    Создаёт путь к temp-файлу в подпапке _av_temp рядом с рабочей папкой.
    Возвращает путь к файлу.

    Никогда не падает:
        1. Пытается создать _av_temp рядом с программой.
        2. Если не удалось — системный temp.
        3. Если и это не удалось — текущая папка.
    """
    work_dir = _get_work_dir()
    temp_dir = work_dir / "_av_temp"

    try:
        temp_dir.mkdir(exist_ok=True)
    except Exception:
        # Fallback 1: системный temp
        try:
            import tempfile
            temp_dir = Path(tempfile.gettempdir()) / "_av_temp"
            temp_dir.mkdir(exist_ok=True)
        except Exception:
            # Fallback 2: рабочая папка
            temp_dir = work_dir

    name = f"matrixtobigdata_{uuid.uuid4().hex[:8]}.csv"
    return temp_dir / name


# ============================================================
# TO_MATRIX (DuckDB → Matrix)
# ============================================================
class ToMatrixNode(Node):
    """
    ToMatrix(data [, limit]) — конвертирует DuckDBTable в MatrExMatrix.

    Загружает все данные в RAM.
    ВНИМАНИЕ: для 4 млн строк может занять 2-4 ГБ RAM.
    Используйте limit для загрузки части данных.
    """

    def __init__(self, data, limit=None):
        self.data = data
        self.limit = limit

    def evaluate(self, env):
        # Вычисляем аргумент
        data_obj = self.data.evaluate(env) if hasattr(self.data, 'evaluate') else self.data

        # Опциональный лимит
        limit = None
        if self.limit is not None:
            limit = self.limit.evaluate(env) if hasattr(self.limit, 'evaluate') else self.limit
            if isinstance(limit, (int, float)):
                limit = int(limit)

        # ============================================================
        # DuckDBTable → MatrExMatrix
        # ============================================================
        if _is_duckdb(data_obj):
            try:
                if limit:
                    data = data_obj.get_data_for_show(limit=limit)
                else:
                    data = data_obj.get_data_for_show(limit=10**9)

                if not data or data == [[""]]:
                    return MatrExMatrix([[""]], True)

                headers = data_obj.get_headers()
                if headers and (not data or data[0] != headers):
                    data = [headers] + data

                return MatrExMatrix(data, True)

            except MemoryError:
                rows = data_obj.get_row_count()
                raise MemoryError(
                    f"Недостаточно RAM для загрузки {rows} строк.\n"
                    f"Используйте limit для загрузки части данных:\n"
                    f"    ToMatrix(m, 100000)"
                )
            except Exception as e:
                raise RuntimeError(f"Ошибка конвертации DuckDB → MatrExMatrix: {e}")

        # ============================================================
        # Уже MatrExMatrix → возвращаем как есть
        # ============================================================
        if hasattr(data_obj, 'data') and hasattr(data_obj, 'is_2d'):
            return data_obj

        # ============================================================
        # list → MatrExMatrix
        # ============================================================
        if isinstance(data_obj, list):
            if data_obj and not isinstance(data_obj[0], list):
                return MatrExMatrix(data_obj, False)
            return MatrExMatrix(data_obj, True)

        # ============================================================
        # Скаляр → матрица 1×1
        # ============================================================
        if isinstance(data_obj, (int, float, str, bool)) or data_obj is None:
            return MatrExMatrix([[data_obj]], True)

        raise TypeError(
            f"ToMatrix: не поддерживаемый тип {type(data_obj)}"
        )

    def __repr__(self):
        if self.limit is not None:
            return f"ToMatrix({self.data}, {self.limit})"
        return f"ToMatrix({self.data})"


# ============================================================
# CONVERT_BIGDATA_TO_MATRIX (синоним ToMatrix)
# ============================================================
class ConvertBigDataToMatrixNode(ToMatrixNode):
    """
    Convert_BigData_To_Matrix(data [, limit]) — синоним ToMatrix.

    DuckDB → Matrix.
    """

    def __repr__(self):
        if self.limit is not None:
            return f"Convert_BigData_To_Matrix({self.data}, {self.limit})"
        return f"Convert_BigData_To_Matrix({self.data})"


# ============================================================
# CONVERT_MATRIX_TO_BIGDATA (Matrix → DuckDB)
# ============================================================
class ConvertMatrixToBigDataNode(Node):
    """
    Convert_Matrix_To_BigData(data) — конвертирует MatrExMatrix в DuckDBTable.

    Создаёт временный CSV рядом с программой (в _av_temp/) и открывает
    его через DuckDB. Временный файл удаляется при выходе из программы.

    РАБОТАЕТ ТОЛЬКО С 2D-МАТРИЦАМИ.
    """

    def __init__(self, data):
        self.data = data

    def evaluate(self, env):
        from duckdb_engine import DuckDBTable
        from .csv import save_csv

        # 1. Вычисляем аргумент
        data_obj = self.data.evaluate(env) if hasattr(self.data, 'evaluate') else self.data

        # 2. Уже DuckDB — возвращаем как есть
        if _is_duckdb(data_obj):
            return data_obj

        # 3. Не матрица — ошибка
        if not isinstance(data_obj, MatrExMatrix):
            raise TypeError(
                f"Convert_Matrix_To_BigData: нужна матрица, "
                f"получен {type(data_obj).__name__}.\n"
                f"  Пример: m2 = Convert_Matrix_To_BigData(m)"
            )

        # 4. Вектор — ошибка
        if not data_obj.is_2d:
            raise ValueError(
                "Convert_Matrix_To_BigData: работает только с 2D-матрицами.\n"
                "  Вектор нельзя конвертировать в BigData."
            )

        # 5. Пустая матрица — ошибка
        if data_obj.rows == 0:
            raise ValueError(
                "Convert_Matrix_To_BigData: матрица пуста.\n"
                "  Нечего конвертировать."
            )

        # 6. Создаём temp-файл
        temp_path = _make_temp_csv_path()

        try:
            # 7. Сохраняем CSV
            save_csv(data_obj.data, str(temp_path))

            # 8. Загружаем как DuckDBTable
            duck = DuckDBTable(str(temp_path))

            # 9. Помечаем для удаления
            duck._tmp_path = str(temp_path)
            _register_temp_file(str(temp_path))

            return duck

        except Exception as e:
            # Если что-то упало — удаляем temp-файл сразу
            try:
                if os.path.exists(str(temp_path)):
                    os.remove(str(temp_path))
            except Exception:
                pass
            raise RuntimeError(
                f"Convert_Matrix_To_BigData: ошибка конвертации: {e}"
            )

    def __repr__(self):
        return f"Convert_Matrix_To_BigData({self.data})"


# ============================================================
# TOBIGDATA (синоним Convert_Matrix_To_BigData)
# ============================================================
class ToBigDataNode(ConvertMatrixToBigDataNode):
    """
    ToBigData(data) — синоним Convert_Matrix_To_BigData.

    Matrix → DuckDB.
    """

    def __repr__(self):
        return f"ToBigData({self.data})"