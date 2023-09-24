from abc import ABC, abstractmethod
from jinja2 import Environment, BaseLoader

from ..models import QuizModel, OpenAnswerQuestionModel, QuestionModel, MultipleChoiceQuestionModel, \
    CompositeQuestionModel


class QuizConverter(ABC):
    @abstractmethod
    def _practice_test_handles(self,  question_model: QuestionModel) -> bool:
        raise NotImplementedError

    @abstractmethod
    def as_practice_test(self, quiz_model: QuizModel) -> str:
        raise NotImplementedError

    @abstractmethod
    def _notecards_handles(self, question_model: QuestionModel) -> bool:
        raise NotImplementedError

    @abstractmethod
    def as_notecards(self, quiz_model: QuizModel) -> str:
        raise NotImplementedError

    @staticmethod
    def _is_open_answer_question(question_model: QuestionModel) -> bool:
        return isinstance(question_model, OpenAnswerQuestionModel)

    @staticmethod
    def _is_multiple_choice_question(question_model: QuestionModel) -> bool:
        return isinstance(question_model, MultipleChoiceQuestionModel)

    @staticmethod
    def _is_composite_question(question_model: QuestionModel) -> bool:
        return isinstance(question_model, CompositeQuestionModel)


class QuizHtmlConverter(QuizConverter):
    def _practice_test_handles(self, question_model: QuestionModel) -> bool:
        if self._is_open_answer_question(question_model):
            return True
        elif self._is_multiple_choice_question(question_model):
            return True
        elif self._is_composite_question(question_model):
            return True
        else:
            return False

    def as_practice_test(self, quiz_model: QuizModel) -> str:
        for question in quiz_model.questions:
            if not self._notecards_handles(question):
                raise ValueError(f"Practice test converter cant handle question f'{question}'")

        env = Environment(loader=BaseLoader())
        env.filters["is_open_answer_question"] = self._is_open_answer_question
        env.filters["is_multiple_choice_question"] = self._is_multiple_choice_question
        env.filters["is_composite_question"] = self._is_composite_question

        template_str = """<!DOCTYPE html>
<html lang="en">
    <head>
        <meta name="description" content="Practice Test">
        <title>{{ quiz.name }}</title>
        <style>
            body { 
                font-family: Arial, sans-serif; 
            }
            .quiz-area { 
                font-size: 1.0em; 
                margin: 0; 
            }
            .quiz-name { 
                font-weight: bold; 
                font-size: 1.5em; 
                margin: 0; 
            }
            .question-statement { 
                font-weight: bold; 
                font-size: 1.0em; 
            }
            .question-choices { 
                list-style-type: none; 
                padding-left: 0; 
            }
            .question-choice { 
                font-size: 1.0em; 
            }
        </style>
    </head>
    <body>
        <header>
            <p class="quiz-area">{{ quiz.area }}</p>
            <p class="quiz-name">{{ quiz.name }}</p>
        </header>
        <div>
            {%- for question in quiz.questions %}
            <div class="question">
                <p class="question-statement">{{ question.statement }}</p>
                {%- if question|is_open_answer_question %}
                {%- elif question|is_multiple_choice_question %}
                <ul class="question-choices">
                    {%- for choice in question.choices %}
                    <li class="question-choice">{{ choice }}</li>
                    {%- endfor %}
                </ul>
                {%- elif question|is_composite_question %}
                {%- for subquestion in question.sub_questions %}
                <div class="question">
                    <p class="question-statement">{{ subquestion.statement }}</p>
                    {%- if subquestion|is_open_answer_question %}
                    {%- elif subquestion|is_multiple_choice_question %}
                    <ul class="question-choices">
                        {%- for choice in subquestion.choices %}
                        <li class="question-choice">{{ choice }}</li>
                        {%- endfor %}
                    </ul>
                    {%- endif %}
                </div>
                {%- endfor %}
                {%- endif %}
            </div>
            {%- endfor %}
        </div>
    </body>
</html>"""

        template = env.from_string(template_str)
        rendered_html = template.render(quiz=quiz_model)
        return rendered_html

    def _notecards_handles(self, question_model: QuestionModel) -> bool:
        if self._is_open_answer_question(question_model):
            return True
        elif self._is_multiple_choice_question(question_model):
            return False
        elif self._is_composite_question(question_model):
            return False
        else:
            return False

    def as_notecards(self, quiz_model: QuizModel) -> str:
        for question in quiz_model.questions:
            if not self._notecards_handles(question):
                raise ValueError(f"Notecard converter cant handle question f'{question}'")

        env = Environment(loader=BaseLoader())
        env.filters["is_open_answer_question"] = self._is_open_answer_question

        template_str = """<!DOCTYPE html>
<html lang="en">
    <head>
        <meta name="description" content="Notecards">
        <title>{{ quiz.name }}</title>
        <style>
            body { 
                font-family: Arial, sans-serif; 
            }
            .notecards {
                column-count: 2;
                column-gap: 20px;
            }
            .notecard {
                width: 300px;
                height: 100px;
                border: 1px solid #000;
                font-size: 1.0em;
                display: flex;
                flex-direction: column;
                justify-content: center;
                align-items: center;
                overflow: hidden;
            }
            .question-statement { 
                font-weight: bold; 
                font-size: 1.0em; 
            }
            .new-print-page {
                page-break-after: always;
            }
        </style>
    </head>
    <body>
        {%- for question in quiz.questions %}
        <div class="notecards">
            <div class="notecard">
                <div class="question-statement">{{ question.statement }}</div>
            </div>
            <div class="notecard">
                <div class="question-statement">{{ question.statement }}</div>
            </div>
        </div>
        {%- endfor %}
        <div class="new-print-page"></div>
        {%- for index, question in questions %}
        <div class="notecards">
            <div class="notecard">
                {%- if question|is_open_answer_question %}
                <div>{{ question.expected_answer }}</div>
                {%- endif %}
            </div>
            <div class="notecard">
                {%- if index % 2 == 1 and index != (len_questions - 1) %}
                {%- if questions|is_open_answer_question %}
                <div>{{ question.expected_answer }}</div>
                {%- endif %}
                {%- endif %}
            </div>
        </div>
        {%- endfor %}
    </body>
</html>"""
        # TODO: talvez pra alinhar só iterar o for ao contrário!
        template = env.from_string(template_str)
        rendered_html = template.render(quiz=quiz_model,
                                        questions=enumerate(quiz_model.questions),
                                        len_questions=len(quiz_model.questions))
        return rendered_html
