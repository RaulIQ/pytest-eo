"""Whether a statement of a module shares a value between its tests."""

import ast
from dataclasses import dataclass
from typing import final

from typing_extensions import override


@final
@dataclass(frozen=True, slots=True)
class Shared(ast.NodeVisitor):
    """Whether a statement assigns a module value besides ``pytest_plugins``."""

    @override
    def generic_visit(self, node: ast.AST) -> bool:
        """Share nothing through a statement that assigns nothing."""
        return False

    @override
    def visit_Assign(self, node: ast.Assign) -> bool:
        """Share the value unless it is the list of plugins."""
        return tuple(ast.unparse(target) for target in node.targets) != (
            "pytest_plugins",
        )

    @override
    def visit_AnnAssign(self, node: ast.AnnAssign) -> bool:
        """Share the annotated value unless it is the list of plugins."""
        return ast.unparse(node.target) != "pytest_plugins"

    @override
    def visit_AugAssign(self, node: ast.AugAssign) -> bool:
        """Share the value that a module changes in place."""
        return True
