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
    return number*2
'''

STATIC = '''"""A package with a static method."""


class Money:
    @staticmethod
    def parse(text):
        return int(text)
'''


def project(pytester: pytest.Pytester, source: str) -> pytest.Pytester:
    pytester.makepyprojecttoml('[tool.eo]\npaths = ["src"]\n')
    package = pytester.path / "src" / "tidy"
    package.mkdir(parents=True)
    (package / "__init__.py").write_text(source)
    return pytester


def test_does_nothing_without_the_option(pytester: pytest.Pytester) -> None:
    result = project(pytester, SLOPPY).runpytest_subprocess()
    assert result.ret == pytest.ExitCode.NO_TESTS_COLLECTED


def test_passes_every_tool_on_tidy_code(pytester: pytest.Pytester) -> None:
    result = project(pytester, TIDY).runpytest_subprocess("--eo")
    assert result.parseoutcomes() == {"passed": 4}


def test_fails_every_tool_on_sloppy_code(pytester: pytest.Pytester) -> None:
    result = project(pytester, SLOPPY).runpytest_subprocess("--eo")
    assert result.parseoutcomes() == {"failed": 4}


def test_reports_static_methods(pytester: pytest.Pytester) -> None:
    result = project(pytester, STATIC).runpytest_subprocess("--eo")
    assert "[flake8:PEO400]" in result.stdout.str()
