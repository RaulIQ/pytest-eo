import ast
import io
import tokenize

from hamcrest import assert_that, empty, equal_to

from pytest_eo.inline_comments import InlineComments


def problems(code: str) -> tuple[tuple[int, int, str], ...]:
    return tuple(
        InlineComments(
            ast.parse(code),
            tuple(tokenize.generate_tokens(io.StringIO(code).readline)),
        ).problems(),
    )


def test_reports_a_comment_inside_a_function() -> None:
    assert_that(
        problems("def heron(a):\n    # halve it\n    return a // 2\n"),
        equal_to(((2, 4, "BOD200 function body must not hold comments"),)),
        "a comment inside a function isnt reported",
    )


def test_reports_a_comment_at_the_end_of_a_row() -> None:
    assert_that(
        tuple(
            (line, column)
            for line, column, _ in problems(
                "async def stork():\n    await nest()  # wait here\n",
            )
        ),
        equal_to(((2, 18),)),
        "a comment after the code of a row isnt reported",
    )


def test_passes_suppressions_inside_a_function() -> None:
    assert_that(
        problems(
            "def crane(a):\n"
            "    b = a  # noqa: E731 - the reason\n"
            "    c = b  # type: ignore[misc]  # the reason\n"
            "    return c  # ruff: ignore[RET504] - the reason\n",
        ),
        empty(),
        "a suppression inside a function doesnt pass",
    )


def test_passes_comments_outside_a_function() -> None:
    assert_that(
        problems(
            "# the module\nclass Ibis:\n    # the field\n    beak: int\n\n\n"
            "# the function\ndef egret():\n    return 3\n",
        ),
        empty(),
        "a comment outside a function doesnt pass",
    )
