"""BOD100: a function body holds no blank lines."""

import ast
import tokenize
from collections.abc import Iterator, Sequence
from dataclasses import dataclass
from typing import final

from typing_extensions import override

from pytest_eo.margin import Margin
from pytest_eo.rule import Rule
from pytest_eo.span import Span


@final
@dataclass(frozen=True, slots=True)
class BlankLines(Rule):
    """Blank lines inside the functions of a module.

    A blank line inside a string is a part of the string, and a blank line
    next to a nested definition is what ``ruff format`` puts there, so
    neither counts.
    """

    _tree: ast.Module
    _tokens: Sequence[tokenize.TokenInfo]

    @override
    def problems(self) -> Iterator[tuple[int, int, str]]:
        """Report every blank line from the first to the last row of a body."""
        nodes = tuple(ast.walk(self._tree))
        inside = {row for node in nodes for row in Span().visit(node)} - {
            row for node in nodes for row in Margin().visit(node)
        }
        return (
            (*token.start, "BOD100 function body must not hold blank lines")
            for token in self._tokens
            if token.type == tokenize.NL
            and not token.line.strip()
            and token.start[0] in inside
        )
