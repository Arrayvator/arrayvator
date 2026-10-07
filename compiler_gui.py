# compiler_gui.py
"""
ArrayVator Compiler: ARRV → EXE.
Builds a standalone folder with the EXE and all libraries.
No Python required on the target PC.

Smart runner selection:
    MINIMAL — core only (no duckdb, no excel, no charts)
    DATA    — duckdb + excel, no charts
    FULL    — everything (duckdb, excel, matplotlib, plotly)

Usage:
    python compiler_gui.py
"""

import os
import re
import sys
import time
import shutil
import struct
import subprocess
import threading
import traceback
from pathlib import Path

try:
    import tkinter as tk
    from tkinter import filedialog, messagebox, scrolledtext, ttk
except ImportError:
    print("Tkinter not installed")
    sys.exit(1)

MAGIC = b"ARRV_PAYLOAD_V1\x00"


# ============================================================
# FIND PYTHON (internal)
# ============================================================
def _find_python():
    """Find a working python.exe."""
    if sys.executable and os.path.exists(sys.executable):
        basename = os.path.basename(sys.executable).lower()
        if 'python' in basename:
            return sys.executable

    for name in ('python', 'python3', 'py'):
        path = shutil.which(name)
        if path and os.path.exists(path):
            if 'python' in os.path.basename(path).lower():
                return path

    candidates = [
        os.path.expanduser(
            r'~\AppData\Local\Python\pythoncore-3.14-64\python.exe'
        ),
        os.path.expanduser(
            r'~\AppData\Local\Python\pythoncore-3.13-64\python.exe'
        ),
        r'C:\Python314\python.exe',
        r'C:\Python313\python.exe',
    ]
    for p in candidates:
        if os.path.exists(p):
            return p

    return None


def _check_builder(python):
    """Internal — check that the builder backend is available."""
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


# ============================================================
# ARRV CODE ANALYSIS — выбор runner'а
# ============================================================
def analyze_arrv(source_code):
    """
    Анализирует код .arrv и возвращает нужный тип runner.

    Возвращает: 'minimal' | 'data' | 'full'

    Логика:
        FULL    — если есть chart / report_* (нужны matplotlib, plotly, tkinter)
        DATA    — если есть BigData/Parquet/Excel/printshow/InputShow
                  (нужны duckdb, openpyxl, calamine, tkinter)
        MINIMAL — всё остальное (только ядро)

    ⚠️  Анализ — по строке. Может ложно сработать на комментариях,
        но fallback на FULL всегда есть.
    """
    code = source_code.lower()

    # ============================================================
    # 1. FULL — графики и отчёты
    # ============================================================
    full_markers = [
        # Графики
        'chart(',
        'chart (',
        # Отчёты (любой report тянет plotly)
        'report(',
        'report (',
        'report_section(',
        'report_text(',
        'report_table(',
        'report_chart(',
        'report_save(',
        'report_show(',
        'report_save_pdf(',
    ]
    for marker in full_markers:
        if marker in code:
            return 'full'

    # ============================================================
    # 2. DATA — duckdb / excel / интерактивные окна
    # ============================================================
    data_markers = [
        # BigData / DuckDB
        'bigdata',
        'duckdb',
        'openparquet(',
        'saveparquet(',
        'tobigdata(',
        'tommatrix(',   # на всякий случай (опечатка)
        'tomatrix(',
        'convert_matrix_to_bigdata(',
        'convert_bigdata_to_matrix(',
        # Excel
        'openexcel(',
        'saveexcel(',
        'openexcelshow(',
        'saveexcelshow(',
        # Интерактивные окна
        'printshow(',
        'inputshow(',
        'inputshowform(',
        'inputlistshow(',
        # DuckDB-специфичные операции, которые могут не работать на Matrix
        'join(',
        'unpivot(',
    ]
    for marker in data_markers:
        if marker in code:
            return 'data'

    # ============================================================
    # 3. MINIMAL — всё остальное
    # ============================================================
    return 'minimal'


# ============================================================
# FILTER INTERNAL LOG LINES
# ============================================================
def _should_filter_line(line):
    """
    Возвращает True, если строку нужно скрыть от пользователя.
    Фильтруем технические сообщения сборщика.
    """
    if not line:
        return True

    stripped = line.strip()
    if not stripped:
        return True

    low = stripped.lower()

    hidden_markers = [
        'pyinstaller',
        'upx is not available',
        'info: python:',
        'info: pyinstaller:',
        'info: platform:',
        'info: wrote ',
        'info: analyzing',
        'info: processing',
        'info: building',
        'info: copying',
        'info: checking',
        'info: loading',
        'info: including',
        'info: excluding',
        'info: looking for',
        'info: found ',
        'info: excluded',
        'info: module',
        'info: bootloader',
        'info: extending',
        'info: appending',
        'info: removing',
        'python 3.',
        'python314.dll',
        'python313.dll',
        'python312.dll',
    ]

    for marker in hidden_markers:
        if marker in low:
            return True

    if stripped.startswith('WARNING:'):
        if 'lib not found' not in low:
            return True
        return False

    return False


# ============================================================
# FIND PROJECT DIR
# ============================================================
def _get_project_dir():
    """Find the project folder."""
    if getattr(sys, 'frozen', False):
        current = Path(sys.executable).parent.resolve()
    else:
        current = Path(__file__).parent.resolve()

    for _ in range(10):
        if (current / 'runner.py').exists() and (current / 'lexer.py').exists():
            return current
        if current.parent == current:
            break
        current = current.parent

    fallback = Path(r"C:\Users\kos\Documents\0\Arrayvator")
    if (fallback / 'runner.py').exists():
        return fallback

    return Path(__file__).parent.resolve()


PROJECT_DIR = _get_project_dir()


# ============================================================
# SANITIZE NAME
# ============================================================
def sanitize_name(name):
    """Keep only latin letters, digits, _ and -."""
    name = re.sub(r'[^a-zA-Z0-9_-]', '', name)
    name = re.sub(r'_+', '_', name)
    name = name.strip('_')
    return name or 'program'


# ============================================================
# FIND RUNNER — с выбором типа
# ============================================================
def _find_runner_dir(needs='full'):
    """
    Ищет папку с runner по типу.

    needs: 'minimal' | 'data' | 'full'

    Возвращает (runner_exe_path, runner_dir_path) или (None, None).

    Fallback: если нужный runner не найден — пробуем full.
    """
    if getattr(sys, 'frozen', False):
        exe_dir = Path(sys.executable).parent.resolve()
    else:
        exe_dir = Path(__file__).parent.resolve()

    def _try_dirs(dirs):
        for runner_dir in dirs:
            if not runner_dir.exists():
                continue

            runner_exe = runner_dir / "runner.exe"
            if runner_exe.exists():
                return runner_exe, runner_dir

            # Имя EXE может отличаться (runner_data.exe и т.п.)
            for exe in runner_dir.glob("*.exe"):
                if exe.name.lower() in ('python.exe', 'pythonw.exe'):
                    continue
                return exe, runner_dir

            python_exe = runner_dir / "python.exe"
            if python_exe.exists():
                return python_exe, runner_dir

        return None, None

    # ============================================================
    # Кандидаты по типу
    # ============================================================
    if needs == 'full':
        candidates = [
            exe_dir.parent / "runner",
            exe_dir / "runner",
            PROJECT_DIR / "dist" / "runner",
            PROJECT_DIR / "dist_runner" / "runner.dist",
        ]
    elif needs == 'data':
        candidates = [
            exe_dir.parent / "runner_data",
            exe_dir / "runner_data",
            PROJECT_DIR / "dist" / "runner_data",
        ]
    elif needs == 'minimal':
        candidates = [
            exe_dir.parent / "runner_minimal",
            exe_dir / "runner_minimal",
            PROJECT_DIR / "dist" / "runner_minimal",
        ]
    else:
        candidates = []

    exe, d = _try_dirs(candidates)
    if exe is not None:
        return exe, d

    # ============================================================
    # Fallback: если не нашли нужный — пробуем full
    # ============================================================
    if needs != 'full':
        return _find_runner_dir('full')

    return None, None


# ============================================================
# BUILD RUNTIME (dev-only helper)
# ============================================================
def build_runner(log_callback=None, progress_callback=None):
    """Build runtime (FULL). Slow — uses indeterminate progress."""
    def log(text):
        if log_callback:
            log_callback(text)

    def progress(value, text=None):
        if progress_callback:
            progress_callback(value, text)

    python = _find_python()
    if not python:
        return False, (
            "Runtime builder is not available.\n"
            "This is a developer-only operation."
        )

    ok, version = _check_builder(python)
    if not ok:
        return False, (
            f"Runtime builder is not available.\n\n"
            f"Details: {version}"
        )

    runner_py = PROJECT_DIR / "runner.py"
    if not runner_py.exists():
        return False, f"runner.py not found: {runner_py}"

    old_dist = PROJECT_DIR / "dist" / "runner"
    if old_dist.exists():
        try:
            shutil.rmtree(old_dist)
            log("Removed old build")
        except Exception:
            pass

    build_dir = PROJECT_DIR / "build"
    if build_dir.exists():
        try:
            shutil.rmtree(build_dir)
        except Exception:
            pass

    log("")
    log("Preparing runtime build (FULL)...")
    log("This will take 1-3 minutes.")
    log("")

    progress(0, "Building runtime...")

    cmd = [
        python, '-m', 'PyInstaller',
        '--onedir',
        '--name', 'runner',
        '--noconfirm',
        '--clean',
        '--collect-all', 'python_calamine',
        '--collect-all', 'pyexcelerate',
        '--collect-all', 'openpyxl',
        '--hidden-import', 'lexer',
        '--hidden-import', 'parser',
        '--hidden-import', 'ast_nodes',
        '--hidden-import', 'runtime',
        '--hidden-import', 'errors',
        '--hidden-import', 'syntax',
        '--hidden-import', 'operators',
        '--distpath', str(PROJECT_DIR / 'dist'),
        '--workpath', str(PROJECT_DIR / 'build'),
        '--specpath', str(PROJECT_DIR),
        str(runner_py),
    ]

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
            if _should_filter_line(line):
                low = line.lower()
                if 'analyzing' in low:
                    progress(20, "Analyzing modules...")
                elif 'processing' in low:
                    progress(40, "Processing modules...")
                elif 'building' in low:
                    progress(60, "Building runtime...")
                elif 'copying' in low:
                    progress(80, "Copying files...")
                continue

            log(line.rstrip())

        process.wait()

        if process.returncode != 0:
            return False, f"Build failed (code {process.returncode})"

    except Exception as e:
        return False, f"Build error: {e}"

    runner_dir = PROJECT_DIR / "dist" / "runner"
    if not runner_dir.exists():
        return False, "Runtime folder not found after build"

    runner_exe = runner_dir / "runner.exe"
    if not runner_exe.exists():
        return False, f"runner.exe not found in {runner_dir}"

    total = sum(
        f.stat().st_size for f in runner_dir.rglob('*') if f.is_file()
    )
    size_mb = total / (1024 * 1024)

    progress(100, "Done")

    return True, (
        f"Runtime built successfully.\n"
        f"Folder: {runner_dir}\n"
        f"EXE:    runner.exe\n"
        f"Size:   {size_mb:.1f} MB"
    )


# ============================================================
# BUILD EXE FROM .ARRV (with runner selection)
# ============================================================
def build_exe(arrv_path, output_dir, exe_name=None,
              log_callback=None, progress_callback=None):
    """
    Create a standalone program/ folder with the embedded code.

    Автоматически выбирает runner:
        MINIMAL — ядро
        DATA    — duckdb + excel
        FULL    — всё

    Progress steps:
        5   — validate
        15  — copy runtime
        40  — runtime copied
        50  — rename EXE
        60  — read source
        75  — embed code
        90  — verify
        100 — done
    """
    def log(text):
        if log_callback:
            log_callback(text)

    def progress(value, text=None):
        if progress_callback:
            progress_callback(value, text)

    progress(5, "Checking runtime...")

    arrv_path = Path(arrv_path).resolve()
    if not arrv_path.exists():
        return False, f"File not found: {arrv_path}"

    # ============================================================
    # 1. Читаем .arrv и анализируем
    # ============================================================
    progress(8, "Reading source...")
    try:
        source_code = arrv_path.read_text(encoding="utf-8")
    except Exception as e:
        return False, f"Could not read .arrv: {e}"

    needs = analyze_arrv(source_code)
    log(f"Analysis: runner = {needs.upper()}")

    # ============================================================
    # 2. Ищем нужный runner (с fallback)
    # ============================================================
    runner_exe, runner_dir = _find_runner_dir(needs)

    if runner_exe is None:
        return False, (
            "Runtime folder not found.\n\n"
            "Expected:\n"
            f"  {PROJECT_DIR / 'dist' / 'runner'}\n"
            f"  or next to the compiler: <dir>/runner\n\n"
            "Click 'Rebuild Runtime' first."
        )

    # Если был fallback — сообщим пользователю
    actual_type = runner_dir.name.replace('runner_', '').replace('runner', 'full')
    if actual_type != needs:
        log(f"⚠️  Runner '{needs}' not found, using '{actual_type}'")

    log(f"Runtime:  {runner_dir}")
    log("")

    exe_name = sanitize_name(exe_name or arrv_path.stem)
    output_dir = Path(output_dir).resolve()
    output_dir.mkdir(parents=True, exist_ok=True)

    program_dir = output_dir / exe_name
    log(f"Source:  {arrv_path}")
    log(f"Output:  {program_dir}")
    log("")

    # ============================================================
    # 3. Copy runtime
    # ============================================================
    progress(15, "Copying runtime...")
    log("Copying runtime...")
    if program_dir.exists():
        shutil.rmtree(program_dir)

    try:
        shutil.copytree(
            runner_dir, program_dir,
            ignore=shutil.ignore_patterns('__pycache__', '*.pyc', '*.pyo'),
        )
    except Exception as e:
        return False, f"Could not copy runtime: {e}"

    progress(40, "Runtime copied")

    # ============================================================
    # 4. Rename runner.exe → program.exe
    # ============================================================
    progress(50, "Renaming EXE...")
    program_exe = program_dir / f"{exe_name}.exe"
    old_name = runner_exe.name

    src_exe = program_dir / old_name
    if not src_exe.exists():
        exes = [
            e for e in program_dir.glob("*.exe")
            if e.name.lower() not in ('python.exe', 'pythonw.exe')
        ]
        if exes:
            src_exe = exes[0]
            old_name = src_exe.name
        else:
            return False, f"EXE not found in {program_dir}"

    try:
        src_exe.rename(program_exe)
        log(f"  Renamed: {old_name} -> {exe_name}.exe")
    except Exception as e:
        return False, f"Could not rename: {e}"

    log("")

    # ============================================================
    # 5. Read .arrv (уже прочитан выше)
    # ============================================================
    progress(60, "Encoding source...")
    payload = source_code.encode("utf-8")
    log(f"Source size: {len(payload)} bytes")
    log("")

    # ============================================================
    # 6. Embed code
    # ============================================================
    progress(75, "Embedding code...")
    log("Embedding code...")
    try:
        exe_data = program_exe.read_bytes()
        log(f"  EXE size: {len(exe_data)} bytes")

        length_bytes = struct.pack("<Q", len(payload))
        new_exe_data = exe_data + MAGIC + length_bytes + payload
        program_exe.write_bytes(new_exe_data)

        # --- 7. Verify ---
        progress(90, "Verifying...")
        check_data = program_exe.read_bytes()
        check_idx = check_data.rfind(MAGIC)
        if check_idx == -1:
            return False, "Internal marker not found after write!"
        check_len = int.from_bytes(
            check_data[check_idx + len(MAGIC):check_idx + len(MAGIC) + 8],
            "little"
        )
        if check_len != len(payload):
            return False, f"Payload mismatch: wrote {len(payload)}, read {check_len}"

        log(f"  Verified: {check_len} bytes embedded")
    except Exception as e:
        return False, f"Could not embed code: {e}"

    log("")

    # ============================================================
    # 8. Result
    # ============================================================
    size_mb = sum(
        f.stat().st_size for f in program_dir.rglob('*') if f.is_file()
    ) / (1024 * 1024)
    file_count = sum(1 for f in program_dir.rglob('*') if f.is_file())

    progress(100, "Done")

    return True, (
        f"Build successful!\n"
        f"Runner:  {actual_type.upper()}\n"
        f"Folder:  {program_dir}\n"
        f"EXE:     {exe_name}.exe\n"
        f"Files:   {file_count}\n"
        f"Size:    {size_mb:.1f} MB\n\n"
        f"Copy the WHOLE folder '{program_dir.name}' to another PC.\n"
        f"Run {exe_name}.exe — no additional software required."
    )


# ============================================================
# GUI
# ============================================================
class CompilerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("ArrayVator Compiler")
        self.root.geometry("900x760")
        self.root.minsize(700, 600)

        self.arrv_path = tk.StringVar()
        self.output_dir = tk.StringVar()
        self.exe_name = tk.StringVar()
        self.is_building = False

        # Progress state
        self._progress_start_time = None
        self._progress_mode = None
        self._progress_text = ""
        self._progress_task = None

        self._build_ui()
        self._check_environment()

    def _build_ui(self):
        # Header
        header = tk.Frame(self.root, bg="#2c3e50", height=60)
        header.pack(fill=tk.X)
        header.pack_propagate(False)
        tk.Label(
            header, text="ArrayVator Compiler",
            font=("Arial", 16, "bold"),
            bg="#2c3e50", fg="white"
        ).pack(side=tk.LEFT, padx=20)
        tk.Label(
            header, text="ARRV  →  EXE",
            font=("Arial", 10),
            bg="#2c3e50", fg="#bdc3c7"
        ).pack(side=tk.LEFT)

        # Runtime panel
        runner_frame = tk.Frame(self.root, bg="#ecf0f1", padx=20, pady=10)
        runner_frame.pack(fill=tk.X)

        self.runner_status = tk.Label(
            runner_frame, text="Checking runtime...",
            font=("Arial", 10), bg="#ecf0f1", anchor="w"
        )
        self.runner_status.pack(side=tk.LEFT, fill=tk.X, expand=True)

        self.build_runner_btn = tk.Button(
            runner_frame, text="Rebuild Runtime",
            command=self._build_runner,
            bg="#3498db", fg="white",
            font=("Arial", 10, "bold"),
            padx=15, pady=5,
        )
        self.build_runner_btn.pack(side=tk.RIGHT)

        # Form
        form = tk.Frame(self.root, bg="#f5f5f5", padx=20, pady=15)
        form.pack(fill=tk.X)

        tk.Label(form, text="Source .arrv:",
                 font=("Arial", 11, "bold"), bg="#f5f5f5").grid(
            row=0, column=0, sticky="w", pady=6)
        tk.Entry(form, textvariable=self.arrv_path,
                 font=("Consolas", 10)).grid(
            row=0, column=1, sticky="ew", padx=8, pady=6)
        tk.Button(form, text="Browse...", command=self._browse_arrv,
                  bg="#87CEEB", width=12).grid(row=0, column=2, pady=6)

        tk.Label(form, text="Output folder:",
                 font=("Arial", 11, "bold"), bg="#f5f5f5").grid(
            row=1, column=0, sticky="w", pady=6)
        tk.Entry(form, textvariable=self.output_dir,
                 font=("Consolas", 10)).grid(
            row=1, column=1, sticky="ew", padx=8, pady=6)
        tk.Button(form, text="Browse...", command=self._browse_output,
                  bg="#87CEEB", width=12).grid(row=1, column=2, pady=6)

        tk.Label(form, text="EXE name:",
                 font=("Arial", 11, "bold"), bg="#f5f5f5").grid(
            row=2, column=0, sticky="w", pady=6)
        tk.Entry(form, textvariable=self.exe_name,
                 font=("Consolas", 10)).grid(
            row=2, column=1, sticky="ew", padx=8, pady=6)
        tk.Label(form, text="(latin letters, no .exe)",
                 font=("Arial", 9), bg="#f5f5f5", fg="#888").grid(
            row=2, column=2, sticky="w", pady=6)

        form.columnconfigure(1, weight=1)

        # Buttons
        btn_frame = tk.Frame(self.root, bg="#f5f5f5", pady=10)
        btn_frame.pack(fill=tk.X)

        self.build_btn = tk.Button(
            btn_frame, text="Build EXE",
            command=self._start_build,
            bg="#27ae60", fg="white",
            font=("Arial", 12, "bold"),
            padx=30, pady=10,
        )
        self.build_btn.pack(side=tk.LEFT, padx=20)

        tk.Button(
            btn_frame, text="Clear Log",
            command=self._clear_log,
            bg="#e0e0e0", font=("Arial", 10),
            padx=15, pady=10,
        ).pack(side=tk.LEFT, padx=5)

        tk.Button(
            btn_frame, text="Open Folder",
            command=self._open_output_dir,
            bg="#e0e0e0", font=("Arial", 10),
            padx=15, pady=10,
        ).pack(side=tk.LEFT, padx=5)

        # Progress bar
        progress_frame = tk.Frame(self.root, bg="#f5f5f5", padx=20)
        progress_frame.pack(fill=tk.X, pady=(0, 10))

        style = ttk.Style()
        try:
            style.theme_use('default')
        except Exception:
            pass
        style.configure(
            "AV.Horizontal.TProgressbar",
            troughcolor="#e0e0e0",
            background="#27ae60",
            lightcolor="#27ae60",
            darkcolor="#1e8449",
            thickness=14,
        )

        self.progress_bar = ttk.Progressbar(
            progress_frame,
            style="AV.Horizontal.TProgressbar",
            orient="horizontal",
            mode="determinate",
            maximum=100,
            value=0,
        )
        self.progress_bar.pack(fill=tk.X)

        self.progress_label = tk.Label(
            progress_frame,
            text="",
            font=("Consolas", 9),
            bg="#f5f5f5",
            fg="#555",
            anchor="w",
        )
        self.progress_label.pack(fill=tk.X, pady=(4, 0))

        # Log
        log_frame = tk.Frame(self.root, bg="#f5f5f5")
        log_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 15))

        tk.Label(log_frame, text="Build log:",
                 font=("Arial", 10, "bold"),
                 bg="#f5f5f5", anchor="w").pack(fill=tk.X)

        self.log_text = scrolledtext.ScrolledText(
            log_frame,
            font=("Consolas", 9),
            bg="#1e1e1e", fg="#d4d4d4",
            insertbackground="white",
            wrap=tk.WORD,
        )
        self.log_text.pack(fill=tk.BOTH, expand=True, pady=5)

        self.log_text.tag_config("error", foreground="#ff6b6b")
        self.log_text.tag_config("success", foreground="#90ee90")
        self.log_text.tag_config("info", foreground="#87ceeb")

        # Status
        self.status = tk.Label(
            self.root, text="Ready",
            font=("Consolas", 9),
            bg="#ecf0f1", fg="#555",
            anchor="w", padx=10, pady=4,
        )
        self.status.pack(fill=tk.X, side=tk.BOTTOM)

    # ============================================================
    # PROGRESS CONTROL
    # ============================================================
    def _progress_start_indeterminate(self, text="Working..."):
        self._progress_mode = 'indeterminate'
        self._progress_start_time = time.time()
        self._progress_text = text

        self.progress_bar.stop()
        self.progress_bar.config(mode="indeterminate", value=0)
        self.progress_bar.start(15)

        self._tick_progress_label()

    def _progress_start_determinate(self, text="Working..."):
        self._progress_mode = 'determinate'
        self._progress_start_time = time.time()
        self._progress_text = text

        self.progress_bar.stop()
        self.progress_bar.config(mode="determinate", value=0)

        self._tick_progress_label()

    def _progress_set(self, value, text=None):
        self.progress_bar.stop()
        self.progress_bar.config(mode="determinate", value=value)
        if text is not None:
            self._progress_text = text
        self._update_progress_label_text()

    def _progress_stop(self, text="Done"):
        self.progress_bar.stop()
        self._progress_mode = None
        self._progress_text = text
        self.progress_label.config(text=text)
        if self._progress_task:
            try:
                self.root.after_cancel(self._progress_task)
            except Exception:
                pass
            self._progress_task = None

    def _tick_progress_label(self):
        if self._progress_start_time is None:
            return

        elapsed = time.time() - self._progress_start_time
        self._update_progress_label_text(elapsed)

        if self._progress_mode is not None:
            self._progress_task = self.root.after(
                500, self._tick_progress_label
            )

    def _update_progress_label_text(self, elapsed=None):
        if elapsed is None and self._progress_start_time is not None:
            elapsed = time.time() - self._progress_start_time

        base = self._progress_text or "Working..."
        if elapsed is not None:
            self.progress_label.config(text=f"{base}   ({elapsed:.1f}s)")
        else:
            self.progress_label.config(text=base)

    # ============================================================
    # ENVIRONMENT
    # ============================================================
    def _check_environment(self):
        # Проверяем наличие трёх runner'ов
        found = []
        for needs in ('full', 'data', 'minimal'):
            exe, d = _find_runner_dir(needs)
            if d:
                found.append(needs.upper())

        if found:
            self.runner_status.config(
                text=f"Runtimes ready: {', '.join(found)}",
                fg="#27ae60"
            )
            self.build_runner_btn.config(text="Rebuild Runtime")

            if getattr(sys, 'frozen', False):
                self.build_runner_btn.config(
                    text="Rebuild Runtime",
                    state="disabled",
                )
        else:
            self.runner_status.config(
                text="Runtime not built — click the button",
                fg="#e74c3c"
            )

    # ============================================================
    # BUILD RUNTIME
    # ============================================================
    def _build_runner(self):
        if self.is_building:
            return

        if not messagebox.askyesno(
            "Rebuild Runtime",
            "Rebuild runtime?\n\n"
            "This takes 1-3 minutes.\n"
            "Usually done once.",
        ):
            return

        self._clear_log()
        self._log("=" * 60)
        self._log("BUILDING RUNTIME")
        self._log("=" * 60)
        self._log("")

        self.is_building = True
        self.build_btn.config(state="disabled")
        self.build_runner_btn.config(state="disabled")
        self._set_status("Building runtime... (1-3 minutes)")

        self._progress_start_indeterminate("Building runtime...")

        def build_thread():
            try:
                success, message = build_runner(
                    log_callback=self._log,
                    progress_callback=self._progress_cb_from_thread,
                )
            except Exception as e:
                success = False
                message = f"Unexpected error:\n{e}\n\n{traceback.format_exc()}"
            self.root.after(0, lambda: self._on_runner_done(success, message))

        threading.Thread(target=build_thread, daemon=True).start()

    def _progress_cb_from_thread(self, value, text=None):
        def _apply():
            if value == 0 and text == "Building runtime...":
                self._progress_text = text or "Working..."
                self._update_progress_label_text()
            elif value >= 100:
                self._progress_stop(text or "Done")
            else:
                self._progress_set(value, text)
        try:
            self.root.after(0, _apply)
        except Exception:
            pass

    def _on_runner_done(self, success, message):
        self.is_building = False
        self.build_btn.config(state="normal")
        self.build_runner_btn.config(state="normal")

        self._log("")
        self._log("=" * 60)
        if success:
            self._log("RUNTIME READY", "success")
            self._log("=" * 60)
            self._log(message, "success")
            self._set_status("Runtime ready")
            self._progress_stop("Runtime ready")
            self._check_environment()
        else:
            self._log("ERROR", "error")
            self._log("=" * 60)
            self._log(message, "error")
            self._set_status("Runtime build error")
            self._progress_stop("Error")
            messagebox.showerror("Error", message)

    # ============================================================
    # FILE DIALOGS
    # ============================================================
    def _browse_arrv(self):
        path = filedialog.askopenfilename(
            title="Select .arrv file",
            initialdir=PROJECT_DIR,
            filetypes=[
                ("ArrayVator files", "*.arrv"),
                ("Text files", "*.txt"),
                ("All files", "*.*"),
            ]
        )
        if path:
            self.arrv_path.set(path)
            if not self.exe_name.get():
                self.exe_name.set(sanitize_name(Path(path).stem))
            if not self.output_dir.get():
                self.output_dir.set(str(Path(path).parent / "dist"))

    def _browse_output(self):
        path = filedialog.askdirectory(
            title="Select output folder",
            initialdir=self.output_dir.get() or str(PROJECT_DIR),
        )
        if path:
            self.output_dir.set(path)

    def _open_output_dir(self):
        path = self.output_dir.get()
        if not path or not os.path.exists(path):
            messagebox.showwarning("Warning", "Folder does not exist")
            return
        try:
            if sys.platform == 'win32':
                os.startfile(path)
            elif sys.platform == 'darwin':
                os.system(f'open "{path}"')
            else:
                os.system(f'xdg-open "{path}"')
        except Exception as e:
            messagebox.showerror("Error", str(e))

    # ============================================================
    # LOG
    # ============================================================
    def _clear_log(self):
        self.log_text.delete(1.0, tk.END)

    def _log(self, text, tag=None):
        if _should_filter_line(text):
            return
        self.log_text.insert(tk.END, text + "\n", tag)
        self.log_text.see(tk.END)
        self.log_text.update_idletasks()

    def _set_status(self, text):
        self.status.config(text=text)
        self.root.update_idletasks()

    # ============================================================
    # BUILD EXE
    # ============================================================
    def _start_build(self):
        if self.is_building:
            return

        arrv = self.arrv_path.get().strip()
        out = self.output_dir.get().strip()
        name = self.exe_name.get().strip()

        if not arrv:
            messagebox.showerror("Error", "Please select a .arrv file")
            return
        if not os.path.exists(arrv):
            messagebox.showerror("Error", f"File not found:\n{arrv}")
            return
        if not out:
            messagebox.showerror("Error", "Please select an output folder")
            return
        if not name:
            name = sanitize_name(Path(arrv).stem)
            self.exe_name.set(name)

        name = sanitize_name(name)
        self.exe_name.set(name)

        self._clear_log()
        self._log("=" * 60)
        self._log("BUILDING EXE")
        self._log("=" * 60)
        self._log(f"Source: {arrv}")
        self._log(f"Output: {out}")
        self._log(f"EXE:    {name}.exe")
        self._log("")

        self.is_building = True
        self.build_btn.config(state="disabled", text="Building...")
        self._set_status("Building...")

        self._progress_start_determinate("Starting...")

        def build_thread():
            try:
                success, message = build_exe(
                    arrv_path=arrv,
                    output_dir=out,
                    exe_name=name,
                    log_callback=self._log,
                    progress_callback=self._progress_cb_from_thread,
                )
            except Exception as e:
                success = False
                message = f"Unexpected error:\n{e}\n\n{traceback.format_exc()}"
            self.root.after(0, lambda: self._on_done(success, message, out, name))

        threading.Thread(target=build_thread, daemon=True).start()

    def _on_done(self, success, message, output_dir, exe_name):
        self.is_building = False
        self.build_btn.config(state="normal", text="Build EXE")

        self._log("")
        self._log("=" * 60)
        if success:
            self._log("DONE", "success")
            self._log("=" * 60)
            self._log(message, "success")
            self._set_status("Build completed successfully")
            self._progress_stop("Done")

            program_dir = Path(output_dir) / exe_name
            if program_dir.exists():
                try:
                    if sys.platform == 'win32':
                        os.startfile(program_dir)
                except Exception:
                    pass
        else:
            self._log("ERROR", "error")
            self._log("=" * 60)
            self._log(message, "error")
            self._set_status("Build error")
            self._progress_stop("Error")
            messagebox.showerror("Build error", message)


# ============================================================
# MAIN
# ============================================================
def main():
    root = tk.Tk()
    app = CompilerApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()