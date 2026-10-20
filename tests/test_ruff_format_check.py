from pytest_eo.check import RuffFormatCheck
from pytest_eo.command import Output
from tests.fakes import FakeCommand


def test_reports_nothing_when_files_are_formatted() -> None:
    check = RuffFormatCheck(FakeCommand(Output("", "", 0)))
    assert check.violations() == (), (
        "formatted files arent read as no violations"
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
    assert check.violations()[0].path == "src/app.py", (
        "a file the formatter would change isnt reported"
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
    assert len(check.violations()) == 1, (
        "the summary line of ruff format isnt ignored"
    )
