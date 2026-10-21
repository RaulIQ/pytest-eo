"""TST200: a test module shares no constants between its tests."""

import ast
from collections.abc import Iterator
from dataclasses import dataclass
from typing import final

from typing_extensions import override

from pytest_eo.rule import Rule
from pytest_eo.shared import Shared


@final
@dataclass(frozen=True, slots=True)
class ModuleConstants(Rule):
    """Values a test module assigns for its tests to share."""

    _tree: ast.Module

    @override
    def problems(self) -> Iterator[tuple[int, int, str]]:
        """Report every module statement that shares a value."""
        return (
            (
                statement.lineno,
                statement.col_offset,
                "TST200 test module must not share constants between its tests",
            )
            for statement in self._tree.body
            if Shared().visit(statement)
        )
