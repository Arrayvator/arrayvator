# parser/parse_functions/report.py
"""
Парсинг функций отчёта.
"""

from ast_nodes.functions.report import (
    ReportNode,
    ReportSectionNode,
    ReportTextNode,
    ReportTableNode,
    ReportChartNode,
    ReportSaveNode,
    ReportShowNode,
    ReportSavePdfNode,
)
from errors import ArrayVatorError


# ============================================================
# ТИПЫ ГРАФИКОВ (такие же, как в chart)
# ============================================================
CHART_KINDS = {
    'BAR', 'LINE', 'PIE', 'HIST', 'SCATTER',
    'BOX', 'HEATMAP', 'PAIR',
}

# Типы, которым НЕ нужен Y
CHART_KINDS_NO_Y = {'HIST', 'HEATMAP', 'PAIR'}

# Типы, которым НУЖЕН Y
CHART_KINDS_NEED_Y = {'BAR', 'LINE', 'PIE', 'SCATTER', 'BOX'}

# Все опции
CHART_OPTIONS = {
    'TITLE', 'XLABEL', 'YLABEL', 'COLOR', 'SAVE',
    'BINS', 'PLOTLY', 'STATIC',
}


def parse_report(self):
    self.expect('LPAREN')
    title = self.parse_expression()
    self.expect('COMMA')
    path = self.parse_expression()
    self.expect('RPAREN')
    return ReportNode(title, path)


def parse_report_section(self):
    self.expect('LPAREN')
    title = self.parse_expression()
    self.expect('RPAREN')
    return ReportSectionNode(title)


def parse_report_text(self):
    self.expect('LPAREN')
    text = self.parse_expression()
    self.expect('RPAREN')
    return ReportTextNode(text)


def parse_report_table(self):
    self.expect('LPAREN')
    data = self.parse_primary()

    title = None
    if self.check('COMMA'):
        self.expect('COMMA')
        opt_token = self.peek()
        if opt_token and opt_token[0] == 'TITLE':
            self.pos += 1
            title = self.parse_expression()

    self.expect('RPAREN')
    return ReportTableNode(data, title)


def parse_report_chart(self):
    """report_chart(тип, x [, y] [, опции])"""
    self.expect('LPAREN')

    # ============================================================
    # 1. Тип графика
    # ============================================================
    kind_token = self.peek()
    if not kind_token or kind_token[0] not in CHART_KINDS:
        raise ArrayVatorError(
            code="REPORT_CHART_BAD_KIND",
            context=self._get_context(kind_token),
        )

    kind = kind_token[0].lower()
    self.pos += 1

    if not self.check('COMMA'):
        raise ArrayVatorError(
            code="REPORT_CHART_BAD_SYNTAX",
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
        if nxt is None or nxt[0] in CHART_OPTIONS or nxt[0] == 'RPAREN':
            self.pos = save_pos
        else:
            y = self.parse_primary()

    # ============================================================
    # 4. Проверка: Y обязателен?
    # ============================================================
    if kind.upper() in CHART_KINDS_NEED_Y and y is None:
        raise ArrayVatorError(
            code="REPORT_CHART_NEED_Y",
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

        # Строковые опции
        if opt_type in ('TITLE', 'XLABEL', 'YLABEL', 'COLOR', 'SAVE'):
            opt_name = opt_type.lower()
            self.pos += 1
            value = self.parse_expression()
            options[opt_name] = value

        # bins N
        elif opt_type == 'BINS':
            self.pos += 1
            value = self.parse_expression()
            options['bins'] = value

        # plotly
        elif opt_type == 'PLOTLY':
            self.pos += 1
            options['plotly'] = True

        # static
        elif opt_type == 'STATIC':
            self.pos += 1
            options['plotly'] = False

        else:
            raise ArrayVatorError(
                code="REPORT_CHART_BAD_OPTION",
                context=self._get_context(opt_token),
                message=(
                    f"report_chart: неверная опция '{opt_token[1]}'.\n"
                    f"  Допустимо: title, xlabel, ylabel, color, "
                    f"save, bins, plotly, static."
                ),
            )

    self.expect('RPAREN')
    return ReportChartNode(kind, x, y, options)


def parse_report_save(self):
    """report_save([show])"""
    self.expect('LPAREN')

    show = None
    if not self.check('RPAREN'):
        show = self.parse_expression()

    self.expect('RPAREN')
    return ReportSaveNode(show)


def parse_report_show(self):
    """report_show()"""
    self.expect('LPAREN')
    self.expect('RPAREN')
    return ReportShowNode()


def parse_report_save_pdf(self):
    """report_save_pdf("file.pdf")"""
    self.expect('LPAREN')
    pdf_path = self.parse_expression()
    self.expect('RPAREN')
    return ReportSavePdfNode(pdf_path)