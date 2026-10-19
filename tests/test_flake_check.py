import pytest

from pytest_eo.check import FlakeCheck
from pytest_eo.command import Output, ToolFailedError
from tests.fakes import FakeCommand

REPORT = "src/app.py:4:1: FIN100 class must be final\n"


def test_reports_nothing_when_flake8_is_clean() -> None:
    check = FlakeCheck(FakeCommand(Output("", "", 0)))
    assert check.violations() == ()


def test_reports_the_rule_code_flake8_found() -> None:
    check = FlakeCheck(FakeCommand(Output(REPORT, "", 1)))
    assert check.violations()[0].code == "FIN100"


def test_reports_the_line_flake8_found() -> None:
    check = FlakeCheck(FakeCommand(Output(REPORT, "", 1)))
    assert check.violations()[0].line == 4


def test_fails_loudly_when_flake8_crashes_without_a_report() -> None:
    check = FlakeCheck(FakeCommand(Output("", "Traceback ...", 1)))
    with pytest.raises(ToolFailedError):
        check.violations()
