# parser/parse_functions/chart.py
"""
Парсинг CHART.

СИНТАКСИС:
    chart(тип, x)
    chart(тип, x, y)
    chart(тип, x, y, опции...)

ТИПЫ:
    bar, line, pie, hist, scatter, box, heatmap, pair

ОПЦИИ:
    title "..."      — заголовок
    xlabel "..."     — подпись X
    ylabel "..."     — подпись Y
    color "..."      — цвет
    save "file.png"  — сохранить в файл
    bins N           — корзин (hist)
    plotly           — интерактивный Plotly
    static           — статичный Matplotlib

ПРИМЕРЫ:
    chart(bar, m[:, "Отдел"], m[:, "Зарплата"])
    chart(line, m[:, "Месяц"], m[:, "Продажи"])
    chart(hist, m[:, "Возраст"], bins 10)
    chart(pie, m[:, "Отдел"], m[:, "Доля"])
    chart(heatmap, m[:, 2:end])
    chart(pair, m[:, 2:end])
    chart(bar, m[:, "Отдел"], m[:, "Зарплата"],
          title "Зарплаты", color "red", plotly)
"""

from ast_nodes import ChartNode
from errors import ArrayVatorError


# ============================================================
# ТИПЫ ГРАФИКОВ
# ============================================================
CHART_KINDS = {
    'BAR', 'LINE', 'PIE', 'HIST', 'SCATTER',
    'BOX', 'HEATMAP', 'PAIR',
}

# Типы, которым НЕ нужен Y (только X)
CHART_KINDS_NO_Y = {'HIST', 'HEATMAP', 'PAIR'}

# Типы, которым ОБЯЗАТЕЛЬНО нужен Y
CHART_KINDS_NEED_Y = {'BAR', 'LINE', 'PIE', 'SCATTER', 'BOX'}


# ============================================================
# ОПЦИИ (все возможные токены)
# ============================================================
CHART_OPTIONS = {
    'TITLE', 'XLABEL', 'YLABEL', 'COLOR', 'SAVE',
    'BINS', 'PLOTLY', 'STATIC',
}


# ============================================================
# ПАРСЕР
# ============================================================
def parse_chart(self):
    """Парсинг CHART"""
    self.expect('LPAREN')

    # ============================================================
    # 1. Тип графика
    # ============================================================
    kind_token = self.peek()
    if not kind_token or kind_token[0] not in CHART_KINDS:
        raise ArrayVatorError(
            code="CHART_BAD_KIND",
            context=self._get_context(kind_token),
        )

    kind = kind_token[0].lower()   # 'bar' / 'line' / ...
    self.pos += 1

    if not self.check('COMMA'):
        raise ArrayVatorError(
            code="CHART_NEED_X",
            context=self._get_context(),
        )
    self.expect('COMMA')

    # ============================================================
    # 2. Данные X (обязательно)
    # ============================================================
    x = self.parse_primary()

    # ============================================================
    # 3. Данные Y (опционально)
    # ============================================================
    y = None
    if self.check('COMMA'):
        save_pos = self.pos
        self.expect('COMMA')

        nxt = self.peek()

        # Если следующий токен — опция или ')' — Y не указан
        if nxt is None or nxt[0] in CHART_OPTIONS or nxt[0] == 'RPAREN':
            self.pos = save_pos
        else:
            y = self.parse_primary()

    # ============================================================
    # 4. Проверка: Y обязателен для некоторых типов
    # ============================================================
    if kind.upper() in CHART_KINDS_NEED_Y and y is None:
        raise ArrayVatorError(
            code="CHART_NEED_Y",
            context=self._get_context(),
        )

    # ============================================================
    # 5. Опции
    # ============================================================
    options = {}

    while self.check('COMMA'):
        self.expect('COMMA')

        opt_token = self.peek()
        if not opt_token:
            break

        opt_type = opt_token[0]

        # ---------------------------------------------------------
        # Строковые опции: title, xlabel, ylabel, color, save
        # ---------------------------------------------------------
        if opt_type in ('TITLE', 'XLABEL', 'YLABEL', 'COLOR', 'SAVE'):
            opt_name = opt_type.lower()
            self.pos += 1
            value = self.parse_expression()
            options[opt_name] = value

        # ---------------------------------------------------------
        # bins N
        # ---------------------------------------------------------
        elif opt_type == 'BINS':
            self.pos += 1
            value = self.parse_expression()

            # Проверка: bins — число >= 1
            try:
                bins_val = (value.evaluate(None)
                            if hasattr(value, 'evaluate')
                            else value)
                if not isinstance(bins_val, (int, float)):
                    raise ArrayVatorError(
                        code="CHART_BAD_BINS",
                        context=self._get_context(),
                    )
                if bins_val < 1:
                    raise ArrayVatorError(
                        code="CHART_BAD_BINS",
                        context=self._get_context(),
                    )
            except ArrayVatorError:
                raise
            except Exception:
                pass

            options['bins'] = value

        # ---------------------------------------------------------
        # plotly
        # ---------------------------------------------------------
        elif opt_type == 'PLOTLY':
            self.pos += 1
            options['plotly'] = True

        # ---------------------------------------------------------
        # static
        # ---------------------------------------------------------
        elif opt_type == 'STATIC':
            self.pos += 1
            options['plotly'] = False

        # ---------------------------------------------------------
        # Неизвестная опция
        # ---------------------------------------------------------
        else:
            raise ArrayVatorError(
                code="CHART_BAD_OPTION",
                context=self._get_context(opt_token),
                message=(
                    f"chart: неверная опция '{opt_token[1]}'.\n"
                    f"  Допустимо: title, xlabel, ylabel, color, "
                    f"save, bins, plotly, static."
                ),
            )

    self.expect('RPAREN')

    return ChartNode(kind, x, y, options)