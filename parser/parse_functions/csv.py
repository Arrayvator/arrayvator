# parser/parse_functions/csv.py
"""
Парсинг CSV-функций:
    OpenCSV("file.csv")               — авто
    OpenCSV("file.csv", BigData)      — принудительно DuckDB
    OpenCSV("file.csv", Table)        — принудительно RAM
    SaveCSV(m, "out.csv")
    OpenCSVShow()                     — диалог + авто
    OpenCSVShow(BigData)              — диалог + DuckDB
    OpenCSVShow(Table)                — диалог + RAM
    SaveCSVShow(m)
"""

from ast_nodes import OpenCSVNode, SaveCSVNode, OpenCSVShowNode, SaveCSVShowNode
from ast_nodes import StringNode
from errors import ArrayVatorError


def parse_csv(self, token_type):
    """Парсинг CSV-функций"""
    self.expect('LPAREN')

    if token_type == 'OPENCSV':
        file_path = self.parse_expression()

        # Опциональный второй аргумент — режим
        mode = None
        if self.check('COMMA'):
            self.expect('COMMA')
            mode = self.parse_expression()

            # Валидация: режим должен быть BigData или Table
            if isinstance(mode, StringNode):
                v = mode.value.strip().lower()
                if v not in ('duckdb', 'matrix'):
                    raise ArrayVatorError(
                        code="CSV_BAD_MODE",
                        context=self._get_context(),
                        message=(
                            f"Неверный режим OpenCSV: '{mode.value}'.\n"
                            f"  Допустимо: BigData, Table."
                        ),
                        suggestion=(
                            "Используйте один из режимов:\n"
                            "     OpenCSV(\"file.csv\")               — авто (по размеру)\n"
                            "     OpenCSV(\"file.csv\", BigData)      — принудительно DuckDB\n"
                            "     OpenCSV(\"file.csv\", Table)        — принудительно RAM"
                        ),
                    )

        self.expect('RPAREN')
        return OpenCSVNode(file_path, mode)

    elif token_type == 'SAVECSV':
        data = self.parse_expression()
        self.expect('COMMA')
        file_path = self.parse_expression()
        self.expect('RPAREN')
        return SaveCSVNode(data, file_path)

    elif token_type == 'OPENCSVSHOW':
        # Опциональный режим
        mode = None
        if not self.check('RPAREN'):
            mode = self.parse_expression()

            if isinstance(mode, StringNode):
                v = mode.value.strip().lower()
                if v not in ('duckdb', 'matrix'):
                    raise ArrayVatorError(
                        code="CSV_BAD_MODE",
                        context=self._get_context(),
                        message=(
                            f"Неверный режим OpenCSVShow: '{mode.value}'.\n"
                            f"  Допустимо: BigData, Table."
                        ),
                        suggestion=(
                            "Используйте один из режимов:\n"
                            "     OpenCSVShow()               — авто\n"
                            "     OpenCSVShow(BigData)        — DuckDB\n"
                            "     OpenCSVShow(Table)          — RAM"
                        ),
                    )

        self.expect('RPAREN')
        return OpenCSVShowNode(mode)

    elif token_type == 'SAVECSVSHOW':
        data = self.parse_expression()
        self.expect('RPAREN')
        return SaveCSVShowNode(data)