"""The attributes that one statement of a class body declares."""

import ast
from dataclasses import dataclass
from typing import final

from typing_extensions import override

from pytest_eo.assigned import Assigned


@final
@dataclass(frozen=True, slots=True)
class Fields(ast.NodeVisitor):  # noqa: ENC100 - a visitor holds no state, ast dispatches on the node
    """Names of the instance attributes a statement of a class body declares.

    An annotated name other than a ``ClassVar`` is a field, as dataclasses
    read it, and so is every attribute of self that ``__init__`` sets.
    """

    @override
    def generic_visit(self, node: ast.AST) -> tuple[str, ...]:
        """Find no field in any other statement."""
        return ()

    @override
    def visit_AnnAssign(self, node: ast.AnnAssign) -> tuple[str, ...]:
        """Name an annotated field, unless it belongs to the class itself."""
        if ast.unparse(node.annotation).split("[")[0].endswith("ClassVar"):
            return ()
        return (ast.unparse(node.target),)

    @override
    def visit_FunctionDef(self, node: ast.FunctionDef) -> tuple[str, ...]:
        """Name the attributes that the constructor sets, at any depth."""
        if node.name != "__init__":
            return ()
        return tuple(
            name for inner in ast.walk(node) for name in Assigned().visit(inner)
        )
