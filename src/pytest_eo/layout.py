"""Which directories of a project the gate checks, and how strictly."""

from typing import Protocol


class Layout(Protocol):
    """Which directories of a project to check, which to skip, and limits."""

    def paths(self) -> tuple[str, ...]:
        """Directories to check, relative to the project root."""
        ...

    def excludes(self) -> tuple[str, ...]:
        """Glob patterns to skip."""
        ...

    def depth(self) -> tuple[int, ...]:
        """How deep calls may nest, or nothing to keep the default."""
        ...
