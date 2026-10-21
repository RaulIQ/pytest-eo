"""A comment of a source file, as the suppression checks see one."""

import re
from collections.abc import Iterator
from typing import Protocol

from pytest_eo.place import Place


class Remark(Protocol):
    """A comment that finds patterns in its own text."""

    def matches(
        self,
        pattern: re.Pattern[str],
    ) -> Iterator[tuple[Place, re.Match[str]]]:
        """Yield every match of the pattern, with where it stands."""
        ...

    def heading(
        self,
        pattern: re.Pattern[str],
    ) -> Iterator[tuple[Place, re.Match[str]]]:
        """Yield the matches only when the comment stands above all code."""
        ...
