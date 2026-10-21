"""The two rows that border a definition."""

import ast
from collections.abc import Iterable, Iterator
from dataclasses import dataclass
from typing import final

from typing_extensions import override


@final
@dataclass(frozen=True, slots=True)
class Edges(Iterable[int]):
    """The row above a definition and its decorators, and the row below it."""

    _node: ast.FunctionDef | ast.AsyncFunctionDef | ast.ClassDef

    @override
    def __iter__(self) -> Iterator[int]:
        """Yield the row above the first decorator and the row past the end."""
        yield (
            min(
                item.lineno for item in (self._node, *self._node.decorator_list)
            )
            - 1
        )
        yield (self._node.end_lineno or self._node.lineno) + 1
