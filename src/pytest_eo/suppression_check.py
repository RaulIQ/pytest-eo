"""Suppression comments: each one gives a reason, and some codes allow none."""

from dataclasses import dataclass
from typing import final

from typing_extensions import override

from pytest_eo.check import Check
from pytest_eo.comments import Comments
from pytest_eo.files import Files
from pytest_eo.narrow_suppressions import NarrowSuppressions
from pytest_eo.violation import Violation
from pytest_eo.wide_suppressions import WideSuppressions


@final
@dataclass(frozen=True, slots=True)
class SuppressionCheck(Check):
    """Suppressions without a reason, of a forbidden rule, or wider than a line.

    It reads ``# noqa: CODE`` and ``# ruff: ignore[CODE-OR-NAME]``, and
    refuses the file-wide and range forms of ruff, flake8 and mypy outright.
    """

    sources: Files
    forbidden: tuple[str, ...]

    @property
    @override
    def name(self) -> str:
        """Short name shown in the pytest report."""
        return "suppressions"

    @override
    def violations(self) -> tuple[Violation, ...]:
        """Read the comments of every file, never running a tool."""
        return tuple(
            found
            for file in self.sources.files()
            for comment in Comments(file)
            for found in (
                *NarrowSuppressions(self.name, comment, self.forbidden),
                *WideSuppressions(self.name, comment),
            )
        )
