"""The attributes that one statement of a constructor sets."""

import ast
from dataclasses import dataclass
from typing import final

from typing_extensions import override

from pytest_eo.owned import Owned


@final
@dataclass(frozen=True, slots=True)
class Assigned(ast.NodeVisitor):  # noqa: ENC100 - a visitor holds no state, ast dispatches on the node
    """Names of the attributes of self that a statement assigns."""

    @override
    def generic_visit(self, node: ast.AST) -> tuple[str, ...]:
        """Find no attribute in a statement that assigns nothing."""
        return ()

    @override
    def visit_Assign(self, node: ast.Assign) -> tuple[str, ...]:
        """Name the attributes of self among the targets of an assignment."""
        return tuple(
            name for target in node.targets for name in Owned().visit(target)
        )

    @override
    def visit_AnnAssign(self, node: ast.AnnAssign) -> tuple[str, ...]:
        """Name the attribute of self that an annotated assignment sets."""
        return tuple(Owned().visit(node.target))
