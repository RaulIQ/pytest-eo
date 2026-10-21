"""A command that fails loudly unless it exits as expected."""

from dataclasses import dataclass
from typing import final

from typing_extensions import override

from pytest_eo.command import Command
from pytest_eo.printout import Printout


@final
@dataclass(frozen=True, slots=True)
class Verified(Command):
    """A tool run that refuses any exit status its reader does not expect."""

    _origin: Command
    _tool: str
    _allowed: tuple[int, ...]

    @override
    def run(self) -> Printout:
        """Run the command and fail on a status outside of the allowed ones."""
        output = self._origin.run()
        if not output.exited(self._allowed):
            reason = f"{self._tool} exited unexpectedly"
            raise output.failure(reason)
        return output
