import ast

from hamcrest import assert_that, empty, equal_to

from pytest_eo.span import Span


def test_spans_every_row_of_a_function() -> None:
    assert_that(
        tuple(
            Span().visit(
                ast.parse(
                    "import os\n\n\ndef lark(a):\n    b = a\n    return b\n",
                ).body[1],
            ),
        ),
        equal_to((4, 5, 6)),
        "the rows of a function arent spanned",
    )


def test_spans_every_row_of_a_coroutine() -> None:
    assert_that(
        tuple(
            Span().visit(
                ast.parse("async def wren():\n    await sky()\n").body[0],
            ),
        ),
        equal_to((1, 2)),
        "the rows of a coroutine arent spanned",
    )


def test_spans_nothing_outside_a_function() -> None:
    assert_that(
        tuple(Span().visit(ast.parse("class Owl:\n    eyes: int\n").body[0])),
        empty(),
        "a class isnt left without a span",
    )
