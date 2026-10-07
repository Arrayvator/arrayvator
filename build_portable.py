# build_portable.py
"""
Портативная сборка ArrayVator с тремя вариантами runner.

Варианты:
    runner/          — FULL (всё: duckdb, matplotlib, plotly, excel)
    runner_data/     — DATA (duckdb, excel, без графики)
    runner_minimal/  — MINIMAL (только ядро)

Компилятор сам выбирает нужный вариант по коду .arrv.

Структура:
    ArrayVator_Portable/
    ├── ArrayVator.exe
    ├── app.ico               ← внешняя иконка
    ├── _internal/
    │   ├── app.ico           ← вшитая иконка
    │   ├── help/             ← вшитая справка (fallback)
    │   └── syntax/           ← база справки (collect-all)
    ├── help/                 ← внешняя справка (приоритет!)
    ├── runner/               ← полный (С КОНСОЛЬЮ)
    ├── runner_data/          ← данные (С КОНСОЛЬЮ)
    ├── runner_minimal/       ← минимальный (С КОНСОЛЬЮ)
    └── compiler/             ← БЕЗ КОНСОЛИ (GUI)

Запуск:
    python build_portable.py
"""

import os
import sys
import site
import shutil
import subprocess
import time
from pathlib import Path

PROJECT_DIR = Path(__file__).parent.resolve()
PORTABLE_DIR = PROJECT_DIR / "ArrayVator_Portable"
DIST_DIR = PROJECT_DIR / "dist"
BUILD_DIR = PROJECT_DIR / "build"
HELP_SRC_DIR = PROJECT_DIR / "help"
ICON_PATH = PROJECT_DIR / "app.ico"


# ============================================================
# ПОИСК UPX
# ============================================================
def _find_upx():
    """Ищет upx.exe в типичных местах."""
    candidates = [
        PROJECT_DIR,
        Path(r"C:\upx"),
        Path.home() / "upx",
        Path(r"C:\Program Files\upx"),
        Path(r"C:\Program Files (x86)\upx"),
    ]
    for upx_path in candidates:
        try:
            if (upx_path / "upx.exe").exists():
                return str(upx_path)
        except Exception:
            continue
    return None


UPX_DIR = _find_upx()


# ============================================================
# ОБЩИЕ ИСКЛЮЧЕНИЯ
# ============================================================
EXCLUDES = [
    '--exclude-module', 'test',
    '--exclude-module', 'tests',
    '--exclude-module', 'unittest',
    '--exclude-module', 'pytest',
    '--exclude-module', 'distutils',
    '--exclude-module', 'setuptools',
    '--exclude-module', 'pip',
    '--exclude-module', 'wheel',
    '--exclude-module', 'pydoc',
    '--exclude-module', 'doctest',
    '--exclude-module', 'pdb',
    '--exclude-module', 'lib2to3',
    '--exclude-module', 'tkinter.test',
    '--exclude-module', 'scipy',
    '--exclude-module', 'pandas',
    '--exclude-module', 'sklearn',
    '--exclude-module', 'IPython',
    '--exclude-module', 'jupyter',
    '--exclude-module', 'notebook',
    '--exclude-module', 'PyQt5',
    '--exclude-module', 'PyQt6',
    '--exclude-module', 'PySide2',
    '--exclude-module', 'PySide6',
    '--exclude-module', 'wx',
    '--exclude-module', 'sqlalchemy',
    '--exclude-module', 'lxml',
    '--exclude-module', 'bs4',
    '--exclude-module', 'pyarrow',
    '--exclude-module', 'playwright',
]


# ============================================================
# UPX ФЛАГИ
# ============================================================
def _build_upx_flags():
    """UPX флаги: не сжимаем exe, pyd, dll."""
    if not UPX_DIR:
        return []

    return [
        '--upx-dir', UPX_DIR,
        '--upx-exclude', '*.exe',
        '--upx-exclude', '*.pyd',
        '--upx-exclude', '*.dll',
        '--upx-exclude', 'vcruntime140.dll',
        '--upx-exclude', 'vcruntime140_1.dll',
        '--upx-exclude', 'msvcp140.dll',
        '--upx-exclude', 'ucrtbase.dll',
        '--upx-exclude', 'python3.dll',
        '--upx-exclude', 'python314.dll',
        '--upx-exclude', 'python313.dll',
        '--upx-exclude', 'python312.dll',
        '--upx-exclude', 'python311.dll',
        '--upx-exclude', 'python310.dll',
    ]


UPX_FLAGS = _build_upx_flags()


# ============================================================
# HELP-ФАЙЛЫ — ВШИВАНИЕ В _internal/help/
# ============================================================
def _build_help_add_data():
    """
    Возвращает флаг --add-data для вшивания help/ в _internal/help/.

    Если папки help/ нет — возвращает [].

    Формат:  --add-data  <src><os.pathsep>help
    На Windows os.pathsep = ';', на Linux/macOS = ':'.
    PyInstaller положит содержимое <src> в подпапку 'help/' внутри сборки.
    """
    if not HELP_SRC_DIR.exists():
        return []
    return [
        '--add-data',
        f'{HELP_SRC_DIR}{os.pathsep}help',
    ]


HELP_ADD_DATA = _build_help_add_data()


# ============================================================
# ИКОНКА — ВШИВАНИЕ В _internal/app.ico
# ============================================================
def _build_icon_flags():
    """
    Возвращает список флагов PyInstaller для иконки.

    --icon    — вшивает иконку в EXE (отображается в проводнике)
    --add-data — кладёт app.ico в _internal/ (доступна во время работы)

    Если app.ico нет — возвращает [].
    """
    if not ICON_PATH.exists():
        return []
    return [
        '--icon', str(ICON_PATH),
        '--add-data', f'{ICON_PATH}{os.pathsep}.',
    ]


ICON_FLAGS = _build_icon_flags()


# ============================================================
# НАШИ МОДУЛИ (общие для всех runner'ов)
#
# ВАЖНО ПРО SYNTAX:
#   Пакет syntax/ содержит подпакеты (autocomplete/, signatures_data/)
#   и ~25 модулей. Точечные --hidden-import syntax.xxx не подтягивают
#   подпакеты, из-за чего панель справки в сборке ломается.
#   Поэтому используем --collect-all syntax — PyInstaller собирает
#   ВСЁ, что лежит внутри syntax/, включая подпакеты.
# ============================================================
PROJECT_MODULES = [
    '--hidden-import', 'lexer',
    '--hidden-import', 'parser',
    '--hidden-import', 'ast_nodes',
    '--hidden-import', 'runtime',
    '--hidden-import', 'errors',
    '--hidden-import', 'errors.db_ru',
    '--hidden-import', 'errors.db_en',
    '--collect-all', 'syntax',
    '--hidden-import', 'operators',
    '--hidden-import', 'environment',
    '--hidden-import', 'duckdb_engine',
    '--hidden-import', 'locales',
]


# ============================================================
# RUNNER: FULL — всё внутри, С КОНСОЛЬЮ
# ============================================================
RUNNER_FULL_FLAGS = [
    '--onedir',
    '--noconfirm',
    '--clean',
    # ВАЖНО: БЕЗ --noconsole — runner должен показывать print()

    # Иконка: --icon + --add-data
    *ICON_FLAGS,

    # Help-файлы внутрь _internal/help/
    *HELP_ADD_DATA,

    # DuckDB
    '--collect-all', 'duckdb',
    '--collect-binaries', 'duckdb',
    '--hidden-import', 'duckdb',
    '--hidden-import', '_duckdb',

    # Excel
    '--collect-all', 'python_calamine',
    '--collect-all', 'pyexcelerate',
    '--collect-all', 'openpyxl',

    # matplotlib
    '--hidden-import', 'matplotlib.backends.backend_tkagg',
    '--hidden-import', 'matplotlib.figure',
    '--hidden-import', 'matplotlib.pyplot',
    '--exclude-module', 'matplotlib.backends.backend_qt5',
    '--exclude-module', 'matplotlib.backends.backend_qt5agg',
    '--exclude-module', 'matplotlib.backends.backend_qt6',
    '--exclude-module', 'matplotlib.backends.backend_qt6agg',
    '--exclude-module', 'matplotlib.backends.backend_gtk3',
    '--exclude-module', 'matplotlib.backends.backend_gtk3agg',
    '--exclude-module', 'matplotlib.backends.backend_gtk4',
    '--exclude-module', 'matplotlib.backends.backend_gtk4agg',
    '--exclude-module', 'matplotlib.backends.backend_wx',
    '--exclude-module', 'matplotlib.backends.backend_wxagg',
    '--exclude-module', 'matplotlib.backends.backend_webagg',
    '--exclude-module', 'matplotlib.backends.backend_nbagg',
    '--exclude-module', 'matplotlib.backends.backend_pdf',
    '--exclude-module', 'matplotlib.backends.backend_ps',
    '--exclude-module', 'matplotlib.backends.backend_svg',
    '--exclude-module', 'matplotlib.tests',
    '--exclude-module', 'matplotlib.testing',
    '--exclude-module', 'matplotlib.sphinxext',

    # plotly
    '--hidden-import', 'plotly.graph_objects',
    '--hidden-import', 'plotly.io',
    '--hidden-import', 'plotly.subplots',
    '--exclude-module', 'plotly.express',
    '--exclude-module', 'plotly.tests',
    '--exclude-module', 'plotly.validators',
    '--exclude-module', 'plotly.data',
    '--exclude-module', 'plotly.dashboard_objs',

    # PIL
    '--exclude-module', 'PIL.ImageQt',
    '--exclude-module', 'PIL.ImageShow',

    # Наши модули (включая --collect-all syntax)
    *PROJECT_MODULES,

    *EXCLUDES,
    *UPX_FLAGS,
]


# ============================================================
# RUNNER: DATA — duckdb + excel, БЕЗ графики, С КОНСОЛЬЮ
# ============================================================
RUNNER_DATA_FLAGS = [
    '--onedir',
    '--noconfirm',
    '--clean',
    # ВАЖНО: БЕЗ --noconsole — runner должен показывать print()

    # Иконка: --icon + --add-data
    *ICON_FLAGS,

    # Help-файлы внутрь _internal/help/
    *HELP_ADD_DATA,

    # DuckDB
    '--collect-all', 'duckdb',
    '--collect-binaries', 'duckdb',
    '--hidden-import', 'duckdb',
    '--hidden-import', '_duckdb',

    # Excel
    '--collect-all', 'python_calamine',
    '--collect-all', 'pyexcelerate',
    '--collect-all', 'openpyxl',

    # Графика — ИСКЛЮЧЕНА
    '--exclude-module', 'matplotlib',
    '--exclude-module', 'numpy',
    '--exclude-module', 'PIL',
    '--exclude-module', 'plotly',

    # Наши модули
    *PROJECT_MODULES,

    *EXCLUDES,
    *UPX_FLAGS,
]


# ============================================================
# RUNNER: MINIMAL — только ядро, С КОНСОЛЬЮ
# ============================================================
RUNNER_MINIMAL_FLAGS = [
    '--onedir',
    '--noconfirm',
    '--clean',
    # ВАЖНО: БЕЗ --noconsole — runner должен показывать print()

    # Иконка: --icon + --add-data
    *ICON_FLAGS,

    # Help-файлы внутрь _internal/help/
    *HELP_ADD_DATA,

    # Исключаем всё тяжёлое
    '--exclude-module', 'duckdb',
    '--exclude-module', 'python_calamine',
    '--exclude-module', 'pyexcelerate',
    '--exclude-module', 'openpyxl',
    '--exclude-module', 'matplotlib',
    '--exclude-module', 'numpy',
    '--exclude-module', 'PIL',
    '--exclude-module', 'plotly',

    # Наши модули (кроме duckdb_engine — он потянет duckdb)
    '--hidden-import', 'lexer',
    '--hidden-import', 'parser',
    '--hidden-import', 'ast_nodes',
    '--hidden-import', 'runtime',
    '--hidden-import', 'errors',
    '--hidden-import', 'errors.db_ru',
    '--hidden-import', 'errors.db_en',
    '--collect-all', 'syntax',
    '--hidden-import', 'operators',
    '--hidden-import', 'environment',
    '--hidden-import', 'locales',
    # duckdb_engine НЕ включаем — он не нужен без BigData

    *EXCLUDES,
    *UPX_FLAGS,
]


# ============================================================
# COMPILER — GUI, БЕЗ КОНСОЛИ
# ============================================================
COMPILER_FLAGS = [
    '--onedir',
    '--noconfirm',
    '--clean',
    '--noconsole',        # ← БЕЗ ЧЁРНОГО ОКНА
    '--windowed',         # ← синоним для Windows

    # Иконка: --icon + --add-data
    *ICON_FLAGS,

    '--exclude-module', 'duckdb',
    '--exclude-module', 'python_calamine',
    '--exclude-module', 'pyexcelerate',
    '--exclude-module', 'openpyxl',
    '--exclude-module', 'matplotlib',
    '--exclude-module', 'plotly',
    '--exclude-module', 'numpy',
    '--exclude-module', 'PIL',
    '--exclude-module', 'requests',
    '--exclude-module', 'urllib3',
    '--exclude-module', 'certifi',
    *EXCLUDES,
    *UPX_FLAGS,
]


# ============================================================
# ARRAYVATOR (редактор) — GUI, БЕЗ КОНСОЛИ
# ============================================================
ARRAYVATOR_FLAGS = [
    '--onedir',
    '--noconfirm',
    '--clean',
    '--noconsole',        # ← БЕЗ ЧЁРНОГО ОКНА
    '--windowed',         # ← синоним для Windows

    # Иконка: --icon + --add-data
    *ICON_FLAGS,

    # Help-файлы внутрь _internal/help/
    *HELP_ADD_DATA,

    # DuckDB
    '--collect-all', 'duckdb',
    '--collect-binaries', 'duckdb',
    '--hidden-import', 'duckdb',
    '--hidden-import', '_duckdb',

    # Excel
    '--collect-all', 'python_calamine',
    '--collect-all', 'pyexcelerate',
    '--collect-all', 'openpyxl',

    # matplotlib
    '--hidden-import', 'matplotlib.backends.backend_tkagg',
    '--hidden-import', 'matplotlib.figure',
    '--hidden-import', 'matplotlib.pyplot',

    # plotly
    '--hidden-import', 'plotly.graph_objects',
    '--hidden-import', 'plotly.io',

    # Наши модули (включая --collect-all syntax)
    *PROJECT_MODULES,

    *EXCLUDES,
    *UPX_FLAGS,
]


# ============================================================
# ПОИСК PYTHON
# ============================================================
def find_python():
    if sys.executable and os.path.exists(sys.executable):
        if 'python' in os.path.basename(sys.executable).lower():
            return sys.executable

    for name in ('python', 'python3', 'py'):
        path = shutil.which(name)
        if path and os.path.exists(path):
            return path

    return None


def check_pyinstaller(python):
    try:
        result = subprocess.run(
            [python, '-m', 'PyInstaller', '--version'],
            capture_output=True, text=True, timeout=60,
            encoding='utf-8', errors='replace',
        )
        if result.returncode == 0:
            return True, result.stdout.strip().split('\n')[0]
        return False, (result.stderr.strip() or result.stdout.strip())
    except Exception as e:
        return False, str(e)


def check_libraries():
    print()
    print("Проверка библиотек:")
    required = [
        ('duckdb', 'duckdb'),
        ('python_calamine', 'python-calamine'),
        ('pyexcelerate', 'pyexcelerate'),
        ('openpyxl', 'openpyxl'),
        ('matplotlib', 'matplotlib'),
        ('plotly', 'plotly'),
    ]
    missing = []
    for import_name, pip_name in required:
        try:
            __import__(import_name)
            print(f"   ✅ {pip_name}")
        except ImportError:
            print(f"   ❌ {pip_name} — не установлен")
            missing.append(pip_name)
    return missing


def check_help_dir():
    """
    Проверяет наличие папки help/ и базовых файлов.

    Возвращает True, если папка есть и в ней есть хотя бы Help.txt.
    """
    print()
    print("Проверка папки help/:")
    if not HELP_SRC_DIR.exists():
        print(f"   ❌ Папка не найдена: {HELP_SRC_DIR}")
        print(f"      Справка в сборке работать НЕ будет.")
        return False

    required_files = [
        'Help.txt', 'Help_EN.txt',
        'short_help_rus.txt', 'short_help_en.txt',
        'about.txt', 'about_EN.txt',
        'license.txt', 'license_EN.txt',
    ]

    found = 0
    for name in required_files:
        path = HELP_SRC_DIR / name
        if path.exists():
            size_kb = path.stat().st_size / 1024
            print(f"   ✅ {name:24s} {size_kb:7.1f} KB")
            found += 1
        else:
            print(f"   ⚠️  {name:24s} отсутствует")

    print(f"   Итого: {found}/{len(required_files)} файлов")

    if not (HELP_SRC_DIR / "Help.txt").exists():
        print(f"   ⚠️  Help.txt не найден — русская справка не откроется!")

    return found > 0


def check_icon():
    """
    Проверяет наличие app.ico.

    Возвращает True, если файл есть.
    """
    print()
    print("Проверка иконки:")
    if not ICON_PATH.exists():
        print(f"   ⚠️  Иконка не найдена: {ICON_PATH}")
        print(f"      Сборка будет с иконкой PyInstaller по умолчанию.")
        print(f"      Положите app.ico в корень проекта.")
        return False

    size_kb = ICON_PATH.stat().st_size / 1024
    print(f"   ✅ app.ico ({size_kb:.1f} KB)")
    return True


def check_syntax_package():
    """
    Проверяет наличие пакета syntax/ — от него зависит панель справки.

    Возвращает True, если пакет есть.
    """
    print()
    print("Проверка пакета syntax/:")

    syntax_dir = PROJECT_DIR / "syntax"
    if not syntax_dir.exists():
        print(f"   ❌ Папка не найдена: {syntax_dir}")
        print(f"      Панель справки в сборке работать НЕ будет.")
        return False

    autocomplete_data = syntax_dir / "autocomplete_data.py"
    if not autocomplete_data.exists():
        print(f"   ❌ Не найден: syntax/autocomplete_data.py")
        return False

    ok(f"autocomplete_data.py ({autocomplete_data.stat().st_size / 1024:.1f} KB)")

    # Подпакеты
    for sub in ("autocomplete", "signatures_data"):
        sub_dir = syntax_dir / sub
        if sub_dir.exists():
            n_py = sum(1 for _ in sub_dir.glob("*.py"))
            print(f"   ✅ syntax/{sub}/ ({n_py} .py файлов)")
        else:
            print(f"   ⚠️  syntax/{sub}/ не найден")

    return True


def ok(msg):
    print(f"   ✅ {msg}")


# ============================================================
# КОПИРОВАНИЕ КРИТИЧНЫХ БИНАРНИКОВ
# ============================================================
def _find_in_site_packages(pattern):
    site_dirs = []

    try:
        site_dirs.extend(site.getsitepackages())
    except Exception:
        pass

    try:
        py_dir = Path(sys.executable).parent
        site_dirs.append(str(py_dir / "Lib" / "site-packages"))
        site_dirs.append(str(py_dir.parent / "Lib" / "site-packages"))
    except Exception:
        pass

    try:
        user_site = site.getusersitepackages()
        if user_site:
            site_dirs.append(user_site)
    except Exception:
        pass

    site_dirs = list(dict.fromkeys(site_dirs))

    for sd in site_dirs:
        sd_path = Path(sd)
        if not sd_path.exists():
            continue
        matches = list(sd_path.glob(pattern))
        if matches:
            return matches[0]
    return None


def copy_extra_binaries(name, result_dir):
    """Копирует _duckdb*.pyd для runner'ов и arrayvator."""
    if name not in ('runner', 'runner_data', 'runner_minimal', 'arrayvator'):
        return

    # Для minimal — не нужно
    if name == 'runner_minimal':
        return

    print()
    print("   Поиск дополнительных бинарников...")

    internal_dir = result_dir / "_internal"
    internal_dir.mkdir(exist_ok=True)

    extras = [
        ("_duckdb*.pyd", internal_dir),
        ("duckdb*.pyd", internal_dir),
    ]

    copied = 0
    for pattern, dst_dir in extras:
        found = _find_in_site_packages(pattern)
        if found:
            dst = dst_dir / found.name
            if not dst.exists():
                try:
                    shutil.copy2(found, dst)
                    size_mb = found.stat().st_size / (1024 * 1024)
                    print(f"   📎 {found.name} ({size_mb:.1f} MB)")
                    copied += 1
                except Exception as e:
                    print(f"   ⚠️  Не удалось скопировать {found.name}: {e}")
            else:
                print(f"   ℹ️  {found.name} уже есть")

    if copied == 0:
        print(f"   ℹ️  Дополнительных бинарников не найдено")


# ============================================================
# СБОРКА ОДНОГО КОМПОНЕНТА
# ============================================================
def build_one(name, script, python, flags):
    print()
    print("=" * 60)
    print(f"СБОРКА: {name}")
    print("=" * 60)
    t0 = time.time()

    script_path = PROJECT_DIR / script
    if not script_path.exists():
        print(f"❌ Файл не найден: {script_path}")
        return False

    cmd = [
        python, '-m', 'PyInstaller',
        '--name', name,
        *flags,
        '--distpath', str(DIST_DIR),
        '--workpath', str(BUILD_DIR / name),
        '--specpath', str(BUILD_DIR),
        str(script_path),
    ]

    short = ' '.join(cmd[:6]) + ' ... ' + cmd[-1].split(os.sep)[-1]
    print(f"Команда: {short}")
    print()

    try:
        process = subprocess.Popen(
            cmd,
            cwd=str(PROJECT_DIR),
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            encoding='utf-8',
            errors='replace',
            bufsize=1,
        )

        for line in process.stdout:
            stripped = line.strip()
            if not stripped:
                continue
            if stripped.startswith('INFO:'):
                continue
            if stripped.startswith('WARNING:'):
                if 'lib not found' in stripped.lower():
                    print(line, end='')
                continue
            print(line, end='')

        process.wait()

        if process.returncode != 0:
            print(f"❌ {name}: код {process.returncode}")
            return False

    except Exception as e:
        print(f"❌ {name}: {e}")
        return False

    result_dir = DIST_DIR / name
    if not result_dir.exists():
        print(f"❌ Папка {result_dir} не создана")
        return False

    copy_extra_binaries(name, result_dir)

    size_mb = _dir_size_mb(result_dir)
    elapsed = time.time() - t0
    print()
    print(f"✅ {name}: {size_mb:.1f} MB ({elapsed:.0f} сек)")
    return True


def _dir_size_mb(path):
    total = 0
    for f in path.rglob('*'):
        if f.is_file():
            try:
                total += f.stat().st_size
            except Exception:
                pass
    return total / (1024 * 1024)


# ============================================================
# КОПИРОВАНИЕ ПАПКИ help/ В ПОРТАТИВНУЮ СБОРКУ
# ============================================================
def copy_help_to_portable():
    """
    Копирует help/ в ArrayVator_Portable/help/.

    Возвращает True при успехе.
    """
    print("\n1b. Help-файлы → help/")

    if not HELP_SRC_DIR.exists():
        print(f"   ⚠️  Папка help/ не найдена: {HELP_SRC_DIR}")
        print(f"      Справка будет только вшитая (_internal/help/),")
        print(f"      либо её не будет вообще.")
        return False

    help_dst = PORTABLE_DIR / "help"

    try:
        shutil.copytree(HELP_SRC_DIR, help_dst)

        txt_count = sum(1 for _ in help_dst.rglob("*.txt"))
        size_kb = _dir_size_kb(help_dst)
        print(f"   ✅ help/  ({txt_count} .txt файлов, {size_kb:.1f} KB)")

        # Проверим наличие Help.txt
        if (help_dst / "Help.txt").exists():
            print(f"      ✅ Help.txt на месте")
        else:
            print(f"      ⚠️  Help.txt ОТСУТСТВУЕТ — русская справка не откроется!")

        return True
    except Exception as e:
        print(f"   ❌ Не удалось скопировать help/: {e}")
        return False


def copy_icon_to_portable():
    """
    Копирует app.ico в ArrayVator_Portable/app.ico.

    Нужно для работы root.iconbitmap() во время выполнения.
    Возвращает True при успехе.
    """
    print("\n1c. Иконка → app.ico")

    if not ICON_PATH.exists():
        print(f"   ⚠️  Иконка не найдена: {ICON_PATH}")
        print(f"      Окно редактора будет с иконкой Tk по умолчанию.")
        return False

    try:
        shutil.copy2(ICON_PATH, PORTABLE_DIR / "app.ico")
        size_kb = ICON_PATH.stat().st_size / 1024
        print(f"   ✅ app.ico ({size_kb:.1f} KB)")
        return True
    except Exception as e:
        print(f"   ❌ Не удалось скопировать app.ico: {e}")
        return False


def _dir_size_kb(path):
    total = 0
    for f in path.rglob('*'):
        if f.is_file():
            try:
                total += f.stat().st_size
            except Exception:
                pass
    return total / 1024


# ============================================================
# СБОРКА ПОРТАТИВНОЙ ПАПКИ
# ============================================================
def assemble_portable():
    print()
    print("=" * 60)
    print("СБОРКА ПОРТАТИВНОЙ ПАПКИ")
    print("=" * 60)

    if PORTABLE_DIR.exists():
        print(f"Удаление старой: {PORTABLE_DIR.name}/")
        try:
            shutil.rmtree(PORTABLE_DIR)
        except Exception as e:
            print(f"⚠️  Не удалось удалить: {e}")

    PORTABLE_DIR.mkdir(parents=True)

    # 1. Editor
    print("\n1. Editor → ArrayVator.exe")
    src = DIST_DIR / "arrayvator"
    if not src.exists():
        print(f"   ❌ Не найдено: {src}")
        return False

    for item in src.iterdir():
        dst = PORTABLE_DIR / item.name
        if item.is_dir():
            shutil.copytree(item, dst)
        else:
            shutil.copy2(item, dst)

    old_exe = PORTABLE_DIR / "arrayvator.exe"
    new_exe = PORTABLE_DIR / "ArrayVator.exe"
    if old_exe.exists():
        old_exe.rename(new_exe)
        print("   ✅ ArrayVator.exe")

    # 1b. Help-файлы (внешняя копия — приоритет при поиске)
    copy_help_to_portable()

    # 1c. Иконка (внешняя копия — для iconbitmap во время работы)
    copy_icon_to_portable()

    # 2. Runner FULL
    print("\n2. Runner FULL → runner/")
    src = DIST_DIR / "runner"
    if not src.exists():
        print(f"   ❌ Не найдено: {src}")
        return False
    shutil.copytree(src, PORTABLE_DIR / "runner")
    print("   ✅ runner/runner.exe (FULL)")

    # 3. Runner DATA
    print("\n3. Runner DATA → runner_data/")
    src = DIST_DIR / "runner_data"
    if not src.exists():
        print(f"   ❌ Не найдено: {src}")
        return False
    shutil.copytree(src, PORTABLE_DIR / "runner_data")
    print("   ✅ runner_data/runner_data.exe (DATA)")

    # 4. Runner MINIMAL
    print("\n4. Runner MINIMAL → runner_minimal/")
    src = DIST_DIR / "runner_minimal"
    if not src.exists():
        print(f"   ❌ Не найдено: {src}")
        return False
    shutil.copytree(src, PORTABLE_DIR / "runner_minimal")
    print("   ✅ runner_minimal/runner_minimal.exe (MINIMAL)")

    # 5. Compiler
    print("\n5. Compiler → compiler/")
    src = DIST_DIR / "compiler"
    if not src.exists():
        print(f"   ❌ Не найдено: {src}")
        return False
    shutil.copytree(src, PORTABLE_DIR / "compiler")
    print("   ✅ compiler/compiler.exe")

    # Проверка структуры
    print("\nПроверка структуры:")
    checks = [
        (PORTABLE_DIR / "ArrayVator.exe",                             "ArrayVator.exe"),
        (PORTABLE_DIR / "app.ico",                                    "app.ico (внешняя иконка)"),
        (PORTABLE_DIR / "_internal",                                  "_internal/"),
        (PORTABLE_DIR / "_internal" / "app.ico",                      "_internal/app.ico (вшитая)"),
        (PORTABLE_DIR / "_internal" / "help" / "Help.txt",            "_internal/help/Help.txt (вшитая)"),
        (PORTABLE_DIR / "_internal" / "syntax" / "autocomplete_data.pyc",
                                                                      "_internal/syntax/autocomplete_data.pyc"),
        (PORTABLE_DIR / "_internal" / "syntax" / "autocomplete",
                                                                      "_internal/syntax/autocomplete/ (подпакет)"),
        (PORTABLE_DIR / "_internal" / "syntax" / "signatures_data",
                                                                      "_internal/syntax/signatures_data/ (подпакет)"),
        (PORTABLE_DIR / "help" / "Help.txt",                          "help/Help.txt (внешняя)"),
        (PORTABLE_DIR / "help" / "Help_EN.txt",                       "help/Help_EN.txt"),
        (PORTABLE_DIR / "help" / "short_help_rus.txt",                "help/short_help_rus.txt"),
        (PORTABLE_DIR / "help" / "short_help_en.txt",                 "help/short_help_en.txt"),
        (PORTABLE_DIR / "help" / "about.txt",                         "help/about.txt"),
        (PORTABLE_DIR / "help" / "about_EN.txt",                      "help/about_EN.txt"),
        (PORTABLE_DIR / "help" / "license.txt",                       "help/license.txt"),
        (PORTABLE_DIR / "help" / "license_EN.txt",                    "help/license_EN.txt"),
        (PORTABLE_DIR / "runner" / "runner.exe",                      "runner/runner.exe"),
        (PORTABLE_DIR / "runner_data" / "runner_data.exe",            "runner_data/runner_data.exe"),
        (PORTABLE_DIR / "runner_minimal" / "runner_minimal.exe",      "runner_minimal/runner_minimal.exe"),
        (PORTABLE_DIR / "compiler" / "compiler.exe",                  "compiler/compiler.exe"),
    ]
    all_ok = True
    for path, name in checks:
        if path.exists():
            print(f"   ✅ {name}")
        else:
            print(f"   ❌ {name} — НЕ НАЙДЕН")
            # Для help-файлов, иконки и pyc это не критично
            if "help" in name or "app.ico" in name:
                print(f"      ⚠️  Может работать неправильно.")
            else:
                all_ok = False

    return all_ok


# ============================================================
# ГЛАВНАЯ
# ============================================================
def main():
    print("=" * 60)
    print("ArrayVator — портативная сборка (3 варианта runner)")
    print("=" * 60)
    print(f"Проект:  {PROJECT_DIR}")
    print(f"Выход:   {PORTABLE_DIR}")

    python = find_python()
    if not python:
        print("\n❌ python.exe не найден")
        return 1
    print(f"Python:  {python}")

    ok_pyi, version = check_pyinstaller(python)
    if not ok_pyi:
        print(f"\n❌ PyInstaller не установлен: {version}")
        print("Установите: pip install pyinstaller")
        return 1
    print(f"PyInstaller: {version}")

    if UPX_DIR:
        print(f"UPX:     {UPX_DIR} (сжатие .pyc)")
    else:
        print("UPX:     не найден (сборка без сжатия)")

    # ------------------------------------------------------------
    # Проверка help/
    # ------------------------------------------------------------
    help_ok = check_help_dir()
    if not help_ok:
        print()
        print("⚠️  Папка help/ пуста или отсутствует.")
        print("   Справка в собранном редакторе работать НЕ будет.")
        ans = input("Продолжить сборку без справки? (y/N): ").strip().lower()
        if ans != 'y':
            return 1

    # ------------------------------------------------------------
    # Проверка пакета syntax/
    # ------------------------------------------------------------
    syntax_ok = check_syntax_package()
    if not syntax_ok:
        print()
        print("⚠️  Пакет syntax/ не найден или неполон.")
        print("   Панель справки в собранном редакторе работать НЕ будет.")
        ans = input("Продолжить сборку без панели справки? (y/N): ").strip().lower()
        if ans != 'y':
            return 1

    # ------------------------------------------------------------
    # Проверка иконки
    # ------------------------------------------------------------
    icon_ok = check_icon()
    if not icon_ok:
        print()
        ans = input("Продолжить сборку без иконки? (y/N): ").strip().lower()
        if ans != 'y':
            return 1

    # ------------------------------------------------------------
    # Проверка библиотек
    # ------------------------------------------------------------
    missing = check_libraries()
    if missing:
        print()
        print("❌ Не установлены библиотеки:")
        for m in missing:
            print(f"     pip install {m}")
        print()
        ans = input("Продолжить? (y/N): ").strip().lower()
        if ans != 'y':
            return 1

    # Очистка
    for d in (DIST_DIR, BUILD_DIR):
        if d.exists():
            try:
                shutil.rmtree(d)
            except Exception as e:
                print(f"⚠️  Не удалось удалить {d.name}/: {e}")
    DIST_DIR.mkdir()
    BUILD_DIR.mkdir()

    # Сборка
    components = [
        ("runner",         "runner.py",       RUNNER_FULL_FLAGS),
        ("runner_data",    "runner.py",       RUNNER_DATA_FLAGS),
        ("runner_minimal", "runner.py",       RUNNER_MINIMAL_FLAGS),
        ("compiler",       "compiler_gui.py", COMPILER_FLAGS),
        ("arrayvator",     "main.py",         ARRAYVATOR_FLAGS),
    ]

    results = {}
    for name, script, flags in components:
        results[name] = build_one(name, script, python, flags)

    if not all(results.values()):
        print()
        print("💥 Не все компоненты собраны")
        return 1

    ok_portable = assemble_portable()

    print()
    print("=" * 60)
    print("ИТОГ")
    print("=" * 60)

    if not ok_portable:
        print("\n💥 Не удалось собрать портативную папку")
        return 1

    print()
    print("Размеры компонентов:")
    for comp, display in [
        ("runner",         "runner/           (FULL, консоль)"),
        ("runner_data",    "runner_data/      (DATA, консоль)"),
        ("runner_minimal", "runner_minimal/   (MINIMAL, консоль)"),
        ("compiler",       "compiler/         (GUI, без консоли)"),
        ("arrayvator",     "editor            (GUI, без консоли)"),
    ]:
        d = DIST_DIR / comp
        if d.exists():
            print(f"  {display:35s} {_dir_size_mb(d):7.1f} MB")

    # Размер help/
    help_dst = PORTABLE_DIR / "help"
    if help_dst.exists():
        print(f"  {'help/ (справка)':35s} {_dir_size_kb(help_dst) / 1024:7.1f} MB")

    # Размер иконки
    icon_dst = PORTABLE_DIR / "app.ico"
    if icon_dst.exists():
        print(f"  {'app.ico (иконка)':35s} {icon_dst.stat().st_size / 1024:7.1f} KB")

    total = _dir_size_mb(PORTABLE_DIR)
    print(f"  {'—' * 45}")
    print(f"  {'ВСЕГО':35s} {total:7.1f} MB")

    print()
    print(f"🎉 Готово!")
    print(f"Папка: {PORTABLE_DIR}")
    print()
    print("Структура:")
    print("  ArrayVator_Portable/")
    print("  ├── ArrayVator.exe          ← БЕЗ консоли")
    print("  ├── app.ico                 ← внешняя иконка")
    print("  ├── _internal/")
    print("  │   ├── app.ico             ← вшитая иконка")
    print("  │   ├── help/               ← вшитая справка (fallback)")
    print("  │   └── syntax/             ← база справки (панель справа)")
    print("  ├── help/                   ← внешняя справка (приоритет!)")
    print("  ├── runner/                 ← С консолью (FULL)")
    print("  ├── runner_data/            ← С консолью (DATA)")
    print("  ├── runner_minimal/         ← С консолью (MINIMAL)")
    print("  └── compiler/               ← БЕЗ консоли (GUI)")
    print()
    print("📌 Что где:")
    print("   • ArrayVator.exe      — редактор. Консоли НЕТ.")
    print("   • runner.exe          — интерпретатор. Консоль ЕСТЬ.")
    print("   • compiler.exe        — компилятор. Консоли НЕТ.")
    print("   • Окно Console в редакторе — работает всегда (Tkinter).")
    print()
    print("📖 Справка:")
    print("   • help/               — внешние .txt, можно править вручную")
    print("   • _internal/help/     — вшитые .txt, fallback")
    print("   • _internal/syntax/   — база функций для панели справки")
    print("   Поиск: сначала внешняя, потом вшитая.")
    print()
    print("🎨 Иконка:")
    print("   • app.ico             — внешняя, для iconbitmap() во время работы")
    print("   • _internal/app.ico   — вшитая, fallback")
    print("   • Иконка самого EXE вшита через --icon.")
    return 0


if __name__ == '__main__':
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\n\n⚠️  Прервано пользователем")
        sys.exit(1)