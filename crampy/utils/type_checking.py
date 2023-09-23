from io import StringIO
from os import PathLike
from typing import Any


def is_pathlike(item: Any) -> bool:
    return isinstance(item, PathLike)


def is_string(item: Any) -> bool:
    return isinstance(item, str)


def is_stringio(item: Any) -> bool:
    return isinstance(item, StringIO)
