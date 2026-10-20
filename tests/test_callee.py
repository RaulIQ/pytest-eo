import ast

from hamcrest import assert_that, equal_to

from pytest_eo.callee import Callee


def test_names_the_function_a_call_goes_to() -> None:
    assert_that(
        Callee().visit(ast.parse("kiwi.peel(3, rind=8)", mode="eval").body),
        equal_to("kiwi.peel"),
        "the function of a call isnt named",
    )


def test_names_nothing_for_a_node_that_isnt_a_call() -> None:
    assert_that(
        Callee().visit(ast.parse("kiwi.peel", mode="eval").body),
        equal_to(""),
        "a node that isnt a call doesnt stay nameless",
    )
