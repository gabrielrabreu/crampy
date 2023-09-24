import unittest

from crampy.models import QuizModel, QuestionModel


class TestQuizModel(unittest.TestCase):
    def test_when_init_then_should_instantiate(self):
        name = "Quiz name"
        area = "Quiz area"
        questions = [QuestionModel(""), QuestionModel("")]

        model = QuizModel(name, area, questions)

        self.assertEqual(model.name, name)
        self.assertEqual(model.area, area)
        self.assertEqual(model.questions, questions)


if __name__ == "__main__":
    unittest.main()
