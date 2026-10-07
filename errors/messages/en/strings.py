# errors/messages/en/strings.py
"""
Errors for string functions: trim, replacetext, deletetext, clean, split.
"""

MESSAGES = {
    "DELETETEXTLEFT_BAD_SYNTAX":
        "Invalid deletetextleft() syntax.\n"
        "  Format: deletetextleft(data, N)",
    "DELETETEXTRIGHT_BAD_SYNTAX":
        "Invalid deletetextright() syntax.\n"
        "  Format: deletetextright(data, N)",

    "TRIM_BAD_SYNTAX":
        "Invalid trim / trimleft / trimright syntax.\n"
        "  Format: trim(data [, \"chars\"])\n"
        "  Example: trim(m[:, \"Name\"])\n"
        "  Example: trimleft(m[:, \"Code\"], \"0\")\n"
        "  Example: trimright(m[:, \"Name\"])",

    "REPLACETEXT_BAD_SYNTAX":
        "Invalid replacetext() syntax.\n"
        "  Format: replacetext(data, \"what\", \"with\" [, ignore])",

    "SPLIT_BAD_SYNTAX":
        "Invalid split() syntax.\n"
        "  Format: split(text [, delimiter] [, skip])",

    "CLEAN_BAD_SYNTAX":
        "Invalid clean() syntax.\n"
        "  Format: clean(data, \"digits\"|\"letters\"|\"special\"|\"alnum\")",

    "DELETETEXT_NEGATIVE_COUNT":
        "Character count cannot be negative.",
    "DELETETEXT_COLUMN_NOT_FOUND":
        "Column not found in matrix.\n"
        "  Check the column name or number.",
    "DELETETEXT_ROW_NOT_FOUND":
        "Row not found in matrix.\n"
        "  Check the row number or value in the first column.",
}