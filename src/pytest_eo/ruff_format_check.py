"""``ruff format --check`` as a source of violations."""

import re
from dataclasses import dataclass
from typing import final

from typing_extensions import override

from pytest_eo.check import Check
from pytest_eo.command import Command
from pytest_eo.place import Place
from pytest_eo.verified import Verified
from pytest_eo.violation import Violation


@final
@dataclass(frozen=True, slots=True)
class RuffFormatCheck(Check):
    """``ruff format --check``: files that the formatter would change."""

    command: Command

    @override
    def name(self) -> str:
        """Short name shown in the pytest report."""
        return "ruff-format"

    @override
    def violations(self) -> tuple[Violation, ...]:
        """Parse the concise report of ``ruff format --check``."""
        output = Verified(self.command, self.name(), (0, 1)).run()
        pattern = re.compile(
            r"^(?P<path>.+?):(?P<line>\d+):(?P<col>\d+): "
            r"(?P<code>\w+): (?P<msg>.+)$"
        )
        found = (pattern.match(line) for line in output.stdout.splitlines())
        return tuple(
            Violation(
                tool=self.name(),
                code=match["code"],
                place=Place(
                    match["path"], int(match["line"]), int(match["col"])
                ),
                message=match["msg"],
            )
            for match in found
            if match
        )
