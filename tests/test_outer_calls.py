import ast

from hamcrest import assert_that, equal_to

from pytest_eo.outer_calls import OuterCalls


def test_finds_the_calls_no_other_call_holds() -> None:
    assert_that(
        tuple(
            (call.lineno, call.col_offset)
            for call in OuterCalls().visit(
                ast.parse("hake = cod(ling(3))\nif pollock:\n    tusk(9)\n"),
            )
        ),
        equal_to(((1, 7), (3, 4))),
        "the calls that no other call holds arent found",
    )


def test_finds_a_chain_of_methods_once() -> None:
    assert_that(
        len(OuterCalls().visit(ast.parse("whiting(1).pout(2).haddock()"))),
        equal_to(1),
        "a chain of methods isnt found as one call",
    )
