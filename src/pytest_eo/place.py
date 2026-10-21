"""Where in the code a tool found something."""

from dataclasses import dataclass
from typing import final

from typing_extensions import override


@final
@dataclass(frozen=True, slots=True)
class Place:
    """A file, a line and a column, as tools and editors point at code."""

    _path: str
    _line: int
    _column: int

    @override
    def __str__(self) -> str:
        """Render as ``path:line:col``."""
        return f"{self._path}:{self._line}:{self._column}"
