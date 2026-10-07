# editor/settings.py
"""
Настройки редактора: язык, тема, шрифт, размеры окна, палитра синтаксиса.
Сохраняются в settings.json рядом с main.py.
"""

import json
import os


class Settings:
    DEFAULTS = {
        "language": "en",
        "theme": "light",
        "font_family": "Consolas",
        "font_size": 12,
        "window_width": 1400,
        "window_height": 800,
        "syntax": {},
    }

    def __init__(self, path):
        self.path = path
        self.data = {
            "language": "en",
            "theme": "light",
            "font_family": "Consolas",
            "font_size": 12,
            "window_width": 1400,
            "window_height": 800,
            "syntax": {},
        }
        self.load()

    def load(self):
        if not os.path.exists(self.path):
            return
        try:
            with open(self.path, 'r', encoding='utf-8') as f:
                loaded = json.load(f)

            if "language" in loaded and loaded["language"] in ("ru", "en"):
                self.data["language"] = loaded["language"]
            if "theme" in loaded and loaded["theme"] in ("dark", "light"):
                self.data["theme"] = loaded["theme"]
            if "font_family" in loaded:
                self.data["font_family"] = loaded["font_family"]
            if "font_size" in loaded:
                self.data["font_size"] = int(loaded["font_size"])
            if "window_width" in loaded:
                self.data["window_width"] = int(loaded["window_width"])
            if "window_height" in loaded:
                self.data["window_height"] = int(loaded["window_height"])
            if "syntax" in loaded and isinstance(loaded["syntax"], dict):
                self.data["syntax"] = loaded["syntax"]
        except Exception:
            pass

    def save(self):
        try:
            with open(self.path, 'w', encoding='utf-8') as f:
                json.dump(self.data, f, ensure_ascii=False, indent=4)
        except Exception:
            pass

    def get(self, key, default=None):
        return self.data.get(key, default)

    def set(self, key, value):
        self.data[key] = value
        self.save()