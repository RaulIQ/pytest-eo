"""Suppression comments: each one gives a reason, and some codes allow none."""

import io
import re
import tokenize
from collections.abc import Iterator
from dataclasses import dataclass
from pathlib import Path
from typing import final

from typing_extensions import override

from pytest_eo.check import Check
from pytest_eo.files import Files
from pytest_eo.violation import Violation

_FORMS = (
    (
        re.compile(
            r"#\s*noqa:\s*(?P<codes>[A-Z]+\d*(?:\s*,\s*[A-Z]+\d*)*)"
            r"(?P<rest>[^#]*)",
        ),
        "# noqa: {}",
    ),
    (
        re.compile(
            r"#\s*ruff:\s*ignore\[(?P<codes>[\w-]+(?:\s*,\s*[\w-]+)*)\]"
            r"(?P<rest>[^#]*)",
        ),
        "# ruff: ignore[{}]",
    ),
)
_REASON = re.compile(r"^\s+-\s+\S")
_SPREAD = r"ruff:\s*(?:noqa|file-ignore|disable)\b|flake8:\s*noqa\b|mypy:"
_WIDE = re.compile(rf"#\s*(?P<kind>{_SPREAD})")
_HEADER = re.compile(rf"#\s*(?P<kind>{_SPREAD}|type:\s*ignore\b(?!\[))")
_SILENT = (tokenize.COMMENT, tokenize.NL, tokenize.NEWLINE, tokenize.ENCODING)


def _comments(file: Path) -> Iterator[tuple[int, int, str, bool]]:
    text = file.read_text(encoding="utf-8")
    try:
        tokens = tuple(tokenize.generate_tokens(io.StringIO(text).readline))
    except (tokenize.TokenError, SyntaxError):
        return
    code = next(token.start for token in tokens if token.type not in _SILENT)
    for token in tokens:
        if token.type == tokenize.COMMENT:
            yield (*token.start, token.string, token.start < code)


def _matches(text: str) -> Iterator[tuple[str, re.Match[str]]]:
    for form, template in _FORMS:
        for match in form.finditer(text):
            yield template, match


@final
@dataclass(frozen=True, slots=True)
class SuppressionCheck(Check):
    """Suppressions without a reason, of a forbidden rule, or wider than a line.

    It reads ``# noqa: CODE`` and ``# ruff: ignore[CODE-OR-NAME]``, and
    refuses the file-wide and range forms of ruff, flake8 and mypy outright.
    """

    sources: Files
    forbidden: tuple[str, ...]

    @property
    @override
    def name(self) -> str:
        """Short name shown in the pytest report."""
        return "suppressions"

    @override
    def violations(self) -> tuple[Violation, ...]:
        """Read the comments of every file, never running a tool."""
        return tuple(
            found for file in self.sources.files() for found in self._file(file)
        )

    def _file(self, file: Path) -> Iterator[Violation]:
        for line, column, text, header in _comments(file):
            for template, match in _matches(text):
                place = (str(file), line, column + match.start() + 1)
                yield from self._match(place, template, match)
            for match in (_HEADER if header else _WIDE).finditer(text):
                yield Violation(
                    self.name,
                    "SUP003",
                    str(file),
                    line,
                    column + match.start() + 1,
                    f"`# {match['kind']}` suppresses beyond its own line: "
                    "suppress on that one line instead, with a reason",
                )

    def _match(
        self,
        place: tuple[str, int, int],
        template: str,
        match: re.Match[str],
    ) -> Iterator[Violation]:
        codes = tuple(code.strip() for code in match["codes"].split(","))
        listed = template.format(", ".join(codes))
        banned = tuple(
            code for code in codes if code.startswith(self.forbidden)
        )
        if banned:
            message = (
                f"{', '.join(banned)} cannot be suppressed: "
                "fix the code instead"
            )
            yield Violation(self.name, "SUP002", *place, message)
        if not _REASON.match(match["rest"]):
            message = (
                f"`{listed}` needs a reason: "
                f"write `{listed} - why the rule cannot hold here`"
            )
            yield Violation(self.name, "SUP001", *place, message)
