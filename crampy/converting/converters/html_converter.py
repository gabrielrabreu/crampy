from jinja2 import Environment, BaseLoader

from .base_converter import BaseConverter
from ...modeling import QuizModel, QuestionModel, CompositeQuestionModel, OpenAnswerQuestionModel


def _is_composite(question_model: QuestionModel) -> bool:
    return isinstance(question_model, CompositeQuestionModel)


def _is_open_answer(question_model: QuestionModel) -> bool:
    return isinstance(question_model, OpenAnswerQuestionModel)


def _add_indentation(text: str, depth: int = 0) -> str:
    text_indented = ""
    for line in text.split("\n"):
        text_indented += "    " * depth + line + "\n"
    return text_indented


class HtmlConverter(BaseConverter):
    def as_practice_test(self, quiz_model: QuizModel) -> str:
        return _PracticeTestHtmlConverter().render(quiz_model)

    def as_notecards(self, quiz_model: QuizModel) -> str:
        return _NotecardsHtmlConverter().render(quiz_model)


class _PracticeTestHtmlConverter:
    @staticmethod
    def _render_style_template() -> str:
        env = Environment(loader=BaseLoader(), autoescape=False)

        template_string = """
    <style>
        body {
            font-family: Arial, sans-serif;
            font-size: 1.0em; 
        }
        .area { 
            margin: 0; 
        }
        .name { 
            font-weight: bold; 
            font-size: 1.5em; 
            margin: 0; 
        }
        .statement_0 { 
            font-weight: bold;
        }
        footer {
            font-size: 0.5em; 
            position: fixed; 
            bottom: 0;
        }
    </style>
""".strip()

        template = env.from_string(template_string)
        return template.render()

    @staticmethod
    def _render_header_template(quiz_area: str, quiz_name: str) -> str:
        env = Environment(loader=BaseLoader(), autoescape=False)

        template_string = """
        <p class="area">{{ quiz_area }}</p>
        <p class="name">{{ quiz_name }}</p>
""".strip()

        template = env.from_string(template_string)
        return template.render(
            quiz_area=quiz_area,
            quiz_name=quiz_name
        )

    @staticmethod
    def _render_main_template(questions: tuple[QuestionModel], depth: int = 0) -> str:
        env = Environment(loader=BaseLoader(), autoescape=False)
        env.filters["is_composite"] = _is_composite
        env.filters["is_open_answer"] = _is_open_answer

        statement_class = f"statement_{depth}"

        template_string = """
        {% for question in questions %}
        <div>
            <p class={{ statement_class }}>
                {{ question.statement }}
            </p>
            {%- if question|is_open_answer %}
            {%- elif question|is_composite -%}
            {{ main_template(question.sub_questions, depth+1) }}
            {%- endif %}
        </div>
        <br>
        {%- endfor %}
""".strip()

        template_string = _add_indentation(template_string, depth)
        template = env.from_string(template_string)
        return template.render(
            questions=questions,
            depth=depth,
            statement_class=statement_class,
            main_template=_PracticeTestHtmlConverter._render_main_template
        )

    @staticmethod
    def _render_footer_template() -> str:
        env = Environment(loader=BaseLoader(), autoescape=False)

        template_string = """
        <p>&copy; 2023 CramPy. All rights reserved.</p>
        """.strip()

        template = env.from_string(template_string)
        return template.render()

    def render(self, quiz_model: QuizModel) -> str:
        env = Environment(loader=BaseLoader(), autoescape=False)

        template_string = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Practice Test</title>
    {{ style_template }}
</head>
<body>
    <header>
        {{ header_template }}
    </header>
    <br>
    <main>{{ main_template }}
    </main>
    <br>
    <footer>{{ footer_template }}
    </footer>
</body>
</html>
""".strip()

        template = env.from_string(template_string)
        return template.render(
            style_template=self._render_style_template(),
            header_template=self._render_header_template(quiz_model.area, quiz_model.name),
            main_template=self._render_main_template(quiz_model.questions),
            footer_template=self._render_footer_template()
        )


class _NotecardsHtmlConverter:
    @staticmethod
    def _render_style_template() -> str:
        env = Environment(loader=BaseLoader(), autoescape=False)
        template_string = """
    <style>
        @page {
            margin: 10mm;
        }
        body {
            margin: 0;
            padding: 0;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
            font-family: Arial, sans-serif;
            font-size: 1.0em; 
        }
        .container {
            margin-top: 35px;
            display: flex;
            flex-wrap: wrap;
            justify-content: center;
            align-items: center;
            text-align: center;
            page-break-after: always;
        }
        .container:last-child {
            page-break-after: auto;
        }
        .notecard {
            width: 300px;
            height: 100px;
            border: 1px solid black;
            margin: 10px;
            display: flex;
            justify-content: center;
            align-items: center;
            text-align: center;
        }
        .hidden-notecard {
            width: 300px;
            height: 100px;
            margin: 10px;
            display: flex;
            justify-content: center;
            align-items: center;
            text-align: center;
        }
    </style>
""".strip()
        template = env.from_string(template_string)
        return template.render()

    @staticmethod
    def _render_main_template(questions: tuple[QuestionModel]) -> str:
        env = Environment(loader=BaseLoader(), autoescape=False)

        amount = len(questions)
        question_list: list[str | None] = []
        answer_list: list[str | None] = []

        for question in questions:
            question_list.append(question.statement)
            if isinstance(question, OpenAnswerQuestionModel):
                answer_list.append(question.expected_answer)

        # The list has to be a multiple of sixteen to fill the entire page to be aligned
        items_needed = (16 - (amount % 16)) % 16
        if items_needed > 0:
            question_list.extend([None] * items_needed)
            answer_list.extend([None] * items_needed)

        # Invert the answer list to when printing this keep the right align between question/answer
        inverted_answer_list: list[str | None] = []
        for i in range(0, len(answer_list), 2):
            if i + 1 < len(answer_list):
                inverted_answer_list.extend([answer_list[i + 1], answer_list[i]])

        template_string = """
        <div class="container">
        {%- for question in questions %}
            {%- if question is not none %}
            <div class="notecard">
                {{ question }}
            </div>
            {%- else %}
            <div class="hidden-notecard"></div>
            {%- endif %}
        {%- endfor %}
        </div>
        <div class="container">
        {%- for answer in answers %}
            {%- if answer is not none %}
            <div class="notecard">
                {{ answer }}
            </div>
            {%- else %}
            <div class="hidden-notecard"></div>
            {%- endif %}
        {%- endfor %}
        </div>
        """.strip()
        template = env.from_string(template_string)
        return template.render(
            questions=question_list,
            answers=inverted_answer_list
        )

    def render(self, quiz_model: QuizModel) -> str:
        env = Environment(loader=BaseLoader(), autoescape=False)
        template_string = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Notecards</title>
    {{ style_template }}
</head>
<body>
    <main>
        {{ main_template }}
    </main>
</body>
</html>
""".strip()
        template = env.from_string(template_string)
        return template.render(
            style_template=self._render_style_template(),
            main_template=self._render_main_template(quiz_model.questions)
        )
