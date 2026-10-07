# errors/messages/en/window.py
"""
Errors for window functions.
"""

MESSAGES = {
    "WINDOW_BAD_SYNTAX":
        "Invalid window function syntax.\n"
        "  Format: <name>(m, by m[:, \"X\"], order m[:, \"Y\"], AZ|ZA)\n"
        "  Example: rownumber(m, by m[:, \"Dept\"], order m[:, \"Salary\"], ZA)",
    "WINDOW_NEED_BY":
        "Window function: 'by' is required for partition.",
    "WINDOW_NEED_ORDER":
        "Window function: 'order' is required for sorting.",
    "QUALIFY_BAD_SYNTAX":
        "Invalid qualify() syntax.\n"
        "  Format: qualify(m, window_function OP value)\n"
        "  Example: qualify(m, rownumber(m, by m[:, \"Dept\"], "
        "order m[:, \"Salary\"], ZA) <= 3)",
}