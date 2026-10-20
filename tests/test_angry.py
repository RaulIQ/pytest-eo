import ast

from hamcrest import assert_that, empty, equal_to

from pytest_eo.angry import AngryTests


def codes(code: str, filename: str) -> tuple[str, ...]:
    return tuple(
        found[2].split()[0]
        for found in AngryTests(ast.parse(code), filename).run()
    )


def test_passes_a_test_that_ends_with_its_only_assertion() -> None:
    code = (
        "def test_sum():\n    total = 2 + 3\n    assert total == 5, 'no five'\n"
    )
    assert_that(
        codes(code, "tests/test_sum.py"),
        empty(),
        "a test with one final assertion doesnt pass",
    )


def test_reports_a_test_with_two_assertions() -> None:
    code = "def test_pair():\n    assert 1, 'no one'\n    assert 2, 'no two'\n"
    assert_that(
        codes(code, "tests/test_pair.py"),
        equal_to(("TST100",)),
        "a test with two assertions doesnt fail",
    )


def test_reports_a_test_whose_assertion_is_not_last() -> None:
    code = "def test_order():\n    assert 'ab', 'no ab'\n    print('ab')\n"
    assert_that(
        codes(code, "tests/test_order.py"),
        equal_to(("TST100",)),
        "a test with its assertion before the end doesnt fail",
    )


def test_reports_a_test_without_assertions() -> None:
    code = "def test_nothing():\n    print('silence')\n"
    assert_that(
        codes(code, "tests/test_nothing.py"),
        equal_to(("TST100",)),
        "a test without assertions doesnt fail",
    )


def test_passes_a_test_that_ends_with_pytest_raises() -> None:
    code = (
        "def test_crash():\n"
        "    with pytest.raises(ZeroDivisionError):\n"
        "        print(7 / 0)\n"
    )
    assert_that(
        codes(code, "tests/test_crash.py"),
        empty(),
        "a test that ends with pytest.raises doesnt pass",
    )


def test_reports_an_assertion_before_pytest_raises() -> None:
    code = (
        "def test_mixed():\n"
        "    assert 4 > 3, 'four isnt bigger'\n"
        "    with pytest.raises(KeyError):\n"
        "        print({}['q'])\n"
    )
    assert_that(
        codes(code, "tests/test_mixed.py"),
        equal_to(("TST100",)),
        "an assertion before pytest.raises doesnt fail",
    )


def test_reports_a_test_method_of_a_test_class() -> None:
    code = "class TestBox:\n    def test_lid(self):\n        print('open')\n"
    assert_that(
        codes(code, "tests/test_box.py"),
        equal_to(("TST100",)),
        "a test method without assertions doesnt fail",
    )


def test_reports_the_line_of_the_test() -> None:
    code = "import os\n\n\ndef test_env():\n    print(os.sep)\n"
    assert_that(
        next(AngryTests(ast.parse(code), "test_env.py").run())[0],
        equal_to(4),
        "the problem isnt reported on the line of the test",
    )


def test_checks_a_file_named_like_a_suffixed_test() -> None:
    code = "def test_tail():\n    print('tail')\n"
    assert_that(
        codes(code, "src/tail_test.py"),
        equal_to(("TST100",)),
        "a file ending in _test.py isnt checked",
    )


def test_ignores_a_file_that_holds_no_tests() -> None:
    code = "def test_like():\n    print('helper')\n"
    assert_that(
        codes(code, "src/likeness.py"),
        empty(),
        "a file that isnt a test file is checked",
    )


def test_ignores_a_helper_of_a_test_file() -> None:
    code = "def source(text):\n    print(text)\n    return text\n"
    assert_that(
        codes(code, "tests/test_source.py"),
        empty(),
        "a helper of a test file isnt left alone",
    )


def test_reports_a_constant_of_a_test_module() -> None:
    assert_that(
        codes("REPORT = 'a.py:1:1: E1 oops'\n", "tests/test_report.py"),
        equal_to(("TST200",)),
        "a constant of a test module doesnt fail",
    )


def test_reports_an_annotated_constant_of_a_test_module() -> None:
    assert_that(
        codes("LIMIT: int = 17\n", "tests/test_limit.py"),
        equal_to(("TST200",)),
        "an annotated constant of a test module doesnt fail",
    )


def test_passes_the_plugins_of_a_test_module() -> None:
    assert_that(
        codes("pytest_plugins = ['pytester']\n", "test_kit.py"),
        empty(),
        "pytest_plugins of a test module doesnt pass",
    )


def test_passes_a_variable_inside_a_test() -> None:
    code = "def test_word():\n    word = 'qx'\n    assert word, 'no word'\n"
    assert_that(
        codes(code, "tests/test_word.py"),
        empty(),
        "a variable inside a test doesnt pass",
    )


def test_ignores_a_constant_of_a_module_without_tests() -> None:
    assert_that(
        codes("TIMEOUT = 9.5\n", "tests/fakes.py"),
        empty(),
        "a constant of a module without tests isnt ignored",
    )


def test_reports_the_line_of_the_constant() -> None:
    code = "import os\n\nROOT = os.sep\n"
    assert_that(
        next(AngryTests(ast.parse(code), "test_root.py").run())[0],
        equal_to(3),
        "the constant isnt reported on its own line",
    )


def test_reports_an_assertion_without_a_message() -> None:
    code = "def test_bare():\n    assert 'ab'.isalpha()\n"
    assert_that(
        codes(code, "tests/test_bare.py"),
        equal_to(("TST300",)),
        "an assertion without a message doesnt fail",
    )


def test_reports_a_message_that_isnt_negative() -> None:
    code = "def test_glad():\n    assert 6 > 5, 'six beats five'\n"
    assert_that(
        codes(code, "tests/test_glad.py"),
        equal_to(("TST300",)),
        "a message without a negation doesnt fail",
    )


def test_passes_a_message_spelled_without_an_apostrophe() -> None:
    code = "def test_lamp():\n    assert 'on', 'the lamp doesnt glow'\n"
    assert_that(
        codes(code, "tests/test_lamp.py"),
        empty(),
        "a negative message without an apostrophe doesnt pass",
    )


def test_passes_a_negative_formatted_message() -> None:
    code = "def test_cup(cup):\n    assert cup, f'{cup} cannot hold tea'\n"
    assert_that(
        codes(code, "tests/test_cup.py"),
        empty(),
        "a negative formatted message doesnt pass",
    )


def test_reports_a_message_held_in_a_variable() -> None:
    code = "def test_box(text):\n    assert len(text) == 2, text\n"
    assert_that(
        codes(code, "tests/test_box.py"),
        equal_to(("TST300",)),
        "a message that cannot be read doesnt fail",
    )


def test_reports_the_line_of_the_assertion() -> None:
    code = "def test_gap():\n    gap = 3\n    assert gap == 3\n"
    assert_that(
        next(AngryTests(ast.parse(code), "test_gap.py").run())[0],
        equal_to(3),
        "the assertion isnt reported on its own line",
    )


def test_passes_a_test_that_ends_with_its_only_matcher() -> None:
    code = (
        "def test_sum():\n"
        "    assert_that(2 + 3, equal_to(5), 'the sum isnt five')\n"
    )
    assert_that(
        codes(code, "tests/test_sum.py"),
        empty(),
        "a test with one final matcher doesnt pass",
    )


def test_reports_a_test_with_two_matchers() -> None:
    code = (
        "def test_pair():\n"
        "    assert_that(1, equal_to(1), 'one isnt one')\n"
        "    assert_that(2, equal_to(2), 'two isnt two')\n"
    )
    assert_that(
        codes(code, "tests/test_pair.py"),
        equal_to(("TST100",)),
        "a test with two matchers doesnt fail",
    )


def test_passes_a_qualified_matcher() -> None:
    code = (
        "def test_cap():\n"
        "    hamcrest.assert_that('q', has_length(1), 'q isnt one letter')\n"
    )
    assert_that(
        codes(code, "tests/test_cap.py"),
        empty(),
        "a matcher called through its module doesnt pass",
    )


def test_reports_a_matcher_without_a_reason() -> None:
    code = "def test_mute():\n    assert_that(9, greater_than(4))\n"
    assert_that(
        codes(code, "tests/test_mute.py"),
        equal_to(("TST300",)),
        "a matcher without a reason doesnt fail",
    )


def test_reports_a_matcher_with_a_reason_that_isnt_negative() -> None:
    code = "def test_ok():\n    assert_that(7, equal_to(7), 'seven is seven')\n"
    assert_that(
        codes(code, "tests/test_ok.py"),
        equal_to(("TST300",)),
        "a matcher with a positive reason doesnt fail",
    )


def test_passes_a_negative_reason_given_by_keyword() -> None:
    code = (
        "def test_key():\n"
        "    assert_that('k', has_length(1), reason='the key cannot be long')\n"
    )
    assert_that(
        codes(code, "tests/test_key.py"),
        empty(),
        "a negative reason given by keyword doesnt pass",
    )
