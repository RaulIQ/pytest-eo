"""What an assertion says when it fails."""

import ast
from dataclasses import dataclass
from typing import final

from typing_extensions import override

from pytest_eo.assertion import Assertion
from pytest_eo.text import Text


@final
@dataclass(frozen=True, slots=True)
class Message(ast.NodeVisitor):
    """The place and words of a failure message, and nothing for other nodes.

    A plain ``assert`` speaks through its message; ``assert_that`` speaks
    through its ``reason`` keyword or else its last argument.
    """

    @override
    def generic_visit(self, node: ast.AST) -> tuple[tuple[int, int, str], ...]:
        """Find no message in a node that asserts nothing."""
        return ()

    @override
    def visit_Assert(
        self, node: ast.Assert
    ) -> tuple[tuple[int, int, str], ...]:
        """Read the message of a plain assert, empty when it has none."""
        return (
            (
                node.lineno,
                node.col_offset,
                Text().visit(node.msg or ast.Constant("")),
            ),
        )

    @override
    def visit_Call(self, node: ast.Call) -> tuple[tuple[int, int, str], ...]:
        """Read the reason of a matcher, given by keyword or last."""
        if not (node.args and Assertion().visit(node)):
            return ()
        return (
            (
                node.lineno,
                node.col_offset,
                Text().visit(
                    next(
                        (
                            word.value
                            for word in node.keywords
                            if word.arg == "reason"
                        ),
                        node.args[-1],
                    ),
                ),
            ),
        )
