# ast_nodes/functions/abc.py
"""
Функция ABC — ABC-анализ (Парето 80/20).

СИНТАКСИС:
    abc(срез)
    abc(срез, %)
    abc(срез, coef)
    abc(срез, %, m[:, 3])
    abc(срез, coef, m[:, end+1])
    abc(срез, 70, 90)
    abc(срез, 70, 90, %)
    abc(срез, 70, 90, %, m[:, 3])

ПРАВИЛА:
    - Пороги по умолчанию: 80 / 95 (классика 80/15/5).
    - Пороги автосортируются: 90, 70 → 70, 90.
    - `%`   — проценты (0–100), округление 2 знака.
    - `coef` — коэффициент (0.0–1.0), округление 4 знака.
    - Целевой столбец — срез m[:, N] или m[:, "Имя"] или m[:, end+1].
    - `__abc` вставляется СПРАВА от исходного среза.
    - `__share` / `__coef` — справа от `__abc` (если целевой не указан)
      или в указанный целевой столбец.
    - Порядок аргументов — ЛЮБОЙ.
    - ПОРЯДОК СТРОК СОХРАНЯЕТСЯ (на DuckDB — через ROW_NUMBER).

DUCKDB:
    - Транслируется в SQL OVER (SUM, ROWS BETWEEN UNBOUNDED PRECEDING).
    - Исходный порядок строк сохраняется через __orig_row.
    - `__abc` вставляется в SELECT явным перечислением столбцов.
"""

from ..base import Node
from errors import ArrayVatorError


def _is_duckdb(val):
    try:
        from duckdb_engine import DuckDBTable
        return isinstance(val, DuckDBTable)
    except ImportError:
        return False


def _resolve_column_index(matrix_obj, col_spec, env):
    from ..utils.index_utils import resolve_column_index
    idx, _ = resolve_column_index(matrix_obj, col_spec, env)
    return idx


def _eval_col_spec(col_node, env):
    """Вычисляет значение из узла-спецификации столбца."""
    if hasattr(col_node, 'evaluate'):
        return col_node.evaluate(env)
    return col_node


def _resolve_duckdb_column(columns, col_spec, env):
    """
    Возвращает 0-based индекс столбца для DuckDB.
    col_spec может быть узлом или готовым значением.
    """
    from .filterif import _resolve_column_for_duckdb

    col_val = col_spec
    if hasattr(col_spec, 'evaluate'):
        col_val = col_spec.evaluate(env)

    return _resolve_column_for_duckdb(columns, col_val)


class AbcNode(Node):
    def __init__(self, data, thresholds=None, option=None, target=None):
        self.data = data            # IndexNode — срез
        self.thresholds = thresholds or []  # список из 0, 1 или 2 Node
        self.option = option        # None | 'percent' | 'coef'
        self.target = target        # IndexNode | None

    def evaluate(self, env):
        from ast_nodes.index import IndexNode

        if not isinstance(self.data, IndexNode):
            raise ArrayVatorError(
                code="ABC_NEED_SLICE",
                context=None,
            )

        matrix_obj = self.data.matrix.evaluate(env)

        # Разрешаем пороги
        th = []
        for t in self.thresholds:
            val = t.evaluate(env) if hasattr(t, 'evaluate') else t
            if not isinstance(val, (int, float)):
                raise ArrayVatorError(
                    code="ABC_BAD_SYNTAX",
                    context=None,
                    message=(
                        f"abc: порог должен быть числом, "
                        f"получен {type(val).__name__}"
                    ),
                )
            th.append(float(val))

        if len(th) == 1:
            th = [th[0], 95.0]
        if len(th) == 0:
            th = [80.0, 95.0]
        # АВТОСОРТИРОВКА порогов (без ошибки)
        if len(th) == 2 and th[0] >= th[1]:
            th[0], th[1] = th[1], th[0]
        if not (0 < th[0] < th[1] < 100):
            raise ArrayVatorError(
                code="ABC_BAD_SYNTAX",
                context=None,
                message=(
                    f"abc: пороги должны быть 0 < A < AB < 100, "
                    f"получено {th}"
                ),
            )

        # DUCKDB
        if _is_duckdb(matrix_obj):
            return self._evaluate_duckdb(matrix_obj, env, th)

        # MATRIX
        if hasattr(matrix_obj, 'data') and matrix_obj.is_2d:
            return self._evaluate_matrix(matrix_obj, env, th)

        raise ArrayVatorError(
            code="ABC_BAD_SYNTAX",
            context=None,
            message=(
                "abc: ожидается матрица или DuckDB.\n"
                "  Пример: abc(m[:, \"Продажи\"])"
            ),
        )

    # ============================================================
    # MATRIX
    # ============================================================
    def _evaluate_matrix(self, matrix_obj, env, thresholds):
        col_spec = _eval_col_spec(self.data.indices[1], env)
        col_idx = _resolve_column_index(matrix_obj, col_spec, env)
        rows = matrix_obj.rows

        header = list(matrix_obj.data[0]) if rows > 0 else []

        values = []
        for i in range(1, rows):
            row = matrix_obj.data[i]
            v = row[col_idx] if col_idx < len(row) else None
            values.append(v)

        # Проверка: есть ли ХОТЬ ОДНО число в столбце
        has_number = False
        for v in values:
            if isinstance(v, (int, float)) and not isinstance(v, bool):
                has_number = True
                break
        if not has_number:
            raise ArrayVatorError(
                code="ABC_NOT_NUMERIC",
                context=None,
            )

        total = 0.0
        for v in values:
            if isinstance(v, (int, float)) and not isinstance(v, bool):
                total += v
        if total == 0:
            raise ArrayVatorError(
                code="ABC_ZERO_SUM",
                context=None,
            )

        indexed = list(enumerate(values))
        indexed.sort(
            key=lambda p: (
                -(p[1] if isinstance(p[1], (int, float)) and not isinstance(p[1], bool) else 0)
            )
        )

        running = 0.0
        abc_by_row = {}
        share_by_row = {}

        for orig_idx, val in indexed:
            if isinstance(val, (int, float)) and not isinstance(val, bool):
                running += val
            cum_pct = running / total * 100.0

            if cum_pct <= thresholds[0]:
                cat = "A"
            elif cum_pct <= thresholds[1]:
                cat = "B"
            else:
                cat = "C"

            abc_by_row[orig_idx] = cat
            if isinstance(val, (int, float)) and not isinstance(val, bool):
                share_by_row[orig_idx] = val / total * 100.0
            else:
                share_by_row[orig_idx] = None

        target_idx = None
        is_new_target = False
        if self.option and self.target is not None:
            target_idx, is_new_target = self._resolve_target_col(
                matrix_obj, env, col_idx
            )

        result_header = list(header)
        abc_pos = col_idx + 1

        result_header.insert(abc_pos, "__abc")

        share_pos = None
        share_header_name = None
        if self.option and target_idx is None:
            share_pos = abc_pos + 1
            share_header_name = "__share" if self.option == 'percent' else "__coef"
            result_header.insert(share_pos, share_header_name)

        if self.option and target_idx is not None:
            if is_new_target:
                pass
            elif target_idx > col_idx:
                target_idx += 1

        if self.option and target_idx is not None and not is_new_target:
            cur_name = result_header[target_idx] if target_idx < len(result_header) else None
            if cur_name is None or (isinstance(cur_name, str) and cur_name.strip() == ""):
                result_header[target_idx] = (
                    "__share" if self.option == 'percent' else "__coef"
                )

        if is_new_target:
            new_name = "__share" if self.option == 'percent' else "__coef"
            result_header.append(new_name)
            target_idx = len(result_header) - 1

        result_data = [result_header]

        for i in range(1, rows):
            row = list(matrix_obj.data[i])
            while len(row) < len(header):
                row.append(None)

            abc_val = abc_by_row.get(i - 1)
            row.insert(abc_pos, abc_val)

            if share_pos is not None:
                sh = share_by_row.get(i - 1)
                if sh is not None:
                    if self.option == 'percent':
                        sh = round(sh, 2)
                    else:
                        sh = round(sh / 100.0, 4)
                row.insert(share_pos, sh)

            if self.option and target_idx is not None and not is_new_target:
                sh = share_by_row.get(i - 1)
                if sh is not None:
                    if self.option == 'percent':
                        sh = round(sh, 2)
                    else:
                        sh = round(sh / 100.0, 4)
                while len(row) <= target_idx:
                    row.append(None)
                row[target_idx] = sh

            if is_new_target:
                sh = share_by_row.get(i - 1)
                if sh is not None:
                    if self.option == 'percent':
                        sh = round(sh, 2)
                    else:
                        sh = round(sh / 100.0, 4)
                while len(row) <= target_idx:
                    row.append(None)
                row[target_idx] = sh

            result_data.append(row)

        if result_data:
            max_cols = max(len(r) for r in result_data)
            for r in result_data:
                while len(r) < max_cols:
                    r.append(None)

        from runtime.matrix import MatrExMatrix
        return MatrExMatrix(result_data, True)

    # ============================================================
    # DUCKDB
    # ============================================================
    def _evaluate_duckdb(self, duck_table, env, thresholds):
        from duckdb_engine import DuckDBTable
        import uuid

        columns = duck_table.get_columns()
        col_spec = _eval_col_spec(self.data.indices[1], env)
        col_idx = _resolve_duckdb_column(columns, col_spec, env)
        if col_idx is None or col_idx < 0 or col_idx >= len(columns):
            raise ArrayVatorError(
                code="ABC_BAD_SYNTAX",
                context=None,
                message="abc: столбец не найден в DuckDB.",
            )

        col_name = columns[col_idx]
        safe_col = '"' + str(col_name).replace('"', '""') + '"'

        t_a = float(thresholds[0])
        t_ab = float(thresholds[1])

        target_name = None
        target_is_new = False
        if self.option and self.target is not None:
            target_name, target_is_new = self._resolve_target_duckdb(
                duck_table, columns, env, col_idx
            )

        # ============================================================
        # ВНУТРЕННИЙ ЗАПРОС: ROW_NUMBER для сохранения порядка
        # ============================================================
        base_sql = (
            f"SELECT *, ROW_NUMBER() OVER () AS __orig_row "
            f"FROM {duck_table.table_name}"
        )

        computed_parts = ["t.*"]
        abc_expr = self._abc_sql(safe_col, t_a, t_ab)
        computed_parts.append(abc_expr)

        if self.option and target_name is None:
            share_expr = self._share_sql(safe_col, self.option)
            share_name = "__share" if self.option == 'percent' else "__coef"
            computed_parts.append(f'{share_expr} AS "{share_name}"')

        computed_sql = (
            f"SELECT {', '.join(computed_parts)} "
            f"FROM ({base_sql}) AS t"
        )

        select_parts = []
        for i, c in enumerate(columns):
            esc = '"' + str(c).replace('"', '""') + '"'
            select_parts.append(esc)
            if i == col_idx:
                select_parts.append('"__abc"')

        if self.option and target_name is None:
            share_name = "__share" if self.option == 'percent' else "__coef"
            select_parts.append(f'"{share_name}"')

        if self.option and target_name is not None and not target_is_new:
            share_expr = self._share_sql(safe_col, self.option)
            safe_target = '"' + str(target_name).replace('"', '""') + '"'
            select_parts.append(f'{share_expr} AS {safe_target}')

        if self.option and target_name is not None and target_is_new:
            share_expr = self._share_sql(safe_col, self.option)
            share_name = "__share" if self.option == 'percent' else "__coef"
            select_parts.append(f'{share_expr} AS "{share_name}"')

        final_sql = (
            f"SELECT {', '.join(select_parts)} "
            f"FROM ({computed_sql}) AS t "
            f"ORDER BY __orig_row"
        )

        new_name = f"abc_{uuid.uuid4().hex[:8]}"
        try:
            duck_table.con.execute(
                f'CREATE OR REPLACE VIEW {new_name} AS {final_sql}'
            )
        except Exception as e:
            raise RuntimeError(f"abc: ошибка DuckDB: {e}\nSQL: {final_sql}")

        return self._make_new_table(duck_table, new_name)

    def _abc_sql(self, safe_col, t_a, t_ab):
        return f"""
            CASE
                WHEN SUM(CAST({safe_col} AS DOUBLE)) OVER (
                    ORDER BY CAST({safe_col} AS DOUBLE) DESC
                    ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
                ) / NULLIF(SUM(CAST({safe_col} AS DOUBLE)) OVER (), 0) * 100 <= {t_a}
                THEN 'A'
                WHEN SUM(CAST({safe_col} AS DOUBLE)) OVER (
                    ORDER BY CAST({safe_col} AS DOUBLE) DESC
                    ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
                ) / NULLIF(SUM(CAST({safe_col} AS DOUBLE)) OVER (), 0) * 100 <= {t_ab}
                THEN 'B'
                ELSE 'C'
            END AS "__abc"
        """

    def _share_sql(self, safe_col, option):
        base = (
            f"CAST({safe_col} AS DOUBLE) "
            f"/ NULLIF(SUM(CAST({safe_col} AS DOUBLE)) OVER (), 0)"
        )
        if option == 'percent':
            return f"ROUND({base} * 100, 2)"
        return f"ROUND({base}, 4)"

    # ============================================================
    # ХЕЛПЕРЫ
    # ============================================================
    def _resolve_target_col(self, matrix_obj, env, src_col_idx):
        from ..utils.index_utils import resolve_column_index

        col_spec_node = self.target.indices[1]
        col_spec = (col_spec_node.evaluate(env)
                    if hasattr(col_spec_node, 'evaluate')
                    else col_spec_node)

        if isinstance(col_spec, str):
            s = col_spec.strip().lower()
            if s.startswith('end+'):
                return (matrix_obj.cols, True)

        try:
            idx, _ = resolve_column_index(matrix_obj, col_spec, env)
            return (idx, False)
        except Exception:
            return (matrix_obj.cols, True)

    def _resolve_target_duckdb(self, duck_table, columns, env, src_col_idx):
        from .filterif import _resolve_column_for_duckdb

        col_spec_node = self.target.indices[1]
        col_spec = (col_spec_node.evaluate(env)
                    if hasattr(col_spec_node, 'evaluate')
                    else col_spec_node)

        if isinstance(col_spec, str):
            s = col_spec.strip().lower()
            if s.startswith('end+'):
                return ("__share", True)

        try:
            idx = _resolve_column_for_duckdb(columns, col_spec)
            if 0 <= idx < len(columns):
                return (columns[idx], False)
        except Exception:
            pass

        return ("__share", True)

    def _make_new_table(self, duck_table, new_name):
        from duckdb_engine import DuckDBTable
        new_table = DuckDBTable.__new__(DuckDBTable)
        new_table.path = duck_table.path
        new_table.table_name = new_name
        new_table.con = duck_table.con
        new_table.utf8_path = duck_table.utf8_path
        new_table.is_temp = False
        new_table._tmp_path = None
        return new_table

    def __repr__(self):
        return f"abc({self.data}, thresholds={self.thresholds}, option={self.option})"