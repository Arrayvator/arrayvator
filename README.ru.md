# ArrayVator

> **DSL для анализа табличных данных** — со **сборкой в `.exe` в 2 клика**.
> Без Python. Без PyInstaller. Без бубна.

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Platform: Windows](https://img.shields.io/badge/platform-Windows-blue.svg)]()
[![Version](https://img.shields.io/badge/version-0.1.0-green.svg)](https://github.com/Arrayvator/arrayvator/releases)

![ArrayVator Editor](screenshot_filterif.png)

---

## Что такое ArrayVator?

ArrayVator — это **предметно-ориентированный язык** для анализа табличных
данных. Вы пишете на понятном синтаксисе, а получаете результат, как
от SQL + Python + Excel, но без необходимости знать все три.

**Ключевые идеи:**

- 📊 **Работа с таблицами** — матрицы, вектора, срезы
- 🚀 **Два движка** — Matrix (RAM) и DuckDB (Big Data)
- 🧠 **Умная справка** — автодополнение + панель справки
- 💬 **Понятные ошибки** — с подсказками, что исправить
- ⚡ **Сборка `.exe` в 2 клика** — упаковка скрипта в готовый файл

---

## 🚀 Killer feature: `.exe` в 2 клика

Пишете скрипт → нажимаете **Инструменты → Экспорт в EXE** → получаете **готовый `.exe`**.

Всё. Без Python, без PyInstaller, без `.spec`-файлов, без возни с DLL.

![ArrayVator Compiler](screenshot_compiler.png)

### Как пользоваться компилятором

1. **Сохраните код** как `.arrv` в редакторе (**Ctrl+S**)
2. Откройте **Инструменты → Экспорт в EXE** — откроется компилятор
3. В компиляторе:
   - **Source .arrv:** — выберите сохранённый `.arrv` (**Browse...**)
   - **Output folder:** — выберите папку куда сохранить `.exe` (**Browse...**)
   - **EXE name:** — введите имя (латиница, без `.exe`)
4. Нажмите **Build EXE** (зелёная кнопка)
5. **Готово!** Ваш `.exe` работает сам по себе

> 💡 **Первый раз?** Нажмите **Rebuild Runtime** — компилятор
> подготовит runtime-файлы. После этого сборка занимает секунды.

### Почему это важно

Если вы **когда-нибудь** пытались упаковать Python-скрипт в `.exe`,
вы знаете эту боль:

- `pip install pyinstaller`
- Написать `.spec`-файл
- Ловить ошибки с `--hidden-import`
- Копировать DLL руками
- Отлаживать `ModuleNotFoundError` в frozen-сборке
- Надеяться, что работает на чужой машине

**ArrayVator делает всё это за вас.**

| Обычный Python | ArrayVator |
|---|---|
| Установить Python | ❌ Не нужно |
| Установить PyInstaller | ❌ Не нужно |
| Писать `.spec` файлы | ❌ Не нужно |
| Разбираться с `--hidden-import` | ❌ Не нужно |
| Паковать DLL | ❌ Не нужно |
| **Результат** | **`.exe` в 2 клика** |

### Автоматический выбор runtime

Компилятор **сам сканирует код** и **подбирает нужный runtime**:

- **`runner_minimal`** — чистый язык (быстро, мало места)
- **`runner_data`** — с Excel / CSV / DuckDB
- **`runner`** — полный: графики + HTML-отчёты

---

## ✨ Возможности

- ⚡ **Сборка `.exe` в 2 клика** — без Python, без PyInstaller
- 📊 **Матрицы и вектора** — таблицы с заголовками, срезы, диапазоны
- 🔍 **Фильтрация** — `filterif`, `deleteif` vs циклы
- 📈 **Агрегаты** — `sum`, `avg`, `min`, `max`, `count`, `median`, `std`
- 🎯 **Условные агрегаты** — `sumif`, `countif`, `avgif`, `minif`, ...
- 📊 **Группировка** — `groupby`, `pivot`, `groupagg`
- 🪟 **Оконные функции** — `rownumber`, `rank`, `lag`, `lead`, `winsum`, `qualify`
- 📅 **Даты и время** — `year`, `adddays`, `DateDiff`, `datetrunc`
- 🧮 **Строки** — `split`, `joinvector`, `replacetext`, `clean`, `trim`
- 🔎 **Поиск** — `find`, `vlookup`
- 🎨 **Условия** — `case`, `applyif`
- 🚀 **BigData** — до 1 млрд строк через DuckDB
- 📉 **Графики** — Matplotlib / Plotly (bar, line, pie, hist, scatter, box, heatmap, pair)
- 📄 **HTML-отчёты** — с интерактивными Plotly-графиками
- 📁 **Файлы** — Excel, CSV, TXT, Parquet, SQLite
- 🧠 **Встроенная справка** — клик по функции → справка справа

---

## 📥 Скачать

Готовую сборку: [**Releases**](https://github.com/Arrayvator/arrayvator/releases/latest)

**Windows** — `ArrayVator_Portable.zip`:

- **`ArrayVator.exe`** — редактор (двойной клик — и работаете)
- **`runner/`** — полный интерпретатор (DuckDB, Excel, графики)
- **`runner_data/`** — для работы с данными (без графики)
- **`runner_minimal/`** — минимальный (только ядро)
- **`compiler/`** — компилятор в EXE (GUI)
- **`help/`** — файлы справки (русский + английский)

**Не требует Python!** Работает на Windows 10/11 (x64).

**Установка:**

1. Скачайте `ArrayVator_Portable.zip`
2. Распакуйте в любую папку
3. Запустите `ArrayVator.exe`

### ⚠️ Первый запуск на Windows

ArrayVator **пока не подписан**. Windows SmartScreen может показать:

> Windows защитила ваш компьютер

**Это нормально.** Нажмите **Подробнее** → **Выполнить в любом случае**.

Исходный код **100% открыт** — проверьте на GitHub или соберите сами.

Мы подали заявку на **бесплатный сертификат подписи**
для open-source проектов (через [SignPath.io](https://signpath.io/)).
Будущие релизы будут подписаны.

---

## 🖼 Скриншоты

### Редактор со встроенной справкой

![ArrayVator Editor](screenshot_filterif.png)

### Панель справки — клик по любой функции

![ArrayVator Help](screenshot_help.png)

### Сборка `.exe` в 2 клика

![ArrayVator Compiler](screenshot_compiler.png)

---

## 🚀 Быстрый старт

```
m = ["Имя", "Отдел", "Зарплата";
     "Аня", "IT", 85000;
     "Боб", "HR", 65000;
     "Света", "IT", 95000]

r = filterif(m[:, "Отдел"] == "IT")
print(r)
```

Вывод:

```
Имя    Отдел  Зарплата
Аня    IT     85000
Света  IT     95000
```

---

## 📚 Примеры

В папке [`examples/`](examples/) — **68 готовых рецептов**
по темам:

| Категория | Что внутри |
|---|---|
| **Основы** | Циклы, условия, матрицы, строки |
| **Фильтрация** | `filterif`, `deleteif` vs циклы |
| **Агрегаты** | `sum`, `avg`, `sumif`, `countif` |
| **Группировка** | `groupby`, `pivot`, `groupagg` — 4 способа одной задачи |
| **Оконные функции** | `rank`, `lag`, `ntile`, `qualify` |
| **Аналитика** | `abc`, `anomaly`, `percentof` |
| **Даты** | Полный справочник по датам и времени |
| **Соединения** | `join`, `joinarray`, `unpivot`, `vlookup` |
| **BigData** | Сравнение Matrix vs DuckDB |

Каждый пример — самодостаточный файл с комментариями, кодом и ожидаемым
выводом. Запускай через **F5** в редакторе.

---

## 🐍 Установка из исходников

**Требования:**

- Python 3.10+
- Windows / Linux / macOS

**Установка:**

```bash
git clone https://github.com/Arrayvator/arrayvator.git
cd arrayvator
pip install -r requirements.txt
python main.py
```

**Зависимости:** `duckdb`, `python-calamine`, `pyexcelerate`, `openpyxl`,
`matplotlib`, `plotly`, `playwright`, `pyinstaller`.

---

## 📖 Документация

- [`examples/`](examples/) — 68 готовых рецептов
- [`help/`](help/) — файлы справки (русский + английский)

---

## 📜 Правила языка

Несколько ключевых правил ArrayVator:

1. **Все функции ВОЗВРАЩАЮТ значение** — сохраняйте результат:
   ```
   m = filterif(m[:, "Отдел"] == "IT")
   ```
2. **`None`** — единственный литерал пустого значения (`null`, `nan` запрещены).
3. **`=`** — присваивание. **`==`** — сравнение.
4. **Логические операторы:** `and`, `or`, `not`.
5. **Индексация С 1** — `m[1, :]` это строка заголовков.
6. **Правило заголовка:**
   - `m[:, "Имя"]` — заголовок НЕ участвует
   - `m[:, 3]` — заголовок УЧАСТВУЕТ
7. **DuckDB (BigData) — read-only** — часть функций только для Matrix.

Подробнее см. [`examples/`](examples/).

---

## 📄 Лицензия

MIT — см. [LICENSE](LICENSE).

---

## 👤 Автор

**Arrayvator**

- Сайт: [arrayvator.ru](http://arrayvator.ru/)
- GitHub: [@Arrayvator](https://github.com/Arrayvator)
