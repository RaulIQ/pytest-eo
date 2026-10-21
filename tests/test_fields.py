import ast

from hamcrest import assert_that, empty, equal_to

from pytest_eo.fields import Fields


def test_names_an_annotated_field() -> None:
    assert_that(
        Fields().visit(ast.parse("plum: str").body[0]),
        equal_to(("plum",)),
        "an annotated field isnt named",
    )


def test_names_nothing_for_a_class_variable() -> None:
    assert_that(
        Fields().visit(ast.parse("plums: ClassVar[int] = 3").body[0]),
        empty(),
        "a class variable isnt left out",
    )


def test_names_the_attributes_set_in_the_constructor() -> None:
    assert_that(
        Fields().visit(
            ast.parse(
                "def __init__(self, a, b):\n"
                "    self.pear = a\n"
                "    if b:\n"
                "        self.quince = b\n",
            ).body[0],
        ),
        equal_to(("pear", "quince")),
        "the attributes set in the constructor arent named",
    )


def test_names_nothing_for_another_method() -> None:
    assert_that(
        Fields().visit(
            ast.parse("def ripen(self):\n    self.fig = 1\n").body[0],
        ),
        empty(),
        "an attribute set outside the constructor isnt left out",
    )
