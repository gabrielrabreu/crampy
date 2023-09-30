from abc import ABC, abstractmethod
from typing import List, Any, Type


class QuestionModel(ABC):
    def __init__(self, statement: str):
        self._statement: str = statement

    @property
    def statement(self) -> str:
        return self._statement

    @classmethod
    @abstractmethod
    def from_dict(cls, data_dict: dict[str, Any]) -> "QuestionModel":
        raise NotImplementedError


class OpenAnswerQuestionModel(QuestionModel):
    def __init__(self, statement: str, expected_answer: str):
        super().__init__(statement)
        self._expected_answer: str = expected_answer

    @property
    def expected_answer(self) -> str:
        return self._expected_answer

    @classmethod
    def from_dict(cls, data_dict: dict[str, Any]) -> "OpenAnswerQuestionModel":
        statement = data_dict["statement"]
        expected_answer = data_dict["expected_answer"]
        question = OpenAnswerQuestionModel(statement, expected_answer)
        return question


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

    @classmethod
    def from_dict(cls, data_dict: dict[str, Any]) -> "CompositeQuestionModel":
        statement = data_dict["statement"]
        question = CompositeQuestionModel(statement)
        for sub_question in data_dict["sub_questions"]:
            question.add_sub_question(QuestionFactory().create(sub_question))
        return question


class QuestionFactory:
    def __init__(self):
        self._switch = self._get_switch()

    def create(self, data_dict: dict[str, Any]) -> QuestionModel:
        type_desc = data_dict["type"]
        case = self._get_switch().get(type_desc)
        if case is None:
            raise ValueError(f"Question type '{type_desc}' is invalid. ")
        return case.from_dict(data_dict)

    @staticmethod
    def _get_switch() -> dict[str, Type[QuestionModel]]:
        switch = {
            "OpenAnswer": OpenAnswerQuestionModel,
            "Composite": CompositeQuestionModel
        }
        return switch
