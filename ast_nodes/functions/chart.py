# ast_nodes/functions/chart.py
"""
Функция CHART — построение графиков и диаграмм.

ПОДДЕРЖКА:
    - Matrix (RAM)
    - DuckDB (BigData) — через ToMatrix или sample

ТИПЫ ГРАФИКОВ:
    bar      — столбчатая
    line     — линейная
    pie      — круговая
    hist     — гистограмма
    scatter  — точки
    box      — ящик с усами
    heatmap  — тепловая карта
    pair     — парные зависимости

ПОКАЗ:
    - Окно Tkinter с toolbar (кнопка Сохранить)
    - Правый клик → контекстное меню (PNG, PDF, SVG, JPG)
    - Опция save "file.png" — автосохранение

PLOTLY:
    - Все типы поддерживаются.
    - heatmap и pair — через plotly.graph_objects + make_subplots.

ВАЖНО:
    _extract_column НЕ отсекает заголовок для 1D-вектора —
    это уже сделал IndexNode при срезе по имени.
"""

import os
import tkinter as tk
from tkinter import filedialog, messagebox

from ..base import Node
from runtime.matrix import MatrExMatrix


def _is_duckdb(val):
    try:
        from duckdb_engine import DuckDBTable
        return isinstance(val, DuckDBTable)
    except ImportError:
        return False


# ============================================================
# ИЗВЛЕЧЕНИЕ ДАННЫХ
# ============================================================
def _extract_column(node, env):
    """
    Извлекает столбец как список значений БЕЗ заголовка.

    ВАЖНО:
        Если node — IndexNode вида m[:, "X"], то IndexNode УЖЕ
        отсекает заголовок (при срезе по имени) и возвращает вектор
        только с данными. Поэтому для 1D-вектора НЕ отсекаем
        ничего повторно.

        Если node — целая матрица (2D), отсекаем первую строку,
        если она похожа на заголовок (первое значение — строка).
    """
    from ast_nodes.index import IndexNode

    if isinstance(node, IndexNode):
        obj = node.evaluate(env)

        # -----------------------------------------------------
        # DuckDB
        # -----------------------------------------------------
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

        # -----------------------------------------------------
        # MatrExMatrix
        # -----------------------------------------------------
        if hasattr(obj, 'data'):
            if obj.is_2d:
                # 2D-матрица без среза → отсекаем заголовок
                data = [row[0] if row else None for row in obj.data]
                if data and isinstance(data[0], str):
                    return data[1:]
                return data
            else:
                # 1D-вектор → заголовок УЖЕ отсечён IndexNode
                return list(obj.data)

        if isinstance(obj, list):
            return obj

    # ---------------------------------------------------------
    # Не IndexNode — вычисляем как есть
    # ---------------------------------------------------------
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


# ============================================================
# ПОСТРОЕНИЕ FIGURE (matplotlib)
# ============================================================
def _build_figure(kind, x, y, options):
    """Строит Figure и возвращает его."""
    try:
        import matplotlib
        matplotlib.use('TkAgg')
        from matplotlib.figure import Figure
    except ImportError:
        raise ImportError(
            "matplotlib не установлен.\n"
            "Установите: pip install matplotlib"
        )

    title = options.get('title')
    xlabel = options.get('xlabel')
    ylabel = options.get('ylabel')
    color = options.get('color')
    bins = options.get('bins', 10)

    fig = Figure(figsize=(10, 6), dpi=100)
    ax = fig.add_subplot(111)

    # BAR
    if kind == 'bar':
        labels = [str(v) for v in x]
        values = []
        for v in y:
            try:
                values.append(float(v))
            except (ValueError, TypeError):
                values.append(0.0)
        ax.bar(labels, values, color=color)
        if xlabel: ax.set_xlabel(xlabel)
        if ylabel: ax.set_ylabel(ylabel)
        if title: ax.set_title(title)

    # LINE
    elif kind == 'line':
        labels = [str(v) for v in x]
        values = []
        for v in y:
            try:
                values.append(float(v))
            except (ValueError, TypeError):
                values.append(0.0)
        ax.plot(labels, values, marker='o', color=color)
        if xlabel: ax.set_xlabel(xlabel)
        if ylabel: ax.set_ylabel(ylabel)
        if title: ax.set_title(title)
        ax.grid(True, alpha=0.3)

    # PIE
    elif kind == 'pie':
        labels = [str(v) for v in x]
        values = []
        for v in y:
            try:
                values.append(float(v))
            except (ValueError, TypeError):
                values.append(0.0)
        ax.pie(values, labels=labels, autopct='%1.1f%%', startangle=90)
        ax.axis('equal')
        if title: ax.set_title(title)

    # HIST
    elif kind == 'hist':
        values = []
        for v in x:
            try:
                values.append(float(v))
            except (ValueError, TypeError):
                continue
        ax.hist(values, bins=bins, color=color, edgecolor='black')
        if xlabel: ax.set_xlabel(xlabel)
        if ylabel: ax.set_ylabel(ylabel)
        if title: ax.set_title(title)
        ax.grid(True, alpha=0.3)

    # SCATTER
    elif kind == 'scatter':
        xs = []
        ys = []
        for a, b in zip(x, y):
            try:
                xs.append(float(a))
                ys.append(float(b))
            except (ValueError, TypeError):
                continue
        ax.scatter(xs, ys, color=color)
        if xlabel: ax.set_xlabel(xlabel)
        if ylabel: ax.set_ylabel(ylabel)
        if title: ax.set_title(title)
        ax.grid(True, alpha=0.3)

    # BOX
    elif kind == 'box':
        groups = {}
        for k, v in zip(x, y):
            try:
                groups.setdefault(str(k), []).append(float(v))
            except (ValueError, TypeError):
                continue
        labels = list(groups.keys())
        data = [groups[k] for k in labels]
        ax.boxplot(data, labels=labels)
        if xlabel: ax.set_xlabel(xlabel)
        if ylabel: ax.set_ylabel(ylabel)
        if title: ax.set_title(title)

    # HEATMAP
    elif kind == 'heatmap':
        matrix = x
        if not matrix:
            raise ValueError("heatmap: нужна матрица")
        data_2d = []
        for row in matrix:
            row_nums = []
            for v in row:
                try:
                    row_nums.append(float(v))
                except (ValueError, TypeError):
                    row_nums.append(0.0)
            data_2d.append(row_nums)
        im = ax.imshow(data_2d, cmap='viridis', aspect='auto')
        fig.colorbar(im, ax=ax)
        if title: ax.set_title(title)

    # PAIR
    elif kind == 'pair':
        matrix = x
        if not matrix or len(matrix) < 1:
            raise ValueError("pair: нужна матрица с данными")
        n_cols = len(matrix[0]) if matrix else 0
        if n_cols < 2:
            raise ValueError("pair: нужно минимум 2 столбца")
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

        fig.clear()
        n = n_cols
        for i in range(n):
            for j in range(n):
                ax_ij = fig.add_subplot(n, n, i * n + j + 1)
                if i == j:
                    ax_ij.hist(cols[i], bins=10, edgecolor='black')
                else:
                    ax_ij.scatter(cols[j], cols[i], s=5, alpha=0.5)
        if title:
            fig.suptitle(title)

    else:
        raise ValueError(f"chart: неизвестный тип '{kind}'")

    fig.tight_layout()
    return fig


# ============================================================
# ПОКАЗ В TKINTER С TOOLBAR И МЕНЮ
# ============================================================
def _show_figure(fig, title=None, auto_save=None):
    """
    Показывает Figure в Tkinter-окне:
      - toolbar (кнопка Сохранить)
      - правый клик → контекстное меню (PNG, PDF, SVG, JPG)
      - автосохранение (если задано auto_save)
    """
    from matplotlib.backends.backend_tkagg import (
        FigureCanvasTkAgg,
        NavigationToolbar2Tk,
    )

    result = {"msg": f"График '{title}' построен." if title else "График построен."}

    # Автосохранение
    if auto_save:
        try:
            fig.savefig(auto_save, dpi=100, bbox_inches='tight')
            result["msg"] += f" Сохранён: {auto_save}"
        except Exception as e:
            result["msg"] += f" Ошибка автосохранения: {e}"

    # ============================================================
    # TKINTER ОКНО
    # ============================================================
    root = tk.Tk()
    root.title(f"График: {title}" if title else "График ArrayVator")
    root.geometry("1000x750")

    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas.draw()
    canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    # Toolbar (включает кнопку Сохранить)
    toolbar = NavigationToolbar2Tk(canvas, root)
    toolbar.update()
    toolbar.pack(side=tk.BOTTOM, fill=tk.X)

    # ============================================================
    # КОНТЕКСТНОЕ МЕНЮ (правый клик)
    # ============================================================
    def save_as(fmt):
        """Диалог сохранения в выбранном формате."""
        ext_map = {
            'png': ".png",
            'pdf': ".pdf",
            'svg': ".svg",
            'jpg': ".jpg",
        }
        default_ext = ext_map.get(fmt, ".png")

        default_name = (title or "chart")
        for ch in '<>:"/\\|?*':
            default_name = default_name.replace(ch, '_')

        filetypes_map = {
            'png': [("PNG image", "*.png")],
            'pdf': [("PDF document", "*.pdf")],
            'svg': [("SVG image", "*.svg")],
            'jpg': [("JPEG image", "*.jpg")],
        }

        path = filedialog.asksaveasfilename(
            parent=root,
            title=f"Сохранить как {fmt.upper()}",
            defaultextension=default_ext,
            initialfile=default_name + default_ext,
            filetypes=filetypes_map.get(fmt, [("All files", "*.*")]),
        )
        if not path:
            return

        try:
            fig.savefig(path, dpi=150, bbox_inches='tight')
            messagebox.showinfo("Сохранено", f"Файл:\n{path}", parent=root)
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось сохранить:\n{e}", parent=root)

    menu = tk.Menu(root, tearoff=0)
    menu.add_command(label="💾 Сохранить как PNG...", command=lambda: save_as('png'))
    menu.add_command(label="📄 Сохранить как PDF...", command=lambda: save_as('pdf'))
    menu.add_command(label="🎨 Сохранить как SVG...", command=lambda: save_as('svg'))
    menu.add_command(label="🖼 Сохранить как JPG...", command=lambda: save_as('jpg'))
    menu.add_separator()
    menu.add_command(label="❌ Закрыть", command=root.destroy)

    def show_menu(event):
        try:
            menu.tk_popup(event.x_root, event.y_root)
        finally:
            menu.grab_release()

    canvas.get_tk_widget().bind("<Button-3>", show_menu)
    root.bind("<Button-3>", show_menu)

    # Ctrl+S — сохранить как PNG
    root.bind("<Control-s>", lambda e: save_as('png'))

    # ============================================================
    # ЗАПУСК
    # ============================================================
    root.mainloop()

    return result["msg"]


# ============================================================
# PLOTLY (интерактив через HTML)
# ============================================================
def _draw_plotly(kind, x, y, options):
    """
    Интерактивный Plotly.

    Поддерживает ВСЕ типы:
        bar, line, pie, hist, scatter, box,
        heatmap, pair
    """
    try:
        import plotly.graph_objects as go
        from plotly.subplots import make_subplots
    except ImportError:
        raise ImportError(
            "plotly не установлен.\n"
            "Установите: pip install plotly"
        )

    title = options.get('title')
    xlabel = options.get('xlabel')
    ylabel = options.get('ylabel')
    save_path = options.get('save')
    color = options.get('color')

    # ============================================================
    # HEATMAP — матрица
    # ============================================================
    if kind == 'heatmap':
        fig = go.Figure(data=go.Heatmap(z=x))
        if title:
            fig.update_layout(title=title)

    # ============================================================
    # PAIR — матрица зависимостей
    # ============================================================
    elif kind == 'pair':
        matrix = x

        if not matrix or len(matrix) < 1:
            raise ValueError("pair: нужна матрица с данными")
        n_cols = len(matrix[0]) if matrix else 0
        if n_cols < 2:
            raise ValueError("pair: нужно минимум 2 столбца")

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

        n = n_cols
        fig = make_subplots(
            rows=n, cols=n,
            shared_xaxes=False,
            shared_yaxes=False,
            horizontal_spacing=0.05,
            vertical_spacing=0.05,
        )

        for i in range(n):
            for j in range(n):
                if i == j:
                    fig.add_trace(
                        go.Histogram(x=cols[i], showlegend=False),
                        row=i + 1, col=j + 1,
                    )
                else:
                    fig.add_trace(
                        go.Scatter(
                            x=cols[j], y=cols[i],
                            mode='markers',
                            marker=dict(size=3, opacity=0.5),
                            showlegend=False,
                        ),
                        row=i + 1, col=j + 1,
                    )

        if title:
            fig.update_layout(
                title=title,
                height=300 * n,
                width=300 * n,
            )

    # ============================================================
    # ОСТАЛЬНЫЕ ТИПЫ
    # ============================================================
    else:
        if kind == 'bar':
            fig = go.Figure(data=[go.Bar(x=x, y=y)])
        elif kind == 'line':
            fig = go.Figure(data=[go.Scatter(
                x=x, y=y, mode='lines+markers'
            )])
        elif kind == 'pie':
            fig = go.Figure(data=[go.Pie(labels=x, values=y)])
        elif kind == 'hist':
            fig = go.Figure(data=[go.Histogram(
                x=x, nbinsx=options.get('bins', 10)
            )])
        elif kind == 'scatter':
            fig = go.Figure(data=[go.Scatter(
                x=x, y=y, mode='markers'
            )])
        elif kind == 'box':
            fig = go.Figure(data=[go.Box(y=y, x=x)])
        else:
            raise ValueError(
                f"plotly: неизвестный тип '{kind}'"
            )

        if title:
            fig.update_layout(title=title)
        if xlabel:
            fig.update_xaxes(title=xlabel)
        if ylabel:
            fig.update_yaxes(title=ylabel)

    # ============================================================
    # СОХРАНЕНИЕ
    # ============================================================
    if save_path:
        fig.write_html(save_path)
        return f"Интерактивный график сохранён: {save_path}"

    import uuid
    fname = f"chart_{uuid.uuid4().hex[:8]}.html"
    fig.write_html(fname)
    return f"Интерактивный график сохранён: {fname}"


# ============================================================
# CHART NODE
# ============================================================
class ChartNode(Node):
    def __init__(self, kind, x, y=None, options=None):
        self.kind = kind
        self.x = x
        self.y = y
        self.options = options or {}

    def evaluate(self, env):
        kind_val = (self.kind.evaluate(env)
                    if hasattr(self.kind, 'evaluate')
                    else self.kind)
        if not isinstance(kind_val, str):
            raise TypeError(
                f"chart: тип графика должен быть строкой, "
                f"получен {type(kind_val)}"
            )
        kind = kind_val.lower()

        # Для heatmap и pair — X это матрица
        if kind == 'heatmap' or kind == 'pair':
            matrix_obj = (self.x.evaluate(env)
                          if hasattr(self.x, 'evaluate')
                          else self.x)
            if _is_duckdb(matrix_obj):
                try:
                    rows = matrix_obj.query(
                        f"SELECT * FROM {matrix_obj.table_name} LIMIT 1000"
                    )
                    data_matrix = [list(r) for r in rows]
                except Exception:
                    data_matrix = []
            elif hasattr(matrix_obj, 'data'):
                data_matrix = [list(r) if isinstance(r, list) else [r]
                               for r in matrix_obj.data]
            else:
                data_matrix = matrix_obj
            x_data = data_matrix
            y_data = None
        else:
            x_data = _extract_column(self.x, env)
            y_data = _extract_column(self.y, env) if self.y is not None else None

        # Опции
        opts = {}
        for k, v in self.options.items():
            val = v.evaluate(env) if hasattr(v, 'evaluate') else v
            opts[k] = val

        use_plotly = opts.pop('plotly', False)
        title = opts.get('title')
        save_path = opts.get('save')

        # ============================================================
        # PLOTLY
        # ============================================================
        if use_plotly:
            return _draw_plotly(kind, x_data, y_data, opts)

        # ============================================================
        # MATPLOTLIB + TKINTER
        # ============================================================
        fig = _build_figure(kind, x_data, y_data, opts)
        return _show_figure(fig, title=title, auto_save=save_path)

    def __repr__(self):
        return f"chart({self.kind}, ..., {len(self.options)} опций)"