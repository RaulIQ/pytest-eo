import ast

from hamcrest import assert_that

from pytest_eo.shared import Shared


def test_shares_an_assigned_constant() -> None:
    assert_that(
        Shared().visit(ast.parse("ZONE = 'q7'").body[0]),
        "an assigned constant isnt shared",
    )


def test_shares_an_annotated_constant() -> None:
    assert_that(
        Shared().visit(ast.parse("ZONE: str = 'q7'").body[0]),
        "an annotated constant isnt shared",
    )


def test_shares_an_augmented_constant() -> None:
    assert_that(
        Shared().visit(ast.parse("ZONE += 'q7'").body[0]),
        "an augmented constant isnt shared",
    )


def test_shares_no_plugins() -> None:
    assert_that(
        not Shared().visit(ast.parse("pytest_plugins = ['pytester']").body[0]),
        "the plugins of a module arent exempt",
    )


def test_shares_no_annotated_plugins() -> None:
    assert_that(
        not Shared().visit(
            ast.parse("pytest_plugins: list[str] = ['pytester']").body[0],
        ),
        "the annotated plugins of a module arent exempt",
    )


def test_shares_no_import() -> None:
    assert_that(
        not Shared().visit(ast.parse("import zlib").body[0]),
        "an import isnt left alone",
    )
