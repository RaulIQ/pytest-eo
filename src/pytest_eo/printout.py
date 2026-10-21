"""What a finished tool left behind, as the checks see it."""

from collections.abc import Iterable
from typing import Protocol

from pytest_eo.tool_failed_error import ToolFailedError


class Printout(Iterable[str], Protocol):
    """The lines a finished tool printed, and how it exited."""

    def exited(self, statuses: tuple[int, ...]) -> bool:
        """Tell whether the tool exited with one of the statuses."""
        ...

    def failure(self, reason: str) -> ToolFailedError:
        """Build the error of a tool that failed, with what it complained."""
        ...
