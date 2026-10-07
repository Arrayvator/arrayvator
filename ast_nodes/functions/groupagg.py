# ast_nodes/functions/groupagg.py
"""
Функция GROUPAGG — блочная агрегация с группировкой по маркеру.

⚠️  РАБОТАЕТ ТОЛЬКО С MATRIX (RAM).
    НЕ работает с BigData (DuckDB).

СИНТАКСИС:
    r = groupagg(m[:, "Клиент"], m[:, "Сумма"], sum)
    r = groupagg(m[:, "Клиент"], m[:, "Сумма"], sum, "ИТОГО")
    r = groupagg(m[:, "Клиент"], m[:, "Сумма"], sum, "ИТОГО", fill)
    r = groupagg(m[:, "Клиент"], m[:, "Сумма"], sum, "ИТОГО", exact)

РЕЖИМЫ:
    fill  — пустые (None, "") присоединяются к текущему блоку (по умолчанию).
    exact — каждое значение — отдельный блок (даже пустое).

ЛОГИКА:
    - Идёт по столбцу-маркеру.
    - Определяет границы блоков.
    - Считает агрегат за блок.
    - Вставляет итог ПОСЛЕ блока.
    - Последний блок — итог в конец.
    - Итоговая строка: первый столбец — None (или "ИТОГО"),
      столбец агрегата — число, остальные — None.
"""

from ..base import Node
from runtime.matrix import MatrExMatrix
from ..utils.index_utils import resolve_column_index


def _is_duckdb(val):
    try:
        from duckdb_engine import DuckDBTable
        return isinstance(val, DuckDBTable)
    except ImportError:
        return False


def _is_empty(val):
    """Пустое значение: None или пустая строка."""
    return val is None or (isinstance(val, str) and val.strip() == "")


def _normalize(val):
    """Нормализация для сравнения."""
    if val is None:
        return None
    if isinstance(val, str):
        return val.strip()
    return val


# ============================================================
# GROUPAGG NODE
# ============================================================
class GroupAggNode(Node):
    def __init__(self, key_slice, value_slice, agg, name=None, mode=None):
        self.key_slice = key_slice
        self.value_slice = value_slice
        self.agg = agg
        self.name = name
        self.mode = mode

    def evaluate(self, env):
        from ast_nodes.index import IndexNode
        from errors import ArrayVatorError

        # 1. Проверка: срезы
        if not isinstance(self.key_slice, IndexNode):
            raise ArrayVatorError(
                code="GROUPAGG_BAD_KEY_SLICE",
                context=None,
                message=(
                    "groupagg: 1-й аргумент — срез m[:, \"X\"].\n"
                    "  Пример: groupagg(m[:, \"Клиент\"], m[:, \"Сумма\"], sum)"
                ),
                suggestion=(
                    "Первый аргумент — срез столбца-маркера:\n"
                    "     m[:, \"Клиент\"]\n"
                    "     m[:, 1]\n"
                    "\n"
                    "Правильно:\n"
                    "     groupagg(m[:, \"Клиент\"], m[:, \"Сумма\"], sum)"
                ),
            )

        if not isinstance(self.value_slice, IndexNode):
            raise ArrayVatorError(
                code="GROUPAGG_BAD_VALUE_SLICE",
                context=None,
                message=(
                    "groupagg: 2-й аргумент — срез m[:, \"X\"].\n"
                    "  Пример: groupagg(m[:, \"Клиент\"], m[:, \"Сумма\"], sum)"
                ),
                suggestion=(
                    "Второй аргумент — срез столбца-значения:\n"
                    "     m[:, \"Сумма\"]\n"
                    "     m[:, 2]\n"
                    "\n"
                    "Правильно:\n"
                    "     groupagg(m[:, \"Клиент\"], m[:, \"Сумма\"], sum)"
                ),
            )

        # 2. Извлекаем матрицу
        matrix_obj = self.key_slice.matrix.evaluate(env)

        # ============================================================
        # ВАЖНО: сначала проверяем BigData (DuckDB)
        # ============================================================
        if _is_duckdb(matrix_obj):
            raise ArrayVatorError(
                code="GROUPAGG_DUCKDB",
                context=None,
                message=(
                    "groupagg работает только с Matrix (RAM), "
                    "не с BigData (DuckDB).\n"
                    "  BigData — read-only view на файл."
                ),
                suggestion=(
                    "BigData (DuckDB) — read-only view на файл.\n"
                    "Он НЕ поддерживает блочную агрегацию.\n"
                    "\n"
                    "Решение:\n"
                    "  1. Конвертировать BigData в Matrix:\n"
                    "        m = ToMatrix(bd)\n"
                    "        r = groupagg(m[:, \"Клиент\"], m[:, \"Сумма\"], sum)\n"
                    "\n"
                    "  2. Использовать SQL-аналог:\n"
                    "        groupby, pivot"
                ),
            )

        if not hasattr(matrix_obj, 'data') or not matrix_obj.is_2d:
            raise ArrayVatorError(
                code="GROUPAGG_BAD_SYNTAX",
                context=None,
                message=(
                    "groupagg: ожидается матрица.\n"
                    "  Пример: groupagg(m[:, \"Клиент\"], m[:, \"Сумма\"], sum)"
                ),
            )

        # ============================================================
        # НОРМАЛИЗАЦИЯ AGGREGATE
        # ============================================================
        # Если по какой-то причине в self.agg оказался узел,
        # а не строка — разворачиваем его
        agg_raw = self.agg
        if hasattr(agg_raw, 'evaluate'):
            agg_raw = agg_raw.evaluate(env)
        if hasattr(agg_raw, 'value'):
            agg_raw = agg_raw.value
        self.agg = str(agg_raw).strip().lower()

        # 3. Индексы столбцов
        key_col_idx = self._resolve_col(self.key_slice, matrix_obj, env)
        val_col_idx = self._resolve_col(self.value_slice, matrix_obj, env)

        # 4. Имя итога
        name_val = None
        if self.name is not None:
            name_val = (self.name.evaluate(env)
                        if hasattr(self.name, 'evaluate')
                        else self.name)

        # 5. Режим
        mode_val = 'fill'
        if self.mode is not None:
            mode_val = (self.mode.evaluate(env)
                        if hasattr(self.mode, 'evaluate')
                        else self.mode)
            if isinstance(mode_val, str):
                mode_val = mode_val.lower()
            if mode_val not in ('fill', 'exact'):
                raise ArrayVatorError(
                    code="GROUPAGG_BAD_MODE",
                    context=None,
                    message=(
                        f"groupagg: режим должен быть 'fill' или 'exact', "
                        f"получен '{mode_val}'"
                    ),
                    suggestion=(
                        "Допустимо только два режима:\n"
                        "     fill  — пустые значения присоединяются к блоку\n"
                        "     exact — каждое значение — отдельный блок"
                    ),
                )

        # 6. Определяем блоки
        blocks = self._find_blocks(matrix_obj, key_col_idx, mode_val)

        # 7. Считаем агрегаты
        result_data = []
        n_cols = matrix_obj.cols

        for block in blocks:
            for row_idx in block['rows']:
                if row_idx < len(matrix_obj.data):
                    row = matrix_obj.data[row_idx]
                    result_data.append(
                        list(row) if isinstance(row, list) else [row]
                    )

            agg_value = self._apply_agg(block['rows'], matrix_obj, val_col_idx)

            summary_row = [None] * n_cols
            if name_val is not None:
                summary_row[0] = name_val
            if val_col_idx < n_cols:
                summary_row[val_col_idx] = agg_value

            result_data.append(summary_row)

        # 8. Выравнивание
        if result_data:
            max_cols = max(len(r) for r in result_data)
            for r in result_data:
                while len(r) < max_cols:
                    r.append(None)

        return MatrExMatrix(result_data, True)

    # ============================================================
    # ПОИСК БЛОКОВ
    # ============================================================
    def _find_blocks(self, matrix_obj, key_col_idx, mode):
        blocks = []

        current_value = None
        current_rows = []

        for i in range(1, matrix_obj.rows):
            if i >= len(matrix_obj.data):
                break
            row = matrix_obj.data[i]
            key_value = row[key_col_idx] if key_col_idx < len(row) else None

            if mode == 'exact':
                if current_rows:
                    blocks.append({'rows': current_rows})
                    current_rows = []
                current_rows.append(i)
                blocks.append({'rows': current_rows})
                current_rows = []

            else:  # fill
                if _is_empty(key_value):
                    current_rows.append(i)
                else:
                    if current_value is None:
                        current_value = _normalize(key_value)
                        current_rows.append(i)
                    else:
                        if _normalize(key_value) == current_value:
                            current_rows.append(i)
                        else:
                            if current_rows:
                                blocks.append({'rows': current_rows})
                            current_value = _normalize(key_value)
                            current_rows = [i]

        if current_rows:
            blocks.append({'rows': current_rows})

        return blocks

    # ============================================================
    # АГРЕГАЦИЯ
    # ============================================================
    def _apply_agg(self, rows, matrix_obj, col_idx):
        from errors import ArrayVatorError

        values = []
        for i in rows:
            if i < len(matrix_obj.data):
                row = matrix_obj.data[i]
                if col_idx < len(row):
                    values.append(row[col_idx])

        # ============================================================
        # COUNT — до проверки nums, потому что count работает с любыми
        # ============================================================
        if self.agg == 'count':
            return len(values)

        # ============================================================
        # Остальные агрегаты — только с числами
        # ============================================================
        nums = []
        for v in values:
            if isinstance(v, (int, float)) and not isinstance(v, bool):
                nums.append(v)

        if not nums:
            return None

        if self.agg == 'sum':
            return sum(nums)
        if self.agg == 'avg':
            return sum(nums) / len(nums)
        if self.agg == 'min':
            return min(nums)
        if self.agg == 'max':
            return max(nums)
        if self.agg == 'median':
            s = sorted(nums)
            n = len(s)
            if n % 2 == 1:
                return s[n // 2]
            return (s[n // 2 - 1] + s[n // 2]) / 2
        if self.agg == 'std':
            mean = sum(nums) / len(nums)
            var = sum((x - mean) ** 2 for x in nums) / len(nums)
            return var ** 0.5
        if self.agg == 'first':
            return nums[0]
        if self.agg == 'last':
            return nums[-1]

        raise ArrayVatorError(
            code="GROUPAGG_BAD_AGG",
            context=None,
            message=(
                f"groupagg: неизвестный агрегат '{self.agg}'.\n"
                f"  Допустимо: sum, count, avg, min, max, median, std, first, last."
            ),
            suggestion=(
                "Допустимо:\n"
                "     sum, count, avg, min, max, median, std, first, last"
            ),
        )

    # ============================================================
    # РАЗРЕШЕНИЕ СТОЛБЦА
    # ============================================================
    def _resolve_col(self, index_node, matrix_obj, env):
        if len(index_node.indices) != 2:
            raise TypeError(
                "groupagg: ожидается срез m[:, \"X\"]"
            )

        col_spec_node = index_node.indices[1]
        col_spec = (col_spec_node.evaluate(env)
                    if hasattr(col_spec_node, 'evaluate')
                    else col_spec_node)

        idx, _ = resolve_column_index(matrix_obj, col_spec, env)
        return idx

    def __repr__(self):
        return f"groupagg({self.key_slice}, {self.value_slice}, {self.agg})"