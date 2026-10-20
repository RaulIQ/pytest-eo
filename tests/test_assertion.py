import ast

from hamcrest import assert_that

from pytest_eo.assertion import Assertion


def test_counts_a_plain_assert() -> None:
    assert_that(
        Assertion().visit(ast.parse("assert tuba, 'no tuba'").body[0]),
        "a plain assert isnt an assertion",
    )


def test_counts_a_matcher() -> None:
    assert_that(
        Assertion().visit(
            ast.parse("assert_that(oboe, empty())", mode="eval").body,
        ),
        "a call of assert_that isnt an assertion",
    )


def test_counts_a_matcher_called_through_its_module() -> None:
    assert_that(
        Assertion().visit(
            ast.parse("hamcrest.assert_that(oboe, empty())", mode="eval").body,
        ),
        "a qualified call of assert_that isnt an assertion",
    )


def test_ignores_any_other_call() -> None:
    assert_that(
        not Assertion().visit(ast.parse("print(lute)", mode="eval").body),
        "a call that doesnt assert is an assertion",
    )
