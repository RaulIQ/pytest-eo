import ast

from hamcrest import assert_that, empty, equal_to

from pytest_eo.module_constants import ModuleConstants


def test_reports_where_a_constant_stands() -> None:
    assert_that(
        tuple(
            ModuleConstants(ast.parse("import os\nSEP = os.sep\n")).problems()
        ),
        equal_to(
            (
                (
                    2,
                    0,
                    (
                        "TST200 test module must not share constants between "
                        "its tests"
                    ),
                ),
            ),
        ),
        "a constant isnt reported where it stands",
    )


def test_ignores_a_variable_inside_a_function() -> None:
    assert_that(
        tuple(
            ModuleConstants(
                ast.parse("def test_ink():\n    ink = 4\n    print(ink)\n"),
            ).problems(),
        ),
        empty(),
        "a variable inside a function isnt ignored",
    )
