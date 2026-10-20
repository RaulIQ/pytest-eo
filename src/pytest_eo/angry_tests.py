"""Rules of Angry Tests, which flake8 runs over the test files of pytest."""

import ast
import re
from collections.abc import Iterator
from dataclasses import dataclass
from pathlib import PurePath
from typing import final

from typing_extensions import override

from pytest_eo.extension import Extension

_NEGATION = re.compile(
    r"\b(?:not|never|no|nothing|cannot|dont|doesnt|didnt|isnt|arent|wasnt"
    r"|werent|wont|cant)\b",
    re.IGNORECASE,
)


def _tests(
    tree: ast.Module,
) -> Iterator[ast.FunctionDef | ast.AsyncFunctionDef]:
    return (
        node
        for node in ast.walk(tree)
        if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef)  # noqa: PEO700 - becomes NodeVisitor rules in #47
        and node.name.startswith("test")
    )


def _raising(statement: ast.stmt) -> bool:
    match statement:
        case ast.With(  # noqa: PEO700 - becomes NodeVisitor rules in #47
            items=[
                ast.withitem(  # noqa: PEO700 - becomes NodeVisitor rules in #47
                    context_expr=ast.Call(  # noqa: PEO700 - becomes NodeVisitor rules in #47
                        func=ast.Attribute(  # noqa: PEO700 - becomes NodeVisitor rules in #47
                            value=ast.Name(id="pytest"),  # noqa: PEO700 - becomes NodeVisitor rules in #47
                            attr="raises",
                        ),
                    ),
                ),
            ],
        ):
            return True
    return False


def _hamcrest(node: ast.AST) -> bool:
    match node:
        case ast.Call(  # noqa: PEO700 - becomes NodeVisitor rules in #47
            func=ast.Name(id="assert_that") | ast.Attribute(attr="assert_that"),  # noqa: PEO700 - becomes NodeVisitor rules in #47
        ):
            found = True
        case _:
            found = False
    return found


def _assertion(statement: ast.stmt) -> bool:
    match statement:
        case ast.Assert():  # noqa: PEO700 - becomes NodeVisitor rules in #47
            found = True
        case ast.Expr(value=value):  # noqa: PEO700 - becomes NodeVisitor rules in #47
            found = _hamcrest(value)
        case _:
            found = False
    return found


def _asserted(test: ast.FunctionDef | ast.AsyncFunctionDef) -> bool:
    count = sum(
        isinstance(node, ast.Assert) or _hamcrest(node)  # noqa: PEO700 - becomes NodeVisitor rules in #47
        for node in ast.walk(test)
    )
    last = test.body[-1]
    return (count == 1 and _assertion(last)) or (count == 0 and _raising(last))


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
            ast.Assign(targets=[ast.Name(id="pytest_plugins")])  # noqa: PEO700 - becomes NodeVisitor rules in #47
            | ast.AnnAssign(target=ast.Name(id="pytest_plugins"))  # noqa: PEO700 - becomes NodeVisitor rules in #47
        ):
            shared = False
        case ast.Assign() | ast.AnnAssign() | ast.AugAssign():  # noqa: PEO700 - becomes NodeVisitor rules in #47
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
        case ast.Constant(value=str() as text):  # noqa: PEO700 - becomes NodeVisitor rules in #47
            found = text
        case ast.JoinedStr(values=parts):  # noqa: PEO700 - becomes NodeVisitor rules in #47
            found = " ".join(_text(part) for part in parts)
        case _:
            found = ""
    return found


def _said(tree: ast.Module) -> Iterator[tuple[ast.stmt | ast.expr, str]]:
    for node in ast.walk(tree):
        match node:
            case ast.Assert(msg=message):  # noqa: PEO700 - becomes NodeVisitor rules in #47
                yield node, _text(message)
            case ast.Call(args=[*_, last], keywords=keywords) if _hamcrest(  # noqa: PEO700 - becomes NodeVisitor rules in #47
                node
            ):
                yield (
                    node,
                    _text(
                        next(
                            (
                                word.value
                                for word in keywords
                                if word.arg == "reason"
                            ),
                            last,
                        ),
                    ),
                )


def _messages(tree: ast.Module) -> Iterator[tuple[int, int, str]]:
    return (
        (
            node.lineno,
            node.col_offset,
            "TST300 assertion must explain its failure with a negation",
        )
        for node, text in _said(tree)
        if not _NEGATION.search(text)
    )


@final
@dataclass(frozen=True, slots=True)
class AngryTests(Extension):
    """Tests that end with their only assertion and share no constants.

    An assertion is a plain ``assert`` or a Hamcrest ``assert_that``; a test
    that ends with ``pytest.raises`` makes its assertion there. Every
    assertion carries a negative message, such as "x doesnt y".
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
