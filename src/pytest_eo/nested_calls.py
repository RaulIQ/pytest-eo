"""NST100: an expression nests calls no deeper than the limit."""

import ast
from collections.abc import Iterator
from dataclasses import dataclass
from typing import final

from typing_extensions import override

from pytest_eo.call_depth import CallDepth
from pytest_eo.outer_calls import OuterCalls
from pytest_eo.rule import Rule


@final
@dataclass(frozen=True, slots=True)
class NestedCalls(Rule):
    """Calls nested so deep that the code reads inside out.

    Objects composed from decorators wrap each other, and every new
    feature adds a level, so the depth needs a limit of its own.
    """

    _tree: ast.Module
    _limit: int

    @override
    def problems(self) -> Iterator[tuple[int, int, str]]:
        """Report every outer call that nests deeper than the limit."""
        return (
            (
                call.lineno,
                call.col_offset,
                (
                    "NST100 expression must not nest more than "
                    f"{self._limit} calls inside each other, found {depth}"
                ),
            )
            for call in OuterCalls().visit(self._tree)
            if (depth := CallDepth().visit(call)) > self._limit
        )
