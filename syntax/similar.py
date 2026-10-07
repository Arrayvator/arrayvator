# syntax/similar.py
"""
Поиск похожих имён функций и ключевых слов.

Используется, когда пользователь опечатался в имени функции.
Возвращает список наиболее вероятных вариантов.

Алгоритм:
    1. Точное совпадение (регистронезависимо) — сразу возвращаем.
    2. Совпадение префикса (первые N символов) — высокий приоритет.
    3. Расстояние Левенштейна — базовая метрика.

Оценка = 0.5 * prefix_score + 0.5 * (1 - lev / max_len)

Порог: возвращаем только те, у кого score >= 0.5.
"""


# ============================================================
# РАССТОЯНИЕ ЛЕВЕНШТЕЙНА
# ============================================================
def _levenshtein(a, b):
    """Классическое расстояние Левенштейна между двумя строками."""
    if a == b:
        return 0
    if not a:
        return len(b)
    if not b:
        return len(a)

    prev = list(range(len(b) + 1))
    for i, ca in enumerate(a, 1):
        curr = [i]
        for j, cb in enumerate(b, 1):
            cost = 0 if ca == cb else 1
            curr.append(min(
                curr[j - 1] + 1,        # вставка
                prev[j] + 1,            # удаление
                prev[j - 1] + cost,     # замена
            ))
        prev = curr
    return prev[-1]


# ============================================================
# ОЦЕНКА СХОДСТВА
# ============================================================
def _prefix_score(a, b, min_prefix=2):
    """
    Оценка совпадения префикса.
    Возвращает 0.0 .. 1.0 — доля общего префикса от минимума длины.
    """
    if not a or not b:
        return 0.0

    n = 0
    for ca, cb in zip(a, b):
        if ca != cb:
            break
        n += 1

    if n < min_prefix:
        return 0.0

    return n / max(1, min(len(a), len(b)))


def _score(query, candidate):
    """
    Итоговая оценка похожести query и candidate.
    0.0 .. 1.0
    """
    q = query.lower()
    c = candidate.lower()

    if q == c:
        return 1.0

    max_len = max(len(q), len(c))
    if max_len == 0:
        return 0.0

    lev = _levenshtein(q, c)
    lev_score = 1.0 - (lev / max_len)

    pref_score = _prefix_score(q, c, min_prefix=2)

    # Итоговая оценка
    score = 0.5 * pref_score + 0.5 * lev_score

    # Бонус за совпадение первого символа
    if q and c and q[0] == c[0]:
        score += 0.05

    return min(1.0, score)


# ============================================================
# ИСТОЧНИК ИМЁН
# ============================================================
def _collect_names():
    """Собирает все известные имена: функции + спецслова + ключевые слова."""
    names = set()

    # 1. Функции из signatures
    try:
        from syntax.signatures import FUNCTION_SIGNATURES
        names.update(FUNCTION_SIGNATURES.keys())
    except Exception:
        pass

    # 2. Функции из autocomplete
    try:
        from syntax.autocomplete_data import AUTOCOMPLETE_ITEMS
        names.update(AUTOCOMPLETE_ITEMS.keys())
    except Exception:
        pass

    # 3. Спец-слова
    try:
        from syntax.autocomplete_data import SPECIAL_WORDS
        names.update(SPECIAL_WORDS.keys())
    except Exception:
        pass

    # 4. Ключевые слова
    try:
        from syntax.autocomplete_data import KEYWORDS
        names.update(KEYWORDS)
    except Exception:
        pass

    # Отсеиваем пустые и односимвольные
    names = {n for n in names if n and len(n) >= 2}

    return sorted(names)


_NAMES_CACHE = None


def _get_names():
    global _NAMES_CACHE
    if _NAMES_CACHE is None:
        _NAMES_CACHE = _collect_names()
    return _NAMES_CACHE


# ============================================================
# ПУБЛИЧНЫЙ API
# ============================================================
def find_similar(query, limit=3, threshold=0.5):
    """
    Ищет похожие имена на query.

    Возвращает список строк длиной до `limit`,
    отсортированный по убыванию оценки.

    Примеры:
        find_similar("filterig")  → ["filterif", "filldown", ...]
        find_similar("sumifff")   → ["sumif"]
        find_similar("xyz123")    → []
    """
    if not query or len(query) < 2:
        return []

    q = query.lower()
    names = _get_names()

    # 1. Точное совпадение (регистронезависимо)
    for n in names:
        if n.lower() == q:
            return [n]

    # 2. Считаем оценки
    scored = []
    for n in names:
        s = _score(q, n)
        if s >= threshold:
            scored.append((s, n))

    # 3. Сортируем: сначала по оценке, потом по алфавиту
    scored.sort(key=lambda x: (-x[0], x[1].lower()))

    return [n for _, n in scored[:limit]]