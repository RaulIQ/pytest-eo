"""Something that runs and leaves an output behind."""

from typing import Protocol

from pytest_eo.output import Output


class Command(Protocol):
    """Something that can be run and produces an :class:`Output`."""

    def run(self) -> Output:
        """Run it and return what it printed."""
        ...
