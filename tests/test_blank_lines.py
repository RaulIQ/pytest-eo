import ast
import io
import tokenize

from hamcrest import assert_that, empty, equal_to

from pytest_eo.blank_lines import BlankLines


def problems(code: str) -> tuple[tuple[int, int, str], ...]:
    return tuple(
        BlankLines(
            ast.parse(code),
            tuple(tokenize.generate_tokens(io.StringIO(code).readline)),
        ).problems(),
    )


def test_reports_a_blank_line_inside_a_function() -> None:
    assert_that(
        problems("def pike(a):\n    b = a + 4\n\n    return b\n"),
        equal_to(((3, 0, "BOD100 function body must not hold blank lines"),)),
        "a blank line inside a function isnt reported",
    )


def test_reports_a_blank_line_inside_brackets() -> None:
    assert_that(
        tuple(
            line
            for line, _, _ in problems(
                "def carp():\n    return max(\n        2,\n\n        5,\n"
                "    )\n",
            )
        ),
        equal_to((4,)),
        "a blank line between arguments isnt reported",
    )


def test_passes_a_blank_line_inside_a_string() -> None:
    assert_that(
        problems('def eel():\n    return """sea\n\nfloor"""\n'),
        empty(),
        "a blank line inside a string doesnt pass",
    )


def test_passes_blank_lines_around_a_nested_function() -> None:
    assert_that(
        problems(
            "def roach(a):\n    b = a\n\n    def bream():\n        return b\n"
            "\n    return bream\n",
        ),
        empty(),
        "blank lines around a nested function dont pass",
    )


def test_passes_blank_lines_between_functions() -> None:
    assert_that(
        problems(
            "class Pond:\n    def tench(self):\n        return 1\n\n"
            "    def perch(self):\n        return 6\n\n\ndef ruffe():\n"
            "    return 8\n",
        ),
        empty(),
        "blank lines between functions dont pass",
    )
