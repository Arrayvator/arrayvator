"""
Утилиты для работы с индексами (end, last, end+N, диапазоны).

ПРАВИЛА:

    Разрешённые формы:
        :   / all            — все строки/столбцы
        2                    — одна строка/столбец (1-based)
        2:5                  — диапазон (1-based, включительно)
        10:end               — от номера до конца
        end                  — последняя
        end-N                — N-я с конца (одна)
        last N               — N последних (диапазон, N < total)
        "Имя"                — по имени (только для столбца)

    Запрещённые формы (ошибка):
        end:end              → пиши "end"
        end-1:end-1          → пиши "end-1"
        end-4:end            → пиши "last 5"
        end-N:5 / 5:end-N    → нельзя
        last N:end           → нельзя
        2:last N             → нельзя
        end+N                → ошибка при чтении (разрешено при записи)
        last N, где N >= len → ошибка

    Заголовок:
        по имени (str)       → skip_header=True
        по номеру / end      → skip_header=False

После реформы мутации:
    - extract_target_name больше не используется.
"""


# ============================================================
# ИСКЛЮЧЕНИЯ
# ============================================================

class IndexError_(Exception):
    """Базовое исключение для ошибок индексации"""
    pass


class ColumnNotFoundError(IndexError_):
    pass


class RowNotFoundError(IndexError_):
    pass


class MultipleColumnsError(IndexError_):
    pass


class MultipleRowsError(IndexError_):
    pass


class OutOfRangeError(IndexError_):
    pass


class InvalidRangeError(IndexError_):
    pass


class InvalidIndexSpecError(IndexError_):
    pass


# ============================================================
# ПАРСИНГ ДИАПАЗОНА
# ============================================================

def parse_range_spec(spec, total, is_column=False):
    """
    Парсит спецификацию диапазона и возвращает (start, end) — 1-based,
    включительно.
    """
    kind = "столбцов" if is_column else "строк"
    kind_one = "столбец" if is_column else "строку"

    # ============================================================
    # 1. ЧИСЛО
    # ============================================================
    if isinstance(spec, (int, float)):
        n = int(spec)
        if n < 1 or n > total:
            raise OutOfRangeError(
                f"{kind_one.capitalize()} {n} за пределами "
                f"(всего {kind}: {total})"
            )
        return (n, n)

    if spec is None:
        return (1, total)

    if not isinstance(spec, str):
        raise InvalidIndexSpecError(
            f"Неверный тип индекса: {type(spec)}"
        )

    # ============================================================
    # 2. НОРМАЛИЗАЦИЯ
    # ============================================================
    s = spec.strip().lower()

    # --- ":" / "all" ---
    if s in (':', 'all'):
        return (1, total)

    # --- "end" ---
    if s == 'end':
        return (total, total)

    # --- "end-N" ---
    if s.startswith('end-'):
        try:
            n = int(s[4:].strip())
        except ValueError:
            raise InvalidRangeError(f"Неверный формат: '{spec}'")

        if n < 0:
            raise InvalidRangeError(
                f"'end-{n}' — N должно быть >= 0"
            )

        idx = total - n
        if idx < 1:
            raise OutOfRangeError(
                f"'end-{n}' за пределами (всего {kind}: {total})"
            )
        return (idx, idx)

    # --- "end+N" — ошибка при чтении ---
    if s.startswith('end+'):
        raise InvalidRangeError(
            f"'end+N' нельзя использовать для чтения.\n"
            f"  Для расширения матрицы используйте присваивание:\n"
            f"      m[:, end+1] = [...]\n"
            f"      m[end+1, :] = [...]"
        )

    # --- "last N" ---
    if s.startswith('last'):
        rest = s[4:].strip()
        if rest == '':
            raise InvalidRangeError(
                "Укажите количество: 'last 1', 'last 2' и т.д."
            )
        try:
            n = int(rest)
        except ValueError:
            raise InvalidRangeError(f"Неверный формат: '{spec}'")

        if n < 1:
            raise OutOfRangeError(
                f"'last {n}' — N должно быть >= 1"
            )
        if n >= total:
            raise OutOfRangeError(
                f"'last {n}' — N должно быть МЕНЬШЕ общего количества "
                f"({kind}: {total})"
            )
        return (total - n + 1, total)

    # ============================================================
    # 3. ДИАПАЗОН "start:end"
    # ============================================================
    if ':' in s:
        parts = s.split(':')

        if len(parts) != 2:
            raise InvalidRangeError(f"Неверный формат диапазона: '{spec}'")

        left, right = parts[0].strip(), parts[1].strip()

        # --- start ---
        if left in ('', 'begin', 'all'):
            start = 1
        else:
            try:
                start = int(left)
            except ValueError:
                raise InvalidRangeError(
                    f"Неверное начало диапазона: '{left}'"
                )
            if start < 1 or start > total:
                raise OutOfRangeError(
                    f"Начало диапазона {start} за пределами "
                    f"(всего {kind}: {total})"
                )

        # --- end ---
        if right in ('', 'end', 'all'):
            end = total
        elif right.startswith('end'):
            if right == 'end':
                end = total
            else:
                raise InvalidRangeError(
                    f"Нельзя использовать '{right}' в конце диапазона.\n"
                    f"  Для последних N используйте 'last N':\n"
                    f"      ❌  s[2:{right}]\n"
                    f"      ✅  s[last N]"
                )
        elif right.startswith('last'):
            raise InvalidRangeError(
                f"Нельзя использовать 'last' в диапазоне.\n"
                f"  Для последних N используйте 'last N':\n"
                f"      ❌  s[2:{right}]\n"
                f"      ✅  s[last N]"
            )
        else:
            try:
                end = int(right)
            except ValueError:
                raise InvalidRangeError(
                    f"Неверный конец диапазона: '{right}'"
                )
            if end < 1 or end > total:
                raise OutOfRangeError(
                    f"Конец диапазона {end} за пределами "
                    f"(всего {kind}: {total})"
                )

        if start > end:
            return (start, end)

        return (start, end)

    # ============================================================
    # 4. НЕИЗВЕСТНАЯ ФОРМА
    # ============================================================
    raise InvalidIndexSpecError(f"Неверная спецификация индекса: '{spec}'")


# ============================================================
# РАЗРЕШЕНИЕ СТОЛБЦА
# ============================================================

def resolve_column_index(matrix_obj, col_spec, env=None, allow_range=False):
    """
    Возвращает (idx_0based, skip_header).

    skip_header=True  — если col_spec это СТРОКА-имя ("Отдел")
    skip_header=False — если число / end / end-N / last N
    """
    col_val = _unwrap(col_spec, env)

    # ============================================================
    # ЧИСЛО
    # ============================================================
    if isinstance(col_val, (int, float)):
        n = int(col_val)
        if n < 1 or n > matrix_obj.cols:
            raise OutOfRangeError(
                f"Столбец {n} за пределами "
                f"(всего столбцов: {matrix_obj.cols})"
            )
        return (n - 1, False)

    if not isinstance(col_val, str):
        raise InvalidIndexSpecError(f"Неверный тип столбца: {type(col_val)}")

    s = col_val.strip().lower()

    # --- end ---
    if s == 'end':
        return (matrix_obj.cols - 1, False)

    # --- end-N ---
    if s.startswith('end-'):
        try:
            n = int(s[4:].strip())
        except ValueError:
            raise InvalidIndexSpecError(f"Неверный формат: '{col_val}'")
        idx = matrix_obj.cols - n - 1
        if idx < 0:
            raise OutOfRangeError(
                f"Столбец 'end-{n}' за пределами "
                f"(всего столбцов: {matrix_obj.cols})"
            )
        return (idx, False)

    # --- end+N — ошибка при чтении ---
    if s.startswith('end+'):
        raise InvalidRangeError(
            f"'end+N' нельзя использовать для чтения.\n"
            f"  Для расширения матрицы используйте присваивание:\n"
            f"      m[:, end+1] = [...]"
        )

    # --- last N ---
    if s.startswith('last'):
        rest = s[4:].strip()
        if rest == '':
            raise InvalidRangeError(
                "Укажите количество: 'last 1', 'last 2' и т.д."
            )
        try:
            n = int(rest)
        except ValueError:
            raise InvalidIndexSpecError(f"Неверный формат: '{col_val}'")

        if n < 1:
            raise OutOfRangeError(f"'last {n}' — N должно быть >= 1")
        if n == 1:
            return (matrix_obj.cols - 1, False)

        raise MultipleColumnsError(
            f"Указано несколько столбцов: 'last {n}'.\n"
            f"  Для функций чтения укажите ОДИН столбец.\n"
            f"  Если нужно сравнить несколько столбцов — "
            f"используйте and/or."
        )

    # --- : / all ---
    if s in (':', 'all'):
        raise MultipleColumnsError(
            f"Указано ':' (все столбцы).\n"
            f"  Для функций чтения укажите ОДИН столбец."
        )

    # --- ДИАПАЗОН ---
    if ':' in s:
        raise MultipleColumnsError(
            f"Указан диапазон столбцов: '{col_val}'.\n"
            f"  Для функций чтения укажите ОДИН столбец."
        )

    # --- ИМЯ СТОЛБЦА В ЗАГОЛОВКАХ ---
    if matrix_obj.rows > 0:
        headers = matrix_obj.data[0]
        headers_lower = [
            str(h).lower().strip() if h is not None else None
            for h in headers
        ]
        if s in headers_lower:
            return (headers_lower.index(s), True)

    raise ColumnNotFoundError(f"Столбец '{col_val}' не найден")


# ============================================================
# РАЗРЕШЕНИЕ СТРОКИ
# ============================================================

def resolve_row_index(matrix_obj, row_spec, env=None):
    """
    Возвращает (idx_0based, skip_header).

    skip_header=True  — если row_spec это СТРОКА-имя (значение в 1-м столбце)
    skip_header=False — если число / end / end-N / last N
    """
    row_val = _unwrap(row_spec, env)

    # ============================================================
    # ЧИСЛО
    # ============================================================
    if isinstance(row_val, (int, float)):
        n = int(row_val)
        if n < 1 or n > matrix_obj.rows:
            raise OutOfRangeError(
                f"Строка {n} за пределами "
                f"(всего строк: {matrix_obj.rows})"
            )
        return (n - 1, False)

    if not isinstance(row_val, str):
        raise InvalidIndexSpecError(f"Неверный тип строки: {type(row_val)}")

    s = row_val.strip().lower()

    # --- end ---
    if s == 'end':
        return (matrix_obj.rows - 1, False)

    # --- end-N ---
    if s.startswith('end-'):
        try:
            n = int(s[4:].strip())
        except ValueError:
            raise InvalidIndexSpecError(f"Неверный формат: '{row_val}'")
        idx = matrix_obj.rows - n - 1
        if idx < 0:
            raise OutOfRangeError(
                f"Строка 'end-{n}' за пределами "
                f"(всего строк: {matrix_obj.rows})"
            )
        return (idx, False)

    # --- end+N — ошибка при чтении ---
    if s.startswith('end+'):
        raise InvalidRangeError(
            f"'end+N' нельзя использовать для чтения.\n"
            f"  Для расширения матрицы используйте присваивание:\n"
            f"      m[end+1, :] = [...]"
        )

    # --- last N ---
    if s.startswith('last'):
        rest = s[4:].strip()
        if rest == '':
            raise InvalidRangeError(
                "Укажите количество: 'last 1', 'last 2' и т.д."
            )
        try:
            n = int(rest)
        except ValueError:
            raise InvalidIndexSpecError(f"Неверный формат: '{row_val}'")

        if n < 1:
            raise OutOfRangeError(f"'last {n}' — N должно быть >= 1")
        if n == 1:
            return (matrix_obj.rows - 1, False)

        raise MultipleRowsError(
            f"Указано несколько строк: 'last {n}'.\n"
            f"  Для функций чтения укажите ОДНУ строку."
        )

    # --- : / all — ошибка ---
    if s in (':', 'all'):
        raise MultipleRowsError(
            f"Указано ':' (все строки).\n"
            f"  Для функций чтения укажите ОДНУ строку."
        )

    # --- ДИАПАЗОН — ошибка ---
    if ':' in s:
        raise MultipleRowsError(
            f"Указан диапазон строк: '{row_val}'.\n"
            f"  Для функций чтения укажите ОДНУ строку."
        )

    # --- ПОИСК ПО ЗНАЧЕНИЮ В ПЕРВОМ СТОЛБЦЕ ---
    for i in range(1, matrix_obj.rows):
        if i < len(matrix_obj.data) and len(matrix_obj.data[i]) > 0:
            cell = matrix_obj.data[i][0]
            if cell is not None and str(cell).lower().strip() == s:
                return (i, True)

    raise RowNotFoundError(
        f"Строка '{row_val}' не найдена в первом столбце"
    )


# ============================================================
# ХЕЛПЕР: РАЗВЁРТКА УЗЛА
# ============================================================

def _unwrap(spec, env):
    """Вычисляет узел, если это узел"""
    if hasattr(spec, 'evaluate'):
        try:
            return spec.evaluate(env)
        except Exception:
            try:
                return spec.evaluate(None)
            except Exception:
                return spec
    return spec


# ============================================================
# СТАРЫЕ ФУНКЦИИ (для обратной совместимости)
# ============================================================

def normalize_row_index(matrix_obj, row_val):
    """DEPRECATED."""
    idx, _ = resolve_row_index(matrix_obj, row_val, None)
    return idx + 1


def normalize_col_index(matrix_obj, col_val):
    """DEPRECATED."""
    idx, _ = resolve_column_index(matrix_obj, col_val, None)
    return idx + 1


def get_value_from_node(node, env):
    if hasattr(node, 'evaluate'):
        return node.evaluate(env)
    return node


def is_row_keyword(val):
    if isinstance(val, str):
        return val.lower() == 'row'
    return False


def is_column_keyword(val):
    if isinstance(val, str):
        return val.lower() in ['column', 'col']
    return False


def is_special_index(val):
    if isinstance(val, str):
        val_lower = val.lower()
        return (val_lower in ['end', 'last'] or
                val_lower.startswith('end+') or
                val_lower.startswith('end-') or
                val_lower.startswith('last '))
    return False


def parse_index_value(val, env):
    if isinstance(val, str):
        val_lower = val.lower()
        if val_lower.startswith('end+') or val_lower.startswith('end-'):
            return val
    return val


# ============================================================
# ЭКСПОРТ
# ============================================================

__all__ = [
    'parse_range_spec',
    'resolve_column_index',
    'resolve_row_index',

    'ColumnNotFoundError',
    'RowNotFoundError',
    'MultipleColumnsError',
    'MultipleRowsError',
    'OutOfRangeError',
    'InvalidRangeError',
    'InvalidIndexSpecError',

    'normalize_row_index',
    'normalize_col_index',
    'get_value_from_node',
    'is_row_keyword',
    'is_column_keyword',
    'is_special_index',
    'parse_index_value',
]