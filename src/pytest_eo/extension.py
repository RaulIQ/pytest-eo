"""A flake8 plugin, as this package sees one."""

from collections.abc import Iterator
from typing import Protocol


class Extension(Protocol):
    """A flake8 plugin: the problems of one parsed file."""

    def run(self) -> Iterator[tuple[int, int, str, type[object]]]:
        """Yield the line, column, message and plugin of every problem."""
        ...
