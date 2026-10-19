"""Fakes: real implementations of the interfaces, with canned behaviour."""

from dataclasses import dataclass
from pathlib import Path
from typing import final

from typing_extensions import override

from pytest_eo.command import Command, Output
from pytest_eo.project import Files


@final
@dataclass(frozen=True, slots=True)
class FakeCommand(Command):
    """A command that prints what it was told to, without running anything."""

    output: Output

    @override
    def run(self) -> Output:
        """Return the canned output."""
        return self.output


@final
@dataclass(frozen=True, slots=True)
class FakeFiles(Files):
    """Files given directly, instead of searched for in a project."""

    paths: tuple[Path, ...]

    @override
    def files(self) -> tuple[Path, ...]:
        """Return the given files."""
        return self.paths
