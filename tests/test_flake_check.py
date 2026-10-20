import pytest

from pytest_eo.check import FlakeCheck
from pytest_eo.command import Output, ToolFailedError
from tests.fakes import FakeCommand


def test_reports_nothing_when_flake8_is_clean() -> None:
    check = FlakeCheck(FakeCommand(Output("", "", 0)))
    assert check.violations() == (), (
        "clean flake8 output isnt read as no violations"
    )


def test_reports_the_rule_code_flake8_found() -> None:
    check = FlakeCheck(
        FakeCommand(
            Output("src/app.py:4:1: FIN100 class must be final\n", "", 1)
        ),
    )
    assert check.violations()[0].code == "FIN100", (
        "the rule code of flake8 isnt reported"
    )


def test_reports_the_line_flake8_found() -> None:
    check = FlakeCheck(
        FakeCommand(Output("lib/wheel.py:17:3: PEO400 no static\n", "", 1)),
    )
    assert check.violations()[0].line == 17, (
        "the line of a flake8 finding isnt reported"
    )


def test_fails_loudly_when_flake8_crashes_without_a_report() -> None:
    check = FlakeCheck(FakeCommand(Output("", "Traceback ...", 1)))
    with pytest.raises(ToolFailedError):
        check.violations()
