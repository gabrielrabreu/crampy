from typing import Type

from .converters import BaseConverter, HtmlConverter
from ..modeling import QuizModel


class Converter:
    def __init__(self):
        self._standard_converters = self._get_standard_converters()

    def convert(self, mode: str, quiz_model: QuizModel, code: str) -> str:
        if mode == "notecards":
            return self._as_notecards(quiz_model, code)
        return self._as_practice_test(quiz_model, code)

    def _as_practice_test(self, quiz_model: QuizModel, code: str) -> str:
        converter = self._get_converter(code)
        return converter.as_practice_test(quiz_model)

    def _as_notecards(self, quiz_model: QuizModel, code: str) -> str:
        converter = self._get_converter(code)
        return converter.as_notecards(quiz_model)

    @staticmethod
    def _get_standard_converters() -> dict[str, Type[BaseConverter]]:
        return {
            "html": HtmlConverter
        }

    def _get_converter(self, code: str) -> BaseConverter:
        converters = self._standard_converters
        if code in converters:
            return converters[code]()
        raise ValueError("Exporting failed: "
                         f"Converter '{code}' does not exist.")
