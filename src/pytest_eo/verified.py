"""A command that fails loudly unless it exits as expected."""

from dataclasses import dataclass
from typing import final

from typing_extensions import override

from pytest_eo.command import Command
from pytest_eo.output import Output
from pytest_eo.tool_failed_error import ToolFailedError


@final
@dataclass(frozen=True, slots=True)
class Verified(Command):
    """A tool run that refuses any exit status its reader does not expect."""

    origin: Command
    tool: str
    allowed: tuple[int, ...]

    @override
    def run(self) -> Output:
        """Run the command and fail on a status outside of the allowed ones."""
        output = self.origin.run()
        if output.status not in self.allowed:
            message = (
                f"{self.tool} exited with {output.status}: "
                f"{output.stderr.strip()}"
            )
            raise ToolFailedError(message)
        return output
