"""The paths a project leaves out of the check."""

from collections.abc import Container
from dataclasses import dataclass
from fnmatch import fnmatch
from typing import final

from typing_extensions import override


@final
@dataclass(frozen=True, slots=True)
class Excludes(Container[str]):
    """Glob patterns and directories that a project leaves unchecked."""

    _patterns: tuple[str, ...]

    @override
    def __contains__(self, path: object) -> bool:
        """Tell whether a POSIX path, relative to the root, is left out."""
        return any(
            fnmatch(str(path), pattern)
            or str(path).startswith(pattern.rstrip("/") + "/")
            for pattern in self._patterns
        )
