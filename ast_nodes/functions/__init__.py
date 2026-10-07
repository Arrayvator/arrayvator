# ast_nodes/functions/__init__.py
"""
Пакет функций ArrayVator
"""

from .statistical import (
    SumNode, MinNode, MaxNode, AvgNode,
    CountNode, MedianNode, StdNode,
)
from .size import LenRowNode, LenColNode, LenNode
from .delete import DeleteNode
from .deleteif import DeleteIfNode
from .filterif import FilterIfNode
from .transpose import TransposeNode
from .math import RoundNode, IntNode, FracNode, FracDigitsNode
from .string import SplitNode, JoinVectorNode, ReplaceTextNode
from .deletetext import DeleteTextLeftNode, DeleteTextRightNode
from .trim import TrimNode, TrimLeftNode, TrimRightNode
from .sort import SortNode
from .find import FindNode, FindIfNode
from .clean import CleanNode
from .insert import InsertNode
from .insertif import InsertIfNode
from .vlookup import VLookupNode
from .excel import (
    OpenExcelNode, SaveExcelNode, OpenExcelShowNode, SaveExcelShowNode,
)
from .csv import OpenCSVNode, SaveCSVNode, OpenCSVShowNode, SaveCSVShowNode
from .txt import OpenTXTNode, SaveTXTNode, OpenTXTShowNode, SaveTXTShowNode
from .parquet import OpenParquetNode, SaveParquetNode
from .sqlite import (
    OpenSQLiteNode, QuerySQLiteNode, SaveSQLiteNode,
    OpenSQLiteShowNode, SaveSQLiteShowNode,
)
from .logging_nodes import LogToFileNode, LogOffNode
from .input_show import InputShowNode, InputShowFormNode
from .input_list_show import InputListShowNode
from .printshow import PrintShowNode
from .tomatrix import (
    ToMatrixNode, ConvertBigDataToMatrixNode,
    ConvertMatrixToBigDataNode, ToBigDataNode,
)
from .deduplicate import (
    UniqueNode, CountDistinctNode, ValueCountsNode, DeleteDuplicateNode,
)
from .datediff import DateDiffNode
from .datetime_now import DateNowNode, TimeNowNode
from .case import CaseNode
from .null_handling import (
    IsNullNode, FillnaNode, DropnaNode, CoalesceNode, NullIfNode,
)
from .type_handling import (
    TypeNode, IsNumberNode, IsIntegerNode, IsFloatNode,
    IsStringNode, IsBooleanNode, ToStringNode, ToNumberNode,
)
from .matrix_ops import ZerosNode, OnesNode, FillNode
from .numseq import NumberSeqNode
from .pivot import PivotNode
from .groupby import GroupByNode
from .groupagg import GroupAggNode
from .filldown import FillDownNode
from .addcolumn import AddColumnNode
from .addrows import AddRowsNode
from .sample import SampleNode
from .applyif import ApplyIfNode
from .join import JoinNode
from .random import RandomNode
from .vector import VectorNode
from .matrix import MatrixCreateNode
from .copy import CopyNode
from .move import MoveNode
from .joinarray import JoinArrayNode
from .date import DateNode
from .unpivot import UnpivotNode
from .matrixmod import MatrixModNode

# ============================================================
# ДАТЫ И ВРЕМЯ
# ============================================================
from .dates_extract import (
    YearNode, MonthNode, DayNode, QuarterNode,
    WeekdayNode, WeekdayNameNode, MonthNameNode,
    AddDaysNode, AddMonthsNode, AddYearsNode,
    DateTruncNode,
    HourNode, MinuteNode, SecondNode,
    AmPmNode, IsPmNode,
    AddHoursNode, AddMinutesNode, AddSecondsNode,
    TimeTruncNode, TimeNode,
)
from .timestamp import TimestampNode
from .is_valid_time import IsValidTimeNode

# ============================================================
# КАЛЕНДАРЬ
# ============================================================
from .calendar import CalendarNode, CalendarProNode

# ============================================================
# НОВЫЕ АНАЛИТИЧЕСКИЕ ФУНКЦИИ
# ============================================================
from .abc import AbcNode
from .percentof import PercentOfNode
from .anomaly import AnomalyNode

# ============================================================
# УСЛОВНЫЕ АГРЕГАТЫ
# ============================================================
from .conditional_agg import (
    SumIfNode, CountIfNode, AvgIfNode,
    MinIfNode, MaxIfNode, MedianIfNode,
    CountUniqueIfNode, SumProductNode,
)

from .window import (
    RowNumberNode, RankNode, DenseRankNode, PercentRankNode,
    CumeDistNode, NTileNode, LagNode, LeadNode,
    FirstValueNode, LastValueNode, NthValueNode,
    WinSumNode, WinAvgNode, WinCountNode, WinMinNode,
    WinMaxNode, WinMedianNode, WinStdevNode,
    QualifyNode,
)
from .chart import ChartNode
from .report import (
    ReportNode, ReportSectionNode, ReportTextNode,
    ReportTableNode, ReportChartNode, ReportSaveNode,
    ReportShowNode, ReportSavePdfNode,
)


__all__ = [
    # Статистические
    'SumNode', 'MinNode', 'MaxNode', 'AvgNode',
    'CountNode', 'MedianNode', 'StdNode',
    # Размеры
    'LenRowNode', 'LenColNode', 'LenNode',
    # Удаление
    'DeleteNode', 'DeleteIfNode',
    # Фильтрация
    'FilterIfNode',
    # Транспонирование
    'TransposeNode',
    # Математические
    'RoundNode', 'IntNode', 'FracNode', 'FracDigitsNode',
    # Строковые
    'SplitNode', 'JoinVectorNode', 'ReplaceTextNode',
    # Удаление символов
    'DeleteTextLeftNode', 'DeleteTextRightNode',
    # Обрезка пробелов
    'TrimNode', 'TrimLeftNode', 'TrimRightNode',
    # Сортировка
    'SortNode',
    # Поиск
    'FindNode', 'FindIfNode',
    # Очистка
    'CleanNode',
    # Вставка
    'InsertNode', 'InsertIfNode',
    # VLOOKUP
    'VLookupNode',
    # Excel
    'OpenExcelNode', 'SaveExcelNode',
    'OpenExcelShowNode', 'SaveExcelShowNode',
    # CSV
    'OpenCSVNode', 'SaveCSVNode',
    'OpenCSVShowNode', 'SaveCSVShowNode',
    # TXT
    'OpenTXTNode', 'SaveTXTNode',
    'OpenTXTShowNode', 'SaveTXTShowNode',
    # Parquet
    'OpenParquetNode', 'SaveParquetNode',
    # SQLite
    'OpenSQLiteNode', 'QuerySQLiteNode', 'SaveSQLiteNode',
    'OpenSQLiteShowNode', 'SaveSQLiteShowNode',
    # Логирование
    'LogToFileNode', 'LogOffNode',
    # Ввод
    'InputShowNode', 'InputShowFormNode', 'InputListShowNode',
    # Печать
    'PrintShowNode',
    # Конвертация
    'ToMatrixNode', 'ConvertBigDataToMatrixNode',
    'ConvertMatrixToBigDataNode', 'ToBigDataNode',
    # Дубликаты
    'UniqueNode', 'CountDistinctNode', 'ValueCountsNode', 'DeleteDuplicateNode',
    # Даты
    'DateDiffNode', 'DateNowNode', 'TimeNowNode', 'DateNode',
    'YearNode', 'MonthNode', 'DayNode', 'QuarterNode',
    'WeekdayNode', 'WeekdayNameNode', 'MonthNameNode',
    'AddDaysNode', 'AddMonthsNode', 'AddYearsNode', 'DateTruncNode',
    'HourNode', 'MinuteNode', 'SecondNode', 'AmPmNode', 'IsPmNode',
    'AddHoursNode', 'AddMinutesNode', 'AddSecondsNode',
    'TimeTruncNode', 'TimeNode', 'TimestampNode', 'IsValidTimeNode',
    # Календарь
    'CalendarNode', 'CalendarProNode',
    # CASE
    'CaseNode',
    # NULL
    'IsNullNode', 'FillnaNode', 'DropnaNode', 'CoalesceNode', 'NullIfNode',
    # Типы
    'TypeNode', 'IsNumberNode', 'IsIntegerNode', 'IsFloatNode',
    'IsStringNode', 'IsBooleanNode', 'ToStringNode', 'ToNumberNode',
    # Матричные операции
    'ZerosNode', 'OnesNode', 'FillNode',
    # Диапазоны
    'NumberSeqNode',
    # Pivot
    'PivotNode',
    # GroupBy
    'GroupByNode',
    # GroupAgg / FillDown
    'GroupAggNode', 'FillDownNode',
    # AddColumn / AddRows
    'AddColumnNode', 'AddRowsNode',
    # Sample
    'SampleNode',
    # ApplyIf
    'ApplyIfNode',
    # Join
    'JoinNode',
    # Random
    'RandomNode',
    # Vector / Matrix
    'VectorNode', 'MatrixCreateNode',
    # Copy / Move / JoinArray
    'CopyNode', 'MoveNode', 'JoinArrayNode',
    # Unpivot
    'UnpivotNode',
    # MatrixMod
    'MatrixModNode',
    # Аналитические
    'AbcNode', 'PercentOfNode', 'AnomalyNode',
    # Условные агрегаты
    'SumIfNode', 'CountIfNode', 'AvgIfNode',
    'MinIfNode', 'MaxIfNode', 'MedianIfNode',
    'CountUniqueIfNode', 'SumProductNode',
    # Window
    'RowNumberNode', 'RankNode', 'DenseRankNode', 'PercentRankNode',
    'CumeDistNode', 'NTileNode', 'LagNode', 'LeadNode',
    'FirstValueNode', 'LastValueNode', 'NthValueNode',
    'WinSumNode', 'WinAvgNode', 'WinCountNode', 'WinMinNode',
    'WinMaxNode', 'WinMedianNode', 'WinStdevNode',
    'QualifyNode',
    # Chart
    'ChartNode',
    # Reports
    'ReportNode', 'ReportSectionNode', 'ReportTextNode',
    'ReportTableNode', 'ReportChartNode', 'ReportSaveNode',
    'ReportShowNode', 'ReportSavePdfNode',
]