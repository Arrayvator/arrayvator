# parser/parse_functions/anomaly.py
"""
Парсинг ANOMALY — поиск аномалий.

СИНТАКСИС (порядок аргументов ЛЮБОЙ):
    anomaly(срез)
    anomaly(срез, iqr)
    anomaly(срез, iqr, 3.0)
    anomaly(срез, zscore, 2)
    anomaly(срез, percentile, 5, 95)
    anomaly(срез, by m[:, "Магазин"])
    anomaly(срез, only)
    anomaly(срез, only, approx)
"""

from ast_nodes import AnomalyNode
from ast_nodes.index import IndexNode
from errors import ArrayVatorError


def parse_anomaly(self):
    """Парсинг ANOMALY."""
    self.expect('LPAREN')

    # 1. Обязательный срез
    data = self.parse_primary()
    if not isinstance(data, IndexNode):
        raise ArrayVatorError(
            code="ANOMALY_NEED_SLICE",
            context=self._get_context(),
        )

    # 2. Остальные аргументы — в любом порядке
    method = None
    params = []
    by = None
    only = False
    approx = False

    while self.check('COMMA'):
        self.expect('COMMA')

        token = self.peek()
        if not token:
            raise ArrayVatorError(
                code="ANOMALY_BAD_SYNTAX",
                context=self._get_context(),
                message="anomaly: неожиданный конец аргументов.",
            )

        # 2.1. Метод
        if token[0] == 'IQR':
            self.expect('IQR')
            if method is not None:
                raise ArrayVatorError(
                    code="ANOMALY_BAD_METHOD",
                    context=self._get_context(token),
                )
            method = 'iqr'

        elif token[0] == 'ZSCORE':
            self.expect('ZSCORE')
            if method is not None:
                raise ArrayVatorError(
                    code="ANOMALY_BAD_METHOD",
                    context=self._get_context(token),
                )
            method = 'zscore'

        elif token[0] == 'PERCENTILE':
            self.expect('PERCENTILE')
            if method is not None:
                raise ArrayVatorError(
                    code="ANOMALY_BAD_METHOD",
                    context=self._get_context(token),
                )
            method = 'percentile'

        # 2.2. Число — параметр метода
        elif token[0] == 'NUMBER':
            val = self.parse_expression()
            params.append(val)

        # 2.3. by срез
        elif token[0] == 'BY':
            self.expect('BY')
            if by is not None:
                raise ArrayVatorError(
                    code="ANOMALY_TOO_MANY_BY",
                    context=self._get_context(token),
                )
            by = self.parse_primary()
            if not isinstance(by, IndexNode):
                raise ArrayVatorError(
                    code="ANOMALY_BAD_BY",
                    context=self._get_context(),
                )

        # 2.4. only
        elif token[0] == 'ONLY':
            self.expect('ONLY')
            only = True

        # 2.5. approx
        elif token[0] == 'APPROX':
            self.expect('APPROX')
            approx = True

        # 2.6. Неизвестный аргумент
        else:
            raise ArrayVatorError(
                code="ANOMALY_BAD_ARG",
                context=self._get_context(token),
                message=(
                    f"anomaly: неожиданный аргумент '{token[1]}'.\n"
                    f"  Ожидается: iqr / zscore / percentile, "
                    f"число, by m[:, ...], only, approx."
                ),
            )

    self.expect('RPAREN')

    # ============================================================
    # 3. Валидация
    # ============================================================
    if len(params) > 2:
        raise ArrayVatorError(
            code="ANOMALY_TOO_MANY_PARAMS",
            context=self._get_context(),
        )

    if method == 'percentile' and len(params) == 1:
        raise ArrayVatorError(
            code="ANOMALY_PERCENTILE_NEEDS_TWO",
            context=self._get_context(),
        )

    return AnomalyNode(
        data,
        method=method,
        params=params,
        by=by,
        only=only,
        approx=approx,
    )