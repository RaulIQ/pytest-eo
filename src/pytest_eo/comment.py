"""One comment of a source file."""

import re
import tokenize
from collections.abc import Iterator
from dataclasses import dataclass
from pathlib import Path
from typing import final

from typing_extensions import override

from pytest_eo.place import Place
from pytest_eo.remark import Remark


@final
@dataclass(frozen=True, slots=True)
class Comment(Remark):
    """A comment of a file, read as the tokenizer gives it."""

    _file: Path
    _token: tokenize.TokenInfo

    @override
    def matches(
        self,
        pattern: re.Pattern[str],
    ) -> Iterator[tuple[Place, re.Match[str]]]:
        """Yield every match of the pattern, with its line and column."""
        line, column = self._token.start
        return (
            (Place(str(self._file), line, column + match.start() + 1), match)
            for match in pattern.finditer(self._token.string)
        )

    @override
    def heading(
        self,
        pattern: re.Pattern[str],
    ) -> Iterator[tuple[Place, re.Match[str]]]:
        """Yield nothing, since a plain comment stands among the code."""
        return iter(())
