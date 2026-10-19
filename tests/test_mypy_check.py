import json

import pytest

from pytest_eo.check import MypyCheck
from pytest_eo.command import Output, ToolFailedError
from tests.fakes import FakeCommand

ERROR = json.dumps(
    {
        "file": "src/app.py",
        "line": 2,
        "column": 0,
        "message": "Function is missing a type annotation",
        "code": "no-untyped-def",
        "severity": "error",
    },
)
NOTE = json.dumps(
    {
        "file": "src/app.py",
        "line": 2,
        "column": 0,
        "message": "Use --disallow-untyped-defs",
        "code": None,
        "severity": "note",
    },
)


def test_reports_nothing_when_types_are_clean() -> None:
    check = MypyCheck(FakeCommand(Output("", "", 0)))
    assert check.violations() == ()


def test_reports_the_error_code_mypy_found() -> None:
    check = MypyCheck(FakeCommand(Output(ERROR, "", 1)))
    assert check.violations()[0].code == "no-untyped-def"


def test_skips_notes_that_only_explain_errors() -> None:
    check = MypyCheck(FakeCommand(Output(f"{ERROR}\n{NOTE}\n", "", 1)))
    assert len(check.violations()) == 1


def test_fails_loudly_when_mypy_cannot_run() -> None:
    check = MypyCheck(FakeCommand(Output("", "no .py files", 2)))
    with pytest.raises(ToolFailedError):
        check.violations()
