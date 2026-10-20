"""TST100: a test ends with its only assertion."""

import ast
from collections.abc import Iterator
from dataclasses import dataclass
from typing import final

from typing_extensions import override

from pytest_eo.assertion import Assertion
from pytest_eo.ending import Ending
from pytest_eo.raising import Raising
from pytest_eo.rule import Rule
from pytest_eo.trial import Trial


@final
@dataclass(frozen=True, slots=True)
class FinalAssertion(Rule):
    """Tests that end with their only assertion, or with ``pytest.raises``.

    A test that ends with ``pytest.raises`` makes its assertion there, so it
    may hold no other one.
    """

    tree: ast.Module

    @override
    def problems(self) -> Iterator[tuple[int, int, str]]:
        """Report every test that doesnt end with its only assertion."""
        for test in (
            found
            for node in ast.walk(self.tree)
            for found in Trial().visit(node)
        ):
            count = sum(Assertion().visit(inner) for inner in ast.walk(test))
            last = test.body[-1]
            if not (
                (count == 1 and Ending().visit(last))
                or (count == 0 and Raising().visit(last))
            ):
                yield (
                    test.lineno,
                    test.col_offset,
                    "TST100 test must end with its only assertion",
                )
