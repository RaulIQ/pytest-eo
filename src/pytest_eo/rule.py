"""A rule of Angry Tests, as this package sees one."""

from collections.abc import Iterator
from typing import Protocol


class Rule(Protocol):
    """One rule of Angry Tests over a parsed test module."""

    def problems(self) -> Iterator[tuple[int, int, str]]:
        """Yield the line, column and message of every break of the rule."""
        ...
