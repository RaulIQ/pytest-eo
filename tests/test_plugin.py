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


def test_refuses_to_suppress_the_ban_on_mocks(pytester: pytest.Pytester) -> None:
    result = project(pytester, MOCKED).runpytest_subprocess("--eo")
    assert "[suppressions:SUP002]" in result.stdout.str()


def test_reports_static_methods(pytester: pytest.Pytester) -> None:
    result = project(pytester, STATIC).runpytest_subprocess("--eo")
    assert "[flake8:PEO400]" in result.stdout.str()


def test_reports_class_names_ending_in_er(pytester: pytest.Pytester) -> None:
    result = project(pytester, AGENTIVE).runpytest_subprocess("--eo")
    assert "tidy/box.py:7:1: [flake8:PEO300]" in result.stdout.str()


def test_reports_public_methods_after_private_ones(pytester: pytest.Pytester) -> None:
    result = project(pytester, UNCONTRACTED).runpytest_subprocess("--eo")
    assert "tidy/box.py:8:5: [flake8:OVR100]" in result.stdout.str()


def test_reports_blocks_nested_too_deep(pytester: pytest.Pytester) -> None:
    result = project(pytester, NESTED).runpytest_subprocess("--eo")
    assert "tidy/box.py:6:5: [ruff:PLR1702]" in result.stdout.str()
