"""One aggregated tool: a named source of violations."""

from typing import Protocol

from pytest_eo.violation import Violation


class Check(Protocol):
    """A named source of violations."""

    def name(self) -> str:
        """Short name shown in the pytest report."""
        ...

    def violations(self) -> tuple[Violation, ...]:
        """Run the tool and return everything it complains about."""
        ...
