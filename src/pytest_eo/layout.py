"""Which directories of a project the gate checks."""

from typing import Protocol


class Layout(Protocol):
    """Which directories of a project to check and which to skip."""

    def paths(self) -> tuple[str, ...]:
        """Directories to check, relative to the project root."""
        ...

    def excludes(self) -> tuple[str, ...]:
        """Glob patterns to skip."""
        ...
