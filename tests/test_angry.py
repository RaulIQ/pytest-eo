import ast

from pytest_eo.angry import AngryTests


def codes(code: str, filename: str) -> tuple[str, ...]:
    return tuple(
        found[2].split()[0]
        for found in AngryTests(ast.parse(code), filename).run()
    )


def test_passes_a_test_that_ends_with_its_only_assertion() -> None:
    code = "def test_sum():\n    total = 2 + 3\n    assert total == 5\n"
    assert codes(code, "tests/test_sum.py") == (), (
        "a test with one final assertion doesnt pass"
    )


def test_reports_a_test_with_two_assertions() -> None:
    code = "def test_pair():\n    assert 1 == 1\n    assert 2 == 2\n"
    assert codes(code, "tests/test_pair.py") == ("TST100",), (
        "a test with two assertions doesnt fail"
    )


def test_reports_a_test_whose_assertion_is_not_last() -> None:
    code = "def test_order():\n    assert len('ab') == 2\n    print('ab')\n"
    assert codes(code, "tests/test_order.py") == ("TST100",), (
        "a test with its assertion before the end doesnt fail"
    )


def test_reports_a_test_without_assertions() -> None:
    code = "def test_nothing():\n    print('silence')\n"
    assert codes(code, "tests/test_nothing.py") == ("TST100",), (
        "a test without assertions doesnt fail"
    )


def test_passes_a_test_that_ends_with_pytest_raises() -> None:
    code = (
        "def test_crash():\n"
        "    with pytest.raises(ZeroDivisionError):\n"
        "        print(7 / 0)\n"
    )
    assert codes(code, "tests/test_crash.py") == (), (
        "a test that ends with pytest.raises doesnt pass"
    )


def test_reports_an_assertion_before_pytest_raises() -> None:
    code = (
        "def test_mixed():\n"
        "    assert 4 > 3\n"
        "    with pytest.raises(KeyError):\n"
        "        print({}['q'])\n"
    )
    assert codes(code, "tests/test_mixed.py") == ("TST100",), (
        "an assertion before pytest.raises doesnt fail"
    )


def test_reports_a_test_method_of_a_test_class() -> None:
    code = "class TestBox:\n    def test_lid(self):\n        print('open')\n"
    assert codes(code, "tests/test_box.py") == ("TST100",), (
        "a test method without assertions doesnt fail"
    )


def test_reports_the_line_of_the_test() -> None:
    code = "import os\n\n\ndef test_env():\n    print(os.sep)\n"
    assert next(AngryTests(ast.parse(code), "test_env.py").run())[0] == 4, (
        "the problem isnt reported on the line of the test"
    )


def test_checks_a_file_named_like_a_suffixed_test() -> None:
    code = "def test_tail():\n    print('tail')\n"
    assert codes(code, "src/tail_test.py") == ("TST100",), (
        "a file ending in _test.py isnt checked"
    )


def test_ignores_a_file_that_holds_no_tests() -> None:
    code = "def test_like():\n    print('helper')\n"
    assert codes(code, "src/likeness.py") == (), (
        "a file that isnt a test file is checked"
    )


def test_ignores_a_helper_of_a_test_file() -> None:
    code = "def source(text):\n    print(text)\n    return text\n"
    assert codes(code, "tests/test_source.py") == (), (
        "a helper of a test file is checked as a test"
    )
