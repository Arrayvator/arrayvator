# runtime/logging_hook.py
"""
Автоматическое логирование всех операций ArrayVator.

Перехватывает Node.execute и Node.evaluate для классов,
у которых есть "человеческое" имя (имя функции/оператора).

Особенность:
    Оборачивает методы даже если они унаследованы (ищет по MRO).
    Например, если SumNode унаследовал evaluate от BaseStatNode —
    обёртка всё равно будет поставлена.

Пример:
    filterif(m[:, "X"] == 1)
    → в лог пишется:
        [1] 10:42:27 — filterif
            До:   2×2
            После: 1×2
"""

import functools
from runtime.logger import logger


# ============================================================
# ИМЕНА КЛАССОВ → ЧЕЛОВЕЧЕСКИЕ ИМЕНА
# ============================================================
_NAME_MAP = {
    # Фильтрация / поиск
    'FilterIfNode': 'filterif',
    'DeleteIfNode': 'deleteif',
    'DeleteNode': 'delete',
    'FindNode': 'find',
    'FindIfNode': 'findif',
    'SortNode': 'sort',
    'UniqueNode': 'Unique',
    'CountDistinctNode': 'CountDistinct',
    'ValueCountsNode': 'ValueCounts',
    'DeleteDuplicateNode': 'DeleteDuplicate',

    # Строки
    'SplitNode': 'split',
    'JoinVectorNode': 'joinvector',
    'ReplaceTextNode': 'replacetext',
    'DeleteTextLeftNode': 'deletetextleft',
    'DeleteTextRightNode': 'deletetextright',
    'TrimNode': 'trim',
    'TrimLeftNode': 'trimleft',
    'TrimRightNode': 'trimright',
    'CleanNode': 'clean',

    # Математика / статистика
    'SumNode': 'sum',
    'MinNode': 'min',
    'MaxNode': 'max',
    'AvgNode': 'avg',
    'RoundNode': 'round',
    'IntNode': 'int',
    'FracNode': 'frac',
    'FracDigitsNode': 'frac_digits',
    'LenNode': 'len',
    'LenRowNode': 'lenrow',
    'LenColNode': 'lencol',
    'BaseStatNode': 'stat',

    # Аналитика
    'AbcNode': 'abc',
    'PercentOfNode': 'percentof',
    'AnomalyNode': 'anomaly',
    'SumIfNode': 'sumif',
    'CountIfNode': 'countif',
    'AvgIfNode': 'avgif',
    'MinIfNode': 'minif',
    'MaxIfNode': 'maxif',
    'MedianIfNode': 'medianif',
    'CountUniqueIfNode': 'countuniqueif',
    'SumProductNode': 'sumproduct',

    # Изменение / копирование
    'InsertNode': 'insert',
    'InsertIfNode': 'insertif',
    'CopyNode': 'copy',
    'MoveNode': 'move',
    'MatrixModNode': 'matrixmod',
    'FillDownNode': 'filldown',
    'AddColumnNode': 'addcolumn',
    'AddRowsNode': 'addrows',
    'ApplyIfNode': 'applyif',
    'TransposeNode': 'transpose',
    'JoinArrayNode': 'joinarray',
    'JoinNode': 'join',
    'UnpivotNode': 'unpivot',
    'PivotNode': 'pivot',
    'GroupByNode': 'groupby',
    'GroupAggNode': 'groupagg',
    'SampleNode': 'sample',

    # Создание
    'MatrixCreateNode': 'matrix',
    'VectorNode': 'vector',
    'ZerosNode': 'zeros',
    'OnesNode': 'ones',
    'FillNode': 'fill',
    'RandomNode': 'random',
    'NumberSeqNode': 'range',
    'CaseNode': 'case',

    # Даты
    'DateNode': 'date',
    'DateDiffNode': 'DateDiff',
    'DateNowNode': 'datenow',
    'TimeNowNode': 'timenow',
    'TimestampNode': 'timestamp',
    'YearNode': 'year',
    'MonthNode': 'month',
    'DayNode': 'day',
    'QuarterNode': 'quarter',
    'WeekdayNode': 'weekday',
    'WeekdayNameNode': 'weekdayname',
    'MonthNameNode': 'monthname',
    'AddDaysNode': 'adddays',
    'AddMonthsNode': 'addmonths',
    'AddYearsNode': 'addyears',
    'DateTruncNode': 'datetrunc',
    'HourNode': 'hour',
    'MinuteNode': 'minute',
    'SecondNode': 'second',
    'AmPmNode': 'ampm',
    'IsPmNode': 'is_pm',
    'AddHoursNode': 'addhours',
    'AddMinutesNode': 'addminutes',
    'AddSecondsNode': 'addseconds',
    'TimeTruncNode': 'timetrunc',
    'TimeNode': 'time',
    'CalendarNode': 'calendar',
    'CalendarProNode': 'calendarpro',
    'IsValidTimeNode': 'is_valid_time',

    # Типы / None
    'IsNullNode': 'isnone',
    'FillnaNode': 'fillna',
    'DropnaNode': 'dropna',
    'CoalesceNode': 'coalesce',
    'NullIfNode': 'noneif',
    'TypeNode': 'type',
    'IsNumberNode': 'is_number',
    'IsIntegerNode': 'is_integer',
    'IsFloatNode': 'is_float',
    'IsStringNode': 'is_string',
    'IsBooleanNode': 'is_boolean',
    'ToStringNode': 'to_string',
    'ToNumberNode': 'to_number',

    # Файлы
    'OpenCSVNode': 'OpenCSV',
    'SaveCSVNode': 'SaveCSV',
    'OpenCSVShowNode': 'OpenCSVShow',
    'SaveCSVShowNode': 'SaveCSVShow',
    'OpenExcelNode': 'OpenExcel',
    'SaveExcelNode': 'SaveExcel',
    'OpenExcelShowNode': 'OpenExcelShow',
    'SaveExcelShowNode': 'SaveExcelShow',
    'OpenTXTNode': 'OpenTXT',
    'SaveTXTNode': 'SaveTXT',
    'OpenTXTShowNode': 'OpenTXTShow',
    'SaveTXTShowNode': 'SaveTXTShow',
    'OpenParquetNode': 'OpenParquet',
    'SaveParquetNode': 'SaveParquet',
    'OpenSQLiteNode': 'OpenSQLite',
    'SaveSQLiteNode': 'SaveSQLite',
    'QuerySQLiteNode': 'QuerySQLite',
    'OpenSQLiteShowNode': 'OpenSQLiteShow',
    'SaveSQLiteShowNode': 'SaveSQLiteShow',

    # BigData
    'ToMatrixNode': 'ToMatrix',
    'ToBigDataNode': 'ToBigData',
    'ConvertBigDataToMatrixNode': 'Convert_BigData_To_Matrix',
    'ConvertMatrixToBigDataNode': 'Convert_Matrix_To_BigData',

    # Оконные
    'RowNumberNode': 'rownumber',
    'RankNode': 'rank',
    'DenseRankNode': 'denserank',
    'PercentRankNode': 'percentrank',
    'CumeDistNode': 'cumedist',
    'NTileNode': 'ntile',
    'LagNode': 'lag',
    'LeadNode': 'lead',
    'FirstValueNode': 'firstvalue',
    'LastValueNode': 'lastvalue',
    'NthValueNode': 'nthvalue',
    'WinSumNode': 'winsum',
    'WinAvgNode': 'winavg',
    'WinCountNode': 'wincount',
    'WinMinNode': 'winmin',
    'WinMaxNode': 'winmax',
    'WinMedianNode': 'winmedian',
    'WinStdevNode': 'winstdev',
    'QualifyNode': 'qualify',

    # Графики / отчёты
    'ChartNode': 'chart',
    'ReportNode': 'report',
    'ReportSectionNode': 'report_section',
    'ReportTextNode': 'report_text',
    'ReportTableNode': 'report_table',
    'ReportChartNode': 'report_chart',
    'ReportSaveNode': 'report_save',
    'ReportShowNode': 'report_show',
    'ReportSavePdfNode': 'report_save_pdf',

    # Логирование
    'LogToFileNode': 'LogToFile',
    'LogOffNode': 'LogOff',

    # Ввод / вывод
    'InputShowNode': 'InputShow',
    'InputShowFormNode': 'InputShowForm',
    'InputListShowNode': 'InputListShow',
    'PrintShowNode': 'printshow',
    'PrintNode': 'print',
    'PrintlnNode': 'println',

    # Управление
    'IfNode': 'if',
    'ForNode': 'for',
    'WhileNode': 'while',
    'TryNode': 'try',
    'BreakNode': 'break',
    'InputNode': 'input',
    'AssignNode': '=',

    # Специальные
    'VLookupNode': 'vlookup',
    'IndexNode': 'index',
}


# ============================================================
# КЛАССЫ, КОТОРЫЕ НЕ ЛОГИРУЕМ (слишком часто вызываются)
# ============================================================
SKIP_CLASSES = {
    'Node',
    'TryNode',
    'IndexNode',
    'VariableNode',
    'PropertyNode',
    'NumberNode',
    'StringNode',
    'BooleanNode',
    'NullNode',
    'MatrixNode',
    'BinaryOp',
    'UnaryOp',
    'AssignNode',
    'IfNode',
    'ForNode',
    'WhileNode',
    'BreakNode',
    'InputNode',
}


# ============================================================
# ОПРЕДЕЛЕНИЕ РЕЗУЛЬТАТА (что логировать)
# ============================================================
def _is_loggable(value):
    """Стоит ли логировать этот объект."""
    if value is None:
        return False
    if isinstance(value, (int, float, str, bool)):
        return True
    if hasattr(value, 'data') or hasattr(value, 'is_2d'):
        return True
    if isinstance(value, list):
        return True
    if hasattr(value, 'table_name'):
        return True
    return False


def _human_name(node):
    """Человеческое имя узла."""
    cls_name = type(node).__name__
    return _NAME_MAP.get(cls_name, cls_name.replace('Node', '').lower())


# ============================================================
# ОБЁРТКА EVALUATE
# ============================================================
def _wrap_evaluate(original):
    @functools.wraps(original)
    def wrapper(self, env):
        if not logger.enabled:
            return original(self, env)

        name = _human_name(self)

        # Замер "до"
        before = None
        try:
            if hasattr(self, 'data') and hasattr(self.data, 'evaluate'):
                before = self.data.evaluate(env)
            elif hasattr(self, 'matrix') and hasattr(self.matrix, 'evaluate'):
                before = self.matrix.evaluate(env)
        except Exception:
            before = None

        try:
            result = original(self, env)
        except Exception as e:
            logger.log_operation(
                name,
                f"{name} — ОШИБКА: {type(e).__name__}: {e}",
                before=before,
                after=None,
            )
            raise

        if _is_loggable(result):
            logger.log_operation(
                name,
                f"{name}(...)",
                before=before,
                after=result,
            )
        else:
            logger.log_operation(
                name,
                f"{name}(...)",
                before=before,
                after=None,
            )
        return result

    return wrapper


# ============================================================
# ОБЁРТКА EXECUTE
# ============================================================
def _wrap_execute(original):
    @functools.wraps(original)
    def wrapper(self, env):
        if not logger.enabled:
            return original(self, env)

        name = _human_name(self)

        try:
            result = original(self, env)
        except Exception as e:
            logger.log_operation(
                name,
                f"{name} — ОШИБКА: {type(e).__name__}: {e}",
            )
            raise

        if type(self).__name__ in (
            'PrintNode', 'PrintlnNode',
            'InputShowNode', 'InputShowFormNode', 'InputListShowNode',
            'PrintShowNode',
            'ChartNode',
            'ReportNode', 'ReportSectionNode', 'ReportTextNode',
            'ReportTableNode', 'ReportChartNode', 'ReportSaveNode',
            'ReportShowNode', 'ReportSavePdfNode',
            'LogToFileNode', 'LogOffNode',
        ):
            logger.log_operation(name, f"{name}(...)")

        return result

    return wrapper


# ============================================================
# ПОИСК МЕТОДА В MRO
# ============================================================
def _find_method_in_mro(cls, method_name):
    """
    Ищет метод вверх по MRO.
    Возвращает сам метод (функцию) или None.
    """
    for base in cls.__mro__:
        if method_name in base.__dict__:
            return base.__dict__[method_name]
    return None


# ============================================================
# ПРИМЕНЕНИЕ КО ВСЕМ КЛАССАМ-НАСЛЕДНИКАМ Node
# ============================================================
_applied = False


def apply_logging_hooks():
    """
    Применяет обёртки ко всем классам-наследникам Node.

    Оборачивает evaluate/execute даже если они унаследованы —
    ищет метод по MRO (cls.__mro__).
    """
    global _applied
    if _applied:
        return
    _applied = True

    # --------------------------------------------------------
    # Импорт базового класса
    # --------------------------------------------------------
    try:
        from ast_nodes.base import Node
    except ImportError:
        return

    # --------------------------------------------------------
    # Сбор всех подклассов
    # --------------------------------------------------------
    def all_subclasses(cls):
        result = set()
        for sub in cls.__subclasses__():
            result.add(sub)
            result.update(all_subclasses(sub))
        return result

    subclasses = all_subclasses(Node)

    if len(subclasses) == 0:
        return

    # --------------------------------------------------------
    # Обёртка классов
    # --------------------------------------------------------
    for cls in subclasses:
        cls_name = cls.__name__

        if cls_name in SKIP_CLASSES:
            continue

        # ============================================================
        # EVALUATE — ищем вверх по MRO
        # ============================================================
        eval_method = _find_method_in_mro(cls, 'evaluate')

        if eval_method is not None:
            # Уже обёрнут?
            if not getattr(eval_method, '_logged', False):
                wrapped = _wrap_evaluate(eval_method)
                wrapped._logged = True
                cls.evaluate = wrapped

        # ============================================================
        # EXECUTE — ищем вверх по MRO
        # ============================================================
        exec_method = _find_method_in_mro(cls, 'execute')

        if exec_method is not None:
            if not getattr(exec_method, '_logged', False):
                wrapped = _wrap_execute(exec_method)
                wrapped._logged = True
                cls.execute = wrapped