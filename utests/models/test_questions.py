import unittest

from crampy.models import QuestionModel, MultipleChoiceQuestionModel, OpenAnswerQuestionModel, CompositeQuestionModel


class TestQuestionModel(unittest.TestCase):
    def test_init_should_instantiate(self):
        statement = "Question statement"
        model = QuestionModel(statement)
        self.assertEqual(model.statement, statement)


class TestMultipleChoiceQuestionModel(unittest.TestCase):
    def test_init_should_instantiate(self):
        statement = "Question statement"
        choices = ["Choice 1", "Choice 2", "Choice 3", "Choice 4"]
        correct_option = 4

        model = MultipleChoiceQuestionModel(statement, choices, correct_option)

        self.assertEqual(model.statement, statement)
        self.assertEqual(model.choices, choices)
        self.assertEqual(model.answer, choices[correct_option - 1])

    def test_init_when_correct_option_out_of_bounds_then_should_raise_index_error(self):
        statement = "Question statement"
        choices = ["Choice 1", "Choice 2", "Choice 3", "Choice 4"]

        with self.assertRaises(IndexError) as context:
            MultipleChoiceQuestionModel(statement, choices, 0)
        self.assertEqual(str(context.exception), f"The correct option '0' is out of bounds "
                                                 f"for the choices of length '4'.")

        with self.assertRaises(IndexError) as context:
            MultipleChoiceQuestionModel(statement, choices, 5)
        self.assertEqual(str(context.exception), f"The correct option '5' is out of bounds "
                                                 f"for the choices of length '4'.")


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
