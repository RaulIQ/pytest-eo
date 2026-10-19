"""One aggregated tool: knows how to run itself and read its report."""

import json
import re
from dataclasses import dataclass
from typing import Protocol, final

from pytest_eo.command import Command, Output, ToolFailedError
from pytest_eo.violation import Violation


class Check(Protocol):
    """A named source of violations."""

    @property
    def name(self) -> str:
        """Short name shown in the pytest report."""
        ...

    def violations(self) -> tuple[Violation, ...]:
        """Run the tool and return everything it complains about."""
        ...


def _expect(output: Output, tool: str, allowed: tuple[int, ...]) -> Output:
    if output.status not in allowed:
        message = f"{tool} exited with {output.status}: {output.stderr.strip()}"
        raise ToolFailedError(message)
    return output


@final
@dataclass(frozen=True, slots=True)
class RuffCheck:
    """``ruff check`` with the locked configuration."""

    command: Command

    @property
    def name(self) -> str:
        """Short name shown in the pytest report."""
        return "ruff"

    def violations(self) -> tuple[Violation, ...]:
        """Parse the JSON report of ``ruff check``."""
        output = _expect(self.command.run(), self.name, (0, 1))
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


@final
@dataclass(frozen=True, slots=True)
class RuffFormatCheck:
    """``ruff format --check``: files that the formatter would change."""

    command: Command

    @property
    def name(self) -> str:
        """Short name shown in the pytest report."""
        return "ruff-format"

    def violations(self) -> tuple[Violation, ...]:
        """Parse the concise report of ``ruff format --check``."""
        output = _expect(self.command.run(), self.name, (0, 1))
        pattern = re.compile(
            r"^(?P<path>.+?):(?P<line>\d+):(?P<col>\d+): (?P<code>\w+): (?P<msg>.+)$"
        )
        found = (pattern.match(line) for line in output.stdout.splitlines())
        return tuple(
            Violation(
                tool=self.name,
                code=match["code"],
                path=match["path"],
                line=int(match["line"]),
                column=int(match["col"]),
                message=match["msg"],
            )
            for match in found
            if match
        )


@final
@dataclass(frozen=True, slots=True)
class MypyCheck:
    """``mypy --strict`` with JSON output."""

    command: Command

    @property
    def name(self) -> str:
        """Short name shown in the pytest report."""
        return "mypy"

    def violations(self) -> tuple[Violation, ...]:
        """Parse one JSON object per line, skipping notes."""
        output = _expect(self.command.run(), self.name, (0, 1))
        lines = (line for line in output.stdout.splitlines() if line.startswith("{"))
        items = (json.loads(line) for line in lines)
        return tuple(
            Violation(
                tool=self.name,
                code=item["code"] or "error",
                path=item["file"],
                line=item["line"],
                column=item["column"],
                message=item["message"],
            )
            for item in items
            if item["severity"] == "error"
        )


@final
@dataclass(frozen=True, slots=True)
class FlakeCheck:
    """``flake8`` with pyeo: rules of Elegant Objects."""

    command: Command

    @property
    def name(self) -> str:
        """Short name shown in the pytest report."""
        return "flake8"

    def violations(self) -> tuple[Violation, ...]:
        """Parse the default ``path:row:col: CODE text`` report of flake8."""
        output = _expect(self.command.run(), self.name, (0, 1))
        pattern = re.compile(
            r"^(?P<path>.+?):(?P<line>\d+):(?P<col>\d+): "
            r"(?P<code>[A-Z]+\d+) (?P<msg>.+)$"
        )
        found = tuple(
            Violation(
                tool=self.name,
                code=match["code"],
                path=match["path"],
                line=int(match["line"]),
                column=int(match["col"]),
                message=match["msg"],
            )
            for match in (pattern.match(line) for line in output.stdout.splitlines())
            if match
        )
        if output.status == 1 and not found:
            message = f"flake8 failed without a report: {output.stderr.strip()}"
            raise ToolFailedError(message)
        return found
