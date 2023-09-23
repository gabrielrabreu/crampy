from io import StringIO
from pathlib import Path
from typing import Union, TextIO

from .type_checking import is_string, is_stringio, is_pathlike


Source = Union[Path, str, StringIO]


class SourceWriter:
    def __init__(self, source: Source):
        self._stream = self._get_stream(source)

    def _get_stream(self, source: Source) -> TextIO:
        path = self._get_path(source)
        if path:
            stream = open(path, "w")
        elif is_stringio(source):
            stream = source
        else:
            raise ValueError("Source writer failed: "
                             f"'{source}' is not a valid stream.")
        return stream

    @staticmethod
    def _get_path(source: Source) -> str | None:
        if is_pathlike(source) and not source.is_dir():
            return str(source)
        if is_string(source):
            path = Path(source)
            return str(source) if not path.is_dir() else None
        return None

    def write(self, content: str) -> None:
        self._stream.write(content)

    def __enter__(self):
        return self

    def __exit__(self, *exc_info):
        self._stream.close()
