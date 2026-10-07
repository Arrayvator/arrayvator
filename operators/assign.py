# operators/assign.py
from ast_nodes import Node, VariableNode, IndexNode, StringNode
from runtime.matrix import MatrExMatrix
from runtime.random_source import RandomSource, forbid_random
from errors import ArrayVatorError


class AssignNode(Node):
    def __init__(self, var_name, value, is_matrix=False, is_index=False, index_node=None):
        self.var_name = var_name.lower()
        self.value = value
        self.is_matrix = is_matrix
        self.is_index = is_index
        self.index_node = index_node

    # ============================================================
    # ХЕЛПЕРЫ
    # ============================================================

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

    def _ensure_rows(self, matrix, row_count):
        while len(matrix.data) < row_count:
            matrix.data.append([None] * matrix.cols)
        matrix.rows = len(matrix.data)

    def _ensure_cols(self, matrix, col_count):
        for row in matrix.data:
            if isinstance(row, list):
                while len(row) < col_count:
                    row.append(None)
        matrix.cols = len(matrix.data[0]) if matrix.data else 0

    def _is_scalar(self, val):
        return isinstance(val, (int, float, str, bool)) or val is None

    def _expand_and_fill(self, matrix, value):
        for i in range(matrix.rows):
            for j in range(matrix.cols):
                if i < len(matrix.data) and j < len(matrix.data[i]):
                    matrix.data[i][j] = value

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
                    return ('last_range', start, n)
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

    def _assign_range(self, matrix, row_start, row_end, col_start, col_end, value,
                      fill_rest_none=False):
        """
        Заполнение диапазона.
        fill_rest_none — если True и value — вектор, то лишние ячейки затираются None.
        """
        if row_start < 1 or col_start < 1:
            raise IndexError(f"Индексы должны быть >= 1")

        if row_end > matrix.rows:
            self._ensure_rows(matrix, row_end)
        if col_end > matrix.cols:
            self._ensure_cols(matrix, col_end)

        if isinstance(value, RandomSource):
            rows_count = row_end - row_start + 1
            cols_count = col_end - col_start + 1
            value = value.generate_2d(rows_count, cols_count)

        if hasattr(value, 'data'):
            val_data = value.data
        else:
            val_data = value

        if self._is_scalar(value):
            for i in range(row_start - 1, row_end):
                for j in range(col_start - 1, col_end):
                    if i < len(matrix.data) and j < len(matrix.data[i]):
                        matrix.data[i][j] = value
            return

        # 2D-матрица
        if isinstance(val_data, list) and val_data and isinstance(val_data[0], list):
            val_rows = len(val_data)
            for i in range(row_start - 1, row_end):
                row_idx = i - (row_start - 1)
                for j in range(col_start - 1, col_end):
                    col_idx = j - (col_start - 1)
                    if i < len(matrix.data) and j < len(matrix.data[i]):
                        if row_idx < val_rows and col_idx < len(val_data[row_idx]):
                            matrix.data[i][j] = val_data[row_idx][col_idx]
                        elif fill_rest_none:
                            matrix.data[i][j] = None
            return

        # 1D-вектор
        if isinstance(val_data, list):
            idx = 0
            for i in range(row_start - 1, row_end):
                for j in range(col_start - 1, col_end):
                    if i < len(matrix.data) and j < len(matrix.data[i]):
                        if idx < len(val_data):
                            matrix.data[i][j] = val_data[idx]
                            idx += 1
                        elif fill_rest_none:
                            matrix.data[i][j] = None
            return

        # Fallback: скаляр
        for i in range(row_start - 1, row_end):
            for j in range(col_start - 1, col_end):
                if i < len(matrix.data) and j < len(matrix.data[i]):
                    matrix.data[i][j] = value

    # ============================================================
    # EXECUTE
    # ============================================================

    def execute(self, env):
        if self.is_index and self.index_node:
            matrix_obj = self.index_node.matrix.evaluate(env)
            if not hasattr(matrix_obj, 'data'):
                raise TypeError("Объект не является матрицей")

            indices = []
            for idx_node in self.index_node.indices:
                idx_val = idx_node.evaluate(env)
                forbid_random(idx_val, "индекс")
                indices.append(idx_val)

            self._apply_numseq_context(matrix_obj, indices, self.value, env)

            val = self.value.evaluate(env)

            if len(indices) == 1:
                self._assign_single(matrix_obj, indices[0], val)
            elif len(indices) == 2:
                self._assign_double(matrix_obj, indices[0], indices[1], val)
            return

        # A: m = random(...)
        val = self.value.evaluate(env)

        if not self.is_index and isinstance(val, RandomSource):
            existing = None
            try:
                existing = env.get(self.var_name)
            except NameError:
                existing = None

            if existing is None:
                env.set(self.var_name, val.generate_one())
                return

            if not hasattr(existing, 'data'):
                env.set(self.var_name, val.generate_one())
                return

            if existing.rows == 0:
                kind = "вектор" if not existing.is_2d else "матрицу"
                raise ValueError(
                    f"Нельзя заполнить пустой {kind} '{self.var_name}' "
                    f"случайными числами: неизвестен размер."
                )

            if existing.is_2d:
                new_data = val.generate_2d(existing.rows, existing.cols)
            else:
                new_data = val.generate(len(existing.data))

            existing.replace_data(new_data, existing.is_2d)
            return

        # C: обычное присваивание
        if self.is_matrix:
            if isinstance(val, list):
                env.set(self.var_name, MatrExMatrix(val, False))
            elif self._is_scalar(val):
                env.set(self.var_name, MatrExMatrix([], False))
            else:
                env.set(self.var_name, MatrExMatrix([], False))
        else:
            if isinstance(val, MatrExMatrix):
                copied_data = [
                    row.copy() if isinstance(row, list) else row
                    for row in val.data
                ]
                env.set(self.var_name, MatrExMatrix(copied_data, val.is_2d))
            else:
                env.set(self.var_name, val)

    # ============================================================
    # КОНТЕКСТ ДЛЯ NumberSeqNode
    # ============================================================
    def _apply_numseq_context(self, matrix_obj, indices, value_node, env):
        from ast_nodes.functions.numseq import NumberSeqNode

        if not isinstance(value_node, NumberSeqNode):
            return

        if len(indices) == 1:
            idx = indices[0]
            if isinstance(idx, str) and idx.lower() in ('all', ':'):
                size = matrix_obj.rows
            elif isinstance(idx, str) and idx.lower() == 'end':
                size = matrix_obj.rows
            elif isinstance(idx, str) and idx.lower().startswith('last'):
                size = matrix_obj.rows
            elif self._is_range(str(idx)):
                start, end = self._parse_range(str(idx), matrix_obj.rows)
                size = end
            elif isinstance(idx, (int, float)):
                size = int(idx)
            else:
                size = matrix_obj.rows
            value_node.set_target_size(size)

        elif len(indices) == 2:
            row, col = indices[0], indices[1]

            row_processed = (self._process_special_index(row, matrix_obj.rows)
                             if isinstance(row, str) else row)
            col_processed = (self._process_special_index(col, matrix_obj.cols)
                             if isinstance(col, str) else col)

            r_start_v = self._slice_start(row_processed, matrix_obj.rows)
            r_end_v = self._slice_end(row_processed, matrix_obj.rows)
            c_start_v = self._slice_start(col_processed, matrix_obj.cols)
            c_end_v = self._slice_end(col_processed, matrix_obj.cols)

            r_size = r_end_v - r_start_v + 1
            c_size = c_end_v - c_start_v + 1

            if r_size == 1 and c_size > 1:
                size = c_end_v
            elif c_size == 1 and r_size > 1:
                size = r_end_v
            else:
                size = max(r_end_v, c_end_v)

            value_node.set_target_size(size)

    def _slice_start(self, spec, total):
        if spec == 'all':
            return 1
        if isinstance(spec, tuple) and spec[0] == 'last_range':
            return spec[1]
        if isinstance(spec, int):
            return spec
        if isinstance(spec, str) and ':' in spec:
            start, end = self._parse_range(spec, total)
            return start
        return 1

    def _slice_end(self, spec, total):
        if spec == 'all':
            return total
        if isinstance(spec, tuple) and spec[0] == 'last_range':
            start, n = spec[1], spec[2]
            end = start + n - 1
            return min(end, total)
        if isinstance(spec, int):
            return spec
        if isinstance(spec, str) and ':' in spec:
            start, end = self._parse_range(spec, total)
            return end
        return total

    # ============================================================
    # _assign_single
    # ============================================================

    def _assign_single(self, matrix_obj, idx, val):
        if isinstance(val, RandomSource):
            if idx == 'all' or (isinstance(idx, str) and idx.lower() == 'all'):
                if matrix_obj.is_2d:
                    val = val.generate_2d(matrix_obj.rows, matrix_obj.cols)
                else:
                    val = val.generate(len(matrix_obj.data))
            elif self._is_range(str(idx)):
                start, end = self._parse_range(str(idx), matrix_obj.rows)
                count = end - start + 1
                if matrix_obj.is_2d:
                    val = val.generate_2d(count, matrix_obj.cols)
                else:
                    val = val.generate(count)
            else:
                val = val.generate_one()

        if hasattr(val, 'data'):
            val_data = val.data
        else:
            val_data = val

        idx_processed = self._process_special_index(idx, matrix_obj.rows) if isinstance(idx, str) else idx

        if isinstance(idx_processed, tuple) and idx_processed[0] == 'last_range':
            start, n = idx_processed[1], idx_processed[2]
            end = start + n - 1

            if not matrix_obj.is_2d:
                while len(matrix_obj.data) < end:
                    matrix_obj.data.append(None)
                matrix_obj.rows = len(matrix_obj.data)

                if isinstance(val_data, list) and not (val_data and isinstance(val_data[0], list)):
                    for i in range(start - 1, end):
                        idx_in_val = i - (start - 1)
                        if idx_in_val < len(val_data):
                            matrix_obj.data[i] = val_data[idx_in_val]
                        else:
                            matrix_obj.data[i] = None
                else:
                    for i in range(start - 1, end):
                        matrix_obj.data[i] = val
                return

            if end > matrix_obj.rows:
                self._ensure_rows(matrix_obj, end)
            self._assign_range(matrix_obj, start, end, 1, matrix_obj.cols, val)
            return

        if idx == 'all' or idx_processed == 'all':
            if not matrix_obj.is_2d:
                if self._is_scalar(val):
                    for i in range(len(matrix_obj.data)):
                        matrix_obj.data[i] = val
                elif isinstance(val_data, list):
                    if len(val_data) > len(matrix_obj.data):
                        while len(matrix_obj.data) < len(val_data):
                            matrix_obj.data.append(None)
                        matrix_obj.rows = len(matrix_obj.data)

                    for i in range(len(val_data)):
                        if i < len(matrix_obj.data):
                            matrix_obj.data[i] = val_data[i]
                else:
                    for i in range(len(matrix_obj.data)):
                        matrix_obj.data[i] = val
                return

            if self._is_scalar(val):
                self._expand_and_fill(matrix_obj, val)
            elif isinstance(val_data, list) and val_data and isinstance(val_data[0], list):
                rows_needed = len(val_data)
                cols_needed = max(len(row) for row in val_data) if val_data else 0

                if rows_needed > matrix_obj.rows:
                    self._ensure_rows(matrix_obj, rows_needed)
                if cols_needed > matrix_obj.cols:
                    self._ensure_cols(matrix_obj, cols_needed)

                for i in range(rows_needed):
                    for j in range(cols_needed):
                        if i < len(val_data) and j < len(val_data[i]):
                            if i < len(matrix_obj.data) and j < len(matrix_obj.data[i]):
                                matrix_obj.data[i][j] = val_data[i][j]
                        else:
                            if i < len(matrix_obj.data) and j < len(matrix_obj.data[i]):
                                matrix_obj.data[i][j] = None
            elif isinstance(val_data, list):
                if len(val_data) > matrix_obj.rows:
                    self._ensure_rows(matrix_obj, len(val_data))
                for i in range(len(val_data)):
                    if i < len(matrix_obj.data) and 0 < len(matrix_obj.data[i]):
                        matrix_obj.data[i][0] = val_data[i]
            else:
                self._expand_and_fill(matrix_obj, val)
            return

        if self._is_range(str(idx)):
            start, end = self._parse_range(str(idx), matrix_obj.rows)
            if start < 1 or end < 1:
                raise IndexError(f"Индексы должны быть >= 1")

            if not matrix_obj.is_2d:
                while len(matrix_obj.data) < end:
                    matrix_obj.data.append(None)
                matrix_obj.rows = len(matrix_obj.data)

                if isinstance(val_data, list) and not (val_data and isinstance(val_data[0], list)):
                    for i in range(start - 1, end):
                        idx_in_val = i - (start - 1)
                        if idx_in_val < len(val_data):
                            matrix_obj.data[i] = val_data[idx_in_val]
                        else:
                            matrix_obj.data[i] = None
                else:
                    for i in range(start - 1, end):
                        matrix_obj.data[i] = val
                return

            if end > matrix_obj.rows:
                self._ensure_rows(matrix_obj, end)
            self._assign_range(matrix_obj, start, end, 1, matrix_obj.cols, val,
                               fill_rest_none=True)
            return

        if isinstance(idx_processed, int):
            if idx_processed < 1:
                raise IndexError(f"Индекс должен быть >= 1, получен {idx_processed}")

            if not matrix_obj.is_2d:
                while len(matrix_obj.data) < idx_processed:
                    matrix_obj.data.append(None)
                matrix_obj.rows = len(matrix_obj.data)

                row_idx = idx_processed - 1

                if isinstance(val_data, list) and not (val_data and isinstance(val_data[0], list)):
                    matrix_obj.data[row_idx] = val_data[0] if val_data else None
                else:
                    matrix_obj.data[row_idx] = val
                return

            if idx_processed > matrix_obj.rows:
                self._ensure_rows(matrix_obj, idx_processed)

            row_idx = idx_processed - 1

            if isinstance(val_data, list) and not (val_data and isinstance(val_data[0], list)):
                if len(val_data) > matrix_obj.cols:
                    self._ensure_cols(matrix_obj, len(val_data))
                for j in range(len(val_data)):
                    if row_idx < len(matrix_obj.data) and j < len(matrix_obj.data[row_idx]):
                        matrix_obj.data[row_idx][j] = val_data[j]
                for j in range(len(val_data), matrix_obj.cols):
                    if row_idx < len(matrix_obj.data) and j < len(matrix_obj.data[row_idx]):
                        matrix_obj.data[row_idx][j] = None
            else:
                for j in range(matrix_obj.cols):
                    if row_idx < len(matrix_obj.data) and j < len(matrix_obj.data[row_idx]):
                        matrix_obj.data[row_idx][j] = val
            return

        raise TypeError(f"Неверный индекс: {idx}")

    # ============================================================
    # _assign_double
    # ============================================================

    def _assign_double(self, matrix_obj, row, col, val):
        if hasattr(row, 'evaluate'):
            try:
                row = row.evaluate(None)
            except:
                pass
        if hasattr(col, 'evaluate'):
            try:
                col = col.evaluate(None)
            except:
                pass

        row_processed = self._process_special_index(row, matrix_obj.rows) if isinstance(row, str) else row
        col_processed = self._process_special_index(col, matrix_obj.cols) if isinstance(col, str) else col

        is_new_row_name = False
        new_row_name = None

        if row_processed == 'all' or row == 'all':
            r_kind = 'all'
            r_start = 1
            r_end = matrix_obj.rows
        elif isinstance(row_processed, tuple) and row_processed[0] == 'last_range':
            r_kind = 'range'
            r_start = row_processed[1]
            r_end = row_processed[1] + row_processed[2] - 1
        elif isinstance(row_processed, int):
            r_kind = 'single'
            r_start = row_processed
            r_end = row_processed
        elif isinstance(row_processed, str) and ':' in row_processed:
            r_kind = 'range'
            r_start, r_end = self._parse_range(row_processed, matrix_obj.rows)
        elif isinstance(row_processed, str):
            # ============================================================
            # ИМЯ СТРОКИ (не число, не диапазон, не спец-слово)
            # ============================================================
            # Ищем значение в первом столбце (строки данных, начиная с 1).
            # Если нашли — берём его позицию (1-based).
            # Если не нашли — добавляем в КОНЕЦ таблицы.
            # ============================================================
            found_row = None
            name_lower = row_processed.strip().lower()
            for i in range(1, len(matrix_obj.data)):
                if i < len(matrix_obj.data[i]) and len(matrix_obj.data[i]) > 0:
                    cell = matrix_obj.data[i][0]
                    if cell is not None and str(cell).strip().lower() == name_lower:
                        found_row = i + 1     # 1-based
                        break

            if found_row is not None:
                r_kind = 'single'
                r_start = found_row
                r_end = found_row
            else:
                # Новая строка → в КОНЕЦ таблицы
                r_kind = 'single'
                r_start = matrix_obj.rows + 1
                r_end = r_start
                is_new_row_name = True
                new_row_name = row_processed
                self._ensure_rows(matrix_obj, r_start)
        else:
            r_kind = 'single'
            r_start = 1
            r_end = 1

        if col_processed == 'all' or col == 'all':
            c_kind = 'all'
            c_start = 1
            c_end = matrix_obj.cols
        elif isinstance(col_processed, tuple) and col_processed[0] == 'last_range':
            c_kind = 'range'
            c_start = col_processed[1]
            c_end = col_processed[1] + col_processed[2] - 1
        elif isinstance(col_processed, int):
            c_kind = 'single'
            c_start = col_processed
            c_end = col_processed
        elif isinstance(col_processed, str) and ':' in col_processed:
            c_kind = 'range'
            c_start, c_end = self._parse_range(col_processed, matrix_obj.cols)
        elif isinstance(col_processed, str):
            headers = matrix_obj.data[0] if matrix_obj.rows > 0 else []
            headers_lower = [str(h).lower() if h is not None else None for h in headers]
            if col_processed.lower() in headers_lower:
                c_kind = 'single'
                c_start = headers_lower.index(col_processed.lower()) + 1
                c_end = c_start
                if r_kind == 'all':
                    r_start = max(r_start, 2)
            else:
                c_kind = 'single'
                c_start = matrix_obj.cols + 1
                c_end = c_start
        else:
            c_kind = 'single'
            c_start = 1
            c_end = 1

        # ============================================================
        # НОВЫЙ СТОЛБЕЦ
        # ============================================================
        is_new_column = (c_kind == 'single' and c_start == matrix_obj.cols + 1)

        if is_new_column:
            # 1. Расширяем матрицу
            if c_end > matrix_obj.cols:
                self._ensure_cols(matrix_obj, c_end)

            # 2. Устанавливаем заголовок
            header_name = None
            if isinstance(col_processed, str):
                s = col_processed.strip().lower()
                if (s not in ('all', ':', 'end')
                        and not s.startswith('end+')
                        and not s.startswith('end-')
                        and not s.startswith('last')):
                    header_name = col_processed

            if matrix_obj.rows > 0 and len(matrix_obj.data[0]) > c_start - 1:
                matrix_obj.data[0][c_start - 1] = header_name

            # 3. Заполняем данными
            if self._is_scalar(val):
                for i in range(1, matrix_obj.rows):
                    while len(matrix_obj.data[i]) <= c_start - 1:
                        matrix_obj.data[i].append(None)
                    matrix_obj.data[i][c_start - 1] = val
                return

            # Вектор (1D)
            is_vector = False
            vector_data = None
            if hasattr(val, 'data') and not val.is_2d:
                is_vector = True
                vector_data = val.data
            elif isinstance(val, list) and not (val and isinstance(val[0], list)):
                is_vector = True
                vector_data = val

            if is_vector:
                for i in range(1, matrix_obj.rows):
                    idx_in_val = i - 1
                    if i < len(matrix_obj.data):
                        while len(matrix_obj.data[i]) <= c_start - 1:
                            matrix_obj.data[i].append(None)
                        if idx_in_val < len(vector_data):
                            matrix_obj.data[i][c_start - 1] = vector_data[idx_in_val]
                        else:
                            matrix_obj.data[i][c_start - 1] = None
                return

            # 2D-матрица — заполняем как обычно, но заголовок уже стоит

        # ============================================================
        # СТАРАЯ ЛОГИКА
        # ============================================================

        if isinstance(val, RandomSource):
            rows_count = r_end - r_start + 1
            cols_count = c_end - c_start + 1

            if rows_count == 1 and cols_count == 1:
                val = val.generate_one()
            elif rows_count == 1:
                val = val.generate(cols_count)
            elif cols_count == 1:
                val = val.generate(rows_count)
            else:
                val = val.generate_2d(rows_count, cols_count)

        if hasattr(val, 'data'):
            val_data = val.data
        else:
            val_data = val

        if r_end > matrix_obj.rows:
            self._ensure_rows(matrix_obj, r_end)
        if c_end > matrix_obj.cols:
            self._ensure_cols(matrix_obj, c_end)

        if r_kind == 'single' and c_kind == 'single':
            if self._is_scalar(val):
                if r_start - 1 < len(matrix_obj.data) and c_start - 1 < len(matrix_obj.data[r_start - 1]):
                    matrix_obj.data[r_start - 1][c_start - 1] = val
            elif isinstance(val_data, list) and val_data:
                if r_start - 1 < len(matrix_obj.data) and c_start - 1 < len(matrix_obj.data[r_start - 1]):
                    matrix_obj.data[r_start - 1][c_start - 1] = val_data[0] if not isinstance(val_data[0], list) else val_data[0][0]

            # Восстанавливаем имя новой строки
            if is_new_row_name and new_row_name is not None:
                if r_start - 1 < len(matrix_obj.data):
                    while len(matrix_obj.data[r_start - 1]) < 1:
                        matrix_obj.data[r_start - 1].append(None)
                    matrix_obj.data[r_start - 1][0] = new_row_name
            return

        # Для строк: если r — single и c — all → затирать остаток None
        fill_rest = (r_kind == 'single' and c_kind == 'all')

        self._assign_range(matrix_obj, r_start, r_end, c_start, c_end, val,
                           fill_rest_none=fill_rest)

        # ============================================================
        # ВОССТАНОВИТЬ ИМЯ НОВОЙ СТРОКИ
        # ============================================================
        # _assign_range могла затереть первый столбец значением.
        # Восстанавливаем имя новой строки.
        # ============================================================
        if is_new_row_name and new_row_name is not None:
            row_idx = r_start - 1
            if row_idx < len(matrix_obj.data):
                while len(matrix_obj.data[row_idx]) < 1:
                    matrix_obj.data[row_idx].append(None)
                matrix_obj.data[row_idx][0] = new_row_name

    def __repr__(self):
        if self.is_index:
            return f"Assign({self.index_node} = {self.value})"
        if self.is_matrix:
            return f"Assign({self.var_name} = [], {self.value})"
        return f"Assign({self.var_name} = {self.value})"


# ============================================================
# PARSE_ASSIGN
# ============================================================

def _check_reserved_name(parser, var_name):
    if var_name.lower() == 'error':
        raise ArrayVatorError(
            code="RESERVED_WORD",
            context=parser._get_context(),
            message=(
                "Имя 'error' зарезервировано.\n"
                "  Используется для обработки ошибок."
            ),
            suggestion=(
                "Используйте другое имя:\n"
                "     err  = ...\n"
                "     err1 = ...\n"
                "\n"
                "Переменная 'error' доступна ТОЛЬКО ДЛЯ ЧТЕНИЯ:\n"
                "     if error then { print(error) }"
            ),
        )


def parse_assign(parser):
    save_pos = parser.pos
    token = parser.peek()
    if not token or token[0] != 'IDENTIFIER':
        return None

    var_name = parser.expect('IDENTIFIER')[1]

    if parser.check('LBRACKET'):
        bracket_pos = parser.pos

        try:
            parser.expect('LBRACKET')
            indices = []

            idx1 = parser._parse_index_expression()
            indices.append(idx1)

            if parser.check('COMMA'):
                parser.expect('COMMA')
                idx2 = parser._parse_index_expression()
                indices.append(idx2)

            parser.expect('RBRACKET')

            if parser.check('ASSIGN'):
                _check_reserved_name(parser, var_name)

                parser.expect('ASSIGN')
                value = parser.parse_expression()
                index_node = IndexNode(VariableNode(var_name), indices)
                return AssignNode(var_name, value, False, True, index_node)
            else:
                parser.pos = save_pos
                return None

        except SyntaxError:
            parser.pos = save_pos
            if parser.check('LBRACKET'):
                parser.expect('LBRACKET')

    if parser.check('LBRACKET'):
        parser.pos = save_pos
        var_name = parser.expect('IDENTIFIER')[1]
        parser.expect('LBRACKET')
        if parser.check('RBRACKET'):
            parser.expect('RBRACKET')
            if parser.check('ASSIGN'):
                _check_reserved_name(parser, var_name)

                parser.expect('ASSIGN')
                value = parser.parse_expression()
                return AssignNode(var_name, value, True, False)
        else:
            parser.pos = save_pos
            var_name = parser.expect('IDENTIFIER')[1]

    if parser.check('ASSIGN'):
        parser.pos = save_pos
        var_name = parser.expect('IDENTIFIER')[1]

        _check_reserved_name(parser, var_name)

        parser.expect('ASSIGN')
        value = parser.parse_expression()
        return AssignNode(var_name, value, False, False)

    parser.pos = save_pos
    return None