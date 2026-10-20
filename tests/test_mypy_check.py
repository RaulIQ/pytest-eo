import json

import pytest
from hamcrest import assert_that, empty, equal_to, has_length

from pytest_eo.mypy_check import MypyCheck
from pytest_eo.output import Output
from pytest_eo.tool_failed_error import ToolFailedError
from tests.support.fake_command import FakeCommand


def test_reports_nothing_when_types_are_clean() -> None:
    check = MypyCheck(FakeCommand(Output("", "", 0)))
    assert_that(
        check.violations(),
        empty(),
        "clean mypy output isnt read as no violations",
    )


def test_reports_the_error_code_mypy_found() -> None:
    error = json.dumps(
        {
            "file": "src/app.py",
            "line": 2,
            "column": 0,
            "message": "Function is missing a type annotation",
            "code": "no-untyped-def",
            "severity": "error",
        },
    )
    check = MypyCheck(FakeCommand(Output(error, "", 1)))
    assert_that(
        check.violations()[0].code,
        equal_to("no-untyped-def"),
        "the error code of mypy isnt reported",
    )


def test_skips_notes_that_only_explain_errors() -> None:
    error = json.dumps(
        {
            "file": "lib/clock.py",
            "line": 11,
            "column": 4,
            "message": "Function is missing a return type annotation",
            "code": "no-untyped-def",
            "severity": "error",
        },
    )
    note = json.dumps(
        {
            "file": "lib/clock.py",
            "line": 11,
            "column": 4,
            "message": 'Use "-> None" if function does not return a value',
            "code": None,
            "severity": "note",
        },
    )
    check = MypyCheck(FakeCommand(Output(f"{error}\n{note}\n", "", 1)))
    assert_that(
        check.violations(), has_length(1), "a note of mypy isnt skipped"
    )


def test_fails_loudly_when_mypy_cannot_run() -> None:
    check = MypyCheck(FakeCommand(Output("", "no .py files", 2)))
    with pytest.raises(ToolFailedError):
        check.violations()
