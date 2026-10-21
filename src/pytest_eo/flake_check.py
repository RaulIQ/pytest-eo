"""``flake8`` with pyeo as a source of violations."""

import re
from dataclasses import dataclass
from typing import final

from typing_extensions import override

from pytest_eo.check import Check
from pytest_eo.command import Command
from pytest_eo.place import Place
from pytest_eo.tool_failed_error import ToolFailedError
from pytest_eo.verified import Verified
from pytest_eo.violation import Violation


@final
@dataclass(frozen=True, slots=True)
class FlakeCheck(Check):
    """``flake8`` with pyeo: rules of Elegant Objects."""

    _command: Command

    @override
    def name(self) -> str:
        """Short name shown in the pytest report."""
        return "flake8"

    @override
    def violations(self) -> tuple[Violation, ...]:
        """Parse the default ``path:row:col: CODE text`` report of flake8."""
        output = Verified(self._command, self.name(), (0, 1)).run()
        pattern = re.compile(
            r"^(?P<path>.+?):(?P<line>\d+):(?P<col>\d+): "
            r"(?P<code>[A-Z]+\d+) (?P<msg>.+)$"
        )
        found = tuple(
            Violation(
                self.name(),
                match["code"],
                Place(match["path"], int(match["line"]), int(match["col"])),
                match["msg"],
            )
            for match in (
                pattern.match(line) for line in output.stdout.splitlines()
            )
            if match
        )
        if output.status == 1 and not found:
            message = f"flake8 failed without a report: {output.stderr.strip()}"
            raise ToolFailedError(message)
        return found
