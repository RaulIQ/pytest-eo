"""The suppressions that reach beyond their own line."""

import re
from collections.abc import Iterable, Iterator
from dataclasses import dataclass
from typing import final

from typing_extensions import override

from pytest_eo.remark import Remark
from pytest_eo.violation import Violation

_SPREAD = r"ruff:\s*(?:noqa|file-ignore|disable)\b|flake8:\s*noqa\b|mypy:"
_WIDE = re.compile(rf"#\s*(?P<kind>{_SPREAD})")
_BARE = re.compile(r"#\s*(?P<kind>type:\s*ignore\b(?!\[))")


@final
@dataclass(frozen=True, slots=True)
class WideSuppressions(Iterable[Violation]):
    """File-wide and range forms of ruff, flake8 and mypy in one comment.

    Above the first code a bare ``# type: ignore`` silences the whole file,
    so there it counts as one of them.
    """

    _tool: str
    _comment: Remark

    @override
    def __iter__(self) -> Iterator[Violation]:
        """Report every form of the comment that suppresses beyond its line."""
        return (
            Violation(
                self._tool,
                "SUP003",
                place,
                f"`# {match['kind']}` suppresses beyond its own line: "
                "suppress on that one line instead, with a reason",
            )
            for place, match in (
                *self._comment.matches(_WIDE),
                *self._comment.heading(_BARE),
            )
        )
