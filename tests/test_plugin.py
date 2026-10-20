import pytest

TIDY = '''"""A tidy package."""


def double(number: int) -> int:
    """Return twice the number."""
    return number * 2
'''

SLOPPY = '''"""A sloppy package."""
import os


class Box:
    pass


def double(number):
    return number*2  # noqa: E226
'''

MOCKED = '''"""A package that sneaks a mock in."""

from unittest import mock  # noqa: TID251 - just this once

__all__ = ["mock"]
'''

STATIC = '''"""A package with a static method."""


class Money:
    @staticmethod
    def parse(text):
        return int(text)
'''


UNCONTRACTED = '''"""A package with a public method after a private one."""


class House:
    def _floors(self):
        return 1

    def area(self):
        return 5
'''


AGENTIVE = '''"""A package with a class named after a doer."""

from typing import final


@final
class Parser:
    """Turns text into numbers."""
'''


NESTED = '''"""A package with blocks nested too deep."""


def depth(flag: bool) -> int:
    """Count how deep the flag goes."""
    if flag:
        if flag:
            if flag:
                if flag:
                    if flag:
                        if flag:
                            return 6
    return 0
'''


def project(pytester: pytest.Pytester, source: str) -> pytest.Pytester:
    pytester.makepyprojecttoml('[tool.eo]\npaths = ["src"]\n')
    package = pytester.path / "src" / "tidy"
    package.mkdir(parents=True)
    (package / "__init__.py").write_text('"""A package under the gate."""\n')
    (package / "box.py").write_text(source)
    return pytester


def test_does_nothing_without_the_option(pytester: pytest.Pytester) -> None:
    result = project(pytester, SLOPPY).runpytest_subprocess()
    assert result.ret == pytest.ExitCode.NO_TESTS_COLLECTED


def test_passes_every_tool_on_tidy_code(pytester: pytest.Pytester) -> None:
    result = project(pytester, TIDY).runpytest_subprocess("--eo")
    assert result.parseoutcomes() == {"passed": 5}


def test_fails_every_tool_on_sloppy_code(pytester: pytest.Pytester) -> None:
    result = project(pytester, SLOPPY).runpytest_subprocess("--eo")
    assert result.parseoutcomes() == {"failed": 5}


def test_refuses_to_suppress_the_ban_on_mocks(
    pytester: pytest.Pytester,
) -> None:
    result = project(pytester, MOCKED).runpytest_subprocess("--eo")
    assert "[suppressions:SUP002]" in result.stdout.str()


def test_reports_static_methods(pytester: pytest.Pytester) -> None:
    result = project(pytester, STATIC).runpytest_subprocess("--eo")
    assert "[flake8:PEO400]" in result.stdout.str()


def test_reports_class_names_ending_in_er(pytester: pytest.Pytester) -> None:
    result = project(pytester, AGENTIVE).runpytest_subprocess("--eo")
    assert "tidy/box.py:7:1: [flake8:PEO300]" in result.stdout.str()


def test_reports_public_methods_after_private_ones(
    pytester: pytest.Pytester,
) -> None:
    result = project(pytester, UNCONTRACTED).runpytest_subprocess("--eo")
    assert "tidy/box.py:8:5: [flake8:OVR100]" in result.stdout.str()


def test_reports_blocks_nested_too_deep(pytester: pytest.Pytester) -> None:
    result = project(pytester, NESTED).runpytest_subprocess("--eo")
    assert "tidy/box.py:6:5: [ruff:PLR1702]" in result.stdout.str()


def test_reports_functions_with_five_arguments(
    pytester: pytest.Pytester,
) -> None:
    result = project(
        pytester,
        '"""A package with a wide function."""\n\n\n'
        "def total(a: int, b: int, c: int, d: int, e: int) -> int:\n"
        '    """Add the numbers up."""\n'
        "    return a + b + c + d + e\n",
    ).runpytest_subprocess("--eo")
    assert "tidy/box.py:4:5: [ruff:PLR0913]" in result.stdout.str(), (
        "five arguments dont fail the gate"
    )


def test_refuses_to_suppress_the_ban_on_mocks_by_name(
    pytester: pytest.Pytester,
) -> None:
    result = project(
        pytester,
        '"""A package that sneaks a mock in by name."""\n\n'
        "from unittest import mock  # ruff: ignore[banned-api] - just once\n\n"
        '__all__ = ["mock"]\n',
    ).runpytest_subprocess("--eo")
    assert "[suppressions:SUP002]" in result.stdout.str(), (
        "a ruff ignore of the ban on mocks doesnt fail the gate"
    )


def test_reports_a_test_with_two_assertions(pytester: pytest.Pytester) -> None:
    gate = project(pytester, TIDY)
    (gate.path / "src" / "tidy" / "test_box.py").write_text(
        '"""Tests of a box."""\n\n\n'
        "def test_lid() -> None:\n"
        '    """Open the lid twice."""\n'
        "    assert len('lid') == 3\n"
        "    assert 'lid'.upper() == 'LID'\n",
    )
    assert "tidy/test_box.py:4:1: [flake8:TST100]" in (
        gate.runpytest_subprocess("--eo").stdout.str()
    ), "a test with two assertions doesnt fail the gate"
