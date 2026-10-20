import ast

from hamcrest import assert_that, empty, equal_to

from pytest_eo.final_assertion import FinalAssertion


def test_passes_a_test_that_ends_with_its_only_assertion() -> None:
    assert_that(
        tuple(
            FinalAssertion(
                ast.parse("def test_gum():\n    assert 3, 'no gum'\n"),
            ).problems(),
        ),
        empty(),
        "a test that ends with its only assertion doesnt pass",
    )


def test_reports_where_a_test_without_assertions_starts() -> None:
    assert_that(
        tuple(
            FinalAssertion(
                ast.parse("import os\n\n\ndef test_tar():\n    print(os)\n"),
            ).problems(),
        ),
        equal_to(((4, 0, "TST100 test must end with its only assertion"),)),
        "a test without assertions isnt reported where it starts",
    )
