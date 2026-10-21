"""The rows right around a definition, where ruff format wants blank lines."""

import ast
from dataclasses import dataclass
from typing import final

from typing_extensions import override

from pytest_eo.edges import Edges


@final
@dataclass(frozen=True, slots=True)
class Margin(ast.NodeVisitor):  # noqa: ENC100 - a visitor holds no state, ast dispatches on the node
    """The rows that border a ``def`` or a ``class``, and none for others.

    ``ruff format`` puts a blank line on both sides of a nested ``def`` or
    ``class``, so a body may hold blank lines there and nowhere else.
    """

    @override
    def generic_visit(self, node: ast.AST) -> tuple[int, ...]:
        """Find no margins around a node that defines nothing."""
        return ()

    @override
    def visit_FunctionDef(self, node: ast.FunctionDef) -> tuple[int, ...]:
        """Find the rows around a function."""
        return tuple(Edges(node))

    @override
    def visit_AsyncFunctionDef(
        self,
        node: ast.AsyncFunctionDef,
    ) -> tuple[int, ...]:
        """Find the rows around a coroutine."""
        return tuple(Edges(node))

    @override
    def visit_ClassDef(self, node: ast.ClassDef) -> tuple[int, ...]:
        """Find the rows around a class."""
        return tuple(Edges(node))
