"""Rules of Angry Tests, which flake8 runs over the test files of pytest."""

import ast
import re
from collections.abc import Iterator
from dataclasses import dataclass
from pathlib import PurePath
from typing import Protocol, final

from typing_extensions import override

_NEGATION = re.compile(
    r"\b(?:not|never|no|nothing|cannot|dont|doesnt|didnt|isnt|arent|wasnt"
    r"|werent|wont|cant)\b",
    re.IGNORECASE,
)


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


def _assertions(tree: ast.Module) -> Iterator[tuple[int, int, str]]:
    return (
        (
            test.lineno,
            test.col_offset,
            "TST100 test must end with its only assertion",
        )
        for test in _tests(tree)
        if not _asserted(test)
    )


def _shared(statement: ast.stmt) -> bool:
    match statement:
        case (
            ast.Assign(targets=[ast.Name(id="pytest_plugins")])
            | ast.AnnAssign(target=ast.Name(id="pytest_plugins"))
        ):
            shared = False
        case ast.Assign() | ast.AnnAssign() | ast.AugAssign():
            shared = True
        case _:
            shared = False
    return shared


def _constants(tree: ast.Module) -> Iterator[tuple[int, int, str]]:
    return (
        (
            statement.lineno,
            statement.col_offset,
            "TST200 test module must not share constants between its tests",
        )
        for statement in tree.body
        if _shared(statement)
    )


def _text(message: ast.expr | None) -> str:
    match message:
        case ast.Constant(value=str() as text):
            found = text
        case ast.JoinedStr(values=parts):
            found = " ".join(_text(part) for part in parts)
        case _:
            found = ""
    return found


def _messages(tree: ast.Module) -> Iterator[tuple[int, int, str]]:
    return (
        (
            node.lineno,
            node.col_offset,
            "TST300 assertion must explain its failure with a negation",
        )
        for node in ast.walk(tree)
        if isinstance(node, ast.Assert)
        and not _NEGATION.search(_text(node.msg))
    )


@final
@dataclass(frozen=True, slots=True)
class AngryTests(Extension):
    """Tests that end with their only assertion and share no constants.

    A test that ends with ``pytest.raises`` makes its assertion there.
    Every assertion carries a negative message, such as "x doesnt y".
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
        for line, column, text in (
            *_assertions(self.tree),
            *_constants(self.tree),
            *_messages(self.tree),
        ):
            yield line, column, text, AngryTests
