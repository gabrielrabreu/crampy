from typing import Type

from modeling import QuizModel
from .parsers import BaseParser, JsonParser


class Parser:
    def __init__(self):
        self._standard_parsers = self._get_standard_parsers()

    def parse(self, data: str, code: str) -> QuizModel:
        parser = self._get_parser(code)
        return parser.parse(data)

    @staticmethod
    def _get_standard_parsers() -> dict[str, Type[BaseParser]]:
        return {
            "json": JsonParser
        }

    def _get_parser(self, code: str) -> BaseParser:
        parsers = self._standard_parsers
        if code in parsers:
            return parsers[code]()
        raise ValueError(f"Parsing failed: "
                         f"Parser '{code}' does not exist.")
