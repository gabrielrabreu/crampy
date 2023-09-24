from abc import ABC
from typing import List


class QuestionModel(ABC):
    def __init__(self, statement: str):
        self.statement: str = statement


class OpenAnswerQuestionModel(QuestionModel):
    def __init__(self, statement: str, expected_answer: str):
        super().__init__(statement)
        self.expected_answer: str = expected_answer


class CompositeQuestionModel(QuestionModel):
    def __init__(self, statement: str, sub_questions: List[QuestionModel]):
        super().__init__(statement)
        self.sub_questions = sub_questions
