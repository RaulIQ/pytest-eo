import ast

from hamcrest import assert_that, equal_to

from pytest_eo.edges import Edges


def test_borders_a_function_with_its_decorators() -> None:
    assert_that(
        tuple(
            Edges(
                ast.FunctionDef(
                    "vole",
                    ast.arguments(),
                    [ast.Pass(lineno=6, col_offset=4)],
                    [
                        ast.Name("slow", lineno=3, col_offset=1),
                        ast.Name("cache", lineno=4, col_offset=1),
                    ],
                    lineno=5,
                    col_offset=0,
                    end_lineno=6,
                ),
            ),
        ),
        equal_to((2, 7)),
        "a function isnt bordered above its decorators",
    )
