"""A command that prints what it was told to, without running anything."""

from dataclasses import dataclass
from typing import final

from typing_extensions import override

from pytest_eo.command import Command
from pytest_eo.printout import Printout


@final
@dataclass(frozen=True, slots=True)
class FakeCommand(Command):
    """A command that prints what it was told to, without running anything."""

    _output: Printout

    @override
    def run(self) -> Printout:
        """Return the canned output."""
        return self._output
