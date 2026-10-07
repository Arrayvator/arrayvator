# parser/parse_functions/__init__.py
"""
Пакет парсинга функций.
"""

from .statistical import (
    parse_statistical,
    parse_count,
    parse_median,
    parse_std,
)
from .size import parse_size
from .delete import parse_delete, parse_deleteif
from .filterif import parse_filterif
from .transpose import parse_transpose
from .math import parse_math
from .string import parse_string
from .deletetext import parse_deletetextleft, parse_deletetextright
from .trim import parse_trim, parse_trimleft, parse_trimright
from .sort import parse_sort
from .find import parse_find, parse_findif
from .clean import parse_clean
from .insert import parse_insert
from .insertif import parse_insertif
from .vlookup import parse_vlookup
from .case import parse_case
from .deduplicate import parse_deduplicate
from .datediff import parse_datediff
from .date import parse_date
from .datetime_now import parse_datenow, parse_timenow, parse_timestamp

# ============================================================
# ДАТЫ И ВРЕМЯ: извлечение, арифметика, обрезка, конвертация
# ============================================================
from .dates_extract import (
    # Даты
    parse_year, parse_month, parse_day, parse_quarter,
    parse_weekday, parse_weekdayname, parse_monthname,
    parse_adddays, parse_addmonths, parse_addyears,
    parse_datetrunc,
    # Время
    parse_hour, parse_minute, parse_second,
    parse_ampm, parse_is_pm,
    parse_addhours, parse_addminutes, parse_addseconds,
    parse_timetrunc, parse_time,
)

# ============================================================
# КАЛЕНДАРЬ
# ============================================================
from .calendar import parse_calendar, parse_calendarpro

from .excel import parse_excel
from .csv import parse_csv
from .txt import parse_txt
from .parquet import parse_parquet
from .sqlite import parse_sqlite
from .logging_nodes import parse_logtofile, parse_logoff
from .input_show import parse_inputshow, parse_inputshowform
from .input_list_show import parse_inputlistshow
from .printshow import parse_printshow
from .tomatrix import (
    parse_to_matrix,
    parse_convert_bigdata_to_matrix,
    parse_convert_matrix_to_bigdata,
    parse_tobigdata,
)
from .null_handling import parse_null_handling
from .type_handling import parse_type_handling, parse_is_valid_time
from .matrix_ops import parse_matrix_ops
from .numseq import parse_numseq
from .pivot import parse_pivot
from .groupby import parse_groupby
from .groupagg import parse_groupagg
from .filldown import parse_filldown
from .addcolumn import parse_addcolumn
from .addrows import parse_addrows
from .sample import parse_sample
from .applyif import parse_applyif
from .join import parse_join
from .random import parse_random
from .vector import parse_vector
from .matrix import parse_matrix_create
from .copy import parse_copy
from .move import parse_move
from .joinarray import parse_joinarray
from .unpivot import parse_unpivot
from .matrixmod import parse_matrixmod

# ============================================================
# НОВЫЕ АНАЛИТИЧЕСКИЕ
# ============================================================
from .abc import parse_abc
from .percentof import parse_percentof
from .anomaly import parse_anomaly

# ============================================================
# УСЛОВНЫЕ АГРЕГАТЫ
# ============================================================
from .conditional_agg import (
    parse_sumif,
    parse_countif,
    parse_avgif,
    parse_minif,
    parse_maxif,
    parse_medianif,
    parse_countuniqueif,
    parse_sumproduct,
)

from .window import (
    parse_rownumber,
    parse_rank,
    parse_denserank,
    parse_percentrank,
    parse_cumedist,
    parse_ntile,
    parse_lag,
    parse_lead,
    parse_firstvalue,
    parse_lastvalue,
    parse_nthvalue,
    parse_winsum,
    parse_winavg,
    parse_wincount,
    parse_winmin,
    parse_winmax,
    parse_winmedian,
    parse_winstdev,
    parse_qualify,
)
from .chart import parse_chart
from .report import (
    parse_report,
    parse_report_section,
    parse_report_text,
    parse_report_table,
    parse_report_chart,
    parse_report_save,
    parse_report_show,
    parse_report_save_pdf,
)


__all__ = [
    # Статистические
    'parse_statistical',
    'parse_count',
    'parse_median',
    'parse_std',

    'parse_size',
    'parse_delete',
    'parse_deleteif',
    'parse_filterif',
    'parse_transpose',
    'parse_math',
    'parse_string',
    'parse_deletetextleft',
    'parse_deletetextright',
    'parse_trim',
    'parse_trimleft',
    'parse_trimright',
    'parse_sort',
    'parse_find',
    'parse_findif',
    'parse_clean',
    'parse_insert',
    'parse_insertif',
    'parse_vlookup',
    'parse_case',
    'parse_deduplicate',
    'parse_datediff',
    'parse_date',
    'parse_datenow',
    'parse_timenow',
    'parse_timestamp',
    # ДАТЫ — новые
    'parse_year',
    'parse_month',
    'parse_day',
    'parse_quarter',
    'parse_weekday',
    'parse_weekdayname',
    'parse_monthname',
    'parse_adddays',
    'parse_addmonths',
    'parse_addyears',
    'parse_datetrunc',
    # ВРЕМЯ — новые
    'parse_hour',
    'parse_minute',
    'parse_second',
    'parse_ampm',
    'parse_is_pm',
    'parse_addhours',
    'parse_addminutes',
    'parse_addseconds',
    'parse_timetrunc',
    'parse_time',
    'parse_is_valid_time',
    # КАЛЕНДАРЬ
    'parse_calendar',
    'parse_calendarpro',
    'parse_excel',
    'parse_csv',
    'parse_txt',
    'parse_parquet',
    'parse_sqlite',
    'parse_logtofile',
    'parse_logoff',
    'parse_inputshow',
    'parse_inputshowform',
    'parse_inputlistshow',
    'parse_printshow',
    'parse_to_matrix',
    'parse_convert_bigdata_to_matrix',
    'parse_convert_matrix_to_bigdata',
    'parse_tobigdata',
    'parse_null_handling',
    'parse_type_handling',
    'parse_matrix_ops',
    'parse_numseq',
    'parse_pivot',
    'parse_groupby',
    'parse_groupagg',
    'parse_filldown',
    'parse_addcolumn',
    'parse_addrows',
    'parse_sample',
    'parse_applyif',
    'parse_join',
    'parse_random',
    'parse_vector',
    'parse_matrix_create',
    'parse_copy',
    'parse_move',
    'parse_joinarray',
    'parse_unpivot',
    'parse_matrixmod',
    # НОВЫЕ
    'parse_abc',
    'parse_percentof',
    'parse_anomaly',
    # УСЛОВНЫЕ АГРЕГАТЫ
    'parse_sumif',
    'parse_countif',
    'parse_avgif',
    'parse_minif',
    'parse_maxif',
    'parse_medianif',
    'parse_countuniqueif',
    'parse_sumproduct',
    # window
    'parse_rownumber',
    'parse_rank',
    'parse_denserank',
    'parse_percentrank',
    'parse_cumedist',
    'parse_ntile',
    'parse_lag',
    'parse_lead',
    'parse_firstvalue',
    'parse_lastvalue',
    'parse_nthvalue',
    'parse_winsum',
    'parse_winavg',
    'parse_wincount',
    'parse_winmin',
    'parse_winmax',
    'parse_winmedian',
    'parse_winstdev',
    'parse_qualify',
    # chart
    'parse_chart',
    # report
    'parse_report',
    'parse_report_section',
    'parse_report_text',
    'parse_report_table',
    'parse_report_chart',
    'parse_report_save',
    'parse_report_show',
    'parse_report_save_pdf',
]