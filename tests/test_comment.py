import re
import tokenize
from pathlib import Path

from hamcrest import assert_that, empty, equal_to

from pytest_eo.comment import Comment


def test_finds_a_pattern_where_it_stands_in_the_file() -> None:
    assert_that(
        tuple(
            str(place)
            for place, _ in Comment(
                Path("lib/moth.py"),
                tokenize.TokenInfo(
                    tokenize.COMMENT, "# wing # wing", (6, 4), (6, 17), ""
                ),
            ).matches(re.compile(r"wing"))
        ),
        equal_to(("lib/moth.py:6:7", "lib/moth.py:6:14")),
        "a pattern isnt found where it stands in the file",
    )


def test_finds_nothing_as_a_heading() -> None:
    assert_that(
        tuple(
            Comment(
                Path("lib/moth.py"),
                tokenize.TokenInfo(
                    tokenize.COMMENT, "# dust", (2, 0), (2, 6), ""
                ),
            ).heading(re.compile(r"dust")),
        ),
        empty(),
        "a comment below the code isnt kept out of headings",
    )
