import ast

from hamcrest import assert_that, empty, equal_to

from pytest_eo.owned import Owned


def test_names_an_attribute_of_self() -> None:
    assert_that(
        Owned().visit(ast.parse("self.wick", mode="eval").body),
        equal_to(("wick",)),
        "an attribute of self isnt named",
    )


def test_names_every_attribute_of_self_in_a_tuple() -> None:
    assert_that(
        Owned().visit(
            ast.parse("self.wax, rope, self.flame", mode="eval").body
        ),
        equal_to(("wax", "flame")),
        "the attributes of self in a tuple arent named",
    )


def test_names_nothing_for_an_attribute_of_another_object() -> None:
    assert_that(
        Owned().visit(ast.parse("lamp.wick", mode="eval").body),
        empty(),
        "an attribute of another object isnt left out",
    )
