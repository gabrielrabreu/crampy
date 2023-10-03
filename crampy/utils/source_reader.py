from pathlib import Path
from typing import TextIO

from .custom_types import Source
from .type_checking import is_string, is_stringio, is_pathlike


class SourceReader:
    def __init__(self, source: Source):
        self._source: Source = source
        self._stream: TextIO | None = None

    def __enter__(self):
        path = self._get_path(self._source)
        if path:
            self._stream = open(path, "r", encoding="utf8")
        elif is_stringio(self._source):
            self._stream = self._source
        else:
            raise ValueError("Source reader failed: "
                             f"'{self._source}' is not a valid stream.")
        return self

    def __exit__(self, *exc_info):
        self._stream.close()

    def read(self) -> str:
        return self._stream.read()

    @staticmethod
    def _get_path(source: Source) -> str | None:
        if is_pathlike(source) and not source.is_dir():
            return str(source)
        if is_string(source):
            path = Path(source)
            return str(source) if not path.is_dir() else None
        return None
