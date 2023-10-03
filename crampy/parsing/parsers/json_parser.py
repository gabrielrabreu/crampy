from json import loads as json_loads

from .base_parser import BaseParser
from ...modeling import QuizModel


class JsonParser(BaseParser):
    def parse(self, data: str) -> QuizModel:
        data_dict = json_loads(data)
        return QuizModel.from_dict(data_dict)
