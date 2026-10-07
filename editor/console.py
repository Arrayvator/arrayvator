# editor/console.py
"""
Окно консоли ArrayVator Editor.
"""

import os
import tkinter as tk
from tkinter import scrolledtext, filedialog, messagebox

from locales import t
from theme import make_button


class ConsoleWindow:
    def __init__(self, root, theme):
        self.root = root
        self.theme = theme
        self.window = None
        self.text_widget = None

    def create(self):
        T = self.theme
        if self.window is None or not self.window.winfo_exists():
            self.window = tk.Toplevel(self.root)
            self.window.title(t("console_title"))
            self.window.geometry("900x600")
            self.window.configure(bg=T['bg'])
            self.window.protocol("WM_DELETE_WINDOW", self.hide)

            header = tk.Frame(self.window, bg=T['bg_alt'], height=40)
            header.pack(fill=tk.X)
            header.pack_propagate(False)

            tk.Label(
                header, text="📟 " + t("console_title"),
                bg=T['bg_alt'], fg=T['text'],
                font=("Segoe UI", 11, "bold"),
            ).pack(side=tk.LEFT, padx=14, pady=10)

            text_frame = tk.Frame(self.window, bg=T['bg'])
            text_frame.pack(fill=tk.BOTH, expand=True, padx=8, pady=8)

            self.text_widget = scrolledtext.ScrolledText(
                text_frame, wrap=tk.WORD, font=("Consolas", 11),
                bg=T['console_bg'], fg=T['console_fg'],
                insertbackground=T['console_fg'],
                relief="flat", bd=0,
                highlightthickness=1,
                highlightbackground=T['border'],
            )
            self.text_widget.pack(expand=True, fill=tk.BOTH)

            self.text_widget.tag_config("error",   foreground=T['console_err'])
            self.text_widget.tag_config("warning", foreground=T['console_warn'])
            self.text_widget.tag_config("success", foreground=T['console_ok'])
            self.text_widget.tag_config("info",    foreground=T['console_info'])
            self.text_widget.tag_config("dim",     foreground=T['console_dim'])
            self.text_widget.tag_config("hint",    foreground=T['console_hint'],
                                        font=("Consolas", 11, "italic"))

            btn_frame = tk.Frame(self.window, bg=T['bg'])
            btn_frame.pack(pady=(0, 12))

            make_button(btn_frame, "🗑  " + t("console_clear"),
                        self.clear, T, variant='ghost').pack(side=tk.LEFT, padx=6)
            make_button(btn_frame, "📋  " + t("console_copy"),
                        self.copy_all, T, variant='ghost').pack(side=tk.LEFT, padx=6)
            make_button(btn_frame, "💾  " + t("console_save"),
                        self.save_to_file, T, variant='ghost').pack(side=tk.LEFT, padx=6)
            make_button(btn_frame, "✕  " + t("console_close"),
                        self.hide, T, variant='danger').pack(side=tk.LEFT, padx=6)

            self.write("=" * 60 + "\n")
            self.write(t("console_title") + "\n")
            self.write("=" * 60 + "\n\n")
            self.write(f"{t('console_workdir')}: {os.getcwd()}\n")
            self.write("=" * 60 + "\n\n")

    def write(self, text):
        try:
            if self.text_widget and self.text_widget.winfo_exists():
                self.text_widget.insert(tk.END, text)
                self.text_widget.see(tk.END)
                self.text_widget.update_idletasks()
        except Exception:
            pass

    def write_error(self, text):
        try:
            if self.text_widget and self.text_widget.winfo_exists():
                self.text_widget.insert(tk.END, text, "error")
                self.text_widget.see(tk.END)
        except Exception:
            pass

    def write_hint(self, text):
        try:
            if self.text_widget and self.text_widget.winfo_exists():
                self.text_widget.insert(tk.END, text, "hint")
                self.text_widget.see(tk.END)
        except Exception:
            pass

    def clear(self):
        try:
            if self.text_widget and self.text_widget.winfo_exists():
                self.text_widget.delete(1.0, tk.END)
        except Exception:
            pass

    def copy_all(self):
        """Копирует всё содержимое консоли в буфер обмена."""
        try:
            if not self.text_widget or not self.text_widget.winfo_exists():
                return

            content = self.text_widget.get("1.0", tk.END)
            self.root.clipboard_clear()
            self.root.clipboard_append(content)
            self.root.update()

            self.write("\n" + t("console_copied") + "\n")
        except Exception as e:
            try:
                messagebox.showerror(
                    t("dlg_error"), str(e),
                    parent=self.window if self.window else self.root
                )
            except Exception:
                pass

    def save_to_file(self):
        """Сохраняет содержимое консоли в TXT-файл."""
        try:
            if not self.text_widget or not self.text_widget.winfo_exists():
                return

            path = filedialog.asksaveasfilename(
                parent=self.window if self.window else self.root,
                title=t("console_save"),
                defaultextension=".txt",
                filetypes=[
                    ("Text files", "*.txt"),
                    ("All files", "*.*"),
                ],
                initialfile="console.txt",
            )
            if not path:
                return

            content = self.text_widget.get("1.0", tk.END)
            with open(path, 'w', encoding='utf-8') as f:
                f.write(content)

            self.write(f"\n{t('console_saved')} {os.path.basename(path)}\n")
        except Exception as e:
            messagebox.showerror(
                t("dlg_error"), str(e),
                parent=self.window if self.window else self.root
            )

    def show(self):
        try:
            if self.window and self.window.winfo_exists():
                self.window.deiconify()
                self.window.lift()
            else:
                self.create()
        except Exception:
            self.create()

    def hide(self):
        try:
            if self.window and self.window.winfo_exists():
                self.window.withdraw()
        except Exception:
            pass