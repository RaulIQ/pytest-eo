"""Whether a node asserts."""

import ast
from dataclasses import dataclass
from typing import final

from typing_extensions import override

from pytest_eo.callee import Callee


@final
@dataclass(frozen=True, slots=True)
class Assertion(ast.NodeVisitor):
    """Whether a node asserts, by a plain ``assert`` or by ``assert_that``."""

    @override
    def generic_visit(self, node: ast.AST) -> bool:
        """Find no assertion in any other node."""
        return False

    @override
    def visit_Assert(self, node: ast.Assert) -> bool:
        """Find an assertion in a plain assert."""
        return True

    @override
    def visit_Call(self, node: ast.Call) -> bool:
        """Find an assertion in a call of ``assert_that``, qualified or not."""
        return str(Callee().visit(node)).rsplit(".", 1)[-1] == "assert_that"
