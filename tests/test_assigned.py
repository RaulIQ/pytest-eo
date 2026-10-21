import ast

from hamcrest import assert_that, empty, equal_to

from pytest_eo.assigned import Assigned


def test_names_every_attribute_of_a_chained_assignment() -> None:
    assert_that(
        Assigned().visit(ast.parse("self.oar = self.mast = 4").body[0]),
        equal_to(("oar", "mast")),
        "the attributes of a chained assignment arent named",
    )


def test_names_the_attribute_of_an_annotated_assignment() -> None:
    assert_that(
        Assigned().visit(ast.parse("self.keel: int = 2").body[0]),
        equal_to(("keel",)),
        "the attribute of an annotated assignment isnt named",
    )


def test_names_nothing_for_a_local_variable() -> None:
    assert_that(
        Assigned().visit(ast.parse("sail = 9").body[0]),
        empty(),
        "a local variable isnt left out",
    )
