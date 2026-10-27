"""The calls of a node that no other call holds."""

import ast
from dataclasses import dataclass
from typing import final

from typing_extensions import override


@final
@dataclass(frozen=True, slots=True)
class OuterCalls(ast.NodeVisitor):  # noqa: ENC100 - a visitor holds no state, ast dispatches on the node
    """The calls that start a nesting, each found once with all it holds."""

    @override
    def generic_visit(self, node: ast.AST) -> tuple[ast.Call, ...]:
        """Collect the outer calls among the children of a node."""
        return tuple(
            call
            for child in ast.iter_child_nodes(node)
            for call in self.visit(child)
        )

    @override
    def visit_Call(self, node: ast.Call) -> tuple[ast.Call, ...]:
        """Find the call itself and nothing inside it."""
        return (node,)
