import unittest

from crampy.models import QuestionModel, OpenAnswerQuestionModel, CompositeQuestionModel


class TestQuestionModel(unittest.TestCase):
    def test_init_should_instantiate(self):
        statement = "Question statement"
        model = QuestionModel(statement)
        self.assertEqual(model.statement, statement)


class TestOpenAnswerQuestionModel(unittest.TestCase):
    def test_init_should_instantiate(self):
        statement = "Question statement"
        expected_answer = "Expected answer"

        model = OpenAnswerQuestionModel(statement, expected_answer)

        self.assertEqual(model.statement, statement)
        self.assertEqual(model.expected_answer, expected_answer)


class TestCompositeQuestionModel(unittest.TestCase):
    def test_init_should_instantiate(self):
        statement = "Question statement"
        sub_questions = [QuestionModel(""), QuestionModel("")]

        model = CompositeQuestionModel(statement, sub_questions)

        self.assertEqual(model.statement, statement)
        self.assertEqual(model.sub_questions, sub_questions)


if __name__ == "__main__":
    unittest.main()
