# check_consistency.py
"""
Проверка согласованности баз ArrayVator.

Проверяет:
    1. Все функции из signatures.py есть в AUTOCOMPLETE_ITEMS + SPECIAL_WORDS.
    2. Ключи db_ru.py и db_en.py совпадают.
    3. Токены из lexer.py есть в KEYWORDS (или служебные).
    4. Все функции из AUTOCOMPLETE_ITEMS имеют signature/description/example.
    5. Все функции из signatures.py имеют category.
    6. Help-файлы есть (в help/ или в корне).

Запуск:
    python check_consistency.py
"""

import re
import sys
from pathlib import Path


PROJECT_DIR = Path(__file__).parent.resolve()


# ============================================================
# ЦВЕТА
# ============================================================
class C:
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    CYAN = '\033[96m'
    BOLD = '\033[1m'
    DIM = '\033[2m'
    END = '\033[0m'


def _section(title):
    print()
    print(f"{C.CYAN}{C.BOLD}{'=' * 60}{C.END}")
    print(f"{C.CYAN}{C.BOLD}  {title}{C.END}")
    print(f"{C.CYAN}{C.BOLD}{'=' * 60}{C.END}")


def _ok(msg):
    print(f"  {C.GREEN}✅{C.END} {msg}")


def _fail(msg):
    print(f"  {C.RED}❌{C.END} {msg}")


def _warn(msg):
    print(f"  {C.YELLOW}⚠️ {C.END} {msg}")


# ============================================================
# ЗАГРУЗКА МОДУЛЕЙ
# ============================================================
def load_modules():
    """Загружает все необходимые модули."""
    sys.path.insert(0, str(PROJECT_DIR))

    result = {}

    try:
        from syntax.signatures import FUNCTION_SIGNATURES
        result['signatures'] = FUNCTION_SIGNATURES
    except ImportError as e:
        print(f"❌ Не удалось загрузить syntax.signatures: {e}")
        result['signatures'] = {}

    try:
        from syntax.autocomplete_data import (
            AUTOCOMPLETE_ITEMS,
            SPECIAL_WORDS,
            KEYWORDS,
        )
        result['autocomplete'] = AUTOCOMPLETE_ITEMS
        result['special'] = SPECIAL_WORDS
        result['keywords'] = KEYWORDS
    except ImportError as e:
        print(f"❌ Не удалось загрузить syntax.autocomplete_data: {e}")
        result['autocomplete'] = {}
        result['special'] = {}
        result['keywords'] = []

    try:
        from errors.db_ru import MESSAGES_RU
        result['db_ru'] = MESSAGES_RU
    except ImportError as e:
        print(f"❌ Не удалось загрузить errors.db_ru: {e}")
        result['db_ru'] = {}

    try:
        from errors.db_en import MESSAGES_EN
        result['db_en'] = MESSAGES_EN
    except ImportError as e:
        print(f"❌ Не удалось загрузить errors.db_en: {e}")
        result['db_en'] = {}

    return result


def extract_lexer_tokens():
    """Извлекает все типы токенов из lexer.py."""
    lexer_path = PROJECT_DIR / "lexer.py"
    if not lexer_path.exists():
        return set()

    src = lexer_path.read_text(encoding="utf-8")

    tokens = set()

    # Ищем паттерны: (r'...', 'TOKEN_TYPE')
    for match in re.finditer(r"\(\s*r?'[^']*'\s*,\s*'([A-Z_][A-Z0-9_]*)'\s*\)", src):
        tokens.add(match.group(1))

    # Ищем также строковые литералы в списках
    # Например: ['ALL', 'END_KEYWORD', ...]
    for match in re.finditer(r"'([A-Z_][A-Z0-9_]*)'", src):
        token = match.group(1)
        if len(token) >= 2 and token.isupper():
            tokens.add(token)

    return tokens


# ============================================================
# ПРОВЕРКИ
# ============================================================
def check_signatures_vs_autocomplete(sig, auto):
    """Все функции из signatures.py должны быть в AUTOCOMPLETE_ITEMS + SPECIAL_WORDS."""
    _section("1. signatures.py vs AUTOCOMPLETE_ITEMS + SPECIAL_WORDS")

    # Объединяем AUTOCOMPLETE и SPECIAL_WORDS
    all_auto = dict(auto)
    try:
        from syntax.autocomplete_data import SPECIAL_WORDS
        all_auto.update(SPECIAL_WORDS)
    except ImportError:
        pass

    sig_names = set(k.lower() for k in sig.keys())
    auto_names = set(k.lower() for k in all_auto.keys())

    missing = sig_names - auto_names
    extra = auto_names - sig_names

    # Игнорируем в extra контрольные конструкции и модификаторы,
    # которые живут в SPECIAL_WORDS / KEYWORDS, но не в signatures.
    IGNORE_EXTRA = {
        # Управляющие
        'if', 'while', 'for', 'break', 'then', 'else',
        # Обработка ошибок
        'try', 'catch', 'error',
        # Логика
        'when', 'true', 'false', 'null', 'none',
        # Индексация
        'end', 'last', 'all', 'begin',
        # Модификаторы
        'az', 'za', 'before', 'after', 'inside', 'ignore',
        'approx', 'skip', 'vertical', 'horizontal',
        # Groupby
        'by', 'agg', 'having', 'order',
        # Аналитика — опции
        'coef', 'iqr', 'zscore', 'percentile', 'only',
        '%',
        # Режимы
        'bigdata', 'table',
        # Графики — типы
        'bar', 'line', 'pie', 'hist', 'scatter', 'box', 'heatmap', 'pair',
        # Графики — опции
        'title', 'save', 'bins', 'color', 'xlabel', 'ylabel',
        'plotly', 'static',
    }
    extra = extra - IGNORE_EXTRA

    if missing:
        _fail(f"В signatures.py есть, но НЕ в AUTOCOMPLETE/SPECIAL: {len(missing)}")
        for name in sorted(missing):
            print(f"      • {name}")
    else:
        _ok("Все функции из signatures.py есть в AUTOCOMPLETE + SPECIAL_WORDS")

    if extra:
        _warn(f"В AUTOCOMPLETE есть, но НЕТ в signatures.py: {len(extra)}")
        for name in sorted(extra):
            print(f"      • {name}")
    else:
        _ok("Все функции из AUTOCOMPLETE есть в signatures.py")

    return len(missing) == 0


def check_db_keys(db_ru, db_en):
    """Ключи db_ru.py и db_en.py должны совпадать."""
    _section("2. db_ru.py vs db_en.py")

    ru_keys = set(db_ru.keys())
    en_keys = set(db_en.keys())

    only_ru = ru_keys - en_keys
    only_en = en_keys - ru_keys

    if only_ru:
        _fail(f"Только в db_ru (нет в db_en): {len(only_ru)}")
        for k in sorted(only_ru):
            print(f"      • {k}")
    else:
        _ok("Все ключи db_ru есть в db_en")

    if only_en:
        _fail(f"Только в db_en (нет в db_ru): {len(only_en)}")
        for k in sorted(only_en):
            print(f"      • {k}")
    else:
        _ok("Все ключи db_en есть в db_ru")

    return not only_ru and not only_en


def check_lexer_vs_keywords(lexer_tokens, keywords):
    """Ключевые слова из lexer.py должны быть в KEYWORDS (или быть служебными)."""
    _section("3. lexer.py vs KEYWORDS")

    # Служебные токены (операторы, литералы, разделители) — не в KEYWORDS
    SERVICE_TOKENS = {
        'PLUS', 'MINUS', 'STAR', 'SLASH', 'MOD', 'POW', 'FLOORDIV',
        'EQUALS', 'NOTEQUAL', 'LESS', 'GREATER', 'LESSEQUAL', 'GREATEREQUAL',
        'ASSIGN', 'COLON', 'COMMA', 'SEMICOLON',
        'LPAREN', 'RPAREN', 'LBRACKET', 'RBRACKET', 'LBRACE', 'RBRACE',
        'AND', 'OR', 'NOT',
        'NUMBER', 'STRING', 'IDENTIFIER',
        'TRUE', 'FALSE', 'NULL', 'NONE',
        'END_PLUS', 'END_MINUS',
        'ERROR',
    }

    # Токены функций — в KEYWORDS их нет (KEYWORDS — это слова языка)
    FUNCTION_TOKENS = {
        # Статистика
        'SUM', 'MIN', 'MAX', 'AVG', 'LEN', 'LENROW', 'LENCOL',
        # Математика
        'ROUND', 'INT', 'FRAC', 'FRAC_DIGITS',
        # Строки
        'SPLIT', 'JOINVECTOR', 'REPLACETEXT', 'CLEAN',
        'DELETETEXTLEFT', 'DELETETEXTRIGHT',
        'TRIM', 'TRIMLEFT', 'TRIMRIGHT',
        # Сортировка / поиск
        'SORT', 'FIND', 'FINDIF', 'VLOOKUP',
        # Фильтрация / удаление
        'FILTERIF', 'DELETEIF', 'DELETE',
        # Модификация
        'INSERT', 'INSERTIF', 'COPY', 'MOVE', 'MATRIXMOD',
        'JOIN', 'JOINARRAY', 'UNPIVOT', 'PIVOT',
        'GROUPBY', 'GROUPAGG', 'FILLDOWN', 'EXACT',
        'ADDCOLUMN', 'ADDROWS', 'TRANSPOSE',
        # Дубликаты
        'UNIQUE', 'COUNT_DISTINCT', 'VALUE_COUNTS', 'DELETE_DUPLICATE',
        # Условные агрегаты
        'SUMIF', 'COUNTIF', 'AVGIF', 'MINIF', 'MAXIF',
        'MEDIANIF', 'COUNTUNIQUEIF', 'SUMPRODUCT',
        # Условия
        'CASE', 'APPLYIF', 'SAMPLE',
        # Создание
        'MATRIX', 'VECTOR', 'ZEROS', 'ONES', 'FILL', 'RANDOM',
        'RANGE', 'NUMSEQ', 'STEP',
        # Аналитика
        'ABC', 'PERCENTOF', 'ANOMALY',
        # Оконные
        'ROWNUMBER', 'RANK', 'DENSERANK', 'PERCENTRANK', 'CUMEDIST', 'NTILE',
        'LAG', 'LEAD', 'FIRSTVALUE', 'LASTVALUE', 'NTHVALUE',
        'WINSUM', 'WINAVG', 'WINCOUNT', 'WINMIN', 'WINMAX',
        'WINMEDIAN', 'WINSTDEV', 'QUALIFY',
        # Даты
        'YEAR', 'MONTH', 'DAY', 'QUARTER',
        'WEEKDAY', 'WEEKDAYNAME', 'MONTHNAME',
        'ADDDAYS', 'ADDMONTHS', 'ADDYEARS', 'DATETRUNC',
        'DATE', 'DATEDIFF', 'DATENOW', 'TIMENOW',
        'CALENDAR', 'CALENDARPRO',
        # Время
        'HOUR', 'MINUTE', 'SECOND', 'AMPM', 'IS_PM',
        'ADDHOURS', 'ADDMINUTES', 'ADDSECONDS',
        'TIMETRUNC', 'TIME', 'TIMESTAMP',
        'IS_VALID_TIME',
        # Типы / None
        'TYPE',
        'IS_NUMBER', 'IS_INTEGER', 'IS_FLOAT', 'IS_STRING', 'IS_BOOLEAN',
        'IS_NULL', 'TO_STRING', 'TO_NUMBER',
        'FILLNA', 'DROPNA', 'COALESCE', 'NULL_IF',
        # Файлы
        'OPENEXCEL', 'SAVEEXCEL', 'OPENEXCELSHOW', 'SAVEEXCELSHOW',
        'OPENCSV', 'SAVECSV', 'OPENCSVSHOW', 'SAVECSVSHOW',
        'OPENTXT', 'SAVETXT', 'OPENTXTSHOW', 'SAVETXTSHOW',
        'OPENPARQUET', 'SAVEPARQUET',
        'OPENSQLITE', 'SAVESQLITE', 'QUERYSQLITE',
        'OPENSQLITESHOW', 'SAVESQLITESHOW',
        # Конвертация
        'TOMATRIX', 'TOBIGDATA',
        'CONVERT_BIGDATA_TO_MATRIX', 'CONVERT_MATRIX_TO_BIGDATA',
        # Ввод / логирование
        'INPUTSHOW', 'INPUTSHOWFORM', 'INPUTLISTSHOW', 'PRINT_SHOW',
        'LOGTOFILE', 'LOGOFF',
        # Графики
        'CHART', 'BAR', 'LINE', 'PIE', 'HIST', 'SCATTER', 'BOX',
        'HEATMAP', 'PAIR',
        'TITLE', 'SAVE', 'BINS', 'COLOR', 'XLABEL', 'YLABEL',
        'PLOTLY', 'STATIC',
        # Отчёты
        'REPORT', 'REPORT_SECTION', 'REPORT_TEXT', 'REPORT_TABLE',
        'REPORT_CHART', 'REPORT_SAVE', 'REPORT_SHOW', 'REPORT_SAVE_PDF',
        # Join
        'ON', 'HOW', 'SUFFIXES',
        # Matrixmod действия (дублируют)
        'DUPLICATE', 'CLEAR', 'KEEP', 'SWAP',
        # Аналитика — опции
        'COEF', 'IQR', 'ZSCORE', 'PERCENTILE', 'ONLY',
        # Индексация и режимы
        'ALL', 'END_KEYWORD', 'BEGIN_KEYWORD', 'LAST_KEYWORD',
        'BIGDATA', 'TABLE',
        'ROWS', 'COLS',
    }

    SKIP = SERVICE_TOKENS | FUNCTION_TOKENS

    keywords_lower = set(k.lower() for k in keywords)

    missing = []
    for tok in lexer_tokens:
        if tok in SKIP:
            continue
        if tok.lower() in keywords_lower:
            continue
        missing.append(tok)

    if missing:
        _warn(f"Токены из lexer, которых нет в KEYWORDS: {len(missing)}")
        for tok in sorted(set(missing)):
            print(f"      • {tok}")
    else:
        _ok("Все ключевые слова из lexer есть в KEYWORDS")

    return len(missing) == 0


def check_autocomplete_fields(auto):
    """У всех записей должны быть signature, description, example."""
    _section("4. AUTOCOMPLETE_ITEMS — обязательные поля")

    problems = []
    for name, item in auto.items():
        if not item.get('signature'):
            problems.append(f"{name}: нет signature")
        if not item.get('description'):
            problems.append(f"{name}: нет description")
        if not item.get('example'):
            problems.append(f"{name}: нет example")

    if problems:
        _fail(f"Проблемы: {len(problems)}")
        for p in problems:
            print(f"      • {p}")
    else:
        _ok(f"Все {len(auto)} записей имеют signature + description + example")

    return len(problems) == 0


def check_special_fields(special):
    """У всех спецслов должны быть signature, description, example."""
    _section("5. SPECIAL_WORDS — обязательные поля")

    problems = []
    for name, item in special.items():
        if not item.get('signature'):
            problems.append(f"{name}: нет signature")
        if not item.get('description'):
            problems.append(f"{name}: нет description")
        if not item.get('example'):
            problems.append(f"{name}: нет example")

    if problems:
        _fail(f"Проблемы: {len(problems)}")
        for p in problems:
            print(f"      • {p}")
    else:
        _ok(f"Все {len(special)} записей имеют signature + description + example")

    return len(problems) == 0


def check_signatures_category(sig):
    """У всех функций в signatures.py должна быть category."""
    _section("6. signatures.py — поле category")

    problems = []
    for name, item in sig.items():
        if not item.get('category'):
            problems.append(name)

    if problems:
        _warn(f"Без category: {len(problems)}")
        for p in sorted(problems):
            print(f"      • {p}")
    else:
        _ok(f"Все {len(sig)} функций имеют category")

    return len(problems) == 0


def check_help_files():
    """Проверяет наличие и размер Help-файлов (в help/ или в корне)."""
    _section("7. Help-файлы")

    ok = True
    for fname, min_size in [
        ('Help.txt', 5000),
        ('Help_EN.txt', 5000),
        ('about.txt', 50),
        ('about_EN.txt', 50),
        ('license.txt', 50),
        ('license_EN.txt', 50),
    ]:
        # Ищем в help/, потом в корне
        candidates = [
            PROJECT_DIR / "help" / fname,
            PROJECT_DIR / fname,
        ]
        path = None
        for c in candidates:
            if c.exists():
                path = c
                break

        if path is None:
            _fail(f"{fname} — не найден (искали в help/ и в корне)")
            ok = False
        else:
            size = path.stat().st_size
            if size < min_size:
                _warn(f"{fname} — подозрительно мал ({size} байт) — {path}")
                ok = False
            else:
                rel = path.relative_to(PROJECT_DIR)
                _ok(f"{fname} — {size} байт — {rel}")

    return ok


# ============================================================
# ГЛАВНАЯ
# ============================================================
def main():
    print(f"{C.BOLD}ArrayVator — проверка согласованности баз{C.END}")
    print(f"Проект: {PROJECT_DIR}")

    modules = load_modules()

    sig = modules.get('signatures', {})
    auto = modules.get('autocomplete', {})
    special = modules.get('special', {})
    keywords = modules.get('keywords', [])
    db_ru = modules.get('db_ru', {})
    db_en = modules.get('db_en', {})

    lexer_tokens = extract_lexer_tokens()

    print()
    print(f"{C.DIM}Загружено:{C.END}")
    print(f"  signatures:       {len(sig)}")
    print(f"  AUTOCOMPLETE:     {len(auto)}")
    print(f"  SPECIAL_WORDS:    {len(special)}")
    print(f"  KEYWORDS:         {len(keywords)}")
    print(f"  db_ru:            {len(db_ru)}")
    print(f"  db_en:            {len(db_en)}")
    print(f"  lexer tokens:     {len(lexer_tokens)}")

    results = []
    results.append(("signatures vs autocomplete",
                    check_signatures_vs_autocomplete(sig, auto)))
    results.append(("db_ru vs db_en", check_db_keys(db_ru, db_en)))
    results.append(("lexer vs KEYWORDS", check_lexer_vs_keywords(lexer_tokens, keywords)))
    results.append(("AUTOCOMPLETE поля", check_autocomplete_fields(auto)))
    results.append(("SPECIAL_WORDS поля", check_special_fields(special)))
    results.append(("signatures category", check_signatures_category(sig)))
    results.append(("Help-файлы", check_help_files()))

    # ============================================================
    # ИТОГ
    # ============================================================
    _section("ИТОГ")

    all_ok = True
    for name, ok in results:
        status = f"{C.GREEN}✅{C.END}" if ok else f"{C.RED}❌{C.END}"
        print(f"  {status} {name}")
        if not ok:
            all_ok = False

    print()
    if all_ok:
        print(f"{C.GREEN}{C.BOLD}🎉 Всё согласовано!{C.END}")
        return 0
    else:
        print(f"{C.RED}{C.BOLD}💥 Есть рассинхроны. Смотри отчёт выше.{C.END}")
        return 1


if __name__ == '__main__':
    sys.exit(main())