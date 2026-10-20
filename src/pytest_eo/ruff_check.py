"""``ruff check`` as a source of violations."""

import json
from dataclasses import dataclass
from typing import final

from typing_extensions import override

from pytest_eo.check import Check
from pytest_eo.command import Command
from pytest_eo.tool_failed_error import ToolFailedError
from pytest_eo.verified import Verified
from pytest_eo.violation import Violation


@final
@dataclass(frozen=True, slots=True)
class RuffCheck(Check):
    """``ruff check`` with the locked configuration."""

    command: Command

    @property
    @override
    def name(self) -> str:
        """Short name shown in the pytest report."""
        return "ruff"

    @override
    def violations(self) -> tuple[Violation, ...]:
        """Parse the JSON report of ``ruff check``."""
        output = Verified(self.command, self.name, (0, 1)).run()
        try:
            items = json.loads(output.stdout or "[]")
        except json.JSONDecodeError as error:
            message = f"ruff printed invalid JSON: {error}"
            raise ToolFailedError(message) from error
        return tuple(
            Violation(
                tool=self.name,
                code=item["code"] or "syntax",
                path=item["filename"],
                line=item["location"]["row"],
                column=item["location"]["column"],
                message=item["message"],
            )
            for item in items
        )
