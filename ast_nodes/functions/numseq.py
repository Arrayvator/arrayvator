# ast_nodes/functions/numseq.py
"""
Функция range / Number — числовая последовательность.

СИНТАКСИС:
    range(N)                     # [1, 2, 3, ..., N]
    range(end)                   # [1, 2, ..., длина_среза]
    range(2:end)                 # [2, 3, ..., длина_среза]
    range(a:b)                   # от a до b с шагом 1
    range(a:b, step S)           # от a до b с шагом S
    range(10:1, step -1)         # обратный порядок

    Number(...)                  # то же самое

ПРАВИЛА:
    - Оба конца включительно.
    - step опционален (по умолчанию 1).
    - step передаётся как `step N` через запятую.
    - step 0 → ошибка.
    - Знак step должен соответствовать направлению:
        a <= b → step > 0
        a >  b → step < 0
    - 'end' — только в контексте присваивания.
      _target_size хранит АБСОЛЮТНЫЙ номер последней строки/столбца
      целевого среза.
    - Возвращает ВЕКТОР (MatrExMatrix с is_2d=False).
    - Обрезка/дополнение None делается в AssignNode, а не здесь.
"""

from ..base import Node


class NumberSeqNode(Node):
    """
    Возвращает вектор чисел.

    Атрибуты:
        mode        — 'simple' (range(N)) | 'range' (a:b) | 'end' (2:end)
        n_node      — N для mode='simple'
        start_node  — a для mode='range'
        end_node    — b для mode='range'; StringNode('end') для mode='end'
        step_node   — S (опц.)
    """

    def __init__(self, mode, n_node=None, start_node=None,
                 end_node=None, step_node=None):
        self.mode = mode  # 'simple' | 'range' | 'end'
        self.n_node = n_node
        self.start_node = start_node
        self.end_node = end_node
        self.step_node = step_node

        # АБСОЛЮТНЫЙ номер последней строки/столбца целевого среза
        self._target_size = None

    def set_target_size(self, size):
        """Вызывается AssignNode перед evaluate."""
        self._target_size = size

    def evaluate(self, env):
        from runtime.matrix import MatrExMatrix

        step = self._eval(self.step_node, env) if self.step_node is not None else 1

        if not isinstance(step, (int, float)) or isinstance(step, bool):
            raise TypeError(
                f"range: step должен быть числом, получено {type(step).__name__}"
            )

        if step == 0:
            raise ValueError("range: step не может быть 0")

        # ============================================================
        # РЕЖИМ 1: range(N) → [1, 2, ..., N]
        # ============================================================
        if self.mode == 'simple':
            n = self._eval(self.n_node, env)
            if not isinstance(n, (int, float)) or isinstance(n, bool):
                raise TypeError(
                    f"range: N должно быть числом, получено {type(n).__name__}"
                )
            n = int(n)
            if n <= 0:
                raise ValueError(f"range: N должно быть > 0, получено {n}")

            if self.step_node is not None:
                raise ValueError(
                    "range(N, step S) — неверно.\n"
                    "  Укажите диапазон: range(1:N, step S)\n"
                    "  Или просто:       range(N)"
                )

            values = list(range(1, n + 1))

        # ============================================================
        # РЕЖИМ 2: range(a:b), range(2:end), range(end)
        # ============================================================
        elif self.mode in ('range', 'end'):
            start = self._eval(self.start_node, env) if self.start_node is not None else 1
            end = self._eval_end(self.end_node, env)

            if not isinstance(start, (int, float)) or isinstance(start, bool):
                raise TypeError(
                    f"range: начало должно быть числом, получено {type(start).__name__}"
                )
            if not isinstance(end, (int, float)) or isinstance(end, bool):
                raise TypeError(
                    f"range: конец должен быть числом, получено {type(end).__name__}"
                )

            values = self._generate(start, end, step)

        else:
            raise ValueError(f"range: неизвестный режим '{self.mode}'")

        # Обрезка/дополнение — в AssignNode, здесь просто возвращаем вектор
        return MatrExMatrix(values, False)

    # ============================================================
    # ГЕНЕРАЦИЯ
    # ============================================================
    def _generate(self, start, end, step):
        is_float = (
            isinstance(start, float)
            or isinstance(end, float)
            or isinstance(step, float)
        )

        if start <= end:
            if step < 0:
                raise ValueError(
                    f"range: при a <= b шаг должен быть > 0, получен {step}"
                )
        else:
            if step > 0:
                raise ValueError(
                    f"range: при a > b шаг должен быть < 0, получен {step}"
                )

        values = []
        current = start
        EPS = 1e-9

        if step > 0:
            while current <= end + EPS:
                values.append(self._round(current) if is_float else int(round(current)))
                current += step
        else:
            while current >= end - EPS:
                values.append(self._round(current) if is_float else int(round(current)))
                current += step

        return values

    # ============================================================
    # ХЕЛПЕРЫ
    # ============================================================
    def _eval(self, node, env):
        if node is None:
            return None
        if hasattr(node, 'evaluate'):
            return node.evaluate(env)
        return node

    def _eval_end(self, node, env):
        """
        Вычисляет конец диапазона.

        Если это 'end', 'end-N', 'end+N' — берём АБСОЛЮТНЫЙ номер
        последней строки/столбца целевого среза (self._target_size)
        и применяем смещение:

            end     → target
            end-N   → target - N
            end+N   → target + N
        """
        val = self._eval(node, env)

        if not isinstance(val, str):
            return val

        s = val.strip().lower()

        if not s.startswith('end'):
            return val

        if self._target_size is None:
            raise ValueError(
                "range: 'end' можно использовать только в присваивании,\n"
                "  например: m[:, 1] = range(2:end)"
            )

        base = self._target_size

        if s == 'end':
            return base
        if s.startswith('end-'):
            try:
                return base - int(s[4:].strip())
            except ValueError:
                return base
        if s.startswith('end+'):
            try:
                return base + int(s[4:].strip())
            except ValueError:
                return base

        return val

    def _round(self, val, digits=10):
        return round(val, digits)

    def __repr__(self):
        if self.mode == 'simple':
            return f"NumberSeq({self.n_node})"
        if self.mode == 'end':
            return f"NumberSeq({self.start_node}:end)"
        if self.step_node is not None:
            return f"NumberSeq({self.start_node}:{self.end_node}, step {self.step_node})"
        return f"NumberSeq({self.start_node}:{self.end_node})"