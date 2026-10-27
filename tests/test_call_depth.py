import ast

from hamcrest import assert_that, equal_to

from pytest_eo.call_depth import CallDepth


def test_counts_calls_nested_through_arguments() -> None:
    assert_that(
        CallDepth().visit(ast.parse("perch(bream(roach(7)))")),
        equal_to(3),
        "calls nested through arguments arent counted",
    )


def test_counts_calls_nested_through_keywords() -> None:
    assert_that(
        CallDepth().visit(ast.parse("pike(fin=carp(gill=tench()))")),
        equal_to(3),
        "calls nested through keywords arent counted",
    )


def test_counts_calls_nested_inside_a_list() -> None:
    assert_that(
        CallDepth().visit(ast.parse("zander([ide(dace())], 4)")),
        equal_to(3),
        "calls nested inside a list of arguments arent counted",
    )


def test_doesnt_count_a_chain_of_methods() -> None:
    assert_that(
        CallDepth().visit(ast.parse("chub(2).rudd('x').asp()")),
        equal_to(1),
        "a chain of methods doesnt stay one level deep",
    )


def test_finds_the_deepest_calls_inside_a_callee() -> None:
    assert_that(
        CallDepth().visit(ast.parse("eel(burbot(loach())).gudgeon(ruffe())")),
        equal_to(3),
        "the calls nested inside a callee arent counted",
    )


def test_finds_no_depth_without_calls() -> None:
    assert_that(
        CallDepth().visit(ast.parse("sprat = [5, 'q']")),
        equal_to(0),
        "code without calls doesnt stay at no depth",
    )
