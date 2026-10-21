import re
import tokenize
from pathlib import Path

from hamcrest import assert_that, equal_to

from pytest_eo.comment import Comment
from pytest_eo.heading import Heading


def test_finds_a_pattern_as_a_heading() -> None:
    assert_that(
        tuple(
            str(place)
            for place, _ in Heading(
                Comment(
                    Path("lib/gnat.py"),
                    tokenize.TokenInfo(
                        tokenize.COMMENT, "# swarm", (1, 0), (1, 7), ""
                    ),
                ),
            ).heading(re.compile(r"swarm"))
        ),
        equal_to(("lib/gnat.py:1:3",)),
        "a comment above the code isnt taken for a heading",
    )


def test_finds_a_pattern_anywhere_too() -> None:
    assert_that(
        tuple(
            str(place)
            for place, _ in Heading(
                Comment(
                    Path("lib/gnat.py"),
                    tokenize.TokenInfo(
                        tokenize.COMMENT, "# swarm", (1, 0), (1, 7), ""
                    ),
                ),
            ).matches(re.compile(r"swarm"))
        ),
        equal_to(("lib/gnat.py:1:3",)),
        "a heading doesnt match like any other comment",
    )
