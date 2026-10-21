"""The suppressions of one line, and what is wrong with them."""

import re
from collections.abc import Iterable, Iterator
from dataclasses import dataclass
from typing import final

from typing_extensions import override

from pytest_eo.comment import Comment
from pytest_eo.place import Place
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


@final
@dataclass(frozen=True, slots=True)
class NarrowSuppressions(Iterable[Violation]):
    """Suppressions of one line that name a forbidden rule or give no reason.

    It reads ``# noqa: CODE`` and ``# ruff: ignore[CODE-OR-NAME]``.
    """

    _tool: str
    _comment: Comment
    _forbidden: tuple[str, ...]

    @override
    def __iter__(self) -> Iterator[Violation]:
        """Report every suppression of the comment that breaks a rule."""
        line, column = self._comment.token.start
        for template, match in (
            (template, match)
            for form, template in _FORMS
            for match in form.finditer(self._comment.token.string)
        ):
            place = Place(
                str(self._comment.file), line, column + match.start() + 1
            )
            codes = tuple(code.strip() for code in match["codes"].split(","))
            listed = template.format(", ".join(codes))
            banned = tuple(
                code for code in codes if code.startswith(self._forbidden)
            )
            if banned:
                yield Violation(
                    self._tool,
                    "SUP002",
                    place,
                    f"{', '.join(banned)} cannot be suppressed: "
                    "fix the code instead",
                )
            if not _REASON.match(match["rest"]):
                yield Violation(
                    self._tool,
                    "SUP001",
                    place,
                    f"`{listed}` needs a reason: "
                    f"write `{listed} - why the rule cannot hold here`",
                )
