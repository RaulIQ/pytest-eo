"""Python files that the gate reads itself."""

from pathlib import Path
from typing import Protocol


class Files(Protocol):
    """Python files of a project that the gate reads itself."""

    def files(self) -> tuple[Path, ...]:
        """Every file to read, in a stable order."""
        ...
