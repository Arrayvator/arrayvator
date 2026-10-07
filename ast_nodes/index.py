# ast_nodes/index.py
from .base import Node
from runtime.matrix import MatrExMatrix
from runtime.random_source import forbid_random


# ============================================================
# ХЕЛПЕРЫ ДЛЯ DUCKDB
# ============================================================
def _is_duckdb(val):
    try:
        from duckdb_engine import DuckDBTable
        return isinstance(val, DuckDBTable)
    except ImportError:
        return False


def _is_row_all(spec):
    """Проверяет, что спецификация — : или all."""
    if isinstance(spec, str):
        return spec.strip().lower() in (':', 'all')
    return False


def _is_col_all(spec):
    """Проверяет, что спецификация — : или all."""
    if isinstance(spec, str):
        return spec.strip().lower() in (':', 'all')
    return False


def _resolve_row_number(spec, total_rows):
    """Преобразует спецификацию строки в 1-based номер."""
    if isinstance(spec, (int, float)):
        return int(spec)

    if isinstance(spec, str):
        s = spec.strip().lower()

        if s == 'end':
            return total_rows
        if s.startswith('end-'):
            try:
                n = int(s[4:].strip())
                return total_rows - n
            except ValueError:
                pass
        try:
            return int(s)
        except ValueError:
            pass

    raise ValueError(f"DuckDB: не удалось определить номер строки из '{spec}'")


def _find_column_name(columns, spec):
    """Ищет имя столбца по спецификации (имя или номер)."""
    if isinstance(spec, (int, float)):
        n = int(spec)
        if 1 <= n <= len(columns):
            return columns[n - 1]
        return None

    if isinstance(spec, str):
        s = spec.strip().lower()

        if s == 'end':
            return columns[-1] if columns else None
        if s.startswith('end-'):
            try:
                n = int(s[4:].strip())
                idx = len(columns) - n - 1
                if 0 <= idx < len(columns):
                    return columns[idx]
            except ValueError:
                pass
        if s.startswith('last'):
            try:
                n = int(s[4:].strip())
                idx = len(columns) - n
                if 0 <= idx < len(columns):
                    return columns[idx]
            except ValueError:
                pass

        # По имени
        for c in columns:
            if str(c).lower().strip() == s:
                return c

    return None


# ============================================================
# INDEX NODE
# ============================================================
class IndexNode(Node):
    def __init__(self, matrix, indices):
        self.matrix = matrix
        self.indices = indices

    def _parse_range(self, range_str, max_val):
        parts = range_str.split(':')
        start = parts[0].strip()
        end = parts[1].strip() if len(parts) > 1 else 'end'

        if start == '' or start == 'begin':
            start = 1
        elif start.lower() == 'end':
            start = max_val
        elif start.lower().startswith('last'):
            try:
                n = int(start.lower().replace('last', '').strip())
                start = max_val - n + 1
                if start < 1:
                    start = 1
            except:
                start = 1
        elif start.lower().startswith('end+'):
            try:
                n = int(start.lower().replace('end+', '').strip())
                start = max_val + n
            except:
                start = max_val
        elif start.lower().startswith('end-'):
            try:
                n = int(start.lower().replace('end-', '').strip())
                start = max_val - n
                if start < 1:
                    start = 1
            except:
                start = max_val
        else:
            start = int(start)

        if end == '' or end == 'end' or end.lower() == 'end':
            end = max_val
        elif end.lower().startswith('last'):
            try:
                n = int(end.lower().replace('last', '').strip())
                end = max_val - n + 1
                if end < 1:
                    end = 1
            except:
                end = max_val
        elif end.lower().startswith('end+'):
            try:
                n = int(end.lower().replace('end+', '').strip())
                end = max_val + n
            except:
                end = max_val
        elif end.lower().startswith('end-'):
            try:
                n = int(end.lower().replace('end-', '').strip())
                end = max_val - n
                if end < 1:
                    end = 1
            except:
                end = max_val
        else:
            end = int(end)

        if start > end:
            start, end = end, start

        return start, end

    def _is_range(self, value):
        return isinstance(value, str) and ':' in value

    def _process_special_index(self, idx, max_val):
        if idx is None:
            return None

        if isinstance(idx, str):
            idx_lower = idx.lower()

            if idx_lower == 'all':
                return 'all'

            if idx_lower == 'end':
                return max_val

            if idx_lower.startswith('last'):
                try:
                    n = int(idx_lower.replace('last', '').strip())
                    if n <= 0:
                        return None
                    start = max_val - n + 1
                    if start < 1:
                        start = 1
                    return ('range', start, max_val)
                except:
                    return None

            if idx_lower.startswith('end+'):
                try:
                    n = int(idx_lower.replace('end+', '').strip())
                    return max_val + n
                except:
                    return None

            if idx_lower.startswith('end-'):
                try:
                    n = int(idx_lower.replace('end-', '').strip())
                    return max_val - n
                except:
                    return None

        return idx

    def evaluate(self, env):
        matrix_obj = self.matrix.evaluate(env)

        # ============================================================
        # DUCKDB (BigData)
        # ============================================================
        if _is_duckdb(matrix_obj):
            return self._evaluate_duckdb(matrix_obj, env)

        if not hasattr(matrix_obj, 'data'):
            if isinstance(matrix_obj, list):
                idx_val = self.indices[0].evaluate(env)
                forbid_random(idx_val, "индекс")
                idx = idx_val
                if isinstance(idx, int) and 1 <= idx <= len(matrix_obj):
                    return matrix_obj[idx - 1]
                raise TypeError("Индекс должен быть числом")
            raise TypeError("Объект не является матрицей")

        indices = []
        for idx_node in self.indices:
            idx_val = idx_node.evaluate(env)
            forbid_random(idx_val, "индекс")
            indices.append(idx_val)

        if len(indices) == 1:
            return self._evaluate_single(matrix_obj, indices[0])
        elif len(indices) == 2:
            return self._evaluate_double(matrix_obj, indices[0], indices[1])
        else:
            raise RuntimeError("Неверное количество индексов")

    # ============================================================
    # DUCKDB
    # ============================================================
    def _evaluate_duckdb(self, duck_table, env):
        """
        Индексация DuckDB:
            big[0, :]           → заголовки (вектор)
            big[1, :]           → 1-я строка данных (вектор)
            big[end, :]         → последняя строка (вектор)
            big[:, "X"]         → столбец (вектор значений)
            big[N, "X"]         → одна ячейка (скаляр)
        """
        if len(self.indices) != 2:
            raise TypeError(
                "DuckDB: поддерживается только два индекса [row, col]"
            )

        row_spec_node = self.indices[0]
        col_spec_node = self.indices[1]

        row_spec = (row_spec_node.evaluate(env)
                    if hasattr(row_spec_node, 'evaluate')
                    else row_spec_node)
        col_spec = (col_spec_node.evaluate(env)
                    if hasattr(col_spec_node, 'evaluate')
                    else col_spec_node)

        columns = duck_table.get_columns()
        total_rows = duck_table.get_row_count()

        # --- Случай 1: big[0, :] — заголовки ---
        if row_spec == 0 or row_spec == '0':
            if _is_col_all(col_spec):
                return MatrExMatrix(list(columns), False)
            raise TypeError(
                "DuckDB: big[0, col] — поддерживается только big[0, :]\n"
                "  Для заголовков используйте: big[0, :]"
            )

        # --- Случай 2: big[:, "X"] — столбец ---
        if _is_row_all(row_spec):
            if _is_col_all(col_spec):
                raise TypeError(
                    "DuckDB: big[:, :] не поддерживается.\n"
                    "  Используйте print(big) для просмотра."
                )

            col_name = _find_column_name(columns, col_spec)
            if col_name is None:
                raise ValueError(
                    f"DuckDB: столбец '{col_spec}' не найден.\n"
                    f"  Доступны: {columns}"
                )

            safe_col = '"' + str(col_name).replace('"', '""') + '"'
            sql = f'SELECT {safe_col} FROM {duck_table.table_name}'
            try:
                rows = duck_table.con.execute(sql).fetchall()
            except Exception as e:
                raise RuntimeError(f"DuckDB: ошибка чтения столбца: {e}")

            values = [r[0] for r in rows]
            return MatrExMatrix(values, False)

        # --- Случай 3: big[N, :] — конкретная строка ---
        if _is_col_all(col_spec):
            row_num = _resolve_row_number(row_spec, total_rows)

            if row_num < 1 or row_num > total_rows:
                raise IndexError(
                    f"DuckDB: строка {row_num} вне диапазона "
                    f"(всего {total_rows})"
                )

            sql = f"SELECT * FROM {duck_table.table_name} LIMIT 1 OFFSET {row_num - 1}"
            try:
                rows = duck_table.con.execute(sql).fetchall()
            except Exception as e:
                raise RuntimeError(f"DuckDB: ошибка чтения строки: {e}")

            if not rows:
                return MatrExMatrix([], False)

            return MatrExMatrix(list(rows[0]), False)

        # --- Случай 4: big[N, "X"] — одна ячейка ---
        col_name = _find_column_name(columns, col_spec)
        if col_name is None:
            raise ValueError(f"DuckDB: столбец '{col_spec}' не найден")

        row_num = _resolve_row_number(row_spec, total_rows)
        if row_num < 1 or row_num > total_rows:
            raise IndexError(
                f"DuckDB: строка {row_num} вне диапазона "
                f"(всего {total_rows})"
            )

        safe_col = '"' + str(col_name).replace('"', '""') + '"'
        sql = (
            f"SELECT {safe_col} FROM {duck_table.table_name} "
            f"LIMIT 1 OFFSET {row_num - 1}"
        )
        try:
            rows = duck_table.con.execute(sql).fetchall()
        except Exception as e:
            raise RuntimeError(f"DuckDB: ошибка чтения ячейки: {e}")

        if not rows:
            return None
        return rows[0][0]

    # ============================================================
    # MATRIX: 1 индекс
    # ============================================================
    def _evaluate_single(self, matrix_obj, idx):
        if isinstance(idx, str):
            idx_lower = idx.lower()

            if idx_lower == 'all':
                if matrix_obj.is_2d:
                    return MatrExMatrix([row.copy() for row in matrix_obj.data], True)
                else:
                    return MatrExMatrix(matrix_obj.data.copy(), False)

            if idx_lower == 'end':
                if matrix_obj.is_2d:
                    if matrix_obj.rows > 0:
                        return matrix_obj.data[-1]
                    return None
                else:
                    if len(matrix_obj.data) > 0:
                        return matrix_obj.data[-1]
                    return None

            if idx_lower.startswith('last'):
                try:
                    n = int(idx_lower.replace('last', '').strip())
                    if n <= 0:
                        return None
                    if matrix_obj.is_2d:
                        start = max(0, matrix_obj.rows - n)
                        return MatrExMatrix([row.copy() for row in matrix_obj.data[start:]], True)
                    else:
                        start = max(0, len(matrix_obj.data) - n)
                        return MatrExMatrix(matrix_obj.data[start:].copy(), False)
                except:
                    pass

        if self._is_range(idx):
            start, end = self._parse_range(idx, matrix_obj.rows)
            if matrix_obj.is_2d:
                result = []
                for i in range(start - 1, end):
                    if i < len(matrix_obj.data):
                        result.append(matrix_obj.data[i].copy())
                    else:
                        result.append([None] * matrix_obj.cols)
                return MatrExMatrix(result, True)
            else:
                if start - 1 < len(matrix_obj.data):
                    return MatrExMatrix(matrix_obj.data[start - 1:end].copy(), False)
                return MatrExMatrix([], False)

        if isinstance(idx, int):
            if idx < 1:
                raise IndexError("Индекс должен быть >= 1")
            if matrix_obj.is_2d:
                if idx > matrix_obj.rows:
                    return None
                if idx <= len(matrix_obj.data):
                    return matrix_obj.data[idx - 1]
                return None
            else:
                if idx > len(matrix_obj.data):
                    return None
                return matrix_obj.data[idx - 1]

        raise TypeError(f"Неверный индекс: {idx}")

    # ============================================================
    # MATRIX: 2 индекса
    # ============================================================
    def _evaluate_double(self, matrix_obj, row, col):
        row_processed = self._process_special_index(row, matrix_obj.rows) if isinstance(row, str) else row

        row_kind = None
        row_start = None
        row_end = None
        row_name = None
        row_is_name = False    # ← НОВОЕ: строка найдена по имени

        if row_processed == 'all' or row == 'all':
            row_kind = 'all'
        elif isinstance(row_processed, tuple) and row_processed[0] == 'range':
            row_kind = 'range'
            row_start = row_processed[1]
            row_end = row_processed[2]
        elif isinstance(row_processed, int):
            row_kind = 'single'
            row_start = row_processed
            row_end = row_processed
        elif isinstance(row_processed, str) and ':' in row_processed:
            row_kind = 'range'
            row_start, row_end = self._parse_range(row_processed, matrix_obj.rows)
        elif isinstance(row_processed, str):
            row_kind = 'name'
            row_name = row_processed
            row_is_name = True
        else:
            row_kind = 'all'

        col_processed = self._process_special_index(col, matrix_obj.cols) if isinstance(col, str) else col

        col_kind = None
        col_start = None
        col_end = None
        col_name = None
        col_is_name = False    # ← НОВОЕ: столбец найден по имени

        if col_processed == 'all' or col == 'all':
            col_kind = 'all'
        elif isinstance(col_processed, tuple) and col_processed[0] == 'range':
            col_kind = 'range'
            col_start = col_processed[1]
            col_end = col_processed[2]
        elif isinstance(col_processed, int):
            col_kind = 'single'
            col_start = col_processed
            col_end = col_processed
        elif isinstance(col_processed, str) and ':' in col_processed:
            col_kind = 'range'
            col_start, col_end = self._parse_range(col_processed, matrix_obj.cols)
        elif isinstance(col_processed, str):
            headers = matrix_obj.data[0] if matrix_obj.rows > 0 else []
            headers_lower = [str(h).lower() if h is not None else None for h in headers]
            if col_processed.lower() in headers_lower:
                col_kind = 'single'
                col_start = headers_lower.index(col_processed.lower()) + 1
                col_end = col_start
                col_is_name = True    # ← НОВОЕ: столбец найден по имени
            else:
                col_kind = 'all'
        else:
            col_kind = 'all'

        if row_kind == 'all':
            r_start = 1
            r_end = matrix_obj.rows
        elif row_kind == 'single':
            r_start = row_start
            r_end = row_end
        elif row_kind == 'range':
            r_start = row_start
            r_end = row_end
        elif row_kind == 'name':
            r_start = None
            r_end = None
            for i in range(matrix_obj.rows):
                if i < len(matrix_obj.data) and len(matrix_obj.data[i]) > 0:
                    cell = matrix_obj.data[i][0]
                    if cell is not None and str(cell).lower() == row_name.lower():
                        r_start = i + 1
                        r_end = i + 1
                        break
            if r_start is None:
                return None
        else:
            r_start = 1
            r_end = matrix_obj.rows

        if col_kind == 'all':
            c_start = 1
            c_end = matrix_obj.cols
        elif col_kind == 'single':
            c_start = col_start
            c_end = col_end
        elif col_kind == 'range':
            c_start = col_start
            c_end = col_end
        else:
            c_start = 1
            c_end = matrix_obj.cols

        if r_end > matrix_obj.rows:
            r_end = matrix_obj.rows
        if c_end > matrix_obj.cols:
            c_end = matrix_obj.cols

        if r_start > r_end or c_start > c_end:
            return MatrExMatrix([], True)

        r_is_single = (r_start == r_end)
        c_is_single = (c_start == c_end)
        r_is_all = (r_start == 1 and r_end == matrix_obj.rows)
        c_is_all = (c_start == 1 and c_end == matrix_obj.cols)

        # ============================================================
        # ОДНА ЯЧЕЙКА
        # ============================================================
        if r_is_single and c_is_single:
            r_idx = r_start - 1
            c_idx = c_start - 1
            if r_idx < len(matrix_obj.data) and c_idx < len(matrix_obj.data[r_idx]):
                return matrix_obj.data[r_idx][c_idx]
            return None

        # ============================================================
        # СТОЛБЕЦ — вектор
        # ============================================================
        if r_is_all and c_is_single:
            c_idx = c_start - 1
            result = []

            # ВАЖНО: если столбец найден ПО ИМЕНИ — пропускаем заголовок
            start_row = 1 if col_is_name else 0

            for i in range(start_row, matrix_obj.rows):
                if i < len(matrix_obj.data):
                    row_data = matrix_obj.data[i]
                    if c_idx < len(row_data):
                        result.append(row_data[c_idx])
                    else:
                        result.append(None)
                else:
                    result.append(None)
            return MatrExMatrix(result, False)

        # ============================================================
        # СТРОКА — вектор
        # ============================================================
        if r_is_single and c_is_all:
            r_idx = r_start - 1
            if r_idx < len(matrix_obj.data):
                return MatrExMatrix(matrix_obj.data[r_idx].copy(), False)
            return MatrExMatrix([], False)

        # ============================================================
        # СТОЛБЦЫ: диапазон строк × один столбец — вектор
        # ============================================================
        if not r_is_single and c_is_single:
            c_idx = c_start - 1
            result = []

            # ВАЖНО: если столбец найден ПО ИМЕНИ — начинаем со строки 1
            start_row = r_start - 1
            if col_is_name and start_row == 0:
                start_row = 1

            for i in range(start_row, r_end):
                if i < len(matrix_obj.data):
                    row_data = matrix_obj.data[i]
                    if c_idx < len(row_data):
                        result.append(row_data[c_idx])
                    else:
                        result.append(None)
                else:
                    result.append(None)
            return MatrExMatrix(result, False)

        # ============================================================
        # СТРОКИ: одна строка × диапазон столбцов — вектор
        # ============================================================
        if r_is_single and not c_is_single:
            r_idx = r_start - 1
            if r_idx < len(matrix_obj.data):
                row_data = matrix_obj.data[r_idx]
                result = []
                for c in range(c_start - 1, c_end):
                    if c < len(row_data):
                        result.append(row_data[c])
                    else:
                        result.append(None)
                return MatrExMatrix(result, False)
            return MatrExMatrix([], False)

        # ============================================================
        # МАТРИЦА: диапазон × диапазон
        # ============================================================
        result = []

        # ВАЖНО: если столбец найден ПО ИМЕНИ — пропускаем заголовок
        start_row = r_start - 1
        if col_is_name and start_row == 0:
            start_row = 1

        for i in range(start_row, r_end):
            if i < len(matrix_obj.data):
                row_data = matrix_obj.data[i]
                new_row = []
                for c in range(c_start - 1, c_end):
                    if c < len(row_data):
                        new_row.append(row_data[c])
                    else:
                        new_row.append(None)
                result.append(new_row)
            else:
                result.append([None] * (c_end - c_start + 1))
        return MatrExMatrix(result, True)

    def __repr__(self):
        return f"Index({self.matrix}[{self.indices}])"