import unittest

from crampy.modeling import QuizModel, QuestionModel, OpenAnswerQuestionModel, CompositeQuestionModel


class TestQuizModel(unittest.TestCase):
    def test_init_should_instantiate(self):
        name = "Name"
        area = "Area"

        model = QuizModel(name, area)

        self.assertEqual(model.name, name)
        self.assertEqual(model.area, area)
        self.assertEqual(len(model.questions), 0)

    def test_add_question_should_add_to_list(self):
        model = QuizModel("Name", "Area")

        question1 = QuestionModel("Statement 1")
        model.add_question(question1)

        question2 = OpenAnswerQuestionModel("Statement 2", "Answer 2")
        model.add_question(question2)

        question3 = CompositeQuestionModel("Statement 3")
        model.add_question(question3)

        self.assertEqual(len(model.questions), 3)
        self.assertIn(question1, model.questions)
        self.assertIn(question2, model.questions)
        self.assertIn(question3, model.questions)


if __name__ == "__main__":
    unittest.main()
