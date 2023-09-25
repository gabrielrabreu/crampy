from typing import Type

from .converters import QuizConverter, QuizHtmlConverter
from ..utils import SourceWriter, Source
from ..models import QuizModel


class QuizExporter:
    def __init__(self):
        self._standard_converters = self._get_standard_converters()

    def as_practice_test(self, quiz_model: QuizModel, code: str, source: Source) -> None:
        converter = self._get_converter(code)
        content = converter.as_practice_test(quiz_model)
        with SourceWriter(source) as writer:
            writer.write(content)

    def as_notecards(self, quiz_model: QuizModel, code: str, source: Source) -> None:
        converter = self._get_converter(code)
        content = converter.as_notecards(quiz_model)
        with SourceWriter(source) as writer:
            writer.write(content)

    @staticmethod
    def _get_standard_converters() -> dict[str, Type[QuizConverter]]:
        return {
            "html": QuizHtmlConverter
        }

    def _get_converter(self, code: str) -> QuizConverter:
        converters = self._standard_converters
        if code in converters:
            return converters[code]()
        raise ValueError("Exporting failed: "
                         f"Converter '{code}' does not exist.")
