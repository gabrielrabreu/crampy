import os
import tempfile
import unittest
from io import StringIO
from pathlib import Path

from crampy.utils import SourceReader


TEMPDIR = os.getenv("TEMPDIR") or tempfile.gettempdir()
PATH = os.path.join(TEMPDIR, "source_reader.test")
RANDOM_CONTENT = "Random text\nAnother random text"


class TestSourceReader(unittest.TestCase):
    def setUp(self) -> None:
        with open(PATH, "w") as file:
            file.write(RANDOM_CONTENT)

    def test_init_when_source_is_path_to_file_then_should_instantiate(self):
        source = Path(PATH)
        with SourceReader(source) as reader:
            self.assertEqual(reader._stream.mode, "r")
            self.assertEqual(reader._stream.name, PATH)
        self.assertTrue(reader._stream.closed)

    def test_init_when_source_is_string_path_to_file_then_should_instantiate(self):
        source = PATH
        with SourceReader(source) as reader:
            self.assertEqual(reader._stream.mode, "r")
            self.assertEqual(reader._stream.name, PATH)
        self.assertTrue(reader._stream.closed)

    def test_init_when_source_is_stringio_then_should_instantiate(self):
        source = StringIO()
        with SourceReader(source) as reader:
            self.assertEqual(reader._stream, source)
        self.assertTrue(reader._stream.closed)

    def test_init_when_source_is_path_to_dir_then_should_raise_value_error(self):
        source = Path(TEMPDIR)
        with self.assertRaises(ValueError) as context:
            with SourceReader(source):
                pass
        self.assertEqual(str(context.exception), f"Source reader failed: '{TEMPDIR}' is not a valid stream.")

    def test_init_when_source_is_string_path_to_dir_then_should_raise_value_error(self):
        source = TEMPDIR
        with self.assertRaises(ValueError) as context:
            with SourceReader(source):
                pass
        self.assertEqual(str(context.exception), f"Source reader failed: '{TEMPDIR}' is not a valid stream.")

    def test_read_when_source_is_path_then_should_read_stream(self):
        source = Path(PATH)
        with SourceReader(source) as reader:
            content = reader.read()

        self.assertTrue(reader._stream.closed)
        self.assertEqual(content, RANDOM_CONTENT)

    def test_read_when_source_is_stringio_then_should_read_stream(self):
        source = StringIO(RANDOM_CONTENT)
        with SourceReader(source) as reader:
            content = reader.read()
        self.assertTrue(reader._stream.closed)
        self.assertEqual(content, RANDOM_CONTENT)

    def tearDown(self) -> None:
        os.remove(PATH)


if __name__ == "__main__":
    unittest.main()
