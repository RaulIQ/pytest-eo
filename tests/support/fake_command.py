"""A command that prints what it was told to, without running anything."""

from dataclasses import dataclass
from typing import final

from typing_extensions import override

from pytest_eo.command import Command
from pytest_eo.output import Output


@final
@dataclass(frozen=True, slots=True)
class FakeCommand(Command):
    """A command that prints what it was told to, without running anything."""

    _output: Output

    @override
    def run(self) -> Output:
        """Return the canned output."""
        return self._output
