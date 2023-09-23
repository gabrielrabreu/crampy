from typing import List

from .questions import QuestionModel


class QuizModel:
    def __init__(self, name: str, area: str, questions: List[QuestionModel]):
        self.name: str = name
        self.area: str = area
        self.questions: List[QuestionModel] = questions
