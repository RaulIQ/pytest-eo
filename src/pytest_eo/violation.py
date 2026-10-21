"""A single style violation reported by one of the aggregated tools."""

from dataclasses import dataclass
from typing import final

from typing_extensions import override

from pytest_eo.place import Place


@final
@dataclass(frozen=True, slots=True)
class Violation:
    """What is wrong, where, and which tool says so."""

    _tool: str
    _code: str
    _place: Place
    _message: str

    @override
    def __str__(self) -> str:
        """Render as ``path:line:col: [tool:code] message``."""
        return f"{self._place}: [{self._tool}:{self._code}] {self._message}"
