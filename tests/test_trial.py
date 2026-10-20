import ast

from hamcrest import assert_that, empty, equal_to

from pytest_eo.trial import Trial


def test_finds_a_test_function() -> None:
    assert_that(
        tuple(
            test.name
            for test in Trial().visit(
                ast.parse("def test_moss():\n    print(2)").body[0],
            )
        ),
        equal_to(("test_moss",)),
        "a test function isnt found",
    )


def test_finds_an_asynchronous_test_function() -> None:
    assert_that(
        tuple(
            test.name
            for test in Trial().visit(
                ast.parse("async def test_fern():\n    print(5)").body[0],
            )
        ),
        equal_to(("test_fern",)),
        "an asynchronous test function isnt found",
    )


def test_skips_a_helper_function() -> None:
    assert_that(
        Trial().visit(ast.parse("def lichen():\n    print(3)").body[0]),
        empty(),
        "a helper function isnt skipped",
    )
