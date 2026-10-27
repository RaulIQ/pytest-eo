import ast

from hamcrest import assert_that, empty, equal_to

from pytest_eo.nested_calls import NestedCalls


def test_reports_calls_nested_past_the_limit() -> None:
    assert_that(
        tuple(
            NestedCalls(
                ast.parse("gannet = tern(skua(auk(puffin())))"), 2
            ).problems(),
        ),
        equal_to(
            (
                (
                    1,
                    9,
                    (
                        "NST100 expression must not nest more than 2 calls "
                        "inside each other, found 4"
                    ),
                ),
            ),
        ),
        "calls nested past the limit arent reported",
    )


def test_passes_calls_nested_up_to_the_limit() -> None:
    assert_that(
        tuple(NestedCalls(ast.parse("loon(grebe(diver()))"), 3).problems()),
        empty(),
        "calls nested up to the limit dont pass",
    )


def test_reports_a_chain_of_methods_once() -> None:
    assert_that(
        len(
            tuple(
                NestedCalls(
                    ast.parse("rail(coot(crake())).moorhen(snipe(curlew()))"),
                    1,
                ).problems(),
            ),
        ),
        equal_to(1),
        "a chain of methods isnt reported once",
    )


def test_reports_calls_inside_a_function() -> None:
    assert_that(
        tuple(
            (line, column)
            for line, column, _ in NestedCalls(
                ast.parse("def plover():\n    return dunlin(knot(ruff()))\n"),
                2,
            ).problems()
        ),
        equal_to(((2, 11),)),
        "calls nested inside a function arent reported",
    )
