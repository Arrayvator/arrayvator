# ast_nodes/functions/find.py
"""
Функция FIND - поиск значений в матрице/векторе.

ВАЖНО: find() НЕ мутирует исходную матрицу.

РЕЖИМЫ:
    find(условие)               → матрица координат [[строка, столбец], ...]
    find(условие, rows)         → вектор номеров строк (уникальные)
    find(условие, cols)         → вектор номеров столбцов (уникальные)

МОДИФИКАТОРЫ (для строк):
    inside  — поиск подстроки
    ignore  — без учёта регистра

СОСТАВНЫЕ УСЛОВИЯ:
    find(m[:, "X"] == "Y" and m[:, "Z"] > 10)
    find(m[:, "X"] == "Y" or  m[:, "Z"] == "W")
    find(not (m[:, "X"] == "Y"))

DUCKDB:
    - Если данные в DuckDBTable → SQL-запрос
    - Номера строк считаются С УЧЁТОМ заголовка (как в Matrix)
"""

from ..base import Node
from runtime.matrix import MatrExMatrix


# ============================================================
# ХЕЛПЕР: определение DuckDBTable
# ============================================================
def _is_duckdb(val):
    try:
        from duckdb_engine import DuckDBTable
        return isinstance(val, DuckDBTable)
    except ImportError:
        return False


# ============================================================
# ХЕЛПЕРЫ: получение маски через filterif-логику
# ============================================================
def _matrix_mask(condition, env, matrix_obj, row_start, row_end,
                  inside=False, ignore=False):
    """Булева маска для 2D-матрицы (список True/False на строку данных)."""
    from .filterif import _evaluate_condition_matrix

    result = _evaluate_condition_matrix(
        condition, env, matrix_obj, row_start, row_end,
        inside=inside, ignore=ignore,
    )

    if not isinstance(result, list):
        n = row_end - row_start + 1
        result = [bool(result)] * n

    return result


def _vector_mask(condition, env, vector_obj, start, end,
                  inside=False, ignore=False):
    """Булева маска для вектора (список True/False на элемент)."""
    from .filterif import _evaluate_condition_vector

    result = _evaluate_condition_vector(
        condition, env, vector_obj, start, end,
        inside=inside, ignore=ignore,
    )

    if not isinstance(result, list):
        n = end - start + 1
        result = [bool(result)] * n

    return result


# ============================================================
# АНАЛИЗ: срез матрицы / вектора
# ============================================================
def _analyze_matrix_slice(index_node, env):
    """
    Разбирает IndexNode m[:, "X"] для MATRIX.

    Возвращает:
        (matrix_obj, row_start, row_end, col_idx)
    или None.
    """
    from ..utils.index_utils import (
        parse_range_spec,
        resolve_column_index,
    )

    if not hasattr(index_node, 'indices'):
        return None
    if len(index_node.indices) != 2:
        return None

    matrix_obj = index_node.matrix.evaluate(env)
    if _is_duckdb(matrix_obj):
        return None
    if not hasattr(matrix_obj, 'data') or not matrix_obj.is_2d:
        return None

    row_spec_node = index_node.indices[0]
    row_spec = (row_spec_node.evaluate(env)
                if hasattr(row_spec_node, 'evaluate')
                else row_spec_node)

    row_start, row_end = parse_range_spec(
        row_spec, matrix_obj.rows, is_column=False
    )

    is_explicit = False
    if isinstance(row_spec, str):
        if row_spec.strip().lower() not in (':', 'all'):
            is_explicit = True
    elif isinstance(row_spec, (int, float)):
        is_explicit = True

    col_spec_node = index_node.indices[1]
    col_spec = (col_spec_node.evaluate(env)
                if hasattr(col_spec_node, 'evaluate')
                else col_spec_node)

    col_idx, skip_header = resolve_column_index(matrix_obj, col_spec, env)

    if not is_explicit and skip_header:
        row_start = max(row_start, 2)

    return (matrix_obj, row_start, row_end, col_idx)


def _analyze_vector_slice(index_node, env):
    """Разбирает IndexNode v[...] для VECTOR. Возвращает (vec, start, end)."""
    from ..utils.index_utils import parse_range_spec

    if not hasattr(index_node, 'indices'):
        return None
    if len(index_node.indices) != 1:
        return None

    vector_obj = index_node.matrix.evaluate(env)
    if not hasattr(vector_obj, 'data') or vector_obj.is_2d:
        return None

    idx_node = index_node.indices[0]
    idx_spec = (idx_node.evaluate(env)
                if hasattr(idx_node, 'evaluate')
                else idx_node)

    start, end = parse_range_spec(
        idx_spec, len(vector_obj.data), is_column=False
    )
    return (vector_obj, start, end)


# ============================================================
# DUCKDB: ПОИСК
# ============================================================
def _find_duckdb(condition, env, duck_table, inside=False, ignore=False,
                 return_rows=False, return_cols=False):
    """
    Поиск в DuckDBTable через SQL.
    """
    import uuid
    from .filterif import _translate_to_sql

    where_sql = _translate_to_sql(
        condition, env, duck_table,
        inside=inside, ignore=ignore,
    )

    columns = duck_table.get_columns()

    # ============================================================
    # COLS — какие столбцы содержат совпадения
    # ============================================================
    if return_cols:
        # Ищем совпадение в ЛЮБОМ столбце
        cols_result = []
        for i, col in enumerate(columns, 1):
            safe_col = '"' + str(col).replace('"', '""') + '"'

            # Подменяем col-условие на конкретный столбец
            single_where = _translate_to_sql_for_column(
                condition, env, duck_table, col,
                inside=inside, ignore=ignore,
            )

            check_sql = (
                f"SELECT COUNT(*) FROM {duck_table.table_name} "
                f"WHERE {single_where}"
            )
            try:
                cnt = duck_table.con.execute(check_sql).fetchone()[0]
            except Exception:
                cnt = 0
            if cnt > 0:
                cols_result.append(i)

        return MatrExMatrix(cols_result, False)

    # ============================================================
    # ROWS — номера строк (1-based, с учётом заголовка)
    # ============================================================
    if return_rows:
        sql = f"""
            SELECT rn FROM (
                SELECT ROW_NUMBER() OVER () + 1 AS rn
                FROM {duck_table.table_name}
            ) AS t
            WHERE rn IN (
                SELECT ROW_NUMBER() OVER () + 1
                FROM {duck_table.table_name}
                WHERE {where_sql}
            )
            ORDER BY rn
        """
        # Проще: сначала индексы совпавших строк
        sql = f"""
            SELECT rn FROM (
                SELECT ROW_NUMBER() OVER () AS rn,
                       *
                FROM {duck_table.table_name}
            )
            WHERE {where_sql}
            ORDER BY rn
        """
        try:
            rows = duck_table.con.execute(sql).fetchall()
        except Exception as e:
            raise RuntimeError(f"Ошибка find (rows): {e}\nSQL: {sql}")

        # rn 1-based по данным, +1 → с учётом заголовка
        unique = []
        seen = set()
        for r in rows:
            rn = r[0] + 1
            if rn not in seen:
                seen.add(rn)
                unique.append(rn)
        return MatrExMatrix(unique, False)

    # ============================================================
    # ОБЫЧНЫЙ РЕЖИМ — координаты [[строка, столбец], ...]
    # ============================================================
    select_parts = []
    for i, col in enumerate(columns, 1):
        safe_col = '"' + str(col).replace('"', '""') + '"'
        select_parts.append(f"""
            SELECT rn + 1 AS "Строка", {i} AS "Столбец"
            FROM (
                SELECT ROW_NUMBER() OVER () AS rn, {safe_col}
                FROM {duck_table.table_name}
            )
            WHERE {_translate_to_sql_for_column(condition, env, duck_table, col, inside=inside, ignore=ignore)}
        """)

    union_sql = " UNION ALL ".join(select_parts) + ' ORDER BY "Строка", "Столбец"'

    try:
        rows = duck_table.con.execute(union_sql).fetchall()
    except Exception as e:
        raise RuntimeError(f"Ошибка find: {e}\nSQL: {union_sql}")

    if not rows:
        return MatrExMatrix([], True)

    data = [[r[0], r[1]] for r in rows]
    return MatrExMatrix(data, True)


def _translate_to_sql_for_column(condition, env, duck_table, col_name,
                                  inside=False, ignore=False):
    """
    Оборачивает условие так, чтобы оно проверялось только для одного столбца.
    Для 2D-условия это не всегда осмысленно, поэтому в find(cols) мы
    просто проверяем КАЖДЫЙ столбец независимо.
    """
    from .filterif import _translate_to_sql

    # Простейший случай: IndexNode == скаляр → сравнение одного столбца
    # Для составного условия — просто применяем как есть, но заменяем
    # имя столбца на текущий.
    # Мы делаем это через хак: заворачиваем условие в подзапрос с
    # алиасом текущего столбца.

    # Практический приём: сгенерировать условие с текущим столбцом,
    # если левый IndexNode указывает на другой столбец — всё равно
    # проверим текущий (для find(cols) это именно то, что нужно).
    from ast_nodes.index import IndexNode

    # Если условие — простое (IndexNode OP scalar) — сравним col
    from ast_nodes.operations import BinaryOp

    def _replace_col(node):
        if isinstance(node, IndexNode):
            return col_name
        if isinstance(node, BinaryOp):
            return BinaryOp(node.op, _replace_col(node.left), _replace_col(node.right))
        return node

    new_cond = _replace_col(condition)

    # Создаём "фейковый" DuckDBTable, у которого условие всегда
    # ссылается на col_name
    return _translate_to_sql(new_cond, env, duck_table,
                              inside=inside, ignore=ignore)


# ============================================================
# FIND NODE
# ============================================================
class FindNode(Node):
    def __init__(self, data, condition=None, arg1=None, arg2=None, arg3=None,
                 return_rows=False, return_cols=False):
        self.data = data
        self.condition = condition
        self.arg1 = arg1
        self.arg2 = arg2
        self.arg3 = arg3
        self.return_rows = return_rows
        self.return_cols = return_cols

    # ------------------------------------------------------------
    # Модификаторы
    # ------------------------------------------------------------
    def _get_modifiers(self, env):
        ignore = False
        inside = False
        for arg in (self.arg1, self.arg2, self.arg3):
            if arg is None:
                continue
            val = arg.evaluate(env) if hasattr(arg, 'evaluate') else arg
            if isinstance(val, str):
                v = val.lower()
                if v == 'ignore':
                    ignore = True
                elif v == 'inside':
                    inside = True
        return ignore, inside

    # ------------------------------------------------------------
    # Evaluate
    # ------------------------------------------------------------
    def evaluate(self, env):
        from ast_nodes.index import IndexNode
        from ast_nodes.operations import BinaryOp
        from ast_nodes.variables import VariableNode

        ignore, inside = self._get_modifiers(env)

        cond = self.condition if self.condition is not None else self.data

        # ============================================================
        # DUCKDB — если условие ссылается на DuckDBTable
        # ============================================================
        duck_ref = self._find_duckdb_ref(cond, env)
        if duck_ref is not None:
            return _find_duckdb(
                cond, env, duck_ref,
                inside=inside, ignore=ignore,
                return_rows=self.return_rows,
                return_cols=self.return_cols,
            )

        # ============================================================
        # MATRIX / VECTOR — ищем target
        # ============================================================
        target = self._find_target(cond, env)
        if target is None:
            return MatrExMatrix([], self.return_rows or self.return_cols or False)

        target_obj, row_start, row_end, col_idx, is_2d = target

        # ============================================================
        # 2D: строим маску и собираем результат
        # ============================================================
        if is_2d:
            mask = _matrix_mask(
                cond, env, target_obj, row_start, row_end,
                inside=inside, ignore=ignore,
            )
            return self._build_result_2d(
                target_obj, row_start, row_end, col_idx, mask
            )

        # ============================================================
        # 1D: вектор
        # ============================================================
        mask = _vector_mask(
            cond, env, target_obj, row_start, row_end,
            inside=inside, ignore=ignore,
        )
        return self._build_result_1d(target_obj, row_start, row_end, mask)

    # ------------------------------------------------------------
    # Поиск DuckDBTable в условии
    # ------------------------------------------------------------
    def _find_duckdb_ref(self, node, env):
        from ast_nodes.index import IndexNode
        from ast_nodes.operations import BinaryOp, UnaryOp
        from ast_nodes.variables import VariableNode

        if isinstance(node, IndexNode):
            try:
                obj = node.matrix.evaluate(env)
            except Exception:
                return None
            return obj if _is_duckdb(obj) else None

        if isinstance(node, BinaryOp):
            left = self._find_duckdb_ref(node.left, env)
            if left is not None:
                return left
            return self._find_duckdb_ref(node.right, env)

        if isinstance(node, UnaryOp):
            return self._find_duckdb_ref(node.right, env)

        if isinstance(node, VariableNode):
            try:
                obj = env.get(node.name)
            except NameError:
                return None
            return obj if _is_duckdb(obj) else None

        return None

    # ------------------------------------------------------------
    # Поиск Matrix / Vector в условии
    # ------------------------------------------------------------
    def _find_target(self, node, env):
        """
        Возвращает (matrix_or_vector, row_start, row_end, col_idx, is_2d)
        для первого IndexNode в условии.
        """
        from ast_nodes.index import IndexNode
        from ast_nodes.operations import BinaryOp, UnaryOp
        from ast_nodes.variables import VariableNode

        if isinstance(node, IndexNode):
            if len(node.indices) == 2:
                info = _analyze_matrix_slice(node, env)
                if info is None:
                    return None
                m, r_start, r_end, col_idx = info
                return (m, r_start, r_end, col_idx, True)

            if len(node.indices) == 1:
                info = _analyze_vector_slice(node, env)
                if info is None:
                    return None
                v, v_start, v_end = info
                return (v, v_start, v_end, None, False)

        if isinstance(node, BinaryOp):
            if node.op in ('AND', 'OR'):
                left = self._find_target(node.left, env)
                if left is not None:
                    return left
                return self._find_target(node.right, env)

            left = self._find_target(node.left, env)
            if left is not None:
                return left
            return self._find_target(node.right, env)

        if isinstance(node, UnaryOp):
            return self._find_target(node.right, env)

        if isinstance(node, VariableNode):
            try:
                obj = env.get(node.name)
            except NameError:
                return None
            if obj is None:
                return None
            if hasattr(obj, 'data') and not obj.is_2d:
                return (obj, 1, len(obj.data), None, False)

        return None

    # ------------------------------------------------------------
    # Сборка результата: 2D
    # ------------------------------------------------------------
    def _build_result_2d(self, matrix_obj, row_start, row_end, col_idx, mask):
        coords = []
        row_set = set()
        col_set = set()

        for i, flag in enumerate(mask):
            if not flag:
                continue
            row_num = row_start + i           # 1-based, с заголовком
            col_num = col_idx + 1             # 1-based

            coords.append([row_num, col_num])
            row_set.add(row_num)
            col_set.add(col_num)

        if self.return_rows:
            return MatrExMatrix(sorted(row_set), False)

        if self.return_cols:
            return MatrExMatrix(sorted(col_set), False)

        return MatrExMatrix(coords, True)

    # ------------------------------------------------------------
    # Сборка результата: 1D
    # ------------------------------------------------------------
    def _build_result_1d(self, vector_obj, start, end, mask):
        rows = []
        for i, flag in enumerate(mask):
            if flag:
                rows.append(start + i)        # 1-based

        if self.return_cols:
            return MatrExMatrix([1] if rows else [], False)

        return MatrExMatrix(rows, False)

    def __repr__(self):
        if self.return_rows:
            mode = ", rows"
        elif self.return_cols:
            mode = ", cols"
        else:
            mode = ""
        return f"find({self.data}, {self.condition}{mode})"


class FindIfNode(Node):
    """Заглушка (старый алиас)."""
    def __init__(self, matrix, condition):
        self.matrix = matrix
        self.condition = condition

    def evaluate(self, env):
        return MatrExMatrix([], False)

    def __repr__(self):
        return f"findif({self.matrix}, {self.condition})"