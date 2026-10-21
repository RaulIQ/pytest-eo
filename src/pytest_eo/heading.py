"""A comment that stands above the first line of code."""

import re
from collections.abc import Iterator
from dataclasses import dataclass
from typing import final

from typing_extensions import override

from pytest_eo.place import Place
from pytest_eo.remark import Remark


@final
@dataclass(frozen=True, slots=True)
class Heading(Remark):
    """A comment above all code, where some forms reach the whole file."""

    _origin: Remark

    @override
    def matches(
        self,
        pattern: re.Pattern[str],
    ) -> Iterator[tuple[Place, re.Match[str]]]:
        """Yield the matches of the comment itself."""
        return self._origin.matches(pattern)

    @override
    def heading(
        self,
        pattern: re.Pattern[str],
    ) -> Iterator[tuple[Place, re.Match[str]]]:
        """Yield the same matches, since this comment heads the file."""
        return self._origin.matches(pattern)
