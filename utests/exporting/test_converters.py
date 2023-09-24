import unittest

from crampy.exporting import QuizHtmlConverter
from crampy.models import QuizModel, OpenAnswerQuestionModel, MultipleChoiceQuestionModel, CompositeQuestionModel


class TestQuizHtmlConverter(unittest.TestCase):
    def test_as_practice_test_when_have_no_questions_then_should_return_content(self):
        converter = QuizHtmlConverter()
        questions = []
        quiz_model = QuizModel("Quiz Name", "Quiz Area", questions)

        content = converter.as_practice_test(quiz_model)

        self.assertIn(f"""<!DOCTYPE html>""", content)
        self.assertIn(f"""<meta name="description" content="Practice Test">""", content)
        self.assertIn(f"""<title>{quiz_model.name}</title>""", content)
        self.assertIn(f"""<p class="quiz-area">{quiz_model.area}</p>""", content)
        self.assertIn(f"""<p class="quiz-name">{quiz_model.name}</p>""", content)

    def test_as_practice_test_when_have_open_answer_questions_then_should_return_content(self):
        converter = QuizHtmlConverter()
        questions = [
            OpenAnswerQuestionModel("Statement 1", "Expected answer 1"),
            OpenAnswerQuestionModel("Statement 2", "Expected answer 2")
        ]
        quiz_model = QuizModel("Quiz Name", "Quiz Area", questions)

        content = converter.as_practice_test(quiz_model)

        self.assertIn(f"""<!DOCTYPE html>""", content)
        self.assertIn(f"""<meta name="description" content="Practice Test">""", content)
        self.assertIn(f"""<title>{quiz_model.name}</title>""", content)
        self.assertIn(f"""<p class="quiz-area">{quiz_model.area}</p>""", content)
        self.assertIn(f"""<p class="quiz-name">{quiz_model.name}</p>""", content)
        for question in questions:
            self.assertIn(f"""<p class="question-statement">{question.statement}</p>""", content)

    def test_as_practice_test_when_have_multiple_choice_questions_then_should_return_content(self):
        converter = QuizHtmlConverter()
        questions = [
            MultipleChoiceQuestionModel("Statement 1", ["Choice 1", "Choice 2"], 1),
            MultipleChoiceQuestionModel("Statement 2", ["Choice A", "Choice B"], 2)
        ]
        quiz_model = QuizModel("Quiz Name", "Quiz Area", questions)

        content = converter.as_practice_test(quiz_model)

        self.assertIn(f"""<!DOCTYPE html>""", content)
        self.assertIn(f"""<meta name="description" content="Practice Test">""", content)
        self.assertIn(f"""<title>{quiz_model.name}</title>""", content)
        self.assertIn(f"""<p class="quiz-area">{quiz_model.area}</p>""", content)
        self.assertIn(f"""<p class="quiz-name">{quiz_model.name}</p>""", content)
        for question in questions:
            self.assertIn(f"""<p class="question-statement">{question.statement}</p>""", content)
            for choice in question.choices:
                self.assertIn(f"""<li class="question-choice">{choice}</li>""", content)

    def test_as_practice_test_when_have_composite_questions_then_should_return_content(self):
        converter = QuizHtmlConverter()
        questions = [
            CompositeQuestionModel("Resolve below", [
                OpenAnswerQuestionModel("Sub Statement 1", "Sub Expected answer 1"),
                MultipleChoiceQuestionModel("Sub Statement 2",
                                            ["Sub Choice A", "Sub Choice B"], 2)
            ])
        ]
        quiz_model = QuizModel("Quiz Name", "Quiz Area", questions)

        content = converter.as_practice_test(quiz_model)

        self.assertIn(f"""<!DOCTYPE html>""", content)
        self.assertIn(f"""<meta name="description" content="Practice Test">""", content)
        self.assertIn(f"""<title>{quiz_model.name}</title>""", content)
        self.assertIn(f"""<p class="quiz-area">{quiz_model.area}</p>""", content)
        self.assertIn(f"""<p class="quiz-name">{quiz_model.name}</p>""", content)
        for question in questions:
            self.assertIn(f"""<p class="question-statement">{question.statement}</p>""", content)
            for subquestion in question.sub_questions:
                self.assertIn(f"""<p class="question-statement">{subquestion.statement}</p>""", content)
                if isinstance(subquestion, MultipleChoiceQuestionModel):
                    for choice in subquestion.choices:
                        self.assertIn(f"""<li class="question-choice">{choice}</li>""", content)

    def test_as_practice_test_when_have_all_question_types_then_should_return_content(self):
        converter = QuizHtmlConverter()
        questions = [
            OpenAnswerQuestionModel("Statement 1", "Expected answer 1"),
            MultipleChoiceQuestionModel("Statement 2", ["Choice A", "Choice B"], 2),
            CompositeQuestionModel("Resolve below", [
                OpenAnswerQuestionModel("Sub Statement 1", "Sub Expected answer 1"),
                MultipleChoiceQuestionModel("Sub Statement 2",
                                            ["Sub Choice A", "Sub Choice B"], 2)
            ])
        ]
        quiz_model = QuizModel("Quiz Name", "Quiz Area", questions)

        content = converter.as_practice_test(quiz_model)

        self.assertIn(f"""<!DOCTYPE html>""", content)
        self.assertIn(f"""<meta name="description" content="Practice Test">""", content)
        self.assertIn(f"""<title>{quiz_model.name}</title>""", content)
        self.assertIn(f"""<p class="quiz-area">{quiz_model.area}</p>""", content)
        self.assertIn(f"""<p class="quiz-name">{quiz_model.name}</p>""", content)
        for question in questions:
            self.assertIn(f"""<p class="question-statement">{question.statement}</p>""", content)
            if isinstance(question, MultipleChoiceQuestionModel):
                for choice in question.choices:
                    self.assertIn(f"""<li class="question-choice">{choice}</li>""", content)
            elif isinstance(question, CompositeQuestionModel):
                for subquestion in question.sub_questions:
                    self.assertIn(f"""<p class="question-statement">{subquestion.statement}</p>""", content)
                    if isinstance(subquestion, MultipleChoiceQuestionModel):
                        for choice in subquestion.choices:
                            self.assertIn(f"""<li class="question-choice">{choice}</li>""", content)

    def test_as_notecards_when_have_no_questions_then_should_return_content(self):
        converter = QuizHtmlConverter()
        questions = []
        quiz_model = QuizModel("Quiz Name", "Quiz Area", questions)

        content = converter.as_notecards(quiz_model)

        self.assertIn(f"""<!DOCTYPE html>""", content)
        self.assertIn(f"""<meta name="description" content="Notecards">""", content)
        self.assertIn(f"""<title>{quiz_model.name}</title>""", content)

    def test_as_notecards_when_have_open_answer_questions_then_should_return_content(self):
        converter = QuizHtmlConverter()
        questions = [
            OpenAnswerQuestionModel("Statement 1", "Expected answer 1"),
            OpenAnswerQuestionModel("Statement 2", "Expected answer 2")
        ]
        quiz_model = QuizModel("Quiz Name", "Quiz Area", questions)

        content = converter.as_notecards(quiz_model)

        self.assertIn(f"""<!DOCTYPE html>""", content)
        self.assertIn(f"""<meta name="description" content="Notecards">""", content)
        self.assertIn(f"""<title>{quiz_model.name}</title>""", content)
        for question in questions:
            self.assertIn(f"""<div class="question-statement">{question.statement}</div>""", content)
            self.assertIn(f"""<div>{question.expected_answer}</div>""", content)

    def test_as_notecards_when_have_multiple_choice_questions_then_should_return_content(self):
        converter = QuizHtmlConverter()
        questions = [
            MultipleChoiceQuestionModel("Statement 1", ["Choice 1", "Choice 2"], 1),
            MultipleChoiceQuestionModel("Statement 2", ["Choice A", "Choice B"], 2)
        ]
        quiz_model = QuizModel("Quiz Name", "Quiz Area", questions)

        content = converter.as_notecards(quiz_model)

        self.assertIn(f"""<!DOCTYPE html>""", content)
        self.assertIn(f"""<meta name="description" content="Notecards">""", content)
        self.assertIn(f"""<title>{quiz_model.name}</title>""", content)
        for question in questions:
            self.assertIn(f"""<div class="question-statement">{question.statement}</div>""", content)
            self.assertIn(f"""<div>{question.answer}</div>""", content)

    def test_as_notecards_when_have_composite_questions_then_should_ignore(self):
        converter = QuizHtmlConverter()
        questions = [
            CompositeQuestionModel("Resolve below", [
                OpenAnswerQuestionModel("Sub Statement 1", "Sub Expected answer 1"),
                MultipleChoiceQuestionModel("Sub Statement 2",
                                            ["Sub Choice A", "Sub Choice B"], 2)
            ])
        ]
        quiz_model = QuizModel("Quiz Name", "Quiz Area", questions)

        content = converter.as_notecards(quiz_model)

        self.assertIn(f"""<!DOCTYPE html>""", content)
        self.assertIn(f"""<meta name="description" content="Notecards">""", content)
        self.assertIn(f"""<title>{quiz_model.name}</title>""", content)
        self.assertNotIn(f"""<div class="question-statement>""", content)

    def test_as_notecards_when_have_all_question_types_then_should_return_content(self):
        converter = QuizHtmlConverter()
        questions = [
            OpenAnswerQuestionModel("Statement 1", "Expected answer 1"),
            MultipleChoiceQuestionModel("Statement 2", ["Choice A", "Choice B"], 2)
        ]
        quiz_model = QuizModel("Quiz Name", "Quiz Area", questions)

        content = converter.as_notecards(quiz_model)

        self.assertIn(f"""<!DOCTYPE html>""", content)
        self.assertIn(f"""<meta name="description" content="Notecards">""", content)
        self.assertIn(f"""<title>{quiz_model.name}</title>""", content)
        for question in questions:
            self.assertIn(f"""<div class="question-statement">{question.statement}</div>""", content)
            if isinstance(question, OpenAnswerQuestionModel):
                self.assertIn(f"""<div>{question.expected_answer}</div>""", content)
            elif isinstance(question, MultipleChoiceQuestionModel):
                self.assertIn(f"""<div>{question.answer}</div>""", content)


if __name__ == "__main__":
    unittest.main()
