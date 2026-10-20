import pytest


def project(pytester: pytest.Pytester, source: str) -> pytest.Pytester:
    pytester.makepyprojecttoml('[tool.eo]\npaths = ["src"]\n')
    package = pytester.path / "src" / "tidy"
    package.mkdir(parents=True)
    (package / "__init__.py").write_text('"""A package under the gate."""\n')
    (package / "box.py").write_text(source)
    return pytester


def test_does_nothing_without_the_option(pytester: pytest.Pytester) -> None:
    result = project(pytester, "import os\n").runpytest_subprocess()
    assert result.ret == pytest.ExitCode.NO_TESTS_COLLECTED


def test_passes_every_tool_on_tidy_code(pytester: pytest.Pytester) -> None:
    result = project(
        pytester,
        '"""A tidy package."""\n'
        "\n"
        "\n"
        "def double(number: int) -> int:\n"
        '    """Return twice the number."""\n'
        "    return number * 2\n",
    ).runpytest_subprocess("--eo")
    assert result.parseoutcomes() == {"passed": 5}


def test_fails_every_tool_on_sloppy_code(pytester: pytest.Pytester) -> None:
    result = project(
        pytester,
        '"""A sloppy package."""\n'
        "import os\n"
        "\n"
        "\n"
        "class Box:\n"
        "    pass\n"
        "\n"
        "\n"
        "def double(number):\n"
        "    return number*2  # noqa: E226\n",
    ).runpytest_subprocess("--eo")
    assert result.parseoutcomes() == {"failed": 5}


def test_refuses_to_suppress_the_ban_on_mocks(
    pytester: pytest.Pytester,
) -> None:
    result = project(
        pytester,
        '"""A package that sneaks a mock in."""\n'
        "\n"
        "from unittest import mock  # noqa: TID251 - just this once\n"
        "\n"
        '__all__ = ["mock"]\n',
    ).runpytest_subprocess("--eo")
    assert "[suppressions:SUP002]" in result.stdout.str()


def test_reports_static_methods(pytester: pytest.Pytester) -> None:
    result = project(
        pytester,
        '"""A package with a static method."""\n'
        "\n"
        "\n"
        "class Money:\n"
        "    @staticmethod\n"
        "    def parse(text):\n"
        "        return int(text)\n",
    ).runpytest_subprocess("--eo")
    assert "[flake8:PEO400]" in result.stdout.str()


def test_reports_class_names_ending_in_er(pytester: pytest.Pytester) -> None:
    result = project(
        pytester,
        '"""A package with a class named after a doer."""\n'
        "\n"
        "from typing import final\n"
        "\n"
        "\n"
        "@final\n"
        "class Parser:\n"
        '    """Turns text into numbers."""\n',
    ).runpytest_subprocess("--eo")
    assert "tidy/box.py:7:1: [flake8:PEO300]" in result.stdout.str()


def test_reports_public_methods_after_private_ones(
    pytester: pytest.Pytester,
) -> None:
    result = project(
        pytester,
        '"""A package with a public method after a private one."""\n'
        "\n"
        "\n"
        "class House:\n"
        "    def _floors(self):\n"
        "        return 1\n"
        "\n"
        "    def area(self):\n"
        "        return 5\n",
    ).runpytest_subprocess("--eo")
    assert "tidy/box.py:8:5: [flake8:OVR100]" in result.stdout.str()


def test_reports_blocks_nested_too_deep(pytester: pytest.Pytester) -> None:
    result = project(
        pytester,
        '"""A package with blocks nested too deep."""\n'
        "\n"
        "\n"
        "def depth(flag: bool) -> int:\n"
        '    """Count how deep the flag goes."""\n'
        "    if flag:\n"
        "        if flag:\n"
        "            if flag:\n"
        "                if flag:\n"
        "                    if flag:\n"
        "                        if flag:\n"
        "                            return 6\n"
        "    return 0\n",
    ).runpytest_subprocess("--eo")
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
    gate = project(pytester, '"""A box under the gate."""\n')
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


def test_reports_a_constant_shared_by_tests(pytester: pytest.Pytester) -> None:
    gate = project(pytester, '"""A box under the gate."""\n')
    (gate.path / "src" / "tidy" / "test_box.py").write_text(
        '"""Tests of a box."""\n\nWIDTH = 31\n',
    )
    assert "tidy/test_box.py:3:1: [flake8:TST200]" in (
        gate.runpytest_subprocess("--eo").stdout.str()
    ), "a constant shared by tests doesnt fail the gate"
