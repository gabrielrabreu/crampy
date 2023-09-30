import os
import tempfile
import unittest
from pathlib import Path

from crampy.converting import QuizExporter, QuizHtmlConverter
from crampy.modeling import QuizModel


TEMPDIR = os.getenv("TEMPDIR") or tempfile.gettempdir()
PATH = os.path.join(TEMPDIR, "exporters.test")


class TestQuizExporter(unittest.TestCase):
    def test_init_should_instantiate(self):
        exporter = QuizExporter()

        self.assertEqual(len(exporter._standard_converters), 1)
        self.assertIn("html", exporter._standard_converters)
        self.assertEqual(exporter._standard_converters["html"], QuizHtmlConverter)

    def test_as_practice_test_when_code_is_html_then_should_write_to_file(self):
        exporter = QuizExporter()
        quiz_model = QuizModel("Name", "Area")
        code = "html"
        source = Path(PATH)

        exporter.as_practice_test(quiz_model, code, source)

        with open(source, "r") as reader:
            content = reader.read()
            self.assertIn(f"""<!DOCTYPE html>""", content)
            self.assertIn(f"""<title>Practice Test</title>""", content)

    def test_as_practice_test_when_code_not_found_then_should_raise_value_error(self):
        exporter = QuizExporter()
        quiz_model = QuizModel("Name", "Area")
        code = "dontexists"
        source = Path(PATH)

        with self.assertRaises(ValueError) as context:
            exporter.as_practice_test(quiz_model, code, source)
        self.assertEqual(str(context.exception), f"Exporting failed: Converter '{code}' does not exist.")

    def test_as_notecards_when_code_is_html_then_should_write_to_file(self):
        exporter = QuizExporter()
        quiz_model = QuizModel("Name", "Area")
        code = "html"
        source = Path(PATH)

        exporter.as_notecards(quiz_model, code, source)

        with open(source, "r") as reader:
            content = reader.read()
            self.assertIn(f"""<!DOCTYPE html>""", content)
            self.assertIn(f"""<title>Notecards</title>""", content)

    def test_as_notecards_when_code_not_found_then_should_raise_value_error(self):
        exporter = QuizExporter()
        quiz_model = QuizModel("Name", "Area")
        code = "dontexists"
        source = Path(PATH)

        with self.assertRaises(ValueError) as context:
            exporter.as_notecards(quiz_model, code, source)
        self.assertEqual(str(context.exception), f"Exporting failed: Converter '{code}' does not exist.")


if __name__ == "__main__":
    unittest.main()
