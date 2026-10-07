# runner.py
"""
Интерпретатор ArrayVator.
Находит MAGIC маркер в СВОЁМ exe и выполняет встроенный код.

Работает с PyInstaller (структура _internal/) и с Nuitka.
"""

import sys
import os
import traceback
from pathlib import Path


MAGIC = b"ARRV_PAYLOAD_V1\x00"


# ============================================================
# ЯВНЫЕ ИМПОРТЫ ДЛЯ PYINSTALLER
# ============================================================
# PyInstaller не видит динамические импорты внутри try/except,
# поэтому объявляем их прямо здесь — тогда он точно соберёт
# все нужные пакеты и их бинарники.
try:
    import duckdb
except ImportError:
    pass

try:
    import python_calamine
except ImportError:
    pass

try:
    import pyexcelerate
except ImportError:
    pass

try:
    import openpyxl
except ImportError:
    pass

try:
    import matplotlib
    import matplotlib.backends.backend_tkagg
except ImportError:
    pass

try:
    import plotly
    import plotly.graph_objects
    import plotly.io
except ImportError:
    pass


# ============================================================
# ОПРЕДЕЛЕНИЕ FROZEN
# ============================================================
def _is_frozen():
    """Определяет, запущены ли мы из собранного exe."""
    if getattr(sys, 'frozen', False):
        return True

    exe = sys.executable.lower() if sys.executable else ''
    if exe.endswith('python.exe') or exe.endswith('pythonw.exe'):
        try:
            exe_dir = Path(sys.executable).parent
            if (exe_dir / 'python314.dll').exists() or \
               (exe_dir / 'python313.dll').exists():
                return True
        except Exception:
            pass
        return False

    return True


FROZEN = _is_frozen()
DEBUG = not FROZEN


# ============================================================
# НАСТРОЙКА sys.path ДЛЯ PYINSTALLER
# ============================================================
def _setup_sys_path():
    """
    PyInstaller кладёт всё в _internal/ и подпапку exe.
    Добавляем оба пути в sys.path, чтобы импорты работали.
    """
    paths_to_add = []

    # PyInstaller: _MEIPASS указывает на _internal/
    if hasattr(sys, '_MEIPASS'):
        paths_to_add.append(sys._MEIPASS)

    # Папка рядом с exe
    if len(sys.argv) > 0:
        try:
            exe_dir = os.path.dirname(os.path.abspath(sys.argv[0]))
            paths_to_add.append(exe_dir)
            # PyInstaller onedir: _internal рядом с exe
            internal = os.path.join(exe_dir, '_internal')
            if os.path.isdir(internal):
                paths_to_add.append(internal)
        except Exception:
            pass

    # Папка самого runner.py (dev-режим)
    try:
        runner_dir = os.path.dirname(os.path.abspath(__file__))
        paths_to_add.append(runner_dir)
    except Exception:
        pass

    for p in paths_to_add:
        if p and os.path.isdir(p) and p not in sys.path:
            sys.path.insert(0, p)


_setup_sys_path()


# ============================================================
# ПОИСК PAYLOAD
# ============================================================
def _find_payload_exe():
    """Возвращает список кандидатов — путей к exe, где может быть payload."""
    candidates = []

    # 1. sys.argv[0] — реальное имя запущенного exe
    if len(sys.argv) > 0:
        try:
            argv_exe = Path(sys.argv[0]).resolve()
            if argv_exe.exists() and argv_exe.suffix.lower() == '.exe':
                candidates.append(argv_exe)
        except Exception:
            pass

    # 2. sys.executable
    try:
        exe_path = Path(sys.executable).resolve()
        if exe_path.exists() and exe_path not in candidates:
            if exe_path.suffix.lower() == '.exe':
                candidates.append(exe_path)
    except Exception:
        pass

    # 3. Любой .exe в папке рядом
    try:
        if len(sys.argv) > 0:
            exe_dir = Path(sys.argv[0]).resolve().parent
        else:
            exe_dir = Path(sys.executable).resolve().parent

        if exe_dir.exists():
            for exe in exe_dir.glob("*.exe"):
                if exe.name.lower() in ('python.exe', 'pythonw.exe'):
                    continue
                if exe not in candidates:
                    candidates.append(exe)
    except Exception:
        pass

    # 4. Fallback для dev-режима
    if not candidates:
        candidates.append(Path(__file__).parent / "runner.exe")

    return candidates


def _extract_payload_from_exe(exe_path):
    """Извлекает код из конкретного EXE файла."""
    try:
        with open(exe_path, "rb") as f:
            data = f.read()
    except Exception as e:
        if DEBUG:
            print(f"  ⚠️  Не удалось прочитать {exe_path.name}: {e}")
        return None

    idx = data.rfind(MAGIC)
    if idx == -1:
        return None

    header_start = idx + len(MAGIC)
    if header_start + 8 > len(data):
        return None

    length = int.from_bytes(data[header_start:header_start + 8], "little")
    payload_start = header_start + 8
    payload_end = payload_start + length

    if payload_end > len(data):
        return None

    return data[payload_start:payload_end].decode("utf-8", errors="replace")


def _extract_payload():
    """Ищет встроенный код в своём exe."""
    if DEBUG:
        print(f"🔍 Поиск MAGIC маркера...")

    candidates = _find_payload_exe()

    if DEBUG:
        print(f"  Кандидатов: {len(candidates)}")
        for c in candidates:
            size = c.stat().st_size if c.exists() else 0
            print(f"  📄 {c.name} ({size} байт)")

    for exe_path in candidates:
        payload = _extract_payload_from_exe(exe_path)
        if payload is not None:
            if DEBUG:
                print(f"  ✅ Код найден в {exe_path.name} ({len(payload)} символов)")
            return payload

    if DEBUG:
        print("  ❌ MAGIC маркер не найден")
    return None


# ============================================================
# ЗАПУСК КОДА ARRAYVATOR
# ============================================================
def run_source(source_code):
    """Выполняет код ArrayVator."""
    if DEBUG:
        print(f"📄 Код: {len(source_code)} символов")
        print("=" * 60)
        print("ИСХОДНЫЙ КОД:")
        print("-" * 60)
        print(source_code[:500])
        if len(source_code) > 500:
            print(f"... (ещё {len(source_code) - 500} символов)")
        print("-" * 60)
        print()

    try:
        # ============================================================
        # 1. Сначала импортируем parser — он тянет ast_nodes.
        #    Это ОБЯЗАТЕЛЬНО до apply_logging_hooks().
        # ============================================================
        from lexer import Lexer
        from parser import Parser

        # ============================================================
        # 2. ТОЛЬКО ТЕПЕРЬ применяем логирование —
        #    ast_nodes уже загружен, все классы Node зарегистрированы.
        # ============================================================
        from runtime.logging_hook import apply_logging_hooks
        apply_logging_hooks()

        if DEBUG:
            print("✅ Модули загружены, логирование применено")

    except ImportError as e:
        print(f"❌ Ошибка импорта: {e}")
        if DEBUG:
            print(f"sys.path: {sys.path[:5]}")
        raise

    lexer = Lexer(source_code)
    tokens = lexer.tokenize()
    if DEBUG:
        print(f"✅ Токенизация: {len(tokens)} токенов")

    parser = Parser(tokens, source=source_code)
    parser.parse_program()

    if DEBUG:
        print("✅ Программа выполнена")


# ============================================================
# ГЛАВНАЯ ФУНКЦИЯ
# ============================================================
def main():
    if DEBUG:
        print("=" * 60)
        print("ArrayVator Runner (debug)")
        print("=" * 60)
        print(f"📂 sys.executable: {sys.executable}")
        print(f"📂 sys.argv: {sys.argv}")
        print(f"📂 sys.frozen: {getattr(sys, 'frozen', False)}")
        print(f"📂 FROZEN (определено вручную): {FROZEN}")
        print()

    # ============================================================
    # РЕЖИМ 1: код встроен в EXE
    # ============================================================
    embedded = _extract_payload()
    if embedded is not None:
        try:
            run_source(embedded)
            return 0
        except Exception as e:
            print()
            print("=" * 60)
            print("❌ ОШИБКА ВЫПОЛНЕНИЯ:")
            print("=" * 60)
            print(str(e))
            if DEBUG:
                traceback.print_exc()
            return 1

    # ============================================================
    # РЕЖИМ 2: передан .arrv файл в аргументах
    # (работает и в frozen, и в dev)
    # ============================================================
    if len(sys.argv) >= 2:
        arrv_path = sys.argv[1]
        if not os.path.exists(arrv_path):
            print(f"❌ Файл не найден: {arrv_path}")
            return 1

        try:
            with open(arrv_path, "r", encoding="utf-8") as f:
                source_code = f.read()
            if DEBUG:
                print(f"📄 Файл: {arrv_path}")
            run_source(source_code)
            return 0
        except Exception as e:
            print()
            print("=" * 60)
            print("❌ ОШИБКА ВЫПОЛНЕНИЯ:")
            print("=" * 60)
            print(str(e))
            if DEBUG:
                traceback.print_exc()
            return 1

    # ============================================================
    # РЕЖИМ 3: ничего не передано
    # ============================================================
    if FROZEN:
        print()
        print("=" * 60)
        print("⚠️  В этом exe нет встроенного кода ArrayVator.")
        print("=" * 60)
        print("   Возможно, файл повреждён или собран неправильно.")
        print()
        print("   Используйте ArrayVator Compiler для сборки программ.")
        return 1

    print("Это runner ArrayVator.")
    print()
    print("Использование:")
    print("  runner.exe                 — выполнить встроенный код")
    print("  runner.exe script.arrv     — выполнить файл")
    return 1


if __name__ == "__main__":
    try:
        code = main()
    except Exception as e:
        print()
        print("=" * 60)
        print("❌ НЕОЖИДАННАЯ ОШИБКА:")
        print("=" * 60)
        print(str(e))
        traceback.print_exc()
        code = 1

    # Пауза только в frozen-режиме
    if FROZEN:
        print()
        print("=" * 60)
        input("Нажмите Enter для выхода...")
    sys.exit(code)