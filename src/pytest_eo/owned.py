"""The attributes of an object that an assignment sets on itself."""

import ast
from dataclasses import dataclass
from typing import final

from typing_extensions import override


@final
@dataclass(frozen=True, slots=True)
class Owned(ast.NodeVisitor):  # noqa: ENC100 - a visitor holds no state, ast dispatches on the node
    """Names of ``self.x`` in an assignment target, and nothing for others."""

    @override
    def generic_visit(self, node: ast.AST) -> tuple[str, ...]:
        """Find no attribute of self in any other target."""
        return ()

    @override
    def visit_Attribute(self, node: ast.Attribute) -> tuple[str, ...]:
        """Name the attribute when it belongs to ``self``."""
        return (node.attr,) if ast.unparse(node.value) == "self" else ()

    @override
    def visit_Tuple(self, node: ast.Tuple) -> tuple[str, ...]:
        """Name the attributes of self among the targets of an unpacking."""
        return tuple(name for item in node.elts for name in self.visit(item))
