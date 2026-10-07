# main.py
"""
ArrayVator Editor 2026 — entry point.

Вся логика — в пакете main_app.
"""

import sys
import os

# ============================================================
# РАБОЧАЯ ПАПКА
# ============================================================
if getattr(sys, 'frozen', False):
    current_dir = os.path.dirname(sys.executable)
else:
    current_dir = os.path.dirname(os.path.abspath(__file__))

if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

try:
    os.chdir(current_dir)
except Exception:
    pass


# ============================================================
# ЗАПУСК
# ============================================================
def main():
    import tkinter as tk
    from main_app import ArrayVatorEditor

    root = tk.Tk()
    app = ArrayVatorEditor(root, current_dir)
    root.protocol("WM_DELETE_WINDOW", app.close_app)
    root.mainloop()


if __name__ == "__main__":
    print("ArrayVator Editor 2026")
    print(f"Working folder: {os.getcwd()}")
    main()
    print("Editor closed")