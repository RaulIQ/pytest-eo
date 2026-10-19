from pytest_eo.check import RuffFormatCheck
from pytest_eo.command import Output
from tests.fakes import FakeCommand

REPORT = (
    "src/app.py:2:1: unformatted: File would be reformatted\n"
    "1 file would be reformatted\n"
)


def test_reports_nothing_when_files_are_formatted() -> None:
    check = RuffFormatCheck(FakeCommand(Output("", "", 0)))
    assert check.violations() == ()


def test_reports_each_file_the_formatter_would_change() -> None:
    check = RuffFormatCheck(FakeCommand(Output(REPORT, "", 1)))
    assert check.violations()[0].path == "src/app.py"


def test_ignores_the_summary_line() -> None:
    check = RuffFormatCheck(FakeCommand(Output(REPORT, "", 1)))
    assert len(check.violations()) == 1
