"""Whether a statement expects an exception."""

import ast
from dataclasses import dataclass
from typing import final

from typing_extensions import override

from pytest_eo.callee import Callee


@final
@dataclass(frozen=True, slots=True)
class Raising(ast.NodeVisitor):  # noqa: ENC100 - a visitor holds no state, ast dispatches on the node
    """Whether a statement is a block under ``pytest.raises`` alone."""

    @override
    def generic_visit(self, node: ast.AST) -> bool:
        """Expect no exception from any other statement."""
        return False

    @override
    def visit_With(self, node: ast.With) -> bool:
        """Expect an exception from a block under ``pytest.raises`` alone."""
        return tuple(
            Callee().visit(item.context_expr) for item in node.items
        ) == ("pytest.raises",)
