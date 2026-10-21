import tokenize
from pathlib import Path

from hamcrest import assert_that, empty, equal_to, matches_regexp

from pytest_eo.comment import Comment
from pytest_eo.narrow_suppressions import NarrowSuppressions


def test_reports_a_suppression_without_a_reason() -> None:
    assert_that(
        tuple(
            str(found)
            for found in NarrowSuppressions(
                "sup",
                Comment(
                    Path("lib/oak.py"),
                    tokenize.TokenInfo(
                        tokenize.COMMENT, "# noqa: F401", (3, 9), (3, 21), ""
                    ),
                    header=False,
                ),
                (),
            )
        ),
        equal_to(
            (
                (
                    "lib/oak.py:3:10: [sup:SUP001] `# noqa: F401` needs a "
                    "reason: write `# noqa: F401 - why the rule cannot hold "
                    "here`"
                ),
            ),
        ),
        "a suppression without a reason isnt reported",
    )


def test_reports_a_code_that_cannot_be_suppressed() -> None:
    assert_that(
        "\n".join(
            str(found)
            for found in NarrowSuppressions(
                "sup",
                Comment(
                    Path("lib/elm.py"),
                    tokenize.TokenInfo(
                        tokenize.COMMENT,
                        "# ruff: ignore[TID251] - only once",
                        (8, 0),
                        (8, 34),
                        "",
                    ),
                    header=False,
                ),
                ("TID251",),
            )
        ),
        matches_regexp(r"\A[^\n]*:SUP002\][^\n]*\Z"),
        "a forbidden code isnt reported",
    )


def test_passes_a_suppression_with_a_reason() -> None:
    assert_that(
        tuple(
            NarrowSuppressions(
                "sup",
                Comment(
                    Path("lib/ash.py"),
                    tokenize.TokenInfo(
                        tokenize.COMMENT,
                        "# noqa: E501 - a long url",
                        (2, 4),
                        (2, 29),
                        "",
                    ),
                    header=False,
                ),
                ("TID251",),
            ),
        ),
        empty(),
        "a suppression with a reason doesnt pass",
    )
