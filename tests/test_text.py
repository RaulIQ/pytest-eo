import ast

from hamcrest import assert_that, equal_to

from pytest_eo.text import Text


def test_reads_a_string() -> None:
    assert_that(
        Text().visit(ast.parse("'the owl doesnt hoot'", mode="eval").body),
        equal_to("the owl doesnt hoot"),
        "a string isnt read",
    )


def test_reads_the_literal_parts_of_a_formatted_string() -> None:
    assert_that(
        Text().visit(ast.parse("f'{owl} cannot {act}'", mode="eval").body),
        equal_to("  cannot  "),
        "the literal parts of a formatted string arent read",
    )


def test_reads_nothing_from_a_variable() -> None:
    assert_that(
        Text().visit(ast.parse("owl", mode="eval").body),
        equal_to(""),
        "a variable doesnt read as nothing",
    )
