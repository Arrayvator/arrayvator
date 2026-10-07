# ast_nodes/functions/report.py
"""
Отчёты ArrayVator — HTML с интерактивными графиками Plotly.

СИНТАКСИС:
    report("Название", "file.html")       # начать
    report_section("1. Статистика")        # секция
    report_text("Текст")                   # абзац
    report_table(m [, title "Таблица"])    # таблица
    report_chart(bar, x, y, title "...")   # график Plotly
    report_save([show])                    # сохранить HTML (show = открыть браузер)
    report_show()                          # открыть в браузере
    report_save_pdf("file.pdf")            # сохранить PDF (Playwright)

ПРАВИЛА:
    - report_save()         — первый вызов открывает браузер, дальше — только сохраняет.
    - report_save(false)    — только сохранить.
    - report_save(true)     — всегда открыть.
    - report_save_pdf()     — если Playwright нет, открывает HTML и подсказывает Ctrl+P.
"""

import os
import sys
import json
import uuid
import datetime
import html as html_module

from ..base import Node
from runtime.matrix import MatrExMatrix


# ============================================================
# ГЛОБАЛЬНЫЙ БУФЕР ОТЧЁТА
# ============================================================
_REPORT_STATE = {
    'title': None,
    'path': None,
    'sections': [],
    'saved_html': None,
    'opened_in_browser': False,   # ← новый флаг
}


def _reset_report():
    _REPORT_STATE['title'] = None
    _REPORT_STATE['path'] = None
    _REPORT_STATE['sections'] = []
    _REPORT_STATE['saved_html'] = None
    _REPORT_STATE['opened_in_browser'] = False


def _current_section():
    if not _REPORT_STATE['sections']:
        _REPORT_STATE['sections'].append({
            'title': None,
            'items': [],
        })
    return _REPORT_STATE['sections'][-1]


def _is_duckdb(val):
    try:
        from duckdb_engine import DuckDBTable
        return isinstance(val, DuckDBTable)
    except ImportError:
        return False


def _esc(text):
    if text is None:
        return ""
    return html_module.escape(str(text))


# ============================================================
# ИЗВЛЕЧЕНИЕ ДАННЫХ
# ============================================================
def _extract_column(node, env):
    """
    Извлекает столбец как список значений БЕЗ заголовка.

    ВАЖНО: для 1D-вектора заголовок УЖЕ отсечён IndexNode
    при срезе по имени. Не отсекаем повторно.
    """
    from ast_nodes.index import IndexNode

    if isinstance(node, IndexNode):
        obj = node.evaluate(env)

        if _is_duckdb(obj):
            try:
                rows = obj.query(f"SELECT * FROM {obj.table_name} LIMIT 10000")
                col_idx = 0
                if hasattr(node, 'indices') and len(node.indices) == 2:
                    col_spec_node = node.indices[1]
                    col_spec = (col_spec_node.evaluate(env)
                                if hasattr(col_spec_node, 'evaluate')
                                else col_spec_node)
                    from .filterif import _resolve_column_for_duckdb
                    columns = obj.get_columns()
                    col_idx = _resolve_column_for_duckdb(columns, col_spec)
                return [row[col_idx] for row in rows]
            except Exception:
                return []

        if hasattr(obj, 'data'):
            if obj.is_2d:
                # 2D-матрица без среза — отсекаем заголовок
                data = [row[0] if row else None for row in obj.data]
                if data and isinstance(data[0], str):
                    return data[1:]
                return data
            else:
                # 1D-вектор — заголовок уже отсечён
                return list(obj.data)

        if isinstance(obj, list):
            return obj

    obj = node.evaluate(env) if hasattr(node, 'evaluate') else node

    if _is_duckdb(obj):
        try:
            rows = obj.query(f"SELECT * FROM {obj.table_name} LIMIT 10000")
            return [row[0] if row else None for row in rows]
        except Exception:
            return []

    if hasattr(obj, 'data'):
        if obj.is_2d:
            data = [row[0] if row else None for row in obj.data]
            if data and isinstance(data[0], str):
                return data[1:]
            return data
        else:
            return list(obj.data)

    if isinstance(obj, list):
        return obj

    return [obj]


def _extract_matrix(node, env):
    """Извлекает матрицу (2D) с заголовком."""
    obj = node.evaluate(env) if hasattr(node, 'evaluate') else node

    if _is_duckdb(obj):
        try:
            rows = obj.query(f"SELECT * FROM {obj.table_name} LIMIT 1000")
            columns = obj.get_columns()
            return [list(columns)] + [list(r) for r in rows]
        except Exception:
            return []

    if hasattr(obj, 'data'):
        return [list(r) if isinstance(r, list) else [r] for r in obj.data]

    if isinstance(obj, list):
        return obj

    return [[obj]]


def _to_json(val):
    if hasattr(val, 'data'):
        val = list(val.data)
    if isinstance(val, list):
        result = []
        for v in val:
            if v is None:
                result.append(None)
            elif isinstance(v, (int, float, bool, str)):
                result.append(v)
            else:
                result.append(str(v))
        return json.dumps(result, ensure_ascii=False)
    return json.dumps(val, ensure_ascii=False)


# ============================================================
# HTML-РЕНДЕР ТАБЛИЦЫ
# ============================================================
def _render_table_html(data, title=None):
    if not data:
        return '<p class="text-muted">Пустая таблица</p>'

    result = []
    if title:
        result.append(f'<h5 class="mt-3">{_esc(title)}</h5>')

    result.append('<div class="table-responsive">')
    result.append('<table class="table table-striped table-hover table-sm">')

    result.append('<thead class="table-dark"><tr>')
    for cell in data[0]:
        result.append(f'<th>{_esc(cell)}</th>')
    result.append('</tr></thead>')

    result.append('<tbody>')
    for row in data[1:]:
        result.append('<tr>')
        for cell in row:
            if cell is None:
                result.append('<td class="text-muted"><i>None</i></td>')
            else:
                result.append(f'<td>{_esc(cell)}</td>')
        result.append('</tr>')
    result.append('</tbody>')

    result.append('</table></div>')
    return "\n".join(result)


# ============================================================
# PLOTLY-ГРАФИК В ОТЧЁТЕ
# ============================================================
def _render_plotly_chart(kind, x, y, options):
    """
    Строит HTML-блок с Plotly для одного графика.

    Поддерживает ВСЕ типы:
        bar, line, pie, hist, scatter, box,
        heatmap, pair
    """
    div_id = f"plot_{uuid.uuid4().hex[:8]}"

    title = options.get('title', '')
    xlabel = options.get('xlabel', '')
    ylabel = options.get('ylabel', '')
    color = options.get('color', None)
    bins = options.get('bins', 10)

    x_json = _to_json(x)
    y_json = _to_json(y) if y is not None else "null"

    # ============================================================
    # HEATMAP
    # ============================================================
    if kind == 'heatmap':
        z_json = _to_json(x)
        trace = f"""
            {{
                z: {z_json},
                type: 'heatmap',
                colorscale: 'Viridis'
            }}
        """

    # ============================================================
    # PAIR — матрица зависимостей
    # ============================================================
    elif kind == 'pair':
        matrix = x
        if not matrix or not isinstance(matrix, list) or len(matrix) < 1:
            matrix = []
        n_cols = len(matrix[0]) if matrix else 0
        if n_cols < 2:
            # Фоллбэк: пустая гистограмма
            trace = "{ x: [], type: 'histogram' }"
        else:
            cols = []
            for j in range(n_cols):
                col_data = []
                for row in matrix:
                    if j < len(row):
                        try:
                            col_data.append(float(row[j]))
                        except (ValueError, TypeError):
                            col_data.append(0.0)
                    else:
                        col_data.append(0.0)
                cols.append(col_data)

            traces = []
            for i in range(n_cols):
                for j in range(n_cols):
                    if i == j:
                        traces.append(
                            f"{{ x: {json.dumps(cols[i])}, "
                            f"type: 'histogram', showlegend: false, "
                            f"xaxis: 'x{ i*n_cols+j+1 if i*n_cols+j > 0 else '' }', "
                            f"yaxis: 'y{ i*n_cols+j+1 if i*n_cols+j > 0 else '' }' }}"
                        )
                    else:
                        traces.append(
                            f"{{ x: {json.dumps(cols[j])}, "
                            f"y: {json.dumps(cols[i])}, "
                            f"mode: 'markers', "
                            f"marker: {{size: 4, opacity: 0.5}}, "
                            f"showlegend: false, "
                            f"xaxis: 'x{ i*n_cols+j+1 if i*n_cols+j > 0 else '' }', "
                            f"yaxis: 'y{ i*n_cols+j+1 if i*n_cols+j > 0 else '' }' }}"
                        )

            # Сетка n×n
            grid = []
            for i in range(n_cols):
                for j in range(n_cols):
                    idx = i * n_cols + j + 1
                    domain_x0 = j / n_cols
                    domain_x1 = (j + 1) / n_cols - 0.02
                    domain_y0 = 1 - (i + 1) / n_cols
                    domain_y1 = 1 - i / n_cols - 0.02

                    grid.append(f"""
                        {{
                            title: '',
                            domain: {{x: [{domain_x0}, {domain_x1}], y: [{domain_y0}, {domain_y1}]}},
                            showticklabels: {'true' if i == n_cols - 1 else 'false'},
                            showgrid: true,
                            zeroline: false
                        }}
                    """)

            layout_extra = f"""
                grid: {{rows: {n_cols}, columns: {n_cols}, pattern: 'independent'}},
                xaxis: {{}}, 
                yaxis: {{}},
                height: {300 * n_cols},
                showlegend: false,
            """

            return f"""
            <div id="{div_id}" class="report-chart"></div>
            <script>
            (function() {{
                var traces = [{','.join(traces)}];
                var layout = {{
                    title: {repr(title)},
                    {layout_extra}
                    margin: {{ t: 50, b: 50, l: 60, r: 30 }},
                    annotations: []
                }};
                Plotly.newPlot("{div_id}", traces, layout, {{responsive: true}});
            }})();
            </script>
            """

    # ============================================================
    # BAR
    # ============================================================
    elif kind == 'bar':
        trace = f"""
            {{
                x: {x_json},
                y: {y_json},
                type: 'bar',
                marker: {{color: {repr(color) if color else "'#4a90d9'"}}}
            }}
        """

    # ============================================================
    # LINE
    # ============================================================
    elif kind == 'line':
        trace = f"""
            {{
                x: {x_json},
                y: {y_json},
                type: 'scatter',
                mode: 'lines+markers',
                line: {{color: {repr(color) if color else "'#27ae60'"}}}
            }}
        """

    # ============================================================
    # PIE
    # ============================================================
    elif kind == 'pie':
        trace = f"""
            {{
                labels: {x_json},
                values: {y_json},
                type: 'pie'
            }}
        """

    # ============================================================
    # HIST — с bins
    # ============================================================
    elif kind == 'hist':
        try:
            nbinsx = int(bins) if bins else 10
        except (ValueError, TypeError):
            nbinsx = 10

        trace = f"""
            {{
                x: {x_json},
                type: 'histogram',
                nbinsx: {nbinsx},
                marker: {{color: {repr(color) if color else "'#e67e22'"}}}
            }}
        """

    # ============================================================
    # SCATTER
    # ============================================================
    elif kind == 'scatter':
        trace = f"""
            {{
                x: {x_json},
                y: {y_json},
                mode: 'markers',
                type: 'scatter',
                marker: {{color: {repr(color) if color else "'#8e44ad'"}}}
            }}
        """

    # ============================================================
    # BOX
    # ============================================================
    elif kind == 'box':
        trace = f"""
            {{
                y: {y_json},
                x: {x_json},
                type: 'box'
            }}
        """

    # ============================================================
    # Неизвестный тип — bar по умолчанию
    # ============================================================
    else:
        trace = f"""
            {{
                x: {x_json},
                y: {y_json},
                type: 'bar'
            }}
        """

    layout = f"""
        {{
            title: {repr(title)},
            xaxis: {{ title: {repr(xlabel)} }},
            yaxis: {{ title: {repr(ylabel)} }},
            margin: {{ t: 50, b: 50, l: 60, r: 30 }},
            height: 450
        }}
    """

    return f"""
    <div id="{div_id}" class="report-chart"></div>
    <script>
    (function() {{
        var trace = {trace};
        var layout = {layout};
        Plotly.newPlot("{div_id}", [trace], layout, {{responsive: true}});
    }})();
    </script>
    """


# ============================================================
# СБОРКА HTML ОТЧЁТА
# ============================================================
def _render_report_html():
    title = _REPORT_STATE['title'] or "Отчёт"
    now = datetime.datetime.now().strftime("%d.%m.%Y %H:%M")

    parts = []

    parts.append(f"""<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{_esc(title)}</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <script src="https://cdn.plot.ly/plotly-2.27.0.min.js"></script>
    <style>
        body {{ font-family: 'Segoe UI', Tahoma, sans-serif; background: #f8f9fa; padding: 30px 0; }}
        .report-container {{ max-width: 1000px; margin: 0 auto; background: white; padding: 40px 50px; border-radius: 8px; box-shadow: 0 2px 15px rgba(0,0,0,0.08); }}
        .report-title {{ color: #2c3e50; border-bottom: 3px solid #3498db; padding-bottom: 15px; margin-bottom: 10px; }}
        .report-meta {{ color: #7f8c8d; font-size: 0.9em; margin-bottom: 30px; }}
        .report-section {{ margin-top: 40px; margin-bottom: 25px; }}
        .report-section h3 {{ color: #34495e; border-left: 5px solid #3498db; padding-left: 15px; padding-bottom: 5px; }}
        .report-text {{ font-size: 1.05em; line-height: 1.6; color: #2c3e50; margin: 15px 0; }}
        .report-chart {{ margin: 20px 0; padding: 10px; background: #fff; border: 1px solid #e9ecef; border-radius: 5px; }}
        .report-footer {{ margin-top: 50px; padding-top: 20px; border-top: 1px solid #dee2e6; text-align: center; color: #95a5a6; font-size: 0.85em; }}
        @media print {{
            body {{ background: white; padding: 0; }}
            .report-container {{ box-shadow: none; padding: 20px; }}
            .no-print {{ display: none !important; }}
        }}
        .floating-btn {{
            position: fixed; top: 20px; right: 20px; z-index: 1000;
            background: #27ae60; color: white; border: none;
            padding: 12px 20px; border-radius: 6px;
            font-size: 14px; font-weight: bold; cursor: pointer;
            box-shadow: 0 4px 12px rgba(0,0,0,0.15);
        }}
        .floating-btn:hover {{ background: #219150; }}
    </style>
</head>
<body>
<button class="floating-btn no-print" onclick="window.print()">🖨 Сохранить в PDF (Ctrl+P)</button>
<div class="report-container">
    <h1 class="report-title">{_esc(title)}</h1>
    <div class="report-meta">
        Дата создания: {now}
    </div>
""")

    for section in _REPORT_STATE['sections']:
        if section['title']:
            parts.append(f'<div class="report-section">')
            parts.append(f'<h3>{_esc(section["title"])}</h3>')
            parts.append('</div>')

        for item in section['items']:
            parts.append(item)

    parts.append(f"""
    <div class="report-footer">
        Отчёт создан в ArrayVator — {now}
    </div>
</div>
</body>
</html>
""")

    return "\n".join(parts)


# ============================================================
# ОТКРЫТИЕ БРАУЗЕРА
# ============================================================
def _open_in_browser(path):
    if not os.path.exists(path):
        raise FileNotFoundError(f"Файл не найден: {path}")

    try:
        if sys.platform == 'win32':
            os.startfile(os.path.abspath(path))
        elif sys.platform == 'darwin':
            import subprocess
            subprocess.Popen(['open', path])
        else:
            import subprocess
            subprocess.Popen(['xdg-open', path])
        return True
    except Exception:
        return False


# ============================================================
# PDF ЧЕРЕЗ PLAYWRIGHT
# ============================================================
def _save_pdf_playwright(html_path, pdf_path):
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        return False, (
            "Playwright не установлен.\n"
            "  Установите: pip install playwright\n"
            "  Затем:      python -m playwright install chromium"
        )

    try:
        abs_html = os.path.abspath(html_path)
        if sys.platform == 'win32':
            url = 'file:///' + abs_html.replace('\\', '/')
        else:
            url = 'file://' + abs_html

        with sync_playwright() as p:
            browser = p.chromium.launch()
            page = browser.new_page()
            page.goto(url, wait_until='networkidle')
            page.wait_for_timeout(2000)
            page.pdf(
                path=os.path.abspath(pdf_path),
                format='A4',
                print_background=True,
                margin={'top': '15mm', 'bottom': '15mm',
                        'left': '15mm', 'right': '15mm'},
            )
            browser.close()

        return True, f"PDF сохранён: {pdf_path}"

    except Exception as e:
        return False, f"Ошибка Playwright: {e}"


# ============================================================
# REPORT
# ============================================================
class ReportNode(Node):
    def __init__(self, title, path):
        self.title = title
        self.path = path

    def evaluate(self, env):
        title = (self.title.evaluate(env)
                 if hasattr(self.title, 'evaluate') else self.title)
        path = (self.path.evaluate(env)
                if hasattr(self.path, 'evaluate') else self.path)

        if not isinstance(title, str):
            raise TypeError(f"report: название должно быть строкой")
        if not isinstance(path, str):
            raise TypeError(f"report: путь должен быть строкой")

        _reset_report()
        _REPORT_STATE['title'] = title
        _REPORT_STATE['path'] = path

        return f"Отчёт '{title}' начат: {path}"

    def __repr__(self):
        return f"report({self.title}, {self.path})"


# ============================================================
# REPORT_SECTION
# ============================================================
class ReportSectionNode(Node):
    def __init__(self, title):
        self.title = title

    def evaluate(self, env):
        title = (self.title.evaluate(env)
                 if hasattr(self.title, 'evaluate') else self.title)
        if not isinstance(title, str):
            raise TypeError(f"report_section: заголовок должен быть строкой")

        _REPORT_STATE['sections'].append({
            'title': title,
            'items': [],
        })
        return f"Секция '{title}' добавлена"

    def __repr__(self):
        return f"report_section({self.title})"


# ============================================================
# REPORT_TEXT
# ============================================================
class ReportTextNode(Node):
    def __init__(self, text):
        self.text = text

    def evaluate(self, env):
        text = (self.text.evaluate(env)
                if hasattr(self.text, 'evaluate') else self.text)
        if not isinstance(text, str):
            text = str(text)

        section = _current_section()
        section['items'].append(
            f'<p class="report-text">{_esc(text)}</p>'
        )
        return "Текст добавлен"

    def __repr__(self):
        return f"report_text({self.text})"


# ============================================================
# REPORT_TABLE
# ============================================================
class ReportTableNode(Node):
    def __init__(self, data, title=None):
        self.data = data
        self.title = title

    def evaluate(self, env):
        data = _extract_matrix(self.data, env)

        title_val = None
        if self.title is not None:
            title_val = (self.title.evaluate(env)
                         if hasattr(self.title, 'evaluate')
                         else self.title)

        section = _current_section()
        section['items'].append(_render_table_html(data, title_val))
        return f"Таблица добавлена ({len(data)} строк)"

    def __repr__(self):
        return f"report_table({self.data})"


# ============================================================
# REPORT_CHART
# ============================================================
class ReportChartNode(Node):
    def __init__(self, kind, x, y=None, options=None):
        self.kind = kind
        self.x = x
        self.y = y
        self.options = options or {}

    def evaluate(self, env):
        kind = (self.kind.evaluate(env)
                if hasattr(self.kind, 'evaluate') else self.kind)
        if not isinstance(kind, str):
            raise TypeError(f"report_chart: тип графика должен быть строкой")
        kind = kind.lower()

        # Для heatmap и pair — X это матрица
        if kind in ('heatmap', 'pair'):
            matrix_obj = (self.x.evaluate(env)
                          if hasattr(self.x, 'evaluate')
                          else self.x)
            if _is_duckdb(matrix_obj):
                try:
                    rows = matrix_obj.query(
                        f"SELECT * FROM {matrix_obj.table_name} LIMIT 1000"
                    )
                    x_data = [list(r) for r in rows]
                except Exception:
                    x_data = []
            elif hasattr(matrix_obj, 'data'):
                x_data = [list(r) if isinstance(r, list) else [r]
                          for r in matrix_obj.data]
            else:
                x_data = matrix_obj
            y_data = None
        else:
            x_data = _extract_column(self.x, env)
            y_data = _extract_column(self.y, env) if self.y is not None else None

        opts = {}
        for k, v in self.options.items():
            val = v.evaluate(env) if hasattr(v, 'evaluate') else v
            opts[k] = val

        section = _current_section()
        section['items'].append(
            _render_plotly_chart(kind, x_data, y_data, opts)
        )
        return f"График '{kind}' добавлен"

    def __repr__(self):
        return f"report_chart({self.kind}, ...)"


# ============================================================
# REPORT_SAVE (с автооткрытием)
# ============================================================
class ReportSaveNode(Node):
    def __init__(self, show=None):
        self.show = show

    def evaluate(self, env):
        path = _REPORT_STATE.get('path')
        if not path:
            raise RuntimeError(
                "report_save: отчёт не начат.\n"
                "  Сначала вызовите report(\"Название\", \"file.html\")"
            )

        html_content = _render_report_html()

        folder = os.path.dirname(os.path.abspath(path))
        if folder and not os.path.exists(folder):
            os.makedirs(folder, exist_ok=True)

        with open(path, 'w', encoding='utf-8') as f:
            f.write(html_content)

        _REPORT_STATE['saved_html'] = os.path.abspath(path)

        title = _REPORT_STATE.get('title') or "Отчёт"

        # ============================================================
        # Явный аргумент
        # ============================================================
        if self.show is not None:
            show_val = (self.show.evaluate(env)
                        if hasattr(self.show, 'evaluate') else self.show)
            if isinstance(show_val, str):
                show_val = show_val.lower() in ('true', 'yes', '1')
            explicit = bool(show_val)

            if explicit:
                _open_in_browser(path)
                return f"Отчёт '{title}' сохранён и открыт: {path}"
            return f"Отчёт '{title}' сохранён: {path}"

        # ============================================================
        # Авто-логика: первый вызов открывает
        # ============================================================
        if not _REPORT_STATE.get('opened_in_browser'):
            _REPORT_STATE['opened_in_browser'] = True
            _open_in_browser(path)
            return f"Отчёт '{title}' сохранён и открыт: {path}"

        return f"Отчёт '{title}' сохранён: {path}"

    def __repr__(self):
        if self.show is not None:
            return f"report_save({self.show})"
        return "report_save()"


# ============================================================
# REPORT_SHOW
# ============================================================
class ReportShowNode(Node):
    def __init__(self):
        pass

    def evaluate(self, env):
        saved = _REPORT_STATE.get('saved_html')
        if saved and os.path.exists(saved):
            ok = _open_in_browser(saved)
            if ok:
                return f"Отчёт открыт: {saved}"
            return f"Не удалось открыть: {saved}"

        path = _REPORT_STATE.get('path')
        if not path:
            raise RuntimeError(
                "report_show: отчёт не начат.\n"
                "  Сначала вызовите report(...)"
            )

        html_content = _render_report_html()
        with open(path, 'w', encoding='utf-8') as f:
            f.write(html_content)

        _REPORT_STATE['saved_html'] = os.path.abspath(path)
        _open_in_browser(path)

        return f"Отчёт открыт: {path}"

    def __repr__(self):
        return "report_show()"


# ============================================================
# REPORT_SAVE_PDF
# ============================================================
class ReportSavePdfNode(Node):
    def __init__(self, pdf_path):
        self.pdf_path = pdf_path

    def evaluate(self, env):
        html_path = _REPORT_STATE.get('saved_html')

        if not html_path or not os.path.exists(html_path):
            html_path = _REPORT_STATE.get('path')
            if not html_path:
                raise RuntimeError(
                    "report_save_pdf: отчёт не начат.\n"
                    "  Сначала вызовите report(...) и report_save()"
                )

            html_content = _render_report_html()
            with open(html_path, 'w', encoding='utf-8') as f:
                f.write(html_content)
            _REPORT_STATE['saved_html'] = os.path.abspath(html_path)

        pdf_path = (self.pdf_path.evaluate(env)
                    if hasattr(self.pdf_path, 'evaluate')
                    else self.pdf_path)
        if not isinstance(pdf_path, str):
            raise TypeError("report_save_pdf: путь должен быть строкой")

        ok, msg = _save_pdf_playwright(html_path, pdf_path)

        if ok:
            return msg

        _open_in_browser(html_path)

        return (
            f"{msg}\n"
            f"  Открыт HTML в браузере: {html_path}\n"
            f"  Сохраните PDF вручную: Ctrl+P → «Сохранить как PDF»"
        )

    def __repr__(self):
        return f"report_save_pdf({self.pdf_path})"