# operators/print_stmt.py
from ast_nodes import Node
from runtime.random_source import forbid_random


# ============================================================
# ФОРМАТИРОВАНИЕ
# ============================================================
def _format_scalar(val):
    if val is None:
        return "None"
    return str(val)


def _format_vector_inline(items):
    """Вектор → '1 2 3' (через пробел)."""
    parts = []
    for v in items:
        if v is None:
            parts.append("None")
        else:
            parts.append(str(v))
    return " ".join(parts)


def _format_matrix_table(rows):
    """Матрица → таблица с выравниванием колонок."""
    if not rows:
        return ""

    display = []
    for row in rows:
        if not isinstance(row, list):
            row = [row]
        display.append([
            "None" if c is None else str(c)
            for c in row
        ])

    n_cols = max(len(r) for r in display)
    for r in display:
        while len(r) < n_cols:
            r.append("None")

    widths = []
    for j in range(n_cols):
        w = max(len(r[j]) for r in display)
        widths.append(max(4, w))

    aligns = []
    for j in range(n_cols):
        has_str = False
        has_num = False
        for r in rows:
            if not isinstance(r, list):
                r = [r]
            if j >= len(r):
                continue
            v = r[j]
            if v is None:
                continue
            if isinstance(v, str):
                has_str = True
            elif isinstance(v, (int, float)) and not isinstance(v, bool):
                has_num = True
        if has_str:
            aligns.append('<')
        elif has_num:
            aligns.append('>')
        else:
            aligns.append('<')

    lines = []
    for r in display:
        parts = []
        for j in range(n_cols):
            w = widths[j]
            a = aligns[j]
            if a == '>':
                parts.append(f"{r[j]:>{w}}")
            else:
                parts.append(f"{r[j]:<{w}}")
        lines.append("  ".join(parts))
    return "\n".join(lines)


def _is_matrix(val):
    if hasattr(val, 'data') and hasattr(val, 'is_2d'):
        return val.is_2d
    if isinstance(val, list) and val and isinstance(val[0], list):
        return True
    return False


def _is_vector(val):
    if hasattr(val, 'data') and hasattr(val, 'is_2d'):
        return not val.is_2d
    if isinstance(val, list) and not (val and isinstance(val[0], list)):
        return True
    return False


def _get_items(val):
    if hasattr(val, 'data'):
        return val.data
    return val


# ============================================================
# PRINT — вектор в одну строку, перевод строки в конце
# ============================================================
class PrintNode(Node):
    """
    print()        — ничего не выводит
    print(x)       — по типу:
                       • вектор  → в одну строку: 1 2 3
                       • матрица → таблицей
                       • скаляр  → как есть
                     В конце ВСЕГДА перевод строки.
    print(a, b, c) — a b c через пробел + перевод строки
    """
    def __init__(self, expressions):
        self.expressions = expressions

    def execute(self, env):
        if not self.expressions:
            return

        values = []
        for expr in self.expressions:
            val = expr.evaluate(env)
            forbid_random(val, "print")
            values.append(val)

        # Один аргумент — по типу
        if len(values) == 1:
            val = values[0]

            if _is_matrix(val):
                print(_format_matrix_table(_get_items(val)))
                return

            if _is_vector(val):
                print(_format_vector_inline(_get_items(val)))
                return

            print(_format_scalar(val))
            return

        # Несколько — через пробел, С переводом строки
        print(" ".join(_format_scalar(v) for v in values))

    def __repr__(self):
        return f"Print({self.expressions})"


# ============================================================
# PRINTLN — вектор построчно, перевод строки в конце
# ============================================================
class PrintlnNode(Node):
    """
    println()        — пустая строка
    println(x)       — по типу:
                         • вектор  → КАЖДЫЙ элемент с новой строки
                         • матрица → таблицей
                         • скаляр  → с новой строки
    println(a, b, c) — a b c через пробел + перевод строки
    """
    def __init__(self, expressions):
        self.expressions = expressions

    def execute(self, env):
        # println() — пустая строка
        if not self.expressions:
            print("")
            return

        values = []
        for expr in self.expressions:
            val = expr.evaluate(env)
            forbid_random(val, "println")
            values.append(val)

        # Один аргумент — по типу
        if len(values) == 1:
            val = values[0]

            # Матрица → таблица
            if _is_matrix(val):
                print(_format_matrix_table(_get_items(val)))
                return

            # Вектор → каждый элемент с новой строки
            if _is_vector(val):
                for item in _get_items(val):
                    print(_format_scalar(item))
                return

            # Скаляр → с новой строки
            print(_format_scalar(val))
            return

        # Несколько аргументов — через пробел В ОДНУ СТРОКУ
        print(" ".join(_format_scalar(v) for v in values))

    def __repr__(self):
        return f"Println({self.expressions})"


# ============================================================
# ПАРСЕР
# ============================================================
def parse_print(parser):
    parser.expect('PRINT')
    expressions = []

    if parser.check('LPAREN'):
        parser.expect('LPAREN')
        if not parser.check('RPAREN'):
            while not parser.check('RPAREN'):
                expr = parser.parse_expression()
                expressions.append(expr)
                if parser.check('COMMA'):
                    parser.expect('COMMA')
                else:
                    break
        parser.expect('RPAREN')
    else:
        expr = parser.parse_expression()
        expressions.append(expr)

    return PrintNode(expressions)


def parse_println(parser):
    parser.expect('PRINTLN')
    expressions = []

    if parser.check('LPAREN'):
        parser.expect('LPAREN')
        if not parser.check('RPAREN'):
            while not parser.check('RPAREN'):
                expr = parser.parse_expression()
                expressions.append(expr)
                if parser.check('COMMA'):
                    parser.expect('COMMA')
                else:
                    break
        parser.expect('RPAREN')
    else:
        expr = parser.parse_expression()
        expressions.append(expr)

    return PrintlnNode(expressions)