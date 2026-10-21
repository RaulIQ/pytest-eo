"""ENC100: a class encapsulates one to four attributes."""

import ast
from dataclasses import dataclass
from typing import final

from typing_extensions import override

from pytest_eo.fields import Fields

_ALLOWED = range(1, 5)


@final
@dataclass(frozen=True, slots=True)
class Capacity(ast.NodeVisitor):  # noqa: ENC100 - a visitor holds no state, ast dispatches on the node
    """A class with no attributes or more than four, and nothing for others.

    A protocol is an interface, which holds no state, so it is left alone.
    """

    @override
    def generic_visit(self, node: ast.AST) -> tuple[tuple[int, int, str], ...]:
        """Find nothing to count in a node that isnt a class."""
        return ()

    @override
    def visit_ClassDef(
        self,
        node: ast.ClassDef,
    ) -> tuple[tuple[int, int, str], ...]:
        """Count the attributes of a class and report a wrong number."""
        count = len(
            {name for item in node.body for name in Fields().visit(item)},
        )
        if count in _ALLOWED or any(
            ast.unparse(base).split("[")[0].endswith("Protocol")
            for base in node.bases
        ):
            return ()
        return (
            (
                node.lineno,
                node.col_offset,
                (
                    "ENC100 class must encapsulate one to four attributes, "
                    f"not {count}"
                ),
            ),
        )
