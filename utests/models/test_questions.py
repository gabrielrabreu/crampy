import unittest

from crampy.modeling import QuestionModel, OpenAnswerQuestionModel, CompositeQuestionModel


class TestQuestionModel(unittest.TestCase):
    def test_init_should_instantiate(self):
        statement = "Statement"
        model = QuestionModel(statement)
        self.assertEqual(model.statement, statement)


class TestOpenAnswerQuestionModel(unittest.TestCase):
    def test_init_should_instantiate(self):
        statement = "Statement"
        expected_answer = "Answer"

        model = OpenAnswerQuestionModel(statement, expected_answer)

        self.assertEqual(model.statement, statement)
        self.assertEqual(model.expected_answer, expected_answer)


class TestCompositeQuestionModel(unittest.TestCase):
    def test_init_should_instantiate(self):
        statement = "Statement"

        model = CompositeQuestionModel(statement)

        self.assertEqual(model.statement, statement)
        self.assertEqual(len(model.sub_questions), 0)

    def test_add_sub_question_should_add_to_list(self):
        statement = "Statement"
        model = CompositeQuestionModel(statement)

        sub_question1 = QuestionModel("Sub Statement 1")
        model.add_sub_question(sub_question1)
        sub_question2 = OpenAnswerQuestionModel("Sub Statement 2", "Sub Answer 2")
        model.add_sub_question(sub_question2)

        self.assertEqual(len(model.sub_questions), 2)
        self.assertIn(sub_question1, model.sub_questions)
        self.assertIn(sub_question2, model.sub_questions)

    def test_add_sub_question_when_composite_then_should_raise_value_error(self):
        statement = "Statement"
        model = CompositeQuestionModel(statement)

        with self.assertRaises(ValueError) as context:
            model.add_sub_question(CompositeQuestionModel("Sub Statement 1"))
        self.assertEqual(str(context.exception), "Can't add a sub question of Composite type.")


if __name__ == "__main__":
    unittest.main()
