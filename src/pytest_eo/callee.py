"""The function a call goes to."""

import ast
from dataclasses import dataclass
from typing import final

from typing_extensions import override


@final
@dataclass(frozen=True, slots=True)
class Callee(ast.NodeVisitor):
    """The source of the function a call goes to; nothing for other nodes."""

    @override
    def generic_visit(self, node: ast.AST) -> str:
        """Name nothing for a node that calls nothing."""
        return ""

    @override
    def visit_Call(self, node: ast.Call) -> str:
        """Name the function of a call as its source spells it."""
        return ast.unparse(node.func)
