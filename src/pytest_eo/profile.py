"""A set of checks to run over a project."""

from typing import Protocol

from pytest_eo.check import Check


class Profile(Protocol):
    """A set of checks to run over a project."""

    def checks(self) -> tuple[Check, ...]:
        """Build the checks; nothing runs until ``violations()`` is called."""
        ...
