# editor/widgets.py
"""
Виджет редактора с нумерацией строк и подсветкой синтаксиса.
"""

import re
import tkinter as tk
from tkinter import font

from editor.autocomplete import AutocompletePopup


HIGHLIGHT_KEYWORDS = [
    "if", "then", "else", "for", "while", "break",
    "true", "false", "null", "None",
    "all", "end", "begin", "last",
    "before", "after", "inside", "ignore", "skip", "approx",
    "vertical", "horizontal", "when",
    "by", "agg", "having",
    "BigData", "Table",
    "order",
    "try", "catch", "error",
    "chart", "bar", "line", "pie", "hist", "scatter", "box", "heatmap", "pair",
    "title", "save", "bins", "color", "xlabel", "ylabel", "plotly", "static",
    "report", "report_section", "report_text", "report_table",
    "report_chart", "report_save", "report_show", "report_save_pdf",
    "delete", "insert", "duplicate", "clear", "keep", "swap",
    "rows", "cols",
    "trim", "trimleft", "trimright",
    "year", "month", "day", "quarter",
    "weekday", "weekdayname", "monthname",
    "adddays", "addmonths", "addyears",
    "datetrunc",
    "sumif", "countif", "avgif", "minif", "maxif",
    "medianif", "countuniqueif", "sumproduct",
    "isnone", "fillna", "dropna", "coalesce", "noneif",
    "type", "is_number", "is_integer", "is_float",
    "is_string", "is_boolean", "to_string", "to_number",
    "range", "Number", "step",
]

HIGHLIGHT_OPERATORS = ["==", "!=", "<=", ">=", "and", "or", "not"]


class NumberedTextEditor(tk.Frame):
    def __init__(self, parent, settings=None, theme=None,
                 syntax_palette=None, **kwargs):
        super().__init__(parent, bg=theme['bg'])

        self.settings = settings
        self.theme = theme
        self.syntax_palette = syntax_palette or {}
        T = theme

        font_family = "Consolas"
        font_size = 12
        if settings:
            font_family = settings.get("font_family", "Consolas")
            font_size = settings.get("font_size", 12)

        self.editor_font = font.Font(family=font_family, size=font_size)
        self.line_font = font.Font(family=font_family, size=font_size)

        # ============================================================
        # ЛЕВАЯ КОЛОНКА — НОМЕРА СТРОК
        # ============================================================
        self.line_numbers = tk.Text(
            self, width=4, padx=8, takefocus=0, border=0,
            background=T['bg_alt'], foreground=T['text_muted'],
            state="disabled", wrap=tk.NONE, font=self.line_font,
            relief="flat",
        )
        self.line_numbers.pack(side=tk.LEFT, fill=tk.Y)

        # ============================================================
        # ЦЕНТР — РЕДАКТОР
        # ============================================================
        self.text_frame = tk.Frame(self, bg=T['border'], bd=0)
        self.text_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(1, 0))

        self.text = tk.Text(
            self.text_frame, wrap=tk.NONE, undo=True,
            font=self.editor_font,
            bg=T['bg_code'], fg=T['text'],
            insertbackground=T['accent'],
            selectbackground=T['bg_select'],
            selectforeground=T['text'],
            tabs=("1c",),
            relief="flat", bd=0,
            padx=8, pady=8,
            **kwargs
        )
        self.text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.v_scroll = tk.Scrollbar(
            self.text_frame, orient="vertical",
            command=self._on_scroll,
            bg=T['bg_alt'], troughcolor=T['bg'],
            activebackground=T['accent'], relief="flat",
        )
        self.v_scroll.pack(side=tk.RIGHT, fill=tk.Y)

        self.h_scroll = tk.Scrollbar(
            self, orient="horizontal",
            command=self.text.xview,
            bg=T['bg_alt'], troughcolor=T['bg'],
            activebackground=T['accent'], relief="flat",
        )
        self.h_scroll.pack(side=tk.BOTTOM, fill=tk.X)

        self.text.config(
            yscrollcommand=self._on_text_scroll,
            xscrollcommand=self.h_scroll.set,
        )

        self._init_syntax_tags()

        # ============================================================
        # ПРИВЯЗКА СОБЫТИЙ
        # ============================================================
        self.text.bind('<KeyRelease>', self._update_line_numbers, add='+')
        self.text.bind('<Button-1>', self._update_line_numbers, add='+')
        self.text.bind('<MouseWheel>', self._update_line_numbers, add='+')
        self.text.bind('<Button-4>', self._update_line_numbers, add='+')
        self.text.bind('<Button-5>', self._update_line_numbers, add='+')
        self.text.bind('<Configure>', self._update_line_numbers, add='+')

        self.line_numbers.bind('<MouseWheel>', self._on_mousewheel_numbers)
        self.line_numbers.bind('<Button-4>', self._on_mousewheel_numbers)
        self.line_numbers.bind('<Button-5>', self._on_mousewheel_numbers)

        self.autocomplete = AutocompletePopup(self.text, T)
        self.on_word_clicked = None

        self.text.bind("<KeyRelease>", self._on_key_release, add='+')
        self.text.bind("<Tab>", self._on_tab, add='+')
        self.text.bind("<Return>", self._on_return, add='+')
        self.text.bind("<Escape>", self._on_escape, add='+')
        self.text.bind("<Up>", self._on_arrow_up, add='+')
        self.text.bind("<Down>", self._on_arrow_down, add='+')
        self.text.bind("<FocusOut>", lambda e: self.autocomplete.hide(), add='+')
        self.text.bind("<ButtonRelease-1>", self._on_click, add='+')

        self._update_line_numbers()
        self.text.after(100, self._highlight_syntax)

    # ============================================================
    # ПОДСВЕТКА СИНТАКСИСА — ТЕГИ
    # ============================================================
    def _init_syntax_tags(self):
        base_family = self.editor_font.cget("family")
        base_size = self.editor_font.cget("size")

        for name in ('keyword', 'function', 'variable', 'string',
                     'number', 'comment', 'operator'):
            entry = self.syntax_palette.get(name, {})
            color = entry.get('color', '#000000')
            bold = entry.get('bold', False)
            italic = entry.get('italic', False)

            weight = "bold" if bold else "normal"
            slant = "italic" if italic else "roman"

            f = font.Font(family=base_family, size=base_size,
                          weight=weight, slant=slant)

            self.text.tag_config(f"syntax_{name}", foreground=color, font=f)

    def set_syntax_palette(self, palette):
        self.syntax_palette = palette
        self._init_syntax_tags()
        self._highlight_syntax()

    def set_font(self, family, size):
        new_font = font.Font(family=family, size=size)
        self.text.config(font=new_font)
        self.line_numbers.config(font=new_font)
        self.editor_font = new_font
        self._init_syntax_tags()

    # ============================================================
    # НУМЕРАЦИЯ СТРОК
    # ============================================================
    def _on_scroll(self, *args):
        self.text.yview(*args)
        self.line_numbers.yview(*args)

    def _on_text_scroll(self, first, last):
        self.v_scroll.set(first, last)
        self.line_numbers.yview_moveto(first)

    def _on_mousewheel_numbers(self, event):
        if event.delta:
            self.text.yview_scroll(int(-1 * (event.delta / 120)), "units")
        elif event.num == 4:
            self.text.yview_scroll(-1, "units")
        elif event.num == 5:
            self.text.yview_scroll(1, "units")
        self._update_line_numbers()

    def _update_line_numbers(self, event=None):
        try:
            total_lines = int(self.text.index('end-1c').split('.')[0])
            self.line_numbers.yview_moveto(self.text.yview()[0])

            numbers = "\n".join(str(i) for i in range(1, total_lines + 1))

            self.line_numbers.config(state="normal")
            self.line_numbers.delete("1.0", "end")
            self.line_numbers.insert("1.0", numbers)
            self.line_numbers.config(state="disabled")

            width = max(3, len(str(total_lines)))
            self.line_numbers.config(width=width)
        except Exception:
            pass

    # ============================================================
    # ПОДСВЕТКА СИНТАКСИСА
    # ============================================================
    def _highlight_syntax(self):
        try:
            for tag in ("syntax_keyword", "syntax_operator", "syntax_function",
                        "syntax_variable", "syntax_string", "syntax_number",
                        "syntax_comment"):
                self.text.tag_remove(tag, "1.0", tk.END)

            content = self.text.get("1.0", "end-1c")

            functions = set()
            try:
                from syntax.autocomplete_data import AUTOCOMPLETE_ITEMS
                functions = set(k.lower() for k in AUTOCOMPLETE_ITEMS.keys())
            except ImportError:
                pass

            keywords_lower = set(k.lower() for k in HIGHLIGHT_KEYWORDS)

            self._highlight_words(HIGHLIGHT_KEYWORDS, "syntax_keyword", content)
            self._highlight_words(HIGHLIGHT_OPERATORS, "syntax_operator", content)

            if functions:
                self._highlight_words(
                    list(functions), "syntax_function", content
                )

            self._highlight_pattern(r'"[^"\n]*"', "syntax_string", content)
            self._highlight_pattern(r"'[^'\n]*'", "syntax_string", content)
            self._highlight_pattern(r'\b\d+\.?\d*\b', "syntax_number", content)
            self._highlight_pattern(r'#[^\n]*', "syntax_comment", content)

            self._highlight_variables(content, keywords_lower, functions)

        except Exception:
            pass

    def _highlight_words(self, words, tag, content):
        for word in words:
            pattern = r'\b' + re.escape(str(word)) + r'\b'
            for match in re.finditer(pattern, content, re.IGNORECASE):
                start_pos = self._offset_to_index(content, match.start())
                end_pos = self._offset_to_index(content, match.end())
                self.text.tag_add(tag, start_pos, end_pos)

    def _highlight_pattern(self, pattern, tag, content):
        for match in re.finditer(pattern, content):
            start_pos = self._offset_to_index(content, match.start())
            end_pos = self._offset_to_index(content, match.end())
            self.text.tag_add(tag, start_pos, end_pos)

    def _highlight_variables(self, content, keywords_lower, functions):
        forbidden_zones = []

        for m in re.finditer(r'"[^"\n]*"', content):
            forbidden_zones.append((m.start(), m.end()))
        for m in re.finditer(r"'[^'\n]*'", content):
            forbidden_zones.append((m.start(), m.end()))
        for m in re.finditer(r'#[^\n]*', content):
            forbidden_zones.append((m.start(), m.end()))

        def in_forbidden(pos):
            for s, e in forbidden_zones:
                if s <= pos < e:
                    return True
            return False

        pattern = re.compile(r'\b[a-zA-Z_][a-zA-Z0-9_]*\b')

        for match in pattern.finditer(content):
            name = match.group(0)
            name_lower = name.lower()

            if in_forbidden(match.start()):
                continue
            if name_lower in keywords_lower:
                continue
            if name_lower in functions:
                continue

            start_pos = self._offset_to_index(content, match.start())
            end_pos = self._offset_to_index(content, match.end())
            self.text.tag_add("syntax_variable", start_pos, end_pos)

    def _offset_to_index(self, content, offset):
        line = content[:offset].count('\n') + 1
        col = offset - content[:offset].rfind('\n') - 1
        if col < 0:
            col = 0
        return f"{line}.{col}"

    # ============================================================
    # ОБЁРТКИ НАД tk.Text
    # ============================================================
    def get(self, *args, **kwargs):
        return self.text.get(*args, **kwargs)

    def insert(self, *args, **kwargs):
        return self.text.insert(*args, **kwargs)

    def delete(self, *args, **kwargs):
        return self.text.delete(*args, **kwargs)

    def index(self, *args, **kwargs):
        return self.text.index(*args, **kwargs)

    def see(self, *args, **kwargs):
        return self.text.see(*args, **kwargs)

    def focus_set(self):
        return self.text.focus_set()

    def edit_undo(self):
        return self.text.edit_undo()

    def edit_redo(self):
        return self.text.edit_redo()

    # ============================================================
    # ОПРЕДЕЛЕНИЕ СЛОВА ПОД КУРСОРОМ
    # ============================================================
    def _get_current_word(self):
        """
        Возвращает (word, start_pos).

        word — набранное слово (может быть пустым).
        start_pos — индекс начала слова (например "1.5").
        """
        try:
            cursor = self.text.index(tk.INSERT)
            line, col = cursor.split('.')
            col = int(col)
            if col == 0:
                return "", None

            line_text = self.text.get(f"{line}.0", f"{line}.{col}")

            # Идём назад от курсора, пока символы — буквы/цифры/_
            i = len(line_text)
            while i > 0 and (
                line_text[i - 1].isalnum()
                or line_text[i - 1] == '_'
            ):
                i -= 1

            word = line_text[i:]
            start_col = col - len(word)
            return word, f"{line}.{start_col}"
        except Exception:
            return "", None

    def _is_in_string_or_comment(self):
        """Проверяет, что курсор внутри строки или комментария."""
        try:
            cursor = self.text.index(tk.INSERT)
            line_num = cursor.split('.')[0]
            line_text = self.text.get(f"{line_num}.0", cursor)

            in_string = False
            string_char = None
            i = 0
            while i < len(line_text):
                ch = line_text[i]
                if in_string:
                    if ch == string_char:
                        in_string = False
                    elif ch == '\\':
                        i += 1
                else:
                    if ch in ('"', "'"):
                        in_string = True
                        string_char = ch
                    elif ch == '#':
                        return True
                i += 1
            return in_string
        except Exception:
            return False

    # ============================================================
    # ОСНОВНОЙ ОБРАБОТЧИК НАЖАТИЯ КЛАВИШ
    # ============================================================
    def _on_key_release(self, event):
        """
        Вызывается после каждого нажатия клавиши.

        Логика:
            1. Пропускаем служебные клавиши.
            2. Если курсор в строке/комментарии — прячем попап.
            3. Получаем текущее слово.
            4. Если слово < 1 символа — прячем попап.
            5. Получаем список кандидатов через get_autocomplete_list():
               - обычный поиск по имени
               - если пусто — поиск по АЛИАСАМ ("впр" → vlookup)
            6. Если список пустой — прячем попап.
            7. Если набрано полное имя функции — прячем попап.
            8. Иначе — показываем попап.
        """
        # Служебные клавиши — только перерисовать подсветку
        if event.keysym in ('Up', 'Down', 'Left', 'Right',
                            'Escape', 'Return', 'Tab',
                            'Shift_L', 'Shift_R', 'Control_L', 'Control_R',
                            'Alt_L', 'Alt_R', 'Caps_Lock'):
            self._highlight_syntax()
            return

        # Импортируем функции автодополнения
        try:
            from syntax.autocomplete_data import get_autocomplete_list
            available = True
        except ImportError:
            available = False

        if not available:
            self._highlight_syntax()
            return

        # Внутри строки/комментария — не показываем попап
        if self._is_in_string_or_comment():
            self.autocomplete.hide()
            self._highlight_syntax()
            return

        # Получаем текущее слово
        word, _ = self._get_current_word()

        if len(word) < 1:
            self.autocomplete.hide()
            self._highlight_syntax()
            return

        # Ищем кандидатов
        items = get_autocomplete_list(word)

        if not items:
            self.autocomplete.hide()
            self._highlight_syntax()
            return

        # ============================================================
        # Если набрано полное имя функции — попап скрыть.
        #
        # Например: набрано "sum" — попап не показываем.
        #           набрано "впр" — попап показываем (vlookup).
        # ============================================================
        if len(items) == 1 and items[0].lower() == word.lower():
            self.autocomplete.hide()
            self._highlight_syntax()
            return

        # ============================================================
        # Показываем попап со списком.
        #
        # Для алиаса "впр" попап покажет ["vlookup"] —
        # пользователь нажмёт Enter / Tab, и слово заменится.
        # ============================================================
        try:
            bbox = self.text.bbox(tk.INSERT)
            if bbox:
                x = bbox[0] + self.text.winfo_rootx()
                y = bbox[1] + bbox[3] + self.text.winfo_rooty()
                self.autocomplete.show(items, x, y)
        except Exception:
            pass

        self._highlight_syntax()

    # ============================================================
    # ВСТАВКА ИЗ АВТОДОПОЛНЕНИЯ
    # ============================================================
    def _on_tab(self, event):
        if self.autocomplete.is_visible():
            self._insert_autocomplete()
            return "break"
        self.text.insert(tk.INSERT, "    ")
        return "break"

    def _on_return(self, event):
        if self.autocomplete.is_visible():
            self._insert_autocomplete()
            return "break"
        return None

    def _on_escape(self, event):
        if self.autocomplete.is_visible():
            self.autocomplete.hide()
            return "break"
        return None

    def _on_arrow_up(self, event):
        if self.autocomplete.is_visible():
            self.autocomplete.move_selection(-1)
            return "break"
        return None

    def _on_arrow_down(self, event):
        if self.autocomplete.is_visible():
            self.autocomplete.move_selection(1)
            return "break"
        return None

    def _insert_autocomplete(self):
        """
        Вставляет выбранный пункт из попапа вместо набранного слова.

        Логика:
            - Слово "впр" → заменяется на "vlookup"
            - Слово "фильтр" → заменяется на "filterif"
            - Слово "sum" → ничего не меняется (уже sum)
        """
        selected = self.autocomplete.get_selected()
        if not selected:
            self.autocomplete.hide()
            return

        word, start_pos = self._get_current_word()
        if not start_pos:
            self.autocomplete.hide()
            return

        cursor = self.text.index(tk.INSERT)

        # Удаляем набранное слово
        self.text.delete(start_pos, cursor)

        # Вставляем выбранное имя функции
        self.text.insert(start_pos, selected)

        # Курсор — в конец вставленного
        new_col = int(start_pos.split('.')[1]) + len(selected)
        new_line = start_pos.split('.')[0]
        self.text.mark_set(tk.INSERT, f"{new_line}.{new_col}")

        self.autocomplete.hide()
        self._update_line_numbers()
        self._highlight_syntax()

        # Открыть справку по функции
        if self.on_word_clicked:
            try:
                self.on_word_clicked(selected)
            except Exception:
                pass

    # ============================================================
    # КЛИК ПО СЛОВУ — ОТКРЫТЬ СПРАВКУ
    # ============================================================
    def _on_click(self, event):
        if self.on_word_clicked:
            try:
                index = self.text.index(f"@{event.x},{event.y}")
                word = self._get_word_at(index)
                if word:
                    self.on_word_clicked(word)
            except Exception:
                pass

    def _get_word_at(self, index):
        try:
            line, col = index.split('.')
            col = int(col)
            line_text = self.text.get(f"{line}.0", f"{line}.end")

            start = col
            while start > 0 and (
                line_text[start - 1].isalnum()
                or line_text[start - 1] == '_'
            ):
                start -= 1

            end = col
            while end < len(line_text) and (
                line_text[end].isalnum()
                or line_text[end] == '_'
            ):
                end += 1

            return line_text[start:end]
        except Exception:
            return ""