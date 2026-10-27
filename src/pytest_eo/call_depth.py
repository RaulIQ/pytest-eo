"""How deep the calls of a node nest inside each other."""

import ast
from dataclasses import dataclass
from typing import final

from typing_extensions import override


@final
@dataclass(frozen=True, slots=True)
class CallDepth(ast.NodeVisitor):  # noqa: ENC100 - a visitor holds no state, ast dispatches on the node
    """The longest run of calls that pass each other as arguments.

    A call adds a level to the calls in its arguments, but not to the call
    it is made on, so a chain of methods stays one level deep.
    """

    @override
    def generic_visit(self, node: ast.AST) -> int:
        """Take the deepest calls among the children of a node."""
        return max(
            (self.visit(child) for child in ast.iter_child_nodes(node)),
            default=0,
        )

    @override
    def visit_Call(self, node: ast.Call) -> int:
        """Add a level to the arguments, but not to the callee."""
        return max(
            self.generic_visit(node),
            1
            + max(
                (self.visit(arg) for arg in (*node.args, *node.keywords)),
                default=0,
            ),
        )
