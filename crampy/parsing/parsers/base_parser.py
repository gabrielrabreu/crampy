from abc import ABC, abstractmethod

from ...modeling import QuizModel


class BaseParser(ABC):
    @abstractmethod
    def parse(self, data: str) -> QuizModel:
        raise NotImplementedError
