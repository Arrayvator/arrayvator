# parser/dispatch/__init__.py
"""
Диспетчеры parse_primary по темам.
"""

from .literals import dispatch as _literals
from .special import dispatch as _special
from .input_output import dispatch as _input_output
from .strings import dispatch as _strings
from .math import dispatch as _math
from .statistics import dispatch as _statistics
from .analytics import dispatch as _analytics
from .filter_delete import dispatch as _filter_delete
from .sort_find import dispatch as _sort_find
from .modify import dispatch as _modify
from .join_unpivot import dispatch as _join_unpivot
from .groupby import dispatch as _groupby
from .case_apply import dispatch as _case_apply
from .dates import dispatch as _dates
from .types import dispatch as _types
from .files import dispatch as _files
from .convert import dispatch as _convert
from .create import dispatch as _create
from .sample_transpose import dispatch as _sample_transpose
from .windows import dispatch as _windows
from .charts import dispatch as _charts
from .reports import dispatch as _reports
from .identifiers import dispatch as _identifiers


DISPATCHERS = [
    _literals,
    _special,
    _input_output,
    _strings,
    _math,
    _statistics,
    _analytics,
    _filter_delete,
    _sort_find,
    _modify,
    _join_unpivot,
    _groupby,
    _case_apply,
    _dates,
    _types,
    _files,
    _convert,
    _create,
    _sample_transpose,
    _windows,
    _charts,
    _reports,
    _identifiers,
]


__all__ = ['DISPATCHERS']