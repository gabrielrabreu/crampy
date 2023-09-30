from typing import List, Any

from .questions import QuestionModel, QuestionFactory


class QuizModel:
    def __init__(self, name: str, area: str):
        self._name: str = name
        self._area: str = area
        self._questions: List[QuestionModel] = []

    @property
    def name(self) -> str:
        return self._name

    @property
    def area(self) -> str:
        return self._area

    @property
    def questions(self) -> tuple[QuestionModel]:
        return tuple(self._questions)

    def add_question(self, question: QuestionModel) -> None:
        self._questions.append(question)

    @classmethod
    def from_dict(cls, data_dict: dict[str, Any]) -> "QuizModel":
        name = data_dict["name"]
        area = data_dict["area"]
        quiz = QuizModel(name, area)
        for question in data_dict["questions"]:
            quiz.add_question(QuestionFactory().create(question))
        return quiz


