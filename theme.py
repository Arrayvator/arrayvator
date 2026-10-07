# theme.py
"""
Темы оформления для ArrayVator Editor / Compiler.

Тёмная:  DARK
Светлая: LIGHT (по умолчанию)

Категории подсветки:
    keyword   — условные операторы (if, then, for, while, ...)
    function  — функции (sum, filterif, groupby, ...)
    variable  — переменные (m, x, total, ...)  ← новая категория
    string    — текст в кавычках
    number    — числа
    comment   — комментарии
    operator  — операторы (==, and, or)
"""


# ============================================================
# ТЁМНАЯ ТЕМА
# ============================================================
DARK = {
    'bg':            '#0d1117',
    'bg_alt':        '#161b22',
    'bg_card':       '#1c2128',
    'bg_code':       '#10141a',
    'bg_hover':      '#21262d',
    'bg_select':     '#264f78',

    'border':        '#30363d',
    'border_hover':  '#8b949e',

    'text':          '#c9d1d9',
    'text_dim':      '#8b949e',
    'text_muted':    '#6e7681',
    'text_inverse':  '#ffffff',

    'accent':        '#58a6ff',
    'accent_2':      '#1f6feb',
    'accent_hover':  '#388bfd',
    'green':         '#3fb950',
    'yellow':        '#d29922',
    'red':           '#f85149',
    'purple':        '#bc8cff',
    'cyan':          '#79c0ff',

    # Синтаксис — дефолт для тёмной
    'syntax_keyword':  '#ff7b72',
    'syntax_function': '#d2a8ff',
    'syntax_variable': '#c9d1d9',
    'syntax_string':   '#a5d6ff',
    'syntax_number':   '#79c0ff',
    'syntax_comment':  '#8b949e',
    'syntax_operator': '#ff7b72',

    # Консоль
    'console_bg':   '#0d1117',
    'console_fg':   '#c9d1d9',
    'console_err':  '#f85149',
    'console_ok':   '#3fb950',
    'console_warn': '#d29922',
    'console_info': '#79c0ff',
    'console_hint': '#d29922',
    'console_dim':  '#6e7681',
}


# ============================================================
# СВЕТЛАЯ ТЕМА (по умолчанию)
# ============================================================
LIGHT = {
    'bg':            '#f5f5f5',
    'bg_alt':        '#ffffff',
    'bg_card':       '#ffffff',
    'bg_code':       '#ffffff',
    'bg_hover':      '#eaeaea',
    'bg_select':     '#cce8ff',

    'border':        '#d0d0d0',
    'border_hover':  '#909090',

    'text':          '#1a1a1a',
    'text_dim':      '#555555',
    'text_muted':    '#808080',
    'text_inverse':  '#ffffff',

    'accent':        '#0066cc',
    'accent_2':      '#0078d4',
    'accent_hover':  '#1a86e0',
    'green':         '#27ae60',
    'yellow':        '#d29922',
    'red':           '#e74c3c',
    'purple':        '#8e44ad',
    'cyan':          '#0086b3',

    # Синтаксис — дефолт для светлой (по твоему запросу)
    'syntax_keyword':  '#000000',   # условные — чёрный
    'syntax_function': '#996600',   # функции — тёмно-коричневый
    'syntax_variable': '#000000',   # переменные — чёрный
    'syntax_string':   '#006600',   # строки — тёмно-зелёный
    'syntax_number':   '#0000CC',   # числа — синий
    'syntax_comment':  '#808080',   # комментарии — серый
    'syntax_operator': '#CC00CC',   # операторы — пурпурный

    # Консоль
    'console_bg':   '#1e1e1e',
    'console_fg':   '#d4d4d4',
    'console_err':  '#ff6b6b',
    'console_ok':   '#90ee90',
    'console_warn': '#ffd700',
    'console_info': '#87ceeb',
    'console_hint': '#ffd700',
    'console_dim':  '#808080',
}


# ============================================================
# ДЕФОЛТНЫЕ СТИЛИ (жирный/курсив)
# ============================================================
DEFAULT_STYLES_LIGHT = {
    'keyword':  {'bold': True,  'italic': False},   # условные — жирные
    'function': {'bold': False, 'italic': False},
    'variable': {'bold': True,  'italic': False},   # переменные — жирные
    'string':   {'bold': False, 'italic': False},
    'number':   {'bold': False, 'italic': False},
    'comment':  {'bold': False, 'italic': True},    # комментарии — курсив
    'operator': {'bold': False, 'italic': False},
}

DEFAULT_STYLES_DARK = {
    'keyword':  {'bold': True,  'italic': False},
    'function': {'bold': False, 'italic': False},
    'variable': {'bold': False, 'italic': False},
    'string':   {'bold': False, 'italic': False},
    'number':   {'bold': False, 'italic': False},
    'comment':  {'bold': False, 'italic': True},
    'operator': {'bold': False, 'italic': False},
}


# ============================================================
# ПОЛУЧИТЬ ТЕМУ
# ============================================================
def get_theme(name='light'):
    if name == 'dark':
        return dict(DARK)
    return dict(LIGHT)


# ============================================================
# ПОЛУЧИТЬ ПАЛИТРУ СИНТАКСИСА
# ============================================================
def get_syntax_palette(theme_name, user_settings=None):
    """
    Возвращает палитру синтаксиса: цвет, bold, italic для каждой категории.

    Категории: keyword, function, variable, string, number, comment, operator
    """
    theme = get_theme(theme_name)
    default_styles = (DEFAULT_STYLES_DARK if theme_name == 'dark'
                      else DEFAULT_STYLES_LIGHT)

    default = {}
    for key in ('keyword', 'function', 'variable', 'string',
                'number', 'comment', 'operator'):
        default[key] = {
            'color':  theme[f'syntax_{key}'],
            'bold':   default_styles[key]['bold'],
            'italic': default_styles[key]['italic'],
        }

    if user_settings:
        for key, val in user_settings.items():
            if key in default and isinstance(val, dict):
                if 'color' in val:
                    default[key]['color'] = val['color']
                if 'bold' in val:
                    default[key]['bold'] = bool(val['bold'])
                if 'italic' in val:
                    default[key]['italic'] = bool(val['italic'])

    return default


# ============================================================
# ХЕЛПЕР: КНОПКА С ХОВЕРОМ
# ============================================================
def make_button(parent, text, command, theme, *,
                variant='ghost', width=None, font=None):
    import tkinter as tk

    if variant == 'primary':
        bg = theme['accent_2']
        bg_hover = theme['accent_hover']
        fg = theme['text_inverse']
        border = theme['accent_2']
    elif variant == 'danger':
        bg = theme['red']
        bg_hover = '#ff6b6b'
        fg = theme['text_inverse']
        border = theme['red']
    else:
        bg = theme['bg_card']
        bg_hover = theme['bg_hover']
        fg = theme['text']
        border = theme['border']

    if font is None:
        font = ("Segoe UI", 10)

    btn = tk.Label(
        parent, text=text, bg=bg, fg=fg, font=font,
        padx=14, pady=7, cursor="hand2",
        bd=1, relief="solid",
        highlightthickness=1,
        highlightbackground=border,
        highlightcolor=border,
    )

    if width:
        btn.config(width=width)

    def on_enter(_): btn.config(bg=bg_hover)
    def on_leave(_): btn.config(bg=bg)
    def on_click(_):
        try: command()
        except Exception: pass

    btn.bind("<Enter>", on_enter)
    btn.bind("<Leave>", on_leave)
    btn.bind("<Button-1>", on_click)
    return btn


# ============================================================
# ХЕЛПЕР: РАЗДЕЛИТЕЛЬ
# ============================================================
def make_separator(parent, theme, orient='horizontal', length=None):
    import tkinter as tk

    if orient == 'horizontal':
        sep = tk.Frame(parent, bg=theme['border'], height=1)
        if length:
            sep.config(width=length)
    else:
        sep = tk.Frame(parent, bg=theme['border'], width=1)
        if length:
            sep.config(height=length)
    return sep


# ============================================================
# ХЕЛПЕР: КАРТОЧКА
# ============================================================
def make_card(parent, theme, **kwargs):
    import tkinter as tk

    return tk.Frame(
        parent,
        bg=theme['bg_card'],
        bd=1, relief="solid",
        highlightthickness=1,
        highlightbackground=theme['border'],
        highlightcolor=theme['border'],
        **kwargs,
    )