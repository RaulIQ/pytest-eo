import ast

from hamcrest import assert_that, equal_to

from pytest_eo.edges import Edges


def test_borders_a_definition_with_its_decorators() -> None:
    assert_that(
        tuple(
            Edges(
                ast.parse("import re\n\n\n\ndef vole():\n    return 0\n").body[
                    1
                ],
                (
                    ast.Name("slow", lineno=3, col_offset=1),
                    ast.Name("cache", lineno=4, col_offset=1),
                ),
            ),
        ),
        equal_to((2, 7)),
        "a definition isnt bordered above its decorators",
    )
