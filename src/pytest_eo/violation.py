"""A single style violation reported by one of the aggregated tools."""

from dataclasses import dataclass
from typing import final


@final
@dataclass(frozen=True, slots=True)
class Violation:
    """What is wrong, where, and which tool says so."""

    tool: str
    code: str
    path: str
    line: int
    column: int
    message: str

    def __str__(self) -> str:
        """Render as ``path:line:col: [tool:code] message``."""
        place = f"{self.path}:{self.line}:{self.column}"
        return f"{place}: [{self.tool}:{self.code}] {self.message}"
