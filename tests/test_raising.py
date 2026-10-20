import ast

from hamcrest import assert_that

from pytest_eo.raising import Raising


def test_sees_pytest_raises() -> None:
    assert_that(
        Raising().visit(
            ast.parse("with pytest.raises(KeyError):\n    print(4)").body[0],
        ),
        "a block under pytest.raises isnt seen as raising",
    )


def test_ignores_another_context() -> None:
    assert_that(
        not Raising().visit(
            ast.parse("with open('m.txt') as f:\n    print(f)").body[0],
        ),
        "a block under another context isnt told apart",
    )


def test_ignores_pytest_raises_among_other_contexts() -> None:
    assert_that(
        not Raising().visit(
            ast.parse(
                "with pytest.raises(OSError), open('q'):\n    print(1)",
            ).body[0],
        ),
        "pytest.raises among other contexts isnt refused",
    )
