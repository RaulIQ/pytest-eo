"""Whether a statement ends a test with its assertion."""

import ast
from dataclasses import dataclass
from typing import final

from typing_extensions import override

from pytest_eo.assertion import Assertion


@final
@dataclass(frozen=True, slots=True)
class Ending(ast.NodeVisitor):
    """Whether a statement is an assertion that may close a test."""

    @override
    def generic_visit(self, node: ast.AST) -> bool:
        """Refuse any other statement as the end of a test."""
        return False

    @override
    def visit_Assert(self, node: ast.Assert) -> bool:
        """Accept a plain assert as the end of a test."""
        return True

    @override
    def visit_Expr(self, node: ast.Expr) -> bool:
        """Accept an expression that asserts, such as a matcher."""
        return bool(Assertion().visit(node.value))
