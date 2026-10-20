import json

import pytest

from pytest_eo.check import RuffCheck
from pytest_eo.command import Output, ToolFailedError
from tests.fakes import FakeCommand


def test_reports_nothing_when_ruff_is_clean() -> None:
    check = RuffCheck(FakeCommand(Output("[]", "", 0)))
    assert check.violations() == (), (
        "clean ruff output isnt read as no violations"
    )


def test_reports_the_rule_code_ruff_found() -> None:
    report = json.dumps(
        [
            {
                "code": "F401",
                "filename": "src/app.py",
                "location": {"row": 3, "column": 8},
                "message": "`os` imported but unused",
            },
        ],
    )
    check = RuffCheck(FakeCommand(Output(report, "", 1)))
    assert check.violations()[0].code == "F401", (
        "the rule code of ruff isnt reported"
    )


def test_reports_the_line_ruff_found() -> None:
    report = json.dumps(
        [
            {
                "code": "E741",
                "filename": "lib/grid.py",
                "location": {"row": 23, "column": 5},
                "message": "Ambiguous variable name: `l`",
            },
        ],
    )
    check = RuffCheck(FakeCommand(Output(report, "", 1)))
    assert check.violations()[0].line == 23, (
        "the line of a ruff finding isnt reported"
    )


def test_fails_loudly_when_ruff_crashes() -> None:
    check = RuffCheck(FakeCommand(Output("", "panic", 2)))
    with pytest.raises(ToolFailedError):
        check.violations()


def test_fails_loudly_when_ruff_prints_garbage() -> None:
    check = RuffCheck(FakeCommand(Output("not json", "", 1)))
    with pytest.raises(ToolFailedError):
        check.violations()
