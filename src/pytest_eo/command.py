"""Something that runs and leaves an output behind."""

from typing import Protocol

from pytest_eo.printout import Printout


class Command(Protocol):
    """Something that can be run and leaves a :class:`Printout`."""

    def run(self) -> Printout:
        """Run it and return what it printed."""
        ...
