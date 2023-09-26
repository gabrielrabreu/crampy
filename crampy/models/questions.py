from abc import ABC
from typing import List


class QuestionModel(ABC):
    def __init__(self, statement: str):
        self._statement: str = statement

    @property
    def statement(self) -> str:
        return self._statement


class OpenAnswerQuestionModel(QuestionModel):
    def __init__(self, statement: str, expected_answer: str):
        super().__init__(statement)
        self._expected_answer: str = expected_answer

    @property
    def expected_answer(self) -> str:
        return self._expected_answer


class CompositeQuestionModel(QuestionModel):
    def __init__(self, statement: str):
        super().__init__(statement)
        self._sub_questions: List[QuestionModel] = []

    @property
    def sub_questions(self) -> tuple[QuestionModel]:
        return tuple(self._sub_questions)

    def add_sub_question(self, sub_question: QuestionModel) -> None:
        if isinstance(sub_question, CompositeQuestionModel):
            raise ValueError("Can't add a sub question of Composite type.")
        self._sub_questions.append(sub_question)
