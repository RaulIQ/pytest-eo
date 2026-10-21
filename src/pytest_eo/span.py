"""The rows that a function takes in its file."""

import ast
from dataclasses import dataclass
from typing import final

from typing_extensions import override


@final
@dataclass(frozen=True, slots=True)
class Span(ast.NodeVisitor):  # noqa: ENC100 - a visitor holds no state, ast dispatches on the node
    """The rows of a function, from ``def`` to its last line, and none else."""

    @override
    def generic_visit(self, node: ast.AST) -> range:
        """Span no rows of a node that isnt a function."""
        return range(0)

    @override
    def visit_FunctionDef(self, node: ast.FunctionDef) -> range:
        """Span the rows of a function."""
        return range(node.lineno, (node.end_lineno or node.lineno) + 1)

    @override
    def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef) -> range:
        """Span the rows of a coroutine."""
        return range(node.lineno, (node.end_lineno or node.lineno) + 1)
