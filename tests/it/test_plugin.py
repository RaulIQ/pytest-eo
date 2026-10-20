import pytest
from hamcrest import assert_that, contains_string, equal_to


def project(pytester: pytest.Pytester, source: str) -> pytest.Pytester:
    pytester.makepyprojecttoml('[tool.eo]\npaths = ["src"]\n')
    package = pytester.path / "src" / "tidy"
    package.mkdir(parents=True)
    (package / "__init__.py").write_text('"""A package under the gate."""\n')
    (package / "box.py").write_text(source)
    return pytester


def test_does_nothing_without_the_option(pytester: pytest.Pytester) -> None:
    result = project(pytester, "import os\n").runpytest_subprocess()
    assert_that(
        result.ret,
        equal_to(pytest.ExitCode.NO_TESTS_COLLECTED),
        "the plugin doesnt stay idle without --eo",
    )


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
    assert_that(
        result.parseoutcomes(),
        equal_to({"passed": 5}),
        "tidy code doesnt pass every tool",
    )


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
    assert_that(
        result.parseoutcomes(),
        equal_to({"failed": 5}),
        "sloppy code doesnt fail every tool",
    )


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
    assert_that(
        result.stdout.str(),
        contains_string("[suppressions:SUP002]"),
        "a suppressed ban on mocks doesnt fail the gate",
    )


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
    assert_that(
        result.stdout.str(),
        contains_string("[flake8:PEO400]"),
        "a static method doesnt fail the gate",
    )


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
    assert_that(
        result.stdout.str(),
        contains_string("tidy/box.py:7:1: [flake8:PEO300]"),
        "a class name ending in -er doesnt fail the gate",
    )


def test_reports_reflection(pytester: pytest.Pytester) -> None:
    result = project(
        pytester,
        '"""A package that asks an object for its type."""\n'
        "\n"
        "\n"
        "def size(box: object) -> int:\n"
        '    """Count the items of a list and nothing else."""\n'
        "    return len(box) if isinstance(box, list) else 0\n",
    ).runpytest_subprocess("--eo")
    assert_that(
        result.stdout.str(),
        contains_string("tidy/box.py:6:24: [flake8:PEO700]"),
        "a call to isinstance doesnt fail the gate",
    )


def test_reports_private_methods(pytester: pytest.Pytester) -> None:
    result = project(
        pytester,
        '"""A package that hides a function."""\n'
        "\n"
        "\n"
        "def _half(number: int) -> int:\n"
        '    """Return half of the number."""\n'
        "    return number // 2\n",
    ).runpytest_subprocess("--eo")
    assert_that(
        result.stdout.str(),
        contains_string("tidy/box.py:4:1: [flake8:NPM100]"),
        "a private function doesnt fail the gate",
    )


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
    assert_that(
        result.stdout.str(),
        contains_string("tidy/box.py:8:5: [flake8:OVR100]"),
        "a public method after a private one doesnt fail the gate",
    )


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
    assert_that(
        result.stdout.str(),
        contains_string("tidy/box.py:6:5: [ruff:PLR1702]"),
        "blocks nested too deep dont fail the gate",
    )


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
    assert_that(
        result.stdout.str(),
        contains_string("tidy/box.py:4:5: [ruff:PLR0913]"),
        "five arguments dont fail the gate",
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
    assert_that(
        result.stdout.str(),
        contains_string("[suppressions:SUP002]"),
        "a ruff ignore of the ban on mocks doesnt fail the gate",
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
    assert_that(
        gate.runpytest_subprocess("--eo").stdout.str(),
        contains_string("tidy/test_box.py:4:1: [flake8:TST100]"),
        "a test with two assertions doesnt fail the gate",
    )


def test_reports_a_constant_shared_by_tests(pytester: pytest.Pytester) -> None:
    gate = project(pytester, '"""A box under the gate."""\n')
    (gate.path / "src" / "tidy" / "test_box.py").write_text(
        '"""Tests of a box."""\n\nWIDTH = 31\n',
    )
    assert_that(
        gate.runpytest_subprocess("--eo").stdout.str(),
        contains_string("tidy/test_box.py:3:1: [flake8:TST200]"),
        "a constant shared by tests doesnt fail the gate",
    )


def test_reports_an_assertion_without_a_message(
    pytester: pytest.Pytester,
) -> None:
    gate = project(pytester, '"""A box under the gate."""\n')
    (gate.path / "src" / "tidy" / "test_box.py").write_text(
        '"""Tests of a box."""\n\n\n'
        "def test_lid() -> None:\n"
        '    """Open the lid."""\n'
        "    assert len('lid') == 3\n",
    )
    assert_that(
        gate.runpytest_subprocess("--eo").stdout.str(),
        contains_string("tidy/test_box.py:6:5: [flake8:TST300]"),
        "an assertion without a message doesnt fail the gate",
    )


def test_reports_a_plain_assert_in_tests(pytester: pytest.Pytester) -> None:
    pytester.makepyprojecttoml('[tool.eo]\npaths = ["tests"]\n')
    (pytester.path / "tests").mkdir()
    (pytester.path / "tests" / "__init__.py").write_text('"""Tests."""\n')
    (pytester.path / "tests" / "test_lid.py").write_text(
        "def test_lid() -> None:\n"
        '    assert len("lid") == 3, "the lid isnt three letters long"\n',
    )
    assert_that(
        pytester.runpytest_subprocess("--eo").stdout.str(),
        contains_string("tests/test_lid.py:2:5: [ruff:S101]"),
        "a plain assert in tests doesnt fail the gate",
    )


def test_passes_a_test_written_with_hamcrest(pytester: pytest.Pytester) -> None:
    pytester.makepyprojecttoml('[tool.eo]\npaths = ["tests"]\n')
    (pytester.path / "tests").mkdir()
    (pytester.path / "tests" / "__init__.py").write_text('"""Tests."""\n')
    (pytester.path / "tests" / "test_rope.py").write_text(
        "from hamcrest import assert_that, has_length\n\n\n"
        "def test_rope() -> None:\n"
        '    assert_that("rope", has_length(4), "the rope isnt four long")\n',
    )
    assert_that(
        pytester.runpytest_subprocess("--eo").parseoutcomes(),
        equal_to({"passed": 6}),
        "a test written with hamcrest doesnt pass every tool and itself",
    )


def test_refuses_to_suppress_the_ban_on_mocks_file_wide(
    pytester: pytest.Pytester,
) -> None:
    result = project(
        pytester,
        "# ruff: file-ignore[banned-api] - the whole module is legacy\n"
        '"""A package that sneaks a mock in for the whole file."""\n\n'
        "from unittest import mock\n\n"
        '__all__ = ["mock"]\n',
    ).runpytest_subprocess("--eo")
    assert_that(
        result.stdout.str(),
        contains_string("tidy/box.py:1:1: [suppressions:SUP003]"),
        "a file-wide ruff suppression doesnt fail the gate",
    )


def test_refuses_to_switch_flake8_off_for_a_file(
    pytester: pytest.Pytester,
) -> None:
    result = project(
        pytester,
        "# flake8: noqa\n"
        '"""A package that hides a mutable class from flake8."""\n\n\n'
        "class Box:\n"
        '    """A box."""\n',
    ).runpytest_subprocess("--eo")
    assert_that(
        result.stdout.str(),
        contains_string("tidy/box.py:1:1: [suppressions:SUP003]"),
        "a file-wide flake8 noqa doesnt fail the gate",
    )


def test_reports_a_tool_that_cannot_run(pytester: pytest.Pytester) -> None:
    pytester.makepyprojecttoml('[tool.eo]\npaths = ["nowhere"]\n')
    assert_that(
        pytester.runpytest_subprocess("--eo").stdout.str(),
        contains_string("tool failure: mypy exited with 2"),
        "a tool that cannot run isnt reported as a tool failure",
    )


def test_reports_a_file_that_isnt_utf8(pytester: pytest.Pytester) -> None:
    pytester.makepyprojecttoml('[tool.eo]\npaths = ["src"]\n')
    (pytester.path / "src").mkdir()
    (pytester.path / "src" / "latin.py").write_bytes(b'name = "caf\xe9"\n')
    assert_that(
        pytester.runpytest_subprocess("--eo").stdout.str(),
        contains_string("'utf-8' codec can't decode byte 0xe9"),
        "a file that isnt utf-8 doesnt fail the suppression check loudly",
    )
