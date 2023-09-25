from io import StringIO
from pathlib import Path
from typing import Union, TextIO

from .type_checking import is_string, is_stringio, is_pathlike


Source = Union[Path, str, StringIO]


class SourceWriter:
    def __init__(self, source: Source):
        self._source: Source = source
        self._stream: TextIO | None = None

    def __enter__(self):
        path = self._get_path(self._source)
        if path:
            self._stream = open(path, "w", encoding="utf8")
        elif is_stringio(self._source):
            self._stream = self._source
        else:
            raise ValueError("Source writer failed: "
                             f"'{self._source}' is not a valid stream.")
        return self

    def __exit__(self, *exc_info):
        if self._stream is not None:
            self._stream.close()

    def write(self, content: str) -> None:
        if self._stream is not None:
            self._stream.write(content)

    @staticmethod
    def _get_path(source: Source) -> str | None:
        if is_pathlike(source) and not source.is_dir():
            return str(source)
        if is_string(source):
            path = Path(source)
            return str(source) if not path.is_dir() else None
        return None
