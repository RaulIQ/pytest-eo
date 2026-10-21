"""What a finished tool printed and how it exited."""

from collections.abc import Iterator
from dataclasses import dataclass
from typing import final

from typing_extensions import override

from pytest_eo.printout import Printout
from pytest_eo.tool_failed_error import ToolFailedError


@final
@dataclass(frozen=True, slots=True)
class Output(Printout):
    """The streams and the exit status of a finished process."""

    _stdout: str
    _stderr: str
    _status: int

    @override
    def __iter__(self) -> Iterator[str]:
        """Read the lines of stdout, where tools print their reports."""
        return iter(self._stdout.splitlines())

    @override
    def exited(self, statuses: tuple[int, ...]) -> bool:
        """Tell whether the process exited with one of the statuses."""
        return self._status in statuses

    @override
    def failure(self, reason: str) -> ToolFailedError:
        """Build the error with the exit status and what went to stderr."""
        return ToolFailedError(
            f"{reason} (status {self._status}): {self._stderr.strip()}",
        )
