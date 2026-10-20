"""Rules of Angry Tests, which flake8 runs over the test files of pytest."""

import ast
from collections.abc import Iterator
from dataclasses import dataclass
from pathlib import PurePath
from typing import Protocol, final

from typing_extensions import override


class Extension(Protocol):
    """A flake8 plugin: the problems of one parsed file."""

    def run(self) -> Iterator[tuple[int, int, str, type[object]]]:
        """Yield the line, column, message and plugin of every problem."""
        ...


def _tests(
    tree: ast.Module,
) -> Iterator[ast.FunctionDef | ast.AsyncFunctionDef]:
    return (
        node
        for node in ast.walk(tree)
        if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef)
        and node.name.startswith("test")
    )


def _raising(statement: ast.stmt) -> bool:
    match statement:
        case ast.With(
            items=[
                ast.withitem(
                    context_expr=ast.Call(
                        func=ast.Attribute(
                            value=ast.Name(id="pytest"),
                            attr="raises",
                        ),
                    ),
                ),
            ],
        ):
            return True
    return False


def _asserted(test: ast.FunctionDef | ast.AsyncFunctionDef) -> bool:
    count = sum(isinstance(node, ast.Assert) for node in ast.walk(test))
    last = test.body[-1]
    return (count == 1 and isinstance(last, ast.Assert)) or (
        count == 0 and _raising(last)
    )


@final
@dataclass(frozen=True, slots=True)
class AngryTests(Extension):
    """Tests that make one assertion, as their last statement.

    A test that ends with ``pytest.raises`` makes its assertion there.
    """

    tree: ast.Module
    filename: str

    @override
    def run(self) -> Iterator[tuple[int, int, str, type[object]]]:
        """Report the tests of a pytest test file that break a rule."""
        if not any(
            PurePath(self.filename).match(pattern)
            for pattern in ("test_*.py", "*_test.py")
        ):
            return
        for test in _tests(self.tree):
            if not _asserted(test):
                yield (
                    test.lineno,
                    test.col_offset,
                    "TST100 test must end with its only assertion",
                    AngryTests,
                )
