# errors/messages/en/functions.py
"""
Errors for analytics and special functions:
abc, percentof, anomaly, conditional aggregates, addcolumn, groupby, ...
"""

MESSAGES = {
    # ============================================================
    # ABC
    # ============================================================
    "ABC_BAD_SYNTAX":
        "Invalid abc() syntax.\n"
        "  Format: abc(slice [, threshold1, threshold2] [, %|coef] [, m[:, N]])\n"
        "  Example: abc(m[:, \"Sales\"])\n"
        "  Example: abc(m[:, \"Sales\"], %)\n"
        "  Example: abc(m[:, \"Sales\"], 70, 90, %, m[:, end+1])\n"
        "\n"
        "  Rules:\n"
        "  • Thresholds (numbers) — at most two.\n"
        "  • Option (% or coef) — only one.\n"
        "  • Target column — only one.\n"
        "  • If target is given — % or coef is required.",

    # ============================================================
    # PERCENTOF
    # ============================================================
    "PERCENTOF_BAD_SYNTAX":
        "Invalid percentof() syntax.\n"
        "  Format: percentof(slice [, coef] [, by m[:, \"Y\"]])\n"
        "  Example: percentof(m[:, \"Sales\"])\n"
        "  Example: percentof(m[:, \"Sales\"], coef)\n"
        "  Example: percentof(m[:, \"Sales\"], by m[:, \"Category\"])",

    # ============================================================
    # ANOMALY
    # ============================================================
    "ANOMALY_BAD_SYNTAX":
        "Invalid anomaly() syntax.\n"
        "  Format: anomaly(slice [, method] [, params] [, by ...] [, only] [, approx])\n"
        "  Methods: iqr (default), zscore, percentile\n"
        "  Example: anomaly(m[:, \"Amount\"])\n"
        "  Example: anomaly(m[:, \"Amount\"], zscore, 2)\n"
        "  Example: anomaly(m[:, \"Amount\"], by m[:, \"Store\"], iqr, approx, only)\n"
        "\n"
        "  Rules:\n"
        "  • Method — only one.\n"
        "  • Numeric parameters — at most two.\n"
        "  • percentile requires TWO parameters (lo, hi).\n"
        "  • by, only, approx — each once.",

    # ============================================================
    # CONDITIONAL AGGREGATES
    # ============================================================
    "CONDAGG_BY_NOT_SLICE":
        "by requires the slice m[:, \"X\"].\n"
        "  Example: sumif(by m[:, \"Department\"], m[:, \"Salary\"])",
    "CONDAGG_VALUE_NOT_SLICE":
        "value_col must be the slice m[:, \"X\"].\n"
        "  Example: sumif(m[:, \"Department\"] == \"IT\", m[:, \"Salary\"])",
    "SUMPRODUCT_BAD_SYNTAX":
        "Invalid sumproduct() syntax.\n"
        "  Format: sumproduct(slice1, slice2 [, slice3, ...])\n"
        "  Example: sumproduct(m[:, \"Price\"], m[:, \"Quantity\"])",

    # ============================================================
    # ADDCOLUMN / ADDROWS
    # ============================================================
    "ADDCOLUMN_BAD_SYNTAX":
        "Invalid addcolumn() syntax.\n"
        "  Format: addcolumn(table, \"Name\", expression)",
    "ADDCOLUMN_NAME_NOT_STRING":
        "addcolumn: column name must be a quoted string.\n"
        "  Example: addcolumn(m, \"Total\", m[:, \"ID\"] + m[:, \"ID_10\"])",

    "ADDROWS_BAD_COUNT":
        "addrows: count must be a number.\n"
        "  Example: addrows(m, 5)",
    "ADDROWS_NEGATIVE":
        "addrows: count cannot be negative.\n"
        "  Example: addrows(m, 3, 0)",

    # ============================================================
    # APPLYIF
    # ============================================================
    "APPLYIF_BAD_SYNTAX":
        "Invalid applyif() syntax.\n"
        "  Format: applyif(condition, m[:, \"X\"] = value)",
    "APPLYIF_NEED_ASSIGN":
        "applyif: '=' is required inside.\n"
        "  Example: applyif(m[:, \"Dept\"] == \"IT\", "
        "m[:, \"Status\"] = \"VIP\")",

    # ============================================================
    # CASE
    # ============================================================
    "CASE_BAD_SYNTAX":
        "Invalid case() syntax.\n"
        "  Format: case(slice, when <cond> then <value>, ..., else <value>)",

    # ============================================================
    # CHART
    # ============================================================
    "CHART_BAD_KIND":
        "chart: invalid chart type.\n"
        "  Allowed: bar, line, pie, hist, scatter, box, heatmap, pair.\n"
        "\n"
        "  Examples:\n"
        "     chart(bar, m[:, \"Dept\"], m[:, \"Salary\"])\n"
        "     chart(line, m[:, \"Month\"], m[:, \"Sales\"])\n"
        "     chart(pie, m[:, \"Dept\"], m[:, \"Share\"])",

    # ============================================================
    # COPY / MOVE
    # ============================================================
    "COPY_BAD_SYNTAX":
        "Invalid copy() syntax.\n"
        "  Format: copy(source, target, before|after)",

    "MOVE_BAD_SYNTAX":
        "Invalid move() syntax.\n"
        "  Format: move(source, target, before|after)",
    "MOVE_TYPE_MISMATCH":
        "Cannot mix column and row in move().\n"
        "  Source and target must be the same type.",

    # ============================================================
    # DELETE
    # ============================================================
    "DELETE_BAD_SYNTAX":
        "Invalid delete() syntax.\n"
        "  Examples:\n"
        "     delete(m[2, :])         — delete a row\n"
        "     delete(m[:, \"Name\"])    — delete a column\n"
        "     delete(m[:, 2:5])       — delete columns 2..5",
    "DELETE_CELLS_NOT_ALLOWED":
        "delete: cannot delete PART of cells.\n"
        "  Delete a WHOLE ROW or a WHOLE COLUMN.",
    "DELETE_BOTH_ALL":
        "delete: specify what to delete — rows or columns.",
    "DELETE_VECTOR_DUCKDB":
        "delete: vector is not supported for DuckDB.\n"
        "  DuckDB works only with 2D tables.",
    "DELETEIF_BAD_SYNTAX":
        "Invalid deleteif() syntax.\n"
        "  Format: deleteif(m[:, \"X\"] == \"Y\")",

    # ============================================================
    # FILTER / FIND
    # ============================================================
    "FILTERIF_BAD_SYNTAX":
        "Invalid filterif() syntax.\n"
        "  Format: filterif(m[:, \"X\"] == \"Y\")",

    "FIND_BAD_SYNTAX":
        "Invalid find() syntax.\n"
        "  Format: find(condition [, inside] [, ignore] [, rows|cols])",

    # ============================================================
    # FILLDOWN
    # ============================================================
    "FILLDOWN_BAD_SYNTAX":
        "Invalid filldown() syntax.\n"
        "  Format: filldown(m[:, \"X\"] [, marker])\n"
        "  Example: filldown(m[:, \"Client\"], \"-\")",

    # ============================================================
    # GROUPAGG / GROUPBY
    # ============================================================
    "GROUPAGG_BAD_SYNTAX":
        "Invalid groupagg() syntax.\n"
        "  Format: groupagg(m[:, \"Key\"], m[:, \"Value\"], agg [, name] [, fill|exact])\n"
        "  Example: groupagg(m[:, \"Client\"], m[:, \"Sum\"], sum, \"TOTAL\")",

    "GROUPBY_BAD_SYNTAX":
        "Invalid groupby() syntax.\n"
        "  Format: groupby(by m[:, \"X\"], agg sum(m[:, \"Y\"]))",
    "GROUPBY_NEED_BY":
        "groupby: 'by' parameter is required.\n"
        "  Example: groupby(by m[:, \"Dept\"], agg sum(m[:, \"Salary\"]))",
    "GROUPBY_NEED_AGG":
        "groupby: 'agg' parameter is required.\n"
        "  Example: groupby(by m[:, \"Dept\"], agg sum(m[:, \"Salary\"]))",

    # ============================================================
    # INSERT / INSERTIF
    # ============================================================
    "INSERT_BAD_SYNTAX":
        "Invalid insert() syntax.\n"
        "  Format: insert(m[N, :], before|after)\n"
        "         insert(m[:, N], before|after)\n"
        "         insert(v, N, before|after)",

    "INSERTIF_BAD_SYNTAX":
        "Invalid insertif() syntax.\n"
        "  Format: insertif(condition, before|after)",

    # ============================================================
    # JOIN / JOINARRAY
    # ============================================================
    "JOIN_BAD_SYNTAX":
        "Invalid join() syntax.\n"
        "  Format: join(m1, m2, on \"ID\" [, how \"left\"])",
    "JOIN_NEED_ON":
        "join: 'on' parameter is required.\n"
        "  Example: join(m1, m2, on \"ID\")",
    "JOIN_COLUMN_NOT_FOUND":
        "join: column not found.",
    "JOIN_BOTH_DUCKDB_OR_MATRIX":
        "join: both tables must be of the same type "
        "(Matrix + Matrix or DuckDB + DuckDB).",

    "JOINARRAY_BAD_SYNTAX":
        "Invalid joinarray() syntax.\n"
        "  Format: joinarray(m1, m2, vertical|horizontal)",
    "JOINARRAY_NO_SLICES":
        "Cannot join partial ranges.\n"
        "  joinarray() works only with WHOLE matrices.",

    # ============================================================
    # MATRIXMOD
    # ============================================================
    "MATRIXMOD_BAD_SYNTAX":
        "Invalid matrixmod() syntax.\n"
        "  Format: matrixmod(m, action, N [, before|after])\n"
        "  Actions: delete, insert, duplicate, clear, keep, swap",

    # ============================================================
    # PIVOT / UNPIVOT
    # ============================================================
    "PIVOT_BAD_SYNTAX":
        "Invalid pivot() syntax.\n"
        "  Format: pivot(slice, slice, agg)",

    "UNPIVOT_BAD_SYNTAX":
        "Invalid unpivot() syntax.\n"
        "  Format: unpivot(slice, by slice [, names \"Name1\", \"Name2\"])",
    "UNPIVOT_COLUMN_OVERLAP":
        "Columns must not overlap between 'data' and 'by'.",
    "UNPIVOT_NEED_BY":
        "unpivot: 'by' parameter is required.\n"
        "  Example: unpivot(m[:, 2:end], by m[:, \"Country\"])",
    "UNPIVOT_TYPE_ERROR":
        "unpivot: expected a matrix or DuckDB.",

    # ============================================================
    # SORT
    # ============================================================
    "SORT_BAD_SYNTAX":
        "Invalid sort() syntax.\n"
        "  Format: sort(m[:, \"X\"], AZ|ZA)",

    # ============================================================
    # VLOOKUP
    # ============================================================
    "VLOOKUP_BAD_SYNTAX":
        "Invalid vlookup() syntax.\n"
        "  Format: vlookup(value, table, column [, search_vector] [, approx])",

    # ============================================================
    # REPORT
    # ============================================================
    "REPORT_BAD_SYNTAX":
        "Invalid report() syntax.\n"
        "  Format: report(\"Title\", \"file.html\")",
    "REPORT_SECTION_BAD_SYNTAX":
        "Invalid report_section() syntax.\n"
        "  Format: report_section(\"Title\")",
    "REPORT_TEXT_BAD_SYNTAX":
        "Invalid report_text() syntax.\n"
        "  Format: report_text(\"Text\")",
    "REPORT_TABLE_BAD_SYNTAX":
        "Invalid report_table() syntax.\n"
        "  Format: report_table(data [, title \"Title\"])",
    "REPORT_CHART_BAD_SYNTAX":
        "Invalid report_chart() syntax.\n"
        "  Format: report_chart(kind, x, y [, title \"...\"])",
    "REPORT_NOT_STARTED":
        "report: report not started.\n"
        "  First call report(\"Title\", \"file.html\")",
    "REPORT_PLAYWRIGHT_MISSING":
        "report_save_pdf: Playwright is not installed.\n"
        "  Install: pip install playwright\n"
        "  Then:    python -m playwright install chromium",

    # ============================================================
    # INPUT / OUTPUT
    # ============================================================
    "INPUTSHOW_BAD_MODE":
        "Invalid InputShow mode.\n"
        "  Allowed: 'text', 'number', 'matrix'.",
    "INPUTSHOWFORM_NO_FIELDS":
        "InputShowForm: no form fields specified.\n"
        "  Example: InputShowForm(\"Form\", \"Name\", \"Age\")",
    "INPUTLISTSHOW_ODD_ARGS":
        "InputListShow: odd number of arguments.\n"
        "  Arguments must go in pairs: \"label\", target.",
    "INPUTLISTSHOW_BAD_TARGET":
        "InputListShow: invalid target.\n"
        "  Target must be a variable or a matrix cell.",

    # ============================================================
    # LOGGING
    # ============================================================
    "LOGTOFILE_BAD_LEVEL":
        "Invalid logging level.\n"
        "  Allowed: 'all', 'matrix', 'summary'.",
    "LOGTOFILE_CANT_OPEN":
        "Could not open log file.",
}