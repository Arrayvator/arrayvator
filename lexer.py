# lexer.py
import re
from errors import ArrayVatorError, ErrorContext


class Lexer:
    def __init__(self, source):
        self.source = source
        self.tokens = []
        self.pos = 0
        self.line = 1
        self.line_start = 0

    def _get_context(self, pos):
        line_start = self.source.rfind('\n', 0, pos) + 1
        line_end = self.source.find('\n', pos)
        if line_end == -1:
            line_end = len(self.source)

        source_line = self.source[line_start:line_end]
        column = pos - line_start
        line_number = self.source[:pos].count('\n') + 1

        return line_number, column, source_line

    def tokenize(self):
        patterns = [
            # ============================================================
            # ОБРАБОТКА ОШИБОК
            # ============================================================
            (r'(?i)\btry\b', 'TRY'),
            (r'(?i)\bcatch\b', 'CATCH'),
            (r'(?i)\berror\b', 'ERROR'),

            # ============================================================
            # ЗАПРЕЩЁННЫЕ ЛИТЕРАЛЫ (ловить ДО None и ДО IDENTIFIER!)
            # null  → BANNED_NULL
            # nan   → BANNED_NAN
            # ============================================================
            (r'(?i)\bnan\b', 'BANNED_NAN'),
            (r'(?i)\bnull\b', 'BANNED_NULL'),

            # ============================================================
            # УПРАВЛЯЮЩИЕ
            # ============================================================
            (r'(?i)\bif\b', 'IF'),
            (r'(?i)\bthen\b', 'THEN'),
            (r'(?i)\belse\b', 'ELSE'),
            (r'(?i)\bfor\b', 'FOR'),
            (r'(?i)\bto\b', 'TO'),
            (r'(?i)\bdo\b', 'DO'),
            (r'(?i)\bwhile\b', 'WHILE'),
            (r'(?i)\bbreak\b', 'BREAK'),

            # ============================================================
            # ВЫВОД / ВВОД
            # ============================================================
            (r'(?i)\bprint\b', 'PRINT'),
            (r'(?i)\bprintln\b', 'PRINTLN'),
            (r'(?i)\bprintshow\b', 'PRINT_SHOW'),
            (r'(?i)\binput\b', 'INPUT'),
            (r'(?i)\bInputListShow\b', 'INPUTLISTSHOW'),
            (r'(?i)\bInputShowForm\b', 'INPUTSHOWFORM'),
            (r'(?i)\bInputShow\b', 'INPUTSHOW'),

            # ============================================================
            # ЛОГИРОВАНИЕ
            # ============================================================
            (r'(?i)\bLogToFile\b', 'LOGTOFILE'),
            (r'(?i)\bLogOff\b', 'LOGOFF'),

            # ============================================================
            # КАЛЕНДАРЬ
            # ============================================================
            (r'(?i)\bcalendarpro\b', 'CALENDARPRO'),
            (r'(?i)\bcalendar\b', 'CALENDAR'),

            # ============================================================
            # ДАТЫ — извлечение
            # ============================================================
            (r'(?i)\bweekdayname\b', 'WEEKDAYNAME'),
            (r'(?i)\bmonthname\b', 'MONTHNAME'),
            (r'(?i)\bweekday\b', 'WEEKDAY'),
            (r'(?i)\bquarter\b', 'QUARTER'),
            (r'(?i)\byear\b', 'YEAR'),
            (r'(?i)\bmonth\b', 'MONTH'),
            (r'(?i)\bday\b', 'DAY'),

            # ============================================================
            # ВРЕМЯ — арифметика (ДО adddays!)
            # ============================================================
            (r'(?i)\baddseconds\b', 'ADDSECONDS'),
            (r'(?i)\baddminutes\b', 'ADDMINUTES'),
            (r'(?i)\baddhours\b', 'ADDHOURS'),

            # ============================================================
            # ДАТЫ — арифметика
            # ============================================================
            (r'(?i)\baddmonths\b', 'ADDMONTHS'),
            (r'(?i)\baddyears\b', 'ADDYEARS'),
            (r'(?i)\badddays\b', 'ADDDAYS'),

            # ============================================================
            # ВРЕМЯ — извлечение
            # ============================================================
            (r'(?i)\bsecond\b', 'SECOND'),
            (r'(?i)\bminute\b', 'MINUTE'),
            (r'(?i)\bhour\b', 'HOUR'),
            (r'(?i)\bis_pm\b', 'IS_PM'),
            (r'(?i)\bampm\b', 'AMPM'),

            # ============================================================
            # ВРЕМЯ — обрезка и конвертация
            # ============================================================
            (r'(?i)\btimetrunc\b', 'TIMETRUNC'),
            (r'(?i)\btimestamp\b', 'TIMESTAMP'),
            (r'(?i)\btime\b', 'TIME'),

            # ============================================================
            # IS_VALID_TIME
            # ============================================================
            (r'(?i)\bis_valid_time\b', 'IS_VALID_TIME'),

            # ============================================================
            # ДАТЫ — обрезка
            # ============================================================
            (r'(?i)\bdatetrunc\b', 'DATETRUNC'),

            # ============================================================
            # ДАТЫ (старые)
            # ============================================================
            (r'(?i)\bDateNow\b', 'DATENOW'),
            (r'(?i)\bTimeNow\b', 'TIMENOW'),
            (r'(?i)\bDateDiff\b', 'DATEDIFF'),
            (r'(?i)\bdate\b', 'DATE'),
            (r'(?i)\bdatediff\b', 'DATEDIFF'),

            # ============================================================
            # RANGE / NUMBER
            # ============================================================
            (r'(?i)\brange\b', 'RANGE'),
            (r'(?i)\bnumber\b', 'NUMSEQ'),
            (r'(?i)\bstep\b', 'STEP'),

            # ============================================================
            # УСЛОВНЫЕ АГРЕГАТЫ
            # ВАЖНО: COUNTIF / COUNTUNIQUEIF / MEDIANIF — ДО COUNT/MEDIAN,
            # чтобы префикс "count" не съел "countif", а "median" — "medianif".
            # ============================================================
            (r'(?i)\bcountuniqueif\b', 'COUNTUNIQUEIF'),
            (r'(?i)\bsumproduct\b', 'SUMPRODUCT'),
            (r'(?i)\bmedianif\b', 'MEDIANIF'),
            (r'(?i)\bcountif\b', 'COUNTIF'),
            (r'(?i)\bsumif\b', 'SUMIF'),
            (r'(?i)\bavgif\b', 'AVGIF'),
            (r'(?i)\bminif\b', 'MINIF'),
            (r'(?i)\bmaxif\b', 'MAXIF'),

            # ============================================================
            # СТАТИСТИКА
            # ВАЖНО: COUNT / MEDIAN / STD идут ПОСЛЕ *if-версий.
            # Регулярка \bcount\b с \b не матчит "countif",
            # но порядок оставлен для читаемости.
            # ============================================================
            (r'(?i)\bcount\b', 'COUNT'),
            (r'(?i)\bmedian\b', 'MEDIAN'),
            (r'(?i)\bstd\b', 'STD'),

            (r'(?i)\bsum\b', 'SUM'),
            (r'(?i)\bmin\b', 'MIN'),
            (r'(?i)\bmax\b', 'MAX'),
            (r'(?i)\bavg\b', 'AVG'),

            (r'(?i)\blenrow\b', 'LENROW'),
            (r'(?i)\blencol\b', 'LENCOL'),
            (r'(?i)\blen\b', 'LEN'),

            # ============================================================
            # УДАЛЕНИЕ
            # ============================================================
            (r'(?i)\bdeleteif\b', 'DELETEIF'),
            (r'(?i)\bdelete\b', 'DELETE'),
            (r'(?i)\btranspose\b', 'TRANSPOSE'),
            (r'(?i)\bfilterif\b', 'FILTERIF'),

            # ============================================================
            # МАТЕМАТИКА
            # ============================================================
            (r'(?i)\bround\b', 'ROUND'),
            (r'(?i)\bfrac_digits\b', 'FRAC_DIGITS'),
            (r'(?i)\bfrac\b', 'FRAC'),
            (r'(?i)\bint\b', 'INT'),

            # ============================================================
            # СТРОКИ
            # ============================================================
            (r'(?i)\breplacetext\b', 'REPLACETEXT'),
            (r'(?i)\bdeletetextleft\b', 'DELETETEXTLEFT'),
            (r'(?i)\bdeletetextright\b', 'DELETETEXTRIGHT'),
            (r'(?i)\btrimleft\b', 'TRIMLEFT'),
            (r'(?i)\btrimright\b', 'TRIMRIGHT'),
            (r'(?i)\btrim\b', 'TRIM'),
            (r'(?i)\bjoinvector\b', 'JOINVECTOR'),
            (r'(?i)\bsplit\b', 'SPLIT'),
            (r'(?i)\bskip\b', 'SKIP'),

            # ============================================================
            # СОРТИРОВКА
            # ============================================================
            (r'(?i)\bsort\b', 'SORT'),
            (r'(?i)\baz\b', 'AZ'),
            (r'(?i)\bza\b', 'ZA'),

            # ============================================================
            # ВСТАВКА
            # ============================================================
            (r'(?i)\binsertif\b', 'INSERTIF'),
            (r'(?i)\binsert\b', 'INSERT'),

            # ============================================================
            # ПОИСК
            # ============================================================
            (r'(?i)\bfindif\b', 'FINDIF'),
            (r'(?i)\bindex\b', 'FIND'),
            (r'(?i)\bfind\b', 'FIND'),
            (r'(?i)\binside\b', 'INSIDE'),
            (r'(?i)\bignore\b', 'IGNORE'),
            (r'(?i)\brows\b', 'ROWS'),
            (r'(?i)\bcols\b', 'COLS'),

            # ============================================================
            # ОЧИСТКА
            # ============================================================
            (r'(?i)\bclean\b', 'CLEAN'),
            (r'(?i)\bbefore\b', 'BEFORE'),
            (r'(?i)\bafter\b', 'AFTER'),

            # ============================================================
            # VLOOKUP
            # ============================================================
            (r'(?i)\bvlookup\b', 'VLOOKUP'),
            (r'(?i)\bapprox\b', 'APPROX'),

            # ============================================================
            # CASE
            # ============================================================
            (r'(?i)\bcase\b', 'CASE'),
            (r'(?i)\bwhen\b', 'WHEN'),

            # ============================================================
            # EXCEL
            # ============================================================
            (r'(?i)\bOpenExcelShow\b', 'OPENEXCELSHOW'),
            (r'(?i)\bSaveExcelShow\b', 'SAVEEXCELSHOW'),
            (r'(?i)\bOpenExcel\b', 'OPENEXCEL'),
            (r'(?i)\bSaveExcel\b', 'SAVEEXCEL'),

            # ============================================================
            # CSV
            # ============================================================
            (r'(?i)\bOpenCSVShow\b', 'OPENCSVSHOW'),
            (r'(?i)\bSaveCSVShow\b', 'SAVECSVSHOW'),
            (r'(?i)\bOpenCSV\b', 'OPENCSV'),
            (r'(?i)\bSaveCSV\b', 'SAVECSV'),

            # ============================================================
            # РЕЖИМЫ
            # ============================================================
            (r'(?i)\bBigData\b', 'BIGDATA'),
            (r'(?i)\bTable\b', 'TABLE'),

            # ============================================================
            # TXT
            # ============================================================
            (r'(?i)\bOpenTXTShow\b', 'OPENTXTSHOW'),
            (r'(?i)\bSaveTXTShow\b', 'SAVETXTSHOW'),
            (r'(?i)\bOpenTXT\b', 'OPENTXT'),
            (r'(?i)\bSaveTXT\b', 'SAVETXT'),

            # ============================================================
            # PARQUET
            # ============================================================
            (r'(?i)\bOpenParquet\b', 'OPENPARQUET'),
            (r'(?i)\bSaveParquet\b', 'SAVEPARQUET'),

            # ============================================================
            # SQLITE
            # ============================================================
            (r'(?i)\bOpenSQLiteShow\b', 'OPENSQLITESHOW'),
            (r'(?i)\bSaveSQLiteShow\b', 'SAVESQLITESHOW'),
            (r'(?i)\bQuerySQLite\b', 'QUERYSQLITE'),
            (r'(?i)\bOpenSQLite\b', 'OPENSQLITE'),
            (r'(?i)\bSaveSQLite\b', 'SAVESQLITE'),

            # ============================================================
            # ДУБЛИКАТЫ
            # ============================================================
            (r'(?i)\bUnique\b', 'UNIQUE'),
            (r'(?i)\bCountDistinct\b', 'COUNT_DISTINCT'),
            (r'(?i)\bValueCounts\b', 'VALUE_COUNTS'),
            (r'(?i)\bDeleteDuplicate\b', 'DELETE_DUPLICATE'),

            # ============================================================
            # СОЗДАНИЕ
            # ============================================================
            (r'(?i)\bzeros\b', 'ZEROS'),
            (r'(?i)\bones\b', 'ONES'),
            (r'(?i)\brandom\b', 'RANDOM'),
            (r'(?i)\bvector\b', 'VECTOR'),
            (r'(?i)\bmatrixmod\b', 'MATRIXMOD'),
            (r'(?i)\bmatrix\b', 'MATRIX'),

            # ============================================================
            # ADDCOLUMN / ADDROWS
            # ============================================================
            (r'(?i)\baddcolumn\b', 'ADDCOLUMN'),
            (r'(?i)\baddrows\b', 'ADDROWS'),

            # ============================================================
            # АНАЛИТИЧЕСКИЕ
            # ============================================================
            (r'(?i)\bpercentof\b', 'PERCENTOF'),
            (r'(?i)\banomaly\b', 'ANOMALY'),
            (r'(?i)\babc\b', 'ABC'),

            (r'(?i)\bcoef\b', 'COEF'),
            (r'(?i)\biqr\b', 'IQR'),
            (r'(?i)\bzscore\b', 'ZSCORE'),
            (r'(?i)\bpercentile\b', 'PERCENTILE'),
            (r'(?i)\bonly\b', 'ONLY'),

            # ============================================================
            # ГРАФИКИ
            # ============================================================
            (r'(?i)\bchart\b', 'CHART'),
            (r'(?i)\bbar\b', 'BAR'),
            (r'(?i)\bline\b', 'LINE'),
            (r'(?i)\bpie\b', 'PIE'),
            (r'(?i)\bhist\b', 'HIST'),
            (r'(?i)\bscatter\b', 'SCATTER'),
            (r'(?i)\bbox\b', 'BOX'),
            (r'(?i)\bheatmap\b', 'HEATMAP'),
            (r'(?i)\bpair\b', 'PAIR'),
            (r'(?i)\btitle\b', 'TITLE'),
            (r'(?i)\bsave\b', 'SAVE'),
            (r'(?i)\bbins\b', 'BINS'),
            (r'(?i)\bcolor\b', 'COLOR'),
            (r'(?i)\bxlabel\b', 'XLABEL'),
            (r'(?i)\bylabel\b', 'YLABEL'),
            (r'(?i)\bplotly\b', 'PLOTLY'),
            (r'(?i)\bstatic\b', 'STATIC'),

            # ============================================================
            # ОТЧЁТЫ
            # ============================================================
            (r'(?i)\breport_section\b', 'REPORT_SECTION'),
            (r'(?i)\breport_text\b', 'REPORT_TEXT'),
            (r'(?i)\breport_table\b', 'REPORT_TABLE'),
            (r'(?i)\breport_chart\b', 'REPORT_CHART'),
            (r'(?i)\breport_save_pdf\b', 'REPORT_SAVE_PDF'),
            (r'(?i)\breport_save\b', 'REPORT_SAVE'),
            (r'(?i)\breport_show\b', 'REPORT_SHOW'),
            (r'(?i)\breport\b', 'REPORT'),

            # ============================================================
            # МАТРИЧНЫЕ
            # ============================================================
            (r'(?i)\bcopy\b', 'COPY'),
            (r'(?i)\bmove\b', 'MOVE'),
            (r'(?i)\bjoinarray\b', 'JOINARRAY'),
            (r'(?i)\bunpivot\b', 'UNPIVOT'),
            (r'(?i)\bvertical\b', 'VERTICAL'),
            (r'(?i)\bhorizontal\b', 'HORIZONTAL'),

            # ============================================================
            # PIVOT
            # ============================================================
            (r'(?i)\bpivot\b', 'PIVOT'),

            # ============================================================
            # GROUPBY
            # ============================================================
            (r'(?i)\bgroupagg\b', 'GROUPAGG'),
            (r'(?i)\bgroupby\b', 'GROUPBY'),
            (r'(?i)\bby\b', 'BY'),
            (r'(?i)\bagg\b', 'AGG'),
            (r'(?i)\bhaving\b', 'HAVING'),

            # ============================================================
            # FILLDOWN
            # ============================================================
            (r'(?i)\bfilldown\b', 'FILLDOWN'),
            (r'(?i)\bfill\b', 'FILL'),
            (r'(?i)\bexact\b', 'EXACT'),

            # ============================================================
            # SAMPLE
            # ============================================================
            (r'(?i)\bsample\b', 'SAMPLE'),

            # ============================================================
            # APPLYIF
            # ============================================================
            (r'(?i)\bapplyif\b', 'APPLYIF'),

            # ============================================================
            # JOIN
            # ============================================================
            (r'(?i)\bjoin\b', 'JOIN'),
            (r'(?i)\bon\b', 'ON'),
            (r'(?i)\bhow\b', 'HOW'),
            (r'(?i)\bsuffixes\b', 'SUFFIXES'),

            # ============================================================
            # КОНВЕРТАЦИЯ
            # ============================================================
            (r'(?i)\bConvert_BigData_To_Matrix\b', 'CONVERT_BIGDATA_TO_MATRIX'),
            (r'(?i)\bConvert_Matrix_To_BigData\b', 'CONVERT_MATRIX_TO_BIGDATA'),
            (r'(?i)\bToMatrix\b', 'TOMATRIX'),
            (r'(?i)\bToBigData\b', 'TOBIGDATA'),

            # ============================================================
            # NONE — литерал и функции
            # ВАЖНО: noneif ДО none, иначе 'none' съест префикс 'noneif'.
            # ============================================================
            (r'(?i)\bisnone\b', 'IS_NONE'),
            (r'(?i)\bfillna\b', 'FILLNA'),
            (r'(?i)\bdropna\b', 'DROPNA'),
            (r'(?i)\bcoalesce\b', 'COALESCE'),
            (r'(?i)\bnoneif\b', 'NONE_IF'),   # функция noneif
            (r'(?i)\bnone\b', 'NONE'),        # литерал None

            # ============================================================
            # ТИПЫ
            # ============================================================
            (r'(?i)\bis_number\b', 'IS_NUMBER'),
            (r'(?i)\bis_integer\b', 'IS_INTEGER'),
            (r'(?i)\bis_float\b', 'IS_FLOAT'),
            (r'(?i)\bis_string\b', 'IS_STRING'),
            (r'(?i)\bis_boolean\b', 'IS_BOOLEAN'),
            (r'(?i)\bto_string\b', 'TO_STRING'),
            (r'(?i)\bto_number\b', 'TO_NUMBER'),
            (r'(?i)\btype\b', 'TYPE'),

            # ============================================================
            # ОКОННЫЕ
            # ============================================================
            (r'(?i)\brownumber\b', 'ROWNUMBER'),
            (r'(?i)\bdenserank\b', 'DENSERANK'),
            (r'(?i)\bpercentrank\b', 'PERCENTRANK'),
            (r'(?i)\bcumedist\b', 'CUMEDIST'),
            (r'(?i)\bntile\b', 'NTILE'),
            (r'(?i)\blead\b', 'LEAD'),
            (r'(?i)\blag\b', 'LAG'),
            (r'(?i)\bfirstvalue\b', 'FIRSTVALUE'),
            (r'(?i)\blastvalue\b', 'LASTVALUE'),
            (r'(?i)\bnthvalue\b', 'NTHVALUE'),
            (r'(?i)\bwinsum\b', 'WINSUM'),
            (r'(?i)\bwinavg\b', 'WINAVG'),
            (r'(?i)\bwincount\b', 'WINCOUNT'),
            (r'(?i)\bwinmin\b', 'WINMIN'),
            (r'(?i)\bwinmax\b', 'WINMAX'),
            (r'(?i)\bwinmedian\b', 'WINMEDIAN'),
            (r'(?i)\bwinstdev\b', 'WINSTDEV'),
            (r'(?i)\bqualify\b', 'QUALIFY'),
            (r'(?i)\border\b', 'ORDER'),
            (r'(?i)\brank\b', 'RANK'),

            # ============================================================
            # MATRIXMOD ДЕЙСТВИЯ
            # ============================================================
            (r'(?i)\bduplicate\b', 'DUPLICATE'),
            (r'(?i)\bclear\b', 'CLEAR'),
            (r'(?i)\bkeep\b', 'KEEP'),
            (r'(?i)\bswap\b', 'SWAP'),

            # ============================================================
            # ИНДЕКСАЦИЯ
            # ============================================================
            (r'(?i)\ball\b', 'ALL'),
            (r'(?i)\bbegin\b', 'BEGIN_KEYWORD'),
            (r'(?i)\blast\b', 'LAST_KEYWORD'),
            (r'(?i)\bend\+\d+', 'END_PLUS'),
            (r'(?i)\bend\-\d+', 'END_MINUS'),
            (r'(?i)\bend\b', 'END_KEYWORD'),

            # ============================================================
            # ЛОГИЧЕСКИЕ
            # ============================================================
            (r'(?i)\bnot\b', 'NOT'),
            (r'(?i)\band\b', 'AND'),
            (r'(?i)\bor\b', 'OR'),

            (r'(?i)\btrue\b', 'TRUE'),
            (r'(?i)\bfalse\b', 'FALSE'),

            # ============================================================
            # ОПЕРАТОРЫ
            # ============================================================
            (r'==', 'EQUALS'),
            (r'<=', 'LESSEQUAL'),
            (r'>=', 'GREATEREQUAL'),
            (r'!=', 'NOTEQUAL'),
            (r'=', 'ASSIGN'),
            (r'\^', 'POW'),
            (r'//', 'FLOORDIV'),
            (r'\{', 'LBRACE'),
            (r'\}', 'RBRACE'),
            (r'\(', 'LPAREN'),
            (r'\)', 'RPAREN'),
            (r'\[', 'LBRACKET'),
            (r'\]', 'RBRACKET'),
            (r':', 'COLON'),
            (r',', 'COMMA'),
            (r';', 'SEMICOLON'),
            (r'<', 'LESS'),
            (r'>', 'GREATER'),
            (r'\+', 'PLUS'),
            (r'-', 'MINUS'),
            (r'\*', 'STAR'),
            (r'/', 'SLASH'),
            (r'%', 'MOD'),

            # ============================================================
            # ЧИСЛА
            # ============================================================
            (r'\d+\.\d+', 'NUMBER'),
            (r'\d+', 'NUMBER'),

            # ============================================================
            # ИДЕНТИФИКАТОРЫ
            # ============================================================
            (r'[a-zA-Zа-яА-Я_][a-zA-Zа-яА-Я0-9_]*', 'IDENTIFIER'),

            # ============================================================
            # КОММЕНТАРИИ И ПРОБЕЛЫ
            # ============================================================
            (r'#.*$', None),
            (r'\s+', None),
        ]

        i = 0
        line = 1

        while i < len(self.source):
            if i > 0:
                line = self.source[:i].count('\n') + 1

            matched = False

            if self.source[i] == '\ufeff':
                i += 1
                continue

            # ============================================================
            # СТРОКИ (кавычки)
            # ============================================================
            if self.source[i] in ('"', "'"):
                quote_char = self.source[i]
                start_line = line

                j = i + 1
                while j < len(self.source) and self.source[j] != quote_char:
                    if self.source[j] == '\n':
                        line_num, column, source_line = self._get_context(i)
                        raise ArrayVatorError(
                            code="UNCLOSED_STRING",
                            context=ErrorContext(
                                line=line_num,
                                column=column,
                                source_line=source_line,
                                source_code=self.source,
                            ),
                        )
                    if self.source[j] == '\\':
                        j += 1
                    j += 1

                if j >= len(self.source):
                    line_num, column, source_line = self._get_context(i)
                    raise ArrayVatorError(
                        code="UNCLOSED_STRING",
                        context=ErrorContext(
                            line=line_num,
                            column=column,
                            source_line=source_line,
                            source_code=self.source,
                        ),
                    )

                value = self.source[i + 1:j]
                self.tokens.append(('STRING', value, start_line))
                i = j + 1
                continue

            # ============================================================
            # ПАТТЕРНЫ
            # ============================================================
            for pattern, token_type in patterns:
                if pattern is None:
                    continue
                regex = re.compile(pattern, re.MULTILINE | re.UNICODE)
                match = regex.match(self.source, i)
                if match:
                    if token_type:
                        value = match.group(0)

                        if token_type == 'IDENTIFIER':
                            value = value.lower()
                        elif token_type in [
                            'ALL', 'END_KEYWORD', 'BEGIN_KEYWORD',
                            'LAST_KEYWORD', 'SKIP', 'AZ', 'ZA',
                            'INSIDE', 'IGNORE', 'BEFORE', 'AFTER',
                            'ROWS', 'COLS',
                            'NONE',
                            'NONE_IF',
                            'BANNED_NAN', 'BANNED_NULL',
                            'END_PLUS', 'END_MINUS',
                            'DATENOW', 'TIMENOW', 'DATEDIFF',
                            'DELETETEXTLEFT', 'DELETETEXTRIGHT',
                            'TRIM', 'TRIMLEFT', 'TRIMRIGHT',
                            'OPENCSV', 'SAVECSV',
                            'OPENCSVSHOW', 'SAVECSVSHOW',
                            'LOGTOFILE', 'LOGOFF',
                            'OPENTXT', 'SAVETXT',
                            'OPENTXTSHOW', 'SAVETXTSHOW',
                            'OPENSQLITE', 'SAVESQLITE',
                            'QUERYSQLITE',
                            'OPENSQLITESHOW', 'SAVESQLITESHOW',
                            'INPUTSHOW', 'INPUTSHOWFORM',
                            'INPUTLISTSHOW',
                            'BIGDATA', 'TABLE',
                            'MATRIXMOD', 'DUPLICATE', 'CLEAR', 'KEEP', 'SWAP',
                            'INSERTIF',
                            'ADDCOLUMN', 'ADDROWS',
                            'GROUPAGG', 'FILLDOWN',
                            'FILL', 'EXACT',
                            'ROWNUMBER', 'RANK', 'DENSERANK',
                            'PERCENTRANK', 'CUMEDIST', 'NTILE',
                            'LAG', 'LEAD',
                            'FIRSTVALUE', 'LASTVALUE', 'NTHVALUE',
                            'WINSUM', 'WINAVG', 'WINCOUNT',
                            'WINMIN', 'WINMAX', 'WINMEDIAN', 'WINSTDEV',
                            'QUALIFY', 'ORDER',
                            'TRY', 'CATCH', 'ERROR',
                            'RANGE', 'NUMSEQ', 'STEP',
                            'ABC', 'PERCENTOF', 'ANOMALY',
                            'COEF', 'IQR', 'ZSCORE', 'PERCENTILE', 'ONLY',
                            # Статистика
                            'COUNT', 'MEDIAN', 'STD',
                            'SUM', 'MIN', 'MAX', 'AVG',
                            # Условные агрегаты
                            'SUMIF', 'COUNTIF', 'AVGIF', 'MINIF', 'MAXIF',
                            'MEDIANIF', 'COUNTUNIQUEIF', 'SUMPRODUCT',
                            'CHART', 'BAR', 'LINE', 'PIE', 'HIST',
                            'SCATTER', 'BOX', 'HEATMAP', 'PAIR',
                            'TITLE', 'SAVE', 'BINS', 'COLOR',
                            'XLABEL', 'YLABEL', 'PLOTLY', 'STATIC',
                            'REPORT', 'REPORT_SECTION', 'REPORT_TEXT',
                            'REPORT_TABLE', 'REPORT_CHART',
                            'REPORT_SAVE', 'REPORT_SHOW', 'REPORT_SAVE_PDF',
                            'YEAR', 'MONTH', 'DAY', 'QUARTER',
                            'WEEKDAY', 'WEEKDAYNAME', 'MONTHNAME',
                            'ADDDAYS', 'ADDMONTHS', 'ADDYEARS',
                            'DATETRUNC',
                            'CALENDAR', 'CALENDARPRO',
                            'HOUR', 'MINUTE', 'SECOND',
                            'AMPM', 'IS_PM',
                            'ADDHOURS', 'ADDMINUTES', 'ADDSECONDS',
                            'TIMETRUNC', 'TIME', 'TIMESTAMP',
                            'IS_VALID_TIME',
                            'IS_NONE', 'FILLNA', 'DROPNA',
                            'COALESCE',
                            'TO', 'DO',
                        ]:
                            value = value.lower()

                        self.tokens.append((token_type, value, line))

                    matched_text = match.group(0)
                    line += matched_text.count('\n')

                    i = match.end()
                    matched = True
                    break

            # ============================================================
            # НЕИЗВЕСТНЫЙ СИМВОЛ
            # ============================================================
            if not matched:
                if self.source[i] in ' \t\n\r\ufeff':
                    i += 1
                    continue

                line_num, column, source_line = self._get_context(i)
                raise ArrayVatorError(
                    code="UNKNOWN_SYMBOL",
                    context=ErrorContext(
                        line=line_num,
                        column=column,
                        source_line=source_line,
                        source_code=self.source,
                    ),
                    message=f"Неизвестный символ: '{self.source[i]}'",
                )

        return self.tokens