import ast

from hamcrest import assert_that, empty, equal_to

from pytest_eo.margin import Margin


def test_finds_the_rows_around_a_decorated_function() -> None:
    assert_that(
        Margin().visit(
            ast.parse(
                "x = 7\n\n@cache\ndef moth():\n    return 3\n\ny = x\n",
            ).body[1],
        ),
        equal_to((2, 6)),
        "the rows around a decorated function arent found",
    )


def test_finds_the_rows_around_a_coroutine() -> None:
    assert_that(
        Margin().visit(
            ast.parse("pass\n\nasync def gnat():\n    await fly()\n").body[1],
        ),
        equal_to((2, 5)),
        "the rows around a coroutine arent found",
    )


def test_finds_the_rows_around_a_class() -> None:
    assert_that(
        Margin().visit(
            ast.parse("\n\nclass Wasp:\n    sting: int\n").body[0],
        ),
        equal_to((2, 5)),
        "the rows around a class arent found",
    )


def test_finds_nothing_around_a_statement() -> None:
    assert_that(
        Margin().visit(ast.parse("print(9)\n").body[0]),
        empty(),
        "a statement isnt left without margins",
    )
