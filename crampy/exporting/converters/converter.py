from abc import ABC, abstractmethod

from ...models import QuizModel


class QuizConverter(ABC):
    @abstractmethod
    def as_practice_test(self, quiz_model: QuizModel) -> str:
        raise NotImplementedError

    @abstractmethod
    def as_notecards(self, quiz_model: QuizModel) -> str:
        raise NotImplementedError
