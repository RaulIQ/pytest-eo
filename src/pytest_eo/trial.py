"""The test functions pytest would run."""

import ast
from dataclasses import dataclass
from typing import final

from typing_extensions import override


@final
@dataclass(frozen=True, slots=True)
class Trial(ast.NodeVisitor):  # noqa: ENC100 - a visitor holds no state, ast dispatches on the node
    """A function whose name makes pytest run it; nothing for other nodes."""

    @override
    def generic_visit(
        self,
        node: ast.AST,
    ) -> tuple[ast.FunctionDef | ast.AsyncFunctionDef, ...]:
        """Find no test in a node that isnt a function."""
        return ()

    @override
    def visit_FunctionDef(
        self,
        node: ast.FunctionDef,
    ) -> tuple[ast.FunctionDef | ast.AsyncFunctionDef, ...]:
        """Find the function when its name starts with ``test``."""
        return (node,) if node.name.startswith("test") else ()

    @override
    def visit_AsyncFunctionDef(
        self,
        node: ast.AsyncFunctionDef,
    ) -> tuple[ast.FunctionDef | ast.AsyncFunctionDef, ...]:
        """Find the coroutine when its name starts with ``test``."""
        return (node,) if node.name.startswith("test") else ()
