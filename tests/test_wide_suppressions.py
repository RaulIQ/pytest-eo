import tokenize
from pathlib import Path

from hamcrest import assert_that, empty, equal_to, matches_regexp

from pytest_eo.comment import Comment
from pytest_eo.heading import Heading
from pytest_eo.wide_suppressions import WideSuppressions


def test_reports_a_file_wide_suppression() -> None:
    assert_that(
        tuple(
            str(found)
            for found in WideSuppressions(
                "sup",
                Comment(
                    Path("lib/fir.py"),
                    tokenize.TokenInfo(
                        tokenize.COMMENT, "# flake8: noqa", (5, 2), (5, 16), ""
                    ),
                ),
            )
        ),
        equal_to(
            (
                (
                    "lib/fir.py:5:3: [sup:SUP003] `# flake8: noqa` suppresses "
                    "beyond its own line: suppress on that one line instead, "
                    "with a reason"
                ),
            ),
        ),
        "a file-wide suppression isnt reported",
    )


def test_reports_a_type_ignore_in_the_header() -> None:
    assert_that(
        "\n".join(
            str(found)
            for found in WideSuppressions(
                "sup",
                Heading(
                    Comment(
                        Path("lib/yew.py"),
                        tokenize.TokenInfo(
                            tokenize.COMMENT,
                            "# type: ignore",
                            (1, 0),
                            (1, 14),
                            "",
                        ),
                    ),
                ),
            )
        ),
        matches_regexp(r"\A[^\n]*:SUP003\][^\n]*\Z"),
        "a type ignore above the first code isnt reported",
    )


def test_passes_a_type_ignore_below_the_first_code() -> None:
    assert_that(
        tuple(
            WideSuppressions(
                "sup",
                Comment(
                    Path("lib/bay.py"),
                    tokenize.TokenInfo(
                        tokenize.COMMENT, "# type: ignore", (6, 9), (6, 23), ""
                    ),
                ),
            ),
        ),
        empty(),
        "a type ignore below the first code doesnt pass",
    )
