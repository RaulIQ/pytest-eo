"""The suppressions that reach beyond their own line."""

import re
from collections.abc import Iterable, Iterator
from dataclasses import dataclass
from typing import final

from typing_extensions import override

from pytest_eo.comment import Comment
from pytest_eo.place import Place
from pytest_eo.violation import Violation

_SPREAD = r"ruff:\s*(?:noqa|file-ignore|disable)\b|flake8:\s*noqa\b|mypy:"
_WIDE = re.compile(rf"#\s*(?P<kind>{_SPREAD})")
_HEADER = re.compile(rf"#\s*(?P<kind>{_SPREAD}|type:\s*ignore\b(?!\[))")


@final
@dataclass(frozen=True, slots=True)
class WideSuppressions(Iterable[Violation]):
    """File-wide and range forms of ruff, flake8 and mypy in one comment.

    Above the first code a bare ``# type: ignore`` silences the whole file,
    so there it counts as one of them.
    """

    tool: str
    comment: Comment

    @override
    def __iter__(self) -> Iterator[Violation]:
        """Report every form of the comment that suppresses beyond its line."""
        line, column = self.comment.token.start
        return (
            Violation(
                self.tool,
                "SUP003",
                Place(str(self.comment.file), line, column + match.start() + 1),
                f"`# {match['kind']}` suppresses beyond its own line: "
                "suppress on that one line instead, with a reason",
            )
            for match in (_HEADER if self.comment.header else _WIDE).finditer(
                self.comment.token.string,
            )
        )
