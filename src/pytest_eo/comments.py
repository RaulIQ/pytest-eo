"""The comments of a source file."""

import io
import tokenize
from collections.abc import Iterable, Iterator
from dataclasses import dataclass
from pathlib import Path
from typing import final

from typing_extensions import override

from pytest_eo.comment import Comment

_SILENT = (tokenize.COMMENT, tokenize.NL, tokenize.NEWLINE, tokenize.ENCODING)


@final
@dataclass(frozen=True, slots=True)
class Comments(Iterable[Comment]):
    """Every comment of a file, or none when the file cannot be tokenized."""

    _file: Path

    @override
    def __iter__(self) -> Iterator[Comment]:
        """Read the comments in order, telling the header from the rest."""
        text = self._file.read_text(encoding="utf-8")
        try:
            tokens = tuple(
                tokenize.generate_tokens(io.StringIO(text).readline),
            )
        except (tokenize.TokenError, SyntaxError):
            return
        code = next(
            token.start for token in tokens if token.type not in _SILENT
        )
        for token in tokens:
            if token.type == tokenize.COMMENT:
                yield Comment(self._file, token, header=token.start < code)
