import pytest
from hamcrest import assert_that, empty, equal_to

from pytest_eo.flake_check import FlakeCheck
from pytest_eo.output import Output
from pytest_eo.tool_failed_error import ToolFailedError
from tests.support.fake_command import FakeCommand


def test_reports_nothing_when_flake8_is_clean() -> None:
    check = FlakeCheck(FakeCommand(Output("", "", 0)))
    assert_that(
        check.violations(),
        empty(),
        "clean flake8 output isnt read as no violations",
    )


def test_reports_the_rule_code_flake8_found() -> None:
    check = FlakeCheck(
        FakeCommand(
            Output("src/app.py:4:1: FIN100 class must be final\n", "", 1)
        ),
    )
    assert_that(
        check.violations()[0].code,
        equal_to("FIN100"),
        "the rule code of flake8 isnt reported",
    )


def test_reports_the_line_flake8_found() -> None:
    check = FlakeCheck(
        FakeCommand(Output("lib/wheel.py:17:3: PEO400 no static\n", "", 1)),
    )
    assert_that(
        check.violations()[0].line,
        equal_to(17),
        "the line of a flake8 finding isnt reported",
    )


def test_fails_loudly_when_flake8_crashes_without_a_report() -> None:
    check = FlakeCheck(FakeCommand(Output("", "Traceback ...", 1)))
    with pytest.raises(ToolFailedError):
        check.violations()
