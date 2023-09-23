import os
import tempfile
import unittest
from io import StringIO
from pathlib import Path

from crampy.utils import SourceWriter


TEMPDIR = os.getenv("TEMPDIR") or tempfile.gettempdir()
PATH = os.path.join(TEMPDIR, "source_writer.test")
RANDOM_CONTENT = "Random text\nAnother random text"


class TestSourceWriter(unittest.TestCase):
    def test_init_when_source_is_path_to_file_then_should_instantiate(self):
        source = Path(PATH)
        with SourceWriter(source) as writer:
            self.assertEqual(writer._stream.mode, "w")
            self.assertEqual(writer._stream.name, PATH)
        self.assertTrue(writer._stream.closed)

    def test_init_when_source_is_string_path_to_file_then_should_instantiate(self):
        source = PATH
        with SourceWriter(source) as writer:
            self.assertEqual(writer._stream.mode, "w")
            self.assertEqual(writer._stream.name, PATH)
        self.assertTrue(writer._stream.closed)

    def test_init_when_source_is_stringio_then_should_instantiate(self):
        source = StringIO()
        with SourceWriter(source) as writer:
            self.assertEqual(writer._stream, source)
        self.assertTrue(writer._stream.closed)

    def test_init_when_source_is_path_to_dir_then_should_raise_value_error(self):
        source = Path(TEMPDIR)
        with self.assertRaises(ValueError) as context:
            with SourceWriter(source):
                pass
        self.assertEqual(str(context.exception), f"Source writer failed: '{TEMPDIR}' is not a valid stream.")

    def test_init_when_source_is_string_path_to_dir_then_should_raise_value_error(self):
        source = TEMPDIR
        with self.assertRaises(ValueError) as context:
            with SourceWriter(source):
                pass
        self.assertEqual(str(context.exception), f"Source writer failed: '{TEMPDIR}' is not a valid stream.")

    def test_write_when_source_is_path_then_should_write_to_stream(self):
        source = Path(PATH)
        with SourceWriter(source) as writer:
            writer.write(RANDOM_CONTENT)

        self.assertTrue(writer._stream.closed)
        with open(source, "r") as reader:
            self.assertEqual(reader.read(), RANDOM_CONTENT)

    def test_write_when_source_is_stringio_then_should_write_to_stream(self):
        source = StringIO()
        with SourceWriter(source) as writer:
            writer.write(RANDOM_CONTENT)
            content = writer._stream.getvalue()
        self.assertTrue(writer._stream.closed)

        with StringIO(content) as reader:
            self.assertEqual(reader.read(), RANDOM_CONTENT)


if __name__ == "__main__":
    unittest.main()
