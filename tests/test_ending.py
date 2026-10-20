import ast

from hamcrest import assert_that

from pytest_eo.ending import Ending


def test_ends_a_test_with_a_plain_assert() -> None:
    assert_that(
        Ending().visit(ast.parse("assert 7 > 2, 'no seven'").body[0]),
        "a plain assert doesnt end a test",
    )


def test_ends_a_test_with_a_matcher() -> None:
    assert_that(
        Ending().visit(
            ast.parse("assert_that(fig, has_length(4), 'no fig')").body[0],
        ),
        "a matcher doesnt end a test",
    )


def test_ends_no_test_with_another_statement() -> None:
    assert_that(
        not Ending().visit(ast.parse("print(fig)").body[0]),
        "a statement that asserts nothing ends a test",
    )
