import ast

from hamcrest import assert_that, empty, equal_to

from pytest_eo.negative_messages import NegativeMessages


def test_reports_where_a_positive_message_stands() -> None:
    assert_that(
        tuple(
            NegativeMessages(
                ast.parse("def test_elk():\n    assert 2, 'elk is fine'\n"),
            ).problems(),
        ),
        equal_to(
            (
                (
                    2,
                    4,
                    "TST300 assertion must explain its failure with a negation",
                ),
            ),
        ),
        "a positive message isnt reported where it stands",
    )


def test_passes_a_negative_message() -> None:
    assert_that(
        tuple(
            NegativeMessages(
                ast.parse("def test_elk():\n    assert 2, 'elk never runs'\n"),
            ).problems(),
        ),
        empty(),
        "a negative message doesnt pass",
    )
