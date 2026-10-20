import ast

from hamcrest import assert_that, empty, equal_to

from pytest_eo.message import Message


def test_reads_the_message_of_an_assert() -> None:
    assert_that(
        Message().visit(ast.parse("assert yak, 'no yak'").body[0]),
        equal_to(((1, 0, "no yak"),)),
        "the message of an assert isnt read",
    )


def test_reads_nothing_from_an_assert_without_a_message() -> None:
    assert_that(
        Message().visit(ast.parse("assert yak").body[0]),
        equal_to(((1, 0, ""),)),
        "an assert without a message doesnt read as nothing",
    )


def test_reads_the_last_argument_of_a_matcher() -> None:
    assert_that(
        Message().visit(
            ast.parse(
                "assert_that(yak, empty(), 'yak isnt bare')", mode="eval"
            ).body,
        ),
        equal_to(((1, 0, "yak isnt bare"),)),
        "the last argument of a matcher isnt read",
    )


def test_reads_the_reason_of_a_matcher() -> None:
    assert_that(
        Message().visit(
            ast.parse(
                "assert_that(yak, empty(), reason='no yak')", mode="eval"
            ).body,
        ),
        equal_to(((1, 0, "no yak"),)),
        "the reason of a matcher isnt read",
    )


def test_reads_nothing_from_another_call() -> None:
    assert_that(
        Message().visit(ast.parse("print('no yak')", mode="eval").body),
        empty(),
        "a call that doesnt assert has a message",
    )
