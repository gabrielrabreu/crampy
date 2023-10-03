from pathlib import Path

from utils import is_pathlike
from .settings import Settings
from ..modeling import QuizModel
from ..converting import Converter
from ..parsing import Parser
from ..utils import SourceReader, SourceWriter


class Transformer:
    def __init__(self, settings: Settings):
        self.settings = settings

    def transform(self, path: Path) -> None:
        quiz_model = self._input(path)
        self._output(path, quiz_model)

    def _input(self, path: Path) -> QuizModel:
        with SourceReader(path) as reader:
            data = reader.read()
        return Parser().parse(data, self._get_source_extension(path))

    def _output(self, path: Path, quiz_model: QuizModel) -> None:
        data = Converter().convert(self.settings.convert_mode, quiz_model, self.settings.convert_extension)
        destination = f"{path.parent}\\{quiz_model.area}_{quiz_model.name}.{self.settings.convert_extension}"
        with SourceWriter(destination) as writer:
            writer.write(data)

    @staticmethod
    def _get_source_extension(path: Path) -> str:
        return path.suffix.lstrip(".")
