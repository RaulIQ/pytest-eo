"""The words of a message as the source spells them."""

import ast
from dataclasses import dataclass
from typing import final

from typing_extensions import override


@final
@dataclass(frozen=True, slots=True)
class Text(ast.NodeVisitor):  # noqa: ENC100 - a visitor holds no state, ast dispatches on the node
    """The literal words of an expression, and nothing for computed ones."""

    @override
    def generic_visit(self, node: ast.AST) -> str:
        """Read nothing from a value only known at run time."""
        return ""

    @override
    def visit_Constant(self, node: ast.Constant) -> str:
        """Read a literal as it is written."""
        return str(node.value)

    @override
    def visit_JoinedStr(self, node: ast.JoinedStr) -> str:
        """Read the literal parts of a formatted string."""
        return " ".join(self.visit(part) for part in node.values)
