"""BOD200: a function body holds no comments."""

import ast
import re
import tokenize
from collections.abc import Iterator, Sequence
from dataclasses import dataclass
from typing import final

from typing_extensions import override

from pytest_eo.rule import Rule
from pytest_eo.span import Span

_SUPPRESSION = re.compile(
    r"#\s*(?:noqa\b|type:\s*ignore\b|ruff:|flake8:|mypy:)"
)


@final
@dataclass(frozen=True, slots=True)
class InlineComments(Rule):
    """Comments inside the functions of a module.

    A suppression is a comment too, but ``eo::suppressions`` governs it, so
    it doesnt count.
    """

    _tree: ast.Module
    _tokens: Sequence[tokenize.TokenInfo]

    @override
    def problems(self) -> Iterator[tuple[int, int, str]]:
        """Report every comment from the first to the last row of a body."""
        inside = {
            row for node in ast.walk(self._tree) for row in Span().visit(node)
        }
        return (
            (*token.start, "BOD200 function body must not hold comments")
            for token in self._tokens
            if token.type == tokenize.COMMENT
            and token.start[0] in inside
            and not _SUPPRESSION.match(token.string)
        )
