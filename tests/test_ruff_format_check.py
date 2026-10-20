from hamcrest import assert_that, empty, equal_to, has_length

from pytest_eo.output import Output
from pytest_eo.ruff_format_check import RuffFormatCheck
from tests.support.fake_command import FakeCommand


def test_reports_nothing_when_files_are_formatted() -> None:
    check = RuffFormatCheck(FakeCommand(Output("", "", 0)))
    assert_that(
        check.violations(),
        empty(),
        "formatted files arent read as no violations",
    )


def test_reports_each_file_the_formatter_would_change() -> None:
    check = RuffFormatCheck(
        FakeCommand(
            Output(
                "src/app.py:2:1: unformatted: File would be reformatted\n",
                "",
                1,
            ),
        ),
    )
    assert_that(
        check.violations()[0].path,
        equal_to("src/app.py"),
        "a file the formatter would change isnt reported",
    )


def test_ignores_the_summary_line() -> None:
    check = RuffFormatCheck(
        FakeCommand(
            Output(
                "kit/rope.py:9:1: unformatted: File would be reformatted\n"
                "1 file would be reformatted\n",
                "",
                1,
            ),
        ),
    )
    assert_that(
        check.violations(),
        has_length(1),
        "the summary line of ruff format isnt ignored",
    )
