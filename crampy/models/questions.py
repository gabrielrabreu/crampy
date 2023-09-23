from abc import ABC
from typing import List


class QuestionModel(ABC):
    def __init__(self, statement: str):
        self.statement: str = statement


class MultipleChoiceQuestionModel(QuestionModel):
    def __init__(self, statement: str, choices: List[str], correct_option: int):
        super().__init__(statement)
        self.choices: List[str] = choices

        if 0 < correct_option <= len(self.choices):
            self.answer: str = self.choices[correct_option - 1]
        else:
            raise IndexError(f"The correct option '{correct_option}' is out of bounds "
                             f"for the choices of length '{len(self.choices)}'.")


class OpenAnswerQuestionModel(QuestionModel):
    def __init__(self, statement: str, expected_answer: str):
        super().__init__(statement)
        self.expected_answer: str = expected_answer


class CompositeQuestionModel(QuestionModel):
    def __init__(self, statement: str, sub_questions: List[QuestionModel]):
        super().__init__(statement)
        self.sub_questions = sub_questions
