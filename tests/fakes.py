"""Fakes: real implementations of the interfaces, with canned behaviour."""

from dataclasses import dataclass

from pytest_eo.command import Output


@dataclass(frozen=True, slots=True)
class FakeCommand:
    """A command that prints what it was told to, without running anything."""

    output: Output

    def run(self) -> Output:
        """Return the canned output."""
        return self.output
