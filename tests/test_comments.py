from pathlib import Path

from hamcrest import assert_that, empty, equal_to

from pytest_eo.comments import Comments


def test_reads_every_comment_of_a_file(tmp_path: Path) -> None:
    file = tmp_path / "gull.py"
    file.write_text("x = 1  # tea\n\ny = 2  # rum\n", encoding="utf-8")
    assert_that(
        tuple(
            (comment.token.start, comment.token.string)
            for comment in Comments(file)
        ),
        equal_to((((1, 7), "# tea"), ((3, 7), "# rum"))),
        "the comments of a file arent read",
    )


def test_tells_the_header_from_the_rest(tmp_path: Path) -> None:
    file = tmp_path / "tern.py"
    file.write_text("# top\n\n# mid\nx = 1  # low\n", encoding="utf-8")
    assert_that(
        tuple(comment.header for comment in Comments(file)),
        equal_to((True, True, False)),
        "the comments above the first code arent told from the rest",
    )


def test_reads_nothing_from_a_file_that_cannot_be_tokenized(
    tmp_path: Path,
) -> None:
    file = tmp_path / "skua.py"
    file.write_text("x = (  # open\n", encoding="utf-8")
    assert_that(
        tuple(Comments(file)),
        empty(),
        "a file that cannot be tokenized doesnt read as empty",
    )
