# parser/parse_functions/window.py
"""
Парсинг оконных функций.

СИНТАКСИС:

    # Над таблицей (первый аргумент — матрица m)
    rownumber(m, by m[:, "X"], order m[:, "Y"], AZ)
    rank(m, by m[:, "X"], order m[:, "Y"], ZA)
    denserank(m, by m[:, "X"], order m[:, "Y"], ZA)
    percentrank(m, by m[:, "X"], order m[:, "Y"], AZ)
    cumedist(m, by m[:, "X"], order m[:, "Y"], AZ)
    ntile(m, 4, by m[:, "X"], order m[:, "Y"], AZ)

    # Над столбцом (первый аргумент — срез m[:, "X"])
    lag(m[:, "X"], 1, 0)
    lead(m[:, "X"], 1, 0)
    firstvalue(m[:, "X"], by m[:, "Y"], order m[:, "Z"], AZ)
    lastvalue(m[:, "X"], by m[:, "Y"], order m[:, "Z"], AZ)
    nthvalue(m[:, "X"], 2, by m[:, "Y"], order m[:, "Z"], AZ)
    winsum(m[:, "X"], by m[:, "Y"], order m[:, "Z"], AZ)
    winavg(m[:, "X"], by m[:, "Y"])
    wincount(m[:, "X"], by m[:, "Y"])
    winmin(m[:, "X"], by m[:, "Y"])
    winmax(m[:, "X"], by m[:, "Y"])
    winmedian(m[:, "X"], by m[:, "Y"])
    winstdev(m[:, "X"], by m[:, "Y"])

    # QUALIFY
    qualify(m, rownumber(by m[:, "X"], order m[:, "Y"], AZ) <= 3)
"""

from ast_nodes import (
    RowNumberNode, RankNode, DenseRankNode, PercentRankNode,
    CumeDistNode, NTileNode, LagNode, LeadNode,
    FirstValueNode, LastValueNode, NthValueNode,
    WinSumNode, WinAvgNode, WinCountNode, WinMinNode,
    WinMaxNode, WinMedianNode, WinStdevNode,
    QualifyNode,
)


# ============================================================
# ХЕЛПЕР: ПАРСИНГ АРГУМЕНТОВ ОКНА
# ============================================================
def _parse_window_args(self):
    """
    Парсит опциональные аргументы окна после первого аргумента:
        by ..., order ..., AZ|ZA
    Возвращает dict с by/order/direction/frame.

    Ожидает, что следующая запятая уже есть (если есть аргументы).
    """
    by = None
    order = None
    direction = None
    frame = None

    while self.check('COMMA'):
        save_pos = self.pos
        self.expect('COMMA')

        token = self.peek()
        if not token:
            self.pos = save_pos
            break

        if token[0] == 'BY':
            self.expect('BY')
            by_list = [self.parse_primary()]
            # Опционально: несколько by через запятую
            while self.check('COMMA'):
                save2 = self.pos
                self.expect('COMMA')
                nxt = self.peek()
                if nxt and nxt[0] in ('ORDER', 'AZ', 'ZA', 'RPAREN'):
                    self.pos = save2
                    break
                try:
                    by_list.append(self.parse_primary())
                except Exception:
                    self.pos = save2
                    break
            by = by_list if len(by_list) > 1 else by_list[0]

        elif token[0] == 'ORDER':
            self.expect('ORDER')
            order = self.parse_primary()

        elif token[0] in ('AZ', 'ZA'):
            direction = self.parse_expression()

        else:
            # Не наш аргумент — возвращаем позицию
            self.pos = save_pos
            break

    return {
        'by': by,
        'order': order,
        'direction': direction,
        'frame': frame,
    }


# ============================================================
# ФУНКЦИИ НАД ТАБЛИЦЕЙ
# ============================================================
def _parse_over_table(self, cls):
    """Общий парсер для rownumber, rank, denserank, percentrank, cumedist."""
    self.expect('LPAREN')
    table = self.parse_expression()
    args = _parse_window_args(self)
    self.expect('RPAREN')
    return cls(table, **args)


def parse_rownumber(self):
    return _parse_over_table(self, RowNumberNode)


def parse_rank(self):
    return _parse_over_table(self, RankNode)


def parse_denserank(self):
    return _parse_over_table(self, DenseRankNode)


def parse_percentrank(self):
    return _parse_over_table(self, PercentRankNode)


def parse_cumedist(self):
    return _parse_over_table(self, CumeDistNode)


def parse_ntile(self):
    self.expect('LPAREN')
    table = self.parse_expression()
    self.expect('COMMA')
    n = self.parse_expression()
    args = _parse_window_args(self)
    self.expect('RPAREN')
    return NTileNode(table, n, **args)


# ============================================================
# LAG / LEAD
# ============================================================
def _parse_lag_lead(self, cls):
    self.expect('LPAREN')
    value = self.parse_primary()

    offset = None
    default = None

    # offset
    if self.check('COMMA'):
        self.expect('COMMA')
        offset = self.parse_expression()

        # default — только если следующий аргумент НЕ by/order/AZ/ZA
        if self.check('COMMA'):
            save_pos = self.pos
            self.expect('COMMA')
            nxt = self.peek()
            if nxt and nxt[0] in ('BY', 'ORDER', 'AZ', 'ZA', 'RPAREN'):
                self.pos = save_pos
            else:
                try:
                    default = self.parse_expression()
                except Exception:
                    self.pos = save_pos

    args = _parse_window_args(self)
    self.expect('RPAREN')
    return cls(value, offset, default, **args)


def parse_lag(self):
    return _parse_lag_lead(self, LagNode)


def parse_lead(self):
    return _parse_lag_lead(self, LeadNode)


# ============================================================
# FIRSTVALUE / LASTVALUE / NTHVALUE
# ============================================================
def _parse_value_over(self, cls):
    self.expect('LPAREN')
    value = self.parse_primary()
    args = _parse_window_args(self)
    self.expect('RPAREN')
    return cls(value, **args)


def parse_firstvalue(self):
    return _parse_value_over(self, FirstValueNode)


def parse_lastvalue(self):
    return _parse_value_over(self, LastValueNode)


def parse_nthvalue(self):
    self.expect('LPAREN')
    value = self.parse_primary()
    self.expect('COMMA')
    n = self.parse_expression()
    args = _parse_window_args(self)
    self.expect('RPAREN')
    return NthValueNode(value, n, **args)


# ============================================================
# WINAGG
# ============================================================
def _parse_winagg(self, cls):
    self.expect('LPAREN')
    value = self.parse_primary()
    args = _parse_window_args(self)
    self.expect('RPAREN')
    return cls(value, **args)


def parse_winsum(self):
    return _parse_winagg(self, WinSumNode)


def parse_winavg(self):
    return _parse_winagg(self, WinAvgNode)


def parse_wincount(self):
    return _parse_winagg(self, WinCountNode)


def parse_winmin(self):
    return _parse_winagg(self, WinMinNode)


def parse_winmax(self):
    return _parse_winagg(self, WinMaxNode)


def parse_winmedian(self):
    return _parse_winagg(self, WinMedianNode)


def parse_winstdev(self):
    return _parse_winagg(self, WinStdevNode)


# ============================================================
# QUALIFY
# ============================================================
def parse_qualify(self):
    self.expect('LPAREN')
    table = self.parse_expression()
    self.expect('COMMA')
    condition = self.parse_expression()
    self.expect('RPAREN')
    return QualifyNode(table, condition)