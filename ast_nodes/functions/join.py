# ast_nodes/functions/join.py
"""
Функция JOIN — соединение двух таблиц по ключу.

СИНТАКСИС:
    join(m1, m2, on "ID")
    join(m1, m2, on "ID", how "left")
    join(m1, m2, on ["ID", "Дата"])
    join(m1, m2, on "ID" == "Код")
    join(m1, m2, on "ID", suffixes ["_1", "_2"])

РЕЖИМЫ HOW:
    "left"  (по умолчанию) — все строки левой + совпадения
    "inner" — только совпадения
    "right" — все строки правой
    "outer" — все строки обеих

ПРАВИЛА:
    - Всегда возвращает НОВУЮ таблицу.
    - on обязателен.
    - how: left (по умолчанию) / inner / right / outer.
    - suffixes: "_1", "_2" по умолчанию.
    - Работает на Matrix и DuckDB.
"""

from ..base import Node
from runtime.matrix import MatrExMatrix


# ============================================================
# ДОПУСТИМЫЕ РЕЖИМЫ HOW
# ============================================================
ALLOWED_HOW = {"left", "inner", "right", "outer"}


# ============================================================
# ХЕЛПЕР: определение DuckDBTable
# ============================================================
def _is_duckdb(val):
    try:
        from duckdb_engine import DuckDBTable
        return isinstance(val, DuckDBTable)
    except ImportError:
        return False


class JoinNode(Node):
    def __init__(self, left, right, on_keys, how="left", suffixes=None):
        self.left = left
        self.right = right
        self.on_keys = on_keys
        self.how = how
        self.suffixes = suffixes or ("_1", "_2")

    def evaluate(self, env):
        # ============================================================
        # ВАЛИДАЦИЯ HOW
        # ============================================================
        how_str = str(self.how).strip().lower()
        if how_str not in ALLOWED_HOW:
            from errors import ArrayVatorError
            raise ArrayVatorError(
                code="JOIN_BAD_HOW",
                context=None,
            )
        # Нормализуем обратно в self.how, чтобы дальше не думать
        self.how = how_str

        # ============================================================
        # 1. Вычисляем таблицы
        # ============================================================
        left_obj = (
            self.left.evaluate(env)
            if hasattr(self.left, 'evaluate')
            else self.left
        )
        right_obj = (
            self.right.evaluate(env)
            if hasattr(self.right, 'evaluate')
            else self.right
        )

        # ============================================================
        # 2. DuckDB
        # ============================================================
        if _is_duckdb(left_obj) or _is_duckdb(right_obj):
            return self._join_duckdb(left_obj, right_obj, env)

        # ============================================================
        # 3. Matrix (RAM)
        # ============================================================
        if hasattr(left_obj, 'data') and hasattr(right_obj, 'data'):
            return self._join_matrix(left_obj, right_obj, env)

        # ============================================================
        # 4. Ошибка типа
        # ============================================================
        raise TypeError(
            "join: оба аргумента должны быть матрицами или DuckDB.\n"
            "  Пример: r = join(m1, m2, on \"ID\")"
        )

    # ============================================================
    # MATRIX
    # ============================================================
    def _join_matrix(self, left_obj, right_obj, env):
        left_header = left_obj.data[0] if left_obj.rows > 0 else []
        right_header = right_obj.data[0] if right_obj.rows > 0 else []

        left_data = left_obj.data[1:]
        right_data = right_obj.data[1:]

        # Индексы ключевых столбцов
        left_key_indices = []
        right_key_indices = []
        for lc, rc in self.on_keys:
            li = self._find_col_index(left_header, lc)
            ri = self._find_col_index(right_header, rc)
            left_key_indices.append(li)
            right_key_indices.append(ri)

        # Правые НЕключевые столбцы
        right_nonkey = [
            i for i in range(len(right_header))
            if i not in right_key_indices
        ]

        # ============================================================
        # КОНФЛИКТЫ ИМЁН
        # ============================================================
        left_cols_set = set(str(c) for c in left_header)
        conflicts = set()
        for i in right_nonkey:
            rname = str(right_header[i])
            if rname in left_cols_set:
                conflicts.add(rname)

        # Левые столбцы (с суффиксом, если конфликт)
        result_header = []
        for c in left_header:
            c_str = str(c)
            if c_str in conflicts:
                result_header.append(c_str + self.suffixes[0])
            else:
                result_header.append(c)

        # Правые НЕключевые (с суффиксом, если конфликт)
        for i in right_nonkey:
            rname = str(right_header[i])
            if rname in conflicts:
                result_header.append(rname + self.suffixes[1])
            else:
                result_header.append(rname)

        # ============================================================
        # ИНДЕКС ПРАВОЙ ТАБЛИЦЫ ПО КЛЮЧУ
        # ============================================================
        right_index = {}
        for ri, row in enumerate(right_data):
            key = tuple(
                row[i] if i < len(row) else None
                for i in right_key_indices
            )
            right_index[key] = row

        result = [result_header]

        # ============================================================
        # LEFT / OUTER
        # ============================================================
        if self.how in ("left", "outer"):
            for row in left_data:
                key = tuple(
                    row[i] if i < len(row) else None
                    for i in left_key_indices
                )
                right_row = right_index.get(key)

                if right_row is not None:
                    new_row = list(row) + [
                        right_row[i] if i < len(right_row) else None
                        for i in right_nonkey
                    ]
                else:
                    new_row = list(row) + [None] * len(right_nonkey)

                result.append(new_row)

        # ============================================================
        # INNER
        # ============================================================
        if self.how == "inner":
            for row in left_data:
                key = tuple(
                    row[i] if i < len(row) else None
                    for i in left_key_indices
                )
                right_row = right_index.get(key)

                if right_row is not None:
                    new_row = list(row) + [
                        right_row[i] if i < len(right_row) else None
                        for i in right_nonkey
                    ]
                    result.append(new_row)

        # ============================================================
        # RIGHT
        # ============================================================
        if self.how == "right":
            for row in right_data:
                key = tuple(
                    row[i] if i < len(row) else None
                    for i in right_key_indices
                )
                match = None
                for lrow in left_data:
                    lkey = tuple(
                        lrow[i] if i < len(lrow) else None
                        for i in left_key_indices
                    )
                    if lkey == key:
                        match = lrow
                        break

                if match is not None:
                    new_row = list(match) + [
                        row[i] if i < len(row) else None
                        for i in right_nonkey
                    ]
                else:
                    new_row = [None] * len(left_header) + [
                        row[i] if i < len(row) else None
                        for i in right_nonkey
                    ]

                result.append(new_row)

        # ============================================================
        # OUTER — добить правые, которые не нашли пары слева
        # ============================================================
        if self.how == "outer":
            left_keys_set = set()
            for row in left_data:
                key = tuple(
                    row[i] if i < len(row) else None
                    for i in left_key_indices
                )
                left_keys_set.add(key)

            for row in right_data:
                key = tuple(
                    row[i] if i < len(row) else None
                    for i in right_key_indices
                )
                if key not in left_keys_set:
                    new_row = [None] * len(left_header) + [
                        row[i] if i < len(row) else None
                        for i in right_nonkey
                    ]
                    result.append(new_row)

        return MatrExMatrix(result, True)

    def _find_col_index(self, header, name):
        name_lower = str(name).strip().lower()
        for i, h in enumerate(header):
            if str(h).strip().lower() == name_lower:
                return i
        raise ValueError(f"join: столбец '{name}' не найден")

    # ============================================================
    # DUCKDB
    # ============================================================
    def _join_duckdb(self, left_obj, right_obj, env):
        from duckdb_engine import DuckDBTable
        import uuid

        if not _is_duckdb(left_obj) or not _is_duckdb(right_obj):
            raise TypeError(
                "join: если один аргумент — DuckDB, оба должны быть DuckDB.\n"
                "  Используйте ToMatrix или ToBigData для конвертации."
            )

        def _esc(name):
            return '"' + str(name).replace('"', '""') + '"'

        # ============================================================
        # Столбцы
        # ============================================================
        left_cols = left_obj.get_columns()
        right_cols = right_obj.get_columns()

        left_key_names = []
        right_key_names = []
        for lc, rc in self.on_keys:
            l_match = self._find_col_by_name(left_cols, lc)
            r_match = self._find_col_by_name(right_cols, rc)
            left_key_names.append(l_match)
            right_key_names.append(r_match)

        right_nonkey_names = [
            c for c in right_cols
            if c not in right_key_names
        ]

        # ============================================================
        # Конфликты имён
        # ============================================================
        left_cols_lower = {c.lower() for c in left_cols}
        conflicts = set()
        for rname in right_nonkey_names:
            if rname.lower() in left_cols_lower:
                conflicts.add(rname.lower())

        # ============================================================
        # SELECT
        # ============================================================
        select_parts = []

        # Левые столбцы
        for c in left_cols:
            esc_c = _esc(c)
            if c.lower() in conflicts:
                alias = _esc(c + self.suffixes[0])
                select_parts.append(f'L.{esc_c} AS {alias}')
            else:
                select_parts.append(f'L.{esc_c}')

        # Правые НЕключевые
        for c in right_nonkey_names:
            esc_c = _esc(c)
            if c.lower() in conflicts:
                alias = _esc(c + self.suffixes[1])
                select_parts.append(f'R.{esc_c} AS {alias}')
            else:
                select_parts.append(f'R.{esc_c}')

        select_sql = ",\n                   ".join(select_parts)

        # ============================================================
        # ON
        # ============================================================
        on_parts = []
        for lname, rname in zip(left_key_names, right_key_names):
            on_parts.append(f'L.{_esc(lname)} = R.{_esc(rname)}')
        on_sql = " AND ".join(on_parts)

        how_map = {
            "left": "LEFT JOIN",
            "inner": "INNER JOIN",
            "right": "RIGHT JOIN",
            "outer": "FULL OUTER JOIN",
        }
        how_sql = how_map.get(self.how, "LEFT JOIN")

        # ============================================================
        # Финальный SQL
        # ============================================================
        new_name = f"joined_{uuid.uuid4().hex[:8]}"
        sql = f"""
            CREATE OR REPLACE VIEW {new_name} AS
            SELECT {select_sql}
            FROM {left_obj.table_name} AS L
            {how_sql} {right_obj.table_name} AS R
            ON {on_sql}
        """

        try:
            left_obj.con.execute(sql)
        except Exception as e:
            raise RuntimeError(f"Ошибка join: {e}\nSQL: {sql}")

        new_table = DuckDBTable.__new__(DuckDBTable)
        new_table.path = left_obj.path
        new_table.table_name = new_name
        new_table.con = left_obj.con
        new_table.utf8_path = left_obj.utf8_path
        new_table.is_temp = False
        new_table._tmp_path = None

        return new_table

    def _find_col_by_name(self, columns, name):
        """Находит реальное имя столбца (с учётом регистра)."""
        name_lower = str(name).strip().lower()
        for c in columns:
            if str(c).strip().lower() == name_lower:
                return c
        raise ValueError(f"join: столбец '{name}' не найден")

    def __repr__(self):
        return f"join({self.left}, {self.right}, on={self.on_keys}, how={self.how})"