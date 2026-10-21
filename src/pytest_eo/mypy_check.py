"""``mypy --strict`` as a source of violations."""

import json
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
class MypyCheck(Check):
    """``mypy --strict`` with JSON output."""

    _command: Command

    @override
    def name(self) -> str:
        """Short name shown in the pytest report."""
        return "mypy"

    @override
    def violations(self) -> tuple[Violation, ...]:
        """Parse one JSON object per line, skipping notes."""
        output = Verified(self._command, self.name(), (0, 1)).run()
        lines = (
            line for line in output.stdout.splitlines() if line.startswith("{")
        )
        items = (json.loads(line) for line in lines)
        return tuple(
            Violation(
                self.name(),
                item["code"] or "error",
                Place(item["file"], item["line"], item["column"]),
                item["message"],
            )
            for item in items
            if item["severity"] == "error"
        )
