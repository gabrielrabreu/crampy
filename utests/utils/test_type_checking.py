import unittest
from io import StringIO
from pathlib import Path

from crampy.utils import is_pathlike, is_stringio, is_string


class TestIsString(unittest.TestCase):
    def test_is_string_when_value_is_string_then_should_return_true(self):
        self.assertTrue(is_string("string"))
        self.assertTrue(is_string(""))


class TestIsStringIO(unittest.TestCase):
    def test_is_stringio_when_value_is_stringio_should_return_true(self):
        self.assertTrue(is_stringio(StringIO()))


class TestIsPathLike(unittest.TestCase):
    def test_is_pathlike_when_value_is_pathlike_should_return_true(self):
        self.assertTrue(is_pathlike(Path()))


if __name__ == "__main__":
    unittest.main()
